"""実PostgreSQL上の食品・レシピをHTTP経由で検索し、公開境界を検査する。"""

import os
import secrets
import time
from collections.abc import Iterator
from typing import Any, cast
from uuid import uuid4

import jwt
import psycopg
import pytest
from database.seed import build_seed, insert_seed, stable_id
from fastapi.testclient import TestClient
from psycopg.rows import dict_row

from app.core.db import get_database
from app.core.dependencies import get_settings
from app.main import create_app

from .conftest import HttpTestClient


@pytest.fixture(scope="module")
def catalog_database() -> Iterator[psycopg.Connection[dict[str, Any]]]:
    database_url = os.environ.get("TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("カタログの実DB検証にはTEST_DATABASE_URLを指定する")
    with psycopg.Connection[dict[str, Any]].connect(
        database_url, row_factory=dict_row
    ) as connection:
        connection.execute("SELECT set_config('recipeweave.role', 'admin', true)")
        insert_seed(connection, build_seed())
        yield connection
        connection.rollback()


@pytest.fixture
def database_client(
    catalog_database: psycopg.Connection[dict[str, Any]],
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[HttpTestClient]:
    monkeypatch.setenv("AUTH_MODE", "local")
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("LOCAL_AUTH_SECRET", secrets.token_hex(32))
    monkeypatch.setenv("LOCAL_AUTH_PASSWORD", secrets.token_urlsafe(24))
    monkeypatch.delenv("AWS_LAMBDA_FUNCTION_NAME", raising=False)
    get_settings.cache_clear()
    app = create_app()
    app.dependency_overrides[get_database] = lambda: catalog_database
    with catalog_database.transaction(force_rollback=True), TestClient(app) as client:
        yield cast(HttpTestClient, client)
    get_settings.cache_clear()


def preview_headers(subject: str = "local:alice") -> dict[str, str]:
    now = int(time.time())
    token = jwt.encode(
        {
            "sub": subject,
            "iss": "recipeweave-local",
            "aud": "recipeweave-api",
            "role": "user",
            "iat": now,
            "exp": now + 300,
        },
        get_settings().local_auth_secret,
        algorithm="HS256",
    )
    return {"Authorization": "Bearer " + token}


def test_public_search_never_exposes_review_pending_recipes(
    database_client: HttpTestClient,
) -> None:
    response = database_client.get("/api/recipes")
    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["items"] == []
    recipe_id = stable_id("recipe", "eggplant-egg")
    assert database_client.get("/api/recipes/" + recipe_id).status_code == 404
    random = database_client.get("/api/recipes/random")
    assert random.status_code == 200
    assert random.json() == {"item": None, "total": 0}


def test_preview_requires_signed_identity_and_local_environment(
    database_client: HttpTestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    query: dict[str, str | list[str]] = {"preview": "true"}
    assert database_client.get("/api/recipes", params=query).status_code == 401
    response = database_client.get("/api/recipes", params=query, headers=preview_headers())
    assert response.status_code == 200
    assert response.json()["total"] == 8
    assert all(item["sample"] for item in response.json()["items"])
    monkeypatch.setenv("ENVIRONMENT", "production")
    get_settings.cache_clear()
    assert (
        database_client.get("/api/recipes", params=query, headers=preview_headers()).status_code
        == 403
    )


def test_food_catalog_reads_all_rows_and_persisted_alias(
    database_client: HttpTestClient,
    catalog_database: psycopg.Connection[dict[str, Any]],
) -> None:
    response = database_client.get("/api/foods")
    assert response.status_code == 200
    assert response.json()["total"] == 1018
    food_id = stable_id("food", "food_88f91799ac")
    catalog_database.execute(
        "INSERT INTO recipeweave.food_alias (id, food_id, alias, locale) VALUES (%s, %s, %s, 'ja')",
        (uuid4(), food_id, "DB保存の検索別名"),
    )
    found = database_client.get("/api/foods", params={"q": "DB保存の検索別名"})
    assert found.status_code == 200
    assert [food["id"] for food in found.json()["items"]] == [food_id]


def test_recipe_detail_uses_database_text_and_quantities(
    database_client: HttpTestClient,
    catalog_database: psycopg.Connection[dict[str, Any]],
) -> None:
    version_id = stable_id("recipe_version", "tomato-egg/1")
    catalog_database.execute(
        "UPDATE recipeweave.recipe_version SET description = %s WHERE id = %s",
        ("DBへ保存した説明をそのまま表示", version_id),
    )
    response = database_client.get(
        "/api/recipes/" + stable_id("recipe", "tomato-egg"),
        params={"preview": "true"},
        headers=preview_headers(),
    )
    assert response.status_code == 200
    recipe = response.json()
    assert recipe["description"] == "DBへ保存した説明をそのまま表示"
    assert recipe["servings"] == 2
    assert recipe["ingredients"][0]["quantity"] == {"value": 200, "unit": "g"}
    assert len(recipe["steps"]) == 3
    assert recipe["steps"][0]["guide"] == "くし形切り"


def test_search_filters_pagination_and_random_exclusion(database_client: HttpTestClient) -> None:
    headers = preview_headers()
    tomato = stable_id("food", "food_88f91799ac")
    egg = stable_id("food", "food_7cd14b25a8")
    response = database_client.get(
        "/api/recipes",
        headers=headers,
        params={"preview": "true", "selectedFoodIds": [tomato, egg], "match": "all"},
    )
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["id"] == stable_id("recipe", "tomato-egg")
    second_page = database_client.get(
        "/api/recipes", headers=headers, params={"preview": "true", "limit": "2", "offset": "2"}
    )
    assert second_page.status_code == 200
    assert second_page.json()["total"] == 8
    assert len(second_page.json()["items"]) == 2
    assert second_page.json()["offset"] == 2
    excluded = database_client.get(
        "/api/recipes",
        headers=headers,
        params={"preview": "true", "excludedFoodIds": egg, "maxMinutes": "10"},
    )
    assert excluded.status_code == 200
    assert all(
        item["minutes"] <= 10 and all(line["foodId"] != egg for line in item["ingredients"])
        for item in excluded.json()["items"]
    )
    recipe_id = stable_id("recipe", "mushroom-butter")
    random = database_client.get(
        "/api/recipes/random",
        headers=headers,
        params={"preview": "true", "excludeId": recipe_id, "excludedFoodIds": egg},
    )
    assert random.status_code == 200
    assert random.json()["item"]["id"] != recipe_id
    assert all(line["foodId"] != egg for line in random.json()["item"]["ingredients"])


def test_invalid_search_inputs_are_rejected(database_client: HttpTestClient) -> None:
    cases: list[dict[str, str | list[str]]] = [
        {"maxMinutes": "-1"},
        {"servings": "2"},
        {"limit": "101"},
        {"offset": "-1"},
        {"selectedFoodIds": "tomato"},
    ]
    for params in cases:
        assert database_client.get("/api/recipes", params=params).status_code == 422
    assert database_client.get("/api/recipes/not-a-uuid").status_code == 422


def test_owned_history_pins_exact_version_and_isolates_withdrawn_content(
    database_client: HttpTestClient,
    catalog_database: psycopg.Connection[dict[str, Any]],
) -> None:
    """取下げ前の所有履歴だけが同じ版を復元でき、他人・匿名へ漏れない。"""
    from database.seed import user_id

    recipe_id = stable_id("recipe", "tomato-egg")
    original_version = stable_id("recipe_version", "tomato-egg/1")
    next_version = uuid4()
    catalog_database.execute(
        """INSERT INTO recipeweave.user_recipe_event
        (id, user_id, recipe_version_id, kind, occurred_at, request_key)
        VALUES (%s, %s, %s, 'liked', CURRENT_TIMESTAMP, %s)""",
        (uuid4(), user_id("local:alice"), original_version, str(uuid4())),
    )
    catalog_database.execute(
        """INSERT INTO recipeweave.recipe_version
        (id, recipe_id, version, release_id, base_servings, output_amount,
         output_unit_id, status, validation, content_hash, description)
        SELECT %s, recipe_id, 2, release_id, base_servings, output_amount,
            output_unit_id, 'draft', 'needs_review', content_hash, '別の版の説明'
        FROM recipeweave.recipe_version WHERE id = %s""",
        (next_version, original_version),
    )
    catalog_database.execute(
        "UPDATE recipeweave.recipe SET status = 'withdrawn', withdrawal_reason = %s WHERE id = %s",
        ("作り方を再確認しているため", recipe_id),
    )
    catalog_database.execute(
        "UPDATE recipeweave.recipe_version SET status = 'withdrawn' WHERE id = %s",
        (original_version,),
    )
    path = "/api/recipes/" + recipe_id
    query: dict[str, str | list[str]] = {"versionId": original_version}
    owner = database_client.get(path, params=query, headers=preview_headers())
    assert owner.status_code == 200
    assert owner.json()["versionId"] == original_version
    assert owner.json()["publicationStatus"] == "withdrawn"
    assert owner.json()["withdrawalReason"] == "作り方を再確認しているため"
    assert len(owner.json()["ingredients"]) == 4
    assert owner.json()["description"] != "別の版の説明"
    assert database_client.get(path, params=query).status_code == 404
    assert (
        database_client.get(path, params=query, headers=preview_headers("local:bob")).status_code
        == 404
    )
    assert (
        database_client.get(
            path, params={"versionId": str(next_version)}, headers=preview_headers()
        ).status_code
        == 404
    )
    assert (
        database_client.get(
            path, params={"versionId": str(uuid4())}, headers=preview_headers()
        ).status_code
        == 404
    )
