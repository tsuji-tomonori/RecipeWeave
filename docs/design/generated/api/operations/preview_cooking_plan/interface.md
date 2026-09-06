# インターフェース: preview_cooking_plan

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/cooking-plan` — 保存せずに調理の段取りを確認する

## 認証

[{"HTTPBearer": []}]

宣言: 検証済みBearerトークンと本人所有権

## パラメーター

なし。

## リクエスト本文

必須

### application/json

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| durationEstimates | array&lt;DurationEstimate&gt; | 任意 | maxItems=500 | Durationestimates |
| items | array&lt;MealItem&gt; | 必須 | minItems=1; maxItems=50 | Items |

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

PlanResponse

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| plan | array&lt;PlannedStep&gt; | 必須 | 追加制約なし | Plan |

### HTTP 401: 認証・版・分量・設備・工程の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 403: 認証・版・分量・設備・工程の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 404: 認証・版・分量・設備・工程の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 422: 認証・版・分量・設備・工程の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 503: 認証・版・分量・設備・工程の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

## 操作のサンプル

```python
SUCCESS = {"説明": "planにDBの料理版と本人の設備で計算した工程を返す。保存や在庫控除は行わない。"}
ERRORS = {401: {"detail": "ログインが必要です"}, 422: {"detail": "この人数の工程時間が未確認です"}}
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "実際の調理開始と同じ規則で、表示する段取りを計算する。",
  "operationId": "preview_cooking_plan",
  "parameters": [],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/PlanRequest"
        }
      }
    },
    "required": true
  },
  "responses": {
    "200": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/PlanResponse"
          }
        }
      },
      "description": "Successful Response"
    },
    "401": {
      "description": "認証・版・分量・設備・工程の検証失敗"
    },
    "403": {
      "description": "認証・版・分量・設備・工程の検証失敗"
    },
    "404": {
      "description": "認証・版・分量・設備・工程の検証失敗"
    },
    "422": {
      "description": "認証・版・分量・設備・工程の検証失敗"
    },
    "503": {
      "description": "認証・版・分量・設備・工程の検証失敗"
    }
  },
  "security": [
    {
      "HTTPBearer": []
    }
  ],
  "summary": "保存せずに調理の段取りを確認する",
  "tags": [
    "利用者の操作"
  ]
}
```
