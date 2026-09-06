"""非所有者DBロールと署名済みHTTP認証で全表・本人分離・競合を実証する。"""

import os
import time
from collections.abc import Iterator
from datetime import UTC, datetime
from typing import Any, cast
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

import jwt
import psycopg
import pytest
from fastapi.testclient import TestClient
from psycopg.rows import dict_row

from app.core.dependencies import get_settings
from app.entities.models import RecipeVersionWrite
from app.entities.registry import SPECIFICATIONS
from app.main import create_app

from .conftest import HttpTestClient

TABLES = sorted({spec.table for spec in SPECIFICATIONS.values()})
SECRET = "recipeweave-test-signing-secret-for-local-ci-only"  # noqa: S105 -- 公開のCI専用鍵


def token(user: str) -> str:
    """本番と分離したテスト用発行者で、署名・用途・期限を持つトークンを作る。"""
    now = int(time.time())
    return jwt.encode(
        dict(
            sub="local:" + user,
            role="admin" if user == "admin" else "user",
            iss="recipeweave-local",
            aud="recipeweave-api",
            iat=now,
            exp=now + 600,
        ),
        SECRET,
        algorithm="HS256",
    )


def headers(user: str) -> dict[str, str]:
    return {"Authorization": "Bearer " + token(user)}


def user_id(user: str) -> UUID:
    return uuid5(NAMESPACE_URL, "recipeweave:user:local:" + user)


@pytest.fixture
def database_client(monkeypatch: pytest.MonkeyPatch) -> Iterator[HttpTestClient]:
    """CIは実PostgreSQLのアプリ専用ロールで要求を送り、superuserなら失敗する。"""
    dsn = os.environ.get("TEST_DATABASE_URL")
    migration = os.environ.get("MIGRATION_DATABASE_URL")
    if not dsn or not migration:
        if os.environ.get("CI"):
            pytest.fail("CIでは実DB2接続の設定を必須とします")
        pytest.skip("実PostgreSQLはCIでTEST_DATABASE_URL/MIGRATION_DATABASE_URLを設定する")
    with psycopg.Connection[dict[str, Any]].connect(dsn, row_factory=dict_row) as connection:
        role = connection.execute(
            "SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user"
        ).fetchone()
        assert role is not None and not role["rolsuper"] and not role["rolbypassrls"]
    monkeypatch.setenv("DATABASE_URL", dsn)
    monkeypatch.setenv("AUTH_MODE", "local")
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("LOCAL_AUTH_SECRET", SECRET)
    monkeypatch.setenv("LOCAL_AUTH_PASSWORD", "local-test-password-only")
    get_settings.cache_clear()
    with TestClient(create_app()) as client:
        yield cast(HttpTestClient, client)
    get_settings.cache_clear()


@pytest.mark.parametrize("table", TABLES)
def test_every_table_has_real_postgresql_read_api(
    database_client: HttpTestClient, table: str
) -> None:
    """Given実DB全表 When管理者が一覧APIを要求 ThenSQLと全列の応答検証が成功。"""
    response = database_client.get("/api/entities/" + table, headers=headers("admin"))
    assert response.status_code == 200, response.text
    rows = cast(list[dict[str, Any]], response.json())
    assert type(rows) is list
    assert all("etag" in row and "id" in row for row in rows)


def test_real_owned_crud_isolation_and_cas(database_client: HttpTestClient) -> None:
    """Given2利用者 When献立作成・他人参照・更新競合・削除 Then本人だけ変更できる。"""
    create = database_client.post(
        "/api/entities/menu",
        headers=headers("alice"),
        json=dict(user_id=str(user_id("alice")), name="DB統合試験-" + str(uuid4()), servings="2.5"),
    )
    assert create.status_code == 201, create.text
    row = create.json()
    path = "/api/entities/menu/" + row["id"]
    first_etag = create.headers["ETag"]
    assert database_client.get(path, headers=headers("bob")).status_code == 404
    assert database_client.get(path, headers=headers("admin")).status_code == 404
    admin_takeover = database_client.put(
        path,
        headers={**headers("admin"), "If-Match": first_etag},
        json=dict(user_id=str(user_id("admin")), name="管理者からの所有者偽装", servings="2"),
    )
    assert admin_takeover.status_code == 409
    assert (
        database_client.put(
            path,
            headers={**headers("alice"), "If-Match": first_etag},
            json=dict(user_id=str(user_id("bob")), name="所有者偽装", servings="2"),
        ).status_code
        == 403
    )
    update = database_client.put(
        path,
        headers={**headers("alice"), "If-Match": first_etag},
        json=dict(user_id=str(user_id("alice")), name="変更後", servings="3.5"),
    )
    assert update.status_code == 200, update.text
    assert update.json()["revision"] == row["revision"] + 1
    conflict = database_client.put(
        path,
        headers={**headers("alice"), "If-Match": first_etag},
        json=dict(user_id=str(user_id("alice")), name="古い画面", servings="5"),
    )
    assert conflict.status_code == 409
    delete = database_client.delete(
        path, headers={**headers("alice"), "If-Match": update.headers["ETag"]}
    )
    assert delete.status_code == 200, delete.text
    assert database_client.get(path, headers=headers("alice")).status_code == 404


def test_database_rls_cannot_be_bypassed_by_raw_row_id(database_client: HttpTestClient) -> None:
    """Given別利用者の行ID WhenAPIを通さず非特権DB接続でSELECT ThenRLSが遮断。"""
    created = database_client.post(
        "/api/entities/menu",
        headers=headers("alice"),
        json=dict(user_id=str(user_id("alice")), name="RLS確認-" + str(uuid4()), servings="1"),
    )
    assert created.status_code == 201, created.text
    dsn = os.environ["TEST_DATABASE_URL"]
    with psycopg.Connection[dict[str, Any]].connect(dsn, row_factory=dict_row) as connection:
        connection.execute(
            "SELECT set_config('recipeweave.user_id', %s, true), "
            "set_config('recipeweave.role', 'user', true)",
            (str(user_id("bob")),),
        )
        row = connection.execute(
            "SELECT id FROM recipeweave.menu WHERE id = %s", (created.json()["id"],)
        ).fetchone()
        assert row is None
    database_client.delete(
        "/api/entities/menu/" + created.json()["id"],
        headers={**headers("alice"), "If-Match": created.headers["ETag"]},
    )


def test_private_input_is_not_echoed_in_validation_response(
    database_client: HttpTestClient,
) -> None:
    """Given未知の個人情報列 When入力検証 Then422だけ返し本文を応答へ複製しない。"""
    payload = dict(
        user_id=str(user_id("alice")),
        name="夕食",
        servings="2",
        rawOcr="private receipt customer phone 090",
    )
    response = database_client.post("/api/entities/menu", headers=headers("alice"), json=payload)
    assert response.status_code == 422
    assert "private receipt" not in response.text


def test_real_catalog_administration_and_retirement(database_client: HttpTestClient) -> None:
    """Given管理者と新単位 When追加・版条件付き編集・廃止 ThenSQL契約どおり保持する。"""
    body = dict(
        code="test-" + str(uuid4()),
        name="試験単位",
        dimension="count",
        factor="1",
        offset="0",
        status="active",
    )
    assert (
        database_client.post("/api/entities/unit", headers=headers("alice"), json=body).status_code
        == 403
    )
    created = database_client.post("/api/entities/unit", headers=headers("admin"), json=body)
    assert created.status_code == 201, created.text
    path = "/api/entities/unit/" + created.json()["id"]
    retired = database_client.put(
        path,
        headers={**headers("admin"), "If-Match": created.headers["ETag"]},
        json={**body, "status": "retired"},
    )
    assert retired.status_code == 200, retired.text
    assert retired.json()["status"] == "retired"
    assert database_client.delete(path, headers=headers("admin")).status_code == 405


def test_real_child_reference_cannot_use_other_users_menu(database_client: HttpTestClient) -> None:
    """Given別人の献立IDと有効なレシピ When明細作成 Then所有者FK経路で403。"""
    created = database_client.post(
        "/api/entities/menu",
        headers=headers("bob"),
        json=dict(user_id=str(user_id("bob")), name="子FK検証-" + str(uuid4()), servings="2"),
    )
    assert created.status_code == 201, created.text
    versions = database_client.get("/api/entities/recipe_version", headers=headers("admin"))
    assert versions.status_code == 200 and versions.json(), versions.text
    version = versions.json()[0]
    recipe = database_client.get(
        "/api/entities/recipe/" + version["recipe_id"], headers=headers("admin")
    )
    assert recipe.status_code == 200, recipe.text
    attempted = database_client.post(
        "/api/entities/menu_item",
        headers=headers("alice"),
        json=dict(
            menu_id=created.json()["id"],
            recipe_version_id=version["id"],
            servings="2",
            role_option_id=recipe.json()["family_option_id"],
            position=1,
        ),
    )
    assert attempted.status_code == 403, attempted.text
    deleted = database_client.delete(
        "/api/entities/menu/" + created.json()["id"],
        headers={**headers("bob"), "If-Match": created.headers["ETag"]},
    )
    assert deleted.status_code == 200


@pytest.mark.parametrize("table", ["menu_item", "user_recipe_event"])
def test_history_cannot_be_created_to_gain_unpublished_recipe_access(
    database_client: HttpTestClient, monkeypatch: pytest.MonkeyPatch, table: str
) -> None:
    """Given他人には未公開の版 When履歴を後付け Then拒否し既存本人履歴だけ継続可能。"""
    versions = database_client.get("/api/entities/recipe_version", headers=headers("admin"))
    assert versions.status_code == 200 and versions.json(), versions.text
    original = versions.json()[0]
    family = database_client.get(
        "/api/entities/recipe/" + original["recipe_id"], headers=headers("admin")
    )
    assert family.status_code == 200, family.text
    recipe_body = dict(
        title="公開境界試験-" + str(uuid4()),
        family_option_id=family.json()["family_option_id"],
        status="draft",
    )
    recipe = database_client.post(
        "/api/entities/recipe", headers=headers("admin"), json=recipe_body
    )
    assert recipe.status_code == 201, recipe.text
    version_body = {name: original[name] for name in RecipeVersionWrite.model_fields}
    version_body.update(
        recipe_id=recipe.json()["id"],
        version=1,
        status="draft",
        validation="needs_review",
        published_at=None,
    )
    version = database_client.post(
        "/api/entities/recipe_version", headers=headers("admin"), json=version_body
    )
    assert version.status_code == 201, version.text
    menus: dict[str, str] = {}
    for user in ("alice", "bob"):
        menu = database_client.post(
            "/api/entities/menu",
            headers=headers(user),
            json=dict(user_id=str(user_id(user)), name="履歴参照試験", servings="2"),
        )
        assert menu.status_code == 201, menu.text
        menus[user] = menu.json()["id"]

    def history_body(user: str, position: int) -> dict[str, Any]:
        if table == "menu_item":
            return dict(
                menu_id=menus[user],
                recipe_version_id=version.json()["id"],
                servings="2",
                role_option_id=recipe_body["family_option_id"],
                position=position,
            )
        return dict(
            user_id=str(user_id(user)),
            recipe_version_id=version.json()["id"],
            kind="liked",
            occurred_at=datetime.now(UTC).isoformat(),
            request_key=str(uuid4()),
        )

    path = "/api/entities/" + table
    monkeypatch.setattr("app.core.entity_service.catalog_preview_enabled", lambda: False)
    rejected = database_client.post(path, headers=headers("alice"), json=history_body("alice", 1))
    assert rejected.status_code == 403, rejected.text
    detail = "/api/recipes/" + recipe.json()["id"]
    assert database_client.get(detail, headers=headers("alice")).status_code == 404

    monkeypatch.setattr("app.core.entity_service.catalog_preview_enabled", lambda: True)
    accepted = database_client.post(path, headers=headers("alice"), json=history_body("alice", 1))
    assert accepted.status_code == 201, accepted.text
    withdrawal = database_client.put(
        "/api/entities/recipe/" + recipe.json()["id"],
        headers={**headers("admin"), "If-Match": recipe.headers["ETag"]},
        json={**recipe_body, "status": "withdrawn", "withdrawal_reason": "再確認のため"},
    )
    assert withdrawal.status_code == 200, withdrawal.text
    new_owner = database_client.post(path, headers=headers("bob"), json=history_body("bob", 1))
    assert new_owner.status_code == 403, new_owner.text
    monkeypatch.setattr("app.core.entity_service.catalog_preview_enabled", lambda: False)
    retained = database_client.post(path, headers=headers("alice"), json=history_body("alice", 2))
    assert retained.status_code == 201, retained.text
    assert database_client.get(detail, headers=headers("alice")).status_code == 200
    assert database_client.get(detail, headers=headers("bob")).status_code == 404
