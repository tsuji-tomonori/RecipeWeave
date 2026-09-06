# ログメッセージ: entity_compatibility_rule_list

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

実logger呼出を抽出する。HTTPのエラー本文や架空のログを、実装ログとして数えない。共有サービスのログはその経路を通る操作へ帰属させる。

| レベル | メッセージ・イベント | 構造化項目 | 発生関数 | 実装位置 |
|---|---|---|---|---|
| WARNING | entity_operation_rejected | extra={'operation_id': spec.operation_id} | EntityService.execute | backend/src/app/core/entity_service.py:50 |
| INFO | entity_operation_completed | extra={'operation_id': spec.operation_id, 'table': spec.table, 'action': spec.action, 'row_count': len(rows)} | EntityService.execute | backend/src/app/core/entity_service.py:106 |
| WARNING | entity_operation_rejected | extra={'operation_id': spec.operation_id, 'sqlstate': exc.sqlstate} | EntityService.execute | backend/src/app/core/entity_service.py:117 |

[詳細設計](detail.md) / [エラー応答](interface.md)
