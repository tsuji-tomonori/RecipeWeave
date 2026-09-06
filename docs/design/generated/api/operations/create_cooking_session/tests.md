# 要因別単体テスト仕様: create_cooking_session

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

要因別の明示対応は未登録。下の実URL試験のみを静的に確認できる。

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_workflow_database.py::test_recipe_cooking_is_planned_from_db_and_consumed_once | 明示URLを呼び出すテスト | assert recipe_response.status_code == 200, recipe_response.text / assert recipe['versionId'] == stable_id('recipe_version', 'tomato-egg/1') / assert all((line['ingredientId'] for line in recipe['ingredients'])) / assert len({line['ingredientId'] for line in recipe['ingredients']}) == len(recipe['ingredients']) / assert started.status_code == 200, started.text / assert len(roles) == 1 / assert roles[0]['role_option_id'] == roles[0]['recipe_role_id'] / assert roles[0]['label'] == '主菜' / assert cooking['mealSnapshot'][0]['recipeVersionId'] == recipe['versionId'] / assert set(cooking['mealSnapshot'][0]['amounts']) == {line['ingredientId'] for line in recipe['ingredients']} / assert len(cooking['plan']) == len(recipe['steps']) / assert {step['id'] for step in cooking['plan']} == {step['id'] for step in recipe['steps']} / assert completed.status_code == 200, completed.text / assert state['cooking']['status'] == 'completed' / assert all((row['applied'] for row in state['cooking']['consumptionResults'])) / assert all((row['quantity']['value'] == 0 for row in state['lots'] if row['id'] in created_lots)) / assert replay.status_code == 409 / assert workspace(workflow_client, 'bob')['version'] == state['version'] / assert response.status_code == 200, response.text |

宣言応答: 200, 401, 403, 404, 409, 422, 503
