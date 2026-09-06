# テーブル仕様: recipeweave.media_asset

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

教育用動画等の版

定義元: `database/migrations/002_relational_schema.sql:statement-334`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| operation_id | uuid | 不可 | なし | なし | 説明する標準動作 |
| media_type | text | 不可 | なし | LENGTH(BTRIM(media_type)) BETWEEN 1 AND 20000; media_type IN ('video', 'animation', 'image') | 動画/アニメ/画像 |
| uri | text | 不可 | なし | LENGTH(BTRIM(uri)) BETWEEN 1 AND 20000 | オブジェクト格納先 |
| sha256 | char(64) | 不可 | なし | sha256 IS NULL OR sha256 ~ '^[0-9a-f]{64}$' | 資産ハッシュ |
| locale | text | 不可 | なし | LENGTH(BTRIM(locale)) BETWEEN 1 AND 20000 | 字幕言語 |
| version | integer | 不可 | なし | version &gt; 0 | 媒体版 |
| parameter_contract | jsonb | 不可 | なし | parameter_contract IS NULL OR PG_COLUMN_SIZE(parameter_contract) &lt;= 1048576 | 対応厚み・食材形状・視点 |
| source_id | uuid | 不可 | なし | なし | 権利・作成根拠 |
| validation | text | 不可 | なし | LENGTH(BTRIM(validation)) BETWEEN 1 AND 20000; validation IN ('pending', 'passed', 'failed', 'needs_review') | 内容検証 |

## 表制約

- `CHECK (version > 0)`
- `CHECK (LENGTH(BTRIM(media_type)) BETWEEN 1 AND 20000)`
- `CHECK (media_type IN ('video', 'animation', 'image'))`
- `CHECK (LENGTH(BTRIM(uri)) BETWEEN 1 AND 20000)`
- `CHECK (sha256 IS NULL OR sha256 ~ '^[0-9a-f]{64}$')`
- `CHECK (LENGTH(BTRIM(locale)) BETWEEN 1 AND 20000)`
- `CHECK (parameter_contract IS NULL OR PG_COLUMN_SIZE(parameter_contract) <= 1048576)`
- `CHECK (LENGTH(BTRIM(validation)) BETWEEN 1 AND 20000)`
- `CHECK (validation IN ('pending', 'passed', 'failed', 'needs_review'))`
- `UNIQUE (operation_id, locale, version, media_type)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_media_asset_operation_id | False | (operation_id) |
| ix_media_asset_source_id | False | (source_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_media_asset_operation_id | operation_id | operation(id) | RESTRICT | RESTRICT | True |
| fk_media_asset_source_id | source_id | source_record(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 表示

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_media_asset_create | C | backend/src/app/apis/entities/media_asset_create/sql/001_create.sql |
| entity_media_asset_get | R | backend/src/app/apis/entities/media_asset_get/sql/001_get.sql |
| entity_media_asset_list | R | backend/src/app/apis/entities/media_asset_list/sql/001_list.sql |
