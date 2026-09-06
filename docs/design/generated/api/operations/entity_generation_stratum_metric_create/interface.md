# インターフェース: entity_generation_stratum_metric_create

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/entities/generation_stratum_metric` — 採用率・飽和度の実測の作成

## 認証

[{"HTTPBearer": []}]

宣言: bearer

## パラメーター

なし。

## リクエスト本文

必須

### application/json

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| attempted | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 試行数 |
| cost_amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 同一通貨の費用 |
| currency | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=3; maxLength=3 | JPY/USD等 |
| input_tokens | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 入力トークン合計 |
| output_tokens | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 出力トークン合計 |
| publishable | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 公開基準通過数 |
| stratum_key | string | 必須 | minLength=1; maxLength=20000 | 層の安定キー(料理構造x食品カテゴリx入手性)。集計定義はテンプレート版に固定 |
| template_id | string (uuid) | 必須 | 追加制約なし | 対象テンプレート |
| unique_count | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 既存集合との差分数 |
| valid | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 適合生成数 |
| window_end | string (date-time) | 必須 | 追加制約なし | 計測窓終了 |
| window_start | string (date-time) | 必須 | 追加制約なし | 計測窓開始 |

## レスポンス

### HTTP 201: Successful Response

Content-Type: `application/json`

GenerationStratumMetricRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| attempted | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 試行数 |
| cost_amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 同一通貨の費用 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時 |
| currency | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=3; maxLength=3 | JPY/USD等 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変ID |
| input_tokens | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 入力トークン合計 |
| output_tokens | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 出力トークン合計 |
| publishable | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 公開基準通過数 |
| stratum_key | string | 必須 | minLength=1; maxLength=20000 | 層の安定キー(料理構造x食品カテゴリx入手性)。集計定義はテンプレート版に固定 |
| template_id | string (uuid) | 必須 | 追加制約なし | 対象テンプレート |
| unique_count | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 既存集合との差分数 |
| valid | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 適合生成数 |
| window_end | string (date-time) | 必須 | 追加制約なし | 計測窓終了 |
| window_start | string (date-time) | 必須 | 追加制約なし | 計測窓開始 |

### HTTP 401: 認証が必要

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 403: 操作・参照権限なし

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 409: 同時更新またはDB業務制約違反

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 422: 入力不正

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 503: DB接続不可

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

## 操作のサンプル

```python
# generate_entity_apis.py による自動生成。直接編集しない。
"""採用率・飽和度の実測の作成。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_generation_stratum_metric_create"
TABLE = "generation_stratum_metric"
ACTION = "create"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "採用率・飽和度の実測の作成。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_generation_stratum_metric_create",
  "parameters": [],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/GenerationStratumMetricWrite"
        }
      }
    },
    "required": true
  },
  "responses": {
    "201": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/GenerationStratumMetricRow"
          }
        }
      },
      "description": "Successful Response"
    },
    "401": {
      "description": "認証が必要"
    },
    "403": {
      "description": "操作・参照権限なし"
    },
    "409": {
      "description": "同時更新またはDB業務制約違反"
    },
    "422": {
      "description": "入力不正"
    },
    "503": {
      "description": "DB接続不可"
    }
  },
  "security": [
    {
      "HTTPBearer": []
    }
  ],
  "summary": "採用率・飽和度の実測の作成",
  "tags": [
    "正規化データ: 採用率・飽和度の実測"
  ]
}
```
