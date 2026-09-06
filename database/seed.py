"""元カタログと試作レシピを正規化テーブルへ再実行可能に投入する。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import defaultdict
from collections.abc import Sequence
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, cast
from uuid import NAMESPACE_URL, UUID, uuid5

import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

ROOT = Path(__file__).resolve().parents[1]
SEED_VERSION = "catalog-2026-09-v3-relational-1"
NORMALIZER_VERSION = "reviewed-v3"
SEED_AT = "2026-09-06T00:00:00+00:00"
Row = dict[str, Any]
Rows = dict[str, list[Row]]


def stable_id(table: str, key: str) -> str:
    """外部入力の固定コードから再現できるUUIDを採番する。"""
    return str(uuid5(NAMESPACE_URL, f"https://recipeweave.example/seed/{table}/{key}"))


def user_id(subject: str) -> str:
    """認証プロバイダと同じ利用者ID規則を使う。"""
    return str(uuid5(NAMESPACE_URL, "recipeweave:user:" + subject))


def canonical(value: Any) -> str:
    """ハッシュと投入差分検査に使う決定的なJSONを作る。"""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def load(path: str) -> Any:
    return json.loads((ROOT / path).read_text())


class SeedBuilder:
    """投入データを外部入力と明示的な補足から組み立てる。"""

    def __init__(self) -> None:
        self.rows: Rows = defaultdict(list)
        self.ids: set[tuple[str, str]] = set()
        self.release_id = stable_id("catalog_release", SEED_VERSION)
        self.catalog = load("spec/database/catalog-source-sheet.json")
        self.foods: list[Row] = load("data/catalog/source_foods.json")
        self.mappings: list[Row] = load("database/seed_data/legacy_food_mapping.json")
        self.samples: list[Row] = load("data/samples/recipes.json")
        self.food_codes = {row["legacyId"]: row["foodCode"] for row in self.mappings}
        self.forms: dict[str, str] = {}
        self.food_names: dict[str, str] = {}
        self.identities: dict[str, str] = {}
        self.options: dict[tuple[str, str], str] = {}

    def add(self, table: str, key: str, **values: Any) -> str:
        identifier = stable_id(table, key)
        if (table, identifier) in self.ids:
            raise ValueError(f"初期データのIDが重複しています: {table}/{key}")
        self.ids.add((table, identifier))
        self.rows[table].append({"id": identifier, **values})
        return identifier

    def option(self, axis: str, code: str, label: str, definition: str = "") -> str:
        key = (axis, code)
        if key not in self.options:
            self.options[key] = self.add(
                "axis_option",
                f"{axis}/{code}",
                axis_id=stable_id("axis", axis),
                code=code,
                label=label,
                definition=definition or label,
                parent_id=None,
                status="active",
            )
        return self.options[key]

    def extra_axis(self, code: str, name: str, purpose: str = "presentation") -> None:
        self.add(
            "axis",
            code,
            code=code,
            name=name,
            purpose=purpose,
            selection="multiple",
            release_id=self.release_id,
            status="active",
        )

    def base(self) -> None:
        self.add(
            "source_record",
            "catalog",
            title="RecipeWeave 食材・組み合わせカタログ",
            url=self.catalog["sourceUrl"],
            locator="1005食品・68軸・924候補値",
            retrieved_at=SEED_AT,
            content_hash=sha(self.catalog),
            license_note="利用者が作成したカタログ定義。個別商品の権利・仕様は未調査。",
        )
        self.add(
            "source_record",
            "samples",
            title="RecipeWeave 初期レシピの登録原稿",
            url=None,
            locator="data/samples/recipes.json",
            retrieved_at=SEED_AT,
            content_hash=sha(self.samples),
            license_note="開発用登録原稿。調理・食味の試作未実施。公開審査済みではない。",
        )
        self.add(
            "catalog_release",
            SEED_VERSION,
            version=SEED_VERSION,
            manifest_hash=sha(
                {"catalog": self.catalog, "foods": self.foods, "mappings": self.mappings}
            ),
            published_at=None,
        )
        units = [
            ("g", "グラム", "mass", 1),
            ("kg", "キログラム", "mass", 1000),
            ("ml", "ミリリットル", "volume", 1),
            ("l", "リットル", "volume", 1000),
            ("個", "個", "count", 1),
            ("人前", "人前", "count", 1),
            ("s", "秒", "time", 1),
            ("min", "分", "time", 60),
            ("℃", "摂氏", "temperature", 1),
            ("mm", "ミリメートル", "length", 1),
            ("cm", "センチメートル", "length", 10),
            ("W", "ワット", "power", 1),
        ]
        for code, name, dimension, factor in units:
            self.add(
                "unit",
                code,
                code=code,
                name=name,
                dimension=dimension,
                factor=factor,
                offset=0,
                status="active",
            )
        for name in ("alice", "bob", "admin"):
            subject = "local:" + name
            self.rows["app_user"].append(
                {
                    "id": user_id(subject),
                    "auth_subject": subject,
                    "state": "active",
                    "locale": "ja",
                    "timezone": "Asia/Tokyo",
                }
            )

    def axes(self) -> None:
        tabs = self.catalog["tabs"]
        for code, name, purpose, selection, *_ in tabs["01_新組合せ軸"][1:]:
            self.add(
                "axis",
                code,
                code=code,
                name=name,
                purpose=purpose,
                selection=selection,
                release_id=self.release_id,
                status="active",
            )
        for axis, code, label, definition, *_ in tabs["03_軸候補全値"][1:]:
            self.option(axis, code, label, definition)
        for code, name, purpose in [
            ("store_category", "売場カテゴリ", "search"),
            ("bootstrap_tag", "初期レシピの特徴", "search"),
            ("storage_location", "保管場所", "presentation"),
            ("pantry_default", "常備品の初期表示", "presentation"),
        ]:
            self.extra_axis(code, name, purpose)

    def food_catalog(self) -> None:
        source = self.catalog["tabs"]["02_食材カタログ"][1:]
        if {row[0] for row in source} != {row["id"] for row in self.foods}:
            raise ValueError("Google Sheetsと食品入力のID集合が一致しません")
        expected = [
            [
                r[k]
                for k in (
                    "id",
                    "name",
                    "category",
                    "kind",
                    "state",
                    "unit",
                    "availability",
                    "role",
                    "note",
                    "stage",
                    "source",
                )
            ]
            for r in self.foods
        ]
        if source != expected:
            raise ValueError("Google Sheetsと食品入力の内容が一致しません")
        food_rows = [*self.foods, *(x["definition"] for x in self.mappings if x["definition"])]
        for row in food_rows:
            code = row["id"]
            self.food_names[code] = row["name"]
            food = self.add(
                "food",
                code,
                code=code,
                name=row["name"],
                kind=row["kind"],
                parent_id=None,
                release_id=self.release_id,
                status="active",
            )
            self.forms[code] = self.add(
                "food_form",
                code + "/standard",
                food_id=food,
                name="標準",
                state=row["state"],
                base_unit_id=stable_id("unit", row["unit"]),
                quantity_basis="as_purchased",
                status="active",
            )
            category = self.option("store_category", row["category"], row["category"])
            self.add("food_axis_option", f"{code}/category", food_id=food, option_id=category)
            availability = self.option(
                "availability",
                {
                    "common": "availability_001",
                    "seasonal": "availability_002",
                    "store_dependent": "availability_003",
                }[row["availability"]],
                {
                    "common": "一般スーパー想定",
                    "seasonal": "季節依存",
                    "store_dependent": "店舗依存",
                }[row["availability"]],
            )
            self.add(
                "food_axis_option", f"{code}/availability", food_id=food, option_id=availability
            )
        sample_foods = {r["id"]: r for r in load("data/samples/foods.json")}
        for row in self.mappings:
            code = row["foodCode"]
            sample = sample_foods[row["legacyId"]]
            for alias in sorted(set([sample["name"], *row["aliases"]])):
                self.add(
                    "food_alias",
                    f"{code}/{alias}",
                    food_id=stable_id("food", code),
                    alias=alias,
                    locale="ja",
                )
            for axis, value in [
                ("storage_location", sample["location"]),
                ("pantry_default", str(sample["pantry"]).lower()),
            ]:
                option = self.option(axis, value, value)
                self.add(
                    "food_axis_option",
                    f"{code}/{axis}",
                    food_id=stable_id("food", code),
                    option_id=option,
                )
        normalization = load("data/catalog/normalization.json")
        for row in normalization["identities"]:
            identity = self.add(
                "food_identity",
                row["id"],
                code=row["id"],
                name=row["name"],
                normalizer_version=NORMALIZER_VERSION,
            )
            for code in row["source_ids"]:
                self.identities[code] = identity
                self.add(
                    "food_identity_member",
                    code,
                    food_id=stable_id("food", code),
                    identity_id=identity,
                    normalizer_version=NORMALIZER_VERSION,
                    reason="reviewed-v3の同一性辞書。形態差はfood_formと工程で保持する。",
                )
        for row in self.mappings:
            if row["definition"]:
                code = row["foodCode"]
                identity = self.add(
                    "food_identity",
                    code,
                    code=code,
                    name=row["definition"]["name"],
                    normalizer_version=NORMALIZER_VERSION,
                )
                self.identities[code] = identity
                self.add(
                    "food_identity_member",
                    code,
                    food_id=stable_id("food", code),
                    identity_id=identity,
                    normalizer_version=NORMALIZER_VERSION,
                    reason=row["sourceExplanation"],
                )

    def generation_templates(self) -> None:
        reviewed = load("data/catalog/v3_reviewed.json")
        counts = {
            r["code"]: r["count"]
            for r in load("data/catalog/normalization.json")["counts_by_template"]
        }
        for row in reviewed["blocks"]:
            contract = {
                "schema_version": 2,
                "primary_identity_ids": sorted(
                    stable_id("food_identity", code) for code in row["primary"]
                ),
                "support_identity_ids": sorted(
                    stable_id("food_identity", code) for code in row["supports"]
                ),
                "support_k": sorted(row["k"]),
                "flavor_codes": sorted(row["flavors"]),
                "route_codes": sorted(row["routes"]),
                "normalizer_version": NORMALIZER_VERSION,
            }
            if "support_sets" in row:
                contract["support_identity_sets"] = [
                    sorted(stable_id("food_identity", code) for code in group)
                    for group in row["support_sets"]
                ]
            self.add(
                "generation_template",
                row["code"],
                code=row["code"],
                version=3,
                release_id=self.release_id,
                contract=contract,
                candidate_count=counts[row["code"]],
                contract_hash=sha(contract),
            )

    def operations(self) -> None:
        for code, name, precondition, parameters, cue, *_ in self.catalog["tabs"][
            "04_標準工程と媒体"
        ][1:]:
            self.add(
                "operation",
                code,
                code=code,
                name=name,
                definition=name,
                precondition=precondition,
                completion_cue=cue,
                status="active",
            )
            for parameter in parameters.split(";"):
                match = re.match(r"(\w+):(decimal|integer|option)", parameter)
                if match is None:
                    raise ValueError(f"標準動作パラメータが解析できません: {parameter}")
                field, value_type = match.groups()
                options = re.search(r"\[([a-z,]+)\]", parameter)
                unit = (
                    "mm"
                    if field.endswith("_mm")
                    else "s"
                    if field.endswith("_s")
                    else ("W" if field.endswith("_w") else "ml" if field.endswith("_ml") else None)
                )
                interval = re.search(r"\(([\d.]+)\.\.([\d.]+)\)", parameter)
                self.add(
                    "operation_parameter",
                    f"{code}/{field}",
                    operation_id=stable_id("operation", code),
                    code=field,
                    name={
                        "thickness_mm": "厚さ",
                        "width_mm": "幅",
                        "length_mm": "長さ",
                        "size_mm": "粒の大きさ",
                        "method": "洗い方",
                        "duration_s": "時間",
                        "heat": "火加減",
                        "power_w": "出力",
                        "water_ml": "湯量",
                        "fraction": "使用割合",
                        "target_capacity_ml": "移し替え先の容量",
                        "portion_count": "盛付け数",
                    }[field],
                    value_type=value_type,
                    unit_id=stable_id("unit", unit) if unit else None,
                    required=False,
                    min_value=Decimal(interval[1])
                    if interval
                    else 0
                    if value_type != "option"
                    else None,
                    max_value=Decimal(interval[2])
                    if interval
                    else 1
                    if field == "fraction"
                    else None,
                    allowed_values=options[1].split(",") if options else None,
                )
        for code, name in [
            ("prepare", "材料を準備する"),
            ("cut_wedge", "くし形切り"),
            ("cut_cube", "角切り"),
            ("cut_rough", "ざく切り"),
            ("label_prepare", "商品表示に従って準備する"),
            ("label_wait", "商品表示の戻し時間を確認する"),
        ]:
            self.add(
                "operation",
                code,
                code=code,
                name=name,
                definition=name,
                precondition="原稿に示した材料・商品表示を確認する。",
                completion_cue="個別工程の完了条件を確認する。",
                status="active",
            )
        for code, name, unit in [
            ("pan", "フライパン", "ml"),
            ("knife", "包丁", None),
            ("pot", "鍋", "ml"),
            ("microwave", "電子レンジ", "W"),
            ("kettle", "ケトル", "ml"),
            ("person", "作業者", None),
            ("bowl", "ボウル", "ml"),
            ("burner", "コンロ", None),
        ]:
            self.add(
                "resource_type",
                code,
                code=code,
                name=name,
                capacity_unit_id=stable_id("unit", unit) if unit else None,
                status="active",
            )
        for name in ("alice", "bob", "admin"):
            owner = user_id("local:" + name)
            for resource in self.rows["resource_type"]:
                self.rows["kitchen_resource"].append(
                    {
                        "id": str(uuid5(UUID(owner), "kitchen:" + resource["code"])),
                        "user_id": owner,
                        "resource_type_id": resource["id"],
                        "name": resource["name"],
                        "capacity": None,
                        "quantity": 1,
                    }
                )
        for code, name, mode, maximum in [
            ("ingredient_linear", "初期分量の比例換算（調理試作は未実施）", "linear", 12),
            ("time_manual", "工程時間は人数変更時に再確認", "manual", 2),
        ]:
            self.add(
                "scaling_rule",
                code,
                name=name,
                mode=mode,
                min_servings=1,
                max_servings=maximum,
                batch_capacity=None,
                round_mode="none",
                round_increment=Decimal("0.01"),
                source_id=stable_id("source_record", "samples"),
            )

    def build(self) -> Rows:
        self.base()
        self.axes()
        self.food_catalog()
        self.generation_templates()
        self.operations()
        self.recipes()
        return dict(self.rows)

    def recipes(self) -> None:
        """未試作の原稿を下書きとして保存し、審査を通ったように見せない。"""
        details = load("database/seed_data/recipe_material_flow.json")
        for code, severity, message in [
            ("seed_structure", "block", "初期原稿の数量・参照・工程構造を検査する"),
            ("cooking_trial", "review", "調理・食味の試作結果を記録する"),
        ]:
            self.add(
                "compatibility_rule",
                code,
                code=code,
                version=1,
                severity=severity,
                predicate={
                    "schema_version": 1,
                    "all": [{"field": "recipe.validation", "op": "exists", "value": True}],
                },
                message=message,
                source_id=stable_id("source_record", "samples"),
                status="active",
            )
        for recipe in self.samples:
            key = recipe["id"]
            detail = details[key]
            family = self.option("dish_family", detail["familyCode"], detail["familyName"])
            recipe_id = self.add(
                "recipe",
                key,
                title=recipe["name"],
                family_option_id=family,
                status="draft",
                withdrawal_reason=None,
            )
            version_id = self.add(
                "recipe_version",
                key + "/1",
                recipe_id=recipe_id,
                version=1,
                release_id=self.release_id,
                base_servings=recipe["servings"],
                output_amount=recipe["servings"],
                output_unit_id=stable_id("unit", "人前"),
                status="draft",
                validation="needs_review",
                content_hash=sha(recipe),
                published_at=None,
                description=recipe["description"],
            )
            dish_role = self.option("dish_role", detail["dishRoleCode"], detail["dishRoleName"])
            facets = [family, dish_role]
            for tag in recipe["tags"]:
                facets.append(self.option("bootstrap_tag", tag, tag))
            for option_id in facets:
                self.add(
                    "recipe_option",
                    key + "/" + option_id,
                    recipe_version_id=version_id,
                    option_id=option_id,
                )
            for line_no, ingredient in enumerate(recipe["ingredients"], 1):
                food_code = self.food_codes[ingredient["foodId"]]
                quantity = ingredient["quantity"]
                role = (
                    "medium"
                    if ingredient["foodId"] == "water"
                    else (
                        "seasoning"
                        if ingredient["foodId"] in detail["seasonings"]
                        else "main"
                        if line_no == 1
                        else "support"
                    )
                )
                line_id = self.add(
                    "recipe_ingredient",
                    f"{key}/{line_no}",
                    recipe_version_id=version_id,
                    line_no=line_no,
                    form_id=self.forms[food_code],
                    product_version_id=None,
                    component_id=None,
                    kit_parent_line_id=None,
                    role=role,
                    demand_kind="utility" if role == "medium" else "purchase",
                    amount_mode="exact",
                    amount=quantity["value"],
                    amount_max=None,
                    unit_id=stable_id("unit", quantity["unit"]),
                    canonical_amount=quantity["value"],
                    conversion_id=None,
                    scaling_rule_id=stable_id("scaling_rule", "ingredient_linear"),
                    optional=False,
                    note=ingredient["note"] or None,
                )
                self.add(
                    "material_node",
                    f"{key}/ingredient/{ingredient['foodId']}",
                    recipe_version_id=version_id,
                    name=self.food_names[food_code],
                    kind="ingredient",
                    ingredient_line_id=line_id,
                    producer_step_id=None,
                    amount=quantity["value"],
                    unit_id=stable_id("unit", quantity["unit"]),
                )
            self.recipe_steps(recipe, detail, version_id)
            signature = {
                "schema_version": 1,
                "ingredient_ratios": sorted(
                    [
                        {
                            "form_id": self.forms[self.food_codes[item["foodId"]]],
                            "amount_per_serving": str(
                                Decimal(str(item["quantity"]["value"]))
                                / Decimal(str(recipe["servings"]))
                            ),
                            "unit_id": stable_id("unit", item["quantity"]["unit"]),
                        }
                        for item in recipe["ingredients"]
                    ],
                    key=lambda x: x["form_id"],
                ),
                "operations": [
                    stable_id("operation", step["operation"]) for step in detail["steps"]
                ],
                "parameters": [
                    {
                        "operation_id": stable_id("operation", step["operation"]),
                        "parameter_id": stable_id(
                            "operation_parameter", step["operation"] + "/" + field
                        ),
                        "value": value,
                    }
                    for step in detail["steps"]
                    for field, value in sorted(step.get("parameters", {}).items())
                ],
                "family_id": family,
            }
            self.add(
                "recipe_signature",
                key,
                recipe_version_id=version_id,
                algorithm_version="seed-normalized-v1",
                exact_hash=sha(signature),
                canonical_payload=signature,
                cluster_key=family,
            )
            for rule, state, actual in [
                ("seed_structure", "passed", "初期原稿の数量・参照・材料受渡しを検査"),
                ("cooking_trial", "needs_review", "未試作。調理・食味・商品条件の審査待ち"),
            ]:
                self.add(
                    "validation_result",
                    f"{key}/{rule}",
                    recipe_version_id=version_id,
                    rule_id=stable_id("compatibility_rule", rule),
                    state=state,
                    evidence={
                        "schema_version": 1,
                        "path": key,
                        "expected": "verified",
                        "actual": actual,
                        "source_ids": [stable_id("source_record", "samples")],
                    },
                    validator_version="seed-structural-v1",
                    evaluated_at=SEED_AT,
                )

    def recipe_steps(self, recipe: Row, detail: Row, version_id: str) -> None:
        key = recipe["id"]
        resources = {
            "フライパン": "pan",
            "包丁": "knife",
            "鍋": "pot",
            "電子レンジ": "microwave",
            "ケトル": "kettle",
        }
        for number, (step, flow) in enumerate(
            zip(recipe["steps"], detail["steps"], strict=True), 1
        ):
            step_key = key + "/" + step["id"]
            step_id = self.add(
                "recipe_step",
                step_key,
                recipe_version_id=version_id,
                step_no=number,
                operation_id=stable_id("operation", flow["operation"]),
                instruction=step["instruction"],
                title=step["title"],
                attention="monitored" if step["mode"] == "passive" else "active",
                duration_min_s=step["minutes"] * 60,
                duration_max_s=step["minutes"] * 60,
                scaling_rule_id=stable_id("scaling_rule", "time_manual"),
                completion_cue=flow["completion"],
            )
            for field, value in flow.get("parameters", {}).items():
                self.add(
                    "step_parameter",
                    step_key + "/" + field,
                    step_id=step_id,
                    parameter_id=stable_id("operation_parameter", flow["operation"] + "/" + field),
                    number_value=value if isinstance(value, int | float) else None,
                    text_value=value if isinstance(value, str) else None,
                    bool_value=None,
                )
            equipment = [resources[item] for item in step["equipment"]]
            if step["mode"] == "active":
                equipment.append("person")
            if "pan" in equipment or "pot" in equipment:
                equipment.append("burner")
            for resource in equipment:
                self.add(
                    "step_resource",
                    step_key + "/" + resource,
                    step_id=step_id,
                    resource_type_id=stable_id("resource_type", resource),
                    quantity=1,
                    capacity_min=None,
                    exclusive=True,
                )
            for material in flow["inputs"]:
                self.add(
                    "step_input",
                    step_key + "/" + material,
                    step_id=step_id,
                    material_id=stable_id("material_node", key + "/" + material),
                    fraction=1,
                )
            for output in flow["outputs"]:
                self.add(
                    "material_node",
                    key + "/" + output["key"],
                    recipe_version_id=version_id,
                    name=output["name"],
                    kind="dish" if number == len(recipe["steps"]) else "intermediate",
                    ingredient_line_id=None,
                    producer_step_id=step_id,
                    amount=None,
                    unit_id=None,
                )
        producers = {
            output["key"]: step["id"]
            for step, flow in zip(recipe["steps"], detail["steps"], strict=True)
            for output in flow["outputs"]
        }
        edges: set[tuple[str, str]] = set()
        for step, flow in zip(recipe["steps"], detail["steps"], strict=True):
            for material in flow["inputs"]:
                if material in producers:
                    edges.add((producers[material], step["id"]))
        for before, after in sorted(edges):
            self.add(
                "step_dependency",
                f"{key}/{before}/{after}",
                before_step_id=stable_id("recipe_step", key + "/" + before),
                after_step_id=stable_id("recipe_step", key + "/" + after),
                kind="material",
                min_lag_s=0,
                max_lag_s=None,
            )


def build_seed() -> Rows:
    return SeedBuilder().build()


def normalize_db(value: Any) -> Any:
    """DBの数値・UUID・日時表現を比較可能にする。"""
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, datetime):
        return value.astimezone(UTC).isoformat()
    if isinstance(value, list):
        items = cast(Sequence[Any], value)
        return [normalize_db(v) for v in items]
    if isinstance(value, dict):
        return {k: normalize_db(v) for k, v in cast(dict[str, Any], value).items()}
    return value


def insert_seed(connection: psycopg.Connection[Row], rows: Rows) -> dict[str, int]:
    """既存行の意味が変わる場合は上書きせず、版更新を要求する。"""
    metadata = {table["name"]: table for table in load("database/schema_catalog.json")["tables"]}
    counts: dict[str, int] = {}
    pending = dict(rows)
    while pending:
        ready = [
            table
            for table in pending
            if all(
                fk["referenced_table"] not in pending or fk["referenced_table"] == table
                for fk in metadata[table]["foreign_keys"]
            )
        ]
        if not ready:
            raise ValueError("初期データのテーブル参照が循環しています")
        for table in ready:
            items = pending.pop(table)
            if not items:
                continue
            columns = list(items[0])
            if any(set(item) != set(columns) for item in items):
                raise ValueError(f"初期データのカラム集合が不一致です: {table}")
            types = {c["name"]: c["type"] for c in metadata[table]["columns"]}
            if not set(columns) <= types.keys():
                raise ValueError(f"初期データに存在しないカラムがあります: {table}")
            statement = sql.SQL(
                "INSERT INTO recipeweave.{} ({}) VALUES ({}) ON CONFLICT (id) DO NOTHING"
            ).format(
                sql.Identifier(table),
                sql.SQL(", ").join(map(sql.Identifier, columns)),
                sql.SQL(", ").join(sql.Placeholder() for _ in columns),
            )
            values = [
                tuple(
                    Jsonb(item[c]) if types[c] == "jsonb" and item[c] is not None else item[c]
                    for c in columns
                )
                for item in items
            ]
            with connection.cursor() as cursor:
                cursor.executemany(statement, values)
            existing = connection.execute(
                sql.SQL("SELECT {} FROM recipeweave.{} WHERE id = ANY(%s::uuid[])").format(
                    sql.SQL(", ").join(map(sql.Identifier, columns)), sql.Identifier(table)
                ),
                ([item["id"] for item in items],),
            ).fetchall()
            by_id = {str(item["id"]): item for item in existing}
            for expected in items:
                actual = by_id.get(expected["id"])
                if normalize_db(actual) != normalize_db(expected):
                    raise ValueError(
                        "既存の初期データと内容が異なります。版を更新してください: "
                        f"{table}/{expected['id']}"
                    )
            counts[table] = len(items)
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="投入予定件数だけを検査・表示する")
    args = parser.parse_args()
    rows = build_seed()
    if args.dry_run:
        print(
            json.dumps(
                {table: len(items) for table, items in sorted(rows.items())},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URLが必要です")
    with psycopg.Connection[Row].connect(database_url, row_factory=dict_row) as connection:
        connection.execute("SELECT set_config('recipeweave.role', 'admin', true)")
        counts = insert_seed(connection, rows)
    print(json.dumps(counts, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
