# 要因別単体テスト仕様: preview_cooking_plan

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

要因別の明示対応は未登録。下の実URL試験のみを静的に確認できる。

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_cooking_plan_api.py::test_preview_has_no_workspace_or_cooking_write | 同じ入力を繰り返しても版・在庫・献立・セッションを変更しない。 | assert first.status_code == 200, first.text / assert first.json()['plan'] / assert all((step['mealItemId'] == item['id'] for step in first.json()['plan'])) / assert again.status_code == 200, again.text / assert again.json() == first.json() / assert workspace(workflow_client) == before |
| backend/tests/test_cooking_plan_api.py::test_preview_rejects_inconsistent_inputs_without_saving | 不明量・異なる単位・未確認人数・不可視版・重複行を受理しない。 | assert response.status_code == expected, response.text / assert workspace(workflow_client) == before |
| backend/tests/test_cooking_plan_api.py::test_manual_time_confirmation_rejects_bad_input_without_saving | 人数変更の見積りは、各料理版・献立行の整数秒として明示確認する。 | assert response.status_code == 422, response.text / assert workspace(workflow_client) == before |
| backend/tests/test_workflow_database.py::test_recipe_cooking_is_planned_from_db_and_consumed_once | 明示URLを呼び出すテスト | assert recipe_response.status_code == 200, recipe_response.text / assert recipe['versionId'] == stable_id('recipe_version', 'tomato-egg/1') / assert all((line['ingredientId'] for line in recipe['ingredients'])) / assert len({line['ingredientId'] for line in recipe['ingredients']}) == len(recipe['ingredients']) / assert rejected.status_code == 422, rejected.text / assert workspace(workflow_client, 'bob') == before / assert unconfirmed.status_code == 422 / assert preview.status_code == 200, preview.text / assert all((task['durationSource'] == 'user_estimate' for task in preview.json()['plan'])) / assert started.status_code == 200, started.text / assert len(roles) == 1 / assert roles[0]['role_option_id'] == roles[0]['recipe_role_id'] / assert roles[0]['label'] == '主菜' / assert cooking['mealSnapshot'][0]['servings'] == 3 / assert all((task['durationSource'] == 'user_estimate' for task in cooking['plan'])) / assert {task['id']: task['confirmedDurationSeconds'] for task in cooking['plan']} == expected_times / assert workspace(workflow_client, 'bob')['cooking']['plan'] == cooking['plan'] / assert [(row['id'], row['minutes']) for row in cooking['plan']] == [(row['id'], row['minutes']) for row in preview.json()['plan']] / assert cooking['mealSnapshot'][0]['recipeVersionId'] == recipe['versionId'] / assert set(cooking['mealSnapshot'][0]['amounts']) == {line['ingredientId'] for line in recipe['ingredients']} / assert len(cooking['plan']) == len(recipe['steps']) / assert {step['id'] for step in cooking['plan']} == {step['id'] for step in recipe['steps']} / assert completed.status_code == 200, completed.text / assert state['cooking']['status'] == 'completed' / assert all((row['applied'] for row in state['cooking']['consumptionResults'])) / assert all((row['quantity']['value'] == 0 for row in state['lots'] if row['id'] in created_lots)) / assert replay.status_code == 409 / assert workspace(workflow_client, 'bob')['version'] == state['version'] / assert response.status_code == 200, response.text |

宣言応答: 200, 401, 403, 404, 422, 503
