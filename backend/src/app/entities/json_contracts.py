"""正本がJSONを許す拡張列の具体契約。数量や外部キーを任意JSONへ退避しない。"""

from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, model_validator


def validate_big_integer(value: str) -> str:
    """Webは10進文字列を使い、DBの符号付き64ビット範囲を超えさせない。"""
    if not -(2**63) <= int(value) < 2**63:
        raise ValueError("64ビット整数の範囲外です")
    return value


BigInteger = Annotated[
    str, Field(pattern=r"^-?(0|[1-9][0-9]{0,18})$"), AfterValidator(validate_big_integer)
]


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class GenerationParameters(ContractModel):
    schema_version: Literal[1] = 1
    temperature: float = Field(ge=0, le=2)
    seed: int | None = None
    max_output_tokens: int = Field(gt=0, le=1_000_000)


class GenerationInput(ContractModel):
    schema_version: Literal[1] = 1
    option_ids: list[UUID] = Field(max_length=1024)
    form_ids: list[UUID] = Field(max_length=1024)
    catalog_release_id: UUID
    policy_version: str = Field(min_length=1, max_length=200)


class Predicate(ContractModel):
    schema_version: Literal[1] = 1
    field: (
        Literal[
            "product.microwave_allowed",
            "step.operation_code",
            "recipe.validation",
            "allergen.presence",
            "resource.capacity",
            "ingredient.amount_mode",
        ]
        | None
    ) = None
    op: Literal["eq", "in", "gt", "exists"] | None = None
    value: str | bool | float | list[str] | None = None
    all: list["Predicate"] | None = Field(default=None, max_length=100)
    any: list["Predicate"] | None = Field(default=None, max_length=100)
    not_: "Predicate | None" = Field(default=None, alias="not")

    @model_validator(mode="after")
    def check_shape(self) -> "Predicate":
        """任意の演算子を拒否し、論理演算の構造と深さを検証する。"""
        choices = [
            self.field is not None,
            self.all is not None,
            self.any is not None,
            self.not_ is not None,
        ]
        if sum(choices) != 1 or (self.field is not None) != (self.op is not None):
            raise ValueError("比較または論理演算を厳密に1種類指定してください")
        pending: list[tuple[Predicate, int]] = [(self, 1)]
        while pending:
            node, depth = pending.pop()
            if depth > 8:
                raise ValueError("述語の再帰は8段階以内です")
            pending.extend((child, depth + 1) for child in (node.all or []) + (node.any or []))
            if node.not_ is not None:
                pending.append((node.not_, depth + 1))
        return self


class RangeValue(ContractModel):
    min: Decimal = Field(ge=0)
    max: Decimal = Field(ge=0)

    @model_validator(mode="after")
    def check_order(self) -> "RangeValue":
        if self.min > self.max:
            raise ValueError("下限は上限以下にしてください")
        return self


class MediaParameters(ContractModel):
    schema_version: Literal[1] = 1
    shape: Literal["cylinder", "leaf", "block", "irregular"]
    thickness_mm: RangeValue | None = None
    view: Literal["overhead", "side", "close_up"]


class ValidationEvidence(ContractModel):
    schema_version: Literal[1] = 1
    path: str = Field(min_length=1, max_length=500)
    expected: str | bool | float | None
    actual: str | bool | float | None
    source_ids: list[UUID] = Field(max_length=100)


class FrozenMenuItem(ContractModel):
    id: UUID
    recipe_version_id: UUID
    servings: Decimal = Field(gt=0)


class FrozenIngredient(ContractModel):
    id: UUID
    form_id: UUID
    amount: Decimal | None = Field(default=None, ge=0)
    unit_id: UUID
    conversion_id: UUID | None = None


class FrozenResource(ContractModel):
    id: UUID
    resource_type_id: UUID
    quantity: int = Field(gt=0)
    capacity: Decimal | None = Field(default=None, gt=0)


class PlannerConfig(ContractModel):
    planner_version: str = Field(min_length=1, max_length=200)
    concurrent_active_tasks: int = Field(ge=1, le=10)


class CookingInput(ContractModel):
    schema_version: Literal[1] = 1
    menu_revision: int = Field(ge=1)
    items: list[FrozenMenuItem] = Field(max_length=100)
    ingredients: list[FrozenIngredient] = Field(max_length=1000)
    resources: list[FrozenResource] = Field(max_length=100)
    planner_config: PlannerConfig


class IngredientRatio(ContractModel):
    form_id: UUID
    amount_per_serving: Decimal = Field(gt=0)
    unit_id: UUID


class CanonicalParameter(ContractModel):
    operation_id: UUID
    parameter_id: UUID
    value: str | bool | float


class CanonicalRecipe(ContractModel):
    schema_version: Literal[1] = 1
    ingredient_ratios: list[IngredientRatio] = Field(max_length=1000)
    operations: list[UUID] = Field(max_length=1000)
    parameters: list[CanonicalParameter] = Field(max_length=1000)
    family_id: UUID


class OutboxPayload(ContractModel):
    schema_version: Literal[1] = 1
    event_id: UUID
    aggregate_id: UUID
    version: int = Field(ge=1)


class ProductPreparation(ContractModel):
    schema_version: Literal[1] = 1
    power_w: Decimal | None = Field(default=None, gt=0)
    water_ml: Decimal | None = Field(default=None, ge=0)
    duration_s: int | None = Field(default=None, gt=0)
    lid: Literal["open", "closed", "vented", "per_label"]


class GenerationTemplateContract(ContractModel):
    schema_version: Literal[2] = 2
    primary_identity_ids: list[UUID] = Field(max_length=10000)
    support_identity_ids: list[UUID] = Field(max_length=10000)
    support_identity_sets: list[Annotated[list[UUID], Field(max_length=3)]] | None = Field(
        default=None, max_length=10000
    )
    support_k: list[Literal[0, 1, 2, 3]] = Field(max_length=4)
    flavor_codes: list[str] = Field(max_length=1000)
    route_codes: list[str] = Field(max_length=1000)
    normalizer_version: str = Field(min_length=1, max_length=200)

    @model_validator(mode="after")
    def check_sets(self) -> "GenerationTemplateContract":
        """同じ設計点を重複して数えないため、集合は整列・一意にする。"""
        for values in (
            self.primary_identity_ids,
            self.support_identity_ids,
            self.support_k,
            self.flavor_codes,
            self.route_codes,
        ):
            if values != sorted(set(values)):
                raise ValueError("候補集合は重複を除いて昇順にしてください")
        if self.support_identity_sets is not None:
            allowed = set(self.support_identity_ids)
            groups: set[tuple[UUID, ...]] = set()
            for group in self.support_identity_sets:
                if group != sorted(set(group)):
                    raise ValueError("副材の組は重複を除いて昇順にしてください")
                if not set(group) <= allowed:
                    raise ValueError("副材の組には許可した副材IDだけを指定してください")
                if len(group) not in self.support_k:
                    raise ValueError("副材の組の要素数はsupport_kに含めてください")
                key = tuple(group)
                if key in groups:
                    raise ValueError("同じ副材の組を複数回指定できません")
                groups.add(key)
        return self
