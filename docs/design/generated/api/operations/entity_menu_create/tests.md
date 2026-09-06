# 要因別単体テスト仕様: entity_menu_create

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

| 要因 | Given: 前提 | When: 操作 | Then: 期待結果 | 実在テストnode |
|---|---|---|---|---|
| サーバー管理列 | 所有者・認証主体・献立版の直接入力 | 型付き入力を検証 | 外部指定を許可しない | backend/tests/test_entity_api.py::test_server_owned_columns_are_not_editable |

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_entity_api_db.py::test_real_owned_crud_isolation_and_cas | Given2利用者 When献立作成・他人参照・更新競合・削除 Then本人だけ変更できる。 | assert create.status_code == 201, create.text / assert database_client.get(path, headers=headers('bob')).status_code == 404 / assert database_client.get(path, headers=headers('admin')).status_code == 404 / assert admin_takeover.status_code == 409 / assert database_client.put(path, headers={**headers('alice'), 'If-Match': first_etag}, json=dict(user_id=str(user_id('bob')), name='所有者偽装', servings='2')).status_code == 403 / assert update.status_code == 200, update.text / assert update.json()['revision'] == row['revision'] + 1 / assert conflict.status_code == 409 / assert delete.status_code == 200, delete.text / assert database_client.get(path, headers=headers('alice')).status_code == 404 |
| backend/tests/test_entity_api_db.py::test_database_rls_cannot_be_bypassed_by_raw_row_id | Given別利用者の行ID WhenAPIを通さず非特権DB接続でSELECT ThenRLSが遮断。 | assert created.status_code == 201, created.text / assert row is None |
| backend/tests/test_entity_api_db.py::test_private_input_is_not_echoed_in_validation_response | Given未知の個人情報列 When入力検証 Then422だけ返し本文を応答へ複製しない。 | assert response.status_code == 422 / assert 'private receipt' not in response.text |
| backend/tests/test_entity_api_db.py::test_real_child_reference_cannot_use_other_users_menu | Given別人の献立IDと有効なレシピ When明細作成 Then所有者FK経路で403。 | assert created.status_code == 201, created.text / assert versions.status_code == 200 and versions.json(), versions.text / assert recipe.status_code == 200, recipe.text / assert attempted.status_code == 403, attempted.text / assert deleted.status_code == 200 |
| backend/tests/test_entity_api_db.py::test_history_cannot_be_created_to_gain_unpublished_recipe_access | Given他人には未公開の版 When履歴を後付け Then拒否し既存本人履歴だけ継続可能。 | assert versions.status_code == 200 and versions.json(), versions.text / assert family.status_code == 200, family.text / assert recipe.status_code == 201, recipe.text / assert version.status_code == 201, version.text / assert rejected.status_code == 403, rejected.text / assert database_client.get(detail, headers=headers('alice')).status_code == 404 / assert accepted.status_code == 201, accepted.text / assert withdrawal.status_code == 200, withdrawal.text / assert new_owner.status_code == 403, new_owner.text / assert retained.status_code == 201, retained.text / assert database_client.get(detail, headers=headers('alice')).status_code == 200 / assert database_client.get(detail, headers=headers('bob')).status_code == 404 / assert menu.status_code == 201, menu.text |

宣言応答: 201, 401, 403, 409, 422, 503
