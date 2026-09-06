"""実HTTP要求ごとのコミット・在庫・レシート・献立調理の業務動線を検査する。"""

import copy
import os
import secrets
import time
from collections.abc import Iterator
from typing import Any, Protocol, cast
from uuid import uuid4

import httpx
import jwt
import psycopg
import pytest
from database.seed import build_seed, insert_seed, stable_id
from fastapi.testclient import TestClient
from psycopg.rows import dict_row

from app.core.dependencies import get_settings
from app.main import create_app


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
    created = workflow_client.post("/api/pantry/lots", headers=headers(), json=body)
    assert created.status_code == 200, created.text
    current = created.json()
    lot = next(row for row in current["lots"] if row["id"] == body["id"])
    assert lot["quantity"] == {"value": None, "unit": "g"}
    assert lot["originalQuantity"]["value"] is None
    stale = stock_body(initial["version"], food_id, 20)
    conflict = workflow_client.post("/api/pantry/lots", headers=headers(), json=stale)
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
    created = workflow_client.post("/api/receipts", headers=headers(), json=body)
    assert created.status_code == 200, created.text
    current = created.json()
    lot = next(row for row in current["lots"] if row["sourceImportId"] == body["id"])
    assert lot["quantity"]["value"] is None
    duplicate = {**body, "expectedVersion": current["version"], "id": str(uuid4())}
    rejected = workflow_client.post("/api/receipts", headers=headers(), json=duplicate)
    assert rejected.status_code == 409
    assert workspace(workflow_client)["version"] == current["version"]
    zero = receipt_body(current["version"], food_id, 0)
    rejected_zero = workflow_client.post("/api/receipts", headers=headers(), json=zero)
    assert rejected_zero.status_code == 422
    assert workspace(workflow_client)["version"] == current["version"]


def test_receipt_partial_undo_preserves_edited_stock(workflow_client: WorkflowClient) -> None:
    current = workspace(workflow_client)
    food_id = stable_id("food", "food_73e2d88788")
    body = receipt_body(current["version"], food_id, 100)
    body["candidates"].append({**body["candidates"][0], "id": str(uuid4())})
    added = workflow_client.post("/api/receipts", headers=headers(), json=body)
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
    changed = workflow_client.put("/api/pantry/lots/" + edited_id, headers=headers(), json=update)
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
    current = workspace(workflow_client, "bob")
    created_lots = []
    for ingredient in recipe["ingredients"]:
        body = stock_body(current["version"], ingredient["foodId"], ingredient["quantity"]["value"])
        body["quantity"]["unit"] = ingredient["quantity"]["unit"]
        response = workflow_client.post("/api/pantry/lots", headers=auth, json=body)
        assert response.status_code == 200, response.text
        current = response.json()
        created_lots.append(body["id"])
    session = {
        "id": str(uuid4()),
        "mealSnapshot": [
            {
                "id": str(uuid4()),
                "recipeId": recipe["id"],
                "servings": recipe["servings"],
                "amounts": {line["foodId"]: line["quantity"] for line in recipe["ingredients"]},
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
    started = workflow_client.post(
        "/api/cooking",
        headers=auth,
        json={"expectedVersion": current["version"], "session": session, "deduct": False},
    )
    assert started.status_code == 200, started.text
    cooking = started.json()["cooking"]
    assert len(cooking["plan"]) == len(recipe["steps"])
    assert {step["id"] for step in cooking["plan"]} == {step["id"] for step in recipe["steps"]}
    finished = copy.deepcopy(cooking)
    finished["completedStepIds"] = [step["key"] for step in cooking["plan"]]
    finished["index"] = len(cooking["plan"])
    finished["status"] = "completed"
    payload = {"expectedVersion": started.json()["version"], "session": finished, "deduct": True}
    completed = workflow_client.put("/api/cooking/" + session["id"], headers=auth, json=payload)
    assert completed.status_code == 200, completed.text
    state = completed.json()
    assert state["cooking"]["status"] == "completed"
    assert all(row["applied"] for row in state["cooking"]["consumptionResults"])
    assert all(row["quantity"]["value"] == 0 for row in state["lots"] if row["id"] in created_lots)
    replay = workflow_client.put("/api/cooking/" + session["id"], headers=auth, json=payload)
    assert replay.status_code == 409
    assert workspace(workflow_client, "bob")["version"] == state["version"]
