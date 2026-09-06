# 要因別単体テスト仕様: entity_unit_create

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
| backend/tests/test_entity_api_db.py::test_real_catalog_administration_and_retirement | Given管理者と新単位 When追加・版条件付き編集・廃止 ThenSQL契約どおり保持する。 | assert database_client.post('/api/entities/unit', headers=headers('alice'), json=body).status_code == 403 / assert created.status_code == 201, created.text / assert retired.status_code == 200, retired.text / assert retired.json()['status'] == 'retired' / assert database_client.delete(path, headers=headers('admin')).status_code == 405 |

宣言応答: 201, 401, 403, 409, 422, 503
