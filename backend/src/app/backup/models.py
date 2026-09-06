# generate_backup_api.py による自動生成。直接編集しない。
from datetime import date
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, Field

from app.entities.json_contracts import BigInteger, ContractModel, CookingInput, ProductPreparation


class UserPreferenceBackupRow(ContractModel):
    """ユーザーの嗜好の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="利用者")
    option_id: UUID = Field(description="味・料理等")
    weight: Decimal = Field(
        description="好みの重み", max_digits=20, decimal_places=6, allow_inf_nan=False
    )


class UserExclusionBackupRow(ContractModel):
    """避けたい食材・物質の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="利用者")
    food_id: UUID | None = Field(description="食材")
    allergen_id: UUID | None = Field(description="アレルゲン")
    strict: bool = Field(description="不明も除外するか")


class UserRecipeEventBackupRow(ContractModel):
    """提案・調理履歴の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="利用者")
    recipe_version_id: UUID = Field(description="提案版")
    kind: Literal["shown", "cooked", "liked", "disliked"] = Field(description="提示/調理/評価")
    occurred_at: AwareDatetime = Field(description="発生時刻")
    request_key: str = Field(description="リクエスト識別子", min_length=1, max_length=20000)


class MenuBackupRow(ContractModel):
    """献立の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    name: str = Field(description="献立名", min_length=1, max_length=20000)
    servings: Decimal = Field(
        description="標準人数", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    revision: int = Field(description="楽観ロック版", gt=0)


class MenuItemBackupRow(ContractModel):
    """献立の料理の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    menu_id: UUID = Field(description="献立")
    recipe_version_id: UUID = Field(description="固定レシピ版")
    servings: Decimal = Field(
        description="その料理を作る人数", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    role_option_id: UUID = Field(description="主菜等")
    position: int = Field(description="表示順", gt=0)


class MenuIngredientOverrideBackupRow(ContractModel):
    """献立別材料確定の全列。ID・作成時刻も元の値を保持する。"""

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


class KitchenResourceBackupRow(ContractModel):
    """キッチンの実資源の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    resource_type_id: UUID = Field(description="コンロ・鍋・人等")
    name: str = Field(description="左コンロ・26cmフライパン等", min_length=1, max_length=20000)
    capacity: Decimal | None = Field(
        description="容量", max_digits=20, decimal_places=6, allow_inf_nan=False
    )
    quantity: int = Field(description="同等資源数", gt=0)
    active: bool = Field(description="新規の調理計画で利用する資源か")


class CookingSessionBackupRow(ContractModel):
    """調理計画実行の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    menu_id: UUID = Field(description="対象献立")
    menu_revision: int = Field(description="献立版", gt=0)
    status: Literal["planned", "cooking", "completed", "cancelled"] = Field(description="実行状態")
    target_at: AwareDatetime | None = Field(description="完成希望時刻")
    planner_version: str = Field(description="計画器の版", min_length=1, max_length=20000)
    input_snapshot: CookingInput = Field(description="材料・資源・人数の固定入力")
    input_hash: str = Field(description="入力ハッシュ", min_length=64, max_length=64)
    current_task_index: int = Field(description="調理画面の現在の工程位置(0始まり)")


class SessionTaskBackupRow(ContractModel):
    """展開済み工程の全列。ID・作成時刻も元の値を保持する。"""

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
    duration_source: Literal["recipe_rule", "user_estimate"] = Field(
        description="計画時間の根拠。料理の時間規則または利用者が確認した見積り"
    )
    confirmed_duration_s: int | None = Field(
        description="利用者が確認した工程の見積り秒数。実測値ではなく、計画後は変更しない"
    )


class TaskDependencyBackupRow(ContractModel):
    """献立展開後依存の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    before_task_id: UUID = Field(description="先行タスク")
    after_task_id: UUID = Field(description="後続タスク")
    min_lag_s: int = Field(description="最小間隔", ge=0)
    max_lag_s: int | None = Field(description="最大間隔")
    reason: str = Field(description="元DAG/洗浄/設備切替等", min_length=1, max_length=20000)


class ResourceReservationBackupRow(ContractModel):
    """資源の予約の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    task_id: UUID = Field(description="使用タスク")
    resource_id: UUID = Field(description="実資源")
    start_s: int = Field(description="占有開始", ge=0)
    end_s: int = Field(description="占有終了")
    quantity: int = Field(description="占有量", gt=0)


class IngredientTotalBackupRow(ContractModel):
    """献立材料集計結果の全列。ID・作成時刻も元の値を保持する。"""

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
    consumption_outcome: str = Field(
        description="未要求・反映済み・在庫不足・数量不明・単位不一致の結果",
        min_length=1,
        max_length=20000,
    )


class PantryLotBackupRow(ContractModel):
    """手持ち食材ロットの全列。ID・作成時刻も元の値を保持する。"""

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
    location: str = Field(description="冷蔵・冷凍・常温の保管場所", min_length=1, max_length=20000)
    priority: str = Field(description="先に使う優先指定", min_length=1, max_length=20000)
    status: str = Field(
        description="在庫の有効・削除・レシート取消状態", min_length=1, max_length=20000
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


class ShoppingItemBackupRow(ContractModel):
    """買い物行の全列。ID・作成時刻も元の値を保持する。"""

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


class ReceiptImportBackupRow(ContractModel):
    """レシート読取・在庫登録の処理単位の全列。ID・作成時刻も元の値を保持する。"""

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
    undo_preserved_count: int = Field(
        description="レシート取消時に編集・消費済みとして残した在庫件数"
    )


class ReceiptLineBackupRow(ContractModel):
    """レシートの商品候補と確定した在庫の対応の全列。ID・作成時刻も元の値を保持する。"""

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


class UserFoodBackupRow(ContractModel):
    """利用者が追加した独自食材の所有の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    food_id: UUID = Field(description="独自食材")


class UserPantryFoodBackupRow(ContractModel):
    """利用者が常備すると設定した食材の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    food_id: UUID = Field(description="常備食材")


class PantryConsumptionBackupRow(ContractModel):
    """調理による在庫消費の冪等台帳の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    user_id: UUID = Field(description="所有者")
    session_id: UUID = Field(description="消費した調理セッション")
    lot_id: UUID = Field(description="消費元ロット")
    amount: Decimal = Field(
        description="消費数量", max_digits=20, decimal_places=6, allow_inf_nan=False, gt=0
    )
    unit_id: UUID = Field(description="消費数量の単位")


class UserShoppingCheckBackupRow(ContractModel):
    """調理前の買い物確認の全列。ID・作成時刻も元の値を保持する。"""

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


class CatalogReleaseBackupRow(ContractModel):
    """カタログ公開版の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    version: str = Field(description="カタログ版番号", min_length=1, max_length=20000)
    manifest_hash: str = Field(
        description="採用したID・内容のハッシュ", min_length=64, max_length=64
    )
    published_at: AwareDatetime | None = Field(description="公開日時")
    owner_id: UUID | None = Field(description="私有カタログの所有者。NULLは共通カタログ")


class FoodBackupRow(ContractModel):
    """購入・利用食材概念の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    code: str = Field(description="固定食材コード", min_length=1, max_length=20000)
    name: str = Field(description="食材名・加工品種別", min_length=1, max_length=100)
    kind: Literal["basic", "processed", "ready_meal", "kit", "utility"] = Field(
        description="基本食材か加工食品か"
    )
    parent_id: UUID | None = Field(description="カテゴリ親")
    release_id: UUID = Field(description="所属公開版")
    status: Literal["active", "retired"] = Field(description="新規使用可否")
    owner_id: UUID | None = Field(description="私有食材の所有者。NULLは共通カタログ食材")


class FoodAliasBackupRow(ContractModel):
    """食材別名の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    food_id: UUID = Field(description="正規食材")
    alias: str = Field(description="別名・かな", min_length=1, max_length=500)
    locale: str = Field(description="言語・地域", min_length=1, max_length=20000)


class FoodFormBackupRow(ContractModel):
    """食材形態の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    food_id: UUID = Field(description="対応食材")
    name: str = Field(description="生皮付き・冷凍刻み等", min_length=1, max_length=500)
    state: Literal["raw", "dry", "frozen", "cooked", "rehydrated", "drained", "peeled", "ready"] = (
        Field(description="処理状態")
    )
    base_unit_id: UUID = Field(description="計算基準単位")
    quantity_basis: Literal["edible", "as_purchased", "drained", "prepared"] = Field(
        description="数量の対象部分"
    )
    status: Literal["active", "retired"] = Field(description="利用状態")


class FoodAxisOptionBackupRow(ContractModel):
    """食材の分類属性の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    food_id: UUID = Field(description="食材")
    option_id: UUID = Field(description="カテゴリ・入手性等の値")


class ProductBackupRow(ContractModel):
    """市販商品識別の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    food_id: UUID = Field(description="汎用食材との対応")
    brand: str = Field(description="ブランド", min_length=1, max_length=20000)
    name: str = Field(description="商品名", min_length=1, max_length=20000)
    gtin: str | None = Field(description="JAN等(先頭0保持)", min_length=1, max_length=20000)
    status: Literal["active", "retired"] = Field(description="終売はretired")


class ConversionBackupRow(ContractModel):
    """食材形態別換算の全列。ID・作成時刻も元の値を保持する。"""

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


class FoodAllergenBackupRow(ContractModel):
    """食材アレルゲン知識の全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    form_id: UUID = Field(description="食材形態")
    allergen_id: UUID = Field(description="対象物質")
    presence: Literal["contains", "may_contain", "absent_verified", "unknown"] = Field(
        description="含有・不明"
    )
    source_id: UUID = Field(description="判断根拠")


class ProductVersionBackupRow(ContractModel):
    """商品仕様版の全列。ID・作成時刻も元の値を保持する。"""

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


class ProductComponentBackupRow(ContractModel):
    """セット内構成品の全列。ID・作成時刻も元の値を保持する。"""

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


class ProductAllergenBackupRow(ContractModel):
    """商品表示アレルゲンの全列。ID・作成時刻も元の値を保持する。"""

    id: UUID = Field(description="不変の行識別子")
    created_at: AwareDatetime = Field(description="作成日時(UTC)")
    product_version_id: UUID = Field(description="商品仕様版")
    allergen_id: UUID = Field(description="物質")
    presence: Literal["contains", "may_contain", "absent_verified", "unknown"] = Field(
        description="表示状態"
    )
    source_id: UUID = Field(description="ラベル等")


class ProductPreparationRuleBackupRow(ContractModel):
    """商品固有の調理条件の全列。ID・作成時刻も元の値を保持する。"""

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


class NutritionFactBackupRow(ContractModel):
    """形態・商品別栄養値の全列。ID・作成時刻も元の値を保持する。"""

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


class FormYieldBackupRow(ContractModel):
    """処理歩留まりの全列。ID・作成時刻も元の値を保持する。"""

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


class BackupTables(ContractModel):
    """一部省略による意図しない消去を避け、全34表を必須にする。"""

    user_preference: list[UserPreferenceBackupRow] = Field(max_length=100000)
    user_exclusion: list[UserExclusionBackupRow] = Field(max_length=100000)
    user_recipe_event: list[UserRecipeEventBackupRow] = Field(max_length=100000)
    menu: list[MenuBackupRow] = Field(max_length=100000)
    menu_item: list[MenuItemBackupRow] = Field(max_length=100000)
    menu_ingredient_override: list[MenuIngredientOverrideBackupRow] = Field(max_length=100000)
    kitchen_resource: list[KitchenResourceBackupRow] = Field(max_length=100000)
    cooking_session: list[CookingSessionBackupRow] = Field(max_length=100000)
    session_task: list[SessionTaskBackupRow] = Field(max_length=100000)
    task_dependency: list[TaskDependencyBackupRow] = Field(max_length=100000)
    resource_reservation: list[ResourceReservationBackupRow] = Field(max_length=100000)
    ingredient_total: list[IngredientTotalBackupRow] = Field(max_length=100000)
    pantry_lot: list[PantryLotBackupRow] = Field(max_length=100000)
    shopping_item: list[ShoppingItemBackupRow] = Field(max_length=100000)
    receipt_import: list[ReceiptImportBackupRow] = Field(max_length=100000)
    receipt_line: list[ReceiptLineBackupRow] = Field(max_length=100000)
    user_food: list[UserFoodBackupRow] = Field(max_length=100000)
    user_pantry_food: list[UserPantryFoodBackupRow] = Field(max_length=100000)
    pantry_consumption: list[PantryConsumptionBackupRow] = Field(max_length=100000)
    user_shopping_check: list[UserShoppingCheckBackupRow] = Field(max_length=100000)
    catalog_release: list[CatalogReleaseBackupRow] = Field(max_length=100000)
    food: list[FoodBackupRow] = Field(max_length=100000)
    food_alias: list[FoodAliasBackupRow] = Field(max_length=100000)
    food_form: list[FoodFormBackupRow] = Field(max_length=100000)
    food_axis_option: list[FoodAxisOptionBackupRow] = Field(max_length=100000)
    product: list[ProductBackupRow] = Field(max_length=100000)
    conversion: list[ConversionBackupRow] = Field(max_length=100000)
    food_allergen: list[FoodAllergenBackupRow] = Field(max_length=100000)
    product_version: list[ProductVersionBackupRow] = Field(max_length=100000)
    product_component: list[ProductComponentBackupRow] = Field(max_length=100000)
    product_allergen: list[ProductAllergenBackupRow] = Field(max_length=100000)
    product_preparation_rule: list[ProductPreparationRuleBackupRow] = Field(max_length=100000)
    nutrition_fact: list[NutritionFactBackupRow] = Field(max_length=100000)
    form_yield: list[FormYieldBackupRow] = Field(max_length=100000)
