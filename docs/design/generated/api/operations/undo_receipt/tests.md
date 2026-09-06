# 要因別単体テスト仕様: undo_receipt

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

要因別の明示対応は未登録。下の実URL試験のみを静的に確認できる。

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_backup_database.py::test_backup_database_preserves_completed_cooking_receipts_and_consumption | Givenレシート・手動時間・調理完了 When全置換 Then原始ID/入力hash/消費台帳を保持。 | assert recipe_response.status_code == 200, recipe_response.text / assert receipt.status_code == 200, receipt.text / assert started.status_code == 200, started.text / assert completed.status_code == 200, completed.text / assert original_session['status'] == 'completed' / assert any((row['session_id'] == session['id'] for row in original['tables']['pantry_consumption'])) / assert tasks and all((row['duration_source'] == 'user_estimate' for row in tasks)) / assert all((row['confirmed_duration_s'] is not None for row in tasks)) / assert any((row['id'] == receipt_id for row in original['tables']['receipt_import'])) / assert restored.status_code == 200, restored.text / assert export(client)['tables'] == original['tables'] / assert completed_previous.status_code == 200, completed_previous.text |
| backend/tests/test_workflow_database.py::test_receipt_unknown_amount_duplicate_and_zero_boundary | 明示URLを呼び出すテスト | assert created.status_code == 200, created.text / assert lot['quantity']['value'] is None / assert rejected.status_code == 409 / assert workspace(workflow_client)['version'] == current['version'] / assert rejected_zero.status_code == 422 / assert workspace(workflow_client)['version'] == current['version'] |
| backend/tests/test_workflow_database.py::test_receipt_partial_undo_preserves_edited_stock | 明示URLを呼び出すテスト | assert added.status_code == 200, added.text / assert len(receipt_lots) == 2 / assert changed.status_code == 200, changed.text / assert undone.status_code == 200, undone.text / assert next((row for row in remaining if row['id'] == edited_id))['quantity']['value'] == 80 / assert next((row for row in remaining if row['id'] == edited_id))['status'] == 'active' / assert next((row for row in remaining if row['id'] != edited_id))['status'] == 'undone' |

宣言応答: 200, 401, 403, 404, 409, 422, 503
