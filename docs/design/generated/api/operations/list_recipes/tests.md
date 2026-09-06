# 要因別単体テスト仕様: list_recipes

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

要因別の明示対応は未登録。下の実URL試験のみを静的に確認できる。

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_api.py::test_catalogue_requires_database_configuration | 明示URLを呼び出すテスト | assert client.get('/api/foods').status_code == 503 / assert client.get('/api/recipes').status_code == 503 |
| backend/tests/test_catalog_database.py::test_public_search_never_exposes_review_pending_recipes | 明示URLを呼び出すテスト | assert response.status_code == 200 / assert response.json()['total'] == 0 / assert response.json()['items'] == [] / assert database_client.get('/api/recipes/' + recipe_id).status_code == 404 / assert random.status_code == 200 / assert random.json() == {'item': None, 'total': 0} |
| backend/tests/test_catalog_database.py::test_preview_requires_signed_identity_and_local_environment | 明示URLを呼び出すテスト | assert database_client.get('/api/recipes', params=query).status_code == 401 / assert response.status_code == 200 / assert response.json()['total'] == 8 / assert all((item['sample'] for item in response.json()['items'])) / assert database_client.get('/api/recipes', params=query, headers=preview_headers()).status_code == 403 |
| backend/tests/test_catalog_database.py::test_search_filters_pagination_and_random_exclusion | 明示URLを呼び出すテスト | assert response.status_code == 200 / assert response.json()['total'] == 1 / assert response.json()['items'][0]['id'] == stable_id('recipe', 'tomato-egg') / assert second_page.status_code == 200 / assert second_page.json()['total'] == 8 / assert len(second_page.json()['items']) == 2 / assert second_page.json()['offset'] == 2 / assert excluded.status_code == 200 / assert all((item['minutes'] &lt;= 10 and all((line['foodId'] != egg for line in item['ingredients'])) for item in excluded.json()['items'])) / assert random.status_code == 200 / assert random.json()['item']['id'] != recipe_id / assert all((line['foodId'] != egg for line in random.json()['item']['ingredients'])) |
| backend/tests/test_catalog_database.py::test_invalid_search_inputs_are_rejected | 明示URLを呼び出すテスト | assert database_client.get('/api/recipes/not-a-uuid').status_code == 422 / assert database_client.get('/api/recipes', params=params).status_code == 422 |

宣言応答: 200, 401, 403, 422, 503
