# テーブル仕様: recipeweave.schema_migrations

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

移行IDとchecksum、完了時刻を保持する運用台帳。DDLの構造確認が成功した後に記録し、アプリAPIから更新しない。

定義元: `database/migrate.py:121`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | TEXT | 不可 | なし | PRIMARY KEY | 適用したマイグレーションの一意なID。 |
| checksum | TEXT | 不可 | なし | NOT NULL | 移行SQLと事後確認SQLのSHA-256。適用済み内容の変更を検出する。 |
| applied_at | TIMESTAMPTZ | 不可 | なし | NOT NULL | 移行台帳の登録時刻。DDLと別のトランザクションで記録する。 |

## 表制約

列制約以外の追加制約なし。

## 索引

独立索引なし。主キー・一意制約の索引は表制約を参照。

## 外部キー

外部キーなし。

保持・所属領域: 未指定 / 共通

## 利用API

APIからのアクセスなし。運用上の用途・旧表の保持は定義元を参照する。
