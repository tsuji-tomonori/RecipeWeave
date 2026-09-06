# 詳細設計: export_backup

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/backups/export` — バックアップを書き出す

## 入力と処理前提

| 項目 | 仕様 |
|---|---|
| authentication | 検証済みBearerトークンと本人所有権 |
| idempotency | 呼出しごとに新しい発行記録を作成し、本文は保存しない |
| transaction | 本人の現在版をロックし、一つのSQLで全業務表を一貫して読み、発行根拠を同時に記録する |
| effects | 本人のバックアップ発行記録を追加する |

| 入力場所 | 名前 | 型 | 必須 |
|---|---|---|---|

## データベースの対象と値の流れ

### `backend/src/app/apis/backup/export_backup/sql/q001_lock_revision.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.workspace_revision | R | user_id: 所有者; revision: 全体のCAS版 |

対象条件: `WHERE user_id = %(actor_id)s`

行ロック: `FOR UPDATE`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:65) / self.identity.user_id (backend/src/app/core/backup_service.py:95) / self.identity.user_id (backend/src/app/core/backup_service.py:107) |

代入・選択式: `revision`

### `backend/src/app/apis/backup/export_backup/sql/q002_profile.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.app_user | R | id: 不変の行識別子; locale: 表示言語; timezone: IANAタイムゾーン |

対象条件: `WHERE id = %(actor_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:65) / self.identity.user_id (backend/src/app/core/backup_service.py:95) / self.identity.user_id (backend/src/app/core/backup_service.py:107) |

代入・選択式: `locale; timezone`

### `backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql`

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
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:65) / self.identity.user_id (backend/src/app/core/backup_service.py:95) / self.identity.user_id (backend/src/app/core/backup_service.py:107) |

代入・選択式: `(SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'option_id', t.option_id, 'weight', CAST(t.weight AS TEXT)) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.user_preference AS t WHERE (t.user_id = %(actor_id)s)) AS rows_user_preference; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'food_id', t.food_id, 'allergen_id', t.allergen_id, 'strict', t.strict) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.user_exclusion AS t WHERE (t.user_id = %(actor_id)s)) AS rows_user_exclusion; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'recipe_version_id', t.recipe_version_id, 'kind', t.kind, 'occurred_at', t.occurred_at, 'request_key', t.request_key) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.user_recipe_event AS t WHERE (t.user_id = %(actor_id)s)) AS rows_user_recipe_event; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'name', t.name, 'servings', CAST(t.servings AS TEXT), 'revision', t.revision) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.menu AS t WHERE (t.user_id = %(actor_id)s)) AS rows_menu; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'menu_id', t.menu_id, 'recipe_version_id', t.recipe_version_id, 'servings', CAST(t.servings AS TEXT), 'role_option_id', t.role_option_id, 'position', t.position) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.menu_item AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.menu AS owner_0 WHERE owner_0.id = t.menu_id AND owner_0.user_id = %(actor_id)s))) AS rows_menu_item; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'menu_item_id', t.menu_item_id, 'ingredient_line_id', t.ingredient_line_id, 'selected', t.selected, 'amount', CAST(t.amount AS TEXT), 'form_id', t.form_id, 'product_version_id', t.product_version_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.menu_ingredient_override AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.menu_item AS owner_0 WHERE owner_0.id = t.menu_item_id AND EXISTS(SELECT owner_1.id FROM recipeweave.menu AS owner_1 WHERE owner_1.id = owner_0.menu_id AND owner_1.user_id = %(actor_id)s)))) AS rows_menu_ingredient_override; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'resource_type_id', t.resource_type_id, 'name', t.name, 'capacity', CAST(t.capacity AS TEXT), 'quantity', t.quantity, 'active', t.active) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.kitchen_resource AS t WHERE (t.user_id = %(actor_id)s)) AS rows_kitchen_resource; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'menu_id', t.menu_id, 'menu_revision', t.menu_revision, 'status', t.status, 'target_at', t.target_at, 'planner_version', t.planner_version, 'input_snapshot', t.input_snapshot, 'input_hash', t.input_hash, 'current_task_index', t.current_task_index) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.cooking_session AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.menu AS owner_0 WHERE owner_0.id = t.menu_id AND owner_0.user_id = %(actor_id)s))) AS rows_cooking_session; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'session_id', t.session_id, 'menu_item_id', t.menu_item_id, 'step_id', t.step_id, 'batch_no', t.batch_no, 'planned_start_s', t.planned_start_s, 'planned_end_s', t.planned_end_s, 'status', t.status, 'actual_start_at', t.actual_start_at, 'actual_end_at', t.actual_end_at, 'timer_started_at', t.timer_started_at, 'timer_duration_s', t.timer_duration_s, 'duration_source', t.duration_source, 'confirmed_duration_s', t.confirmed_duration_s) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.session_task AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.cooking_session AS owner_0 WHERE owner_0.id = t.session_id AND EXISTS(SELECT owner_1.id FROM recipeweave.menu AS owner_1 WHERE owner_1.id = owner_0.menu_id AND owner_1.user_id = %(actor_id)s)))) AS rows_session_task; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'before_task_id', t.before_task_id, 'after_task_id', t.after_task_id, 'min_lag_s', t.min_lag_s, 'max_lag_s', t.max_lag_s, 'reason', t.reason) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.task_dependency AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.session_task AS owner_0 WHERE owner_0.id = t.before_task_id AND EXISTS(SELECT owner_1.id FROM recipeweave.cooking_session AS owner_1 WHERE owner_1.id = owner_0.session_id AND EXISTS(SELECT owner_2.id FROM recipeweave.menu AS owner_2 WHERE owner_2.id = owner_1.menu_id AND owner_2.user_id = %(actor_id)s))))) AS rows_task_dependency; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'task_id', t.task_id, 'resource_id', t.resource_id, 'start_s', t.start_s, 'end_s', t.end_s, 'quantity', t.quantity) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.resource_reservation AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.session_task AS owner_0 WHERE owner_0.id = t.task_id AND EXISTS(SELECT owner_1.id FROM recipeweave.cooking_session AS owner_1 WHERE owner_1.id = owner_0.session_id AND EXISTS(SELECT owner_2.id FROM recipeweave.menu AS owner_2 WHERE owner_2.id = owner_1.menu_id AND owner_2.user_id = %(actor_id)s))))) AS rows_resource_reservation; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'session_id', t.session_id, 'form_id', t.form_id, 'product_version_id', t.product_version_id, 'unit_id', t.unit_id, 'required_amount', CAST(t.required_amount AS TEXT), 'quality', t.quality, 'calculation_version', t.calculation_version, 'actual_amount', CAST(t.actual_amount AS TEXT), 'consumption_outcome', t.consumption_outcome) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.ingredient_total AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.cooking_session AS owner_0 WHERE owner_0.id = t.session_id AND EXISTS(SELECT owner_1.id FROM recipeweave.menu AS owner_1 WHERE owner_1.id = owner_0.menu_id AND owner_1.user_id = %(actor_id)s)))) AS rows_ingredient_total; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'form_id', t.form_id, 'product_version_id', t.product_version_id, 'amount', CAST(t.amount AS TEXT), 'unit_id', t.unit_id, 'expires_on', t.expires_on, 'opened_at', t.opened_at, 'location', t.location, 'priority', t.priority, 'status', t.status, 'source_import_id', t.source_import_id, 'quantity_quality', t.quantity_quality, 'original_form_id', t.original_form_id, 'original_amount', CAST(t.original_amount AS TEXT), 'original_unit_id', t.original_unit_id, 'updated_at', t.updated_at, 'edited', t.edited) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.pantry_lot AS t WHERE (t.user_id = %(actor_id)s)) AS rows_pantry_lot; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'session_id', t.session_id, 'total_id', t.total_id, 'product_version_id', t.product_version_id, 'net_shortage', CAST(t.net_shortage AS TEXT), 'package_count', t.package_count, 'surplus_amount', CAST(t.surplus_amount AS TEXT), 'checked', t.checked, 'client_key', t.client_key, 'checked_at', t.checked_at, 'archived', t.archived) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.shopping_item AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.cooking_session AS owner_0 WHERE owner_0.id = t.session_id AND EXISTS(SELECT owner_1.id FROM recipeweave.menu AS owner_1 WHERE owner_1.id = owner_0.menu_id AND owner_1.user_id = %(actor_id)s)))) AS rows_shopping_item; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'file_sha256', t.file_sha256, 'idempotency_key', t.idempotency_key, 'status', t.status, 'revision', CAST(t.revision AS TEXT), 'committed_at', t.committed_at, 'reverted_at', t.reverted_at, 'undo_preserved_count', t.undo_preserved_count) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.receipt_import AS t WHERE (t.user_id = %(actor_id)s)) AS rows_receipt_import; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'import_id', t.import_id, 'line_no', t.line_no, 'raw_name', t.raw_name, 'form_id', t.form_id, 'product_version_id', t.product_version_id, 'amount', CAST(t.amount AS TEXT), 'unit_id', t.unit_id, 'decision', t.decision, 'pantry_lot_id', t.pantry_lot_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.receipt_line AS t WHERE (EXISTS(SELECT owner_0.id FROM recipeweave.receipt_import AS owner_0 WHERE owner_0.id = t.import_id AND owner_0.user_id = %(actor_id)s))) AS rows_receipt_line; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'food_id', t.food_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.user_food AS t WHERE (t.user_id = %(actor_id)s)) AS rows_user_food; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'food_id', t.food_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.user_pantry_food AS t WHERE (t.user_id = %(actor_id)s)) AS rows_user_pantry_food; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'session_id', t.session_id, 'lot_id', t.lot_id, 'amount', CAST(t.amount AS TEXT), 'unit_id', t.unit_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.pantry_consumption AS t WHERE (t.user_id = %(actor_id)s)) AS rows_pantry_consumption; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'user_id', t.user_id, 'key', t.key, 'signature', t.signature, 'food_id', t.food_id, 'amount', CAST(t.amount AS TEXT), 'unit_id', t.unit_id, 'checked_at', t.checked_at, 'archived', t.archived) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.user_shopping_check AS t WHERE (t.user_id = %(actor_id)s)) AS rows_user_shopping_check; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'version', t.version, 'manifest_hash', t.manifest_hash, 'published_at', t.published_at, 'owner_id', t.owner_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.catalog_release AS t WHERE (t.owner_id = %(actor_id)s)) AS rows_catalog_release; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'code', t.code, 'name', t.name, 'kind', t.kind, 'parent_id', t.parent_id, 'release_id', t.release_id, 'status', t.status, 'owner_id', t.owner_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.food AS t WHERE (t.owner_id = %(actor_id)s)) AS rows_food; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'food_id', t.food_id, 'alias', t.alias, 'locale', t.locale) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.food_alias AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s))) AS rows_food_alias; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'food_id', t.food_id, 'name', t.name, 'state', t.state, 'base_unit_id', t.base_unit_id, 'quantity_basis', t.quantity_basis, 'status', t.status) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.food_form AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s))) AS rows_food_form; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'food_id', t.food_id, 'option_id', t.option_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.food_axis_option AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s))) AS rows_food_axis_option; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'food_id', t.food_id, 'brand', t.brand, 'name', t.name, 'gtin', t.gtin, 'status', t.status) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.product AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s))) AS rows_product; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'form_id', t.form_id, 'from_unit_id', t.from_unit_id, 'to_unit_id', t.to_unit_id, 'factor', CAST(t.factor AS TEXT), 'quality', t.quality, 'source_id', t.source_id, 'conditions', t.conditions, 'release_id', t.release_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.conversion AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s))) AS rows_conversion; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'form_id', t.form_id, 'allergen_id', t.allergen_id, 'presence', t.presence, 'source_id', t.source_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.food_allergen AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s))) AS rows_food_allergen; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'product_id', t.product_id, 'version', t.version, 'form_id', t.form_id, 'net_amount', CAST(t.net_amount AS TEXT), 'unit_id', t.unit_id, 'drain_amount', CAST(t.drain_amount AS TEXT), 'source_id', t.source_id, 'preparation_note', t.preparation_note, 'valid_from', t.valid_from) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.product_version AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id WHERE product.id = t.product_id AND food.owner_id = %(actor_id)s))) AS rows_product_version; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'product_version_id', t.product_version_id, 'form_id', t.form_id, 'name', t.name, 'amount', CAST(t.amount AS TEXT), 'unit_id', t.unit_id, 'quality', t.quality) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.product_component AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s))) AS rows_product_component; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'product_version_id', t.product_version_id, 'allergen_id', t.allergen_id, 'presence', t.presence, 'source_id', t.source_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.product_allergen AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s))) AS rows_product_allergen; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'product_version_id', t.product_version_id, 'operation_id', t.operation_id, 'allowed', t.allowed, 'use_original_container', t.use_original_container, 'parameter_contract', t.parameter_contract, 'source_id', t.source_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.product_preparation_rule AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s))) AS rows_product_preparation_rule; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'form_id', t.form_id, 'product_version_id', t.product_version_id, 'nutrient_id', t.nutrient_id, 'amount', CAST(t.amount AS TEXT), 'basis_amount', CAST(t.basis_amount AS TEXT), 'basis_unit_id', t.basis_unit_id, 'source_id', t.source_id) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.nutrition_fact AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s) OR EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.product AS product ON food.id = product.food_id INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s))) AS rows_nutrition_fact; (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', t.id, 'created_at', t.created_at, 'input_form_id', t.input_form_id, 'output_form_id', t.output_form_id, 'yield_ratio', CAST(t.yield_ratio AS TEXT), 'source_id', t.source_id, 'quality', t.quality, 'conditions', t.conditions) ORDER BY t.id), CAST('[]' AS JSONB)) FROM recipeweave.form_yield AS t WHERE (EXISTS(SELECT 1 FROM recipeweave.food AS food INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id WHERE form.id = t.input_form_id AND food.owner_id = %(actor_id)s))) AS rows_form_yield`

### `backend/src/app/apis/backup/export_backup/sql/q021_issue_artifact.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.backup_artifact | C | id: バックアップ本文に含める不変の発行識別子; user_id: 発行先の本人。利用者消去後だけNULLへ匿名化する; body_sha256: 発行識別子を含む正規化済み本文全体のSHA-256; format_version: 対応するバックアップの形式版。現在は2 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/backup_service.py:59) / self.identity.user_id (backend/src/app/core/backup_service.py:65) / self.identity.user_id (backend/src/app/core/backup_service.py:95) / self.identity.user_id (backend/src/app/core/backup_service.py:107) |
| artifact_id | document.artifact_id (backend/src/app/core/backup_service.py:107) |
| body_sha256 | digest (backend/src/app/core/backup_service.py:107) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(artifact_id)s |
| user_id | %(actor_id)s |
| body_sha256 | %(body_sha256)s |
| format_version | 2 |

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

## 出力

| 関数 | 返却式 | 定義元 |
|---|---|---|
| handle | execute(BackupService(database, identity)) | backend/src/app/apis/backup/export_backup/router.py:22 |
| execute | service.export_backup() | backend/src/app/apis/backup/export_backup/functions.py:5 |
| canonical_backup | json.dumps(document.model_dump(mode='json', by_alias=True), ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8') | backend/src/app/core/backup_service.py:37 |
| BackupService.queries | OperationQueries(self.connection, 'backup/' + operation) | backend/src/app/core/backup_service.py:55 |
| BackupService.current_revision | int(rows[0]['revision']) | backend/src/app/core/backup_service.py:58 |
| BackupService.export_tables | BackupTables.model_validate({key.removeprefix('rows_'): value for key, value in rows[0].items()}) | backend/src/app/core/backup_service.py:64 |
| BackupService.checked_digest | hashlib.sha256(encoded).hexdigest() | backend/src/app/core/backup_service.py:70 |
| BackupService.export_backup | document | backend/src/app/core/backup_service.py:90 |

APIとして返す型・status・headerは [インターフェース](interface.md) の実OpenAPIを参照。

## 責務

| 関数 | 処理 | 定義元 |
|---|---|---|
| handle | 本人の現在データを書き出し、発行した本文の根拠だけを記録する。 | backend/src/app/apis/backup/export_backup/router.py:22 |
| execute | バックアップを書き出す。認証済み本人と固定SQLを使う。 | backend/src/app/apis/backup/export_backup/functions.py:5 |
| canonical_backup | 日時・UUID・十進数の正規表現を型で確定し、JSON項目の記述順と空白に依存しない本文へする。 | backend/src/app/core/backup_service.py:37 |
| BackupService.queries | 個別説明なし | backend/src/app/core/backup_service.py:55 |
| BackupService.current_revision | 個別説明なし | backend/src/app/core/backup_service.py:58 |
| BackupService.export_tables | 個別説明なし | backend/src/app/core/backup_service.py:64 |
| BackupService.checked_digest | 個別説明なし | backend/src/app/core/backup_service.py:70 |
| BackupService.export_backup | 一貫した全行と表示設定を取得し、本文を保存せず発行根拠だけを記録する。 | backend/src/app/core/backup_service.py:90 |

[SQL](queries.md) / [シーケンス](sequence.md) / [ログ](messages.md) / [要因別テスト](tests.md)
