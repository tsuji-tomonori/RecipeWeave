# テーブル仕様: recipeweave.user_state

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

旧Devスナップショット。移行履歴専用でサービスのデータ正本には使用しない

定義元: `database/migrations/001_user_state.sql:statement-1`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| subject | text | 不可 | なし | PRIMARY KEY |  |
| revision | bigint | 不可 | なし | なし |  |
| payload | jsonb | 不可 | なし | なし |  |
| updated_at | timestamptz | 不可 | なし | なし |  |

## 表制約

- `PRIMARY KEY (subject)`

## 索引

独立索引なし。主キー・一意制約の索引は表制約を参照。

## 外部キー

外部キーなし。

保持・所属領域: legacy / 移行互換

## 利用API

APIからのアクセスなし。運用上の用途・旧表の保持は定義元を参照する。
