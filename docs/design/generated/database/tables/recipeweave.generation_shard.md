# テーブル仕様: recipeweave.generation_shard

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

列挙範囲・リース管理

定義元: `database/migrations/002_relational_schema.sql:statement-636`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変ID |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時 |
| template_id | uuid | 不可 | なし | なし | テンプレート版 |
| start_ordinal | bigint | 不可 | なし | start_ordinal &gt;= 0; end_ordinal &gt; start_ordinal; next_ordinal &gt;= start_ordinal AND next_ordinal &lt;= end_ordinal | 開始序数 |
| end_ordinal | bigint | 不可 | なし | end_ordinal &gt; start_ordinal; next_ordinal &gt;= start_ordinal AND next_ordinal &lt;= end_ordinal; state &lt;&gt; 'done' OR next_ordinal = end_ordinal | 終了序数（排他的） |
| next_ordinal | bigint | 不可 | なし | next_ordinal &gt;= start_ordinal AND next_ordinal &lt;= end_ordinal; state &lt;&gt; 'done' OR next_ordinal = end_ordinal | 再開位置 |
| lease_owner | text | 可 | なし | (lease_owner IS NULL) = (lease_expires_at IS NULL); state &lt;&gt; 'running' OR lease_owner IS NOT NULL | ワーカー識別子 |
| lease_expires_at | timestamptz | 可 | なし | (lease_owner IS NULL) = (lease_expires_at IS NULL) | 有効期限 |
| fence_token | bigint | 不可 | なし | fence_token &gt;= 0 | 古い所有者の書込みを拒否 |
| state | text | 不可 | なし | state &lt;&gt; 'running' OR lease_owner IS NOT NULL; state &lt;&gt; 'done' OR next_ordinal = end_ordinal; LENGTH(BTRIM(state)) BETWEEN 1 AND 20000; state IN ('queued', 'running', 'done', 'failed') | 待機/実行/完了/停止 |

## 表制約

- `CHECK (start_ordinal >= 0)`
- `CHECK (end_ordinal > start_ordinal)`
- `CHECK (next_ordinal >= start_ordinal AND next_ordinal <= end_ordinal)`
- `CHECK (fence_token >= 0)`
- `CHECK ((lease_owner IS NULL) = (lease_expires_at IS NULL))`
- `CHECK (state <> 'running' OR lease_owner IS NOT NULL)`
- `CHECK (state <> 'done' OR next_ordinal = end_ordinal)`
- `CHECK (LENGTH(BTRIM(state)) BETWEEN 1 AND 20000)`
- `CHECK (state IN ('queued', 'running', 'done', 'failed'))`
- `UNIQUE (template_id, start_ordinal)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_generation_shard_template_id | False | (template_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_generation_shard_template_id | template_id | generation_template(id) | RESTRICT | RESTRICT | True |

保持・所属領域: transient / 大規模生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_generation_shard_create | C | backend/src/app/apis/entities/generation_shard_create/sql/001_create.sql |
| entity_generation_shard_get | R | backend/src/app/apis/entities/generation_shard_get/sql/001_get.sql |
| entity_generation_shard_list | R | backend/src/app/apis/entities/generation_shard_list/sql/001_list.sql |
| advance_shard | U | backend/src/app/apis/generation/advance_shard/sql/001_execute.sql |
| claim_shard | R,U | backend/src/app/apis/generation/claim_shard/sql/001_execute.sql |
| renew_shard | U | backend/src/app/apis/generation/renew_shard/sql/001_execute.sql |
