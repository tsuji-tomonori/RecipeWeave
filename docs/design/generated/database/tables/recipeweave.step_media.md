# テーブル仕様: recipeweave.step_media

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

工程別メディア選択

定義元: `database/migrations/002_relational_schema.sql:statement-347`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| step_id | uuid | 不可 | なし | なし | 対象工程 |
| media_id | uuid | 不可 | なし | なし | 適用メディア |
| start_ms | integer | 不可 | なし | start_ms &gt;= 0; end_ms &gt; start_ms | 表示開始点 |
| end_ms | integer | 不可 | なし | end_ms &gt; start_ms | 終了点 |

## 表制約

- `CHECK (start_ms >= 0)`
- `CHECK (end_ms > start_ms)`
- `UNIQUE (step_id, media_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_step_media_step_id | False | (step_id) |
| ix_step_media_media_id | False | (media_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_step_media_step_id | step_id | recipe_step(id) | RESTRICT | RESTRICT | True |
| fk_step_media_media_id | media_id | media_asset(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 表示

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_step_media_create | C | backend/src/app/apis/entities/step_media_create/sql/001_create.sql |
| entity_step_media_get | R | backend/src/app/apis/entities/step_media_get/sql/001_get.sql |
| entity_step_media_list | R | backend/src/app/apis/entities/step_media_list/sql/001_list.sql |
| entity_step_media_update | U | backend/src/app/apis/entities/step_media_update/sql/001_update.sql |
