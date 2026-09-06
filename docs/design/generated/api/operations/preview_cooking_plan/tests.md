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

宣言応答: 200, 401, 403, 404, 422, 503
