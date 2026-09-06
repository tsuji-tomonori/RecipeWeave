# 詳細設計: local_login

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/auth/local-login` — 開発環境へログインする

## 入力と処理前提

| 項目 | 仕様 |
|---|---|
| authentication | public; 開発環境限定。本文の資格情報を検証 |
| idempotency | 新しい期限のアクセストークンを発行する |
| transaction | 要求のPostgreSQLトランザクション |
| effects | 本人の開発用トークンを発行 |

| 入力場所 | 名前 | 型 | 必須 |
|---|---|---|---|

### 本文: application/json

| 入力 | 型 | 必須 | 制約 | 意味 |
|---|---|---|---|---|
| password | string | 必須 | minLength=1; maxLength=200 | Password |
| username | string | 必須 | minLength=1; maxLength=50 | Username |

## データベースの対象と値の流れ

この操作に属するSQLはない。永続化を行う処理は下記の関数責務と依存ポートで確認する。

## 分岐・拒否条件

| 判定条件 | 例外・応答 | 定義元 |
|---|---|---|

## 出力

| 関数 | 返却式 | 定義元 |
|---|---|---|
| handle | execute(request) | backend/src/app/apis/auth/local_login/router.py:17 |
| execute | local_login(request) | backend/src/app/apis/auth/local_login/functions.py:4 |

APIとして返す型・status・headerは [インターフェース](interface.md) の実OpenAPIを参照。

## 責務

| 関数 | 処理 | 定義元 |
|---|---|---|
| handle | 開発環境へログインする。 | backend/src/app/apis/auth/local_login/router.py:17 |
| execute | 開発環境へログインする。秘密情報はログへ出力しない。 | backend/src/app/apis/auth/local_login/functions.py:4 |

[SQL](queries.md) / [シーケンス](sequence.md) / [ログ](messages.md) / [要因別テスト](tests.md)
