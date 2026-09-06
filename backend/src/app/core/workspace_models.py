"""各画面操作の入力。全ワークスペースを書き換える入力型は提供しない。"""

from typing import Annotated, Literal

from pydantic import Field

from app.core.models import (
    CookingSession,
    Food,
    Identifier,
    Location,
    MealItem,
    Quantity,
    Settings,
    ShoppingCheck,
    ShortText,
    WireModel,
)


class RevisionRequest(WireModel):
    expected_version: Annotated[int, Field(ge=0, le=9007199254740990)]


class StockInput(WireModel):
    food_id: Identifier
    quantity: Quantity
    form: ShortText = "標準"
    location: Location = "冷蔵"
    priority: bool = False
    expires_on: Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$")] | None = None


class CreatePantryRequest(RevisionRequest, StockInput):
    id: Identifier


class UpdatePantryRequest(RevisionRequest, StockInput):
    restore: bool = False


class MenuItemRequest(RevisionRequest):
    item: MealItem


class SettingsRequest(RevisionRequest):
    settings: Settings


class ShoppingRequest(RevisionRequest):
    checks: Annotated[list[ShoppingCheck], Field(max_length=1000)]


class CustomFoodRequest(RevisionRequest):
    food: Food


class ReceiptCandidate(WireModel):
    id: Identifier
    raw_text: ShortText
    food_id: Identifier | None
    quantity: Quantity
    selected: bool
    status: Literal["matched", "review", "excluded"]
    reason: ShortText


class ReceiptRequest(RevisionRequest):
    id: Identifier
    image_hash: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    purchase_signature: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    candidates: Annotated[list[ReceiptCandidate], Field(min_length=1, max_length=200)]
    allow_duplicate: bool = False
    custom_foods: Annotated[list[Food], Field(max_length=200)] = Field(default_factory=list)


class CookingRequest(RevisionRequest):
    session: CookingSession
    deduct: bool = False
