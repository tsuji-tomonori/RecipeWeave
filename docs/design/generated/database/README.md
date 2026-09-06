# 物理テーブル一覧

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

全マイグレーションの実DDLと移行台帳のCREATE文で作られる表を掲載する。原設計との対応は [原設計との対応](SOURCE-MAPPING.md)、トリガー・RLS等は [DB制約と手続き](CONTRACTS.md) から確認できる。

| テーブル | 意味 | 列数 | 定義元 |
|---|---|---|---|
| [recipeweave.allergen](tables/recipeweave.allergen.md) | アレルゲン概念 | 5 | database/migrations/002_relational_schema.sql:statement-111 |
| [recipeweave.app_user](tables/recipeweave.app_user.md) | アプリ利用者 | 6 | database/migrations/002_relational_schema.sql:statement-439 |
| [recipeweave.audit_event](tables/recipeweave.audit_event.md) | 変更・公開監査 | 8 | database/migrations/002_relational_schema.sql:statement-582 |
| [recipeweave.axis](tables/recipeweave.axis.md) | 組み合わせ軸 | 8 | database/migrations/002_relational_schema.sql:statement-152 |
| [recipeweave.axis_option](tables/recipeweave.axis_option.md) | 軸候補値 | 8 | database/migrations/002_relational_schema.sql:statement-162 |
| [recipeweave.candidate_attempt](tables/recipeweave.candidate_attempt.md) | 試行済み設計点の台帳 | 10 | database/migrations/002_relational_schema.sql:statement-648 |
| [recipeweave.catalog_release](tables/recipeweave.catalog_release.md) | カタログ公開版 | 6 | database/migrations/002_relational_schema.sql:statement-13 |
| [recipeweave.compatibility_rule](tables/recipeweave.compatibility_rule.md) | 組み合わせ・公開ルール | 9 | database/migrations/002_relational_schema.sql:statement-400 |
| [recipeweave.conversion](tables/recipeweave.conversion.md) | 食材形態別換算 | 10 | database/migrations/002_relational_schema.sql:statement-57 |
| [recipeweave.cooking_session](tables/recipeweave.cooking_session.md) | 調理計画実行 | 10 | database/migrations/002_relational_schema.sql:statement-507 |
| [recipeweave.food](tables/recipeweave.food.md) | 購入・利用食材概念 | 9 | database/migrations/002_relational_schema.sql:statement-30 |
| [recipeweave.food_alias](tables/recipeweave.food_alias.md) | 食材別名 | 5 | database/migrations/002_relational_schema.sql:statement-40 |
| [recipeweave.food_allergen](tables/recipeweave.food_allergen.md) | 食材アレルゲン知識 | 6 | database/migrations/002_relational_schema.sql:statement-118 |
| [recipeweave.food_axis_option](tables/recipeweave.food_axis_option.md) | 食材の分類属性 | 4 | database/migrations/002_relational_schema.sql:statement-172 |
| [recipeweave.food_form](tables/recipeweave.food_form.md) | 食材形態 | 8 | database/migrations/002_relational_schema.sql:statement-47 |
| [recipeweave.food_identity](tables/recipeweave.food_identity.md) | 料理同一性上の食品 | 5 | database/migrations/002_relational_schema.sql:statement-611 |
| [recipeweave.food_identity_member](tables/recipeweave.food_identity_member.md) | 購買食品から同一性への対応 | 6 | database/migrations/002_relational_schema.sql:statement-618 |
| [recipeweave.form_yield](tables/recipeweave.form_yield.md) | 処理歩留まり | 8 | database/migrations/002_relational_schema.sql:statement-69 |
| [recipeweave.generation_choice](tables/recipeweave.generation_choice.md) | 生成軸の選択値 | 4 | database/migrations/002_relational_schema.sql:statement-377 |
| [recipeweave.generation_food](tables/recipeweave.generation_food.md) | 生成の食材入力 | 5 | database/migrations/002_relational_schema.sql:statement-383 |
| [recipeweave.generation_job](tables/recipeweave.generation_job.md) | 事前生成ジョブ | 10 | database/migrations/002_relational_schema.sql:statement-365 |
| [recipeweave.generation_policy](tables/recipeweave.generation_policy.md) | AI生成方針版 | 8 | database/migrations/002_relational_schema.sql:statement-355 |
| [recipeweave.generation_result](tables/recipeweave.generation_result.md) | 生成結果の出自 | 8 | database/migrations/002_relational_schema.sql:statement-390 |
| [recipeweave.generation_shard](tables/recipeweave.generation_shard.md) | 列挙範囲・リース管理 | 10 | database/migrations/002_relational_schema.sql:statement-636 |
| [recipeweave.generation_stratum_metric](tables/recipeweave.generation_stratum_metric.md) | 採用率・飽和度の実測 | 14 | database/migrations/002_relational_schema.sql:statement-683 |
| [recipeweave.generation_template](tables/recipeweave.generation_template.md) | 列挙テンプレート版 | 8 | database/migrations/002_relational_schema.sql:statement-626 |
| [recipeweave.ingredient_total](tables/recipeweave.ingredient_total.md) | 献立材料集計結果 | 11 | database/migrations/002_relational_schema.sql:statement-549 |
| [recipeweave.kitchen_resource](tables/recipeweave.kitchen_resource.md) | キッチンの実資源 | 8 | database/migrations/002_relational_schema.sql:statement-498 |
| [recipeweave.material_node](tables/recipeweave.material_node.md) | 材料・中間物ノード | 9 | database/migrations/002_relational_schema.sql:statement-290 |
| [recipeweave.media_asset](tables/recipeweave.media_asset.md) | 教育用動画等の版 | 11 | database/migrations/002_relational_schema.sql:statement-334 |
| [recipeweave.menu](tables/recipeweave.menu.md) | 献立 | 6 | database/migrations/002_relational_schema.sql:statement-471 |
| [recipeweave.menu_ingredient_override](tables/recipeweave.menu_ingredient_override.md) | 献立別材料確定 | 8 | database/migrations/002_relational_schema.sql:statement-488 |
| [recipeweave.menu_item](tables/recipeweave.menu_item.md) | 献立の料理 | 7 | database/migrations/002_relational_schema.sql:statement-479 |
| [recipeweave.nutrient](tables/recipeweave.nutrient.md) | 栄養成分種別 | 5 | database/migrations/002_relational_schema.sql:statement-134 |
| [recipeweave.nutrition_fact](tables/recipeweave.nutrition_fact.md) | 形態・商品別栄養値 | 9 | database/migrations/002_relational_schema.sql:statement-141 |
| [recipeweave.operation](tables/recipeweave.operation.md) | 標準調理動作 | 8 | database/migrations/002_relational_schema.sql:statement-245 |
| [recipeweave.operation_parameter](tables/recipeweave.operation_parameter.md) | 動作パラメータ定義 | 11 | database/migrations/002_relational_schema.sql:statement-255 |
| [recipeweave.outbox_event](tables/recipeweave.outbox_event.md) | 検索・キャッシュ更新配信 | 7 | database/migrations/002_relational_schema.sql:statement-592 |
| [recipeweave.pantry_consumption](tables/recipeweave.pantry_consumption.md) | 調理による在庫消費の冪等台帳 | 7 | database/migrations/003_service_operations.sql:statement-43 |
| [recipeweave.pantry_lot](tables/recipeweave.pantry_lot.md) | 手持ち食材ロット | 19 | database/migrations/002_relational_schema.sql:statement-560 |
| [recipeweave.product](tables/recipeweave.product.md) | 市販商品識別 | 7 | database/migrations/002_relational_schema.sql:statement-79 |
| [recipeweave.product_allergen](tables/recipeweave.product_allergen.md) | 商品表示アレルゲン | 6 | database/migrations/002_relational_schema.sql:statement-126 |
| [recipeweave.product_component](tables/recipeweave.product_component.md) | セット内構成品 | 8 | database/migrations/002_relational_schema.sql:statement-101 |
| [recipeweave.product_preparation_rule](tables/recipeweave.product_preparation_rule.md) | 商品固有の調理条件 | 8 | database/migrations/002_relational_schema.sql:statement-601 |
| [recipeweave.product_version](tables/recipeweave.product_version.md) | 商品仕様版 | 11 | database/migrations/002_relational_schema.sql:statement-88 |
| [recipeweave.receipt_import](tables/recipeweave.receipt_import.md) | レシート読取・在庫登録の処理単位 | 10 | database/migrations/003_service_operations.sql:statement-1 |
| [recipeweave.receipt_line](tables/recipeweave.receipt_line.md) | レシートの商品候補と確定した在庫の対応 | 11 | database/migrations/003_service_operations.sql:statement-12 |
| [recipeweave.recipe](tables/recipeweave.recipe.md) | レシピ同一性 | 6 | database/migrations/002_relational_schema.sql:statement-178 |
| [recipeweave.recipe_embedding](tables/recipeweave.recipe_embedding.md) | 近似検索用特徴量 | 7 | database/migrations/002_relational_schema.sql:statement-674 |
| [recipeweave.recipe_ingredient](tables/recipeweave.recipe_ingredient.md) | レシピ材料明細 | 19 | database/migrations/002_relational_schema.sql:statement-225 |
| [recipeweave.recipe_option](tables/recipeweave.recipe_option.md) | 版の分類・特徴 | 4 | database/migrations/002_relational_schema.sql:statement-200 |
| [recipeweave.recipe_search_document](tables/recipeweave.recipe_search_document.md) | 公開検索用文書 | 12 | database/migrations/002_relational_schema.sql:statement-660 |
| [recipeweave.recipe_signature](tables/recipeweave.recipe_signature.md) | 内容重複判定署名 | 7 | database/migrations/002_relational_schema.sql:statement-421 |
| [recipeweave.recipe_similarity](tables/recipeweave.recipe_similarity.md) | 近似レシピ関係 | 7 | database/migrations/002_relational_schema.sql:statement-430 |
| [recipeweave.recipe_step](tables/recipeweave.recipe_step.md) | 調理工程ノード | 12 | database/migrations/002_relational_schema.sql:statement-268 |
| [recipeweave.recipe_version](tables/recipeweave.recipe_version.md) | レシピ内容版 | 13 | database/migrations/002_relational_schema.sql:statement-186 |
| [recipeweave.resource_reservation](tables/recipeweave.resource_reservation.md) | 資源の予約 | 7 | database/migrations/002_relational_schema.sql:statement-540 |
| [recipeweave.resource_type](tables/recipeweave.resource_type.md) | 道具・設備・作業者種別 | 6 | database/migrations/002_relational_schema.sql:statement-317 |
| [recipeweave.scaling_point](tables/recipeweave.scaling_point.md) | 検証済み換算点 | 5 | database/migrations/002_relational_schema.sql:statement-218 |
| [recipeweave.scaling_rule](tables/recipeweave.scaling_rule.md) | 人数変更規則 | 10 | database/migrations/002_relational_schema.sql:statement-206 |
| [recipeweave.schema_migrations](tables/recipeweave.schema_migrations.md) | 移行IDとchecksum、完了時刻を保持する運用台帳。DDLの構造確認が成功した後に記録し、アプリAPIから更新しない。 | 3 | database/migrate.py:121 |
| [recipeweave.session_task](tables/recipeweave.session_task.md) | 展開済み工程 | 13 | database/migrations/002_relational_schema.sql:statement-518 |
| [recipeweave.shopping_item](tables/recipeweave.shopping_item.md) | 買い物行 | 12 | database/migrations/002_relational_schema.sql:statement-571 |
| [recipeweave.source_record](tables/recipeweave.source_record.md) | 根拠資料 | 8 | database/migrations/002_relational_schema.sql:statement-3 |
| [recipeweave.step_dependency](tables/recipeweave.step_dependency.md) | 工程依存辺 | 7 | database/migrations/002_relational_schema.sql:statement-308 |
| [recipeweave.step_input](tables/recipeweave.step_input.md) | 工程への材料受渡し | 5 | database/migrations/002_relational_schema.sql:statement-301 |
| [recipeweave.step_media](tables/recipeweave.step_media.md) | 工程別メディア選択 | 6 | database/migrations/002_relational_schema.sql:statement-347 |
| [recipeweave.step_parameter](tables/recipeweave.step_parameter.md) | 工程の型付きパラメータ | 7 | database/migrations/002_relational_schema.sql:statement-281 |
| [recipeweave.step_resource](tables/recipeweave.step_resource.md) | 工程の資源要求 | 7 | database/migrations/002_relational_schema.sql:statement-325 |
| [recipeweave.task_dependency](tables/recipeweave.task_dependency.md) | 献立展開後依存 | 7 | database/migrations/002_relational_schema.sql:statement-531 |
| [recipeweave.unit](tables/recipeweave.unit.md) | 単位 | 8 | database/migrations/002_relational_schema.sql:statement-20 |
| [recipeweave.user_exclusion](tables/recipeweave.user_exclusion.md) | 避けたい食材・物質 | 6 | database/migrations/002_relational_schema.sql:statement-454 |
| [recipeweave.user_food](tables/recipeweave.user_food.md) | 利用者が追加した独自食材の所有 | 4 | database/migrations/003_service_operations.sql:statement-31 |
| [recipeweave.user_pantry_food](tables/recipeweave.user_pantry_food.md) | 利用者が常備すると設定した食材 | 4 | database/migrations/003_service_operations.sql:statement-37 |
| [recipeweave.user_preference](tables/recipeweave.user_preference.md) | ユーザーの嗜好 | 5 | database/migrations/002_relational_schema.sql:statement-447 |
| [recipeweave.user_recipe_event](tables/recipeweave.user_recipe_event.md) | 提案・調理履歴 | 7 | database/migrations/002_relational_schema.sql:statement-462 |
| [recipeweave.user_shopping_check](tables/recipeweave.user_shopping_check.md) | 調理前の買い物確認 | 10 | database/migrations/003_service_operations.sql:statement-152 |
| [recipeweave.user_state](tables/recipeweave.user_state.md) | 旧Devスナップショット。移行履歴専用でサービスのデータ正本には使用しない | 4 | database/migrations/001_user_state.sql:statement-1 |
| [recipeweave.validation_result](tables/recipeweave.validation_result.md) | 公開前評価結果 | 8 | database/migrations/002_relational_schema.sql:statement-411 |
| [recipeweave.workspace_revision](tables/recipeweave.workspace_revision.md) | 利用者ワークスペースの原子的更新版 | 4 | database/migrations/003_service_operations.sql:statement-25 |

[ER図](ER.md) / [APIとのCRUD](../api/CRUD.md)
