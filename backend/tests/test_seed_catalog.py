"""カタログ投入の完全性と、試作原稿を公開済みにしない境界を検査する。"""

import copy
import os
from collections import Counter
from decimal import Decimal
from math import comb
from typing import Any

import psycopg
import pytest
from database.seed import SeedBuilder, build_seed, insert_seed, load, sha, stable_id, user_id
from psycopg.rows import dict_row


@pytest.fixture(scope="module")
def seed_rows() -> dict[str, list[dict[str, Any]]]:
    return build_seed()


def test_all_catalog_foods_axes_options_are_imported(
    seed_rows: dict[str, list[dict[str, Any]]],
) -> None:
    """元スプレッドシートのIDを一件も落とさず、追加概念は別IDにする。"""
    tabs = load("spec/database/catalog-source-sheet.json")["tabs"]
    foods = {row["code"] for row in seed_rows["food"]}
    axes = {row["code"] for row in seed_rows["axis"]}
    options = {row["id"] for row in seed_rows["axis_option"]}
    assert {row[0] for row in tabs["02_食材カタログ"][1:]} <= foods
    assert len(foods) == 1018
    assert {row[0] for row in tabs["01_新組合せ軸"][1:]} <= axes
    assert {
        stable_id("axis_option", row[0] + "/" + row[1]) for row in tabs["03_軸候補全値"][1:]
    } <= options
    assert len(seed_rows["food_identity_member"]) == len(foods)


def test_all_seed_references_resolve(seed_rows: dict[str, list[dict[str, Any]]]) -> None:
    """投入順だけでなく全FK対象が実在することを確認する。"""
    metadata = {table["name"]: table for table in load("database/schema_catalog.json")["tables"]}
    for table, rows in seed_rows.items():
        ids = [row["id"] for row in rows]
        assert len(ids) == len(set(ids)), table
        columns = {column["name"] for column in metadata[table]["columns"]}
        for row in rows:
            assert set(row) <= columns, (table, set(row) - columns)
        for relation in metadata[table]["foreign_keys"]:
            targets = {
                tuple(row[column] for column in relation["referenced_columns"])
                for row in seed_rows.get(relation["referenced_table"], [])
            }
            for row in rows:
                values = tuple(row.get(column) for column in relation["columns"])
                if None not in values:
                    assert values in targets, (table, relation, values)


def test_initial_recipes_are_review_pending(seed_rows: dict[str, list[dict[str, Any]]]) -> None:
    """構造検査を調理・食味の試作にすり替えず公開対象に含めない。"""
    assert len(seed_rows["recipe"]) == 8
    assert len(seed_rows["recipe_ingredient"]) == 34
    assert len(seed_rows["recipe_step"]) == 25
    assert all(row["status"] == "draft" for row in seed_rows["recipe"])
    assert all(
        row["status"] == "draft"
        and row["validation"] == "needs_review"
        and row["published_at"] is None
        for row in seed_rows["recipe_version"]
    )
    assert "recipe_search_document" not in seed_rows
    trial_id = stable_id("compatibility_rule", "cooking_trial")
    trials = [row for row in seed_rows["validation_result"] if row["rule_id"] == trial_id]
    assert len(trials) == 8
    assert all(row["state"] == "needs_review" for row in trials)


def test_materials_have_one_consumer_and_real_dependency_edges(
    seed_rows: dict[str, list[dict[str, Any]]],
) -> None:
    """材料を消費したように見せるだけの辺や、二重使用を防ぐ。"""
    materials = {row["id"]: row for row in seed_rows["material_node"]}
    steps = {row["id"]: row for row in seed_rows["recipe_step"]}
    edges = {
        (row["before_step_id"], row["after_step_id"])
        for row in seed_rows["step_dependency"]
        if row["kind"] == "material"
    }
    consumers: Counter[str] = Counter()
    derived_edges: set[tuple[str, str]] = set()
    for row in seed_rows["step_input"]:
        consumers[row["material_id"]] += row["fraction"]
        material = materials[row["material_id"]]
        consumer = steps[row["step_id"]]
        assert consumer["recipe_version_id"] == material["recipe_version_id"]
        if material["producer_step_id"]:
            producer = steps[material["producer_step_id"]]
            assert producer["step_no"] < consumer["step_no"]
            derived_edges.add((producer["id"], consumer["id"]))
    assert edges == derived_edges
    for row in materials.values():
        assert consumers[row["id"]] == (0 if row["kind"] == "dish" else 1)


def test_generation_template_counts_are_computed_from_real_identities(
    seed_rows: dict[str, list[dict[str, Any]]],
) -> None:
    """候補件数を固定値として信じず、許可集合から再計算する。"""
    identity_ids = {row["id"] for row in seed_rows["food_identity"]}
    for row in seed_rows["generation_template"]:
        contract = row["contract"]
        primaries = set(contract["primary_identity_ids"])
        supports = set(contract["support_identity_ids"])
        assert primaries | supports <= identity_ids
        calculated = sum(
            comb(len(supports - {primary}), k)
            for primary in primaries
            for k in contract["support_k"]
        )
        if "support_identity_sets" in contract:
            calculated = sum(
                1
                for primary in primaries
                for group in contract["support_identity_sets"]
                if primary not in group
            )
        calculated *= len(contract["flavor_codes"]) * len(contract["route_codes"])
        assert row["candidate_count"] == calculated, row["code"]
        assert row["contract_hash"] == sha(contract)


def test_seed_is_deterministic_and_quantity_signatures_are_per_serving(
    seed_rows: dict[str, list[dict[str, Any]]],
) -> None:
    assert build_seed() == seed_rows
    versions = {row["id"]: row for row in seed_rows["recipe_version"]}
    for signature in seed_rows["recipe_signature"]:
        version = versions[signature["recipe_version_id"]]
        ingredients = [
            row
            for row in seed_rows["recipe_ingredient"]
            if row["recipe_version_id"] == version["id"]
        ]
        payload = signature["canonical_payload"]
        quantities = {
            row["form_id"]: Decimal(row["amount_per_serving"])
            for row in payload["ingredient_ratios"]
        }
        for ingredient in ingredients:
            assert quantities[ingredient["form_id"]] == (
                Decimal(str(ingredient["amount"])) / Decimal(str(version["base_servings"]))
            )
        assert "title" not in payload
        assert signature["exact_hash"] == sha(payload)


def test_catalog_snapshot_mismatch_is_rejected() -> None:
    builder = SeedBuilder()
    builder.base()
    builder.axes()
    builder.foods = copy.deepcopy(builder.foods)
    builder.foods.pop()
    with pytest.raises(ValueError, match="ID集合"):
        builder.food_catalog()


def test_seed_real_database_idempotency_and_drift_rejection(
    seed_rows: dict[str, list[dict[str, Any]]],
) -> None:
    """実PostgreSQLへ二度投入し、改変済み初期行を黙って上書きしない。"""
    database_url = os.environ.get("TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("実DB検証にはTEST_DATABASE_URLを指定する")
    with psycopg.Connection[dict[str, Any]].connect(
        database_url, row_factory=dict_row
    ) as connection:
        connection.execute("SELECT set_config('recipeweave.role', 'admin', true)")
        first = insert_seed(connection, seed_rows)
        second = insert_seed(connection, seed_rows)
        assert first == second
        connection.execute(
            "UPDATE recipeweave.app_user SET locale = 'en' WHERE id = %s", (user_id("local:alice"),)
        )
        with pytest.raises(ValueError, match="既存の初期データ"):
            insert_seed(connection, seed_rows)
        connection.rollback()


def test_seed_json_matches_typed_crud_contracts(
    seed_rows: dict[str, list[dict[str, Any]]],
) -> None:
    """DBへ入ってもGETで検証エラーになるJSON形状を初期投入前に検出する。"""
    from app.entities.json_contracts import (
        CanonicalRecipe,
        GenerationTemplateContract,
        Predicate,
        ValidationEvidence,
    )

    for row in seed_rows["recipe_signature"]:
        CanonicalRecipe.model_validate(row["canonical_payload"])
    for row in seed_rows["generation_template"]:
        GenerationTemplateContract.model_validate(row["contract"])
    for row in seed_rows["compatibility_rule"]:
        Predicate.model_validate(row["predicate"])
    for row in seed_rows["validation_result"]:
        ValidationEvidence.model_validate(row["evidence"])
