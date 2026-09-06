# 詳細設計: restore_backup

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/backups/restore` — 確認したバックアップで本人のデータを全置換する

## 入力と処理前提

| 項目 | 仕様 |
|---|---|
| authentication | 検証済みBearerトークンと本人所有権 |
| idempotency | 本人・本文digest・未使用intent・expectedVersionを照合し、確認を一度だけ消費する |
| transaction | 現在版をロックし、全行置換・確認消費・版増分・監査・outboxを一つのトランザクションで確定する |
| effects | 本人の全業務行・私有食品を置換し、現在版・監査・outboxを記録する |

| 入力場所 | 名前 | 型 | 必須 |
|---|---|---|---|

### 本文: application/json

| 入力 | 型 | 必須 | 制約 | 意味 |
|---|---|---|---|---|
| backup | BackupDocument-Input | 必須 | 追加制約なし |  |
| confirmed | boolean | 必須 | const=true | 全置換の最終確認を明示した場合だけtrue |
| expectedVersion | integer | 必須 | minimum=0.0 | Expectedversion |
| intentId | string (uuid) | 必須 | 追加制約なし | Intentid |

## データベースの対象と値の流れ

### `backend/src/app/apis/backup/restore_backup/sql/q001_lock_revision.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.workspace_revision | R | user_id: 所有者; revision: 全体のCAS版 |

対象条件: `WHERE user_id = %(actor_id)s`

行ロック: `FOR UPDATE`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

代入・選択式: `revision`

### `backend/src/app/apis/backup/restore_backup/sql/q002_profile.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.app_user | R | id: 不変の行識別子; locale: 表示言語; timezone: IANAタイムゾーン |

対象条件: `WHERE id = %(actor_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

代入・選択式: `locale; timezone`

### `backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.catalog_release | R | id: 不変の行識別子; created_at: 作成日時（UTC）; version: カタログ版番号; manifest_hash: 採用したID・内容のハッシュ; published_at: 公開日時; owner_id: 私有カタログの所有者。NULLは共通カタログ |
| recipeweave.conversion | R | id: 不変の行識別子; created_at: 作成日時（UTC）; form_id: 換算対象形態; from_unit_id: 入力単位; to_unit_id: 出力単位; factor: 出力量=入力量×倍率; quality: 実測・推定区別; source_id: 換算根拠; conditions: サイズ・温度・すり切り等; release_id: 換算版 |
| recipeweave.cooking_session | R | id: 不変の行識別子; created_at: 作成日時（UTC）; menu_id: 対象献立; menu_revision: 献立版; status: 実行状態; target_at: 完成希望時刻; planner_version: 計画器の版; input_snapshot: 材料・資源・人数の固定入力; input_hash: 入力ハッシュ; current_task_index: 調理画面の現在の工程位置（0始まり） |
| recipeweave.food | R | id: 不変の行識別子; created_at: 作成日時（UTC）; code: 固定食材コード; name: 食材名・加工品種別; kind: 基本食材か加工食品か; parent_id: カテゴリ親; release_id: 所属公開版; status: 新規使用可否; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.food_alias | R | id: 不変の行識別子; created_at: 作成日時（UTC）; food_id: 正規食材; alias: 別名・かな; locale: 言語・地域 |
| recipeweave.food_allergen | R | id: 不変の行識別子; created_at: 作成日時（UTC）; form_id: 食材形態; allergen_id: 対象物質; presence: 含有・不明; source_id: 判断根拠 |
| recipeweave.food_axis_option | R | id: 不変の行識別子; created_at: 作成日時（UTC）; food_id: 食材; option_id: カテゴリ・入手性等の値 |
| recipeweave.food_form | R | id: 不変の行識別子; created_at: 作成日時（UTC）; food_id: 対応食材; name: 生皮付き・冷凍刻み等; state: 処理状態; base_unit_id: 計算基準単位; quantity_basis: 数量の対象部分; status: 利用状態 |
| recipeweave.form_yield | R | id: 不変の行識別子; created_at: 作成日時（UTC）; input_form_id: 処理前形態; output_form_id: 処理後形態; yield_ratio: 出力量/入力量; source_id: 根拠; quality: 精度区分; conditions: 皮むき・水戻し等の条件 |
| recipeweave.ingredient_total | R | id: 不変の行識別子; created_at: 作成日時（UTC）; session_id: 固定計算対象; form_id: 合算可能な形態; product_version_id: 商品固定; unit_id: 基準単位; required_amount: 必要量; quality: 最も低い入力精度; calculation_version: 計算器版; actual_amount: 利用者が確定した実使用量。不明はNULL; consumption_outcome: 未要求・反映済み・在庫不足・数量不明・単位不一致の結果 |
| recipeweave.kitchen_resource | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; resource_type_id: コンロ・鍋・人等; name: 左コンロ・26cmフライパン等; capacity: 容量; quantity: 同等資源数; active: 新規の調理計画で利用する資源か |
| recipeweave.menu | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; name: 献立名; servings: 標準人数; revision: 楽観ロック版 |
| recipeweave.menu_ingredient_override | R | id: 不変の行識別子; created_at: 作成日時（UTC）; menu_item_id: 対象料理; ingredient_line_id: 元材料行; selected: 任意材料を使うか; amount: 適量等の確定基準量; form_id: 明示的代替形態; product_version_id: 購入商品指定 |
| recipeweave.menu_item | R | id: 不変の行識別子; created_at: 作成日時（UTC）; menu_id: 献立; recipe_version_id: 固定レシピ版; servings: その料理を作る人数; role_option_id: 主菜等; position: 表示順 |
| recipeweave.nutrition_fact | R | id: 不変の行識別子; created_at: 作成日時（UTC）; form_id: 汎用形態; product_version_id: 商品仕様; nutrient_id: 栄養成分; amount: 基準量あたり成分量; basis_amount: 基準量; basis_unit_id: 基準単位; source_id: 出典 |
| recipeweave.pantry_consumption | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; session_id: 消費した調理セッション; lot_id: 消費元ロット; amount: 消費数量; unit_id: 消費数量の単位 |
| recipeweave.pantry_lot | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; form_id: 食材形態; product_version_id: 商品版; amount: 残量; unit_id: 単位; expires_on: 表示期限; opened_at: 開封時点; location: 冷蔵・冷凍・常温の保管場所; priority: 先に使う優先指定; status: 在庫の有効・削除・レシート取消状態; source_import_id: 登録元レシート; quantity_quality: 数量の確定・不明; original_form_id: 登録時の食材形態; original_amount: 登録時数量。不明はNULL; original_unit_id: 登録時単位; updated_at: 最終編集日時; edited: 登録後の編集有無 |
| recipeweave.product | R | id: 不変の行識別子; created_at: 作成日時（UTC）; food_id: 汎用食材との対応; brand: ブランド; name: 商品名; gtin: JAN等（先頭0保持）; status: 終売はretired |
| recipeweave.product_allergen | R | id: 不変の行識別子; created_at: 作成日時（UTC）; product_version_id: 商品仕様版; allergen_id: 物質; presence: 表示状態; source_id: ラベル等 |
| recipeweave.product_component | R | id: 不変の行識別子; created_at: 作成日時（UTC）; product_version_id: 親商品版; form_id: 麺・ソース・かやく等; name: 構成品名; amount: 量（不明はNULL）; unit_id: 構成品量単位; quality: 数量の根拠 |
| recipeweave.product_preparation_rule | R | id: 不変の行識別子; created_at: 作成日時（UTC）; product_version_id: 対象商品仕様; operation_id: 対象標準動作; allowed: 表示で許可される方法か; use_original_container: 付属容器で調理するか; parameter_contract: 電力・注湯量・時間・蓋などの確定条件; source_id: 商品表示根拠 |
| recipeweave.product_version | R | id: 不変の行識別子; created_at: 作成日時（UTC）; product_id: 商品; version: 仕様版; form_id: 販売形態; net_amount: 1包装の内容量; unit_id: 内容量単位; drain_amount: 固形量; source_id: メーカー表示根拠; preparation_note: 容器・加熱方式・表示手順; valid_from: 適用開始日 |
| recipeweave.receipt_import | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; file_sha256: 画像本文のSHA256。本文はDBに保存しない; idempotency_key: 本人内で一意の再送防止キー; status: draft/committed/revertedの状態; revision: 楽観ロック版; committed_at: 在庫へ登録した日時; reverted_at: 登録取消日時; undo_preserved_count: レシート取消時に編集・消費済みとして残した在庫件数 |
| recipeweave.receipt_line | R | id: 不変の行識別子; created_at: 作成日時（UTC）; import_id: レシート処理; line_no: レシート内の表示順; raw_name: 利用者が確認できる商品原表記; form_id: 確定した食材形態; product_version_id: 確定した商品版; amount: 数量。不明はNULL; unit_id: 確定数量の単位; decision: accepted/skipped/unresolved; pantry_lot_id: 登録したロット |
| recipeweave.resource_reservation | R | id: 不変の行識別子; created_at: 作成日時（UTC）; task_id: 使用タスク; resource_id: 実資源; start_s: 占有開始; end_s: 占有終了; quantity: 占有量 |
| recipeweave.session_task | R | id: 不変の行識別子; created_at: 作成日時（UTC）; session_id: 実行; menu_item_id: 料理; step_id: 元工程; batch_no: 容量分割した回; planned_start_s: 開始相対秒; planned_end_s: 終了相対秒; status: 進捗; actual_start_at: 実開始; actual_end_at: 実完了; timer_started_at: 稼働中タイマーの開始日時; timer_duration_s: 利用者が設定したタイマー秒数; duration_source: 計画時間の根拠。料理の時間規則または利用者が確認した見積り; confirmed_duration_s: 利用者が確認した工程の見積り秒数。実測値ではなく、計画後は変更しない |
| recipeweave.shopping_item | R | id: 不変の行識別子; created_at: 作成日時（UTC）; session_id: 対象調理; total_id: 需要行; product_version_id: 購入SKU; net_shortage: 在庫控除後の不足量; package_count: 購入包装数; surplus_amount: 購入後余剰; checked: 購入済み; client_key: 画面操作の安定キー; checked_at: 購入確認日時; archived: 完了した買い物の保管状態 |
| recipeweave.task_dependency | R | id: 不変の行識別子; created_at: 作成日時（UTC）; before_task_id: 先行タスク; after_task_id: 後続タスク; min_lag_s: 最小間隔; max_lag_s: 最大間隔; reason: 元DAG/洗浄/設備切替等 |
| recipeweave.user_exclusion | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 利用者; food_id: 食材; allergen_id: アレルゲン; strict: 不明も除外するか |
| recipeweave.user_food | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; food_id: 独自食材 |
| recipeweave.user_pantry_food | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; food_id: 常備食材 |
| recipeweave.user_preference | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 利用者; option_id: 味・料理等; weight: 好みの重み |
| recipeweave.user_recipe_event | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 利用者; recipe_version_id: 提案版; kind: 提示/調理/評価; occurred_at: 発生時刻; request_key: リクエスト識別子 |
| recipeweave.user_shopping_check | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; key: 買い物対象の安定キー; signature: 数量・商品条件の一致確認用署名; food_id: 対象食材; amount: 必要数量。不明はNULL; unit_id: 数量単位; checked_at: 購入確認日時; archived: 保管済みか |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

代入・選択式: `(SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'option_id', t.option_id, 'weight', CAST(t.weight AS TEXT)) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.user_preference AS t WHERE (t.user_id = %(actor_id)s)) AS rows_user_preference; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'food_id', t.food_id, 'allergen_id', t.allergen_id, 'strict', t.strict) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.user_exclusion AS t WHERE (t.user_id = %(actor_id)s)) AS rows_user_exclusion; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'recipe_version_id', t.recipe_version_id, 'kind', t.kind, 'occurred_at', t.occurred_at, 'request_key', t.request_key) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.user_recipe_event AS t WHERE (t.user_id = %(actor_id)s)) AS rows_user_recipe_event; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'name', t.name, 'servings', CAST(t.servings AS TEXT), 'revision', t.revision) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.menu AS t WHERE (t.user_id = %(actor_id)s)) AS rows_menu; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'menu_id', t.menu_id, 'recipe_version_id', t.recipe_version_id, 'servings', CAST(t.servings AS TEXT), 'role_option_id', t.role_option_id, 'position', t.position) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.menu_item AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.menu AS owner_0 WHERE owner_0.id = t.menu_id AND owner_0.user_id = %(actor_id)s))) AS rows_menu_item; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'menu_item_id', t.menu_item_id, 'ingredient_line_id', t.ingredient_line_id, 'selected', t.selected, 'amount', CAST(t.amount AS TEXT), 'form_id', t.form_id, 'product_version_id', t.product_version_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.menu_ingredient_override AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.menu_item AS owner_0 WHERE owner_0.id = t.menu_item_id AND EXISTS(SELECT owner_1.id FROM recipeweave.menu AS owner_1 WHERE owner_1.id = owner_0.menu_id AND owner_1.user_id = %(actor_id)s)))) AS rows_menu_ingredient_override; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'resource_type_id', t.resource_type_id, 'name', t.name, 'capacity', CAST(t.capacity AS TEXT), 'quantity', t.quantity, 'active', t.active) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.kitchen_resource AS t WHERE (t.user_id = %(actor_id)s)) AS rows_kitchen_resource; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'menu_id', t.menu_id, 'menu_revision', t.menu_revision, 'status', t.status, 'target_at', t.target_at, 'planner_version', t.planner_version, 'input_snapshot', t.input_snapshot, 'input_hash', t.input_hash, 'current_task_index', t.current_task_index) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.cooking_session AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.menu AS owner_0 WHERE owner_0.id = t.menu_id AND owner_0.user_id = %(actor_id)s))) AS rows_cooking_session; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'session_id', t.session_id, 'menu_item_id', t.menu_item_id, 'step_id', t.step_id, 'batch_no', t.batch_no, 'planned_start_s', t.planned_start_s, 'planned_end_s', t.planned_end_s, 'status', t.status, 'actual_start_at', t.actual_start_at, 'actual_end_at', t.actual_end_at, 'timer_started_at', t.timer_started_at, 'timer_duration_s', t.timer_duration_s, 'duration_source', t.duration_source, 'confirmed_duration_s', t.confirmed_duration_s) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.session_task AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.cooking_session AS owner_0 WHERE owner_0.id = t.session_id AND EXISTS(SELECT owner_1.id FROM recipeweave.menu AS owner_1 WHERE owner_1.id = owner_0.menu_id AND owner_1.user_id = %(actor_id)s)))) AS rows_session_task; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'before_task_id', t.before_task_id, 'after_task_id', t.after_task_id, 'min_lag_s', t.min_lag_s, 'max_lag_s', t.max_lag_s, 'reason', t.reason) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.task_dependency AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.session_task AS owner_0 WHERE owner_0.id = t.before_task_id AND EXISTS(SELECT owner_1.id FROM recipeweave.cooking_session AS owner_1 WHERE owner_1.id = owner_0.session_id AND EXISTS(SELECT owner_2.id FROM recipeweave.menu AS owner_2 WHERE owner_2.id = owner_1.menu_id AND owner_2.user_id = %(actor_id)s))))) AS rows_task_dependency; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'task_id', t.task_id, 'resource_id', t.resource_id, 'start_s', t.start_s, 'end_s', t.end_s, 'quantity', t.quantity) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.resource_reservation AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.session_task AS owner_0 WHERE owner_0.id = t.task_id AND EXISTS(SELECT owner_1.id FROM recipeweave.cooking_session AS owner_1 WHERE owner_1.id = owner_0.session_id AND EXISTS(SELECT owner_2.id FROM recipeweave.menu AS owner_2 WHERE owner_2.id = owner_1.menu_id AND owner_2.user_id = %(actor_id)s))))) AS rows_resource_reservation; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'session_id', t.session_id, 'form_id', t.form_id, 'product_version_id', t.product_version_id, 'unit_id', t.unit_id, 'required_amount', CAST(t.required_amount AS TEXT), 'quality', t.quality, 'calculation_version', t.calculation_version, 'actual_amount', CAST(t.actual_amount AS TEXT), 'consumption_outcome', t.consumption_outcome) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.ingredient_total AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.cooking_session AS owner_0 WHERE owner_0.id = t.session_id AND EXISTS(SELECT owner_1.id FROM recipeweave.menu AS owner_1 WHERE owner_1.id = owner_0.menu_id AND owner_1.user_id = %(actor_id)s)))) AS rows_ingredient_total; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'form_id', t.form_id, 'product_version_id', t.product_version_id, 'amount', CAST(t.amount AS TEXT), 'unit_id', t.unit_id, 'expires_on', t.expires_on, 'opened_at', t.opened_at, 'location', t.location, 'priority', t.priority, 'status', t.status, 'source_import_id', t.source_import_id, 'quantity_quality', t.quantity_quality, 'original_form_id', t.original_form_id, 'original_amount', CAST(t.original_amount AS TEXT), 'original_unit_id', t.original_unit_id, 'updated_at', t.updated_at, 'edited', t.edited) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.pantry_lot AS t WHERE (t.user_id = %(actor_id)s)) AS rows_pantry_lot; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'session_id', t.session_id, 'total_id', t.total_id, 'product_version_id', t.product_version_id, 'net_shortage', CAST(t.net_shortage AS TEXT), 'package_count', t.package_count, 'surplus_amount', CAST(t.surplus_amount AS TEXT), 'checked', t.checked, 'client_key', t.client_key, 'checked_at', t.checked_at, 'archived', t.archived) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.shopping_item AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.cooking_session AS owner_0 WHERE owner_0.id = t.session_id AND EXISTS(SELECT owner_1.id FROM recipeweave.menu AS owner_1 WHERE owner_1.id = owner_0.menu_id AND owner_1.user_id = %(actor_id)s)))) AS rows_shopping_item; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'file_sha256', t.file_sha256, 'idempotency_key', t.idempotency_key, 'status', t.status, 'revision', CAST(t.revision AS TEXT), 'committed_at', t.committed_at, 'reverted_at', t.reverted_at, 'undo_preserved_count', t.undo_preserved_count) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.receipt_import AS t WHERE (t.user_id = %(actor_id)s)) AS rows_receipt_import; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'import_id', t.import_id, 'line_no', t.line_no, 'raw_name', t.raw_name, 'form_id', t.form_id, 'product_version_id', t.product_version_id, 'amount', CAST(t.amount AS TEXT), 'unit_id', t.unit_id, 'decision', t.decision, 'pantry_lot_id', t.pantry_lot_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.receipt_line AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.receipt_import AS owner_0 WHERE owner_0.id = t.import_id AND owner_0.user_id = %(actor_id)s))) AS rows_receipt_line; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'food_id', t.food_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.user_food AS t WHERE (t.user_id = %(actor_id)s)) AS rows_user_food; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'food_id', t.food_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.user_pantry_food AS t WHERE (t.user_id = %(actor_id)s)) AS rows_user_pantry_food; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'session_id', t.session_id, 'lot_id', t.lot_id, 'amount', CAST(t.amount AS TEXT), 'unit_id', t.unit_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.pantry_consumption AS t WHERE (t.user_id = %(actor_id)s)) AS rows_pantry_consumption; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'key', t.key, 'signature', t.signature, 'food_id', t.food_id, 'amount', CAST(t.amount AS TEXT), 'unit_id', t.unit_id, 'checked_at', t.checked_at, 'archived', t.archived) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.user_shopping_check AS t WHERE (t.user_id = %(actor_id)s)) AS rows_user_shopping_check; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'version', t.version, 'manifest_hash', t.manifest_hash, 'published_at', t.published_at, 'owner_id', t.owner_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.catalog_release AS t WHERE (t.owner_id = %(actor_id)s)) AS rows_catalog_release; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'code', t.code, 'name', t.name, 'kind', t.kind, 'parent_id', t.parent_id, 'release_id', t.release_id, 'status', t.status, 'owner_id', t.owner_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.food AS t WHERE (t.owner_id = %(actor_id)s)) AS rows_food; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'food_id', t.food_id, 'alias', t.alias, 'locale', t.locale) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.food_alias AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s))) AS rows_food_alias; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'food_id', t.food_id, 'name', t.name, 'state', t.state, 'base_unit_id', t.base_unit_id, 'quantity_basis', t.quantity_basis, 'status', t.status) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.food_form AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s))) AS rows_food_form; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'food_id', t.food_id, 'option_id', t.option_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.food_axis_option AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s))) AS rows_food_axis_option; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'food_id', t.food_id, 'brand', t.brand, 'name', t.name, 'gtin', t.gtin, 'status', t.status) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.product AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s))) AS rows_product; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'form_id', t.form_id, 'from_unit_id', t.from_unit_id, 'to_unit_id', t.to_unit_id, 'factor', CAST(t.factor AS TEXT), 'quality', t.quality, 'source_id', t.source_id, 'conditions', t.conditions, 'release_id', t.release_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.conversion AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s))) AS rows_conversion; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'form_id', t.form_id, 'allergen_id', t.allergen_id, 'presence', t.presence, 'source_id', t.source_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.food_allergen AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s))) AS rows_food_allergen; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'product_id', t.product_id, 'version', t.version, 'form_id', t.form_id, 'net_amount', CAST(t.net_amount AS TEXT), 'unit_id', t.unit_id, 'drain_amount', CAST(t.drain_amount AS TEXT), 'source_id', t.source_id, 'preparation_note', t.preparation_note, 'valid_from', t.valid_from) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.product_version AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id WHERE product.id = t.product_id AND food.owner_id = %(actor_id)s))) AS rows_product_version; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'product_version_id', t.product_version_id, 'form_id', t.form_id, 'name', t.name, 'amount', CAST(t.amount AS TEXT), 'unit_id', t.unit_id, 'quality', t.quality) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.product_component AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s))) AS rows_product_component; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'product_version_id', t.product_version_id, 'allergen_id', t.allergen_id, 'presence', t.presence, 'source_id', t.source_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.product_allergen AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s))) AS rows_product_allergen; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'product_version_id', t.product_version_id, 'operation_id', t.operation_id, 'allowed', t.allowed, 'use_original_container', t.use_original_container, 'parameter_contract', t.parameter_contract, 'source_id', t.source_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.product_preparation_rule AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s))) AS rows_product_preparation_rule; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'form_id', t.form_id, 'product_version_id', t.product_version_id, 'nutrient_id', t.nutrient_id, 'amount', CAST(t.amount AS TEXT), 'basis_amount', CAST(t.basis_amount AS TEXT), 'basis_unit_id', t.basis_unit_id, 'source_id', t.source_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.nutrition_fact AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s) OR EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s))) AS rows_nutrition_fact; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'input_form_id', t.input_form_id, 'output_form_id', t.output_form_id, 'yield_ratio', CAST(t.yield_ratio AS TEXT), 'source_id', t.source_id, 'quality', t.quality, 'conditions', t.conditions) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.form_yield AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id WHERE form.id = t.input_form_id AND food.owner_id = %(actor_id)s))) AS rows_form_yield`

### `backend/src/app/apis/backup/restore_backup/sql/q020_artifact.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.backup_artifact | R | id: バックアップ本文に含める不変の発行識別子; user_id: 発行先の本人。利用者消去後だけNULLへ匿名化する; body_sha256: 発行識別子を含む正規化済み本文全体のSHA-256; format_version: 対応するバックアップの形式版。現在は2 |

対象条件: `WHERE id = %(artifact_id)s AND user_id = %(actor_id)s AND body_sha256 = %(body_sha256)s AND format_version = 2`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |
| artifact_id | document.artifact_id (backend/src/app/core/backup_service.py:80) / request.backup.artifact_id (backend/src/app/core/backup_service.py:260) |
| body_sha256 | digest (backend/src/app/core/backup_service.py:80) / digest (backend/src/app/core/backup_service.py:260) / digest (backend/src/app/core/backup_service.py:274) |

代入・選択式: `id`

### `backend/src/app/apis/backup/restore_backup/sql/q023_lock_intent.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.backup_restore_intent | R | id: 確認画面へ返す不変の復元確認識別子; user_id: 復元する本人。利用者消去後だけNULLへ匿名化する; artifact_id: 本人へ発行したバックアップ証拠の識別子; body_sha256: 確認した本文全体のSHA-256。発行記録と一致する; current_revision: 確認時の現在データの更新版。復元直前にも同じ値であることを検査する; expires_at: 確認の有効期限。発行から最大15分; consumed_at: 復元と同一トランザクションで確定する使用日時。取消・再使用は不可 |

対象条件: `WHERE id = %(intent_id)s AND user_id = %(actor_id)s AND artifact_id = %(artifact_id)s AND body_sha256 = %(body_sha256)s AND current_revision = %(current_revision)s AND consumed_at IS NULL AND expires_at > CLOCK_TIMESTAMP()`

行ロック: `FOR UPDATE`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |
| artifact_id | document.artifact_id (backend/src/app/core/backup_service.py:80) / request.backup.artifact_id (backend/src/app/core/backup_service.py:260) |
| body_sha256 | digest (backend/src/app/core/backup_service.py:80) / digest (backend/src/app/core/backup_service.py:260) / digest (backend/src/app/core/backup_service.py:274) |
| current_revision | revision (backend/src/app/core/backup_service.py:260) / revision (backend/src/app/core/backup_service.py:274) |
| intent_id | request.intent_id (backend/src/app/core/backup_service.py:260) / request.intent_id (backend/src/app/core/backup_service.py:274) |

代入・選択式: `id`

### `backend/src/app/apis/backup/restore_backup/sql/q024_consume_intent.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.backup_restore_intent | U | id: 確認画面へ返す不変の復元確認識別子; user_id: 復元する本人。利用者消去後だけNULLへ匿名化する; body_sha256: 確認した本文全体のSHA-256。発行記録と一致する; current_revision: 確認時の現在データの更新版。復元直前にも同じ値であることを検査する; expires_at: 確認の有効期限。発行から最大15分; consumed_at: 復元と同一トランザクションで確定する使用日時。取消・再使用は不可 |

対象条件: `WHERE id = %(intent_id)s AND user_id = %(actor_id)s AND body_sha256 = %(body_sha256)s AND current_revision = %(current_revision)s AND consumed_at IS NULL AND expires_at > CLOCK_TIMESTAMP()`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |
| body_sha256 | digest (backend/src/app/core/backup_service.py:80) / digest (backend/src/app/core/backup_service.py:260) / digest (backend/src/app/core/backup_service.py:274) |
| current_revision | revision (backend/src/app/core/backup_service.py:260) / revision (backend/src/app/core/backup_service.py:274) |
| intent_id | request.intent_id (backend/src/app/core/backup_service.py:260) / request.intent_id (backend/src/app/core/backup_service.py:274) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| consumed_at | CLOCK_TIMESTAMP() |

代入・選択式: `consumed_at = CLOCK_TIMESTAMP()`

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_catalog_release.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.catalog_release | D | owner_id: 私有カタログの所有者。NULLは共通カタログ |

対象条件: `WHERE (t.owner_id = %(actor_id)s)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_conversion.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.conversion | D | form_id: 換算対象形態 |
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材 |

対象条件: `WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_cooking_session.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.cooking_session | D | menu_id: 対象献立 |
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |

対象条件: `WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.menu AS owner_0 WHERE owner_0.id = t.menu_id AND owner_0.user_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_food.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | D | owner_id: 私有食材の所有者。NULLは共通カタログ食材 |

対象条件: `WHERE (t.owner_id = %(actor_id)s)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_food_alias.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.food_alias | D | food_id: 正規食材 |

対象条件: `WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_food_allergen.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.food_allergen | D | form_id: 食材形態 |
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材 |

対象条件: `WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_food_axis_option.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.food_axis_option | D | food_id: 食材 |

対象条件: `WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_food_form.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.food_form | D | food_id: 対応食材 |

対象条件: `WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_form_yield.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材 |
| recipeweave.form_yield | D | input_form_id: 処理前形態 |

対象条件: `WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id WHERE form.id = t.input_form_id AND food.owner_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_ingredient_total.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.cooking_session | R | id: 不変の行識別子; menu_id: 対象献立 |
| recipeweave.ingredient_total | D | session_id: 固定計算対象 |
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |

対象条件: `WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.cooking_session AS owner_0 WHERE owner_0.id = t.session_id AND EXISTS(SELECT owner_1.id FROM recipeweave.menu AS owner_1 WHERE owner_1.id = owner_0.menu_id AND owner_1.user_id = %(actor_id)s)))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_kitchen_resource.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.kitchen_resource | D | user_id: 所有者 |

対象条件: `WHERE (t.user_id = %(actor_id)s)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_menu.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu | D | user_id: 所有者 |

対象条件: `WHERE (t.user_id = %(actor_id)s)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_menu_ingredient_override.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |
| recipeweave.menu_ingredient_override | D | menu_item_id: 対象料理 |
| recipeweave.menu_item | R | id: 不変の行識別子; menu_id: 献立 |

対象条件: `WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.menu_item AS owner_0 WHERE owner_0.id = t.menu_item_id AND EXISTS(SELECT owner_1.id FROM recipeweave.menu AS owner_1 WHERE owner_1.id = owner_0.menu_id AND owner_1.user_id = %(actor_id)s)))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_menu_item.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |
| recipeweave.menu_item | D | menu_id: 献立 |

対象条件: `WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.menu AS owner_0 WHERE owner_0.id = t.menu_id AND owner_0.user_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_nutrition_fact.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材 |
| recipeweave.nutrition_fact | D | form_id: 汎用形態; product_version_id: 商品仕様 |
| recipeweave.product | R | id: 不変の行識別子; food_id: 汎用食材との対応 |
| recipeweave.product_version | R | id: 不変の行識別子; product_id: 商品 |

対象条件: `WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s) OR EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_pantry_consumption.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.pantry_consumption | D | user_id: 所有者 |

対象条件: `WHERE (t.user_id = %(actor_id)s)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_pantry_lot.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.pantry_lot | D | user_id: 所有者 |

対象条件: `WHERE (t.user_id = %(actor_id)s)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_product.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.product | D | food_id: 汎用食材との対応 |

対象条件: `WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_product_allergen.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.product | R | id: 不変の行識別子; food_id: 汎用食材との対応 |
| recipeweave.product_allergen | D | product_version_id: 商品仕様版 |
| recipeweave.product_version | R | id: 不変の行識別子; product_id: 商品 |

対象条件: `WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_product_component.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.product | R | id: 不変の行識別子; food_id: 汎用食材との対応 |
| recipeweave.product_component | D | product_version_id: 親商品版 |
| recipeweave.product_version | R | id: 不変の行識別子; product_id: 商品 |

対象条件: `WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_product_preparation_rule.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.product | R | id: 不変の行識別子; food_id: 汎用食材との対応 |
| recipeweave.product_preparation_rule | D | product_version_id: 対象商品仕様 |
| recipeweave.product_version | R | id: 不変の行識別子; product_id: 商品 |

対象条件: `WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_product_version.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.product | R | id: 不変の行識別子; food_id: 汎用食材との対応 |
| recipeweave.product_version | D | product_id: 商品 |

対象条件: `WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id WHERE product.id = t.product_id AND food.owner_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_receipt_import.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.receipt_import | D | user_id: 所有者 |

対象条件: `WHERE (t.user_id = %(actor_id)s)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_receipt_line.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.receipt_import | R | id: 不変の行識別子; user_id: 所有者 |
| recipeweave.receipt_line | D | import_id: レシート処理 |

対象条件: `WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.receipt_import AS owner_0 WHERE owner_0.id = t.import_id AND owner_0.user_id = %(actor_id)s))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_resource_reservation.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.cooking_session | R | id: 不変の行識別子; menu_id: 対象献立 |
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |
| recipeweave.resource_reservation | D | task_id: 使用タスク |
| recipeweave.session_task | R | id: 不変の行識別子; session_id: 実行 |

対象条件: `WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.session_task AS owner_0 WHERE owner_0.id = t.task_id AND EXISTS(SELECT owner_1.id FROM recipeweave.cooking_session AS owner_1 WHERE owner_1.id = owner_0.session_id AND EXISTS(SELECT owner_2.id FROM recipeweave.menu AS owner_2 WHERE owner_2.id = owner_1.menu_id AND owner_2.user_id = %(actor_id)s))))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_session_task.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.cooking_session | R | id: 不変の行識別子; menu_id: 対象献立 |
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |
| recipeweave.session_task | D | session_id: 実行 |

対象条件: `WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.cooking_session AS owner_0 WHERE owner_0.id = t.session_id AND EXISTS(SELECT owner_1.id FROM recipeweave.menu AS owner_1 WHERE owner_1.id = owner_0.menu_id AND owner_1.user_id = %(actor_id)s)))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_shopping_item.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.cooking_session | R | id: 不変の行識別子; menu_id: 対象献立 |
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |
| recipeweave.shopping_item | D | session_id: 対象調理 |

対象条件: `WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.cooking_session AS owner_0 WHERE owner_0.id = t.session_id AND EXISTS(SELECT owner_1.id FROM recipeweave.menu AS owner_1 WHERE owner_1.id = owner_0.menu_id AND owner_1.user_id = %(actor_id)s)))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_task_dependency.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.cooking_session | R | id: 不変の行識別子; menu_id: 対象献立 |
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |
| recipeweave.session_task | R | id: 不変の行識別子; session_id: 実行 |
| recipeweave.task_dependency | D | before_task_id: 先行タスク |

対象条件: `WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.session_task AS owner_0 WHERE owner_0.id = t.before_task_id AND EXISTS(SELECT owner_1.id FROM recipeweave.cooking_session AS owner_1 WHERE owner_1.id = owner_0.session_id AND EXISTS(SELECT owner_2.id FROM recipeweave.menu AS owner_2 WHERE owner_2.id = owner_1.menu_id AND owner_2.user_id = %(actor_id)s))))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_exclusion.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.user_exclusion | D | user_id: 利用者 |

対象条件: `WHERE (t.user_id = %(actor_id)s)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_food.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.user_food | D | user_id: 所有者 |

対象条件: `WHERE (t.user_id = %(actor_id)s)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_pantry_food.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.user_pantry_food | D | user_id: 所有者 |

対象条件: `WHERE (t.user_id = %(actor_id)s)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_preference.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.user_preference | D | user_id: 利用者 |

対象条件: `WHERE (t.user_id = %(actor_id)s)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_recipe_event.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.user_recipe_event | D | user_id: 利用者 |

対象条件: `WHERE (t.user_id = %(actor_id)s)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_shopping_check.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.user_shopping_check | D | user_id: 所有者 |

対象条件: `WHERE (t.user_id = %(actor_id)s)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_catalog_release.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.catalog_release | C | id: 不変の行識別子; created_at: 作成日時（UTC）; version: カタログ版番号; manifest_hash: 採用したID・内容のハッシュ; published_at: 公開日時; owner_id: 私有カタログの所有者。NULLは共通カタログ |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| created_at | request.backup.tables.catalog_release の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.catalog_release の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| manifest_hash | request.backup.tables.catalog_release の各行.manifest_hash → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| owner_id | request.backup.tables.catalog_release の各行.owner_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| published_at | request.backup.tables.catalog_release の各行.published_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| version | request.backup.tables.catalog_release の各行.version → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| version | %(version)s |
| manifest_hash | %(manifest_hash)s |
| published_at | %(published_at)s |
| owner_id | %(owner_id)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_conversion.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.conversion | C | id: 不変の行識別子; created_at: 作成日時（UTC）; form_id: 換算対象形態; from_unit_id: 入力単位; to_unit_id: 出力単位; factor: 出力量=入力量×倍率; quality: 実測・推定区別; source_id: 換算根拠; conditions: サイズ・温度・すり切り等; release_id: 換算版 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| conditions | request.backup.tables.conversion の各行.conditions → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.conversion の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| factor | request.backup.tables.conversion の各行.factor → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| form_id | request.backup.tables.conversion の各行.form_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| from_unit_id | request.backup.tables.conversion の各行.from_unit_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.conversion の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| quality | request.backup.tables.conversion の各行.quality → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| release_id | request.backup.tables.conversion の各行.release_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| source_id | request.backup.tables.conversion の各行.source_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| to_unit_id | request.backup.tables.conversion の各行.to_unit_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| form_id | %(form_id)s |
| from_unit_id | %(from_unit_id)s |
| to_unit_id | %(to_unit_id)s |
| factor | %(factor)s |
| quality | %(quality)s |
| source_id | %(source_id)s |
| conditions | %(conditions)s |
| release_id | %(release_id)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_cooking_session.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.cooking_session | C | id: 不変の行識別子; created_at: 作成日時（UTC）; menu_id: 対象献立; menu_revision: 献立版; status: 実行状態; target_at: 完成希望時刻; planner_version: 計画器の版; input_snapshot: 材料・資源・人数の固定入力; input_hash: 入力ハッシュ; current_task_index: 調理画面の現在の工程位置（0始まり） |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| created_at | request.backup.tables.cooking_session の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| current_task_index | request.backup.tables.cooking_session の各行.current_task_index → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.cooking_session の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| input_hash | request.backup.tables.cooking_session の各行.input_hash → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| input_snapshot | request.backup.tables.cooking_session の各行.input_snapshot → document.tables.model_dump(mode='python') → data[table] → dict(row) → 非NULLならJsonb(to_jsonable_python(values[column]))へ変換 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| menu_id | request.backup.tables.cooking_session の各行.menu_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| menu_revision | request.backup.tables.cooking_session の各行.menu_revision → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| planner_version | request.backup.tables.cooking_session の各行.planner_version → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| status | request.backup.tables.cooking_session の各行.status → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| target_at | request.backup.tables.cooking_session の各行.target_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| menu_id | %(menu_id)s |
| menu_revision | %(menu_revision)s |
| status | %(status)s |
| target_at | %(target_at)s |
| planner_version | %(planner_version)s |
| input_snapshot | %(input_snapshot)s |
| input_hash | %(input_hash)s |
| current_task_index | %(current_task_index)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_food.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | C | id: 不変の行識別子; created_at: 作成日時（UTC）; code: 固定食材コード; name: 食材名・加工品種別; kind: 基本食材か加工食品か; parent_id: カテゴリ親; release_id: 所属公開版; status: 新規使用可否; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| code | request.backup.tables.food の各行.code → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.food の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.food の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| kind | request.backup.tables.food の各行.kind → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| name | request.backup.tables.food の各行.name → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| owner_id | request.backup.tables.food の各行.owner_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| parent_id | request.backup.tables.food の各行.parent_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| release_id | request.backup.tables.food の各行.release_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| status | request.backup.tables.food の各行.status → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| code | %(code)s |
| name | %(name)s |
| kind | %(kind)s |
| parent_id | %(parent_id)s |
| release_id | %(release_id)s |
| status | %(status)s |
| owner_id | %(owner_id)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_food_alias.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food_alias | C | id: 不変の行識別子; created_at: 作成日時（UTC）; food_id: 正規食材; alias: 別名・かな; locale: 言語・地域 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| alias | request.backup.tables.food_alias の各行.alias → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.food_alias の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| food_id | request.backup.tables.food_alias の各行.food_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.food_alias の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| locale | request.backup.tables.food_alias の各行.locale → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| food_id | %(food_id)s |
| alias | %(alias)s |
| locale | %(locale)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_food_allergen.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food_allergen | C | id: 不変の行識別子; created_at: 作成日時（UTC）; form_id: 食材形態; allergen_id: 対象物質; presence: 含有・不明; source_id: 判断根拠 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| allergen_id | request.backup.tables.food_allergen の各行.allergen_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.food_allergen の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| form_id | request.backup.tables.food_allergen の各行.form_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.food_allergen の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| presence | request.backup.tables.food_allergen の各行.presence → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| source_id | request.backup.tables.food_allergen の各行.source_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| form_id | %(form_id)s |
| allergen_id | %(allergen_id)s |
| presence | %(presence)s |
| source_id | %(source_id)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_food_axis_option.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food_axis_option | C | id: 不変の行識別子; created_at: 作成日時（UTC）; food_id: 食材; option_id: カテゴリ・入手性等の値 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| created_at | request.backup.tables.food_axis_option の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| food_id | request.backup.tables.food_axis_option の各行.food_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.food_axis_option の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| option_id | request.backup.tables.food_axis_option の各行.option_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| food_id | %(food_id)s |
| option_id | %(option_id)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_food_form.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food_form | C | id: 不変の行識別子; created_at: 作成日時（UTC）; food_id: 対応食材; name: 生皮付き・冷凍刻み等; state: 処理状態; base_unit_id: 計算基準単位; quantity_basis: 数量の対象部分; status: 利用状態 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| base_unit_id | request.backup.tables.food_form の各行.base_unit_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.food_form の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| food_id | request.backup.tables.food_form の各行.food_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.food_form の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| name | request.backup.tables.food_form の各行.name → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| quantity_basis | request.backup.tables.food_form の各行.quantity_basis → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| state | request.backup.tables.food_form の各行.state → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| status | request.backup.tables.food_form の各行.status → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| food_id | %(food_id)s |
| name | %(name)s |
| state | %(state)s |
| base_unit_id | %(base_unit_id)s |
| quantity_basis | %(quantity_basis)s |
| status | %(status)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_form_yield.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.form_yield | C | id: 不変の行識別子; created_at: 作成日時（UTC）; input_form_id: 処理前形態; output_form_id: 処理後形態; yield_ratio: 出力量/入力量; source_id: 根拠; quality: 精度区分; conditions: 皮むき・水戻し等の条件 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| conditions | request.backup.tables.form_yield の各行.conditions → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.form_yield の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.form_yield の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| input_form_id | request.backup.tables.form_yield の各行.input_form_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| output_form_id | request.backup.tables.form_yield の各行.output_form_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| quality | request.backup.tables.form_yield の各行.quality → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| source_id | request.backup.tables.form_yield の各行.source_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| yield_ratio | request.backup.tables.form_yield の各行.yield_ratio → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| input_form_id | %(input_form_id)s |
| output_form_id | %(output_form_id)s |
| yield_ratio | %(yield_ratio)s |
| source_id | %(source_id)s |
| quality | %(quality)s |
| conditions | %(conditions)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_ingredient_total.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.ingredient_total | C | id: 不変の行識別子; created_at: 作成日時（UTC）; session_id: 固定計算対象; form_id: 合算可能な形態; product_version_id: 商品固定; unit_id: 基準単位; required_amount: 必要量; quality: 最も低い入力精度; calculation_version: 計算器版; actual_amount: 利用者が確定した実使用量。不明はNULL; consumption_outcome: 未要求・反映済み・在庫不足・数量不明・単位不一致の結果 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actual_amount | request.backup.tables.ingredient_total の各行.actual_amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| calculation_version | request.backup.tables.ingredient_total の各行.calculation_version → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| consumption_outcome | request.backup.tables.ingredient_total の各行.consumption_outcome → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.ingredient_total の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| form_id | request.backup.tables.ingredient_total の各行.form_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.ingredient_total の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| product_version_id | request.backup.tables.ingredient_total の各行.product_version_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| quality | request.backup.tables.ingredient_total の各行.quality → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| required_amount | request.backup.tables.ingredient_total の各行.required_amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| session_id | request.backup.tables.ingredient_total の各行.session_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| unit_id | request.backup.tables.ingredient_total の各行.unit_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| session_id | %(session_id)s |
| form_id | %(form_id)s |
| product_version_id | %(product_version_id)s |
| unit_id | %(unit_id)s |
| required_amount | %(required_amount)s |
| quality | %(quality)s |
| calculation_version | %(calculation_version)s |
| actual_amount | %(actual_amount)s |
| consumption_outcome | %(consumption_outcome)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_kitchen_resource.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.kitchen_resource | C | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; resource_type_id: コンロ・鍋・人等; name: 左コンロ・26cmフライパン等; capacity: 容量; quantity: 同等資源数; active: 新規の調理計画で利用する資源か |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| active | request.backup.tables.kitchen_resource の各行.active → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| capacity | request.backup.tables.kitchen_resource の各行.capacity → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.kitchen_resource の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.kitchen_resource の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| name | request.backup.tables.kitchen_resource の各行.name → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| quantity | request.backup.tables.kitchen_resource の各行.quantity → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| resource_type_id | request.backup.tables.kitchen_resource の各行.resource_type_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| user_id | request.backup.tables.kitchen_resource の各行.user_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| user_id | %(user_id)s |
| resource_type_id | %(resource_type_id)s |
| name | %(name)s |
| capacity | %(capacity)s |
| quantity | %(quantity)s |
| active | %(active)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_menu.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu | C | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; name: 献立名; servings: 標準人数; revision: 楽観ロック版 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| created_at | request.backup.tables.menu の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.menu の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| name | request.backup.tables.menu の各行.name → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| revision | request.backup.tables.menu の各行.revision → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| servings | request.backup.tables.menu の各行.servings → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| user_id | request.backup.tables.menu の各行.user_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| user_id | %(user_id)s |
| name | %(name)s |
| servings | %(servings)s |
| revision | %(revision)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_menu_ingredient_override.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu_ingredient_override | C | id: 不変の行識別子; created_at: 作成日時（UTC）; menu_item_id: 対象料理; ingredient_line_id: 元材料行; selected: 任意材料を使うか; amount: 適量等の確定基準量; form_id: 明示的代替形態; product_version_id: 購入商品指定 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| amount | request.backup.tables.menu_ingredient_override の各行.amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.menu_ingredient_override の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| form_id | request.backup.tables.menu_ingredient_override の各行.form_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.menu_ingredient_override の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| ingredient_line_id | request.backup.tables.menu_ingredient_override の各行.ingredient_line_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| menu_item_id | request.backup.tables.menu_ingredient_override の各行.menu_item_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| product_version_id | request.backup.tables.menu_ingredient_override の各行.product_version_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| selected | request.backup.tables.menu_ingredient_override の各行.selected → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| menu_item_id | %(menu_item_id)s |
| ingredient_line_id | %(ingredient_line_id)s |
| selected | %(selected)s |
| amount | %(amount)s |
| form_id | %(form_id)s |
| product_version_id | %(product_version_id)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_menu_item.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu_item | C | id: 不変の行識別子; created_at: 作成日時（UTC）; menu_id: 献立; recipe_version_id: 固定レシピ版; servings: その料理を作る人数; role_option_id: 主菜等; position: 表示順 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| created_at | request.backup.tables.menu_item の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.menu_item の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| menu_id | request.backup.tables.menu_item の各行.menu_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| position | request.backup.tables.menu_item の各行.position → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| recipe_version_id | request.backup.tables.menu_item の各行.recipe_version_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| role_option_id | request.backup.tables.menu_item の各行.role_option_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| servings | request.backup.tables.menu_item の各行.servings → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| menu_id | %(menu_id)s |
| recipe_version_id | %(recipe_version_id)s |
| servings | %(servings)s |
| role_option_id | %(role_option_id)s |
| position | %(position)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_nutrition_fact.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.nutrition_fact | C | id: 不変の行識別子; created_at: 作成日時（UTC）; form_id: 汎用形態; product_version_id: 商品仕様; nutrient_id: 栄養成分; amount: 基準量あたり成分量; basis_amount: 基準量; basis_unit_id: 基準単位; source_id: 出典 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| amount | request.backup.tables.nutrition_fact の各行.amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| basis_amount | request.backup.tables.nutrition_fact の各行.basis_amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| basis_unit_id | request.backup.tables.nutrition_fact の各行.basis_unit_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.nutrition_fact の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| form_id | request.backup.tables.nutrition_fact の各行.form_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.nutrition_fact の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| nutrient_id | request.backup.tables.nutrition_fact の各行.nutrient_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| product_version_id | request.backup.tables.nutrition_fact の各行.product_version_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| source_id | request.backup.tables.nutrition_fact の各行.source_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| form_id | %(form_id)s |
| product_version_id | %(product_version_id)s |
| nutrient_id | %(nutrient_id)s |
| amount | %(amount)s |
| basis_amount | %(basis_amount)s |
| basis_unit_id | %(basis_unit_id)s |
| source_id | %(source_id)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_pantry_consumption.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.pantry_consumption | C | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; session_id: 消費した調理セッション; lot_id: 消費元ロット; amount: 消費数量; unit_id: 消費数量の単位 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| amount | request.backup.tables.pantry_consumption の各行.amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.pantry_consumption の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.pantry_consumption の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| lot_id | request.backup.tables.pantry_consumption の各行.lot_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| session_id | request.backup.tables.pantry_consumption の各行.session_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| unit_id | request.backup.tables.pantry_consumption の各行.unit_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| user_id | request.backup.tables.pantry_consumption の各行.user_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| user_id | %(user_id)s |
| session_id | %(session_id)s |
| lot_id | %(lot_id)s |
| amount | %(amount)s |
| unit_id | %(unit_id)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_pantry_lot.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.pantry_lot | C | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; form_id: 食材形態; product_version_id: 商品版; amount: 残量; unit_id: 単位; expires_on: 表示期限; opened_at: 開封時点; location: 冷蔵・冷凍・常温の保管場所; priority: 先に使う優先指定; status: 在庫の有効・削除・レシート取消状態; source_import_id: 登録元レシート; quantity_quality: 数量の確定・不明; original_form_id: 登録時の食材形態; original_amount: 登録時数量。不明はNULL; original_unit_id: 登録時単位; updated_at: 最終編集日時; edited: 登録後の編集有無 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| amount | request.backup.tables.pantry_lot の各行.amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.pantry_lot の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| edited | request.backup.tables.pantry_lot の各行.edited → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| expires_on | request.backup.tables.pantry_lot の各行.expires_on → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| form_id | request.backup.tables.pantry_lot の各行.form_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.pantry_lot の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| location | request.backup.tables.pantry_lot の各行.location → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| opened_at | request.backup.tables.pantry_lot の各行.opened_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| original_amount | request.backup.tables.pantry_lot の各行.original_amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| original_form_id | request.backup.tables.pantry_lot の各行.original_form_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| original_unit_id | request.backup.tables.pantry_lot の各行.original_unit_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| priority | request.backup.tables.pantry_lot の各行.priority → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| product_version_id | request.backup.tables.pantry_lot の各行.product_version_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| quantity_quality | request.backup.tables.pantry_lot の各行.quantity_quality → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| source_import_id | request.backup.tables.pantry_lot の各行.source_import_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| status | request.backup.tables.pantry_lot の各行.status → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| unit_id | request.backup.tables.pantry_lot の各行.unit_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| updated_at | request.backup.tables.pantry_lot の各行.updated_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| user_id | request.backup.tables.pantry_lot の各行.user_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| user_id | %(user_id)s |
| form_id | %(form_id)s |
| product_version_id | %(product_version_id)s |
| amount | %(amount)s |
| unit_id | %(unit_id)s |
| expires_on | %(expires_on)s |
| opened_at | %(opened_at)s |
| location | %(location)s |
| priority | %(priority)s |
| status | %(status)s |
| source_import_id | %(source_import_id)s |
| quantity_quality | %(quantity_quality)s |
| original_form_id | %(original_form_id)s |
| original_amount | %(original_amount)s |
| original_unit_id | %(original_unit_id)s |
| updated_at | %(updated_at)s |
| edited | %(edited)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_product.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.product | C | id: 不変の行識別子; created_at: 作成日時（UTC）; food_id: 汎用食材との対応; brand: ブランド; name: 商品名; gtin: JAN等（先頭0保持）; status: 終売はretired |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| brand | request.backup.tables.product の各行.brand → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.product の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| food_id | request.backup.tables.product の各行.food_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| gtin | request.backup.tables.product の各行.gtin → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.product の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| name | request.backup.tables.product の各行.name → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| status | request.backup.tables.product の各行.status → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| food_id | %(food_id)s |
| brand | %(brand)s |
| name | %(name)s |
| gtin | %(gtin)s |
| status | %(status)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_product_allergen.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.product_allergen | C | id: 不変の行識別子; created_at: 作成日時（UTC）; product_version_id: 商品仕様版; allergen_id: 物質; presence: 表示状態; source_id: ラベル等 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| allergen_id | request.backup.tables.product_allergen の各行.allergen_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.product_allergen の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.product_allergen の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| presence | request.backup.tables.product_allergen の各行.presence → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| product_version_id | request.backup.tables.product_allergen の各行.product_version_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| source_id | request.backup.tables.product_allergen の各行.source_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| product_version_id | %(product_version_id)s |
| allergen_id | %(allergen_id)s |
| presence | %(presence)s |
| source_id | %(source_id)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_product_component.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.product_component | C | id: 不変の行識別子; created_at: 作成日時（UTC）; product_version_id: 親商品版; form_id: 麺・ソース・かやく等; name: 構成品名; amount: 量（不明はNULL）; unit_id: 構成品量単位; quality: 数量の根拠 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| amount | request.backup.tables.product_component の各行.amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.product_component の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| form_id | request.backup.tables.product_component の各行.form_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.product_component の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| name | request.backup.tables.product_component の各行.name → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| product_version_id | request.backup.tables.product_component の各行.product_version_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| quality | request.backup.tables.product_component の各行.quality → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| unit_id | request.backup.tables.product_component の各行.unit_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| product_version_id | %(product_version_id)s |
| form_id | %(form_id)s |
| name | %(name)s |
| amount | %(amount)s |
| unit_id | %(unit_id)s |
| quality | %(quality)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_product_preparation_rule.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.product_preparation_rule | C | id: 不変の行識別子; created_at: 作成日時（UTC）; product_version_id: 対象商品仕様; operation_id: 対象標準動作; allowed: 表示で許可される方法か; use_original_container: 付属容器で調理するか; parameter_contract: 電力・注湯量・時間・蓋などの確定条件; source_id: 商品表示根拠 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| allowed | request.backup.tables.product_preparation_rule の各行.allowed → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.product_preparation_rule の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.product_preparation_rule の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| operation_id | request.backup.tables.product_preparation_rule の各行.operation_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| parameter_contract | request.backup.tables.product_preparation_rule の各行.parameter_contract → document.tables.model_dump(mode='python') → data[table] → dict(row) → 非NULLならJsonb(to_jsonable_python(values[column]))へ変換 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| product_version_id | request.backup.tables.product_preparation_rule の各行.product_version_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| source_id | request.backup.tables.product_preparation_rule の各行.source_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| use_original_container | request.backup.tables.product_preparation_rule の各行.use_original_container → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| product_version_id | %(product_version_id)s |
| operation_id | %(operation_id)s |
| allowed | %(allowed)s |
| use_original_container | %(use_original_container)s |
| parameter_contract | %(parameter_contract)s |
| source_id | %(source_id)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_product_version.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.product_version | C | id: 不変の行識別子; created_at: 作成日時（UTC）; product_id: 商品; version: 仕様版; form_id: 販売形態; net_amount: 1包装の内容量; unit_id: 内容量単位; drain_amount: 固形量; source_id: メーカー表示根拠; preparation_note: 容器・加熱方式・表示手順; valid_from: 適用開始日 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| created_at | request.backup.tables.product_version の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| drain_amount | request.backup.tables.product_version の各行.drain_amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| form_id | request.backup.tables.product_version の各行.form_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.product_version の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| net_amount | request.backup.tables.product_version の各行.net_amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| preparation_note | request.backup.tables.product_version の各行.preparation_note → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| product_id | request.backup.tables.product_version の各行.product_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| source_id | request.backup.tables.product_version の各行.source_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| unit_id | request.backup.tables.product_version の各行.unit_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| valid_from | request.backup.tables.product_version の各行.valid_from → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| version | request.backup.tables.product_version の各行.version → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| product_id | %(product_id)s |
| version | %(version)s |
| form_id | %(form_id)s |
| net_amount | %(net_amount)s |
| unit_id | %(unit_id)s |
| drain_amount | %(drain_amount)s |
| source_id | %(source_id)s |
| preparation_note | %(preparation_note)s |
| valid_from | %(valid_from)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_receipt_import.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.receipt_import | C | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; file_sha256: 画像本文のSHA256。本文はDBに保存しない; idempotency_key: 本人内で一意の再送防止キー; status: draft/committed/revertedの状態; revision: 楽観ロック版; committed_at: 在庫へ登録した日時; reverted_at: 登録取消日時; undo_preserved_count: レシート取消時に編集・消費済みとして残した在庫件数 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| committed_at | request.backup.tables.receipt_import の各行.committed_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.receipt_import の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| file_sha256 | request.backup.tables.receipt_import の各行.file_sha256 → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.receipt_import の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| idempotency_key | request.backup.tables.receipt_import の各行.idempotency_key → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| reverted_at | request.backup.tables.receipt_import の各行.reverted_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| revision | request.backup.tables.receipt_import の各行.revision → document.tables.model_dump(mode='python') → data[table] → dict(row) → 非NULLならint(values[column])へ変換 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| status | request.backup.tables.receipt_import の各行.status → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| undo_preserved_count | request.backup.tables.receipt_import の各行.undo_preserved_count → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| user_id | request.backup.tables.receipt_import の各行.user_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| user_id | %(user_id)s |
| file_sha256 | %(file_sha256)s |
| idempotency_key | %(idempotency_key)s |
| status | %(status)s |
| revision | %(revision)s |
| committed_at | %(committed_at)s |
| reverted_at | %(reverted_at)s |
| undo_preserved_count | %(undo_preserved_count)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_receipt_line.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.receipt_line | C | id: 不変の行識別子; created_at: 作成日時（UTC）; import_id: レシート処理; line_no: レシート内の表示順; raw_name: 利用者が確認できる商品原表記; form_id: 確定した食材形態; product_version_id: 確定した商品版; amount: 数量。不明はNULL; unit_id: 確定数量の単位; decision: accepted/skipped/unresolved; pantry_lot_id: 登録したロット |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| amount | request.backup.tables.receipt_line の各行.amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.receipt_line の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| decision | request.backup.tables.receipt_line の各行.decision → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| form_id | request.backup.tables.receipt_line の各行.form_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.receipt_line の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| import_id | request.backup.tables.receipt_line の各行.import_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| line_no | request.backup.tables.receipt_line の各行.line_no → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| pantry_lot_id | request.backup.tables.receipt_line の各行.pantry_lot_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| product_version_id | request.backup.tables.receipt_line の各行.product_version_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| raw_name | request.backup.tables.receipt_line の各行.raw_name → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| unit_id | request.backup.tables.receipt_line の各行.unit_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| import_id | %(import_id)s |
| line_no | %(line_no)s |
| raw_name | %(raw_name)s |
| form_id | %(form_id)s |
| product_version_id | %(product_version_id)s |
| amount | %(amount)s |
| unit_id | %(unit_id)s |
| decision | %(decision)s |
| pantry_lot_id | %(pantry_lot_id)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_resource_reservation.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.resource_reservation | C | id: 不変の行識別子; created_at: 作成日時（UTC）; task_id: 使用タスク; resource_id: 実資源; start_s: 占有開始; end_s: 占有終了; quantity: 占有量 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| created_at | request.backup.tables.resource_reservation の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| end_s | request.backup.tables.resource_reservation の各行.end_s → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.resource_reservation の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| quantity | request.backup.tables.resource_reservation の各行.quantity → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| resource_id | request.backup.tables.resource_reservation の各行.resource_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| start_s | request.backup.tables.resource_reservation の各行.start_s → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| task_id | request.backup.tables.resource_reservation の各行.task_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| task_id | %(task_id)s |
| resource_id | %(resource_id)s |
| start_s | %(start_s)s |
| end_s | %(end_s)s |
| quantity | %(quantity)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_session_task.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.session_task | C | id: 不変の行識別子; created_at: 作成日時（UTC）; session_id: 実行; menu_item_id: 料理; step_id: 元工程; batch_no: 容量分割した回; planned_start_s: 開始相対秒; planned_end_s: 終了相対秒; status: 進捗; actual_start_at: 実開始; actual_end_at: 実完了; timer_started_at: 稼働中タイマーの開始日時; timer_duration_s: 利用者が設定したタイマー秒数; duration_source: 計画時間の根拠。料理の時間規則または利用者が確認した見積り; confirmed_duration_s: 利用者が確認した工程の見積り秒数。実測値ではなく、計画後は変更しない |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actual_end_at | request.backup.tables.session_task の各行.actual_end_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| actual_start_at | request.backup.tables.session_task の各行.actual_start_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| batch_no | request.backup.tables.session_task の各行.batch_no → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| confirmed_duration_s | request.backup.tables.session_task の各行.confirmed_duration_s → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.session_task の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| duration_source | request.backup.tables.session_task の各行.duration_source → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.session_task の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| menu_item_id | request.backup.tables.session_task の各行.menu_item_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| planned_end_s | request.backup.tables.session_task の各行.planned_end_s → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| planned_start_s | request.backup.tables.session_task の各行.planned_start_s → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| session_id | request.backup.tables.session_task の各行.session_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| status | request.backup.tables.session_task の各行.status → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| step_id | request.backup.tables.session_task の各行.step_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| timer_duration_s | request.backup.tables.session_task の各行.timer_duration_s → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| timer_started_at | request.backup.tables.session_task の各行.timer_started_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| session_id | %(session_id)s |
| menu_item_id | %(menu_item_id)s |
| step_id | %(step_id)s |
| batch_no | %(batch_no)s |
| planned_start_s | %(planned_start_s)s |
| planned_end_s | %(planned_end_s)s |
| status | %(status)s |
| actual_start_at | %(actual_start_at)s |
| actual_end_at | %(actual_end_at)s |
| timer_started_at | %(timer_started_at)s |
| timer_duration_s | %(timer_duration_s)s |
| duration_source | %(duration_source)s |
| confirmed_duration_s | %(confirmed_duration_s)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_shopping_item.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.shopping_item | C | id: 不変の行識別子; created_at: 作成日時（UTC）; session_id: 対象調理; total_id: 需要行; product_version_id: 購入SKU; net_shortage: 在庫控除後の不足量; package_count: 購入包装数; surplus_amount: 購入後余剰; checked: 購入済み; client_key: 画面操作の安定キー; checked_at: 購入確認日時; archived: 完了した買い物の保管状態 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| archived | request.backup.tables.shopping_item の各行.archived → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| checked | request.backup.tables.shopping_item の各行.checked → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| checked_at | request.backup.tables.shopping_item の各行.checked_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| client_key | request.backup.tables.shopping_item の各行.client_key → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.shopping_item の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.shopping_item の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| net_shortage | request.backup.tables.shopping_item の各行.net_shortage → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| package_count | request.backup.tables.shopping_item の各行.package_count → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| product_version_id | request.backup.tables.shopping_item の各行.product_version_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| session_id | request.backup.tables.shopping_item の各行.session_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| surplus_amount | request.backup.tables.shopping_item の各行.surplus_amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| total_id | request.backup.tables.shopping_item の各行.total_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| session_id | %(session_id)s |
| total_id | %(total_id)s |
| product_version_id | %(product_version_id)s |
| net_shortage | %(net_shortage)s |
| package_count | %(package_count)s |
| surplus_amount | %(surplus_amount)s |
| checked | %(checked)s |
| client_key | %(client_key)s |
| checked_at | %(checked_at)s |
| archived | %(archived)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_task_dependency.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.task_dependency | C | id: 不変の行識別子; created_at: 作成日時（UTC）; before_task_id: 先行タスク; after_task_id: 後続タスク; min_lag_s: 最小間隔; max_lag_s: 最大間隔; reason: 元DAG/洗浄/設備切替等 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| after_task_id | request.backup.tables.task_dependency の各行.after_task_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| before_task_id | request.backup.tables.task_dependency の各行.before_task_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.task_dependency の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.task_dependency の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| max_lag_s | request.backup.tables.task_dependency の各行.max_lag_s → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| min_lag_s | request.backup.tables.task_dependency の各行.min_lag_s → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| reason | request.backup.tables.task_dependency の各行.reason → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| before_task_id | %(before_task_id)s |
| after_task_id | %(after_task_id)s |
| min_lag_s | %(min_lag_s)s |
| max_lag_s | %(max_lag_s)s |
| reason | %(reason)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_exclusion.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.user_exclusion | C | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 利用者; food_id: 食材; allergen_id: アレルゲン; strict: 不明も除外するか |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| allergen_id | request.backup.tables.user_exclusion の各行.allergen_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.user_exclusion の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| food_id | request.backup.tables.user_exclusion の各行.food_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.user_exclusion の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| strict | request.backup.tables.user_exclusion の各行.strict → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| user_id | request.backup.tables.user_exclusion の各行.user_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| user_id | %(user_id)s |
| food_id | %(food_id)s |
| allergen_id | %(allergen_id)s |
| strict | %(strict)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_food.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.user_food | C | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; food_id: 独自食材 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| created_at | request.backup.tables.user_food の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| food_id | request.backup.tables.user_food の各行.food_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.user_food の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| user_id | request.backup.tables.user_food の各行.user_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| user_id | %(user_id)s |
| food_id | %(food_id)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_pantry_food.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.user_pantry_food | C | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; food_id: 常備食材 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| created_at | request.backup.tables.user_pantry_food の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| food_id | request.backup.tables.user_pantry_food の各行.food_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.user_pantry_food の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| user_id | request.backup.tables.user_pantry_food の各行.user_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| user_id | %(user_id)s |
| food_id | %(food_id)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_preference.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.user_preference | C | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 利用者; option_id: 味・料理等; weight: 好みの重み |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| created_at | request.backup.tables.user_preference の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.user_preference の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| option_id | request.backup.tables.user_preference の各行.option_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| user_id | request.backup.tables.user_preference の各行.user_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| weight | request.backup.tables.user_preference の各行.weight → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| user_id | %(user_id)s |
| option_id | %(option_id)s |
| weight | %(weight)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_recipe_event.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.user_recipe_event | C | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 利用者; recipe_version_id: 提案版; kind: 提示/調理/評価; occurred_at: 発生時刻; request_key: リクエスト識別子 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| created_at | request.backup.tables.user_recipe_event の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.user_recipe_event の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| kind | request.backup.tables.user_recipe_event の各行.kind → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| occurred_at | request.backup.tables.user_recipe_event の各行.occurred_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| recipe_version_id | request.backup.tables.user_recipe_event の各行.recipe_version_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| request_key | request.backup.tables.user_recipe_event の各行.request_key → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| user_id | request.backup.tables.user_recipe_event の各行.user_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| user_id | %(user_id)s |
| recipe_version_id | %(recipe_version_id)s |
| kind | %(kind)s |
| occurred_at | %(occurred_at)s |
| request_key | %(request_key)s |

### `backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_shopping_check.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.user_shopping_check | C | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; key: 買い物対象の安定キー; signature: 数量・商品条件の一致確認用署名; food_id: 対象食材; amount: 必要数量。不明はNULL; unit_id: 数量単位; checked_at: 購入確認日時; archived: 保管済みか |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| amount | request.backup.tables.user_shopping_check の各行.amount → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| archived | request.backup.tables.user_shopping_check の各行.archived → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| checked_at | request.backup.tables.user_shopping_check の各行.checked_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| created_at | request.backup.tables.user_shopping_check の各行.created_at → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| food_id | request.backup.tables.user_shopping_check の各行.food_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| id | request.backup.tables.user_shopping_check の各行.id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| key | request.backup.tables.user_shopping_check の各行.key → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| signature | request.backup.tables.user_shopping_check の各行.signature → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| unit_id | request.backup.tables.user_shopping_check の各行.unit_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |
| user_id | request.backup.tables.user_shopping_check の各行.user_id → document.tables.model_dump(mode='python') → data[table] → dict(row) → 値を維持 → **valuesの名前付きSQL引数。(backend/src/app/core/backup_service.py:116, 171) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(id)s |
| created_at | %(created_at)s |
| user_id | %(user_id)s |
| key | %(key)s |
| signature | %(signature)s |
| food_id | %(food_id)s |
| amount | %(amount)s |
| unit_id | %(unit_id)s |
| checked_at | %(checked_at)s |
| archived | %(archived)s |

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_allergen.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.allergen | R | id: 不変の行識別子 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (TRUE)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_axis_option.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.axis_option | R | id: 不変の行識別子 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (TRUE)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_catalog_release.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.catalog_release | R | id: 不変の行識別子; owner_id: 私有カタログの所有者。NULLは共通カタログ |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (t.owner_id IS NULL)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_food.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (t.owner_id IS NULL)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_food_form.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id IS NULL))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_nutrient.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.nutrient | R | id: 不変の行識別子 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (TRUE)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_operation.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.operation | R | id: 不変の行識別子 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (TRUE)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_product.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.product | R | id: 不変の行識別子; food_id: 汎用食材との対応 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id IS NULL))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_product_version.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; owner_id: 私有食材の所有者。NULLは共通カタログ食材 |
| recipeweave.product | R | id: 不変の行識別子; food_id: 汎用食材との対応 |
| recipeweave.product_version | R | id: 不変の行識別子; product_id: 商品 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id WHERE product.id = t.product_id AND food.owner_id IS NULL))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_recipe_ingredient.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.recipe_ingredient | R | id: 不変の行識別子 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (TRUE)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_recipe_step.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.recipe_step | R | id: 不変の行識別子 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (TRUE)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_recipe_version.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.recipe_version | R | id: 不変の行識別子 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (TRUE)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_resource_type.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.resource_type | R | id: 不変の行識別子 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (TRUE)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_source_record.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.source_record | R | id: 不変の行識別子 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (TRUE)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q300_reference_unit.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.unit | R | id: 不変の行識別子 |

対象条件: `WHERE t.id = ANY(CAST(%(reference_ids)s AS UUID[])) AND (TRUE)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| reference_ids | sorted(values) (backend/src/app/core/backup_service.py:166) |

代入・選択式: `t.id`

### `backend/src/app/apis/backup/restore_backup/sql/q800_constraints_immediate.sql`

実行条件: このSQLの呼出し経路で実行

保留していた遅延可能な制約を直ちに検査し、以後も即時検査する。

この文自体の行CRUDはない。制約違反は呼出元へ返し、プレビューの試験書込みを保持するか戻すかは呼出元のトランザクション制御に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q801_constraints_deferred.sql`

実行条件: このSQLの呼出し経路で実行

遅延可能な制約の検査をトランザクション終了まで遅延する。

この文自体の行CRUDはない。制約違反は呼出元へ返し、プレビューの試験書込みを保持するか戻すかは呼出元のトランザクション制御に従う。

### `backend/src/app/apis/backup/restore_backup/sql/q802_restore_profile.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.app_user | U | id: 不変の行識別子; locale: 表示言語; timezone: IANAタイムゾーン |

対象条件: `WHERE id = %(actor_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |
| locale | document.profile.locale (backend/src/app/core/backup_service.py:186) |
| timezone | document.profile.timezone (backend/src/app/core/backup_service.py:186) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| locale | %(locale)s |
| timezone | %(timezone)s |

代入・選択式: `locale = %(locale)s; timezone = %(timezone)s`

### `backend/src/app/apis/backup/restore_backup/sql/q901_advance_revision.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.workspace_revision | U | user_id: 所有者; revision: 全体のCAS版 |

対象条件: `WHERE user_id = %(actor_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| revision | revision + 1 |

代入・選択式: `revision = revision + 1`

### `backend/src/app/apis/backup/restore_backup/sql/q902_append_audit.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.audit_event | C | id: 不変の行識別子; actor_id: 実行者（削除時匿名化）; action: publish/withdraw/erase等; entity_type: 対象テーブルの許可リスト; entity_key_hash: 対象識別子のハッシュ; reason: 理由（個人情報を含めない）; occurred_at: 時刻 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |
| key_hash | hashlib.sha256(str(self.identity.user_id).encode()).hexdigest() (backend/src/app/core/backup_service.py:284) |
| row_id | uuid4() (backend/src/app/core/backup_service.py:284) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(row_id)s |
| actor_id | %(actor_id)s |
| action | 'backup/restore' |
| entity_type | 'workspace' |
| entity_key_hash | %(key_hash)s |
| reason | '本人が確認した全置換復元' |
| occurred_at | CURRENT_TIMESTAMP |

### `backend/src/app/apis/backup/restore_backup/sql/q903_append_outbox.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.outbox_event | C | id: 不変の行識別子; event_type: recipe_published/withdrawn/user_erased等; aggregate_id: 対象ID（配信対象でありFKでない）; payload: schema_version付き最小通知; attempt_count: 再試行数 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:80) / self.identity.user_id (backend/src/app/core/backup_service.py:186) / self.identity.user_id (backend/src/app/core/backup_service.py:175) / self.identity.user_id (backend/src/app/core/backup_service.py:260) / self.identity.user_id (backend/src/app/core/backup_service.py:274) / self.identity.user_id (backend/src/app/core/backup_service.py:283) / self.identity.user_id (backend/src/app/core/backup_service.py:284) / self.identity.user_id (backend/src/app/core/backup_service.py:291) |
| event_id | event_id (backend/src/app/core/backup_service.py:291) |
| version | revision + 1 (backend/src/app/core/backup_service.py:291) / int(revision[0]['revision']) if revision else 0 (backend/src/app/core/workspace_service.py:167) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(event_id)s |
| event_type | 'workspace.restored' |
| aggregate_id | %(actor_id)s |
| payload | JSONB_BUILD_OBJECT('schema_version', 1, 'event_id', CAST(%(event_id)s AS TEXT), 'aggregate_id', CAST(%(actor_id)s AS TEXT), 'version', CAST(%(version)s AS BIGINT)) |
| attempt_count | 0 |

### `backend/src/app/apis/workspace/get_workspace/sql/q001_revision.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.workspace_revision | R | user_id: 所有者; revision: 全体のCAS版 |

対象条件: `WHERE user_id = %(user_id)s`

行ロック: `FOR SHARE`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) |

代入・選択式: `revision`

### `backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材; name: 生皮付き・冷凍刻み等 |
| recipeweave.pantry_lot | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; form_id: 食材形態; amount: 残量; unit_id: 単位; expires_on: 表示期限; location: 冷蔵・冷凍・常温の保管場所; priority: 先に使う優先指定; status: 在庫の有効・削除・レシート取消状態; source_import_id: 登録元レシート; original_form_id: 登録時の食材形態; original_amount: 登録時数量。不明はNULL; original_unit_id: 登録時単位; updated_at: 最終編集日時; edited: 登録後の編集有無 |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |

対象条件: `WHERE p.user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) |

代入・選択式: `p.id; f.food_id; f.name AS form; p.amount; u.code AS unit; p.original_amount; p.location; p.priority; p.expires_on; p.created_at; p.updated_at; p.source_import_id; p.status; p.edited; COALESCE(ofm.food_id, f.food_id) AS original_food_id; COALESCE(ou.code, u.code) AS original_unit`

### `backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.pantry_consumption | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; session_id: 消費した調理セッション; lot_id: 消費元ロット; amount: 消費数量; unit_id: 消費数量の単位 |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |

対象条件: `WHERE c.user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) |

代入・選択式: `c.lot_id; c.amount; u.code AS unit; c.session_id`

### `backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.receipt_import | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; file_sha256: 画像本文のSHA256。本文はDBに保存しない; idempotency_key: 本人内で一意の再送防止キー; status: draft/committed/revertedの状態; reverted_at: 登録取消日時 |

対象条件: `WHERE r.user_id = %(user_id)s AND r.status IN ('committed', 'reverted')`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) |

代入・選択式: `r.id; r.file_sha256; r.idempotency_key; r.created_at; r.status; r.reverted_at`

### `backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者; revision: 楽観ロック版 |
| recipeweave.menu_item | R | id: 不変の行識別子; menu_id: 献立; recipe_version_id: 固定レシピ版; servings: その料理を作る人数; position: 表示順 |
| recipeweave.recipe_version | R | id: 不変の行識別子; recipe_id: 所属レシピ |

対象条件: `WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| menu_id | menu_id (backend/src/app/core/workspace_service.py:188) / menu_id (backend/src/app/core/workspace_service.py:206) |
| user_id | self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) |

代入・選択式: `mi.id; rv.recipe_id; mi.servings; mi.recipe_version_id; m.revision`

### `backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材; name: 生皮付き・冷凍刻み等 |
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |
| recipeweave.menu_ingredient_override | R | id: 不変の行識別子; menu_item_id: 対象料理; ingredient_line_id: 元材料行; selected: 任意材料を使うか; amount: 適量等の確定基準量 |
| recipeweave.menu_item | R | id: 不変の行識別子; menu_id: 献立; recipe_version_id: 固定レシピ版; servings: その料理を作る人数; position: 表示順 |
| recipeweave.recipe_ingredient | R | id: 不変の行識別子; recipe_version_id: 親版; line_no: 表示順; form_id: 使用形態; amount: 確定値または範囲下限; unit_id: 登録単位 |
| recipeweave.recipe_version | R | id: 不変の行識別子; base_servings: 登録分量が何人前か |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |

対象条件: `WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| menu_id | menu_id (backend/src/app/core/workspace_service.py:188) / menu_id (backend/src/app/core/workspace_service.py:206) |
| user_id | self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) |

代入・選択式: `mi.id AS menu_item_id; f.food_id; f.name AS form; ri.id AS ingredient_id; u.code AS unit; ov.id AS override_id; CASE WHEN ov.selected = FALSE THEN 0 ELSE ov.amount END AS override_amount; ri.amount * mi.servings / rv.base_servings AS scaled_amount`

### `backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.recipe_version | R | id: 不変の行識別子; recipe_id: 所属レシピ |
| recipeweave.user_recipe_event | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 利用者; recipe_version_id: 提案版; kind: 提示/調理/評価; occurred_at: 発生時刻 |

対象条件: `WHERE ranked.rank = 1 AND ranked.kind = 'liked'`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) |

代入・選択式: `ranked.recipe_id`

### `backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.kitchen_resource | R | user_id: 所有者; resource_type_id: コンロ・鍋・人等; active: 新規の調理計画で利用する資源か |
| recipeweave.resource_type | R | id: 不変の行識別子; code: burner/pan/person等; name: 道具名 |
| recipeweave.user_exclusion | R | user_id: 利用者; food_id: 食材 |
| recipeweave.user_pantry_food | R | user_id: 所有者; food_id: 常備食材 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) |

### `backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; name: 食材名・加工品種別 |
| recipeweave.food_form | R | food_id: 対応食材; base_unit_id: 計算基準単位 |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |
| recipeweave.user_food | R | user_id: 所有者; food_id: 独自食材 |

対象条件: `WHERE uf.user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) |

代入・選択式: `f.id; f.name; u.code AS unit`

### `backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |
| recipeweave.user_shopping_check | R | id: 不変の行識別子; user_id: 所有者; key: 買い物対象の安定キー; signature: 数量・商品条件の一致確認用署名; food_id: 対象食材; amount: 必要数量。不明はNULL; unit_id: 数量単位; checked_at: 購入確認日時; archived: 保管済みか |

対象条件: `WHERE c.user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) |

代入・選択式: `c.key AS client_key; c.signature; c.food_id; c.amount; u.code AS unit; c.checked_at; c.archived`

### `backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.cooking_session | R | id: 不変の行識別子; created_at: 作成日時（UTC）; menu_id: 対象献立; status: 実行状態; input_snapshot: 材料・資源・人数の固定入力; current_task_index: 調理画面の現在の工程位置（0始まり） |
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |

対象条件: `WHERE m.user_id = %(user_id)s AND s.status <> 'cancelled'`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) |

代入・選択式: `s.id; s.menu_id; s.status; s.current_task_index; s.input_snapshot`

### `backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu_item | R | id: 不変の行識別子; recipe_version_id: 固定レシピ版; position: 表示順 |
| recipeweave.recipe | R | id: 不変の行識別子; title: 代表名 |
| recipeweave.recipe_step | R | id: 不変の行識別子; step_no: 表示順（依存順とは別）; instruction: 個別補足; attention: 作業者拘束; duration_max_s: 所要秒上限; scaling_rule_id: 時間の人数変更規則; title: 工程の短い見出し |
| recipeweave.recipe_version | R | id: 不変の行識別子; recipe_id: 所属レシピ |
| recipeweave.scaling_rule | R | id: 不変の行識別子; mode: 比例・バッチ等 |
| recipeweave.session_task | R | id: 不変の行識別子; session_id: 実行; menu_item_id: 料理; step_id: 元工程; planned_start_s: 開始相対秒; planned_end_s: 終了相対秒; status: 進捗; timer_started_at: 稼働中タイマーの開始日時; timer_duration_s: 利用者が設定したタイマー秒数; duration_source: 計画時間の根拠。料理の時間規則または利用者が確認した見積り; confirmed_duration_s: 利用者が確認した工程の見積り秒数。実測値ではなく、計画後は変更しない |

対象条件: `WHERE t.session_id = %(session_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| session_id | 型付きクエリの引数。呼出元のSQL仕様を参照。 |

代入・選択式: `t.id; t.menu_item_id; t.step_id; t.planned_start_s; t.planned_end_s; t.duration_source; t.confirmed_duration_s; t.status; t.timer_started_at; t.timer_duration_s; rv.recipe_id; r.title AS recipe_name; st.title; st.instruction; st.attention; st.duration_max_s; scaling.mode AS scaling_mode`

### `backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.resource_type | R | id: 不変の行識別子; code: burner/pan/person等; name: 道具名 |
| recipeweave.session_task | R | id: 不変の行識別子; session_id: 実行; step_id: 元工程 |
| recipeweave.step_resource | R | step_id: 対象工程; resource_type_id: 要求種別 |

対象条件: `WHERE t.session_id = %(session_id)s AND r.code <> 'person'`

| SQLバインド | 実装上の値の出所 |
|---|---|
| session_id | 型付きクエリの引数。呼出元のSQL仕様を参照。 |

代入・選択式: `t.id AS task_id; r.name`

### `backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材; name: 生皮付き・冷凍刻み等 |
| recipeweave.ingredient_total | R | id: 不変の行識別子; session_id: 固定計算対象; form_id: 合算可能な形態; product_version_id: 商品固定; unit_id: 基準単位; required_amount: 必要量; actual_amount: 利用者が確定した実使用量。不明はNULL; consumption_outcome: 未要求・反映済み・在庫不足・数量不明・単位不一致の結果 |
| recipeweave.pantry_consumption | R | id: 不変の行識別子; session_id: 消費した調理セッション; lot_id: 消費元ロット; amount: 消費数量 |
| recipeweave.pantry_lot | R | id: 不変の行識別子; form_id: 食材形態; product_version_id: 商品版; unit_id: 単位 |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |

対象条件: `WHERE total.session_id = %(session_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| session_id | 型付きクエリの引数。呼出元のSQL仕様を参照。 |

代入・選択式: `total.id; fm.food_id; fm.name AS form; total.required_amount; total.actual_amount; total.consumption_outcome; u.code AS unit; COALESCE(SUM(c.amount), 0) AS consumed_amount; ARRAY_AGG(c.lot_id) FILTER(WHERE c.id IS NOT NULL) AS lot_ids`

### `backend/src/app/apis/auth/get_me/sql/q001_set_identity.sql`

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| role | identity.role (backend/src/app/core/identity.py:82) |
| user_id | str(identity.user_id) (backend/src/app/core/identity.py:82) / identity.user_id (backend/src/app/core/identity.py:83) / identity.user_id (backend/src/app/core/identity.py:86) / identity.user_id (backend/src/app/core/identity.py:89) / identity.user_id (backend/src/app/core/identity.py:96) |

代入・選択式: `SET_CONFIG('recipeweave.user_id', %(user_id)s, TRUE) AS user_setting; SET_CONFIG('recipeweave.role', %(role)s, TRUE) AS role_setting`

### `backend/src/app/apis/auth/get_me/sql/q002_initialize_user.sql`

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.app_user | C | id: 不変の行識別子; auth_subject: 認証基盤の不透明識別子; state: 利用/削除処理; locale: 表示言語; timezone: IANAタイムゾーン |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| subject | identity.subject (backend/src/app/core/identity.py:83) / identity.subject (backend/src/app/core/identity.py:86) |
| user_id | str(identity.user_id) (backend/src/app/core/identity.py:82) / identity.user_id (backend/src/app/core/identity.py:83) / identity.user_id (backend/src/app/core/identity.py:86) / identity.user_id (backend/src/app/core/identity.py:89) / identity.user_id (backend/src/app/core/identity.py:96) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(user_id)s |
| auth_subject | %(subject)s |
| state | 'active' |
| locale | 'ja' |
| timezone | 'Asia/Tokyo' |

競合時の処理: `ON CONFLICT(auth_subject) DO NOTHING`

### `backend/src/app/apis/auth/get_me/sql/q003_select_user.sql`

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.app_user | R | id: 不変の行識別子; auth_subject: 認証基盤の不透明識別子; state: 利用/削除処理 |

対象条件: `WHERE id = %(user_id)s AND auth_subject = %(subject)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| subject | identity.subject (backend/src/app/core/identity.py:83) / identity.subject (backend/src/app/core/identity.py:86) |
| user_id | str(identity.user_id) (backend/src/app/core/identity.py:82) / identity.user_id (backend/src/app/core/identity.py:83) / identity.user_id (backend/src/app/core/identity.py:86) / identity.user_id (backend/src/app/core/identity.py:89) / identity.user_id (backend/src/app/core/identity.py:96) |

代入・選択式: `id; state`

### `backend/src/app/apis/auth/get_me/sql/q004_initialize_revision.sql`

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.workspace_revision | C | id: 不変の行識別子; user_id: 所有者; revision: 全体のCAS版 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| row_id | uuid5(identity.user_id, 'workspace') (backend/src/app/core/identity.py:89) / uuid5(identity.user_id, 'kitchen:' + resource_code) (backend/src/app/core/identity.py:96) |
| user_id | str(identity.user_id) (backend/src/app/core/identity.py:82) / identity.user_id (backend/src/app/core/identity.py:83) / identity.user_id (backend/src/app/core/identity.py:86) / identity.user_id (backend/src/app/core/identity.py:89) / identity.user_id (backend/src/app/core/identity.py:96) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(row_id)s |
| user_id | %(user_id)s |
| revision | 0 |

競合時の処理: `ON CONFLICT(user_id) DO NOTHING`

### `backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql`

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.kitchen_resource | CR | id: 不変の行識別子; user_id: 所有者; resource_type_id: コンロ・鍋・人等; name: 左コンロ・26cmフライパン等; capacity: 容量; quantity: 同等資源数; active: 新規の調理計画で利用する資源か |
| recipeweave.resource_type | R | id: 不変の行識別子; code: burner/pan/person等; name: 道具名; status: 使用状態 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| resource_code | resource_code (backend/src/app/core/identity.py:96) |
| row_id | uuid5(identity.user_id, 'workspace') (backend/src/app/core/identity.py:89) / uuid5(identity.user_id, 'kitchen:' + resource_code) (backend/src/app/core/identity.py:96) |
| user_id | str(identity.user_id) (backend/src/app/core/identity.py:82) / identity.user_id (backend/src/app/core/identity.py:83) / identity.user_id (backend/src/app/core/identity.py:86) / identity.user_id (backend/src/app/core/identity.py:89) / identity.user_id (backend/src/app/core/identity.py:96) |

競合時の処理: `ON CONFLICT(id) DO NOTHING`

## 分岐・拒否条件

| 判定条件 | 例外・応答 | 定義元 |
|---|---|---|
| not rows | HTTPException(409, '本人の更新版を取得できません') | backend/src/app/core/backup_service.py:58 |
| document.owner_id != self.identity.user_id | HTTPException(403, '別の利用者のバックアップは復元できません') | backend/src/app/core/backup_service.py:70 |
| len(encoded) &gt; MAX_BACKUP_BYTES | HTTPException(413, 'バックアップの上限は5,000,000バイトです') | backend/src/app/core/backup_service.py:70 |
| not proof | HTTPException(403, 'この本人へ発行したバックアップと内容が一致しません') | backend/src/app/core/backup_service.py:78 |
| len(ids[table]) != len(rows) | HTTPException(422, '同じテーブルに重複した行IDがあります') | backend/src/app/core/backup_service.py:116 |
| target == 'app_user' | HTTPException(403, '本人以外のアカウントを参照できません') | backend/src/app/core/backup_service.py:116 |
| actual_hash != session['input_hash'] | HTTPException(409, '保存された調理入力とハッシュが一致しません') | backend/src/app/core/backup_service.py:116 |
| snapshot.menu_revision != session['menu_revision'] | HTTPException(409, '調理入力の献立版が保存した版と一致しません') | backend/src/app/core/backup_service.py:116 |
| {row['id'] for row in actual} != values | HTTPException(409, '必要な共有カタログがないか、参照先を利用できません') | backend/src/app/core/backup_service.py:116 |
| value != self.identity.user_id | HTTPException(403, '本人以外のアカウントを参照できません') | backend/src/app/core/backup_service.py:116 |
| column in row and row[column] != self.identity.user_id | HTTPException(403, '本人の業務行・私有食材だけを復元できます') | backend/src/app/core/backup_service.py:116 |
| target in OWNED | HTTPException(422, 'バックアップ内の本人データの参照が不足しています') | backend/src/app/core/backup_service.py:116 |
| request.expected_version != revision | HTTPException(409, '確認後に更新されています。内容をもう一度確認してください') | backend/src/app/core/backup_service.py:249 |
| not intent | HTTPException(409, '確認が期限切れ・使用済みです。もう一度内容を確認してください') | backend/src/app/core/backup_service.py:249 |
| not consumed | HTTPException(409, '確認が有効でなくなったため復元を取り消しました') | backend/src/app/core/backup_service.py:249 |

## 出力

| 関数 | 返却式 | 定義元 |
|---|---|---|
| handle | execute(BackupService(database, identity), request) | backend/src/app/apis/backup/restore_backup/router.py:22 |
| execute | service.restore_backup(request) | backend/src/app/apis/backup/restore_backup/functions.py:6 |
| canonical_backup | json.dumps(document.model_dump(mode='json', by_alias=True), ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8') | backend/src/app/core/backup_service.py:37 |
| BackupService.queries | OperationQueries(self.connection, 'backup/' + operation) | backend/src/app/core/backup_service.py:55 |
| BackupService.current_revision | int(rows[0]['revision']) | backend/src/app/core/backup_service.py:58 |
| BackupService.checked_digest | hashlib.sha256(encoded).hexdigest() | backend/src/app/core/backup_service.py:70 |
| BackupService.check_proof | digest | backend/src/app/core/backup_service.py:78 |
| BackupService.check_references | data | backend/src/app/core/backup_service.py:116 |
| BackupService.check_references | 本文なし | backend/src/app/core/backup_service.py:116 |
| BackupService.check_references | 本文なし | backend/src/app/core/backup_service.py:116 |
| BackupService.restore_backup | result | backend/src/app/core/backup_service.py:249 |
| quantity | {'value': None if value is None else float(value), 'unit': unit} | backend/src/app/core/workspace_service.py:41 |
| iso | value.isoformat() if isinstance(value, date &#124; datetime) else None | backend/src/app/core/workspace_service.py:46 |
| WorkspaceService.queries | OperationQueries(self.connection, 'workspace/' + name) | backend/src/app/core/workspace_service.py:60 |
| WorkspaceService.get_workspace | AppSnapshot.model_validate({'schemaVersion': 1, 'version': int(revision[0]['revision']) if revision else 0, 'lots': lots, 'imports': imports, 'drafts': {}, 'meal': meal, 'saved': [str(r['recipe_id']) for r in q.run('q007_saved', user_id=self.user_id)], 'shoppingChecks': checks, 'cooking': cooking, 'settings': settings, 'customFoods': customs, 'search': {'selectedFoodIds': [], 'match': 'all', 'maxMinutes': None, 'noShopping': False, 'equipment': []}}) | backend/src/app/core/workspace_service.py:81 |
| WorkspaceService.read_meal | [{'id': str(r['id']), 'recipeId': str(r['recipe_id']), 'recipeVersionId': str(r['recipe_version_id']), 'servings': float(r['servings']), 'adjusted': any((a['override_id'] is not None for a in amounts if a['menu_item_id'] == r['id'])), 'amounts': {str(a['ingredient_id']): quantity(a['override_amount'] if a['override_id'] else a['scaled_amount'], a['unit']) for a in amounts if a['menu_item_id'] == r['id']}} for r in q.run('q005_menu', menu_id=menu_id, user_id=self.user_id)] | backend/src/app/core/workspace_service.py:187 |

APIとして返す型・status・headerは [インターフェース](interface.md) の実OpenAPIを参照。

## 責務

| 関数 | 処理 | 定義元 |
|---|---|---|
| handle | 確認したバックアップで本人のデータを全置換する。利用者の確認がない全置換を受け付けない。 | backend/src/app/apis/backup/restore_backup/router.py:22 |
| execute | 確認したバックアップで本人のデータを全置換する。認証済み本人と固定SQLを使う。 | backend/src/app/apis/backup/restore_backup/functions.py:6 |
| canonical_backup | 日時・UUID・十進数の正規表現を型で確定し、JSON項目の記述順と空白に依存しない本文へする。 | backend/src/app/core/backup_service.py:37 |
| BackupService.queries | 個別説明なし | backend/src/app/core/backup_service.py:55 |
| BackupService.current_revision | 個別説明なし | backend/src/app/core/backup_service.py:58 |
| BackupService.checked_digest | 個別説明なし | backend/src/app/core/backup_service.py:70 |
| BackupService.check_proof | 個別説明なし | backend/src/app/core/backup_service.py:78 |
| BackupService.check_references | 他人の行、欠落した本人行、消失した共有参照を、削除前にまとめて検査する。 | backend/src/app/core/backup_service.py:116 |
| BackupService.replace_rows | 依存の子から削除し、元IDと全列で親から挿入して全遅延制約を検証する。 | backend/src/app/core/backup_service.py:171 |
| BackupService.restore_backup | 同じ本人・本文・確認・現行版を再検証し、全置換と単回消費を一括確定する。 | backend/src/app/core/backup_service.py:249 |
| quantity | 未知の数量をNULLのまま通信し、DBの十進値を表示用の数へ変換する。 | backend/src/app/core/workspace_service.py:41 |
| iso | 日時はISO形式にそろえる。 | backend/src/app/core/workspace_service.py:46 |
| WorkspaceService.queries | 個別説明なし | backend/src/app/core/workspace_service.py:60 |
| WorkspaceService.get_workspace | 在庫・献立・設定・履歴を各テーブルから集約し、一貫した版を返す。 | backend/src/app/core/workspace_service.py:81 |
| WorkspaceService.read_meal | 個別説明なし | backend/src/app/core/workspace_service.py:187 |

[SQL](queries.md) / [シーケンス](sequence.md) / [ログ](messages.md) / [要因別テスト](tests.md)
