# テーブル仕様: recipeweave.generation_stratum_metric

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

採用率・飽和度の実測

定義元: `database/migrations/002_relational_schema.sql:statement-683`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変ID |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時 |
| template_id | uuid | 不可 | なし | なし | 対象テンプレート |
| window_start | timestamptz | 不可 | なし | window_start &lt; window_end | 計測窓開始 |
| window_end | timestamptz | 不可 | なし | window_start &lt; window_end | 計測窓終了 |
| attempted | bigint | 不可 | なし | attempted &gt;= 0; valid &gt;= 0 AND valid &lt;= attempted | 試行数 |
| valid | bigint | 不可 | なし | valid &gt;= 0 AND valid &lt;= attempted; unique_count &gt;= 0 AND unique_count &lt;= valid | 適合生成数 |
| unique_count | bigint | 不可 | なし | unique_count &gt;= 0 AND unique_count &lt;= valid; publishable &gt;= 0 AND publishable &lt;= unique_count | 既存集合との差分数 |
| publishable | bigint | 不可 | なし | publishable &gt;= 0 AND publishable &lt;= unique_count | 公開基準通過数 |
| input_tokens | bigint | 不可 | なし | input_tokens &gt;= 0 | 入力トークン合計 |
| output_tokens | bigint | 不可 | なし | output_tokens &gt;= 0 | 出力トークン合計 |
| cost_amount | numeric(20,6) | 可 | なし | cost_amount IS NULL OR cost_amount &gt;= 0; (cost_amount IS NULL) = (currency IS NULL); cost_amount IS NULL OR cost_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 同一通貨の費用 |
| currency | char(3) | 可 | なし | (cost_amount IS NULL) = (currency IS NULL); currency IS NULL OR currency ~ '^[A-Z]{3}$' | JPY/USD等 |
| stratum_key | text | 不可 | なし | LENGTH(BTRIM(stratum_key)) BETWEEN 1 AND 20000 | 層の安定キー（料理構造×食品カテゴリ×入手性）。集計定義はテンプレート版に固定 |

## 表制約

- `CHECK (window_start < window_end)`
- `CHECK (attempted >= 0)`
- `CHECK (valid >= 0 AND valid <= attempted)`
- `CHECK (unique_count >= 0 AND unique_count <= valid)`
- `CHECK (publishable >= 0 AND publishable <= unique_count)`
- `CHECK (input_tokens >= 0)`
- `CHECK (output_tokens >= 0)`
- `CHECK (cost_amount IS NULL OR cost_amount >= 0)`
- `CHECK ((cost_amount IS NULL) = (currency IS NULL))`
- `CHECK (currency IS NULL OR currency ~ '^[A-Z]{3}$')`
- `CHECK (cost_amount IS NULL OR cost_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (LENGTH(BTRIM(stratum_key)) BETWEEN 1 AND 20000)`
- `UNIQUE (template_id, stratum_key, window_start, window_end)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_generation_stratum_metric_template_id | False | ( template_id ) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_generation_stratum_metric_template_id | template_id | generation_template(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 大規模生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_generation_stratum_metric_create | C | backend/src/app/apis/entities/generation_stratum_metric_create/sql/001_create.sql |
| entity_generation_stratum_metric_get | R | backend/src/app/apis/entities/generation_stratum_metric_get/sql/001_get.sql |
| entity_generation_stratum_metric_list | R | backend/src/app/apis/entities/generation_stratum_metric_list/sql/001_list.sql |
