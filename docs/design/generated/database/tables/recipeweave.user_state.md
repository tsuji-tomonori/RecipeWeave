# テーブル仕様: recipeweave.user_state

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

認証済み利用者ごとに、検証済みの端末状態とサーバー側の版を保持する。レシピ正規化DBの将来設計とは別の、Dev同期用の物理テーブル。

定義元: `database/migrations/001_user_state.sql`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| subject | TEXT | 不可 | なし | PRIMARY KEY | 検証済みCognitoアクセストークンのsub。呼出者から任意の利用者IDを受け取らない。 |
| revision | BIGINT | 不可 | なし | NOT NULL | サーバー側の楽観ロック用の版。新規は1、更新は期待版に一致するときだけ1増える。 |
| payload | JSONB | 不可 | なし | NOT NULL | AppSnapshotの検証を通ったJSON状態。画像、OCR全文、トークン等は格納しない。内部の版とサーバーrevisionは別に扱う。 |
| updated_at | TIMESTAMPTZ | 不可 | なし | NOT NULL | SQLのCURRENT_TIMESTAMPで記録する作成・更新時刻。 |

## 表制約

列制約以外の追加制約なし。

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| get_state | R | backend/src/app/apis/state/get_state/sql/001_select_state.sql |
| put_state | C | backend/src/app/apis/state/put_state/sql/001_insert_state.sql |
| put_state | U | backend/src/app/apis/state/put_state/sql/002_update_state.sql |
