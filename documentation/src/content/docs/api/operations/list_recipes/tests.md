---
title: "検証仕様: list_recipes"
---

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_api.py::test_catalogue_and_recipe_search | 明示URLを呼び出すテスト | assert health.status_code == 200 / assert health.json()['catalog'] == 'sample' / assert all_recipes.status_code == 200 / assert all_recipes.json()['total'] == 8 / assert filtered.status_code == 200 / assert filtered.json()['total'] == 1 / assert filtered.json()['items'][0]['id'] == 'tomato-egg' / assert client.get('/api/recipes/tomato-egg').status_code == 200 / assert client.get('/api/recipes/no-such-recipe').status_code == 404 / assert client.get('/api/foods', params={'q': 'トマト'}).json()['total'] == 1 |
| backend/tests/test_api.py::test_filter_boundaries_and_no_portions_in_search | 明示URLを呼び出すテスト | assert response.status_code == 200 / assert all((item['minutes'] &lt;= 10 for item in response.json()['items'])) / assert client.get('/api/recipes', params={'maxMinutes': '-1'}).status_code == 422 / assert client.get('/api/recipes', params={'servings': '2'}).status_code == 422 / assert all(('egg' not in [ingredient['foodId'] for ingredient in recipe['ingredients']] for recipe in excluded.json()['items'])) |

宣言応答: 200, 422
