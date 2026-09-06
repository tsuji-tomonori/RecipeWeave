from typing import Literal
from uuid import UUID

from pydantic import ConfigDict, Field

from app.core.models import Recipe, WireModel


class RecipeSearch(WireModel):
    model_config = ConfigDict(strict=False)
    q: str = Field(default="", max_length=100)
    selected_food_ids: list[UUID] = Field(default_factory=list[UUID], max_length=100)
    excluded_food_ids: list[UUID] = Field(default_factory=list[UUID], max_length=100)
    match: Literal["all", "any"] = "all"
    max_minutes: float | None = Field(default=None, gt=0, le=1440)
    equipment: list[str] = Field(default_factory=list[str], max_length=50)
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0, le=1000000)
    preview: bool = False


class RecipesResponse(WireModel):
    items: list[Recipe]
    total: int
    limit: int
    offset: int
