"""実HTTP要求ごとのコミット・在庫・レシート・献立調理の業務動線を検査する。"""

import copy
import os
import secrets
import time
from collections.abc import Iterator
from typing import TYPE_CHECKING, Any, Protocol, cast
from uuid import UUID, uuid4

import httpx
import jwt
import psycopg
import pytest
from database.seed import build_seed, insert_seed, stable_id
from fastapi.testclient import TestClient
from psycopg.rows import dict_row

from app.core.dependencies import get_settings
from app.main import create_app

if TYPE_CHECKING:
    from cryptography.hazmat.primitives.asymmetric import rsa

    from app.integrations.auth.cognito_provider import CognitoVerifier


class WorkflowClient(Protocol):
    def get(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
    ) -> httpx.Response: ...

    def post(
        self, url: str, *, headers: dict[str, str] | None = None, json: Any = None
    ) -> httpx.Response: ...

    def patch(
        self, url: str, *, headers: dict[str, str] | None = None, json: Any = None
    ) -> httpx.Response: ...

    def put(
        self, url: str, *, headers: dict[str, str] | None = None, json: Any = None
    ) -> httpx.Response: ...


@pytest.fixture(scope="module")
def workflow_client() -> Iterator[WorkflowClient]:
    """接続依存を置き換えず、実際の要求単位commitの成否を確認する。"""
    database_url = os.environ.get("TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("業務動線の実DB検証にはTEST_DATABASE_URLを指定する")
    with psycopg.Connection[dict[str, Any]].connect(database_url, row_factory=dict_row) as db:
        db.execute("SELECT set_config('recipeweave.role', 'admin', true)")
        insert_seed(db, build_seed())
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("DATABASE_URL", database_url)
        patch.setenv("AUTH_MODE", "local")
        patch.setenv("ENVIRONMENT", "test")
        patch.setenv("LOCAL_AUTH_SECRET", secrets.token_hex(32))
        patch.setenv("LOCAL_AUTH_PASSWORD", secrets.token_urlsafe(24))
        patch.delenv("AWS_LAMBDA_FUNCTION_NAME", raising=False)
        get_settings.cache_clear()
        with TestClient(create_app(), raise_server_exceptions=False) as client:
            yield cast(WorkflowClient, client)
        get_settings.cache_clear()


def headers(subject: str = "alice") -> dict[str, str]:
    now = int(time.time())
    token = jwt.encode(
        {
            "sub": "local:" + subject,
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


def workspace(client: WorkflowClient, subject: str = "alice") -> dict[str, Any]:
    response = client.get("/api/workspace", headers=headers(subject))
    assert response.status_code == 200, response.text
    return cast(dict[str, Any], response.json())


def stock_body(version: int, food_id: str, amount: float | None) -> dict[str, Any]:
    return {
        "expectedVersion": version,
        "id": str(uuid4()),
        "foodId": food_id,
        "quantity": {"value": amount, "unit": "g"},
        "form": "標準",
        "location": "冷蔵",
        "priority": False,
        "expiresOn": None,
    }


def receipt_body(version: int, food_id: str, amount: float | None) -> dict[str, Any]:
    return {
        "expectedVersion": version,
        "id": str(uuid4()),
        "imageHash": secrets.token_hex(32),
        "purchaseSignature": secrets.token_hex(32),
        "allowDuplicate": False,
        "customFoods": [],
        "candidates": [
            {
                "id": str(uuid4()),
                "rawText": "にんじん",
                "foodId": food_id,
                "quantity": {"value": amount, "unit": "g"},
                "selected": True,
                "status": "matched",
                "reason": "利用者が食品を確認",
            }
        ],
    }


def test_unknown_stock_and_atomic_revision_conflict(workflow_client: WorkflowClient) -> None:
    initial = workspace(workflow_client)
    food_id = stable_id("food", "food_73e2d88788")
    body = stock_body(initial["version"], food_id, None)
    created = workflow_client.post("/api/pantry-lots", headers=headers(), json=body)
    assert created.status_code == 200, created.text
    current = created.json()
    lot = next(row for row in current["lots"] if row["id"] == body["id"])
    assert lot["quantity"] == {"value": None, "unit": "g"}
    assert lot["originalQuantity"]["value"] is None
    stale = stock_body(initial["version"], food_id, 20)
    conflict = workflow_client.post("/api/pantry-lots", headers=headers(), json=stale)
    assert conflict.status_code == 409
    latest = workspace(workflow_client)
    assert latest["version"] == current["version"]
    assert all(row["id"] != stale["id"] for row in latest["lots"])


def test_receipt_unknown_amount_duplicate_and_zero_boundary(
    workflow_client: WorkflowClient,
) -> None:
    food_id = stable_id("food", "food_73e2d88788")
    original = workspace(workflow_client)
    body = receipt_body(original["version"], food_id, None)
    created = workflow_client.post("/api/receipts/commit", headers=headers(), json=body)
    assert created.status_code == 200, created.text
    current = created.json()
    lot = next(row for row in current["lots"] if row["sourceImportId"] == body["id"])
    assert lot["quantity"]["value"] is None
    duplicate = {**body, "expectedVersion": current["version"], "id": str(uuid4())}
    rejected = workflow_client.post("/api/receipts/commit", headers=headers(), json=duplicate)
    assert rejected.status_code == 409
    assert workspace(workflow_client)["version"] == current["version"]
    zero = receipt_body(current["version"], food_id, 0)
    rejected_zero = workflow_client.post("/api/receipts/commit", headers=headers(), json=zero)
    assert rejected_zero.status_code == 422
    assert workspace(workflow_client)["version"] == current["version"]


def test_receipt_partial_undo_preserves_edited_stock(workflow_client: WorkflowClient) -> None:
    current = workspace(workflow_client)
    food_id = stable_id("food", "food_73e2d88788")
    body = receipt_body(current["version"], food_id, 100)
    body["candidates"].append({**body["candidates"][0], "id": str(uuid4())})
    added = workflow_client.post("/api/receipts/commit", headers=headers(), json=body)
    assert added.status_code == 200, added.text
    state = added.json()
    receipt_lots = [row for row in state["lots"] if row["sourceImportId"] == body["id"]]
    assert len(receipt_lots) == 2
    edited_id = receipt_lots[0]["id"]
    update = {
        "expectedVersion": state["version"],
        "foodId": food_id,
        "quantity": {"value": 80, "unit": "g"},
        "form": "標準",
        "location": "冷蔵",
        "priority": False,
        "expiresOn": None,
        "restore": False,
    }
    changed = workflow_client.patch("/api/pantry-lots/" + edited_id, headers=headers(), json=update)
    assert changed.status_code == 200, changed.text
    undone = workflow_client.post(
        "/api/receipts/" + body["id"] + "/undo",
        headers=headers(),
        json={"expectedVersion": changed.json()["version"]},
    )
    assert undone.status_code == 200, undone.text
    remaining = [row for row in undone.json()["lots"] if row["sourceImportId"] == body["id"]]
    assert next(row for row in remaining if row["id"] == edited_id)["quantity"]["value"] == 80
    assert next(row for row in remaining if row["id"] == edited_id)["status"] == "active"
    assert next(row for row in remaining if row["id"] != edited_id)["status"] == "undone"


def test_deferred_constraint_failure_is_not_reported_as_success(
    workflow_client: WorkflowClient,
) -> None:
    """遅延FK違反を応答前に拒否し、先行した設定削除・版更新も戻す。"""
    initial = workspace(workflow_client)
    invalid = {
        "expectedVersion": initial["version"],
        "settings": {
            "excludedFoodIds": [str(uuid4())],
            "pantryFoodIds": [],
            "equipment": initial["settings"]["equipment"],
        },
    }
    response = workflow_client.put("/api/settings", headers=headers(), json=invalid)
    assert 400 <= response.status_code < 500, response.text
    after = workspace(workflow_client)
    assert after["version"] == initial["version"]
    assert after["settings"] == initial["settings"]


def test_recipe_cooking_is_planned_from_db_and_consumed_once(
    workflow_client: WorkflowClient,
) -> None:
    auth = headers("bob")
    recipe_response = workflow_client.get(
        "/api/recipes/" + stable_id("recipe", "tomato-egg"),
        headers=auth,
        params={"preview": "true"},
    )
    assert recipe_response.status_code == 200, recipe_response.text
    recipe = recipe_response.json()
    assert recipe["versionId"] == stable_id("recipe_version", "tomato-egg/1")
    assert all(line["ingredientId"] for line in recipe["ingredients"])
    assert len({line["ingredientId"] for line in recipe["ingredients"]}) == len(
        recipe["ingredients"]
    )
    requested_servings = 3
    scaled_amounts = {
        line["ingredientId"]: {
            "value": line["quantity"]["value"] * requested_servings / recipe["servings"],
            "unit": line["quantity"]["unit"],
        }
        for line in recipe["ingredients"]
    }
    current = workspace(workflow_client, "bob")
    created_lots: list[str] = []
    for ingredient in recipe["ingredients"]:
        body = stock_body(
            current["version"],
            ingredient["foodId"],
            scaled_amounts[ingredient["ingredientId"]]["value"],
        )
        body["quantity"]["unit"] = ingredient["quantity"]["unit"]
        response = workflow_client.post("/api/pantry-lots", headers=auth, json=body)
        assert response.status_code == 200, response.text
        current = response.json()
        created_lots.append(body["id"])
    session: dict[str, Any] = {
        "id": str(uuid4()),
        "mealSnapshot": [
            {
                "id": str(uuid4()),
                "recipeId": recipe["id"],
                "recipeVersionId": recipe["versionId"],
                "servings": requested_servings,
                "amounts": scaled_amounts,
                "adjusted": False,
            }
        ],
        "plan": [],
        "index": 0,
        "completedStepIds": [],
        "timers": [],
        "status": "active",
        "consumptionResults": [],
    }
    estimates = [
        {
            "mealItemId": session["mealSnapshot"][0]["id"],
            "stepId": step["id"],
            "durationSeconds": int(step["minutes"] * 60 + 30),
        }
        for step in recipe["steps"]
    ]
    before = workspace(workflow_client, "bob")
    rejected = workflow_client.post(
        "/api/cooking-sessions",
        headers=auth,
        json={"expectedVersion": current["version"], "session": session, "deduct": False},
    )
    assert rejected.status_code == 422, rejected.text
    assert workspace(workflow_client, "bob") == before
    unconfirmed = workflow_client.post(
        "/api/cooking-plan", headers=auth, json={"items": session["mealSnapshot"]}
    )
    assert unconfirmed.status_code == 422
    preview = workflow_client.post(
        "/api/cooking-plan",
        headers=auth,
        json={"items": session["mealSnapshot"], "durationEstimates": estimates},
    )
    assert preview.status_code == 200, preview.text
    assert all(task["durationSource"] == "user_estimate" for task in preview.json()["plan"])
    started = workflow_client.post(
        "/api/cooking-sessions",
        headers=auth,
        json={
            "expectedVersion": current["version"],
            "session": session,
            "deduct": False,
            "durationEstimates": estimates,
        },
    )
    assert started.status_code == 200, started.text
    cooking = started.json()["cooking"]
    with psycopg.Connection[dict[str, Any]].connect(
        os.environ["TEST_DATABASE_URL"], row_factory=dict_row
    ) as connection:
        connection.execute("SELECT set_config('recipeweave.role', 'admin', true)")
        roles = connection.execute(
            """SELECT item.role_option_id, relation.option_id AS recipe_role_id, option.label
            FROM recipeweave.cooking_session AS cooking
            JOIN recipeweave.menu_item AS item ON cooking.menu_id = item.menu_id
            JOIN recipeweave.recipe_option AS relation
                ON item.recipe_version_id = relation.recipe_version_id
            JOIN recipeweave.axis_option AS option ON relation.option_id = option.id
            JOIN recipeweave.axis AS axis ON option.axis_id = axis.id
            WHERE cooking.id = %s AND axis.code = 'dish_role'""",
            (session["id"],),
        ).fetchall()
    assert len(roles) == 1
    assert roles[0]["role_option_id"] == roles[0]["recipe_role_id"]
    assert roles[0]["label"] == "主菜"
    with psycopg.Connection[dict[str, Any]].connect(
        os.environ["TEST_DATABASE_URL"], row_factory=dict_row
    ) as connection:
        connection.execute("SELECT set_config('recipeweave.role', 'admin', true)")
        with pytest.raises(psycopg.IntegrityError):
            connection.execute(
                "UPDATE recipeweave.session_task "
                "SET confirmed_duration_s = confirmed_duration_s + 1 "
                "WHERE session_id = %s",
                (UUID(session["id"]),),
            )
    assert cooking["mealSnapshot"][0]["servings"] == 3
    assert all(task["durationSource"] == "user_estimate" for task in cooking["plan"])
    expected_times = {row["stepId"]: row["durationSeconds"] for row in estimates}
    assert {
        task["id"]: task["confirmedDurationSeconds"] for task in cooking["plan"]
    } == expected_times
    assert workspace(workflow_client, "bob")["cooking"]["plan"] == cooking["plan"]
    assert [(row["id"], row["minutes"]) for row in cooking["plan"]] == [
        (row["id"], row["minutes"]) for row in preview.json()["plan"]
    ]
    assert cooking["mealSnapshot"][0]["recipeVersionId"] == recipe["versionId"]
    assert set(cooking["mealSnapshot"][0]["amounts"]) == {
        line["ingredientId"] for line in recipe["ingredients"]
    }
    assert len(cooking["plan"]) == len(recipe["steps"])
    assert {step["id"] for step in cooking["plan"]} == {step["id"] for step in recipe["steps"]}
    finished = copy.deepcopy(cooking)
    finished["completedStepIds"] = [step["key"] for step in cooking["plan"]]
    finished["index"] = len(cooking["plan"])
    finished["status"] = "completed"
    payload = {"expectedVersion": started.json()["version"], "session": finished, "deduct": True}
    completed = workflow_client.patch(
        "/api/cooking-sessions/" + session["id"], headers=auth, json=payload
    )
    assert completed.status_code == 200, completed.text
    state = completed.json()
    assert state["cooking"]["status"] == "completed"
    assert all(row["applied"] for row in state["cooking"]["consumptionResults"])
    assert all(row["quantity"]["value"] == 0 for row in state["lots"] if row["id"] in created_lots)
    replay = workflow_client.patch(
        "/api/cooking-sessions/" + session["id"], headers=auth, json=payload
    )
    assert replay.status_code == 409
    assert workspace(workflow_client, "bob")["version"] == state["version"]


def test_first_cognito_login_initializes_only_internal_resources_once(
    workflow_client: WorkflowClient,
    private_key: "rsa.RSAPrivateKey",
    verifier: "CognitoVerifier",
) -> None:
    """署名を検証した新規利用者へ内部作業枠だけを作り、再ログインで増やさない。"""
    from app.core import identity

    from .conftest import CLIENT_ID, ISSUER, access_token

    subject = "first-login-" + str(uuid4())
    auth = {"Authorization": "Bearer " + access_token(private_key, subject)}

    def configured_verifier(issuer: str, client_id: str) -> "CognitoVerifier":
        assert issuer == ISSUER
        assert client_id == CLIENT_ID
        return verifier

    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("AUTH_MODE", "cognito")
        patch.setenv("COGNITO_ISSUER", ISSUER)
        patch.setenv("COGNITO_CLIENT_ID", CLIENT_ID)
        patch.setattr(identity, "CognitoVerifier", configured_verifier)
        get_settings.cache_clear()
        first = workflow_client.get("/api/workspace", headers=auth)
        assert first.status_code == 200, first.text
        assert first.json()["settings"]["equipment"] == []
        second = workflow_client.get("/api/workspace", headers=auth)
        assert second.status_code == 200, second.text
        assert second.json()["version"] == first.json()["version"]
        with psycopg.Connection[dict[str, Any]].connect(
            os.environ["TEST_DATABASE_URL"], row_factory=dict_row
        ) as connection:
            connection.execute("SELECT set_config('recipeweave.role', 'admin', true)")
            rows = connection.execute(
                """SELECT resource.code, kitchen.capacity, kitchen.quantity, kitchen.active
                FROM recipeweave.kitchen_resource AS kitchen
                JOIN recipeweave.resource_type AS resource ON kitchen.resource_type_id = resource.id
                JOIN recipeweave.app_user AS person ON kitchen.user_id = person.id
                WHERE person.auth_subject = %s ORDER BY resource.code""",
                (subject,),
            ).fetchall()
        assert [row["code"] for row in rows] == ["bowl", "burner", "person"]
        assert all(
            row["capacity"] is None and row["quantity"] == 1 and row["active"] for row in rows
        )
    get_settings.cache_clear()


@pytest.mark.parametrize("subject", ["alice", "bob"])
def test_workspace_set_order_does_not_follow_kitchen_heap_order(
    workflow_client: WorkflowClient, subject: str
) -> None:
    """器具の同値更新で物理行順が変わっても、読取り結果と版を変えない。"""
    before = workspace(workflow_client, subject)
    assert before["settings"]["equipment"]
    with psycopg.Connection[dict[str, Any]].connect(
        os.environ["TEST_DATABASE_URL"], row_factory=dict_row
    ) as connection:
        connection.execute("SELECT set_config('recipeweave.role', 'admin', true)")
        rows = connection.execute(
            """SELECT kitchen.id FROM recipeweave.kitchen_resource AS kitchen
            JOIN recipeweave.app_user AS person ON kitchen.user_id = person.id
            WHERE person.auth_subject = %s ORDER BY kitchen.id DESC""",
            ("local:" + subject,),
        ).fetchall()
        for row in rows:
            connection.execute(
                "UPDATE recipeweave.kitchen_resource SET name = name WHERE id = %s",
                (row["id"],),
            )
    after = workspace(workflow_client, subject)
    assert after == before
    assert after["settings"]["equipment"] == sorted(after["settings"]["equipment"])
    assert after["settings"]["excludedFoodIds"] == sorted(after["settings"]["excludedFoodIds"])
    assert after["settings"]["pantryFoodIds"] == sorted(after["settings"]["pantryFoodIds"])
