# Driveの原DB設計と物理実装の対応

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

原表を一つずつ実DDLへ照合する。原設計の全列型・NULL性もカタログ生成時に確認し、追加列と変更根拠はschema-policyのcolumn_evolutionsで明示する。

| 原テーブル | 領域 | 意味 | 原列数 | 実列数 | 物理実装 |
|---|---|---|---|---|---|
| source_record | 共通 | 根拠資料 | 8 | 8 | [実DDL仕様](tables/recipeweave.source_record.md) |
| catalog_release | 共通 | カタログ公開版 | 5 | 6 | [実DDL仕様](tables/recipeweave.catalog_release.md) |
| unit | 数量 | 単位 | 8 | 8 | [実DDL仕様](tables/recipeweave.unit.md) |
| food | 食材 | 購入・利用食材概念 | 8 | 9 | [実DDL仕様](tables/recipeweave.food.md) |
| food_alias | 食材 | 食材別名 | 5 | 5 | [実DDL仕様](tables/recipeweave.food_alias.md) |
| food_form | 食材 | 食材形態 | 8 | 8 | [実DDL仕様](tables/recipeweave.food_form.md) |
| conversion | 数量 | 食材形態別換算 | 10 | 10 | [実DDL仕様](tables/recipeweave.conversion.md) |
| form_yield | 数量 | 処理歩留まり | 8 | 8 | [実DDL仕様](tables/recipeweave.form_yield.md) |
| product | 食材 | 市販商品識別 | 7 | 7 | [実DDL仕様](tables/recipeweave.product.md) |
| product_version | 食材 | 商品仕様版 | 11 | 11 | [実DDL仕様](tables/recipeweave.product_version.md) |
| product_component | 食材 | セット内構成品 | 8 | 8 | [実DDL仕様](tables/recipeweave.product_component.md) |
| allergen | 食材 | アレルゲン概念 | 5 | 5 | [実DDL仕様](tables/recipeweave.allergen.md) |
| food_allergen | 食材 | 食材アレルゲン知識 | 6 | 6 | [実DDL仕様](tables/recipeweave.food_allergen.md) |
| product_allergen | 食材 | 商品表示アレルゲン | 6 | 6 | [実DDL仕様](tables/recipeweave.product_allergen.md) |
| nutrient | 食材 | 栄養成分種別 | 5 | 5 | [実DDL仕様](tables/recipeweave.nutrient.md) |
| nutrition_fact | 食材 | 形態・商品別栄養値 | 9 | 9 | [実DDL仕様](tables/recipeweave.nutrition_fact.md) |
| axis | 発想 | 組み合わせ軸 | 8 | 8 | [実DDL仕様](tables/recipeweave.axis.md) |
| axis_option | 発想 | 軸候補値 | 8 | 8 | [実DDL仕様](tables/recipeweave.axis_option.md) |
| food_axis_option | 発想 | 食材の分類属性 | 4 | 4 | [実DDL仕様](tables/recipeweave.food_axis_option.md) |
| recipe | レシピ | レシピ同一性 | 6 | 6 | [実DDL仕様](tables/recipeweave.recipe.md) |
| recipe_version | レシピ | レシピ内容版 | 12 | 13 | [実DDL仕様](tables/recipeweave.recipe_version.md) |
| recipe_option | レシピ | 版の分類・特徴 | 4 | 4 | [実DDL仕様](tables/recipeweave.recipe_option.md) |
| scaling_rule | 数量 | 人数変更規則 | 10 | 10 | [実DDL仕様](tables/recipeweave.scaling_rule.md) |
| scaling_point | 数量 | 検証済み換算点 | 5 | 5 | [実DDL仕様](tables/recipeweave.scaling_point.md) |
| recipe_ingredient | レシピ | レシピ材料明細 | 18 | 19 | [実DDL仕様](tables/recipeweave.recipe_ingredient.md) |
| operation | 工程 | 標準調理動作 | 8 | 8 | [実DDL仕様](tables/recipeweave.operation.md) |
| operation_parameter | 工程 | 動作パラメータ定義 | 11 | 11 | [実DDL仕様](tables/recipeweave.operation_parameter.md) |
| recipe_step | 工程 | 調理工程ノード | 11 | 12 | [実DDL仕様](tables/recipeweave.recipe_step.md) |
| step_parameter | 工程 | 工程の型付きパラメータ | 7 | 7 | [実DDL仕様](tables/recipeweave.step_parameter.md) |
| material_node | 工程 | 材料・中間物ノード | 9 | 9 | [実DDL仕様](tables/recipeweave.material_node.md) |
| step_input | 工程 | 工程への材料受渡し | 5 | 5 | [実DDL仕様](tables/recipeweave.step_input.md) |
| step_dependency | 工程 | 工程依存辺 | 7 | 7 | [実DDL仕様](tables/recipeweave.step_dependency.md) |
| resource_type | 工程 | 道具・設備・作業者種別 | 6 | 6 | [実DDL仕様](tables/recipeweave.resource_type.md) |
| step_resource | 工程 | 工程の資源要求 | 7 | 7 | [実DDL仕様](tables/recipeweave.step_resource.md) |
| media_asset | 表示 | 教育用動画等の版 | 11 | 11 | [実DDL仕様](tables/recipeweave.media_asset.md) |
| step_media | 表示 | 工程別メディア選択 | 6 | 6 | [実DDL仕様](tables/recipeweave.step_media.md) |
| generation_policy | 生成 | AI生成方針版 | 8 | 8 | [実DDL仕様](tables/recipeweave.generation_policy.md) |
| generation_job | 生成 | 事前生成ジョブ | 10 | 10 | [実DDL仕様](tables/recipeweave.generation_job.md) |
| generation_choice | 生成 | 生成軸の選択値 | 4 | 4 | [実DDL仕様](tables/recipeweave.generation_choice.md) |
| generation_food | 生成 | 生成の食材入力 | 5 | 5 | [実DDL仕様](tables/recipeweave.generation_food.md) |
| generation_result | 生成 | 生成結果の出自 | 8 | 8 | [実DDL仕様](tables/recipeweave.generation_result.md) |
| compatibility_rule | 生成 | 組み合わせ・公開ルール | 9 | 9 | [実DDL仕様](tables/recipeweave.compatibility_rule.md) |
| validation_result | 生成 | 公開前評価結果 | 8 | 8 | [実DDL仕様](tables/recipeweave.validation_result.md) |
| recipe_signature | 検索 | 内容重複判定署名 | 7 | 7 | [実DDL仕様](tables/recipeweave.recipe_signature.md) |
| recipe_similarity | 検索 | 近似レシピ関係 | 7 | 7 | [実DDL仕様](tables/recipeweave.recipe_similarity.md) |
| app_user | 利用者 | アプリ利用者 | 6 | 6 | [実DDL仕様](tables/recipeweave.app_user.md) |
| user_preference | 利用者 | ユーザーの嗜好 | 5 | 5 | [実DDL仕様](tables/recipeweave.user_preference.md) |
| user_exclusion | 利用者 | 避けたい食材・物質 | 6 | 6 | [実DDL仕様](tables/recipeweave.user_exclusion.md) |
| user_recipe_event | 利用者 | 提案・調理履歴 | 7 | 7 | [実DDL仕様](tables/recipeweave.user_recipe_event.md) |
| menu | 献立 | 献立 | 6 | 6 | [実DDL仕様](tables/recipeweave.menu.md) |
| menu_item | 献立 | 献立の料理 | 7 | 7 | [実DDL仕様](tables/recipeweave.menu_item.md) |
| menu_ingredient_override | 献立 | 献立別材料確定 | 8 | 8 | [実DDL仕様](tables/recipeweave.menu_ingredient_override.md) |
| kitchen_resource | 献立 | キッチンの実資源 | 7 | 8 | [実DDL仕様](tables/recipeweave.kitchen_resource.md) |
| cooking_session | 献立 | 調理計画実行 | 9 | 10 | [実DDL仕様](tables/recipeweave.cooking_session.md) |
| session_task | 献立 | 展開済み工程 | 11 | 13 | [実DDL仕様](tables/recipeweave.session_task.md) |
| task_dependency | 献立 | 献立展開後依存 | 7 | 7 | [実DDL仕様](tables/recipeweave.task_dependency.md) |
| resource_reservation | 献立 | 資源の予約 | 7 | 7 | [実DDL仕様](tables/recipeweave.resource_reservation.md) |
| ingredient_total | 献立 | 献立材料集計結果 | 9 | 11 | [実DDL仕様](tables/recipeweave.ingredient_total.md) |
| pantry_lot | 献立 | 手持ち食材ロット | 9 | 19 | [実DDL仕様](tables/recipeweave.pantry_lot.md) |
| shopping_item | 献立 | 買い物行 | 9 | 12 | [実DDL仕様](tables/recipeweave.shopping_item.md) |
| audit_event | 運用 | 変更・公開監査 | 8 | 8 | [実DDL仕様](tables/recipeweave.audit_event.md) |
| outbox_event | 運用 | 検索・キャッシュ更新配信 | 7 | 7 | [実DDL仕様](tables/recipeweave.outbox_event.md) |
| product_preparation_rule | 食材 | 商品固有の調理条件 | 8 | 8 | [実DDL仕様](tables/recipeweave.product_preparation_rule.md) |
| food_identity | 大規模生成 | 料理同一性上の食品 | 5 | 5 | [実DDL仕様](tables/recipeweave.food_identity.md) |
| food_identity_member | 大規模生成 | 購買食品から同一性への対応 | 6 | 6 | [実DDL仕様](tables/recipeweave.food_identity_member.md) |
| generation_template | 大規模生成 | 列挙テンプレート版 | 8 | 8 | [実DDL仕様](tables/recipeweave.generation_template.md) |
| generation_shard | 大規模生成 | 列挙範囲・リース管理 | 10 | 10 | [実DDL仕様](tables/recipeweave.generation_shard.md) |
| candidate_attempt | 大規模生成 | 試行済み設計点の台帳 | 10 | 10 | [実DDL仕様](tables/recipeweave.candidate_attempt.md) |
| recipe_search_document | 大規模生成 | 公開検索用文書 | 12 | 12 | [実DDL仕様](tables/recipeweave.recipe_search_document.md) |
| recipe_embedding | 大規模生成 | 近似検索用特徴量 | 7 | 7 | [実DDL仕様](tables/recipeweave.recipe_embedding.md) |
| generation_stratum_metric | 大規模生成 | 採用率・飽和度の実測 | 14 | 14 | [実DDL仕様](tables/recipeweave.generation_stratum_metric.md) |

移行台帳、レシート等の追加表は [全物理テーブル一覧](README.md) に含める。
