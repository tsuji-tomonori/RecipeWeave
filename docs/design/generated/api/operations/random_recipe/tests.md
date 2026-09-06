# 要因別単体テスト仕様: random_recipe

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

要因別の明示対応は未登録。下の実URL試験のみを静的に確認できる。

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_catalog_database.py::test_public_search_never_exposes_review_pending_recipes | 明示URLを呼び出すテスト | assert response.status_code == 200 / assert response.json()['total'] == 0 / assert response.json()['items'] == [] / assert database_client.get('/api/recipes/' + recipe_id).status_code == 404 / assert random.status_code == 200 / assert random.json() == {'item': None, 'total': 0} |
| backend/tests/test_catalog_database.py::test_search_filters_pagination_and_random_exclusion | 明示URLを呼び出すテスト | assert response.status_code == 200 / assert response.json()['total'] == 1 / assert response.json()['items'][0]['id'] == stable_id('recipe', 'tomato-egg') / assert second_page.status_code == 200 / assert second_page.json()['total'] == 8 / assert len(second_page.json()['items']) == 2 / assert second_page.json()['offset'] == 2 / assert excluded.status_code == 200 / assert all((item['minutes'] &lt;= 10 and all((line['foodId'] != egg for line in item['ingredients'])) for item in excluded.json()['items'])) / assert random.status_code == 200 / assert random.json()['item']['id'] != recipe_id / assert all((line['foodId'] != egg for line in random.json()['item']['ingredients'])) |
| backend/tests/test_catalog_database.py::test_aws_dev_preview_requires_explicit_flag_and_signed_cognito_identity | CognitoのDevでは未試作8件を認証後だけ表示し、本番公開へ昇格させない。 | assert database_client.get('/api/recipes', params=query).status_code == 401 / assert database_client.get('/api/recipes', params=query, headers=invalid_auth).status_code == 401 / assert listed.status_code == 200, listed.text / assert listed.json()['total'] == 8 / assert all((row['sample'] and row['publicationStatus'] == 'draft' for row in listed.json()['items'])) / assert detail.status_code == 200, detail.text / assert random.status_code == 200 and random.json()['item']['sample'] / assert public.status_code == 200 and public.json()['total'] == 0 / assert database_client.get('/api/recipes', params=query, headers=auth).status_code == 403 / assert database_client.get('/api/recipes', params=query, headers=auth).status_code == 403 / assert issuer == ISSUER / assert client_id == CLIENT_ID |

宣言応答: 200, 401, 403, 422, 503
