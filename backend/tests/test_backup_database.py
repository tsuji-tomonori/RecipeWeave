"""非特権PostgreSQLで本人バックアップの往復・真正性・原子的取消しを確認する。"""

import copy
import os
import secrets
import time
from collections.abc import Iterator
from decimal import Decimal
from typing import Any, cast
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

import jwt
import psycopg
import pytest
from database.seed import build_seed, insert_seed, stable_id
from fastapi.testclient import TestClient
from psycopg.rows import dict_row

from app.core.db import get_database
from app.core.dependencies import get_settings
from app.core.operation_queries import OperationQueries
from app.main import create_app

from .conftest import HttpTestClient


@pytest.fixture
def backup_client() -> Iterator[tuple[HttpTestClient, psycopg.Connection[dict[str, Any]]]]:
    """要求ごとのsavepointと最後の全取消しで、本物のRLS・制約を隔離検証する。"""
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        if os.environ.get("CI"):
            pytest.fail("CIの必須DB検証にTEST_DATABASE_URLがありません")
        pytest.skip("実DBバックアップ検証にはTEST_DATABASE_URLを指定する")
    with (
        psycopg.Connection[dict[str, Any]].connect(url, row_factory=dict_row) as connection,
        connection.transaction(force_rollback=True),
    ):
        role = connection.execute(
            "SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user"
        ).fetchone()
        assert role and not role["rolsuper"] and not role["rolbypassrls"]
        connection.execute("SELECT set_config('recipeweave.role', 'admin', true)")
        insert_seed(connection, build_seed())
        with pytest.MonkeyPatch.context() as patch:
            patch.setenv("DATABASE_URL", url)
            patch.setenv("AUTH_MODE", "local")
            patch.setenv("ENVIRONMENT", "test")
            patch.setenv("LOCAL_AUTH_SECRET", secrets.token_hex(32))
            patch.setenv("LOCAL_AUTH_PASSWORD", secrets.token_urlsafe(24))
            patch.delenv("AWS_LAMBDA_FUNCTION_NAME", raising=False)
            get_settings.cache_clear()
            application = create_app()

            def database() -> Iterator[psycopg.Connection[dict[str, Any]]]:
                with connection.transaction():
                    yield connection

            application.dependency_overrides[get_database] = database
            with TestClient(application, raise_server_exceptions=False) as client:
                yield cast(HttpTestClient, client), connection
            get_settings.cache_clear()


def auth(user: str = "alice") -> dict[str, str]:
    now = int(time.time())
    claims = {
        "sub": "local:" + user,
        "iss": "recipeweave-local",
        "aud": "recipeweave-api",
        "role": "user",
        "iat": now,
        "exp": now + 300,
    }
    return {
        "Authorization": "Bearer "
        + jwt.encode(claims, get_settings().local_auth_secret, algorithm="HS256")
    }


def account(user: str = "alice") -> UUID:
    return uuid5(NAMESPACE_URL, "recipeweave:user:local:" + user)


def export(client: HttpTestClient, user: str = "alice") -> dict[str, Any]:
    response = client.post("/api/backups/export", headers=auth(user))
    assert response.status_code == 200, response.text
    return cast(dict[str, Any], response.json())


def state(client: HttpTestClient) -> dict[str, Any]:
    response = client.get("/api/workspace", headers=auth())
    assert response.status_code == 200, response.text
    return cast(dict[str, Any], response.json())


def add_stock(client: HttpTestClient, amount: int | None = None) -> dict[str, Any]:
    current = state(client)
    response = client.post(
        "/api/pantry-lots",
        headers=auth(),
        json={
            "expectedVersion": current["version"],
            "id": str(uuid4()),
            "foodId": stable_id("food", "food_73e2d88788"),
            "quantity": {"value": amount, "unit": "g"},
            "location": "冷蔵",
        },
    )
    assert response.status_code == 200, response.text
    return cast(dict[str, Any], response.json())


def preview(client: HttpTestClient, document: dict[str, Any]) -> dict[str, Any]:
    response = client.post("/api/backups/preview", headers=auth(), json={"backup": document})
    assert response.status_code == 200, response.text
    return cast(dict[str, Any], response.json())


def restore_body(document: dict[str, Any], confirmation: dict[str, Any]) -> dict[str, Any]:
    return {
        "backup": document,
        "intentId": confirmation["intentId"],
        "expectedVersion": confirmation["expectedVersion"],
        "confirmed": True,
    }


def test_backup_database_round_trip_preserves_complete_rows_and_decimal(
    backup_client: tuple[HttpTestClient, psycopg.Connection[dict[str, Any]]],
) -> None:
    """Given私有食品・未知数量・正確な小数 When確認後復元 Then全列同値で共有/別人不変。"""
    client, db = backup_client
    initial = state(client)
    custom_id = str(uuid4())
    custom = client.post(
        "/api/foods/custom",
        headers=auth(),
        json={
            "expectedVersion": initial["version"],
            "food": {
                "id": custom_id,
                "name": "復元用の食材",
                "category": "その他",
                "aliases": [],
                "defaultUnit": "g",
                "location": "冷蔵",
                "pantry": False,
                "imageIndex": None,
                "componentsKnown": False,
                "componentFoodIds": [],
            },
        },
    )
    assert custom.status_code == 200, custom.text
    add_stock(client)
    option = db.execute("SELECT id FROM recipeweave.axis_option ORDER BY id LIMIT 1").fetchone()
    assert option
    preference_id = uuid4()
    exact = Decimal("12345678901234.123456")
    db.execute(
        "INSERT INTO recipeweave.user_preference (id,user_id,option_id,weight) "
        "VALUES (%s,%s,%s,%s)",
        (preference_id, account(), option["id"], exact),
    )
    original = export(client)
    other_before = export(client, "bob")
    db.execute("SELECT set_config('recipeweave.role', 'admin', true)")
    catalog_before = db.execute(
        "SELECT id, title, status FROM recipeweave.recipe ORDER BY id"
    ).fetchall()
    changed = add_stock(client, 5)
    confirmation = preview(client, original)
    assert confirmation["expectedVersion"] == changed["version"]
    assert len(confirmation["counts"]) == 34
    assert state(client) == changed
    response = client.post(
        "/api/backups/restore", headers=auth(), json=restore_body(original, confirmation)
    )
    assert response.status_code == 200, response.text
    assert response.json()["version"] == changed["version"] + 1
    after = export(client)
    assert after["tables"] == original["tables"]
    assert after["profile"] == original["profile"]
    assert any(row["amount"] is None for row in after["tables"]["pantry_lot"])
    row = next(row for row in after["tables"]["user_preference"] if row["id"] == str(preference_id))
    assert row["weight"] == str(exact)
    actual = db.execute(
        "SELECT weight FROM recipeweave.user_preference WHERE id=%s", (preference_id,)
    ).fetchone()
    assert actual and actual["weight"] == exact
    assert export(client, "bob")["tables"] == other_before["tables"]
    db.execute("SELECT set_config('recipeweave.role', 'admin', true)")
    assert (
        db.execute("SELECT id, title, status FROM recipeweave.recipe ORDER BY id").fetchall()
        == catalog_before
    )


def test_backup_database_tamper_foreign_owner_cas_and_single_use(
    backup_client: tuple[HttpTestClient, psycopg.Connection[dict[str, Any]]],
) -> None:
    """Given発行済み本人ファイル When改竄/別人/更新競合/再送 Then変更せず拒否。"""
    client, _ = backup_client
    original = export(client)
    tampered = copy.deepcopy(original)
    tampered["profile"]["timezone"] = "UTC"
    rejected = client.post("/api/backups/preview", headers=auth(), json={"backup": tampered})
    assert rejected.status_code == 403
    foreign = client.post("/api/backups/preview", headers=auth("bob"), json={"backup": original})
    assert foreign.status_code == 403
    confirmation = preview(client, original)
    changed = add_stock(client, 3)
    stale = client.post(
        "/api/backups/restore", headers=auth(), json=restore_body(original, confirmation)
    )
    assert stale.status_code == 409
    assert state(client) == changed
    confirmation = preview(client, original)
    body = restore_body(original, confirmation)
    cancelled = client.post(
        "/api/backups/restore", headers=auth(), json={**body, "confirmed": False}
    )
    assert cancelled.status_code == 422
    accepted = client.post("/api/backups/restore", headers=auth(), json=body)
    assert accepted.status_code == 200, accepted.text
    replay = client.post("/api/backups/restore", headers=auth(), json=body)
    assert replay.status_code == 409


def test_backup_database_late_failure_rolls_back_rows_revision_and_intent(
    backup_client: tuple[HttpTestClient, psycopg.Connection[dict[str, Any]]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Given置換/確認消費/版更新後のDB失敗 When監査追記 Then全部戻し確認も未使用。"""
    client, db = backup_client
    original = export(client)
    changed = add_stock(client, 7)
    before = export(client)
    confirmation = preview(client, original)
    actual_run = OperationQueries.run

    def fail_audit(self: OperationQueries, query_name: str, **values: Any) -> list[dict[str, Any]]:
        if self.operation == "backup/restore_backup" and query_name == "q902_append_audit":
            self.connection.execute(
                "DO $$ BEGIN RAISE check_violation USING MESSAGE='試験用の監査失敗'; END $$"
            )
        return actual_run(self, query_name, **values)

    monkeypatch.setattr(OperationQueries, "run", fail_audit)
    response = client.post(
        "/api/backups/restore", headers=auth(), json=restore_body(original, confirmation)
    )
    assert response.status_code == 409, response.text
    assert state(client) == changed
    assert export(client)["tables"] == before["tables"]
    intent = db.execute(
        "SELECT consumed_at FROM recipeweave.backup_restore_intent WHERE id=%s",
        (UUID(confirmation["intentId"]),),
    ).fetchone()
    assert intent and intent["consumed_at"] is None


def test_backup_database_preserves_completed_cooking_receipts_and_consumption(
    backup_client: tuple[HttpTestClient, psycopg.Connection[dict[str, Any]]],
) -> None:
    """Givenレシート・手動時間・調理完了 When全置換 Then原始ID/入力hash/消費台帳を保持。"""
    client, _ = backup_client
    current = state(client)
    if current["cooking"] and current["cooking"]["status"] != "completed":
        previous = copy.deepcopy(current["cooking"])
        previous["completedStepIds"] = [step["key"] for step in previous["plan"]]
        previous["index"] = len(previous["plan"])
        previous["status"] = "completed"
        completed_previous = client.patch(
            "/api/cooking-sessions/" + previous["id"],
            headers=auth(),
            json={"expectedVersion": current["version"], "session": previous, "deduct": False},
        )
        assert completed_previous.status_code == 200, completed_previous.text
        current = completed_previous.json()
    recipe_response = client.get(
        "/api/recipes/" + stable_id("recipe", "tomato-egg"),
        headers=auth(),
        params={"preview": "true"},
    )
    assert recipe_response.status_code == 200, recipe_response.text
    recipe = recipe_response.json()
    receipt_id = str(uuid4())
    candidates = [
        {
            "id": str(uuid4()),
            "rawText": line["foodId"],
            "foodId": line["foodId"],
            "quantity": line["quantity"],
            "selected": True,
            "status": "matched",
            "reason": "復元試験で数量を確認",
        }
        for line in recipe["ingredients"]
    ]
    receipt = client.post(
        "/api/receipts/commit",
        headers=auth(),
        json={
            "expectedVersion": current["version"],
            "id": receipt_id,
            "imageHash": secrets.token_hex(32),
            "purchaseSignature": secrets.token_hex(32),
            "allowDuplicate": False,
            "customFoods": [],
            "candidates": candidates,
        },
    )
    assert receipt.status_code == 200, receipt.text
    current = receipt.json()
    meal = {
        "id": str(uuid4()),
        "recipeId": recipe["id"],
        "recipeVersionId": recipe["versionId"],
        "servings": recipe["servings"],
        "amounts": {line["ingredientId"]: line["quantity"] for line in recipe["ingredients"]},
        "adjusted": False,
    }
    session: dict[str, Any] = {
        "id": str(uuid4()),
        "mealSnapshot": [meal],
        "plan": [],
        "index": 0,
        "completedStepIds": [],
        "timers": [],
        "status": "active",
        "consumptionResults": [],
    }
    estimates = [
        {
            "mealItemId": meal["id"],
            "stepId": step["id"],
            "durationSeconds": int(step["minutes"] * 60 + 30),
        }
        for step in recipe["steps"]
    ]
    started = client.post(
        "/api/cooking-sessions",
        headers=auth(),
        json={
            "expectedVersion": current["version"],
            "session": session,
            "deduct": False,
            "durationEstimates": estimates,
        },
    )
    assert started.status_code == 200, started.text
    cooking = copy.deepcopy(started.json()["cooking"])
    cooking["completedStepIds"] = [step["key"] for step in cooking["plan"]]
    cooking["index"] = len(cooking["plan"])
    cooking["status"] = "completed"
    completed = client.patch(
        "/api/cooking-sessions/" + session["id"],
        headers=auth(),
        json={"expectedVersion": started.json()["version"], "session": cooking, "deduct": True},
    )
    assert completed.status_code == 200, completed.text
    original = export(client)
    original_session = next(
        row for row in original["tables"]["cooking_session"] if row["id"] == session["id"]
    )
    assert original_session["status"] == "completed"
    assert any(
        row["session_id"] == session["id"] for row in original["tables"]["pantry_consumption"]
    )
    tasks = [
        row for row in original["tables"]["session_task"] if row["session_id"] == session["id"]
    ]
    assert tasks and all(row["duration_source"] == "user_estimate" for row in tasks)
    assert all(row["confirmed_duration_s"] is not None for row in tasks)
    assert any(row["id"] == receipt_id for row in original["tables"]["receipt_import"])
    add_stock(client, 20)
    confirmation = preview(client, original)
    restored = client.post(
        "/api/backups/restore", headers=auth(), json=restore_body(original, confirmation)
    )
    assert restored.status_code == 200, restored.text
    assert export(client)["tables"] == original["tables"]


def test_backup_database_export_proof_restores_withdrawn_history_without_self_grant(
    backup_client: tuple[HttpTestClient, psycopg.Connection[dict[str, Any]]],
) -> None:
    """Given正当に発行後に履歴消失/版取下げ When本人の同一本文を復元 Then元履歴だけ回復。"""
    client, db = backup_client
    state(client)
    recipe_id, version_id, event_id = uuid4(), uuid4(), uuid4()
    db.execute("SELECT set_config('recipeweave.role', 'admin', true)")
    db.execute(
        "INSERT INTO recipeweave.recipe (id,title,family_option_id,status) "
        "SELECT %s, '履歴復元の検証', family_option_id, 'draft' "
        "FROM recipeweave.recipe WHERE id=%s",
        (recipe_id, UUID(stable_id("recipe", "tomato-egg"))),
    )
    db.execute(
        "INSERT INTO recipeweave.recipe_version "
        "(id,recipe_id,version,release_id,base_servings,output_amount,output_unit_id,"
        "status,validation,content_hash,description) "
        "SELECT %s,%s,1,release_id,base_servings,output_amount,output_unit_id,"
        "'draft','needs_review',content_hash,description "
        "FROM recipeweave.recipe_version WHERE id=%s",
        (version_id, recipe_id, UUID(stable_id("recipe_version", "tomato-egg/1"))),
    )
    db.execute(
        "INSERT INTO recipeweave.user_recipe_event "
        "(id,user_id,recipe_version_id,kind,occurred_at,request_key) "
        "VALUES (%s,%s,%s,'liked',NOW(),%s)",
        (event_id, account(), version_id, str(uuid4())),
    )
    original = export(client)
    db.execute("DELETE FROM recipeweave.user_recipe_event WHERE id=%s", (event_id,))
    db.execute("SELECT set_config('recipeweave.role', 'admin', true)")
    db.execute(
        "UPDATE recipeweave.recipe SET status='withdrawn',"
        "withdrawal_reason='復元の境界検証' WHERE id=%s",
        (recipe_id,),
    )
    db.execute(
        "UPDATE recipeweave.recipe_version SET status='withdrawn' WHERE id=%s", (version_id,)
    )
    assert not db.execute(
        "SELECT id FROM recipeweave.user_recipe_event WHERE id=%s", (event_id,)
    ).fetchall()
    confirmation = preview(client, original)
    restored = client.post(
        "/api/backups/restore", headers=auth(), json=restore_body(original, confirmation)
    )
    assert restored.status_code == 200, restored.text
    after = export(client)
    assert after["tables"] == original["tables"]
    foreign = client.post("/api/backups/preview", headers=auth("bob"), json={"backup": original})
    assert foreign.status_code == 403
    altered = copy.deepcopy(original)
    altered["tables"]["user_recipe_event"][-1]["recipe_version_id"] = str(uuid4())
    tampered = client.post("/api/backups/preview", headers=auth(), json={"backup": altered})
    assert tampered.status_code == 403
