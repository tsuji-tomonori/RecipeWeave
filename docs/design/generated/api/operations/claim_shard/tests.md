# 要因別単体テスト仕様: claim_shard

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

| 要因 | Given: 前提 | When: 操作 | Then: 期待結果 | 実在テストnode |
|---|---|---|---|---|
| ワーカー認可 | 一般利用者 | リース操作を要求 | SQL前に403 | backend/tests/test_entity_generation.py::test_generation_lease_requires_admin |
| ワーカーフェンス | 有効な所有者・フェンスに一致する行なし | リース操作を要求 | 409を返し変更なし | backend/tests/test_entity_generation.py::test_expired_or_superseded_lease_is_conflict |

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

対象URLを直接呼ぶテストなし。間接的な検証は検証記録を参照する。

宣言応答: 200, 401, 403, 409, 422, 503
