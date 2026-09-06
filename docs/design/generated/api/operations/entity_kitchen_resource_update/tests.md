# 要因別単体テスト仕様: entity_kitchen_resource_update

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

| 要因 | Given: 前提 | When: 操作 | Then: 期待結果 | 実在テストnode |
|---|---|---|---|---|
| 更新条件欠落 | 行版ヘッダーなし | 更新または削除を呼ぶ | SQL前に428 | backend/tests/test_entity_api.py::test_mutation_requires_if_match |
| 楽観競合 | 要求した行版に一致する行がない | 更新または削除を呼ぶ | 409を返し監査を追記しない | backend/tests/test_entity_api.py::test_stale_update_is_conflict |

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

対象URLを直接呼ぶテストなし。間接的な検証は検証記録を参照する。

宣言応答: 200, 401, 403, 409, 422, 428, 503
