from uuid import UUID

from pydantic import ConfigDict, Field

from app.core.models import Recipe, WireModel


class RandomRecipeSearch(WireModel):
    model_config = ConfigDict(strict=False)
    exclude_id: UUID | None = None
    excluded_food_ids: list[UUID] = Field(default_factory=list[UUID], max_length=100)
    preview: bool = False


class RandomRecipeResponse(WireModel):
    item: Recipe | None
    total: int
