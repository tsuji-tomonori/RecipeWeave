from typing import Literal

from pydantic import ConfigDict, Field

from app.core.models import Recipe, WireModel


class RecipeSearch(WireModel):
    model_config = ConfigDict(strict=False)
    q: str = Field(default="", max_length=100)
    selected_food_ids: list[str] = Field(default_factory=list, max_length=100)
    excluded_food_ids: list[str] = Field(default_factory=list, max_length=100)
    match: Literal["all", "any"] = "all"
    max_minutes: float | None = Field(default=None, gt=0, le=1440)
    equipment: list[str] = Field(default_factory=list, max_length=50)


class RecipesResponse(WireModel):
    items: list[Recipe]
    total: int
    sample: Literal[True] = True
