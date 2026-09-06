"""正規化DBの操作別SQLから食品・料理の通信モデルを復元する。"""

from typing import Any, Literal
from uuid import UUID

from psycopg import Connection

from app.core.models import Food, Recipe
from app.core.operation_queries import OperationQueries


class PostgresCatalog:
    """実行時にサンプルJSONを参照しないカタログ境界。"""

    def __init__(self, connection: Connection[dict[str, Any]]) -> None:
        self.connection = connection

    def foods(self, query: str = "") -> tuple[list[Food], int]:
        rows = OperationQueries(self.connection, "foods/list_foods").run(
            "q001_select_foods", q=query
        )
        return [Food.model_validate(row) for row in rows[0]["items"]], int(rows[0]["total"])

    def recipes(
        self,
        *,
        operation: Literal["list_recipes", "get_recipe", "random_recipe"],
        query: str = "",
        selected_food_ids: list[UUID] | None = None,
        excluded_food_ids: list[UUID] | None = None,
        match: Literal["all", "any"] = "all",
        max_minutes: float | None = None,
        equipment: list[str] | None = None,
        limit: int = 50,
        offset: int = 0,
        preview: bool = False,
        recipe_id: UUID | None = None,
        exclude_id: UUID | None = None,
    ) -> tuple[list[Recipe], int]:
        queries = {
            "list_recipes": ("recipes/list_recipes", "q001_select_recipes"),
            "get_recipe": ("recipes/get_recipe", "q001_select_recipe"),
            "random_recipe": ("recipes/random_recipe", "q001_random_recipe"),
        }
        slug, statement = queries[operation]
        rows = OperationQueries(self.connection, slug).run(
            statement,
            q=query,
            selected_food_ids=selected_food_ids or [],
            excluded_food_ids=excluded_food_ids or [],
            match=match,
            max_minutes=max_minutes,
            equipment=equipment or [],
            limit=limit,
            offset=offset,
            preview=preview,
            recipe_id=recipe_id,
            exclude_id=exclude_id,
        )
        return [Recipe.model_validate(row) for row in rows[0]["items"]], int(rows[0]["total"])
