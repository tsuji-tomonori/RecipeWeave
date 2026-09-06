# インターフェース: get_health

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/health` — 稼働状況とサンプル公開範囲

## 認証

[]

宣言: public

## パラメーター

なし。

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

HealthResponse

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| catalog | string | 任意 | const="sample"; default="sample" | Catalog |
| cloudSync | string | 任意 | const="not-deployed"; default="not-deployed" | Cloudsync |
| status | string | 任意 | const="ok"; default="ok" | Status |

## 操作のサンプル

```python
SUCCESS = {"status": "ok", "catalog": "sample", "cloudSync": "not-deployed"}
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "operationId": "get_health",
  "parameters": [],
  "responses": {
    "200": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/HealthResponse"
          }
        }
      },
      "description": "Successful Response"
    }
  },
  "summary": "稼働状況とサンプル公開範囲"
}
```
