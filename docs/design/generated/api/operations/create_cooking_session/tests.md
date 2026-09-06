# 要因別単体テスト仕様: create_cooking_session

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

要因別の明示対応は未登録。下の実URL試験のみを静的に確認できる。

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_backup_database.py::test_backup_database_preserves_completed_cooking_receipts_and_consumption | Givenレシート・手動時間・調理完了 When全置換 Then原始ID/入力hash/消費台帳を保持。 | assert recipe_response.status_code == 200, recipe_response.text / assert receipt.status_code == 200, receipt.text / assert started.status_code == 200, started.text / assert completed.status_code == 200, completed.text / assert original_session['status'] == 'completed' / assert any((row['session_id'] == session['id'] for row in original['tables']['pantry_consumption'])) / assert tasks and all((row['duration_source'] == 'user_estimate' for row in tasks)) / assert all((row['confirmed_duration_s'] is not None for row in tasks)) / assert any((row['id'] == receipt_id for row in original['tables']['receipt_import'])) / assert restored.status_code == 200, restored.text / assert export(client)['tables'] == original['tables'] / assert completed_previous.status_code == 200, completed_previous.text |
| backend/tests/test_workflow_database.py::test_recipe_cooking_is_planned_from_db_and_consumed_once | 明示URLを呼び出すテスト | assert recipe_response.status_code == 200, recipe_response.text / assert recipe['versionId'] == stable_id('recipe_version', 'tomato-egg/1') / assert all((line['ingredientId'] for line in recipe['ingredients'])) / assert len({line['ingredientId'] for line in recipe['ingredients']}) == len(recipe['ingredients']) / assert rejected.status_code == 422, rejected.text / assert workspace(workflow_client, 'bob') == before / assert unconfirmed.status_code == 422 / assert preview.status_code == 200, preview.text / assert all((task['durationSource'] == 'user_estimate' for task in preview.json()['plan'])) / assert started.status_code == 200, started.text / assert len(roles) == 1 / assert roles[0]['role_option_id'] == roles[0]['recipe_role_id'] / assert roles[0]['label'] == '主菜' / assert cooking['mealSnapshot'][0]['servings'] == 3 / assert all((task['durationSource'] == 'user_estimate' for task in cooking['plan'])) / assert {task['id']: task['confirmedDurationSeconds'] for task in cooking['plan']} == expected_times / assert workspace(workflow_client, 'bob')['cooking']['plan'] == cooking['plan'] / assert [(row['id'], row['minutes']) for row in cooking['plan']] == [(row['id'], row['minutes']) for row in preview.json()['plan']] / assert cooking['mealSnapshot'][0]['recipeVersionId'] == recipe['versionId'] / assert set(cooking['mealSnapshot'][0]['amounts']) == {line['ingredientId'] for line in recipe['ingredients']} / assert len(cooking['plan']) == len(recipe['steps']) / assert {step['id'] for step in cooking['plan']} == {step['id'] for step in recipe['steps']} / assert completed.status_code == 200, completed.text / assert state['cooking']['status'] == 'completed' / assert all((row['applied'] for row in state['cooking']['consumptionResults'])) / assert all((row['quantity']['value'] == 0 for row in state['lots'] if row['id'] in created_lots)) / assert replay.status_code == 409 / assert workspace(workflow_client, 'bob')['version'] == state['version'] / assert response.status_code == 200, response.text |

宣言応答: 200, 401, 403, 404, 409, 422, 503
