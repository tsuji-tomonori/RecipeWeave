# インターフェース: entity_recipe_search_document_get

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/entities/recipe_search_document/{row_id}` — 公開検索用文書の取得

## 認証

[{"HTTPBearer": []}]

宣言: bearer

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| path | row_id | 必須 | string (uuid) | 追加制約なし |  |

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

RecipeSearchDocumentRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時 |
| display_title | string | 必須 | minLength=1; maxLength=20000 | 表示タイトル |
| eligible | boolean | 必須 | 追加制約なし | 公開可能か |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| facet_option_ids | array&lt;string (uuid)&gt; | 必須 | maxItems=1024 | 料理・味等の検索軸 |
| food_identity_ids | array&lt;string (uuid)&gt; | 必須 | maxItems=1024 | 検索用食品ID集合 |
| id | string (uuid) | 必須 | 追加制約なし | 不変ID |
| projected_at | string (date-time) | 必須 | 追加制約なし | 更新時点 |
| projection_version | string | 必須 | minLength=1; maxLength=20000 | 検索文書の生成器版 |
| published_version_id | string (uuid) | 必須 | 追加制約なし | 検索対象の公開版 |
| recipe_id | string (uuid) | 必須 | 追加制約なし | 同一性単位で1件 |
| search_text | string | 必須 | minLength=1; maxLength=20000 | 検索用本文 |
| source_hash | string | 必須 | minLength=64; maxLength=64 | 正本一致確認 |

### HTTP 401: 認証が必要

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 403: 操作・参照権限なし

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 404: 対象なし

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
"""公開検索用文書の取得。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_recipe_search_document_get"
TABLE = "recipe_search_document"
ACTION = "get"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "公開検索用文書の取得。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_recipe_search_document_get",
  "parameters": [
    {
      "in": "path",
      "name": "row_id",
      "required": true,
      "schema": {
        "format": "uuid",
        "title": "Row Id",
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/RecipeSearchDocumentRow"
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
    "404": {
      "description": "対象なし"
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
  "summary": "公開検索用文書の取得",
  "tags": [
    "正規化データ: 公開検索用文書"
  ]
}
```
