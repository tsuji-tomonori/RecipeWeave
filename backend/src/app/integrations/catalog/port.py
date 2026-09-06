"""カタログ操作が必要とするDB検索結果の境界。"""

from typing import Literal, Protocol
from uuid import UUID

from app.core.models import Food, Recipe


class CatalogPort(Protocol):
    def foods(self, query: str = "") -> tuple[list[Food], int]: ...

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
        version_id: UUID | None = None,
        owner_id: UUID | None = None,
    ) -> tuple[list[Recipe], int]: ...
