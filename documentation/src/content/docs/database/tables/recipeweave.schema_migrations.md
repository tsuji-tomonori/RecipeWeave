---
title: "テーブル仕様: recipeweave.schema_migrations"
---

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

移行IDとchecksum、完了時刻を保持する運用台帳。DDLの構造確認が成功した後に記録し、アプリAPIから更新しない。

定義元: `database/migrate.py:117`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | TEXT | 不可 | なし | PRIMARY KEY | 適用したマイグレーションの一意なID。 |
| checksum | TEXT | 不可 | なし | NOT NULL | 移行SQLと事後確認SQLのSHA-256。適用済み内容の変更を検出する。 |
| applied_at | TIMESTAMPTZ | 不可 | なし | NOT NULL | 移行台帳の登録時刻。DDLと別のトランザクションで記録する。 |

## 表制約

列制約以外の追加制約なし。

## 利用API

APIからのアクセスなし。マイグレーション実行時のみ利用する。
