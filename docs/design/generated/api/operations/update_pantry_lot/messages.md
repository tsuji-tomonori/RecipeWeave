# ログメッセージ: update_pantry_lot

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

実logger呼出を抽出する。HTTPのエラー本文や架空のログを、実装ログとして数えない。共有サービスのログはその経路を通る操作へ帰属させる。

対象のrouter・functions・共有操作サービスには、実装されたログ出力がない。

[詳細設計](detail.md) / [エラー応答](interface.md)
