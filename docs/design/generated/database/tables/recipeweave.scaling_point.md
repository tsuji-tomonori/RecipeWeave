# テーブル仕様: recipeweave.scaling_point

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

検証済み換算点

定義元: `database/migrations/002_relational_schema.sql:statement-218`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| rule_id | uuid | 不可 | なし | なし | 曲線規則 |
| servings | numeric(20,6) | 不可 | なし | servings &gt; 0; servings IS NULL OR servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 人数 |
| multiplier | numeric(20,6) | 不可 | なし | multiplier &gt; 0; multiplier IS NULL OR multiplier::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 登録量への倍率 |

## 表制約

- `CHECK (servings > 0)`
- `CHECK (multiplier > 0)`
- `CHECK (servings IS NULL OR servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (multiplier IS NULL OR multiplier::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `UNIQUE (rule_id, servings)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_scaling_point_rule_id | False | (rule_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_scaling_point_rule_id | rule_id | scaling_rule(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 数量

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_scaling_point_create | C | backend/src/app/apis/entities/scaling_point_create/sql/001_create.sql |
| entity_scaling_point_get | R | backend/src/app/apis/entities/scaling_point_get/sql/001_get.sql |
| entity_scaling_point_list | R | backend/src/app/apis/entities/scaling_point_list/sql/001_list.sql |
