"""実DBの段取りプレビューが保存操作を伴わず、材料版・工程制約を検証する。"""

from typing import Any, cast
from uuid import uuid4

import pytest

from . import test_workflow_database
from .test_workflow_database import WorkflowClient, headers, workspace

workflow_client = test_workflow_database.workflow_client


def menu_item(client: WorkflowClient) -> dict[str, Any]:
    response = client.get("/api/recipes", headers=headers(), params={"preview": "true"})
    assert response.status_code == 200, response.text
    recipe = response.json()["items"][0]
    return {
        "id": str(uuid4()),
        "recipeId": recipe["id"],
        "recipeVersionId": recipe["versionId"],
        "servings": recipe["servings"],
        "amounts": {
            ingredient["ingredientId"]: ingredient["quantity"]
            for ingredient in recipe["ingredients"]
        },
        "adjusted": False,
    }


def test_preview_has_no_workspace_or_cooking_write(workflow_client: WorkflowClient) -> None:
    """同じ入力を繰り返しても版・在庫・献立・セッションを変更しない。"""
    before = workspace(workflow_client)
    item = menu_item(workflow_client)
    first = workflow_client.post("/api/cooking-plan", headers=headers(), json={"items": [item]})
    assert first.status_code == 200, first.text
    assert first.json()["plan"]
    assert all(step["mealItemId"] == item["id"] for step in first.json()["plan"])
    again = workflow_client.post("/api/cooking-plan", headers=headers(), json={"items": [item]})
    assert again.status_code == 200, again.text
    assert again.json() == first.json()
    assert workspace(workflow_client) == before


@pytest.mark.parametrize("invalid", ["duplicate", "version", "unit", "unknown", "servings"])
def test_preview_rejects_inconsistent_inputs_without_saving(
    workflow_client: WorkflowClient, invalid: str
) -> None:
    """不明量・異なる単位・未確認人数・不可視版・重複行を受理しない。"""
    before = workspace(workflow_client)
    item = menu_item(workflow_client)
    items = [item]
    expected = 422
    if invalid == "duplicate":
        items.append(item)
    elif invalid == "version":
        item["recipeVersionId"] = str(uuid4())
        expected = 404
    elif invalid == "servings":
        item["servings"] = 999
    else:
        quantity = next(iter(cast(dict[str, dict[str, Any]], item["amounts"]).values()))
        if invalid == "unknown":
            quantity["value"] = None
        else:
            quantity["unit"] = "ml" if quantity["unit"] != "ml" else "g"
    response = workflow_client.post("/api/cooking-plan", headers=headers(), json={"items": items})
    assert response.status_code == expected, response.text
    assert workspace(workflow_client) == before


@pytest.mark.parametrize("invalid", ["zero", "fraction", "missing", "duplicate", "wrong_step"])
def test_manual_time_confirmation_rejects_bad_input_without_saving(
    workflow_client: WorkflowClient, invalid: str
) -> None:
    """人数変更の見積りは、各料理版・献立行の整数秒として明示確認する。"""
    before = workspace(workflow_client)
    item = menu_item(workflow_client)
    recipe = workflow_client.get(
        "/api/recipes/" + item["recipeId"],
        headers=headers(),
        params={"preview": "true", "versionId": item["recipeVersionId"]},
    ).json()
    item["servings"] = 3
    estimates = [
        {"mealItemId": item["id"], "stepId": step["id"], "durationSeconds": 90}
        for step in recipe["steps"]
    ]
    if invalid == "zero":
        estimates[0]["durationSeconds"] = 0
    elif invalid == "fraction":
        estimates[0]["durationSeconds"] = 0.5
    elif invalid == "missing":
        estimates.pop()
    elif invalid == "duplicate":
        estimates.append(estimates[0])
    else:
        estimates[0]["stepId"] = str(uuid4())
    response = workflow_client.post(
        "/api/cooking-plan",
        headers=headers(),
        json={"items": [item], "durationEstimates": estimates},
    )
    assert response.status_code == 422, response.text
    assert workspace(workflow_client) == before
