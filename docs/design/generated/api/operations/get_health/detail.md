# 詳細設計: get_health

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/health` — 稼働状況とサンプル公開範囲

## 入力と処理前提

| 項目 | 仕様 |
|---|---|
| authentication | public |
| idempotency | 読取専用 |
| transaction | なし |
| effects | なし |

| 入力場所 | 名前 | 型 | 必須 |
|---|---|---|---|

## データベースの対象と値の流れ

この操作に属するSQLはない。永続化を行う処理は下記の関数責務と依存ポートで確認する。

## 分岐・拒否条件

| 判定条件 | 例外・応答 | 定義元 |
|---|---|---|

## 出力

| 関数 | 返却式 | 定義元 |
|---|---|---|
| get_health | api_functions.get_health() | backend/src/app/apis/health/get_health/router.py:11 |
| get_health | HealthResponse() | backend/src/app/apis/health/get_health/functions.py:4 |

APIとして返す型・status・headerは [インターフェース](interface.md) の実OpenAPIを参照。

## 責務

| 関数 | 処理 | 定義元 |
|---|---|---|
| get_health | 個別説明なし | backend/src/app/apis/health/get_health/router.py:11 |
| get_health | AWSへの配備やカタログの網羅性を示唆せず、このAPIの状態を返す。 | backend/src/app/apis/health/get_health/functions.py:4 |

[SQL](queries.md) / [シーケンス](sequence.md) / [ログ](messages.md) / [要因別テスト](tests.md)
