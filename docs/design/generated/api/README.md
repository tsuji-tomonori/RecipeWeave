# API一覧

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

| operationId | HTTP | パス | 要約 | 認証 | 応答 |
|---|---|---|---|---|---|
| [local_login](operations/local_login/interface.md) | POST | /api/auth/local-login | 開発環境へログインする | public; 開発環境限定。本文の資格情報を検証 | 200, 401, 404, 422, 503 |
| [export_backup](operations/export_backup/interface.md) | POST | /api/backups/export | バックアップを書き出す | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 409, 413, 422, 503 |
| [preview_backup](operations/preview_backup/interface.md) | POST | /api/backups/preview | バックアップの全置換内容を検証する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 409, 413, 422, 503 |
| [restore_backup](operations/restore_backup/interface.md) | POST | /api/backups/restore | 確認したバックアップで本人のデータを全置換する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 409, 413, 422, 503 |
| [preview_cooking_plan](operations/preview_cooking_plan/interface.md) | POST | /api/cooking-plan | 保存せずに調理の段取りを確認する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 422, 503 |
| [create_cooking_session](operations/create_cooking_session/interface.md) | POST | /api/cooking-sessions | 調理計画を確定して開始する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [update_cooking_session](operations/update_cooking_session/interface.md) | PATCH | /api/cooking-sessions/{row_id} | 工程・タイマー・調理完了を記録する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [entity_allergen_list](operations/entity_allergen_list/interface.md) | GET | /api/entities/allergen | アレルゲン概念の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_allergen_create](operations/entity_allergen_create/interface.md) | POST | /api/entities/allergen | アレルゲン概念の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_allergen_get](operations/entity_allergen_get/interface.md) | GET | /api/entities/allergen/{row_id} | アレルゲン概念の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_allergen_update](operations/entity_allergen_update/interface.md) | PUT | /api/entities/allergen/{row_id} | アレルゲン概念の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_app_user_list](operations/entity_app_user_list/interface.md) | GET | /api/entities/app_user | アプリ利用者の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_app_user_get](operations/entity_app_user_get/interface.md) | GET | /api/entities/app_user/{row_id} | アプリ利用者の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_app_user_update](operations/entity_app_user_update/interface.md) | PUT | /api/entities/app_user/{row_id} | アプリ利用者の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_audit_event_list](operations/entity_audit_event_list/interface.md) | GET | /api/entities/audit_event | 変更・公開監査の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_audit_event_get](operations/entity_audit_event_get/interface.md) | GET | /api/entities/audit_event/{row_id} | 変更・公開監査の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_axis_list](operations/entity_axis_list/interface.md) | GET | /api/entities/axis | 組み合わせ軸の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_axis_create](operations/entity_axis_create/interface.md) | POST | /api/entities/axis | 組み合わせ軸の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_axis_get](operations/entity_axis_get/interface.md) | GET | /api/entities/axis/{row_id} | 組み合わせ軸の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_axis_update](operations/entity_axis_update/interface.md) | PUT | /api/entities/axis/{row_id} | 組み合わせ軸の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_axis_option_list](operations/entity_axis_option_list/interface.md) | GET | /api/entities/axis_option | 軸候補値の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_axis_option_create](operations/entity_axis_option_create/interface.md) | POST | /api/entities/axis_option | 軸候補値の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_axis_option_get](operations/entity_axis_option_get/interface.md) | GET | /api/entities/axis_option/{row_id} | 軸候補値の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_axis_option_update](operations/entity_axis_option_update/interface.md) | PUT | /api/entities/axis_option/{row_id} | 軸候補値の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_backup_artifact_list](operations/entity_backup_artifact_list/interface.md) | GET | /api/entities/backup_artifact | 本人へ発行したバックアップの証拠。本文を保存せず、削除後も匿名化した発行記録を保持するの一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_backup_artifact_get](operations/entity_backup_artifact_get/interface.md) | GET | /api/entities/backup_artifact/{row_id} | 本人へ発行したバックアップの証拠。本文を保存せず、削除後も匿名化した発行記録を保持するの取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_backup_restore_intent_list](operations/entity_backup_restore_intent_list/interface.md) | GET | /api/entities/backup_restore_intent | 復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度だけ消費するの一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_backup_restore_intent_get](operations/entity_backup_restore_intent_get/interface.md) | GET | /api/entities/backup_restore_intent/{row_id} | 復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度だけ消費するの取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_candidate_attempt_list](operations/entity_candidate_attempt_list/interface.md) | GET | /api/entities/candidate_attempt | 試行済み設計点の台帳の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_candidate_attempt_create](operations/entity_candidate_attempt_create/interface.md) | POST | /api/entities/candidate_attempt | 試行済み設計点の台帳の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_candidate_attempt_get](operations/entity_candidate_attempt_get/interface.md) | GET | /api/entities/candidate_attempt/{row_id} | 試行済み設計点の台帳の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_candidate_attempt_update](operations/entity_candidate_attempt_update/interface.md) | PUT | /api/entities/candidate_attempt/{row_id} | 試行済み設計点の台帳の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_catalog_release_list](operations/entity_catalog_release_list/interface.md) | GET | /api/entities/catalog_release | カタログ公開版の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_catalog_release_create](operations/entity_catalog_release_create/interface.md) | POST | /api/entities/catalog_release | カタログ公開版の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_catalog_release_get](operations/entity_catalog_release_get/interface.md) | GET | /api/entities/catalog_release/{row_id} | カタログ公開版の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_catalog_release_update](operations/entity_catalog_release_update/interface.md) | PUT | /api/entities/catalog_release/{row_id} | カタログ公開版の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_compatibility_rule_list](operations/entity_compatibility_rule_list/interface.md) | GET | /api/entities/compatibility_rule | 組み合わせ・公開ルールの一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_compatibility_rule_create](operations/entity_compatibility_rule_create/interface.md) | POST | /api/entities/compatibility_rule | 組み合わせ・公開ルールの作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_compatibility_rule_get](operations/entity_compatibility_rule_get/interface.md) | GET | /api/entities/compatibility_rule/{row_id} | 組み合わせ・公開ルールの取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_conversion_list](operations/entity_conversion_list/interface.md) | GET | /api/entities/conversion | 食材形態別換算の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_conversion_create](operations/entity_conversion_create/interface.md) | POST | /api/entities/conversion | 食材形態別換算の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_conversion_get](operations/entity_conversion_get/interface.md) | GET | /api/entities/conversion/{row_id} | 食材形態別換算の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_conversion_update](operations/entity_conversion_update/interface.md) | PUT | /api/entities/conversion/{row_id} | 食材形態別換算の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_cooking_session_list](operations/entity_cooking_session_list/interface.md) | GET | /api/entities/cooking_session | 調理計画実行の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_cooking_session_create](operations/entity_cooking_session_create/interface.md) | POST | /api/entities/cooking_session | 調理計画実行の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_cooking_session_delete](operations/entity_cooking_session_delete/interface.md) | DELETE | /api/entities/cooking_session/{row_id} | 調理計画実行の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_cooking_session_get](operations/entity_cooking_session_get/interface.md) | GET | /api/entities/cooking_session/{row_id} | 調理計画実行の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_cooking_session_update](operations/entity_cooking_session_update/interface.md) | PUT | /api/entities/cooking_session/{row_id} | 調理計画実行の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_food_list](operations/entity_food_list/interface.md) | GET | /api/entities/food | 購入・利用食材概念の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_food_create](operations/entity_food_create/interface.md) | POST | /api/entities/food | 購入・利用食材概念の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_food_get](operations/entity_food_get/interface.md) | GET | /api/entities/food/{row_id} | 購入・利用食材概念の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_food_update](operations/entity_food_update/interface.md) | PUT | /api/entities/food/{row_id} | 購入・利用食材概念の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_food_alias_list](operations/entity_food_alias_list/interface.md) | GET | /api/entities/food_alias | 食材別名の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_food_alias_create](operations/entity_food_alias_create/interface.md) | POST | /api/entities/food_alias | 食材別名の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_food_alias_get](operations/entity_food_alias_get/interface.md) | GET | /api/entities/food_alias/{row_id} | 食材別名の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_food_alias_update](operations/entity_food_alias_update/interface.md) | PUT | /api/entities/food_alias/{row_id} | 食材別名の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_food_allergen_list](operations/entity_food_allergen_list/interface.md) | GET | /api/entities/food_allergen | 食材アレルゲン知識の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_food_allergen_create](operations/entity_food_allergen_create/interface.md) | POST | /api/entities/food_allergen | 食材アレルゲン知識の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_food_allergen_get](operations/entity_food_allergen_get/interface.md) | GET | /api/entities/food_allergen/{row_id} | 食材アレルゲン知識の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_food_axis_option_list](operations/entity_food_axis_option_list/interface.md) | GET | /api/entities/food_axis_option | 食材の分類属性の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_food_axis_option_create](operations/entity_food_axis_option_create/interface.md) | POST | /api/entities/food_axis_option | 食材の分類属性の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_food_axis_option_get](operations/entity_food_axis_option_get/interface.md) | GET | /api/entities/food_axis_option/{row_id} | 食材の分類属性の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_food_axis_option_update](operations/entity_food_axis_option_update/interface.md) | PUT | /api/entities/food_axis_option/{row_id} | 食材の分類属性の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_food_form_list](operations/entity_food_form_list/interface.md) | GET | /api/entities/food_form | 食材形態の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_food_form_create](operations/entity_food_form_create/interface.md) | POST | /api/entities/food_form | 食材形態の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_food_form_get](operations/entity_food_form_get/interface.md) | GET | /api/entities/food_form/{row_id} | 食材形態の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_food_form_update](operations/entity_food_form_update/interface.md) | PUT | /api/entities/food_form/{row_id} | 食材形態の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_food_identity_list](operations/entity_food_identity_list/interface.md) | GET | /api/entities/food_identity | 料理同一性上の食品の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_food_identity_create](operations/entity_food_identity_create/interface.md) | POST | /api/entities/food_identity | 料理同一性上の食品の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_food_identity_get](operations/entity_food_identity_get/interface.md) | GET | /api/entities/food_identity/{row_id} | 料理同一性上の食品の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_food_identity_member_list](operations/entity_food_identity_member_list/interface.md) | GET | /api/entities/food_identity_member | 購買食品から同一性への対応の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_food_identity_member_create](operations/entity_food_identity_member_create/interface.md) | POST | /api/entities/food_identity_member | 購買食品から同一性への対応の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_food_identity_member_get](operations/entity_food_identity_member_get/interface.md) | GET | /api/entities/food_identity_member/{row_id} | 購買食品から同一性への対応の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_form_yield_list](operations/entity_form_yield_list/interface.md) | GET | /api/entities/form_yield | 処理歩留まりの一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_form_yield_create](operations/entity_form_yield_create/interface.md) | POST | /api/entities/form_yield | 処理歩留まりの作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_form_yield_get](operations/entity_form_yield_get/interface.md) | GET | /api/entities/form_yield/{row_id} | 処理歩留まりの取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_generation_choice_list](operations/entity_generation_choice_list/interface.md) | GET | /api/entities/generation_choice | 生成軸の選択値の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_generation_choice_create](operations/entity_generation_choice_create/interface.md) | POST | /api/entities/generation_choice | 生成軸の選択値の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_generation_choice_get](operations/entity_generation_choice_get/interface.md) | GET | /api/entities/generation_choice/{row_id} | 生成軸の選択値の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_generation_choice_update](operations/entity_generation_choice_update/interface.md) | PUT | /api/entities/generation_choice/{row_id} | 生成軸の選択値の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_generation_food_list](operations/entity_generation_food_list/interface.md) | GET | /api/entities/generation_food | 生成の食材入力の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_generation_food_create](operations/entity_generation_food_create/interface.md) | POST | /api/entities/generation_food | 生成の食材入力の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_generation_food_get](operations/entity_generation_food_get/interface.md) | GET | /api/entities/generation_food/{row_id} | 生成の食材入力の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_generation_food_update](operations/entity_generation_food_update/interface.md) | PUT | /api/entities/generation_food/{row_id} | 生成の食材入力の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_generation_job_list](operations/entity_generation_job_list/interface.md) | GET | /api/entities/generation_job | 事前生成ジョブの一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_generation_job_create](operations/entity_generation_job_create/interface.md) | POST | /api/entities/generation_job | 事前生成ジョブの作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_generation_job_get](operations/entity_generation_job_get/interface.md) | GET | /api/entities/generation_job/{row_id} | 事前生成ジョブの取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_generation_job_update](operations/entity_generation_job_update/interface.md) | PUT | /api/entities/generation_job/{row_id} | 事前生成ジョブの更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_generation_policy_list](operations/entity_generation_policy_list/interface.md) | GET | /api/entities/generation_policy | AI生成方針版の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_generation_policy_create](operations/entity_generation_policy_create/interface.md) | POST | /api/entities/generation_policy | AI生成方針版の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_generation_policy_get](operations/entity_generation_policy_get/interface.md) | GET | /api/entities/generation_policy/{row_id} | AI生成方針版の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_generation_result_list](operations/entity_generation_result_list/interface.md) | GET | /api/entities/generation_result | 生成結果の出自の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_generation_result_create](operations/entity_generation_result_create/interface.md) | POST | /api/entities/generation_result | 生成結果の出自の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_generation_result_get](operations/entity_generation_result_get/interface.md) | GET | /api/entities/generation_result/{row_id} | 生成結果の出自の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_generation_shard_list](operations/entity_generation_shard_list/interface.md) | GET | /api/entities/generation_shard | 列挙範囲・リース管理の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_generation_shard_create](operations/entity_generation_shard_create/interface.md) | POST | /api/entities/generation_shard | 列挙範囲・リース管理の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_generation_shard_get](operations/entity_generation_shard_get/interface.md) | GET | /api/entities/generation_shard/{row_id} | 列挙範囲・リース管理の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_generation_stratum_metric_list](operations/entity_generation_stratum_metric_list/interface.md) | GET | /api/entities/generation_stratum_metric | 採用率・飽和度の実測の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_generation_stratum_metric_create](operations/entity_generation_stratum_metric_create/interface.md) | POST | /api/entities/generation_stratum_metric | 採用率・飽和度の実測の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_generation_stratum_metric_get](operations/entity_generation_stratum_metric_get/interface.md) | GET | /api/entities/generation_stratum_metric/{row_id} | 採用率・飽和度の実測の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_generation_template_list](operations/entity_generation_template_list/interface.md) | GET | /api/entities/generation_template | 列挙テンプレート版の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_generation_template_create](operations/entity_generation_template_create/interface.md) | POST | /api/entities/generation_template | 列挙テンプレート版の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_generation_template_get](operations/entity_generation_template_get/interface.md) | GET | /api/entities/generation_template/{row_id} | 列挙テンプレート版の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_ingredient_total_list](operations/entity_ingredient_total_list/interface.md) | GET | /api/entities/ingredient_total | 献立材料集計結果の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_ingredient_total_get](operations/entity_ingredient_total_get/interface.md) | GET | /api/entities/ingredient_total/{row_id} | 献立材料集計結果の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_kitchen_resource_list](operations/entity_kitchen_resource_list/interface.md) | GET | /api/entities/kitchen_resource | キッチンの実資源の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_kitchen_resource_create](operations/entity_kitchen_resource_create/interface.md) | POST | /api/entities/kitchen_resource | キッチンの実資源の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_kitchen_resource_delete](operations/entity_kitchen_resource_delete/interface.md) | DELETE | /api/entities/kitchen_resource/{row_id} | キッチンの実資源の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_kitchen_resource_get](operations/entity_kitchen_resource_get/interface.md) | GET | /api/entities/kitchen_resource/{row_id} | キッチンの実資源の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_kitchen_resource_update](operations/entity_kitchen_resource_update/interface.md) | PUT | /api/entities/kitchen_resource/{row_id} | キッチンの実資源の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_material_node_list](operations/entity_material_node_list/interface.md) | GET | /api/entities/material_node | 材料・中間物節点の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_material_node_create](operations/entity_material_node_create/interface.md) | POST | /api/entities/material_node | 材料・中間物節点の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_material_node_get](operations/entity_material_node_get/interface.md) | GET | /api/entities/material_node/{row_id} | 材料・中間物節点の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_material_node_update](operations/entity_material_node_update/interface.md) | PUT | /api/entities/material_node/{row_id} | 材料・中間物節点の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_media_asset_list](operations/entity_media_asset_list/interface.md) | GET | /api/entities/media_asset | 教育用動画等の版の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_media_asset_create](operations/entity_media_asset_create/interface.md) | POST | /api/entities/media_asset | 教育用動画等の版の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_media_asset_get](operations/entity_media_asset_get/interface.md) | GET | /api/entities/media_asset/{row_id} | 教育用動画等の版の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_menu_list](operations/entity_menu_list/interface.md) | GET | /api/entities/menu | 献立の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_menu_create](operations/entity_menu_create/interface.md) | POST | /api/entities/menu | 献立の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_menu_delete](operations/entity_menu_delete/interface.md) | DELETE | /api/entities/menu/{row_id} | 献立の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_menu_get](operations/entity_menu_get/interface.md) | GET | /api/entities/menu/{row_id} | 献立の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_menu_update](operations/entity_menu_update/interface.md) | PUT | /api/entities/menu/{row_id} | 献立の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_menu_ingredient_override_list](operations/entity_menu_ingredient_override_list/interface.md) | GET | /api/entities/menu_ingredient_override | 献立別材料確定の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_menu_ingredient_override_create](operations/entity_menu_ingredient_override_create/interface.md) | POST | /api/entities/menu_ingredient_override | 献立別材料確定の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_menu_ingredient_override_delete](operations/entity_menu_ingredient_override_delete/interface.md) | DELETE | /api/entities/menu_ingredient_override/{row_id} | 献立別材料確定の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_menu_ingredient_override_get](operations/entity_menu_ingredient_override_get/interface.md) | GET | /api/entities/menu_ingredient_override/{row_id} | 献立別材料確定の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_menu_ingredient_override_update](operations/entity_menu_ingredient_override_update/interface.md) | PUT | /api/entities/menu_ingredient_override/{row_id} | 献立別材料確定の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_menu_item_list](operations/entity_menu_item_list/interface.md) | GET | /api/entities/menu_item | 献立の料理の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_menu_item_create](operations/entity_menu_item_create/interface.md) | POST | /api/entities/menu_item | 献立の料理の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_menu_item_delete](operations/entity_menu_item_delete/interface.md) | DELETE | /api/entities/menu_item/{row_id} | 献立の料理の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_menu_item_get](operations/entity_menu_item_get/interface.md) | GET | /api/entities/menu_item/{row_id} | 献立の料理の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_menu_item_update](operations/entity_menu_item_update/interface.md) | PUT | /api/entities/menu_item/{row_id} | 献立の料理の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_nutrient_list](operations/entity_nutrient_list/interface.md) | GET | /api/entities/nutrient | 栄養成分種別の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_nutrient_create](operations/entity_nutrient_create/interface.md) | POST | /api/entities/nutrient | 栄養成分種別の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_nutrient_get](operations/entity_nutrient_get/interface.md) | GET | /api/entities/nutrient/{row_id} | 栄養成分種別の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_nutrient_update](operations/entity_nutrient_update/interface.md) | PUT | /api/entities/nutrient/{row_id} | 栄養成分種別の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_nutrition_fact_list](operations/entity_nutrition_fact_list/interface.md) | GET | /api/entities/nutrition_fact | 形態・商品別栄養値の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_nutrition_fact_create](operations/entity_nutrition_fact_create/interface.md) | POST | /api/entities/nutrition_fact | 形態・商品別栄養値の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_nutrition_fact_get](operations/entity_nutrition_fact_get/interface.md) | GET | /api/entities/nutrition_fact/{row_id} | 形態・商品別栄養値の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_operation_list](operations/entity_operation_list/interface.md) | GET | /api/entities/operation | 標準調理動作の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_operation_create](operations/entity_operation_create/interface.md) | POST | /api/entities/operation | 標準調理動作の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_operation_get](operations/entity_operation_get/interface.md) | GET | /api/entities/operation/{row_id} | 標準調理動作の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_operation_update](operations/entity_operation_update/interface.md) | PUT | /api/entities/operation/{row_id} | 標準調理動作の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_operation_parameter_list](operations/entity_operation_parameter_list/interface.md) | GET | /api/entities/operation_parameter | 動作パラメータ定義の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_operation_parameter_create](operations/entity_operation_parameter_create/interface.md) | POST | /api/entities/operation_parameter | 動作パラメータ定義の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_operation_parameter_get](operations/entity_operation_parameter_get/interface.md) | GET | /api/entities/operation_parameter/{row_id} | 動作パラメータ定義の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_operation_parameter_update](operations/entity_operation_parameter_update/interface.md) | PUT | /api/entities/operation_parameter/{row_id} | 動作パラメータ定義の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_outbox_event_list](operations/entity_outbox_event_list/interface.md) | GET | /api/entities/outbox_event | 検索・キャッシュ更新配信の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_outbox_event_get](operations/entity_outbox_event_get/interface.md) | GET | /api/entities/outbox_event/{row_id} | 検索・キャッシュ更新配信の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_pantry_consumption_list](operations/entity_pantry_consumption_list/interface.md) | GET | /api/entities/pantry_consumption | 調理による在庫消費の冪等台帳の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_pantry_consumption_get](operations/entity_pantry_consumption_get/interface.md) | GET | /api/entities/pantry_consumption/{row_id} | 調理による在庫消費の冪等台帳の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_pantry_lot_list](operations/entity_pantry_lot_list/interface.md) | GET | /api/entities/pantry_lot | 手持ち食材ロットの一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_pantry_lot_create](operations/entity_pantry_lot_create/interface.md) | POST | /api/entities/pantry_lot | 手持ち食材ロットの作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_pantry_lot_delete](operations/entity_pantry_lot_delete/interface.md) | DELETE | /api/entities/pantry_lot/{row_id} | 手持ち食材ロットの削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_pantry_lot_get](operations/entity_pantry_lot_get/interface.md) | GET | /api/entities/pantry_lot/{row_id} | 手持ち食材ロットの取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_pantry_lot_update](operations/entity_pantry_lot_update/interface.md) | PUT | /api/entities/pantry_lot/{row_id} | 手持ち食材ロットの更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_product_list](operations/entity_product_list/interface.md) | GET | /api/entities/product | 市販商品識別の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_product_create](operations/entity_product_create/interface.md) | POST | /api/entities/product | 市販商品識別の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_product_get](operations/entity_product_get/interface.md) | GET | /api/entities/product/{row_id} | 市販商品識別の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_product_update](operations/entity_product_update/interface.md) | PUT | /api/entities/product/{row_id} | 市販商品識別の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_product_allergen_list](operations/entity_product_allergen_list/interface.md) | GET | /api/entities/product_allergen | 商品表示アレルゲンの一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_product_allergen_create](operations/entity_product_allergen_create/interface.md) | POST | /api/entities/product_allergen | 商品表示アレルゲンの作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_product_allergen_get](operations/entity_product_allergen_get/interface.md) | GET | /api/entities/product_allergen/{row_id} | 商品表示アレルゲンの取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_product_component_list](operations/entity_product_component_list/interface.md) | GET | /api/entities/product_component | セット内構成品の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_product_component_create](operations/entity_product_component_create/interface.md) | POST | /api/entities/product_component | セット内構成品の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_product_component_get](operations/entity_product_component_get/interface.md) | GET | /api/entities/product_component/{row_id} | セット内構成品の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_product_preparation_rule_list](operations/entity_product_preparation_rule_list/interface.md) | GET | /api/entities/product_preparation_rule | 商品固有の調理条件の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_product_preparation_rule_create](operations/entity_product_preparation_rule_create/interface.md) | POST | /api/entities/product_preparation_rule | 商品固有の調理条件の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_product_preparation_rule_get](operations/entity_product_preparation_rule_get/interface.md) | GET | /api/entities/product_preparation_rule/{row_id} | 商品固有の調理条件の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_product_version_list](operations/entity_product_version_list/interface.md) | GET | /api/entities/product_version | 商品仕様版の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_product_version_create](operations/entity_product_version_create/interface.md) | POST | /api/entities/product_version | 商品仕様版の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_product_version_get](operations/entity_product_version_get/interface.md) | GET | /api/entities/product_version/{row_id} | 商品仕様版の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_receipt_import_list](operations/entity_receipt_import_list/interface.md) | GET | /api/entities/receipt_import | レシート読取・在庫登録の処理単位の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_receipt_import_create](operations/entity_receipt_import_create/interface.md) | POST | /api/entities/receipt_import | レシート読取・在庫登録の処理単位の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_receipt_import_delete](operations/entity_receipt_import_delete/interface.md) | DELETE | /api/entities/receipt_import/{row_id} | レシート読取・在庫登録の処理単位の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_receipt_import_get](operations/entity_receipt_import_get/interface.md) | GET | /api/entities/receipt_import/{row_id} | レシート読取・在庫登録の処理単位の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_receipt_import_update](operations/entity_receipt_import_update/interface.md) | PUT | /api/entities/receipt_import/{row_id} | レシート読取・在庫登録の処理単位の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_receipt_line_list](operations/entity_receipt_line_list/interface.md) | GET | /api/entities/receipt_line | レシートの商品候補と確定した在庫の対応の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_receipt_line_create](operations/entity_receipt_line_create/interface.md) | POST | /api/entities/receipt_line | レシートの商品候補と確定した在庫の対応の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_receipt_line_delete](operations/entity_receipt_line_delete/interface.md) | DELETE | /api/entities/receipt_line/{row_id} | レシートの商品候補と確定した在庫の対応の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_receipt_line_get](operations/entity_receipt_line_get/interface.md) | GET | /api/entities/receipt_line/{row_id} | レシートの商品候補と確定した在庫の対応の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_receipt_line_update](operations/entity_receipt_line_update/interface.md) | PUT | /api/entities/receipt_line/{row_id} | レシートの商品候補と確定した在庫の対応の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_recipe_list](operations/entity_recipe_list/interface.md) | GET | /api/entities/recipe | レシピ同一性の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_recipe_create](operations/entity_recipe_create/interface.md) | POST | /api/entities/recipe | レシピ同一性の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_recipe_get](operations/entity_recipe_get/interface.md) | GET | /api/entities/recipe/{row_id} | レシピ同一性の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_recipe_update](operations/entity_recipe_update/interface.md) | PUT | /api/entities/recipe/{row_id} | レシピ同一性の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_recipe_embedding_list](operations/entity_recipe_embedding_list/interface.md) | GET | /api/entities/recipe_embedding | 近似検索用特徴量の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_recipe_embedding_create](operations/entity_recipe_embedding_create/interface.md) | POST | /api/entities/recipe_embedding | 近似検索用特徴量の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_recipe_embedding_get](operations/entity_recipe_embedding_get/interface.md) | GET | /api/entities/recipe_embedding/{row_id} | 近似検索用特徴量の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_recipe_embedding_update](operations/entity_recipe_embedding_update/interface.md) | PUT | /api/entities/recipe_embedding/{row_id} | 近似検索用特徴量の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_recipe_ingredient_list](operations/entity_recipe_ingredient_list/interface.md) | GET | /api/entities/recipe_ingredient | レシピ材料明細の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_recipe_ingredient_create](operations/entity_recipe_ingredient_create/interface.md) | POST | /api/entities/recipe_ingredient | レシピ材料明細の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_recipe_ingredient_get](operations/entity_recipe_ingredient_get/interface.md) | GET | /api/entities/recipe_ingredient/{row_id} | レシピ材料明細の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_recipe_ingredient_update](operations/entity_recipe_ingredient_update/interface.md) | PUT | /api/entities/recipe_ingredient/{row_id} | レシピ材料明細の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_recipe_option_list](operations/entity_recipe_option_list/interface.md) | GET | /api/entities/recipe_option | 版の分類・特徴の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_recipe_option_create](operations/entity_recipe_option_create/interface.md) | POST | /api/entities/recipe_option | 版の分類・特徴の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_recipe_option_get](operations/entity_recipe_option_get/interface.md) | GET | /api/entities/recipe_option/{row_id} | 版の分類・特徴の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_recipe_option_update](operations/entity_recipe_option_update/interface.md) | PUT | /api/entities/recipe_option/{row_id} | 版の分類・特徴の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_recipe_search_document_list](operations/entity_recipe_search_document_list/interface.md) | GET | /api/entities/recipe_search_document | 公開検索用文書の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_recipe_search_document_get](operations/entity_recipe_search_document_get/interface.md) | GET | /api/entities/recipe_search_document/{row_id} | 公開検索用文書の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_recipe_signature_list](operations/entity_recipe_signature_list/interface.md) | GET | /api/entities/recipe_signature | 内容重複判定署名の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_recipe_signature_create](operations/entity_recipe_signature_create/interface.md) | POST | /api/entities/recipe_signature | 内容重複判定署名の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_recipe_signature_get](operations/entity_recipe_signature_get/interface.md) | GET | /api/entities/recipe_signature/{row_id} | 内容重複判定署名の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_recipe_similarity_list](operations/entity_recipe_similarity_list/interface.md) | GET | /api/entities/recipe_similarity | 近似レシピ関係の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_recipe_similarity_create](operations/entity_recipe_similarity_create/interface.md) | POST | /api/entities/recipe_similarity | 近似レシピ関係の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_recipe_similarity_get](operations/entity_recipe_similarity_get/interface.md) | GET | /api/entities/recipe_similarity/{row_id} | 近似レシピ関係の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_recipe_similarity_update](operations/entity_recipe_similarity_update/interface.md) | PUT | /api/entities/recipe_similarity/{row_id} | 近似レシピ関係の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_recipe_step_list](operations/entity_recipe_step_list/interface.md) | GET | /api/entities/recipe_step | 調理工程節点の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_recipe_step_create](operations/entity_recipe_step_create/interface.md) | POST | /api/entities/recipe_step | 調理工程節点の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_recipe_step_get](operations/entity_recipe_step_get/interface.md) | GET | /api/entities/recipe_step/{row_id} | 調理工程節点の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_recipe_step_update](operations/entity_recipe_step_update/interface.md) | PUT | /api/entities/recipe_step/{row_id} | 調理工程節点の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_recipe_version_list](operations/entity_recipe_version_list/interface.md) | GET | /api/entities/recipe_version | レシピ内容版の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_recipe_version_create](operations/entity_recipe_version_create/interface.md) | POST | /api/entities/recipe_version | レシピ内容版の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_recipe_version_get](operations/entity_recipe_version_get/interface.md) | GET | /api/entities/recipe_version/{row_id} | レシピ内容版の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_recipe_version_update](operations/entity_recipe_version_update/interface.md) | PUT | /api/entities/recipe_version/{row_id} | レシピ内容版の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_resource_reservation_list](operations/entity_resource_reservation_list/interface.md) | GET | /api/entities/resource_reservation | 資源の予約の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_resource_reservation_create](operations/entity_resource_reservation_create/interface.md) | POST | /api/entities/resource_reservation | 資源の予約の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_resource_reservation_delete](operations/entity_resource_reservation_delete/interface.md) | DELETE | /api/entities/resource_reservation/{row_id} | 資源の予約の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_resource_reservation_get](operations/entity_resource_reservation_get/interface.md) | GET | /api/entities/resource_reservation/{row_id} | 資源の予約の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_resource_reservation_update](operations/entity_resource_reservation_update/interface.md) | PUT | /api/entities/resource_reservation/{row_id} | 資源の予約の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_resource_type_list](operations/entity_resource_type_list/interface.md) | GET | /api/entities/resource_type | 道具・設備・作業者種別の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_resource_type_create](operations/entity_resource_type_create/interface.md) | POST | /api/entities/resource_type | 道具・設備・作業者種別の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_resource_type_get](operations/entity_resource_type_get/interface.md) | GET | /api/entities/resource_type/{row_id} | 道具・設備・作業者種別の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_resource_type_update](operations/entity_resource_type_update/interface.md) | PUT | /api/entities/resource_type/{row_id} | 道具・設備・作業者種別の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_scaling_point_list](operations/entity_scaling_point_list/interface.md) | GET | /api/entities/scaling_point | 検証済み換算点の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_scaling_point_create](operations/entity_scaling_point_create/interface.md) | POST | /api/entities/scaling_point | 検証済み換算点の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_scaling_point_get](operations/entity_scaling_point_get/interface.md) | GET | /api/entities/scaling_point/{row_id} | 検証済み換算点の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_scaling_rule_list](operations/entity_scaling_rule_list/interface.md) | GET | /api/entities/scaling_rule | 人数変更規則の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_scaling_rule_create](operations/entity_scaling_rule_create/interface.md) | POST | /api/entities/scaling_rule | 人数変更規則の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_scaling_rule_get](operations/entity_scaling_rule_get/interface.md) | GET | /api/entities/scaling_rule/{row_id} | 人数変更規則の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_session_task_list](operations/entity_session_task_list/interface.md) | GET | /api/entities/session_task | 展開済み工程の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_session_task_create](operations/entity_session_task_create/interface.md) | POST | /api/entities/session_task | 展開済み工程の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_session_task_delete](operations/entity_session_task_delete/interface.md) | DELETE | /api/entities/session_task/{row_id} | 展開済み工程の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_session_task_get](operations/entity_session_task_get/interface.md) | GET | /api/entities/session_task/{row_id} | 展開済み工程の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_session_task_update](operations/entity_session_task_update/interface.md) | PUT | /api/entities/session_task/{row_id} | 展開済み工程の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_shopping_item_list](operations/entity_shopping_item_list/interface.md) | GET | /api/entities/shopping_item | 買い物行の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_shopping_item_create](operations/entity_shopping_item_create/interface.md) | POST | /api/entities/shopping_item | 買い物行の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_shopping_item_delete](operations/entity_shopping_item_delete/interface.md) | DELETE | /api/entities/shopping_item/{row_id} | 買い物行の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_shopping_item_get](operations/entity_shopping_item_get/interface.md) | GET | /api/entities/shopping_item/{row_id} | 買い物行の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_shopping_item_update](operations/entity_shopping_item_update/interface.md) | PUT | /api/entities/shopping_item/{row_id} | 買い物行の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_source_record_list](operations/entity_source_record_list/interface.md) | GET | /api/entities/source_record | 根拠資料の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_source_record_create](operations/entity_source_record_create/interface.md) | POST | /api/entities/source_record | 根拠資料の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_source_record_get](operations/entity_source_record_get/interface.md) | GET | /api/entities/source_record/{row_id} | 根拠資料の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_source_record_update](operations/entity_source_record_update/interface.md) | PUT | /api/entities/source_record/{row_id} | 根拠資料の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_step_dependency_list](operations/entity_step_dependency_list/interface.md) | GET | /api/entities/step_dependency | 工程依存辺の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_step_dependency_create](operations/entity_step_dependency_create/interface.md) | POST | /api/entities/step_dependency | 工程依存辺の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_step_dependency_get](operations/entity_step_dependency_get/interface.md) | GET | /api/entities/step_dependency/{row_id} | 工程依存辺の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_step_dependency_update](operations/entity_step_dependency_update/interface.md) | PUT | /api/entities/step_dependency/{row_id} | 工程依存辺の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_step_input_list](operations/entity_step_input_list/interface.md) | GET | /api/entities/step_input | 工程への材料受渡しの一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_step_input_create](operations/entity_step_input_create/interface.md) | POST | /api/entities/step_input | 工程への材料受渡しの作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_step_input_get](operations/entity_step_input_get/interface.md) | GET | /api/entities/step_input/{row_id} | 工程への材料受渡しの取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_step_input_update](operations/entity_step_input_update/interface.md) | PUT | /api/entities/step_input/{row_id} | 工程への材料受渡しの更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_step_media_list](operations/entity_step_media_list/interface.md) | GET | /api/entities/step_media | 工程別メディア選択の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_step_media_create](operations/entity_step_media_create/interface.md) | POST | /api/entities/step_media | 工程別メディア選択の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_step_media_get](operations/entity_step_media_get/interface.md) | GET | /api/entities/step_media/{row_id} | 工程別メディア選択の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_step_media_update](operations/entity_step_media_update/interface.md) | PUT | /api/entities/step_media/{row_id} | 工程別メディア選択の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_step_parameter_list](operations/entity_step_parameter_list/interface.md) | GET | /api/entities/step_parameter | 工程の型付きパラメータの一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_step_parameter_create](operations/entity_step_parameter_create/interface.md) | POST | /api/entities/step_parameter | 工程の型付きパラメータの作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_step_parameter_get](operations/entity_step_parameter_get/interface.md) | GET | /api/entities/step_parameter/{row_id} | 工程の型付きパラメータの取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_step_parameter_update](operations/entity_step_parameter_update/interface.md) | PUT | /api/entities/step_parameter/{row_id} | 工程の型付きパラメータの更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_step_resource_list](operations/entity_step_resource_list/interface.md) | GET | /api/entities/step_resource | 工程の資源要求の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_step_resource_create](operations/entity_step_resource_create/interface.md) | POST | /api/entities/step_resource | 工程の資源要求の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_step_resource_get](operations/entity_step_resource_get/interface.md) | GET | /api/entities/step_resource/{row_id} | 工程の資源要求の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_step_resource_update](operations/entity_step_resource_update/interface.md) | PUT | /api/entities/step_resource/{row_id} | 工程の資源要求の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_task_dependency_list](operations/entity_task_dependency_list/interface.md) | GET | /api/entities/task_dependency | 献立展開後依存の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_task_dependency_create](operations/entity_task_dependency_create/interface.md) | POST | /api/entities/task_dependency | 献立展開後依存の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_task_dependency_delete](operations/entity_task_dependency_delete/interface.md) | DELETE | /api/entities/task_dependency/{row_id} | 献立展開後依存の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_task_dependency_get](operations/entity_task_dependency_get/interface.md) | GET | /api/entities/task_dependency/{row_id} | 献立展開後依存の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_task_dependency_update](operations/entity_task_dependency_update/interface.md) | PUT | /api/entities/task_dependency/{row_id} | 献立展開後依存の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_unit_list](operations/entity_unit_list/interface.md) | GET | /api/entities/unit | 単位の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_unit_create](operations/entity_unit_create/interface.md) | POST | /api/entities/unit | 単位の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_unit_get](operations/entity_unit_get/interface.md) | GET | /api/entities/unit/{row_id} | 単位の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_unit_update](operations/entity_unit_update/interface.md) | PUT | /api/entities/unit/{row_id} | 単位の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_user_exclusion_list](operations/entity_user_exclusion_list/interface.md) | GET | /api/entities/user_exclusion | 避けたい食材・物質の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_user_exclusion_create](operations/entity_user_exclusion_create/interface.md) | POST | /api/entities/user_exclusion | 避けたい食材・物質の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_user_exclusion_delete](operations/entity_user_exclusion_delete/interface.md) | DELETE | /api/entities/user_exclusion/{row_id} | 避けたい食材・物質の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_user_exclusion_get](operations/entity_user_exclusion_get/interface.md) | GET | /api/entities/user_exclusion/{row_id} | 避けたい食材・物質の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_user_exclusion_update](operations/entity_user_exclusion_update/interface.md) | PUT | /api/entities/user_exclusion/{row_id} | 避けたい食材・物質の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_user_food_list](operations/entity_user_food_list/interface.md) | GET | /api/entities/user_food | 利用者が追加した独自食材の所有の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_user_food_create](operations/entity_user_food_create/interface.md) | POST | /api/entities/user_food | 利用者が追加した独自食材の所有の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_user_food_delete](operations/entity_user_food_delete/interface.md) | DELETE | /api/entities/user_food/{row_id} | 利用者が追加した独自食材の所有の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_user_food_get](operations/entity_user_food_get/interface.md) | GET | /api/entities/user_food/{row_id} | 利用者が追加した独自食材の所有の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_user_food_update](operations/entity_user_food_update/interface.md) | PUT | /api/entities/user_food/{row_id} | 利用者が追加した独自食材の所有の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_user_pantry_food_list](operations/entity_user_pantry_food_list/interface.md) | GET | /api/entities/user_pantry_food | 利用者が常備すると設定した食材の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_user_pantry_food_create](operations/entity_user_pantry_food_create/interface.md) | POST | /api/entities/user_pantry_food | 利用者が常備すると設定した食材の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_user_pantry_food_delete](operations/entity_user_pantry_food_delete/interface.md) | DELETE | /api/entities/user_pantry_food/{row_id} | 利用者が常備すると設定した食材の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_user_pantry_food_get](operations/entity_user_pantry_food_get/interface.md) | GET | /api/entities/user_pantry_food/{row_id} | 利用者が常備すると設定した食材の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_user_pantry_food_update](operations/entity_user_pantry_food_update/interface.md) | PUT | /api/entities/user_pantry_food/{row_id} | 利用者が常備すると設定した食材の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_user_preference_list](operations/entity_user_preference_list/interface.md) | GET | /api/entities/user_preference | ユーザーの嗜好の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_user_preference_create](operations/entity_user_preference_create/interface.md) | POST | /api/entities/user_preference | ユーザーの嗜好の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_user_preference_delete](operations/entity_user_preference_delete/interface.md) | DELETE | /api/entities/user_preference/{row_id} | ユーザーの嗜好の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_user_preference_get](operations/entity_user_preference_get/interface.md) | GET | /api/entities/user_preference/{row_id} | ユーザーの嗜好の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_user_preference_update](operations/entity_user_preference_update/interface.md) | PUT | /api/entities/user_preference/{row_id} | ユーザーの嗜好の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_user_recipe_event_list](operations/entity_user_recipe_event_list/interface.md) | GET | /api/entities/user_recipe_event | 提案・調理履歴の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_user_recipe_event_create](operations/entity_user_recipe_event_create/interface.md) | POST | /api/entities/user_recipe_event | 提案・調理履歴の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_user_recipe_event_delete](operations/entity_user_recipe_event_delete/interface.md) | DELETE | /api/entities/user_recipe_event/{row_id} | 提案・調理履歴の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_user_recipe_event_get](operations/entity_user_recipe_event_get/interface.md) | GET | /api/entities/user_recipe_event/{row_id} | 提案・調理履歴の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_user_shopping_check_list](operations/entity_user_shopping_check_list/interface.md) | GET | /api/entities/user_shopping_check | 調理前の買い物確認の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_user_shopping_check_create](operations/entity_user_shopping_check_create/interface.md) | POST | /api/entities/user_shopping_check | 調理前の買い物確認の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_user_shopping_check_delete](operations/entity_user_shopping_check_delete/interface.md) | DELETE | /api/entities/user_shopping_check/{row_id} | 調理前の買い物確認の削除 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_user_shopping_check_get](operations/entity_user_shopping_check_get/interface.md) | GET | /api/entities/user_shopping_check/{row_id} | 調理前の買い物確認の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_user_shopping_check_update](operations/entity_user_shopping_check_update/interface.md) | PUT | /api/entities/user_shopping_check/{row_id} | 調理前の買い物確認の更新 | bearer | 200, 401, 403, 409, 422, 428, 503 |
| [entity_validation_result_list](operations/entity_validation_result_list/interface.md) | GET | /api/entities/validation_result | 公開前評価結果の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_validation_result_create](operations/entity_validation_result_create/interface.md) | POST | /api/entities/validation_result | 公開前評価結果の作成 | bearer | 201, 401, 403, 409, 422, 503 |
| [entity_validation_result_get](operations/entity_validation_result_get/interface.md) | GET | /api/entities/validation_result/{row_id} | 公開前評価結果の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [entity_workspace_revision_list](operations/entity_workspace_revision_list/interface.md) | GET | /api/entities/workspace_revision | 利用者ワークスペースの原子的更新版の一覧 | bearer | 200, 401, 403, 409, 422, 503 |
| [entity_workspace_revision_get](operations/entity_workspace_revision_get/interface.md) | GET | /api/entities/workspace_revision/{row_id} | 利用者ワークスペースの原子的更新版の取得 | bearer | 200, 401, 403, 404, 409, 422, 503 |
| [list_foods](operations/list_foods/interface.md) | GET | /api/foods | 食材候補を検索する | public | 200, 401, 422, 503 |
| [create_custom_food](operations/create_custom_food/interface.md) | POST | /api/foods/custom | 本人の独自食材を登録する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [claim_shard](operations/claim_shard/interface.md) | POST | /api/generation/shards/claim | 生成範囲のリース取得 | bearer | 200, 401, 403, 409, 422, 503 |
| [renew_shard](operations/renew_shard/interface.md) | PUT | /api/generation/shards/{row_id}/lease | 生成リースの延長 | bearer | 200, 401, 403, 409, 422, 503 |
| [advance_shard](operations/advance_shard/interface.md) | PUT | /api/generation/shards/{row_id}/progress | 生成範囲の進捗確定 | bearer | 200, 401, 403, 409, 422, 503 |
| [get_health](operations/get_health/interface.md) | GET | /api/health | 稼働状況とサンプル公開範囲 | public | 200 |
| [get_me](operations/get_me/interface.md) | GET | /api/me | 本人のプロフィールを取得する | 検証済みBearerトークン | 200, 401, 404, 422, 503 |
| [add_menu_item](operations/add_menu_item/interface.md) | POST | /api/menus/current/items | 献立へ料理を加える | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [delete_menu_item](operations/delete_menu_item/interface.md) | DELETE | /api/menus/current/items/{row_id} | 献立から料理を外す | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [update_menu_item](operations/update_menu_item/interface.md) | PATCH | /api/menus/current/items/{row_id} | 献立の人数・分量を変更する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [create_pantry_lot](operations/create_pantry_lot/interface.md) | POST | /api/pantry-lots | 手持ち食材を登録する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [delete_pantry_lot](operations/delete_pantry_lot/interface.md) | DELETE | /api/pantry-lots/{row_id} | 手持ち食材を削除する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [update_pantry_lot](operations/update_pantry_lot/interface.md) | PATCH | /api/pantry-lots/{row_id} | 手持ち食材を修正・復元する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [commit_receipt](operations/commit_receipt/interface.md) | POST | /api/receipts/commit | 確認したレシートを在庫へ登録する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [undo_receipt](operations/undo_receipt/interface.md) | POST | /api/receipts/{row_id}/undo | レシート登録を取り消す | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [list_recipes](operations/list_recipes/interface.md) | GET | /api/recipes | 食材・時間から保存済みの料理を探す | public | 200, 401, 403, 422, 503 |
| [random_recipe](operations/random_recipe/interface.md) | GET | /api/recipes/random | 保存済みの料理から一品を選ぶ | public; previewには開発環境の認証が必要 | 200, 401, 403, 422, 503 |
| [get_recipe](operations/get_recipe/interface.md) | GET | /api/recipes/{recipe_id} | 料理の材料と工程を表示する | public | 200, 401, 403, 404, 422, 503 |
| [unsave_recipe](operations/unsave_recipe/interface.md) | DELETE | /api/saved-recipes/{row_id} | 料理の保存を解除する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [save_recipe](operations/save_recipe/interface.md) | PUT | /api/saved-recipes/{row_id} | 料理を保存する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [put_settings](operations/put_settings/interface.md) | PUT | /api/settings | 好み・常備食材・器具を設定する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [put_shopping_checks](operations/put_shopping_checks/interface.md) | PUT | /api/shopping-checks | 買い物の確認状況を保存する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |
| [get_workspace](operations/get_workspace/interface.md) | GET | /api/workspace | ワークスペースを取得する | 検証済みBearerトークンと本人所有権 | 200, 401, 403, 404, 409, 422, 503 |

[CRUD対応](CRUD.md) / [共有モデル](MODELS.md) / [共通エラー](ERRORS.md)
