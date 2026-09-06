# インターフェース: entity_media_asset_get

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/entities/media_asset/{row_id}` — 教育用動画等の版の取得

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

MediaAssetRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| locale | string | 必須 | minLength=1; maxLength=20000 | 字幕言語 |
| media_type | string | 必須 | enum=["video", "animation", "image"] | 動画/アニメ/画像 |
| operation_id | string (uuid) | 必須 | 追加制約なし | 説明する標準動作 |
| parameter_contract | MediaParameters-Output | 必須 | 追加制約なし | 対応厚み・食材形状・視点 |
| sha256 | string | 必須 | minLength=64; maxLength=64 | 資産ハッシュ |
| source_id | string (uuid) | 必須 | 追加制約なし | 権利・作成根拠 |
| uri | string | 必須 | minLength=1; maxLength=20000 | オブジェクト格納先 |
| validation | string | 必須 | enum=["pending", "passed", "failed", "needs_review"] | 内容検証 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 媒体版 |

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
"""教育用動画等の版の取得。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_media_asset_get"
TABLE = "media_asset"
ACTION = "get"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "教育用動画等の版の取得。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_media_asset_get",
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
            "$ref": "#/components/schemas/MediaAssetRow"
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
  "summary": "教育用動画等の版の取得",
  "tags": [
    "正規化データ: 教育用動画等の版"
  ]
}
```
