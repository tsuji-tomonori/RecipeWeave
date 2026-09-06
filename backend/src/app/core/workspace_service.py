"""画面操作を正規化された業務行へ変換し、所有権と版を原子的に検査する。"""

import hashlib
from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4, uuid5

from fastapi import HTTPException
from psycopg import Connection

from app.core.identity import Identity, local_auth_enabled
from app.core.models import AppSnapshot, Food, MealItem
from app.core.operation_queries import OperationQueries
from app.core.workspace_models import (
    CookingRequest,
    CreatePantryRequest,
    CustomFoodRequest,
    MenuItemRequest,
    ReceiptRequest,
    RevisionRequest,
    SettingsRequest,
    ShoppingRequest,
    StockInput,
    UpdatePantryRequest,
)

LOCATIONS = {"冷蔵": "fridge", "冷凍": "freezer", "常温": "pantry"}
DISPLAY_LOCATIONS = {value: key for key, value in LOCATIONS.items()}


def identifier(value: str) -> UUID:
    """画面から来る識別子はUUIDとして検証する。"""
    try:
        return UUID(value)
    except ValueError as exc:
        raise HTTPException(422, "識別子の形式が不正です") from exc


def quantity(value: Any, unit: str) -> dict[str, Any]:
    """未知の数量をNULLのまま通信し、DBの十進値を表示用の数へ変換する。"""
    return {"value": None if value is None else float(value), "unit": unit}


def iso(value: Any) -> str | None:
    """日時はISO形式にそろえる。"""
    return value.isoformat() if isinstance(value, date | datetime) else None


class WorkspaceService:
    """要求単位のDBトランザクションを使い、JSONスナップショットは保存しない。"""

    def __init__(self, connection: Connection[dict[str, Any]], identity: Identity) -> None:
        self.connection = connection
        self.identity = identity
        self.user_id = identity.user_id
        self.menu_id = uuid5(self.user_id, "current-menu")

    def queries(self, name: str) -> OperationQueries:
        return OperationQueries(self.connection, "workspace/" + name)

    def begin(self, name: str, request: RevisionRequest) -> OperationQueries:
        queries = self.queries(name)
        rows = queries.run("q900_lock_revision", user_id=self.user_id)
        if not rows or int(rows[0]["revision"]) != request.expected_version:
            raise HTTPException(409, "他の画面で更新されています。最新の内容を読み込んでください")
        return queries

    def finish(self, queries: OperationQueries) -> AppSnapshot:
        queries.run("q901_advance_revision", user_id=self.user_id)
        queries.run(
            "q902_append_audit",
            row_id=uuid4(),
            user_id=self.user_id,
            action=queries.operation,
            key_hash=hashlib.sha256(str(self.user_id).encode()).hexdigest(),
        )
        return self.get_workspace()

    def get_workspace(self) -> AppSnapshot:
        """在庫・献立・設定・履歴を各テーブルから集約し、一貫した版を返す。"""
        q = self.queries("get_workspace")
        revision = q.run("q001_revision", user_id=self.user_id)
        consumptions = q.run("q003_consumption", user_id=self.user_id)
        lots = [
            {
                "id": str(r["id"]),
                "foodId": str(r["food_id"]),
                "originalFoodId": str(r["original_food_id"]),
                "quantity": quantity(r["amount"], r["unit"]),
                "originalQuantity": quantity(r["original_amount"], r["original_unit"]),
                "form": r["form"],
                "location": DISPLAY_LOCATIONS[r["location"]],
                "priority": r["priority"] == "use_first",
                "expiresOn": iso(r["expires_on"]),
                "createdAt": iso(r["created_at"]),
                "updatedAt": iso(r["updated_at"]),
                "sourceImportId": str(r["source_import_id"]) if r["source_import_id"] else None,
                "status": r["status"],
                "edited": r["edited"],
                "consumed": [
                    quantity(c["amount"], c["unit"]) for c in consumptions if c["lot_id"] == r["id"]
                ],
            }
            for r in q.run("q002_lots", user_id=self.user_id)
        ]
        imports = [
            {
                "id": str(r["id"]),
                "imageHash": r["file_sha256"],
                "purchaseSignature": r["idempotency_key"].split(":")[0],
                "createdAt": iso(r["created_at"]),
                "state": "registered" if r["status"] == "committed" else "undone",
                "createdLotIds": [
                    lot["id"] for lot in lots if lot["sourceImportId"] == str(r["id"])
                ],
                "undoneAt": iso(r["reverted_at"]),
            }
            for r in q.run("q004_receipts", user_id=self.user_id)
        ]
        meal = self.read_meal(q, self.menu_id)
        settings: dict[str, list[str]] = {
            "excludedFoodIds": [],
            "pantryFoodIds": [],
            "equipment": [],
        }
        setting_keys = {
            "excluded": "excludedFoodIds",
            "pantry": "pantryFoodIds",
            "equipment": "equipment",
        }
        for r in q.run("q008_settings", user_id=self.user_id):
            settings[setting_keys[r["kind"]]].append(r["value"])
        customs: list[dict[str, Any]] = [
            {
                "id": str(r["id"]),
                "name": r["name"],
                "aliases": [],
                "category": "追加した食材",
                "defaultUnit": r["unit"],
                "location": "冷蔵",
                "pantry": False,
                "imageIndex": None,
                "componentsKnown": False,
                "componentFoodIds": [],
            }
            for r in q.run("q009_custom_foods", user_id=self.user_id)
        ]
        checks = [
            {
                "key": r["client_key"],
                "signature": r["signature"],
                "foodId": str(r["food_id"]),
                "quantity": quantity(r["amount"], r["unit"]),
                "checkedAt": iso(r["checked_at"]),
                "archived": r["archived"],
            }
            for r in q.run("q010_shopping", user_id=self.user_id)
        ]
        from app.core.cooking_service import CookingService

        cooking = CookingService(self).read_current()
        return AppSnapshot.model_validate(
            {
                "schemaVersion": 1,
                "version": int(revision[0]["revision"]) if revision else 0,
                "lots": lots,
                "imports": imports,
                "drafts": {},
                "meal": meal,
                "saved": [str(r["recipe_id"]) for r in q.run("q007_saved", user_id=self.user_id)],
                "shoppingChecks": checks,
                "cooking": cooking,
                "settings": settings,
                "customFoods": customs,
                "search": {
                    "selectedFoodIds": [],
                    "match": "all",
                    "maxMinutes": None,
                    "noShopping": False,
                    "equipment": [],
                },
            }
        )

    def read_meal(self, q: OperationQueries, menu_id: UUID) -> list[dict[str, Any]]:
        amounts = q.run("q006_ingredients", menu_id=menu_id, user_id=self.user_id)
        return [
            {
                "id": str(r["id"]),
                "recipeId": str(r["recipe_id"]),
                "servings": float(r["servings"]),
                "adjusted": any(
                    a["override_id"] is not None for a in amounts if a["menu_item_id"] == r["id"]
                ),
                "amounts": {
                    str(a["food_id"]): quantity(
                        a["override_amount"] if a["override_id"] else a["scaled_amount"], a["unit"]
                    )
                    for a in amounts
                    if a["menu_item_id"] == r["id"]
                },
            }
            for r in q.run("q005_menu", menu_id=menu_id, user_id=self.user_id)
        ]

    def _stock(self, q: OperationQueries, value: StockInput) -> dict[str, Any]:
        form = q.run(
            "q001_resolve_form",
            food_id=identifier(value.food_id),
            form=value.form,
            unit=value.quantity.unit,
            user_id=self.user_id,
        )
        if not form:
            raise HTTPException(422, "食材・形態・単位の組合せが見つかりません")
        try:
            expires = date.fromisoformat(value.expires_on) if value.expires_on else None
        except ValueError as exc:
            raise HTTPException(422, "期限の日付が不正です") from exc
        return {
            **form[0],
            "user_id": self.user_id,
            "amount": Decimal(str(value.quantity.value))
            if value.quantity.value is not None
            else None,
            "quality": "unknown" if value.quantity.value is None else "known",
            "expires_on": expires,
            "location": LOCATIONS[value.location],
            "priority": "use_first" if value.priority else "normal",
        }

    def create_pantry_lot(self, request: CreatePantryRequest) -> AppSnapshot:
        """数量不明を含めて本人の在庫を登録する。"""
        q = self.begin("create_pantry_lot", request)
        q.run(
            "q002_insert_lot",
            **self._stock(q, request),
            row_id=identifier(request.id),
            import_id=None,
        )
        return self.finish(q)

    def update_pantry_lot(self, request: UpdatePantryRequest, row_id: UUID) -> AppSnapshot:
        """元の登録値を保ち、編集・復元できる本人の在庫だけを更新する。"""
        q = self.begin("update_pantry_lot", request)
        rows = q.run(
            "q002_update_lot", **self._stock(q, request), row_id=row_id, restore=request.restore
        )
        if not rows:
            raise HTTPException(404, "この在庫は編集・復元できません")
        return self.finish(q)

    def delete_pantry_lot(self, request: RevisionRequest, row_id: UUID) -> AppSnapshot:
        """消費履歴を残し、在庫を利用対象から外す。"""
        q = self.begin("delete_pantry_lot", request)
        if not q.run("q001_delete_lot", row_id=row_id, user_id=self.user_id):
            raise HTTPException(404, "在庫が見つからないか削除済みです")
        return self.finish(q)

    def add_item(self, q: OperationQueries, item: MealItem, menu_id: UUID, name: str) -> None:
        version = q.run(
            "q010_recipe", recipe_id=identifier(item.recipe_id), preview=local_auth_enabled()
        )
        if not version:
            raise HTTPException(404, "料理が公開されていません")
        ingredients = q.run("q011_ingredients", version_id=version[0]["id"])
        if set(item.amounts) != {str(r["food_id"]) for r in ingredients}:
            raise HTTPException(422, "材料の構成が料理版と一致しません")
        # 同じ食品が複数材料行に分かれる料理は、曖昧なfood_id単位上書きを拒否する。
        if len({r["food_id"] for r in ingredients}) != len(ingredients):
            raise HTTPException(422, "この料理は材料行ごとの分量指定APIを利用してください")
        q.run("q012_menu", menu_id=menu_id, user_id=self.user_id, name=name)
        q.run(
            "q013_insert_item",
            row_id=identifier(item.id),
            menu_id=menu_id,
            version_id=version[0]["id"],
            servings=Decimal(str(item.servings)),
        )
        for ingredient in ingredients:
            amount = item.amounts[str(ingredient["food_id"])]
            if amount.value is None or amount.unit != ingredient["unit"]:
                raise HTTPException(422, "確定した分量と料理の単位を指定してください")
            if amount.value == 0 and not ingredient["optional"]:
                raise HTTPException(422, "必須材料には0より大きい分量を指定してください")
            q.run(
                "q014_override",
                row_id=uuid4(),
                item_id=identifier(item.id),
                ingredient_id=ingredient["id"],
                amount=Decimal(str(amount.value)) if amount.value > 0 else None,
                selected=amount.value > 0,
            )
        q.run("q015_advance_menu", menu_id=menu_id, user_id=self.user_id)

    def add_menu_item(self, request: MenuItemRequest) -> AppSnapshot:
        """確認した料理版・人数・材料別分量を献立へ保存する。"""
        q = self.begin("add_menu_item", request)
        self.add_item(q, request.item, self.menu_id, "現在の献立")
        return self.finish(q)

    def update_menu_item(self, request: MenuItemRequest, row_id: UUID) -> AppSnapshot:
        """本人の献立項目を置き換え、調理用に確定済みの献立は変更しない。"""
        if identifier(request.item.id) != row_id:
            raise HTTPException(422, "対象の料理IDが一致しません")
        q = self.begin("update_menu_item", request)
        if not q.run("q001_delete_item", row_id=row_id, menu_id=self.menu_id, user_id=self.user_id):
            raise HTTPException(404, "献立の料理が見つかりません")
        self.add_item(q, request.item, self.menu_id, "現在の献立")
        return self.finish(q)

    def delete_menu_item(self, request: RevisionRequest, row_id: UUID) -> AppSnapshot:
        """現在の献立から本人の項目を取り除く。"""
        q = self.begin("delete_menu_item", request)
        if not q.run("q001_delete_item", row_id=row_id, menu_id=self.menu_id, user_id=self.user_id):
            raise HTTPException(404, "献立の料理が見つかりません")
        return self.finish(q)

    def _save_recipe(self, name: str, request: RevisionRequest, row_id: UUID) -> AppSnapshot:
        q = self.begin(name, request)
        rows = q.run("q001_recipe", recipe_id=row_id, preview=local_auth_enabled())
        if not rows:
            raise HTTPException(404, "料理が公開されていません")
        q.run(
            "q002_event",
            row_id=uuid4(),
            user_id=self.user_id,
            version_id=rows[0]["id"],
            request_key=f"{name}:{request.expected_version}:{row_id}",
        )
        return self.finish(q)

    def save_recipe(self, request: RevisionRequest, row_id: UUID) -> AppSnapshot:
        """料理の保存を本人の履歴へ記録する。"""
        return self._save_recipe("save_recipe", request, row_id)

    def unsave_recipe(self, request: RevisionRequest, row_id: UUID) -> AppSnapshot:
        """保存の解除を本人の履歴へ追記する。"""
        return self._save_recipe("unsave_recipe", request, row_id)

    def put_settings(self, request: SettingsRequest) -> AppSnapshot:
        """除外・常備・器具の選択を関連行として保存する。"""
        q = self.begin("put_settings", request)
        for statement in ["q001_clear_exclusion", "q002_clear_pantry", "q003_clear_equipment"]:
            q.run(statement, user_id=self.user_id)
        for food in set(request.settings.excluded_food_ids):
            q.run("q004_exclusion", row_id=uuid4(), user_id=self.user_id, food_id=identifier(food))
        for food in set(request.settings.pantry_food_ids):
            q.run("q005_pantry", row_id=uuid4(), user_id=self.user_id, food_id=identifier(food))
        for equipment in set(request.settings.equipment):
            if not q.run("q006_equipment", row_id=uuid4(), user_id=self.user_id, name=equipment):
                raise HTTPException(422, "未登録の器具が含まれています")
        return self.finish(q)

    def put_shopping_checks(self, request: ShoppingRequest) -> AppSnapshot:
        """買い物確認を数量・単位とともに保存する。"""
        q = self.begin("put_shopping_checks", request)
        q.run("q001_clear", user_id=self.user_id)
        for item in request.checks:
            try:
                checked_at = datetime.fromisoformat(item.checked_at.replace("Z", "+00:00"))
            except ValueError as exc:
                raise HTTPException(422, "購入確認日時が不正です") from exc
            if not q.run(
                "q002_insert",
                row_id=uuid4(),
                user_id=self.user_id,
                key=item.key,
                signature=item.signature,
                food_id=identifier(item.food_id),
                amount=item.quantity.value,
                unit=item.quantity.unit,
                checked_at=checked_at,
                archived=item.archived,
            ):
                raise HTTPException(422, "買い物の単位が見つかりません")
        return self.finish(q)

    def _custom_food(self, q: OperationQueries, food: Food) -> None:
        food_id = identifier(food.id)
        if food.components_known or food.component_food_ids or food.aliases:
            raise HTTPException(422, "独自食材の構成や別名はこの操作では確定できません")
        release_id = uuid5(self.user_id, "private-catalog")
        q.run("q019_private_release", release_id=release_id, user_id=self.user_id,
              version=f"private:{self.user_id}", manifest=hashlib.sha256(b"private-catalog-v1").hexdigest())
        q.run(
            "q020_custom_food",
            food_id=food_id,
            code=f"USER-{food_id}",
            name=food.name.strip(),
            user_id=self.user_id,
            release_id=release_id,
        )
        q.run("q021_custom_owner", row_id=uuid4(), user_id=self.user_id, food_id=food_id)
        if not q.run(
            "q022_custom_form",
            row_id=uuid5(food_id, "standard"),
            food_id=food_id,
            unit=food.default_unit,
        ):
            raise HTTPException(422, "食材の単位が見つかりません")

    def create_custom_food(self, request: CustomFoodRequest) -> AppSnapshot:
        """カタログにない食材を本人の所有として登録する。"""
        q = self.begin("create_custom_food", request)
        self._custom_food(q, request.food)
        return self.finish(q)

    def commit_receipt(self, request: ReceiptRequest) -> AppSnapshot:
        """確認済み商品だけを在庫へ登録し、同じ要求の二重反映を防ぐ。"""
        q = self.begin("commit_receipt", request)
        import_id = identifier(request.id)
        duplicate = q.run(
            "q003_duplicate",
            user_id=self.user_id,
            import_id=import_id,
            hash=request.image_hash,
            signature=request.purchase_signature + "%",
        )
        if any(r["id"] == import_id for r in duplicate) or (
            duplicate and not request.allow_duplicate
        ):
            raise HTTPException(409, "このレシートは登録済みです。重複を確認してください")
        selected = [
            c for c in request.candidates if c.selected and c.food_id and c.status != "excluded"
        ]
        if any(c.selected and (not c.food_id or c.status == "excluded") for c in request.candidates):
            raise HTTPException(422, "選択した行の食材を確認してください")
        if any(c.quantity.value == 0 for c in selected):
            raise HTTPException(422, "レシートの数量は0より大きい数か数量不明にしてください")
        if not selected:
            raise HTTPException(422, "在庫に入れる食材を一つ以上選んでください")
        for food in request.custom_foods:
            if food.id not in {c.food_id for c in selected}:
                raise HTTPException(422, "選択されていない独自食材は登録できません")
            self._custom_food(q, food)
        q.run(
            "q004_import",
            import_id=import_id,
            user_id=self.user_id,
            hash=request.image_hash,
            key=f"{request.purchase_signature}:{import_id}",
        )
        for number, candidate in enumerate(selected, 1):
            stock = StockInput(food_id=str(candidate.food_id), quantity=candidate.quantity)
            resolved = self._stock(q, stock)
            lot_id = uuid5(import_id, f"line:{number}")
            q.run("q002_insert_lot", **resolved, row_id=lot_id, import_id=import_id)
            q.run(
                "q005_line",
                row_id=uuid5(import_id, f"receipt-line:{number}"),
                import_id=import_id,
                line_no=number,
                name=candidate.raw_text,
                form_id=resolved["form_id"],
                amount=resolved["amount"],
                unit_id=resolved["unit_id"],
                lot_id=lot_id,
            )
        return self.finish(q)

    def undo_receipt(self, request: RevisionRequest, row_id: UUID) -> AppSnapshot:
        """未使用・未編集の登録分だけを取り消し、使用済みの在庫は残す。"""
        q = self.begin("undo_receipt", request)
        rows = q.run("q001_import", row_id=row_id, user_id=self.user_id)
        if not rows or rows[0]["status"] != "committed":
            raise HTTPException(409, "レシートがないか取消済みです")
        q.run("q002_eligible_lots", row_id=row_id, user_id=self.user_id)
        q.run("q003_revert", row_id=row_id, user_id=self.user_id)
        return self.finish(q)

    def create_cooking_session(self, request: CookingRequest) -> AppSnapshot:
        """DBの料理と材料から調理計画を構築する。"""
        from app.core.cooking_service import CookingService

        return CookingService(self).create(request)

    def update_cooking_session(self, request: CookingRequest, row_id: UUID) -> AppSnapshot:
        """工程の進行と在庫消費をDBで検証して確定する。"""
        from app.core.cooking_service import CookingService

        return CookingService(self).update(request, row_id)
