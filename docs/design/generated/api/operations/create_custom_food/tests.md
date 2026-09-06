# 要因別単体テスト仕様: create_custom_food

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

要因別の明示対応は未登録。下の実URL試験のみを静的に確認できる。

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_backup_database.py::test_backup_database_round_trip_preserves_complete_rows_and_decimal | Given私有食品・未知数量・正確な小数 When確認後復元 Then全列同値で共有/別人不変。 | assert custom.status_code == 200, custom.text / assert option / assert confirmation['expectedVersion'] == changed['version'] / assert len(confirmation['counts']) == 34 / assert state(client) == changed / assert response.status_code == 200, response.text / assert response.json()['version'] == changed['version'] + 1 / assert after['tables'] == original['tables'] / assert after['profile'] == original['profile'] / assert any((row['amount'] is None for row in after['tables']['pantry_lot'])) / assert row['weight'] == str(exact) / assert actual and actual['weight'] == exact / assert export(client, 'bob')['tables'] == other_before['tables'] / assert db.execute('SELECT id, title, status FROM recipeweave.recipe ORDER BY id').fetchall() == catalog_before |

宣言応答: 200, 401, 403, 404, 409, 422, 503
