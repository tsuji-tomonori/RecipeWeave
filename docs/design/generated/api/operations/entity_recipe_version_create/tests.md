# 要因別単体テスト仕様: entity_recipe_version_create

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

| 要因 | Given: 前提 | When: 操作 | Then: 期待結果 | 実在テストnode |
|---|---|---|---|---|
| 管理者権限 | 一般利用者で認証済み | カタログまたは運用APIを呼ぶ | DB操作前に403 | backend/tests/test_entity_api.py::test_catalog_requires_admin |

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_entity_api_db.py::test_history_cannot_be_created_to_gain_unpublished_recipe_access | Given他人には未公開の版 When履歴を後付け Then拒否し既存本人履歴だけ継続可能。 | assert versions.status_code == 200 and versions.json(), versions.text / assert family.status_code == 200, family.text / assert recipe.status_code == 201, recipe.text / assert version.status_code == 201, version.text / assert rejected.status_code == 403, rejected.text / assert database_client.get(detail, headers=headers('alice')).status_code == 404 / assert accepted.status_code == 201, accepted.text / assert withdrawal.status_code == 200, withdrawal.text / assert new_owner.status_code == 403, new_owner.text / assert retained.status_code == 201, retained.text / assert database_client.get(detail, headers=headers('alice')).status_code == 200 / assert database_client.get(detail, headers=headers('bob')).status_code == 404 / assert menu.status_code == 201, menu.text |

宣言応答: 201, 401, 403, 409, 422, 503
