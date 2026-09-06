# テーブル仕様: recipeweave.food_identity_member

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

購買食品から同一性への対応

定義元: `database/migrations/002_relational_schema.sql:statement-618`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変ID |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時 |
| food_id | uuid | 不可 | なし | なし | 元の食品 |
| identity_id | uuid | 不可 | なし | なし | 同一性ID |
| normalizer_version | text | 不可 | なし | LENGTH(BTRIM(normalizer_version)) BETWEEN 1 AND 20000 | 正規化器版 |
| reason | text | 不可 | なし | LENGTH(BTRIM(reason)) BETWEEN 1 AND 20000 | 同一視の理由 |

## 表制約

- `CHECK (LENGTH(BTRIM(normalizer_version)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(reason)) BETWEEN 1 AND 20000)`
- `UNIQUE (food_id, normalizer_version)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_food_identity_member_food_id | False | (food_id) |
| ix_food_identity_member_identity_id | False | (identity_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_food_identity_member_food_id | food_id | food(id) | RESTRICT | RESTRICT | True |
| fk_food_identity_member_identity_id | identity_id | food_identity(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 大規模生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_food_identity_member_create | C | backend/src/app/apis/entities/food_identity_member_create/sql/001_create.sql |
| entity_food_identity_member_get | R | backend/src/app/apis/entities/food_identity_member_get/sql/001_get.sql |
| entity_food_identity_member_list | R | backend/src/app/apis/entities/food_identity_member_list/sql/001_list.sql |
