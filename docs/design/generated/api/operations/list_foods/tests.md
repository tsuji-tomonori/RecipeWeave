# 要因別単体テスト仕様: list_foods

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

要因別の明示対応は未登録。下の実URL試験のみを静的に確認できる。

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_api.py::test_catalogue_requires_database_configuration | 明示URLを呼び出すテスト | assert client.get('/api/foods').status_code == 503 / assert client.get('/api/recipes').status_code == 503 |
| backend/tests/test_catalog_database.py::test_food_catalog_reads_all_rows_and_persisted_alias | 明示URLを呼び出すテスト | assert response.status_code == 200 / assert response.json()['total'] == 1018 / assert found.status_code == 200 / assert [food['id'] for food in found.json()['items']] == [food_id] |

宣言応答: 200, 401, 422, 503
