"""frontend/src/lib/types.ts と対応する検証済みの通信モデル。

この範囲を限定したスナップショットは端末データの移行境界であり、
料理・食材・工程の正規化されたデータベースモデルを置き換えない。
"""

from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

Identifier = Annotated[str, Field(min_length=1, max_length=128)]
ShortText = Annotated[str, Field(max_length=500)]
Unit = Literal["g", "ml", "個", "パック", "袋", "缶", "本", "枚", "点"]
Location = Literal["冷蔵", "冷凍", "常温"]
PositiveAmount = Annotated[float, Field(ge=0, le=1000000, allow_inf_nan=False)]
Servings = Annotated[float, Field(gt=0, le=1000, allow_inf_nan=False)]


class WireModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, extra="forbid", strict=True
    )


class Quantity(WireModel):
    value: PositiveAmount | None
    unit: Unit


class Food(WireModel):
    id: Identifier
    name: Annotated[str, Field(min_length=1, max_length=100)]
    aliases: Annotated[list[ShortText], Field(max_length=100)]
    category: ShortText
    default_unit: Unit
    location: Location
    pantry: bool
    image_index: Annotated[int, Field(ge=0)] | None
    components_known: bool
    component_food_ids: Annotated[list[Identifier], Field(max_length=100)]


class RecipeIngredient(WireModel):
    food_id: Identifier
    quantity: Quantity
    form: ShortText
    note: ShortText


class RecipeStep(WireModel):
    id: Identifier
    title: ShortText
    instruction: Annotated[str, Field(max_length=5000)]
    minutes: PositiveAmount
    mode: Literal["active", "passive"]
    equipment: Annotated[list[ShortText], Field(max_length=50)]
    guide: ShortText | None


class Recipe(WireModel):
    id: Identifier
    name: ShortText
    description: Annotated[str, Field(max_length=5000)]
    servings: Servings
    minutes: PositiveAmount
    equipment: Annotated[list[ShortText], Field(max_length=50)]
    ingredients: Annotated[list[RecipeIngredient], Field(max_length=100)]
    steps: Annotated[list[RecipeStep], Field(max_length=100)]
    arrangement_ids: Annotated[list[Identifier], Field(max_length=100)]
    tags: Annotated[list[ShortText], Field(max_length=100)]
    sample: Literal[True]


class RecipeDraft(WireModel):
    recipe_id: Identifier
    servings: Servings
    amounts: dict[Identifier, Quantity]
    adjusted: bool


class MealItem(RecipeDraft):
    id: Identifier


class StockLot(WireModel):
    id: Identifier
    food_id: Identifier
    original_food_id: Identifier
    quantity: Quantity
    original_quantity: Quantity
    form: ShortText
    location: Location
    priority: bool
    expires_on: Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$")] | None
    created_at: ShortText
    updated_at: ShortText
    source_import_id: Identifier | None
    status: Literal["active", "deleted", "undone"]
    consumed: Annotated[list[Quantity], Field(max_length=1000)]
    edited: bool


class ReceiptImport(WireModel):
    id: Identifier
    image_hash: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    purchase_signature: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    created_at: ShortText
    state: Literal["registered", "undone"]
    created_lot_ids: Annotated[list[Identifier], Field(max_length=200)]
    undone_at: ShortText | None


class ShoppingCheck(WireModel):
    key: ShortText
    signature: ShortText
    food_id: Identifier
    quantity: Quantity
    checked_at: ShortText
    archived: bool


class PlannedStep(RecipeStep):
    key: ShortText
    meal_item_id: Identifier
    recipe_id: Identifier
    recipe_name: ShortText
    start_minute: PositiveAmount
    end_minute: PositiveAmount


class CookingTimer(WireModel):
    step_key: ShortText
    started_at: Annotated[float, Field(ge=0, allow_inf_nan=False)]
    duration_seconds: PositiveAmount


class ConsumptionResult(WireModel):
    food_id: Identifier
    quantity: Quantity
    form: ShortText
    applied: bool
    reason: ShortText
    lot_ids: Annotated[list[Identifier], Field(max_length=1000)]


class CookingSession(WireModel):
    id: Identifier
    meal_snapshot: Annotated[list[MealItem], Field(max_length=50)]
    plan: Annotated[list[PlannedStep], Field(max_length=500)]
    index: Annotated[int, Field(ge=0, le=500)]
    completed_step_ids: Annotated[list[Identifier], Field(max_length=500)]
    timers: Annotated[list[CookingTimer], Field(max_length=50)]
    status: Literal["active", "paused", "completed"]
    consumption_results: Annotated[list[ConsumptionResult], Field(max_length=1000)]


class Settings(WireModel):
    excluded_food_ids: Annotated[list[Identifier], Field(max_length=1000)]
    pantry_food_ids: Annotated[list[Identifier], Field(max_length=1000)]
    equipment: Annotated[list[ShortText], Field(max_length=50)]


class SearchFilters(WireModel):
    selected_food_ids: Annotated[list[Identifier], Field(max_length=100)]
    match: Literal["all", "any"]
    max_minutes: PositiveAmount | None
    no_shopping: bool
    equipment: Annotated[list[ShortText], Field(max_length=50)]


class AppSnapshot(WireModel):
    schema_version: Literal[1]
    version: Annotated[int, Field(ge=0)]
    lots: Annotated[list[StockLot], Field(max_length=5000)]
    imports: Annotated[list[ReceiptImport], Field(max_length=1000)]
    drafts: dict[Identifier, RecipeDraft]
    meal: Annotated[list[MealItem], Field(max_length=50)]
    saved: Annotated[list[Identifier], Field(max_length=10000)]
    shopping_checks: Annotated[list[ShoppingCheck], Field(max_length=1000)]
    cooking: CookingSession | None
    settings: Settings
    custom_foods: Annotated[list[Food], Field(max_length=1000)]
    search: SearchFilters

    @model_validator(mode="after")
    def validate_unique_ids(self) -> Self:
        """スナップショット内で識別子が重複する曖昧なデータを拒否する。"""
        for collection in (self.lots, self.imports, self.meal, self.custom_foods):
            ids = [item.id for item in collection]
            if len(ids) != len(set(ids)):
                raise ValueError("duplicate identities in snapshot")
        if len(self.drafts) > 1000:
            raise ValueError("too many drafts")
        return self


class StateEnvelope(WireModel):
    version: Annotated[int, Field(ge=0)]
    snapshot: AppSnapshot | None


class PutStateRequest(WireModel):
    expected_version: Annotated[int, Field(ge=0, le=9223372036854775806)]
    snapshot: AppSnapshot
