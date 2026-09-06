# generate_entity_apis.py による自動生成。直接編集しない。
from datetime import date
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from app.entities.json_contracts import (
    BigInteger,
    CanonicalRecipe,
    CookingInput,
    GenerationInput,
    GenerationParameters,
    GenerationTemplateContract,
    MediaParameters,
    OutboxPayload,
    Predicate,
    ProductPreparation,
    ValidationEvidence,
)


class EntityModel(BaseModel):
    """追加項目を拒否し、行ごとの列契約をOpenAPIへ公開する。"""

    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class SourceRecordRow(EntityModel):
    """根拠資料のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    title: str = Field(description="根拠名", min_length=1, max_length=20000)
    url: str | None = Field(description="公式資料URL", min_length=1, max_length=20000)
    locator: str | None = Field(description="資料内位置", min_length=1, max_length=20000)
    retrieved_at: AwareDatetime | None = Field(description="取得時点")
    content_hash: str | None = Field(description="参照内容のハッシュ", min_length=64, max_length=64)
    license_note: str | None = Field(
        description="利用条件・権利確認", min_length=1, max_length=20000
    )
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class SourceRecordWrite(EntityModel):
    """根拠資料の編集可能列。未指定NULL列はNULLにする。"""

    title: str = Field(description="根拠名", min_length=1, max_length=20000)
    url: str | None = Field(default=None, description="公式資料URL", min_length=1, max_length=20000)
    locator: str | None = Field(
        default=None, description="資料内位置", min_length=1, max_length=20000
    )
    retrieved_at: AwareDatetime | None = Field(default=None, description="取得時点")
    content_hash: str | None = Field(
        default=None, description="参照内容のハッシュ", min_length=64, max_length=64
    )
    license_note: str | None = Field(
        default=None, description="利用条件・権利確認", min_length=1, max_length=20000
    )


class CatalogReleaseRow(EntityModel):
    """カタログ公開版のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    version: str = Field(description="カタログ版番号", min_length=1, max_length=20000)
    manifest_hash: str = Field(
        description="採用したID・内容のハッシュ", min_length=64, max_length=64
    )
    published_at: AwareDatetime | None = Field(description="公開日時")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class CatalogReleaseWrite(EntityModel):
    """カタログ公開版の編集可能列。未指定NULL列はNULLにする。"""

    version: str = Field(description="カタログ版番号", min_length=1, max_length=20000)
    manifest_hash: str = Field(
        description="採用したID・内容のハッシュ", min_length=64, max_length=64
    )
    published_at: AwareDatetime | None = Field(default=None, description="公開日時")


class UnitRow(EntityModel):
    """単位のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    code: str = Field(description="単位コード", min_length=1, max_length=20000)
    name: str = Field(description="表示名", min_length=1, max_length=20000)
    dimension: Literal["mass", "volume", "count", "time", "temperature", "length", "power"] = Field(
        description="物理次元"
    )
    factor: Decimal = Field(
        description="同一次元の基準単位への倍率",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
        gt=0,
    )
    offset: Decimal = Field(
        description="温度等のオフセット", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    status: Literal["active", "retired"] = Field(description="利用状態")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class UnitWrite(EntityModel):
    """単位の編集可能列。未指定NULL列はNULLにする。"""

    code: str = Field(description="単位コード", min_length=1, max_length=20000)
    name: str = Field(description="表示名", min_length=1, max_length=20000)
    dimension: Literal["mass", "volume", "count", "time", "temperature", "length", "power"] = Field(
        description="物理次元"
    )
    factor: Decimal = Field(
        description="同一次元の基準単位への倍率",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
        gt=0,
    )
    offset: Decimal = Field(
        description="温度等のオフセット", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    status: Literal["active", "retired"] = Field(description="利用状態")


class FoodRow(EntityModel):
    """購入・利用食材概念のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    code: str = Field(description="固定食材コード", min_length=1, max_length=20000)
    name: str = Field(description="食材名・加工品種別", min_length=1, max_length=20000)
    kind: Literal["basic", "processed", "ready_meal", "kit", "utility"] = Field(
        description="基本食材か加工食品か"
    )
    parent_id: UUID | None = Field(description="カテゴリ親")
    release_id: UUID = Field(description="所属公開版")
    status: Literal["active", "retired"] = Field(description="新規使用可否")
    owner_id: UUID | None = Field(description="私有食材の所有者。NULLは共通カタログ食材")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class FoodWrite(EntityModel):
    """購入・利用食材概念の編集可能列。未指定NULL列はNULLにする。"""

    code: str = Field(description="固定食材コード", min_length=1, max_length=20000)
    name: str = Field(description="食材名・加工品種別", min_length=1, max_length=20000)
    kind: Literal["basic", "processed", "ready_meal", "kit", "utility"] = Field(
        description="基本食材か加工食品か"
    )
    parent_id: UUID | None = Field(default=None, description="カテゴリ親")
    release_id: UUID = Field(description="所属公開版")
    status: Literal["active", "retired"] = Field(description="新規使用可否")


class FoodAliasRow(EntityModel):
    """食材別名のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    food_id: UUID = Field(description="正規食材")
    alias: str = Field(description="別名・かな", min_length=1, max_length=20000)
    locale: str = Field(description="言語・地域", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class FoodAliasWrite(EntityModel):
    """食材別名の編集可能列。未指定NULL列はNULLにする。"""

    food_id: UUID = Field(description="正規食材")
    alias: str = Field(description="別名・かな", min_length=1, max_length=20000)
    locale: str = Field(description="言語・地域", min_length=1, max_length=20000)


class FoodFormRow(EntityModel):
    """食材形態のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    food_id: UUID = Field(description="対応食材")
    name: str = Field(description="生皮付き・冷凍刻み等", min_length=1, max_length=20000)
    state: Literal["raw", "dry", "frozen", "cooked", "rehydrated", "drained", "peeled", "ready"] = (
        Field(description="処理状態")
    )
    base_unit_id: UUID = Field(description="計算基準単位")
    quantity_basis: Literal["edible", "as_purchased", "drained", "prepared"] = Field(
        description="数量の対象部分"
    )
    status: Literal["active", "retired"] = Field(description="利用状態")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class FoodFormWrite(EntityModel):
    """食材形態の編集可能列。未指定NULL列はNULLにする。"""

    food_id: UUID = Field(description="対応食材")
    name: str = Field(description="生皮付き・冷凍刻み等", min_length=1, max_length=20000)
    state: Literal["raw", "dry", "frozen", "cooked", "rehydrated", "drained", "peeled", "ready"] = (
        Field(description="処理状態")
    )
    base_unit_id: UUID = Field(description="計算基準単位")
    quantity_basis: Literal["edible", "as_purchased", "drained", "prepared"] = Field(
        description="数量の対象部分"
    )
    status: Literal["active", "retired"] = Field(description="利用状態")


class ConversionRow(EntityModel):
    """食材形態別換算のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    form_id: UUID = Field(description="換算対象形態")
    from_unit_id: UUID = Field(description="入力単位")
    to_unit_id: UUID = Field(description="出力単位")
    factor: Decimal = Field(
        description="出力量=入力量x倍率", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    quality: Literal["measured", "manufacturer", "reference", "estimated", "unknown"] = Field(
        description="実測・推定区別"
    )
    source_id: UUID | None = Field(description="換算根拠")
    conditions: str = Field(description="サイズ・温度・すり切り等", min_length=1, max_length=20000)
    release_id: UUID = Field(description="換算版")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ConversionWrite(EntityModel):
    """食材形態別換算の編集可能列。未指定NULL列はNULLにする。"""

    form_id: UUID = Field(description="換算対象形態")
    from_unit_id: UUID = Field(description="入力単位")
    to_unit_id: UUID = Field(description="出力単位")
    factor: Decimal = Field(
        description="出力量=入力量x倍率", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    quality: Literal["measured", "manufacturer", "reference", "estimated", "unknown"] = Field(
        description="実測・推定区別"
    )
    source_id: UUID | None = Field(default=None, description="換算根拠")
    conditions: str = Field(description="サイズ・温度・すり切り等", min_length=1, max_length=20000)
    release_id: UUID = Field(description="換算版")


class FormYieldRow(EntityModel):
    """処理歩留まりのDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    input_form_id: UUID = Field(description="処理前形態")
    output_form_id: UUID = Field(description="処理後形態")
    yield_ratio: Decimal = Field(
        description="出力量/入力量", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    source_id: UUID | None = Field(description="根拠")
    quality: Literal["measured", "manufacturer", "reference", "estimated", "unknown"] = Field(
        description="精度区分"
    )
    conditions: str = Field(description="皮むき・水戻し等の条件", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class FormYieldWrite(EntityModel):
    """処理歩留まりの編集可能列。未指定NULL列はNULLにする。"""

    input_form_id: UUID = Field(description="処理前形態")
    output_form_id: UUID = Field(description="処理後形態")
    yield_ratio: Decimal = Field(
        description="出力量/入力量", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    source_id: UUID | None = Field(default=None, description="根拠")
    quality: Literal["measured", "manufacturer", "reference", "estimated", "unknown"] = Field(
        description="精度区分"
    )
    conditions: str = Field(description="皮むき・水戻し等の条件", min_length=1, max_length=20000)


class ProductRow(EntityModel):
    """市販商品識別のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    food_id: UUID = Field(description="汎用食材との対応")
    brand: str = Field(description="ブランド", min_length=1, max_length=20000)
    name: str = Field(description="商品名", min_length=1, max_length=20000)
    gtin: str | None = Field(description="JAN等(先頭0保持)", min_length=1, max_length=20000)
    status: Literal["active", "retired"] = Field(description="終売はretired")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ProductWrite(EntityModel):
    """市販商品識別の編集可能列。未指定NULL列はNULLにする。"""

    food_id: UUID = Field(description="汎用食材との対応")
    brand: str = Field(description="ブランド", min_length=1, max_length=20000)
    name: str = Field(description="商品名", min_length=1, max_length=20000)
    gtin: str | None = Field(
        default=None, description="JAN等(先頭0保持)", min_length=1, max_length=20000
    )
    status: Literal["active", "retired"] = Field(description="終売はretired")


class ProductVersionRow(EntityModel):
    """商品仕様版のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    product_id: UUID = Field(description="商品")
    version: int = Field(description="仕様版", gt=0)
    form_id: UUID = Field(description="販売形態")
    net_amount: Decimal = Field(
        description="1包装の内容量", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    unit_id: UUID = Field(description="内容量単位")
    drain_amount: Decimal | None = Field(
        description="固形量", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    source_id: UUID = Field(description="メーカー表示根拠")
    preparation_note: str = Field(
        description="容器・加熱方式・表示手順", min_length=1, max_length=20000
    )
    valid_from: date = Field(description="適用開始日")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ProductVersionWrite(EntityModel):
    """商品仕様版の編集可能列。未指定NULL列はNULLにする。"""

    product_id: UUID = Field(description="商品")
    version: int = Field(description="仕様版", gt=0)
    form_id: UUID = Field(description="販売形態")
    net_amount: Decimal = Field(
        description="1包装の内容量", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    unit_id: UUID = Field(description="内容量単位")
    drain_amount: Decimal | None = Field(
        default=None, description="固形量", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    source_id: UUID = Field(description="メーカー表示根拠")
    preparation_note: str = Field(
        description="容器・加熱方式・表示手順", min_length=1, max_length=20000
    )
    valid_from: date = Field(description="適用開始日")


class ProductComponentRow(EntityModel):
    """セット内構成品のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    product_version_id: UUID = Field(description="親商品版")
    form_id: UUID = Field(description="麺・ソース・かやく等")
    name: str = Field(description="構成品名", min_length=1, max_length=20000)
    amount: Decimal | None = Field(
        description="量(不明はNULL)", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    unit_id: UUID | None = Field(description="構成品量単位")
    quality: Literal["measured", "manufacturer", "reference", "estimated", "unknown"] = Field(
        description="数量の根拠"
    )
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ProductComponentWrite(EntityModel):
    """セット内構成品の編集可能列。未指定NULL列はNULLにする。"""

    product_version_id: UUID = Field(description="親商品版")
    form_id: UUID = Field(description="麺・ソース・かやく等")
    name: str = Field(description="構成品名", min_length=1, max_length=20000)
    amount: Decimal | None = Field(
        default=None,
        description="量(不明はNULL)",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
    )
    unit_id: UUID | None = Field(default=None, description="構成品量単位")
    quality: Literal["measured", "manufacturer", "reference", "estimated", "unknown"] = Field(
        description="数量の根拠"
    )


class AllergenRow(EntityModel):
    """アレルゲン概念のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    code: str = Field(description="固定コード", min_length=1, max_length=20000)
    name: str = Field(description="名称", min_length=1, max_length=20000)
    source_id: UUID | None = Field(description="分類出典")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class AllergenWrite(EntityModel):
    """アレルゲン概念の編集可能列。未指定NULL列はNULLにする。"""

    code: str = Field(description="固定コード", min_length=1, max_length=20000)
    name: str = Field(description="名称", min_length=1, max_length=20000)
    source_id: UUID | None = Field(default=None, description="分類出典")


class FoodAllergenRow(EntityModel):
    """食材アレルゲン知識のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    form_id: UUID = Field(description="食材形態")
    allergen_id: UUID = Field(description="対象物質")
    presence: Literal["contains", "may_contain", "absent_verified", "unknown"] = Field(
        description="含有・不明"
    )
    source_id: UUID = Field(description="判断根拠")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class FoodAllergenWrite(EntityModel):
    """食材アレルゲン知識の編集可能列。未指定NULL列はNULLにする。"""

    form_id: UUID = Field(description="食材形態")
    allergen_id: UUID = Field(description="対象物質")
    presence: Literal["contains", "may_contain", "absent_verified", "unknown"] = Field(
        description="含有・不明"
    )
    source_id: UUID = Field(description="判断根拠")


class ProductAllergenRow(EntityModel):
    """商品表示アレルゲンのDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    product_version_id: UUID = Field(description="商品仕様版")
    allergen_id: UUID = Field(description="物質")
    presence: Literal["contains", "may_contain", "absent_verified", "unknown"] = Field(
        description="表示状態"
    )
    source_id: UUID = Field(description="ラベル等")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ProductAllergenWrite(EntityModel):
    """商品表示アレルゲンの編集可能列。未指定NULL列はNULLにする。"""

    product_version_id: UUID = Field(description="商品仕様版")
    allergen_id: UUID = Field(description="物質")
    presence: Literal["contains", "may_contain", "absent_verified", "unknown"] = Field(
        description="表示状態"
    )
    source_id: UUID = Field(description="ラベル等")


class NutrientRow(EntityModel):
    """栄養成分種別のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    code: str = Field(description="energy_kcal等", min_length=1, max_length=20000)
    name: str = Field(description="エネルギー等", min_length=1, max_length=20000)
    unit_label: str = Field(description="kcal/g/mg/μg", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class NutrientWrite(EntityModel):
    """栄養成分種別の編集可能列。未指定NULL列はNULLにする。"""

    code: str = Field(description="energy_kcal等", min_length=1, max_length=20000)
    name: str = Field(description="エネルギー等", min_length=1, max_length=20000)
    unit_label: str = Field(description="kcal/g/mg/μg", min_length=1, max_length=20000)


class NutritionFactRow(EntityModel):
    """形態・商品別栄養値のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    form_id: UUID | None = Field(description="汎用形態")
    product_version_id: UUID | None = Field(description="商品仕様")
    nutrient_id: UUID = Field(description="栄養成分")
    amount: Decimal = Field(
        description="基準量あたり成分量", max_digits=20, decimal_places=6, allow_inf_nan=False, ge=0
    )
    basis_amount: Decimal = Field(
        description="基準量", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    basis_unit_id: UUID = Field(description="基準単位")
    source_id: UUID = Field(description="出典")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class NutritionFactWrite(EntityModel):
    """形態・商品別栄養値の編集可能列。未指定NULL列はNULLにする。"""

    form_id: UUID | None = Field(default=None, description="汎用形態")
    product_version_id: UUID | None = Field(default=None, description="商品仕様")
    nutrient_id: UUID = Field(description="栄養成分")
    amount: Decimal = Field(
        description="基準量あたり成分量", max_digits=20, decimal_places=6, allow_inf_nan=False, ge=0
    )
    basis_amount: Decimal = Field(
        description="基準量", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    basis_unit_id: UUID = Field(description="基準単位")
    source_id: UUID = Field(description="出典")


class AxisRow(EntityModel):
    """組み合わせ軸のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    code: str = Field(description="軸コード", min_length=1, max_length=20000)
    name: str = Field(description="軸名", min_length=1, max_length=20000)
    purpose: Literal["generation", "search", "constraint", "derived", "presentation"] = Field(
        description="生成/検索/制約等"
    )
    selection: Literal["single", "multiple"] = Field(description="単複")
    release_id: UUID = Field(description="定義版")
    status: Literal["active", "retired"] = Field(description="採用状態")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class AxisWrite(EntityModel):
    """組み合わせ軸の編集可能列。未指定NULL列はNULLにする。"""

    code: str = Field(description="軸コード", min_length=1, max_length=20000)
    name: str = Field(description="軸名", min_length=1, max_length=20000)
    purpose: Literal["generation", "search", "constraint", "derived", "presentation"] = Field(
        description="生成/検索/制約等"
    )
    selection: Literal["single", "multiple"] = Field(description="単複")
    release_id: UUID = Field(description="定義版")
    status: Literal["active", "retired"] = Field(description="採用状態")


class AxisOptionRow(EntityModel):
    """軸候補値のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    axis_id: UUID = Field(description="親軸")
    code: str = Field(description="値コード", min_length=1, max_length=20000)
    label: str = Field(description="候補名", min_length=1, max_length=20000)
    definition: str = Field(description="値の意味", min_length=1, max_length=20000)
    parent_id: UUID | None = Field(description="同軸の階層親")
    status: Literal["active", "retired"] = Field(description="選択可否")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class AxisOptionWrite(EntityModel):
    """軸候補値の編集可能列。未指定NULL列はNULLにする。"""

    axis_id: UUID = Field(description="親軸")
    code: str = Field(description="値コード", min_length=1, max_length=20000)
    label: str = Field(description="候補名", min_length=1, max_length=20000)
    definition: str = Field(description="値の意味", min_length=1, max_length=20000)
    parent_id: UUID | None = Field(default=None, description="同軸の階層親")
    status: Literal["active", "retired"] = Field(description="選択可否")


class FoodAxisOptionRow(EntityModel):
    """食材の分類属性のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    food_id: UUID = Field(description="食材")
    option_id: UUID = Field(description="カテゴリ・入手性等の値")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class FoodAxisOptionWrite(EntityModel):
    """食材の分類属性の編集可能列。未指定NULL列はNULLにする。"""

    food_id: UUID = Field(description="食材")
    option_id: UUID = Field(description="カテゴリ・入手性等の値")


class RecipeRow(EntityModel):
    """レシピ同一性のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    title: str = Field(description="代表名", min_length=1, max_length=20000)
    family_option_id: UUID = Field(description="料理ファミリ")
    status: Literal["draft", "published", "withdrawn"] = Field(description="公開状態")
    withdrawal_reason: str | None = Field(description="取下げ理由", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class RecipeWrite(EntityModel):
    """レシピ同一性の編集可能列。未指定NULL列はNULLにする。"""

    title: str = Field(description="代表名", min_length=1, max_length=20000)
    family_option_id: UUID = Field(description="料理ファミリ")
    status: Literal["draft", "published", "withdrawn"] = Field(description="公開状態")
    withdrawal_reason: str | None = Field(
        default=None, description="取下げ理由", min_length=1, max_length=20000
    )


class RecipeVersionRow(EntityModel):
    """レシピ内容版のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    recipe_id: UUID = Field(description="所属レシピ")
    version: int = Field(description="版番号", gt=0)
    release_id: UUID = Field(description="採用カタログ版")
    base_servings: Decimal = Field(
        description="登録分量が何人前か", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    output_amount: Decimal = Field(
        description="完成量", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    output_unit_id: UUID = Field(description="完成量単位")
    status: Literal["draft", "published", "withdrawn"] = Field(description="版の状態")
    validation: Literal["pending", "passed", "failed", "needs_review"] = Field(
        description="公開審査"
    )
    content_hash: str = Field(description="内容ハッシュ", min_length=64, max_length=64)
    published_at: AwareDatetime | None = Field(description="公開日時")
    description: str | None = Field(description="料理の紹介文", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class RecipeVersionWrite(EntityModel):
    """レシピ内容版の編集可能列。未指定NULL列はNULLにする。"""

    recipe_id: UUID = Field(description="所属レシピ")
    version: int = Field(description="版番号", gt=0)
    release_id: UUID = Field(description="採用カタログ版")
    base_servings: Decimal = Field(
        description="登録分量が何人前か", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    output_amount: Decimal = Field(
        description="完成量", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    output_unit_id: UUID = Field(description="完成量単位")
    status: Literal["draft", "published", "withdrawn"] = Field(description="版の状態")
    validation: Literal["pending", "passed", "failed", "needs_review"] = Field(
        description="公開審査"
    )
    content_hash: str = Field(description="内容ハッシュ", min_length=64, max_length=64)
    published_at: AwareDatetime | None = Field(default=None, description="公開日時")
    description: str | None = Field(
        default=None, description="料理の紹介文", min_length=1, max_length=20000
    )


class RecipeOptionRow(EntityModel):
    """版の分類・特徴のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    recipe_version_id: UUID = Field(description="対象版")
    option_id: UUID = Field(description="特徴値")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class RecipeOptionWrite(EntityModel):
    """版の分類・特徴の編集可能列。未指定NULL列はNULLにする。"""

    recipe_version_id: UUID = Field(description="対象版")
    option_id: UUID = Field(description="特徴値")


class ScalingRuleRow(EntityModel):
    """人数変更規則のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    name: str = Field(description="規則名", min_length=1, max_length=20000)
    mode: Literal["linear", "fixed_batch", "capacity_batch", "validated_curve", "manual"] = Field(
        description="比例・バッチ等"
    )
    min_servings: Decimal = Field(
        description="検証済み人数下限", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    max_servings: Decimal = Field(
        description="検証済み人数上限", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    batch_capacity: Decimal | None = Field(
        description="1バッチ上限", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    round_mode: Literal["none", "half_up", "ceil"] = Field(description="表示丸め")
    round_increment: Decimal = Field(
        description="表示・購入の刻み", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    source_id: UUID | None = Field(description="検証根拠")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ScalingRuleWrite(EntityModel):
    """人数変更規則の編集可能列。未指定NULL列はNULLにする。"""

    name: str = Field(description="規則名", min_length=1, max_length=20000)
    mode: Literal["linear", "fixed_batch", "capacity_batch", "validated_curve", "manual"] = Field(
        description="比例・バッチ等"
    )
    min_servings: Decimal = Field(
        description="検証済み人数下限", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    max_servings: Decimal = Field(
        description="検証済み人数上限", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    batch_capacity: Decimal | None = Field(
        default=None,
        description="1バッチ上限",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
    )
    round_mode: Literal["none", "half_up", "ceil"] = Field(description="表示丸め")
    round_increment: Decimal = Field(
        description="表示・購入の刻み", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    source_id: UUID | None = Field(default=None, description="検証根拠")


class ScalingPointRow(EntityModel):
    """検証済み換算点のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    rule_id: UUID = Field(description="曲線規則")
    servings: Decimal = Field(
        description="人数", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    multiplier: Decimal = Field(
        description="登録量への倍率", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ScalingPointWrite(EntityModel):
    """検証済み換算点の編集可能列。未指定NULL列はNULLにする。"""

    rule_id: UUID = Field(description="曲線規則")
    servings: Decimal = Field(
        description="人数", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    multiplier: Decimal = Field(
        description="登録量への倍率", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )


class RecipeIngredientRow(EntityModel):
    """レシピ材料明細のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    recipe_version_id: UUID = Field(description="親版")
    line_no: int = Field(description="表示順", gt=0)
    form_id: UUID = Field(description="使用形態")
    product_version_id: UUID | None = Field(description="商品指定時の仕様版")
    component_id: UUID | None = Field(description="セット内構成品を使う場合")
    kit_parent_line_id: UUID | None = Field(description="購入対象となるセットの親行")
    role: Literal["main", "support", "seasoning", "aroma", "texture", "garnish", "medium"] = Field(
        description="料理での役割"
    )
    demand_kind: Literal["purchase", "utility", "kit_component"] = Field(description="購入対象区分")
    amount_mode: Literal["exact", "range", "to_taste"] = Field(description="確定/範囲/適量")
    amount: Decimal | None = Field(
        description="確定値または範囲下限", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    amount_max: Decimal | None = Field(
        description="範囲上限", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    unit_id: UUID = Field(description="登録単位")
    canonical_amount: Decimal | None = Field(
        description="登録版の基準量", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    conversion_id: UUID | None = Field(description="非基準単位の換算根拠")
    scaling_rule_id: UUID = Field(description="人数変換規則")
    optional: bool = Field(description="任意追加材料")
    note: str | None = Field(description="材料の補足", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class RecipeIngredientWrite(EntityModel):
    """レシピ材料明細の編集可能列。未指定NULL列はNULLにする。"""

    recipe_version_id: UUID = Field(description="親版")
    line_no: int = Field(description="表示順", gt=0)
    form_id: UUID = Field(description="使用形態")
    product_version_id: UUID | None = Field(default=None, description="商品指定時の仕様版")
    component_id: UUID | None = Field(default=None, description="セット内構成品を使う場合")
    kit_parent_line_id: UUID | None = Field(default=None, description="購入対象となるセットの親行")
    role: Literal["main", "support", "seasoning", "aroma", "texture", "garnish", "medium"] = Field(
        description="料理での役割"
    )
    demand_kind: Literal["purchase", "utility", "kit_component"] = Field(description="購入対象区分")
    amount_mode: Literal["exact", "range", "to_taste"] = Field(description="確定/範囲/適量")
    amount: Decimal | None = Field(
        default=None,
        description="確定値または範囲下限",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
    )
    amount_max: Decimal | None = Field(
        default=None, description="範囲上限", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    unit_id: UUID = Field(description="登録単位")
    canonical_amount: Decimal | None = Field(
        default=None,
        description="登録版の基準量",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
    )
    conversion_id: UUID | None = Field(default=None, description="非基準単位の換算根拠")
    scaling_rule_id: UUID = Field(description="人数変換規則")
    optional: bool = Field(description="任意追加材料")
    note: str | None = Field(default=None, description="材料の補足", min_length=1, max_length=20000)


class OperationRow(EntityModel):
    """標準調理動作のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    code: str = Field(description="cut_ginkgo等", min_length=1, max_length=20000)
    name: str = Field(description="いちょう切り等", min_length=1, max_length=20000)
    definition: str = Field(description="動作の意味", min_length=1, max_length=20000)
    precondition: str = Field(description="入力食材・必要状態", min_length=1, max_length=20000)
    completion_cue: str = Field(description="完了確認方法", min_length=1, max_length=20000)
    status: Literal["active", "retired"] = Field(description="使用状態")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class OperationWrite(EntityModel):
    """標準調理動作の編集可能列。未指定NULL列はNULLにする。"""

    code: str = Field(description="cut_ginkgo等", min_length=1, max_length=20000)
    name: str = Field(description="いちょう切り等", min_length=1, max_length=20000)
    definition: str = Field(description="動作の意味", min_length=1, max_length=20000)
    precondition: str = Field(description="入力食材・必要状態", min_length=1, max_length=20000)
    completion_cue: str = Field(description="完了確認方法", min_length=1, max_length=20000)
    status: Literal["active", "retired"] = Field(description="使用状態")


class OperationParameterRow(EntityModel):
    """動作パラメータ定義のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    operation_id: UUID = Field(description="動作")
    code: str = Field(description="thickness_mm等", min_length=1, max_length=20000)
    name: str = Field(description="厚さ等", min_length=1, max_length=20000)
    value_type: Literal["decimal", "integer", "boolean", "text", "option"] = Field(
        description="値型"
    )
    unit_id: UUID | None = Field(description="単位")
    required: bool = Field(description="必須か")
    min_value: Decimal | None = Field(
        description="許容下限", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    max_value: Decimal | None = Field(
        description="許容上限", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    allowed_values: list[str] | None = Field(description="option型の具体値配列")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class OperationParameterWrite(EntityModel):
    """動作パラメータ定義の編集可能列。未指定NULL列はNULLにする。"""

    operation_id: UUID = Field(description="動作")
    code: str = Field(description="thickness_mm等", min_length=1, max_length=20000)
    name: str = Field(description="厚さ等", min_length=1, max_length=20000)
    value_type: Literal["decimal", "integer", "boolean", "text", "option"] = Field(
        description="値型"
    )
    unit_id: UUID | None = Field(default=None, description="単位")
    required: bool = Field(description="必須か")
    min_value: Decimal | None = Field(
        default=None, description="許容下限", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    max_value: Decimal | None = Field(
        default=None, description="許容上限", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    allowed_values: list[str] | None = Field(default=None, description="option型の具体値配列")


class RecipeStepRow(EntityModel):
    """調理工程節点のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    recipe_version_id: UUID = Field(description="所属版")
    step_no: int = Field(description="表示順(依存順とは別)", gt=0)
    operation_id: UUID = Field(description="標準動作")
    instruction: str = Field(description="個別補足", min_length=1, max_length=20000)
    attention: Literal["active", "monitored", "passive"] = Field(description="作業者拘束")
    duration_min_s: int = Field(description="所要秒下限", ge=0)
    duration_max_s: int = Field(description="所要秒上限")
    scaling_rule_id: UUID = Field(description="時間の人数変更規則")
    completion_cue: str = Field(description="実測・目視の終了条件", min_length=1, max_length=20000)
    title: str | None = Field(description="工程の短い見出し", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class RecipeStepWrite(EntityModel):
    """調理工程節点の編集可能列。未指定NULL列はNULLにする。"""

    recipe_version_id: UUID = Field(description="所属版")
    step_no: int = Field(description="表示順(依存順とは別)", gt=0)
    operation_id: UUID = Field(description="標準動作")
    instruction: str = Field(description="個別補足", min_length=1, max_length=20000)
    attention: Literal["active", "monitored", "passive"] = Field(description="作業者拘束")
    duration_min_s: int = Field(description="所要秒下限", ge=0)
    duration_max_s: int = Field(description="所要秒上限")
    scaling_rule_id: UUID = Field(description="時間の人数変更規則")
    completion_cue: str = Field(description="実測・目視の終了条件", min_length=1, max_length=20000)
    title: str | None = Field(
        default=None, description="工程の短い見出し", min_length=1, max_length=20000
    )


class StepParameterRow(EntityModel):
    """工程の型付きパラメータのDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    step_id: UUID = Field(description="対象工程")
    parameter_id: UUID = Field(description="動作パラメータ")
    number_value: Decimal | None = Field(
        description="数値", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    text_value: str | None = Field(description="文字・optionコード", min_length=1, max_length=20000)
    bool_value: bool | None = Field(description="真偽")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class StepParameterWrite(EntityModel):
    """工程の型付きパラメータの編集可能列。未指定NULL列はNULLにする。"""

    step_id: UUID = Field(description="対象工程")
    parameter_id: UUID = Field(description="動作パラメータ")
    number_value: Decimal | None = Field(
        default=None, description="数値", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    text_value: str | None = Field(
        default=None, description="文字・optionコード", min_length=1, max_length=20000
    )
    bool_value: bool | None = Field(default=None, description="真偽")


class MaterialNodeRow(EntityModel):
    """材料・中間物節点のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    recipe_version_id: UUID = Field(description="親版")
    name: str = Field(description="切ったにんじん・合わせ調味料等", min_length=1, max_length=20000)
    kind: Literal["ingredient", "intermediate", "dish", "waste"] = Field(
        description="入力/中間/完成/廃棄"
    )
    ingredient_line_id: UUID | None = Field(description="原材料明細")
    producer_step_id: UUID | None = Field(description="生成工程")
    amount: Decimal | None = Field(
        description="予定生成量", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    unit_id: UUID | None = Field(description="生成量単位")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class MaterialNodeWrite(EntityModel):
    """材料・中間物節点の編集可能列。未指定NULL列はNULLにする。"""

    recipe_version_id: UUID = Field(description="親版")
    name: str = Field(description="切ったにんじん・合わせ調味料等", min_length=1, max_length=20000)
    kind: Literal["ingredient", "intermediate", "dish", "waste"] = Field(
        description="入力/中間/完成/廃棄"
    )
    ingredient_line_id: UUID | None = Field(default=None, description="原材料明細")
    producer_step_id: UUID | None = Field(default=None, description="生成工程")
    amount: Decimal | None = Field(
        default=None, description="予定生成量", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    unit_id: UUID | None = Field(default=None, description="生成量単位")


class StepInputRow(EntityModel):
    """工程への材料受渡しのDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    step_id: UUID = Field(description="受取工程")
    material_id: UUID = Field(description="受け渡す材料")
    fraction: Decimal = Field(
        description="当該節点生成量の利用割合", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class StepInputWrite(EntityModel):
    """工程への材料受渡しの編集可能列。未指定NULL列はNULLにする。"""

    step_id: UUID = Field(description="受取工程")
    material_id: UUID = Field(description="受け渡す材料")
    fraction: Decimal = Field(
        description="当該節点生成量の利用割合", max_digits=20, decimal_places=6, allow_inf_nan=False
    )


class StepDependencyRow(EntityModel):
    """工程依存辺のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    before_step_id: UUID = Field(description="先行工程")
    after_step_id: UUID = Field(description="後続工程")
    kind: Literal["material", "sequence", "safety", "quality"] = Field(description="依存理由")
    min_lag_s: int = Field(description="完了後最低待機", ge=0)
    max_lag_s: int | None = Field(description="品質上の最大待機")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class StepDependencyWrite(EntityModel):
    """工程依存辺の編集可能列。未指定NULL列はNULLにする。"""

    before_step_id: UUID = Field(description="先行工程")
    after_step_id: UUID = Field(description="後続工程")
    kind: Literal["material", "sequence", "safety", "quality"] = Field(description="依存理由")
    min_lag_s: int = Field(description="完了後最低待機", ge=0)
    max_lag_s: int | None = Field(default=None, description="品質上の最大待機")


class ResourceTypeRow(EntityModel):
    """道具・設備・作業者種別のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    code: str = Field(description="burner/pan/person等", min_length=1, max_length=20000)
    name: str = Field(description="道具名", min_length=1, max_length=20000)
    capacity_unit_id: UUID | None = Field(description="鍋容量等の単位")
    status: Literal["active", "retired"] = Field(description="使用状態")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ResourceTypeWrite(EntityModel):
    """道具・設備・作業者種別の編集可能列。未指定NULL列はNULLにする。"""

    code: str = Field(description="burner/pan/person等", min_length=1, max_length=20000)
    name: str = Field(description="道具名", min_length=1, max_length=20000)
    capacity_unit_id: UUID | None = Field(default=None, description="鍋容量等の単位")
    status: Literal["active", "retired"] = Field(description="使用状態")


class StepResourceRow(EntityModel):
    """工程の資源要求のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    step_id: UUID = Field(description="対象工程")
    resource_type_id: UUID = Field(description="要求種別")
    quantity: int = Field(description="必要台数・人数", gt=0)
    capacity_min: Decimal | None = Field(
        description="必要最低容量", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    exclusive: bool = Field(description="占有するか")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class StepResourceWrite(EntityModel):
    """工程の資源要求の編集可能列。未指定NULL列はNULLにする。"""

    step_id: UUID = Field(description="対象工程")
    resource_type_id: UUID = Field(description="要求種別")
    quantity: int = Field(description="必要台数・人数", gt=0)
    capacity_min: Decimal | None = Field(
        default=None,
        description="必要最低容量",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
    )
    exclusive: bool = Field(description="占有するか")


class MediaAssetRow(EntityModel):
    """教育用動画等の版のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    operation_id: UUID = Field(description="説明する標準動作")
    media_type: Literal["video", "animation", "image"] = Field(description="動画/アニメ/画像")
    uri: str = Field(description="オブジェクト格納先", min_length=1, max_length=20000)
    sha256: str = Field(description="資産ハッシュ", min_length=64, max_length=64)
    locale: str = Field(description="字幕言語", min_length=1, max_length=20000)
    version: int = Field(description="媒体版", gt=0)
    parameter_contract: MediaParameters = Field(description="対応厚み・食材形状・視点")
    source_id: UUID = Field(description="権利・作成根拠")
    validation: Literal["pending", "passed", "failed", "needs_review"] = Field(
        description="内容検証"
    )
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class MediaAssetWrite(EntityModel):
    """教育用動画等の版の編集可能列。未指定NULL列はNULLにする。"""

    operation_id: UUID = Field(description="説明する標準動作")
    media_type: Literal["video", "animation", "image"] = Field(description="動画/アニメ/画像")
    uri: str = Field(description="オブジェクト格納先", min_length=1, max_length=20000)
    sha256: str = Field(description="資産ハッシュ", min_length=64, max_length=64)
    locale: str = Field(description="字幕言語", min_length=1, max_length=20000)
    version: int = Field(description="媒体版", gt=0)
    parameter_contract: MediaParameters = Field(description="対応厚み・食材形状・視点")
    source_id: UUID = Field(description="権利・作成根拠")
    validation: Literal["pending", "passed", "failed", "needs_review"] = Field(
        description="内容検証"
    )


class StepMediaRow(EntityModel):
    """工程別メディア選択のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    step_id: UUID = Field(description="対象工程")
    media_id: UUID = Field(description="適用メディア")
    start_ms: int = Field(description="表示開始点", ge=0)
    end_ms: int = Field(description="終了点")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class StepMediaWrite(EntityModel):
    """工程別メディア選択の編集可能列。未指定NULL列はNULLにする。"""

    step_id: UUID = Field(description="対象工程")
    media_id: UUID = Field(description="適用メディア")
    start_ms: int = Field(description="表示開始点", ge=0)
    end_ms: int = Field(description="終了点")


class GenerationPolicyRow(EntityModel):
    """AI生成方針版のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    version: str = Field(description="方針識別子", min_length=1, max_length=20000)
    prompt_template: str = Field(description="入力テンプレ", min_length=1, max_length=20000)
    model_identifier: str = Field(description="利用モデル名・版", min_length=1, max_length=20000)
    parameter_json: GenerationParameters = Field(description="temperature/seed等の記録")
    schema_version: str = Field(description="出力JSON契約", min_length=1, max_length=20000)
    release_id: UUID = Field(description="候補カタログ版")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class GenerationPolicyWrite(EntityModel):
    """AI生成方針版の編集可能列。未指定NULL列はNULLにする。"""

    version: str = Field(description="方針識別子", min_length=1, max_length=20000)
    prompt_template: str = Field(description="入力テンプレ", min_length=1, max_length=20000)
    model_identifier: str = Field(description="利用モデル名・版", min_length=1, max_length=20000)
    parameter_json: GenerationParameters = Field(description="temperature/seed等の記録")
    schema_version: str = Field(description="出力JSON契約", min_length=1, max_length=20000)
    release_id: UUID = Field(description="候補カタログ版")


class GenerationJobRow(EntityModel):
    """事前生成ジョブのDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    policy_id: UUID = Field(description="実行方針")
    idempotency_key: str = Field(
        description="入力と方針から作る重複キー", min_length=64, max_length=64
    )
    status: Literal["queued", "running", "succeeded", "failed", "cancelled"] = Field(
        description="進行状態"
    )
    started_at: AwareDatetime | None = Field(description="開始")
    finished_at: AwareDatetime | None = Field(description="終了")
    seed: int | None = Field(description="再現用seed")
    error_code: str | None = Field(description="失敗分類", min_length=1, max_length=20000)
    attempt_count: int = Field(description="試行回数", ge=0)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class GenerationJobWrite(EntityModel):
    """事前生成ジョブの編集可能列。未指定NULL列はNULLにする。"""

    policy_id: UUID = Field(description="実行方針")
    idempotency_key: str = Field(
        description="入力と方針から作る重複キー", min_length=64, max_length=64
    )
    status: Literal["queued", "running", "succeeded", "failed", "cancelled"] = Field(
        description="進行状態"
    )
    started_at: AwareDatetime | None = Field(default=None, description="開始")
    finished_at: AwareDatetime | None = Field(default=None, description="終了")
    seed: int | None = Field(default=None, description="再現用seed")
    error_code: str | None = Field(
        default=None, description="失敗分類", min_length=1, max_length=20000
    )
    attempt_count: int = Field(description="試行回数", ge=0)


class GenerationChoiceRow(EntityModel):
    """生成軸の選択値のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    job_id: UUID = Field(description="実行")
    option_id: UUID = Field(description="選択した軸候補")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class GenerationChoiceWrite(EntityModel):
    """生成軸の選択値の編集可能列。未指定NULL列はNULLにする。"""

    job_id: UUID = Field(description="実行")
    option_id: UUID = Field(description="選択した軸候補")


class GenerationFoodRow(EntityModel):
    """生成の食材入力のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    job_id: UUID = Field(description="実行")
    form_id: UUID = Field(description="食材形態")
    role: Literal["main", "support", "seasoning", "aroma", "texture", "garnish", "medium"] = Field(
        description="役割"
    )
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class GenerationFoodWrite(EntityModel):
    """生成の食材入力の編集可能列。未指定NULL列はNULLにする。"""

    job_id: UUID = Field(description="実行")
    form_id: UUID = Field(description="食材形態")
    role: Literal["main", "support", "seasoning", "aroma", "texture", "garnish", "medium"] = Field(
        description="役割"
    )


class GenerationResultRow(EntityModel):
    """生成結果の出自のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    recipe_version_id: UUID = Field(description="生成した版")
    job_id: UUID | None = Field(description="短期ジョブ参照")
    policy_id: UUID = Field(description="恒久方針参照")
    input_snapshot: GenerationInput = Field(description="確定入力をschema_versionで検証")
    raw_output_uri: str | None = Field(description="原出力保存先", min_length=1, max_length=20000)
    raw_output_hash: str = Field(description="原出力ハッシュ", min_length=64, max_length=64)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class GenerationResultWrite(EntityModel):
    """生成結果の出自の編集可能列。未指定NULL列はNULLにする。"""

    recipe_version_id: UUID = Field(description="生成した版")
    job_id: UUID | None = Field(default=None, description="短期ジョブ参照")
    policy_id: UUID = Field(description="恒久方針参照")
    input_snapshot: GenerationInput = Field(description="確定入力をschema_versionで検証")
    raw_output_uri: str | None = Field(
        default=None, description="原出力保存先", min_length=1, max_length=20000
    )
    raw_output_hash: str = Field(description="原出力ハッシュ", min_length=64, max_length=64)


class CompatibilityRuleRow(EntityModel):
    """組み合わせ・公開ルールのDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    code: str = Field(description="規則コード", min_length=1, max_length=20000)
    version: int = Field(description="規則版", gt=0)
    severity: Literal["block", "review", "score"] = Field(description="除外/保留/順位")
    predicate: Predicate = Field(description="型付き条件式")
    message: str = Field(description="理由", min_length=1, max_length=20000)
    source_id: UUID | None = Field(description="根拠")
    status: Literal["active", "retired"] = Field(description="利用状態")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class CompatibilityRuleWrite(EntityModel):
    """組み合わせ・公開ルールの編集可能列。未指定NULL列はNULLにする。"""

    code: str = Field(description="規則コード", min_length=1, max_length=20000)
    version: int = Field(description="規則版", gt=0)
    severity: Literal["block", "review", "score"] = Field(description="除外/保留/順位")
    predicate: Predicate = Field(description="型付き条件式")
    message: str = Field(description="理由", min_length=1, max_length=20000)
    source_id: UUID | None = Field(default=None, description="根拠")
    status: Literal["active", "retired"] = Field(description="利用状態")


class ValidationResultRow(EntityModel):
    """公開前評価結果のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    recipe_version_id: UUID = Field(description="対象版")
    rule_id: UUID = Field(description="適用規則版")
    state: Literal["pending", "passed", "failed", "needs_review"] = Field(description="結果")
    evidence: ValidationEvidence = Field(description="検査箇所・値・根拠")
    validator_version: str = Field(description="検証器版", min_length=1, max_length=20000)
    evaluated_at: AwareDatetime = Field(description="検査日時")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ValidationResultWrite(EntityModel):
    """公開前評価結果の編集可能列。未指定NULL列はNULLにする。"""

    recipe_version_id: UUID = Field(description="対象版")
    rule_id: UUID = Field(description="適用規則版")
    state: Literal["pending", "passed", "failed", "needs_review"] = Field(description="結果")
    evidence: ValidationEvidence = Field(description="検査箇所・値・根拠")
    validator_version: str = Field(description="検証器版", min_length=1, max_length=20000)
    evaluated_at: AwareDatetime = Field(description="検査日時")


class RecipeSignatureRow(EntityModel):
    """内容重複判定署名のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    recipe_version_id: UUID = Field(description="対象版")
    algorithm_version: str = Field(
        description="正規化アルゴリズム版", min_length=1, max_length=20000
    )
    exact_hash: str = Field(
        description="材料比率・工程・主要条件のハッシュ", min_length=64, max_length=64
    )
    canonical_payload: CanonicalRecipe = Field(description="正規化対象の監査用内容")
    cluster_key: str = Field(description="料理近似群キー", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class RecipeSignatureWrite(EntityModel):
    """内容重複判定署名の編集可能列。未指定NULL列はNULLにする。"""

    recipe_version_id: UUID = Field(description="対象版")
    algorithm_version: str = Field(
        description="正規化アルゴリズム版", min_length=1, max_length=20000
    )
    exact_hash: str = Field(
        description="材料比率・工程・主要条件のハッシュ", min_length=64, max_length=64
    )
    canonical_payload: CanonicalRecipe = Field(description="正規化対象の監査用内容")
    cluster_key: str = Field(description="料理近似群キー", min_length=1, max_length=20000)


class RecipeSimilarityRow(EntityModel):
    """近似レシピ関係のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    left_version_id: UUID = Field(description="左版")
    right_version_id: UUID = Field(description="右版")
    algorithm_version: str = Field(description="評価器版", min_length=1, max_length=20000)
    score: Decimal = Field(
        description="類似度0..1", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    explanation: str = Field(description="材料/味付/工程の一致差分", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class RecipeSimilarityWrite(EntityModel):
    """近似レシピ関係の編集可能列。未指定NULL列はNULLにする。"""

    left_version_id: UUID = Field(description="左版")
    right_version_id: UUID = Field(description="右版")
    algorithm_version: str = Field(description="評価器版", min_length=1, max_length=20000)
    score: Decimal = Field(
        description="類似度0..1", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    explanation: str = Field(description="材料/味付/工程の一致差分", min_length=1, max_length=20000)


class AppUserRow(EntityModel):
    """アプリ利用者のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    auth_subject: str = Field(description="認証基盤の不透明識別子", min_length=1, max_length=20000)
    state: Literal["active", "erasure_pending"] = Field(description="利用/削除処理")
    locale: str = Field(description="表示言語", min_length=1, max_length=20000)
    timezone: str = Field(description="IANAタイムゾーン", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class AppUserWrite(EntityModel):
    """アプリ利用者の編集可能列。未指定NULL列はNULLにする。"""

    locale: str = Field(description="表示言語", min_length=1, max_length=20000)
    timezone: str = Field(description="IANAタイムゾーン", min_length=1, max_length=20000)


class UserPreferenceRow(EntityModel):
    """ユーザーの嗜好のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="利用者")
    option_id: UUID = Field(description="味・料理等")
    weight: Decimal = Field(
        description="好みの重み", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class UserPreferenceWrite(EntityModel):
    """ユーザーの嗜好の編集可能列。未指定NULL列はNULLにする。"""

    user_id: UUID = Field(description="利用者")
    option_id: UUID = Field(description="味・料理等")
    weight: Decimal = Field(
        description="好みの重み", max_digits=20, decimal_places=6, allow_inf_nan=False
    )


class UserExclusionRow(EntityModel):
    """避けたい食材・物質のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="利用者")
    food_id: UUID | None = Field(description="食材")
    allergen_id: UUID | None = Field(description="アレルゲン")
    strict: bool = Field(description="不明も除外するか")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class UserExclusionWrite(EntityModel):
    """避けたい食材・物質の編集可能列。未指定NULL列はNULLにする。"""

    user_id: UUID = Field(description="利用者")
    food_id: UUID | None = Field(default=None, description="食材")
    allergen_id: UUID | None = Field(default=None, description="アレルゲン")
    strict: bool = Field(description="不明も除外するか")


class UserRecipeEventRow(EntityModel):
    """提案・調理履歴のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="利用者")
    recipe_version_id: UUID = Field(description="提案版")
    kind: Literal["shown", "cooked", "liked", "disliked"] = Field(description="提示/調理/評価")
    occurred_at: AwareDatetime = Field(description="発生時刻")
    request_key: str = Field(description="リクエスト識別子", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class UserRecipeEventWrite(EntityModel):
    """提案・調理履歴の編集可能列。未指定NULL列はNULLにする。"""

    user_id: UUID = Field(description="利用者")
    recipe_version_id: UUID = Field(description="提案版")
    kind: Literal["shown", "cooked", "liked", "disliked"] = Field(description="提示/調理/評価")
    occurred_at: AwareDatetime = Field(description="発生時刻")
    request_key: str = Field(description="リクエスト識別子", min_length=1, max_length=20000)


class MenuRow(EntityModel):
    """献立のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    name: str = Field(description="献立名", min_length=1, max_length=20000)
    servings: Decimal = Field(
        description="標準人数", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    revision: int = Field(description="楽観ロック版", gt=0)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class MenuWrite(EntityModel):
    """献立の編集可能列。未指定NULL列はNULLにする。"""

    user_id: UUID = Field(description="所有者")
    name: str = Field(description="献立名", min_length=1, max_length=20000)
    servings: Decimal = Field(
        description="標準人数", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )


class MenuItemRow(EntityModel):
    """献立の料理のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    menu_id: UUID = Field(description="献立")
    recipe_version_id: UUID = Field(description="固定レシピ版")
    servings: Decimal = Field(
        description="その料理を作る人数", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    role_option_id: UUID = Field(description="主菜等")
    position: int = Field(description="表示順", gt=0)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class MenuItemWrite(EntityModel):
    """献立の料理の編集可能列。未指定NULL列はNULLにする。"""

    menu_id: UUID = Field(description="献立")
    recipe_version_id: UUID = Field(description="固定レシピ版")
    servings: Decimal = Field(
        description="その料理を作る人数", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    role_option_id: UUID = Field(description="主菜等")
    position: int = Field(description="表示順", gt=0)


class MenuIngredientOverrideRow(EntityModel):
    """献立別材料確定のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    menu_item_id: UUID = Field(description="対象料理")
    ingredient_line_id: UUID = Field(description="元材料行")
    selected: bool = Field(description="任意材料を使うか")
    amount: Decimal | None = Field(
        description="適量等の確定基準量", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    form_id: UUID | None = Field(description="明示的代替形態")
    product_version_id: UUID | None = Field(description="購入商品指定")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class MenuIngredientOverrideWrite(EntityModel):
    """献立別材料確定の編集可能列。未指定NULL列はNULLにする。"""

    menu_item_id: UUID = Field(description="対象料理")
    ingredient_line_id: UUID = Field(description="元材料行")
    selected: bool = Field(description="任意材料を使うか")
    amount: Decimal | None = Field(
        default=None,
        description="適量等の確定基準量",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
    )
    form_id: UUID | None = Field(default=None, description="明示的代替形態")
    product_version_id: UUID | None = Field(default=None, description="購入商品指定")


class KitchenResourceRow(EntityModel):
    """キッチンの実資源のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    resource_type_id: UUID = Field(description="コンロ・鍋・人等")
    name: str = Field(description="左コンロ・26cmフライパン等", min_length=1, max_length=20000)
    capacity: Decimal | None = Field(
        description="容量", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    quantity: int = Field(description="同等資源数", gt=0)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class KitchenResourceWrite(EntityModel):
    """キッチンの実資源の編集可能列。未指定NULL列はNULLにする。"""

    user_id: UUID = Field(description="所有者")
    resource_type_id: UUID = Field(description="コンロ・鍋・人等")
    name: str = Field(description="左コンロ・26cmフライパン等", min_length=1, max_length=20000)
    capacity: Decimal | None = Field(
        default=None, description="容量", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    quantity: int = Field(description="同等資源数", gt=0)


class CookingSessionRow(EntityModel):
    """調理計画実行のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    menu_id: UUID = Field(description="対象献立")
    menu_revision: int = Field(description="献立版", gt=0)
    status: Literal["planned", "cooking", "paused", "completed", "cancelled"] = Field(
        description="実行状態"
    )
    target_at: AwareDatetime | None = Field(description="完成希望時刻")
    planner_version: str = Field(description="計画器の版", min_length=1, max_length=20000)
    input_snapshot: CookingInput = Field(description="材料・資源・人数の固定入力")
    input_hash: str = Field(description="入力ハッシュ", min_length=64, max_length=64)
    current_task_index: int = Field(description="調理画面の現在の工程位置(0始まり)", ge=0)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class CookingSessionWrite(EntityModel):
    """調理計画実行の編集可能列。未指定NULL列はNULLにする。"""

    menu_id: UUID = Field(description="対象献立")
    menu_revision: int = Field(description="献立版", gt=0)
    status: Literal["planned", "cooking", "paused", "completed", "cancelled"] = Field(
        description="実行状態"
    )
    target_at: AwareDatetime | None = Field(default=None, description="完成希望時刻")
    planner_version: str = Field(description="計画器の版", min_length=1, max_length=20000)
    input_snapshot: CookingInput = Field(description="材料・資源・人数の固定入力")
    input_hash: str = Field(description="入力ハッシュ", min_length=64, max_length=64)
    current_task_index: int = Field(description="調理画面の現在の工程位置(0始まり)", ge=0)


class SessionTaskRow(EntityModel):
    """展開済み工程のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    session_id: UUID = Field(description="実行")
    menu_item_id: UUID = Field(description="料理")
    step_id: UUID = Field(description="元工程")
    batch_no: int = Field(description="容量分割した回", gt=0)
    planned_start_s: int = Field(description="開始相対秒", ge=0)
    planned_end_s: int = Field(description="終了相対秒")
    status: Literal["pending", "running", "completed", "skipped"] = Field(description="進捗")
    actual_start_at: AwareDatetime | None = Field(description="実開始")
    actual_end_at: AwareDatetime | None = Field(description="実完了")
    timer_started_at: AwareDatetime | None = Field(description="稼働中タイマーの開始日時")
    timer_duration_s: int | None = Field(description="利用者が設定したタイマー秒数")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class SessionTaskWrite(EntityModel):
    """展開済み工程の編集可能列。未指定NULL列はNULLにする。"""

    session_id: UUID = Field(description="実行")
    menu_item_id: UUID = Field(description="料理")
    step_id: UUID = Field(description="元工程")
    batch_no: int = Field(description="容量分割した回", gt=0)
    planned_start_s: int = Field(description="開始相対秒", ge=0)
    planned_end_s: int = Field(description="終了相対秒")
    status: Literal["pending", "running", "completed", "skipped"] = Field(description="進捗")
    actual_start_at: AwareDatetime | None = Field(default=None, description="実開始")
    actual_end_at: AwareDatetime | None = Field(default=None, description="実完了")
    timer_started_at: AwareDatetime | None = Field(
        default=None, description="稼働中タイマーの開始日時"
    )
    timer_duration_s: int | None = Field(default=None, description="利用者が設定したタイマー秒数")


class TaskDependencyRow(EntityModel):
    """献立展開後依存のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    before_task_id: UUID = Field(description="先行タスク")
    after_task_id: UUID = Field(description="後続タスク")
    min_lag_s: int = Field(description="最小間隔", ge=0)
    max_lag_s: int | None = Field(description="最大間隔")
    reason: str = Field(description="元DAG/洗浄/設備切替等", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class TaskDependencyWrite(EntityModel):
    """献立展開後依存の編集可能列。未指定NULL列はNULLにする。"""

    before_task_id: UUID = Field(description="先行タスク")
    after_task_id: UUID = Field(description="後続タスク")
    min_lag_s: int = Field(description="最小間隔", ge=0)
    max_lag_s: int | None = Field(default=None, description="最大間隔")
    reason: str = Field(description="元DAG/洗浄/設備切替等", min_length=1, max_length=20000)


class ResourceReservationRow(EntityModel):
    """資源の予約のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    task_id: UUID = Field(description="使用タスク")
    resource_id: UUID = Field(description="実資源")
    start_s: int = Field(description="占有開始", ge=0)
    end_s: int = Field(description="占有終了")
    quantity: int = Field(description="占有量", gt=0)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ResourceReservationWrite(EntityModel):
    """資源の予約の編集可能列。未指定NULL列はNULLにする。"""

    task_id: UUID = Field(description="使用タスク")
    resource_id: UUID = Field(description="実資源")
    start_s: int = Field(description="占有開始", ge=0)
    end_s: int = Field(description="占有終了")
    quantity: int = Field(description="占有量", gt=0)


class IngredientTotalRow(EntityModel):
    """献立材料集計結果のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    session_id: UUID = Field(description="固定計算対象")
    form_id: UUID = Field(description="合算可能な形態")
    product_version_id: UUID | None = Field(description="商品固定")
    unit_id: UUID = Field(description="基準単位")
    required_amount: Decimal = Field(
        description="必要量", max_digits=20, decimal_places=6, allow_inf_nan=False, ge=0
    )
    quality: Literal["measured", "manufacturer", "reference", "estimated", "unknown"] = Field(
        description="最も低い入力精度"
    )
    calculation_version: str = Field(description="計算器版", min_length=1, max_length=20000)
    actual_amount: Decimal | None = Field(
        description="利用者が確定した実使用量。不明はNULL",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
    )
    consumption_outcome: Literal[
        "not_requested", "applied", "insufficient", "unknown", "incompatible"
    ] = Field(description="未要求・反映済み・在庫不足・数量不明・単位不一致の結果")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class IngredientTotalWrite(EntityModel):
    """献立材料集計結果の編集可能列。未指定NULL列はNULLにする。"""

    session_id: UUID = Field(description="固定計算対象")
    form_id: UUID = Field(description="合算可能な形態")
    product_version_id: UUID | None = Field(default=None, description="商品固定")
    unit_id: UUID = Field(description="基準単位")
    required_amount: Decimal = Field(
        description="必要量", max_digits=20, decimal_places=6, allow_inf_nan=False, ge=0
    )
    quality: Literal["measured", "manufacturer", "reference", "estimated", "unknown"] = Field(
        description="最も低い入力精度"
    )
    calculation_version: str = Field(description="計算器版", min_length=1, max_length=20000)
    actual_amount: Decimal | None = Field(
        default=None,
        description="利用者が確定した実使用量。不明はNULL",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
    )
    consumption_outcome: Literal[
        "not_requested", "applied", "insufficient", "unknown", "incompatible"
    ] = Field(description="未要求・反映済み・在庫不足・数量不明・単位不一致の結果")


class PantryLotRow(EntityModel):
    """手持ち食材ロットのDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    form_id: UUID = Field(description="食材形態")
    product_version_id: UUID | None = Field(description="商品版")
    amount: Decimal | None = Field(
        description="残量", max_digits=20, decimal_places=6, allow_inf_nan=False, ge=0
    )
    unit_id: UUID = Field(description="単位")
    expires_on: date | None = Field(description="表示期限")
    opened_at: AwareDatetime | None = Field(description="開封時点")
    location: Literal["fridge", "freezer", "pantry"] = Field(
        description="冷蔵・冷凍・常温の保管場所"
    )
    priority: Literal["normal", "use_first"] = Field(description="先に使う優先指定")
    status: Literal["active", "deleted", "undone"] = Field(
        description="在庫の有効・削除・レシート取消状態"
    )
    source_import_id: UUID | None = Field(description="登録元レシート")
    quantity_quality: str = Field(description="数量の確定・不明", min_length=1, max_length=20000)
    original_form_id: UUID | None = Field(description="登録時の食材形態")
    original_amount: Decimal | None = Field(
        description="登録時数量。不明はNULL", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    original_unit_id: UUID | None = Field(description="登録時単位")
    updated_at: AwareDatetime = Field(description="最終編集日時")
    edited: bool = Field(description="登録後の編集有無")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class PantryLotWrite(EntityModel):
    """手持ち食材ロットの編集可能列。未指定NULL列はNULLにする。"""

    user_id: UUID = Field(description="所有者")
    form_id: UUID = Field(description="食材形態")
    product_version_id: UUID | None = Field(default=None, description="商品版")
    amount: Decimal | None = Field(
        default=None, description="残量", max_digits=20, decimal_places=6, allow_inf_nan=False, ge=0
    )
    unit_id: UUID = Field(description="単位")
    expires_on: date | None = Field(default=None, description="表示期限")
    opened_at: AwareDatetime | None = Field(default=None, description="開封時点")
    location: Literal["fridge", "freezer", "pantry"] = Field(
        description="冷蔵・冷凍・常温の保管場所"
    )
    priority: Literal["normal", "use_first"] = Field(description="先に使う優先指定")
    status: Literal["active", "deleted", "undone"] = Field(
        description="在庫の有効・削除・レシート取消状態"
    )
    source_import_id: UUID | None = Field(default=None, description="登録元レシート")
    quantity_quality: str = Field(description="数量の確定・不明", min_length=1, max_length=20000)
    original_form_id: UUID | None = Field(default=None, description="登録時の食材形態")
    original_amount: Decimal | None = Field(
        default=None,
        description="登録時数量。不明はNULL",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
    )
    original_unit_id: UUID | None = Field(default=None, description="登録時単位")
    updated_at: AwareDatetime = Field(description="最終編集日時")
    edited: bool = Field(description="登録後の編集有無")


class ShoppingItemRow(EntityModel):
    """買い物行のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    session_id: UUID = Field(description="対象調理")
    total_id: UUID = Field(description="需要行")
    product_version_id: UUID | None = Field(description="購入SKU")
    net_shortage: Decimal = Field(
        description="在庫控除後の不足量", max_digits=20, decimal_places=6, allow_inf_nan=False, ge=0
    )
    package_count: int | None = Field(description="購入包装数")
    surplus_amount: Decimal | None = Field(
        description="購入後余剰", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    checked: bool = Field(description="購入済み")
    client_key: str | None = Field(description="画面操作の安定キー", min_length=1, max_length=20000)
    checked_at: AwareDatetime | None = Field(description="購入確認日時")
    archived: bool = Field(description="完了した買い物の保管状態")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ShoppingItemWrite(EntityModel):
    """買い物行の編集可能列。未指定NULL列はNULLにする。"""

    session_id: UUID = Field(description="対象調理")
    total_id: UUID = Field(description="需要行")
    product_version_id: UUID | None = Field(default=None, description="購入SKU")
    net_shortage: Decimal = Field(
        description="在庫控除後の不足量", max_digits=20, decimal_places=6, allow_inf_nan=False, ge=0
    )
    package_count: int | None = Field(default=None, description="購入包装数")
    surplus_amount: Decimal | None = Field(
        default=None, description="購入後余剰", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    checked: bool = Field(description="購入済み")
    client_key: str | None = Field(
        default=None, description="画面操作の安定キー", min_length=1, max_length=20000
    )
    checked_at: AwareDatetime | None = Field(default=None, description="購入確認日時")
    archived: bool = Field(description="完了した買い物の保管状態")


class AuditEventRow(EntityModel):
    """変更・公開監査のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    actor_id: UUID | None = Field(description="実行者(削除時匿名化)")
    action: str = Field(description="publish/withdraw/erase等", min_length=1, max_length=20000)
    entity_type: str = Field(description="対象テーブルの許可リスト", min_length=1, max_length=20000)
    entity_key_hash: str = Field(description="対象識別子のハッシュ", min_length=64, max_length=64)
    reason: str = Field(description="理由(個人情報を含めない)", min_length=1, max_length=20000)
    occurred_at: AwareDatetime = Field(description="時刻")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class AuditEventWrite(EntityModel):
    """変更・公開監査の編集可能列。未指定NULL列はNULLにする。"""

    actor_id: UUID | None = Field(default=None, description="実行者(削除時匿名化)")
    action: str = Field(description="publish/withdraw/erase等", min_length=1, max_length=20000)
    entity_type: str = Field(description="対象テーブルの許可リスト", min_length=1, max_length=20000)
    entity_key_hash: str = Field(description="対象識別子のハッシュ", min_length=64, max_length=64)
    reason: str = Field(description="理由(個人情報を含めない)", min_length=1, max_length=20000)
    occurred_at: AwareDatetime = Field(description="時刻")


class OutboxEventRow(EntityModel):
    """検索・キャッシュ更新配信のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    event_type: str = Field(
        description="recipe_published/withdrawn/user_erased等", min_length=1, max_length=20000
    )
    aggregate_id: UUID = Field(description="対象ID(配信対象でありFKでない)")
    payload: OutboxPayload = Field(description="schema_version付き最小通知")
    delivered_at: AwareDatetime | None = Field(description="配送完了")
    attempt_count: int = Field(description="再試行数", ge=0)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class OutboxEventWrite(EntityModel):
    """検索・キャッシュ更新配信の編集可能列。未指定NULL列はNULLにする。"""

    event_type: str = Field(
        description="recipe_published/withdrawn/user_erased等", min_length=1, max_length=20000
    )
    aggregate_id: UUID = Field(description="対象ID(配信対象でありFKでない)")
    payload: OutboxPayload = Field(description="schema_version付き最小通知")
    delivered_at: AwareDatetime | None = Field(default=None, description="配送完了")
    attempt_count: int = Field(description="再試行数", ge=0)


class ProductPreparationRuleRow(EntityModel):
    """商品固有の調理条件のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    product_version_id: UUID = Field(description="対象商品仕様")
    operation_id: UUID = Field(description="対象標準動作")
    allowed: bool = Field(description="表示で許可される方法か")
    use_original_container: bool = Field(description="付属容器で調理するか")
    parameter_contract: ProductPreparation = Field(
        description="電力・注湯量・時間・蓋などの確定条件"
    )
    source_id: UUID = Field(description="商品表示根拠")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ProductPreparationRuleWrite(EntityModel):
    """商品固有の調理条件の編集可能列。未指定NULL列はNULLにする。"""

    product_version_id: UUID = Field(description="対象商品仕様")
    operation_id: UUID = Field(description="対象標準動作")
    allowed: bool = Field(description="表示で許可される方法か")
    use_original_container: bool = Field(description="付属容器で調理するか")
    parameter_contract: ProductPreparation = Field(
        description="電力・注湯量・時間・蓋などの確定条件"
    )
    source_id: UUID = Field(description="商品表示根拠")


class FoodIdentityRow(EntityModel):
    """料理同一性上の食品のDB応答。"""

    id: UUID = Field(description="不変ID")
    created_at: AwareDatetime = Field(description="作成日時")
    code: str = Field(description="形態を横断した食品コード", min_length=1, max_length=20000)
    name: str = Field(description="食品名", min_length=1, max_length=20000)
    normalizer_version: str = Field(description="正規化器の版", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class FoodIdentityWrite(EntityModel):
    """料理同一性上の食品の編集可能列。未指定NULL列はNULLにする。"""

    code: str = Field(description="形態を横断した食品コード", min_length=1, max_length=20000)
    name: str = Field(description="食品名", min_length=1, max_length=20000)
    normalizer_version: str = Field(description="正規化器の版", min_length=1, max_length=20000)


class FoodIdentityMemberRow(EntityModel):
    """購買食品から同一性への対応のDB応答。"""

    id: UUID = Field(description="不変ID")
    created_at: AwareDatetime = Field(description="作成日時")
    food_id: UUID = Field(description="元の食品")
    identity_id: UUID = Field(description="同一性ID")
    normalizer_version: str = Field(description="正規化器版", min_length=1, max_length=20000)
    reason: str = Field(description="同一視の理由", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class FoodIdentityMemberWrite(EntityModel):
    """購買食品から同一性への対応の編集可能列。未指定NULL列はNULLにする。"""

    food_id: UUID = Field(description="元の食品")
    identity_id: UUID = Field(description="同一性ID")
    normalizer_version: str = Field(description="正規化器版", min_length=1, max_length=20000)
    reason: str = Field(description="同一視の理由", min_length=1, max_length=20000)


class GenerationTemplateRow(EntityModel):
    """列挙テンプレート版のDB応答。"""

    id: UUID = Field(description="不変ID")
    created_at: AwareDatetime = Field(description="作成日時")
    code: str = Field(description="テンプレートコード", min_length=1, max_length=20000)
    version: int = Field(description="定義版", gt=0)
    release_id: UUID = Field(description="カタログ版")
    contract: GenerationTemplateContract = Field(description="主副材の許可集合・k・味付・経路")
    candidate_count: BigInteger = Field(description="この定義の正確な設計点数")
    contract_hash: str = Field(description="定義ハッシュ", min_length=64, max_length=64)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class GenerationTemplateWrite(EntityModel):
    """列挙テンプレート版の編集可能列。未指定NULL列はNULLにする。"""

    code: str = Field(description="テンプレートコード", min_length=1, max_length=20000)
    version: int = Field(description="定義版", gt=0)
    release_id: UUID = Field(description="カタログ版")
    contract: GenerationTemplateContract = Field(description="主副材の許可集合・k・味付・経路")
    candidate_count: BigInteger = Field(description="この定義の正確な設計点数")
    contract_hash: str = Field(description="定義ハッシュ", min_length=64, max_length=64)


class GenerationShardRow(EntityModel):
    """列挙範囲・リース管理のDB応答。"""

    id: UUID = Field(description="不変ID")
    created_at: AwareDatetime = Field(description="作成日時")
    template_id: UUID = Field(description="テンプレート版")
    start_ordinal: BigInteger = Field(description="開始序数")
    end_ordinal: BigInteger = Field(description="終了序数(排他的)")
    next_ordinal: BigInteger = Field(description="再開位置")
    lease_owner: str | None = Field(description="ワーカー識別子", min_length=1, max_length=20000)
    lease_expires_at: AwareDatetime | None = Field(description="有効期限")
    fence_token: BigInteger = Field(description="古い所有者の書込みを拒否")
    state: Literal["queued", "running", "done", "failed"] = Field(description="待機/実行/完了/停止")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class GenerationShardWrite(EntityModel):
    """列挙範囲・リース管理の編集可能列。未指定NULL列はNULLにする。"""

    template_id: UUID = Field(description="テンプレート版")
    start_ordinal: BigInteger = Field(description="開始序数")
    end_ordinal: BigInteger = Field(description="終了序数(排他的)")
    next_ordinal: BigInteger = Field(description="再開位置")
    lease_owner: str | None = Field(
        default=None, description="ワーカー識別子", min_length=1, max_length=20000
    )
    lease_expires_at: AwareDatetime | None = Field(default=None, description="有効期限")
    fence_token: BigInteger = Field(description="古い所有者の書込みを拒否")
    state: Literal["queued", "running", "done", "failed"] = Field(description="待機/実行/完了/停止")


class CandidateAttemptRow(EntityModel):
    """試行済み設計点の台帳のDB応答。"""

    id: UUID = Field(description="不変ID")
    created_at: AwareDatetime = Field(description="作成日時")
    template_id: UUID = Field(description="定義版")
    ordinal: BigInteger = Field(description="設計点の序数")
    design_key: str = Field(description="正規化した設計キー", min_length=64, max_length=64)
    job_id: UUID | None = Field(description="生成ジョブ")
    state: Literal["pending", "invalid", "generated", "duplicate", "accepted", "failed"] = Field(
        description="候補の段階"
    )
    reason_code: str | None = Field(description="棄却理由", min_length=1, max_length=20000)
    recipe_version_id: UUID | None = Field(description="採用した版")
    attempts: int = Field(description="試行上限(暫定)")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class CandidateAttemptWrite(EntityModel):
    """試行済み設計点の台帳の編集可能列。未指定NULL列はNULLにする。"""

    template_id: UUID = Field(description="定義版")
    ordinal: BigInteger = Field(description="設計点の序数")
    design_key: str = Field(description="正規化した設計キー", min_length=64, max_length=64)
    job_id: UUID | None = Field(default=None, description="生成ジョブ")
    state: Literal["pending", "invalid", "generated", "duplicate", "accepted", "failed"] = Field(
        description="候補の段階"
    )
    reason_code: str | None = Field(
        default=None, description="棄却理由", min_length=1, max_length=20000
    )
    recipe_version_id: UUID | None = Field(default=None, description="採用した版")
    attempts: int = Field(description="試行上限(暫定)")


class RecipeSearchDocumentRow(EntityModel):
    """公開検索用文書のDB応答。"""

    id: UUID = Field(description="不変ID")
    created_at: AwareDatetime = Field(description="作成日時")
    recipe_id: UUID = Field(description="同一性単位で1件")
    published_version_id: UUID = Field(description="検索対象の公開版")
    projection_version: str = Field(
        description="検索文書の生成器版", min_length=1, max_length=20000
    )
    display_title: str = Field(description="表示タイトル", min_length=1, max_length=20000)
    food_identity_ids: list[UUID] = Field(description="検索用食品ID集合", max_length=1024)
    facet_option_ids: list[UUID] = Field(description="料理・味等の検索軸", max_length=1024)
    search_text: str = Field(description="検索用本文", min_length=1, max_length=20000)
    eligible: bool = Field(description="公開可能か")
    source_hash: str = Field(description="正本一致確認", min_length=64, max_length=64)
    projected_at: AwareDatetime = Field(description="更新時点")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class RecipeSearchDocumentWrite(EntityModel):
    """公開検索用文書の編集可能列。未指定NULL列はNULLにする。"""

    recipe_id: UUID = Field(description="同一性単位で1件")
    published_version_id: UUID = Field(description="検索対象の公開版")
    projection_version: str = Field(
        description="検索文書の生成器版", min_length=1, max_length=20000
    )
    display_title: str = Field(description="表示タイトル", min_length=1, max_length=20000)
    food_identity_ids: list[UUID] = Field(description="検索用食品ID集合", max_length=1024)
    facet_option_ids: list[UUID] = Field(description="料理・味等の検索軸", max_length=1024)
    search_text: str = Field(description="検索用本文", min_length=1, max_length=20000)
    eligible: bool = Field(description="公開可能か")
    source_hash: str = Field(description="正本一致確認", min_length=64, max_length=64)
    projected_at: AwareDatetime = Field(description="更新時点")


class RecipeEmbeddingRow(EntityModel):
    """近似検索用特徴量のDB応答。"""

    id: UUID = Field(description="不変ID")
    created_at: AwareDatetime = Field(description="作成日時")
    recipe_version_id: UUID = Field(description="対象版")
    model_version: str = Field(description="埋め込みモデル固定版", min_length=1, max_length=20000)
    content_hash: str = Field(description="入力内容ハッシュ", min_length=64, max_length=64)
    embedding: list[float] = Field(description="仮定768次元float32", min_length=768, max_length=768)
    created_for_index: str = Field(description="検索索引版", min_length=1, max_length=20000)
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class RecipeEmbeddingWrite(EntityModel):
    """近似検索用特徴量の編集可能列。未指定NULL列はNULLにする。"""

    recipe_version_id: UUID = Field(description="対象版")
    model_version: str = Field(description="埋め込みモデル固定版", min_length=1, max_length=20000)
    content_hash: str = Field(description="入力内容ハッシュ", min_length=64, max_length=64)
    embedding: list[float] = Field(description="仮定768次元float32", min_length=768, max_length=768)
    created_for_index: str = Field(description="検索索引版", min_length=1, max_length=20000)


class GenerationStratumMetricRow(EntityModel):
    """採用率・飽和度の実測のDB応答。"""

    id: UUID = Field(description="不変ID")
    created_at: AwareDatetime = Field(description="作成日時")
    template_id: UUID = Field(description="対象テンプレート")
    window_start: AwareDatetime = Field(description="計測窓開始")
    window_end: AwareDatetime = Field(description="計測窓終了")
    attempted: BigInteger = Field(description="試行数")
    valid: BigInteger = Field(description="適合生成数")
    unique_count: BigInteger = Field(description="既存集合との差分数")
    publishable: BigInteger = Field(description="公開基準通過数")
    input_tokens: BigInteger = Field(description="入力トークン合計")
    output_tokens: BigInteger = Field(description="出力トークン合計")
    cost_amount: Decimal | None = Field(
        description="同一通貨の費用", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    currency: str | None = Field(description="JPY/USD等", min_length=3, max_length=3)
    stratum_key: str = Field(
        description="層の安定キー(料理構造x食品カテゴリx入手性)。集計定義はテンプレート版に固定",
        min_length=1,
        max_length=20000,
    )
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class GenerationStratumMetricWrite(EntityModel):
    """採用率・飽和度の実測の編集可能列。未指定NULL列はNULLにする。"""

    template_id: UUID = Field(description="対象テンプレート")
    window_start: AwareDatetime = Field(description="計測窓開始")
    window_end: AwareDatetime = Field(description="計測窓終了")
    attempted: BigInteger = Field(description="試行数")
    valid: BigInteger = Field(description="適合生成数")
    unique_count: BigInteger = Field(description="既存集合との差分数")
    publishable: BigInteger = Field(description="公開基準通過数")
    input_tokens: BigInteger = Field(description="入力トークン合計")
    output_tokens: BigInteger = Field(description="出力トークン合計")
    cost_amount: Decimal | None = Field(
        default=None,
        description="同一通貨の費用",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
    )
    currency: str | None = Field(default=None, description="JPY/USD等", min_length=3, max_length=3)
    stratum_key: str = Field(
        description="層の安定キー(料理構造x食品カテゴリx入手性)。集計定義はテンプレート版に固定",
        min_length=1,
        max_length=20000,
    )


class ReceiptImportRow(EntityModel):
    """レシート読取・在庫登録の処理単位のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    file_sha256: str | None = Field(
        description="画像本文のSHA256。本文はDBに保存しない", min_length=64, max_length=64
    )
    idempotency_key: str = Field(
        description="本人内で一意の再送防止キー", min_length=1, max_length=20000
    )
    status: Literal["draft", "committed", "reverted"] = Field(
        description="draft/committed/revertedの状態"
    )
    revision: BigInteger = Field(description="楽観ロック版")
    committed_at: AwareDatetime | None = Field(description="在庫へ登録した日時")
    reverted_at: AwareDatetime | None = Field(description="登録取消日時")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ReceiptImportWrite(EntityModel):
    """レシート読取・在庫登録の処理単位の編集可能列。未指定NULL列はNULLにする。"""

    user_id: UUID = Field(description="所有者")
    file_sha256: str | None = Field(
        default=None,
        description="画像本文のSHA256。本文はDBに保存しない",
        min_length=64,
        max_length=64,
    )
    idempotency_key: str = Field(
        description="本人内で一意の再送防止キー", min_length=1, max_length=20000
    )
    status: Literal["draft", "committed", "reverted"] = Field(
        description="draft/committed/revertedの状態"
    )
    revision: BigInteger = Field(description="楽観ロック版")
    committed_at: AwareDatetime | None = Field(default=None, description="在庫へ登録した日時")
    reverted_at: AwareDatetime | None = Field(default=None, description="登録取消日時")


class ReceiptLineRow(EntityModel):
    """レシートの商品候補と確定した在庫の対応のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    import_id: UUID = Field(description="レシート処理")
    line_no: int = Field(description="レシート内の表示順", gt=0)
    raw_name: str = Field(
        description="利用者が確認できる商品原表記", min_length=1, max_length=20000
    )
    form_id: UUID | None = Field(description="確定した食材形態")
    product_version_id: UUID | None = Field(description="確定した商品版")
    amount: Decimal | None = Field(
        description="数量。不明はNULL", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    unit_id: UUID | None = Field(description="確定数量の単位")
    decision: Literal["accepted", "skipped", "unresolved"] = Field(
        description="accepted/skipped/unresolved"
    )
    pantry_lot_id: UUID | None = Field(description="登録したロット")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class ReceiptLineWrite(EntityModel):
    """レシートの商品候補と確定した在庫の対応の編集可能列。未指定NULL列はNULLにする。"""

    import_id: UUID = Field(description="レシート処理")
    line_no: int = Field(description="レシート内の表示順", gt=0)
    raw_name: str = Field(
        description="利用者が確認できる商品原表記", min_length=1, max_length=20000
    )
    form_id: UUID | None = Field(default=None, description="確定した食材形態")
    product_version_id: UUID | None = Field(default=None, description="確定した商品版")
    amount: Decimal | None = Field(
        default=None,
        description="数量。不明はNULL",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
    )
    unit_id: UUID | None = Field(default=None, description="確定数量の単位")
    decision: Literal["accepted", "skipped", "unresolved"] = Field(
        description="accepted/skipped/unresolved"
    )
    pantry_lot_id: UUID | None = Field(default=None, description="登録したロット")


class WorkspaceRevisionRow(EntityModel):
    """利用者ワークスペースの原子的更新版のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    revision: BigInteger = Field(description="全体のCAS版")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class WorkspaceRevisionWrite(EntityModel):
    """利用者ワークスペースの原子的更新版の編集可能列。未指定NULL列はNULLにする。"""

    user_id: UUID = Field(description="所有者")
    revision: BigInteger = Field(description="全体のCAS版")


class UserFoodRow(EntityModel):
    """利用者が追加した独自食材の所有のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    food_id: UUID = Field(description="独自食材")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class UserFoodWrite(EntityModel):
    """利用者が追加した独自食材の所有の編集可能列。未指定NULL列はNULLにする。"""

    user_id: UUID = Field(description="所有者")
    food_id: UUID = Field(description="独自食材")


class UserPantryFoodRow(EntityModel):
    """利用者が常備すると設定した食材のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    food_id: UUID = Field(description="常備食材")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class UserPantryFoodWrite(EntityModel):
    """利用者が常備すると設定した食材の編集可能列。未指定NULL列はNULLにする。"""

    user_id: UUID = Field(description="所有者")
    food_id: UUID = Field(description="常備食材")


class PantryConsumptionRow(EntityModel):
    """調理による在庫消費の冪等台帳のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    session_id: UUID = Field(description="消費した調理セッション")
    lot_id: UUID = Field(description="消費元ロット")
    amount: Decimal = Field(
        description="消費数量", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    unit_id: UUID = Field(description="消費数量の単位")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class PantryConsumptionWrite(EntityModel):
    """調理による在庫消費の冪等台帳の編集可能列。未指定NULL列はNULLにする。"""

    user_id: UUID = Field(description="所有者")
    session_id: UUID = Field(description="消費した調理セッション")
    lot_id: UUID = Field(description="消費元ロット")
    amount: Decimal = Field(
        description="消費数量", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    unit_id: UUID = Field(description="消費数量の単位")


class UserShoppingCheckRow(EntityModel):
    """調理前の買い物確認のDB応答。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    key: str = Field(description="買い物対象の安定キー", min_length=1, max_length=20000)
    signature: str = Field(
        description="数量・商品条件の一致確認用署名", min_length=1, max_length=20000
    )
    food_id: UUID | None = Field(description="対象食材")
    amount: Decimal | None = Field(
        description="必要数量。不明はNULL", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    unit_id: UUID | None = Field(description="数量単位")
    checked_at: AwareDatetime | None = Field(description="購入確認日時")
    archived: bool = Field(description="保管済みか")
    etag: str = Field(pattern=r"^[0-9]+$", description="更新・削除時のIf-Matchに使う行版")


class UserShoppingCheckWrite(EntityModel):
    """調理前の買い物確認の編集可能列。未指定NULL列はNULLにする。"""

    user_id: UUID = Field(description="所有者")
    key: str = Field(description="買い物対象の安定キー", min_length=1, max_length=20000)
    signature: str = Field(
        description="数量・商品条件の一致確認用署名", min_length=1, max_length=20000
    )
    food_id: UUID | None = Field(default=None, description="対象食材")
    amount: Decimal | None = Field(
        default=None,
        description="必要数量。不明はNULL",
        max_digits=20,
        decimal_places=6,
        allow_inf_nan=False,
    )
    unit_id: UUID | None = Field(default=None, description="数量単位")
    checked_at: AwareDatetime | None = Field(default=None, description="購入確認日時")
    archived: bool = Field(description="保管済みか")
