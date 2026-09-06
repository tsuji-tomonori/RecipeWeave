"""公開条件と所有設備を検証し、DBを書き換えず調理の段取りを計算する。"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import HTTPException
from psycopg import Connection
from pydantic import Field

from app.core.cooking_planner import build_plan
from app.core.identity import Identity, local_auth_enabled
from app.core.models import MealItem, PlannedStep, Recipe, WireModel
from app.core.operation_queries import OperationQueries
from app.integrations.catalog.postgres_provider import PostgresCatalog


class PlanRequest(WireModel):
    """未保存の分量調整も、明示した料理版の材料行だけへ適用する。"""

    items: Annotated[list[MealItem], Field(min_length=1, max_length=50)]


class PlanResponse(WireModel):
    """保存済みの調理タスクと共通の表示形式。"""

    plan: list[PlannedStep]


def _uuid(value: str | None) -> UUID:
    try:
        return UUID(value or "")
    except ValueError as exc:
        raise HTTPException(422, "料理・材料・献立の識別子を確認してください") from exc


def validate_item(item: MealItem, recipe: Recipe) -> None:
    """同一食品の複数材料行を混同せず、単位や未知量の不整合を拒否する。"""
    keys = {ingredient.ingredient_id for ingredient in recipe.ingredients}
    if None in keys or set(item.amounts) != keys:
        raise HTTPException(422, "指定した料理版と材料の構成が一致しません")
    for ingredient in recipe.ingredients:
        if ingredient.ingredient_id is None:
            raise HTTPException(422, "材料行の識別子が登録されていません")
        amount = item.amounts[ingredient.ingredient_id]
        if amount.value is None or amount.unit != ingredient.quantity.unit:
            raise HTTPException(422, "材料の量を確定し、登録済みの単位で指定してください")


class CookingPlanService:
    """読み取りSQLだけを呼び、調理開始と共通のDAG計画器を使う。"""

    def __init__(self, connection: Connection[dict[str, Any]], identity: Identity) -> None:
        self.connection = connection
        self.identity = identity

    def preview(self, request: PlanRequest) -> PlanResponse:
        """最新の設備と閲覧可能な料理版から、変更を保存せず計算する。"""
        catalog = PostgresCatalog(self.connection)
        queries = OperationQueries(self.connection, "workspace/preview_cooking_plan")
        recipes: dict[UUID, Recipe] = {}
        steps: list[dict[str, Any]] = []
        dependencies: list[dict[str, Any]] = []
        requirements: dict[tuple[UUID, UUID], dict[str, Any]] = {}
        for position, item in enumerate(request.items):
            item_id = _uuid(item.id)
            if item_id in recipes:
                raise HTTPException(422, "同じ献立行が重複しています")
            recipe_rows, _ = catalog.recipes(
                operation="get_recipe",
                recipe_id=_uuid(item.recipe_id),
                version_id=_uuid(item.recipe_version_id),
                owner_id=self.identity.user_id,
                preview=local_auth_enabled(),
            )
            if not recipe_rows:
                raise HTTPException(404, "この料理版は利用できません")
            recipe = recipe_rows[0]
            validate_item(item, recipe)
            recipes[item_id] = recipe
            version_id = _uuid(recipe.version_id)
            steps.extend(
                queries.run(
                    "q001_steps",
                    item_id=item_id,
                    position=position,
                    servings=item.servings,
                    version_id=version_id,
                )
            )
            dependencies.extend(
                queries.run("q002_dependencies", item_id=item_id, version_id=version_id)
            )
            for row in queries.run("q003_requirements", version_id=version_id):
                requirements[(row["step_id"], row["resource_type_id"])] = row
        resources = queries.run("q004_resources", user_id=self.identity.user_id)
        try:
            tasks = build_plan(steps, dependencies, list(requirements.values()), resources)
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        resource_names = {row["id"]: row["name"] for row in resources}
        result: list[PlannedStep] = []
        for task in tasks:
            recipe = recipes[task.item_id]
            step = next(step for step in recipe.steps if step.id == str(task.step_id))
            result.append(
                PlannedStep.model_validate(
                    {
                        **step.model_dump(),
                        "key": f"{task.item_id}:{task.step_id}",
                        "meal_item_id": str(task.item_id),
                        "recipe_id": recipe.id,
                        "recipe_name": recipe.name,
                        "minutes": (task.end - task.start) / 60,
                        "start_minute": task.start / 60,
                        "end_minute": task.end / 60,
                        "equipment": [
                            resource_names[resource_id] for resource_id, _ in task.reservations
                        ],
                    }
                )
            )
        return PlanResponse(plan=result)
