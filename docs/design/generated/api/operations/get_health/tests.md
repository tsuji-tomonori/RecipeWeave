# 検証仕様: get_health

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_api.py::test_catalogue_and_recipe_search | 明示URLを呼び出すテスト | assert health.status_code == 200 / assert health.json()['catalog'] == 'sample' / assert all_recipes.status_code == 200 / assert all_recipes.json()['total'] == 8 / assert filtered.status_code == 200 / assert filtered.json()['total'] == 1 / assert filtered.json()['items'][0]['id'] == 'tomato-egg' / assert client.get('/api/recipes/tomato-egg').status_code == 200 / assert client.get('/api/recipes/no-such-recipe').status_code == 404 / assert client.get('/api/foods', params={'q': 'トマト'}).json()['total'] == 1 |

宣言応答: 200
