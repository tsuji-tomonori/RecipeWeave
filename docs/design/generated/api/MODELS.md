# 共有モデル・enum・制約

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## AllergenRow

アレルゲン概念のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | 固定コード |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| name | string | 必須 | minLength=1; maxLength=20000 | 名称 |
| source_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 分類出典 |

```json
{
  "additionalProperties": false,
  "description": "アレルゲン概念のDB応答。",
  "properties": {
    "code": {
      "description": "固定コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "name": {
      "description": "名称",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "source_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "分類出典",
      "title": "Source Id"
    }
  },
  "required": [
    "id",
    "created_at",
    "code",
    "name",
    "source_id",
    "etag"
  ],
  "title": "AllergenRow",
  "type": "object"
}
```

## AllergenWrite

アレルゲン概念の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | 固定コード |
| name | string | 必須 | minLength=1; maxLength=20000 | 名称 |
| source_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 分類出典 |

```json
{
  "additionalProperties": false,
  "description": "アレルゲン概念の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "code": {
      "description": "固定コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "name": {
      "description": "名称",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "source_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "分類出典",
      "title": "Source Id"
    }
  },
  "required": [
    "code",
    "name"
  ],
  "title": "AllergenWrite",
  "type": "object"
}
```

## AppSnapshot



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| cooking | anyOf(CookingSession, null) | 必須 | 追加制約なし |  |
| customFoods | array&lt;Food&gt; | 必須 | maxItems=1000 | Customfoods |
| drafts | object | 必須 | additionalProperties={"$ref": "#/components/schemas/RecipeDraft"} | Drafts |
| imports | array&lt;ReceiptImport&gt; | 必須 | maxItems=1000 | Imports |
| lots | array&lt;StockLot&gt; | 必須 | maxItems=5000 | Lots |
| meal | array&lt;MealItem&gt; | 必須 | maxItems=50 | Meal |
| saved | array&lt;string&gt; | 必須 | maxItems=10000; 要素の制約=minLength=1; maxLength=128 | Saved |
| schemaVersion | integer | 必須 | const=1 | Schemaversion |
| search | SearchFilters | 必須 | 追加制約なし |  |
| settings | Settings | 必須 | 追加制約なし |  |
| shoppingChecks | array&lt;ShoppingCheck&gt; | 必須 | maxItems=1000 | Shoppingchecks |
| version | integer | 必須 | minimum=0.0 | Version |

```json
{
  "additionalProperties": false,
  "properties": {
    "cooking": {
      "anyOf": [
        {
          "$ref": "#/components/schemas/CookingSession"
        },
        {
          "type": "null"
        }
      ]
    },
    "customFoods": {
      "items": {
        "$ref": "#/components/schemas/Food"
      },
      "maxItems": 1000,
      "title": "Customfoods",
      "type": "array"
    },
    "drafts": {
      "additionalProperties": {
        "$ref": "#/components/schemas/RecipeDraft"
      },
      "propertyNames": {
        "maxLength": 128,
        "minLength": 1
      },
      "title": "Drafts",
      "type": "object"
    },
    "imports": {
      "items": {
        "$ref": "#/components/schemas/ReceiptImport"
      },
      "maxItems": 1000,
      "title": "Imports",
      "type": "array"
    },
    "lots": {
      "items": {
        "$ref": "#/components/schemas/StockLot"
      },
      "maxItems": 5000,
      "title": "Lots",
      "type": "array"
    },
    "meal": {
      "items": {
        "$ref": "#/components/schemas/MealItem"
      },
      "maxItems": 50,
      "title": "Meal",
      "type": "array"
    },
    "saved": {
      "items": {
        "maxLength": 128,
        "minLength": 1,
        "type": "string"
      },
      "maxItems": 10000,
      "title": "Saved",
      "type": "array"
    },
    "schemaVersion": {
      "const": 1,
      "title": "Schemaversion",
      "type": "integer"
    },
    "search": {
      "$ref": "#/components/schemas/SearchFilters"
    },
    "settings": {
      "$ref": "#/components/schemas/Settings"
    },
    "shoppingChecks": {
      "items": {
        "$ref": "#/components/schemas/ShoppingCheck"
      },
      "maxItems": 1000,
      "title": "Shoppingchecks",
      "type": "array"
    },
    "version": {
      "minimum": 0.0,
      "title": "Version",
      "type": "integer"
    }
  },
  "required": [
    "schemaVersion",
    "version",
    "lots",
    "imports",
    "drafts",
    "meal",
    "saved",
    "shoppingChecks",
    "cooking",
    "settings",
    "customFoods",
    "search"
  ],
  "title": "AppSnapshot",
  "type": "object"
}
```

## AppUserRow

アプリ利用者のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| auth_subject | string | 必須 | minLength=1; maxLength=20000 | 認証基盤の不透明識別子 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| locale | string | 必須 | minLength=1; maxLength=20000 | 表示言語 |
| state | string | 必須 | enum=["active", "erasure_pending"] | 利用/削除処理 |
| timezone | string | 必須 | minLength=1; maxLength=20000 | IANAタイムゾーン |

```json
{
  "additionalProperties": false,
  "description": "アプリ利用者のDB応答。",
  "properties": {
    "auth_subject": {
      "description": "認証基盤の不透明識別子",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Auth Subject",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "locale": {
      "description": "表示言語",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Locale",
      "type": "string"
    },
    "state": {
      "description": "利用/削除処理",
      "enum": [
        "active",
        "erasure_pending"
      ],
      "title": "State",
      "type": "string"
    },
    "timezone": {
      "description": "IANAタイムゾーン",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Timezone",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "auth_subject",
    "state",
    "locale",
    "timezone",
    "etag"
  ],
  "title": "AppUserRow",
  "type": "object"
}
```

## AppUserWrite

アプリ利用者の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| locale | string | 必須 | minLength=1; maxLength=20000 | 表示言語 |
| timezone | string | 必須 | minLength=1; maxLength=20000 | IANAタイムゾーン |

```json
{
  "additionalProperties": false,
  "description": "アプリ利用者の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "locale": {
      "description": "表示言語",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Locale",
      "type": "string"
    },
    "timezone": {
      "description": "IANAタイムゾーン",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Timezone",
      "type": "string"
    }
  },
  "required": [
    "locale",
    "timezone"
  ],
  "title": "AppUserWrite",
  "type": "object"
}
```

## AuditEventRow

変更・公開監査のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| action | string | 必須 | minLength=1; maxLength=20000 | publish/withdraw/erase等 |
| actor_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 実行者(削除時匿名化) |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| entity_key_hash | string | 必須 | minLength=64; maxLength=64 | 対象識別子のハッシュ |
| entity_type | string | 必須 | minLength=1; maxLength=20000 | 対象テーブルの許可リスト |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| occurred_at | string (date-time) | 必須 | 追加制約なし | 時刻 |
| reason | string | 必須 | minLength=1; maxLength=20000 | 理由(個人情報を含めない) |

```json
{
  "additionalProperties": false,
  "description": "変更・公開監査のDB応答。",
  "properties": {
    "action": {
      "description": "publish/withdraw/erase等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Action",
      "type": "string"
    },
    "actor_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "実行者(削除時匿名化)",
      "title": "Actor Id"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "entity_key_hash": {
      "description": "対象識別子のハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Entity Key Hash",
      "type": "string"
    },
    "entity_type": {
      "description": "対象テーブルの許可リスト",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Entity Type",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "occurred_at": {
      "description": "時刻",
      "format": "date-time",
      "title": "Occurred At",
      "type": "string"
    },
    "reason": {
      "description": "理由(個人情報を含めない)",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Reason",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "actor_id",
    "action",
    "entity_type",
    "entity_key_hash",
    "reason",
    "occurred_at",
    "etag"
  ],
  "title": "AuditEventRow",
  "type": "object"
}
```

## AxisOptionRow

軸候補値のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| axis_id | string (uuid) | 必須 | 追加制約なし | 親軸 |
| code | string | 必須 | minLength=1; maxLength=20000 | 値コード |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| definition | string | 必須 | minLength=1; maxLength=20000 | 値の意味 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| label | string | 必須 | minLength=1; maxLength=500 | 候補名 |
| parent_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 同軸の階層親 |
| status | string | 必須 | enum=["active", "retired"] | 選択可否 |

```json
{
  "additionalProperties": false,
  "description": "軸候補値のDB応答。",
  "properties": {
    "axis_id": {
      "description": "親軸",
      "format": "uuid",
      "title": "Axis Id",
      "type": "string"
    },
    "code": {
      "description": "値コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "definition": {
      "description": "値の意味",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Definition",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "label": {
      "description": "候補名",
      "maxLength": 500,
      "minLength": 1,
      "title": "Label",
      "type": "string"
    },
    "parent_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "同軸の階層親",
      "title": "Parent Id"
    },
    "status": {
      "description": "選択可否",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "axis_id",
    "code",
    "label",
    "definition",
    "parent_id",
    "status",
    "etag"
  ],
  "title": "AxisOptionRow",
  "type": "object"
}
```

## AxisOptionWrite

軸候補値の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| axis_id | string (uuid) | 必須 | 追加制約なし | 親軸 |
| code | string | 必須 | minLength=1; maxLength=20000 | 値コード |
| definition | string | 必須 | minLength=1; maxLength=20000 | 値の意味 |
| label | string | 必須 | minLength=1; maxLength=500 | 候補名 |
| parent_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 同軸の階層親 |
| status | string | 必須 | enum=["active", "retired"] | 選択可否 |

```json
{
  "additionalProperties": false,
  "description": "軸候補値の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "axis_id": {
      "description": "親軸",
      "format": "uuid",
      "title": "Axis Id",
      "type": "string"
    },
    "code": {
      "description": "値コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "definition": {
      "description": "値の意味",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Definition",
      "type": "string"
    },
    "label": {
      "description": "候補名",
      "maxLength": 500,
      "minLength": 1,
      "title": "Label",
      "type": "string"
    },
    "parent_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "同軸の階層親",
      "title": "Parent Id"
    },
    "status": {
      "description": "選択可否",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "axis_id",
    "code",
    "label",
    "definition",
    "status"
  ],
  "title": "AxisOptionWrite",
  "type": "object"
}
```

## AxisRow

組み合わせ軸のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | 軸コード |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| name | string | 必須 | minLength=1; maxLength=20000 | 軸名 |
| purpose | string | 必須 | enum=["generation", "search", "constraint", "derived", "presentation"] | 生成/検索/制約等 |
| release_id | string (uuid) | 必須 | 追加制約なし | 定義版 |
| selection | string | 必須 | enum=["single", "multiple"] | 単複 |
| status | string | 必須 | enum=["active", "retired"] | 採用状態 |

```json
{
  "additionalProperties": false,
  "description": "組み合わせ軸のDB応答。",
  "properties": {
    "code": {
      "description": "軸コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "name": {
      "description": "軸名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "purpose": {
      "description": "生成/検索/制約等",
      "enum": [
        "generation",
        "search",
        "constraint",
        "derived",
        "presentation"
      ],
      "title": "Purpose",
      "type": "string"
    },
    "release_id": {
      "description": "定義版",
      "format": "uuid",
      "title": "Release Id",
      "type": "string"
    },
    "selection": {
      "description": "単複",
      "enum": [
        "single",
        "multiple"
      ],
      "title": "Selection",
      "type": "string"
    },
    "status": {
      "description": "採用状態",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "code",
    "name",
    "purpose",
    "selection",
    "release_id",
    "status",
    "etag"
  ],
  "title": "AxisRow",
  "type": "object"
}
```

## AxisWrite

組み合わせ軸の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | 軸コード |
| name | string | 必須 | minLength=1; maxLength=20000 | 軸名 |
| purpose | string | 必須 | enum=["generation", "search", "constraint", "derived", "presentation"] | 生成/検索/制約等 |
| release_id | string (uuid) | 必須 | 追加制約なし | 定義版 |
| selection | string | 必須 | enum=["single", "multiple"] | 単複 |
| status | string | 必須 | enum=["active", "retired"] | 採用状態 |

```json
{
  "additionalProperties": false,
  "description": "組み合わせ軸の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "code": {
      "description": "軸コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "name": {
      "description": "軸名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "purpose": {
      "description": "生成/検索/制約等",
      "enum": [
        "generation",
        "search",
        "constraint",
        "derived",
        "presentation"
      ],
      "title": "Purpose",
      "type": "string"
    },
    "release_id": {
      "description": "定義版",
      "format": "uuid",
      "title": "Release Id",
      "type": "string"
    },
    "selection": {
      "description": "単複",
      "enum": [
        "single",
        "multiple"
      ],
      "title": "Selection",
      "type": "string"
    },
    "status": {
      "description": "採用状態",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "code",
    "name",
    "purpose",
    "selection",
    "release_id",
    "status"
  ],
  "title": "AxisWrite",
  "type": "object"
}
```

## CandidateAttemptRow

試行済み設計点の台帳のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| attempts | integer | 必須 | 追加制約なし | 試行上限(暫定) |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時 |
| design_key | string | 必須 | minLength=64; maxLength=64 | 正規化した設計キー |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変ID |
| job_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 生成ジョブ |
| ordinal | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 設計点の序数 |
| reason_code | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | 棄却理由 |
| recipe_version_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 採用した版 |
| state | string | 必須 | enum=["pending", "invalid", "generated", "duplicate", "accepted", "failed"] | 候補の段階 |
| template_id | string (uuid) | 必須 | 追加制約なし | 定義版 |

```json
{
  "additionalProperties": false,
  "description": "試行済み設計点の台帳のDB応答。",
  "properties": {
    "attempts": {
      "description": "試行上限(暫定)",
      "title": "Attempts",
      "type": "integer"
    },
    "created_at": {
      "description": "作成日時",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "design_key": {
      "description": "正規化した設計キー",
      "maxLength": 64,
      "minLength": 64,
      "title": "Design Key",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変ID",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "job_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "生成ジョブ",
      "title": "Job Id"
    },
    "ordinal": {
      "description": "設計点の序数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Ordinal",
      "type": "string"
    },
    "reason_code": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "棄却理由",
      "title": "Reason Code"
    },
    "recipe_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "採用した版",
      "title": "Recipe Version Id"
    },
    "state": {
      "description": "候補の段階",
      "enum": [
        "pending",
        "invalid",
        "generated",
        "duplicate",
        "accepted",
        "failed"
      ],
      "title": "State",
      "type": "string"
    },
    "template_id": {
      "description": "定義版",
      "format": "uuid",
      "title": "Template Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "template_id",
    "ordinal",
    "design_key",
    "job_id",
    "state",
    "reason_code",
    "recipe_version_id",
    "attempts",
    "etag"
  ],
  "title": "CandidateAttemptRow",
  "type": "object"
}
```

## CandidateAttemptWrite

試行済み設計点の台帳の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| attempts | integer | 必須 | 追加制約なし | 試行上限(暫定) |
| design_key | string | 必須 | minLength=64; maxLength=64 | 正規化した設計キー |
| job_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 生成ジョブ |
| ordinal | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 設計点の序数 |
| reason_code | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | 棄却理由 |
| recipe_version_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 採用した版 |
| state | string | 必須 | enum=["pending", "invalid", "generated", "duplicate", "accepted", "failed"] | 候補の段階 |
| template_id | string (uuid) | 必須 | 追加制約なし | 定義版 |

```json
{
  "additionalProperties": false,
  "description": "試行済み設計点の台帳の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "attempts": {
      "description": "試行上限(暫定)",
      "title": "Attempts",
      "type": "integer"
    },
    "design_key": {
      "description": "正規化した設計キー",
      "maxLength": 64,
      "minLength": 64,
      "title": "Design Key",
      "type": "string"
    },
    "job_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "生成ジョブ",
      "title": "Job Id"
    },
    "ordinal": {
      "description": "設計点の序数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Ordinal",
      "type": "string"
    },
    "reason_code": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "棄却理由",
      "title": "Reason Code"
    },
    "recipe_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "採用した版",
      "title": "Recipe Version Id"
    },
    "state": {
      "description": "候補の段階",
      "enum": [
        "pending",
        "invalid",
        "generated",
        "duplicate",
        "accepted",
        "failed"
      ],
      "title": "State",
      "type": "string"
    },
    "template_id": {
      "description": "定義版",
      "format": "uuid",
      "title": "Template Id",
      "type": "string"
    }
  },
  "required": [
    "template_id",
    "ordinal",
    "design_key",
    "state",
    "attempts"
  ],
  "title": "CandidateAttemptWrite",
  "type": "object"
}
```

## CanonicalParameter



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| operation_id | string (uuid) | 必須 | 追加制約なし | Operation Id |
| parameter_id | string (uuid) | 必須 | 追加制約なし | Parameter Id |
| value | anyOf(string, boolean, number) | 必須 | 追加制約なし | Value |

```json
{
  "additionalProperties": false,
  "properties": {
    "operation_id": {
      "format": "uuid",
      "title": "Operation Id",
      "type": "string"
    },
    "parameter_id": {
      "format": "uuid",
      "title": "Parameter Id",
      "type": "string"
    },
    "value": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "boolean"
        },
        {
          "type": "number"
        }
      ],
      "title": "Value"
    }
  },
  "required": [
    "operation_id",
    "parameter_id",
    "value"
  ],
  "title": "CanonicalParameter",
  "type": "object"
}
```

## CanonicalRecipe-Input



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| family_id | string (uuid) | 必須 | 追加制約なし | Family Id |
| ingredient_ratios | array&lt;IngredientRatio-Input&gt; | 必須 | maxItems=1000 | Ingredient Ratios |
| operations | array&lt;string (uuid)&gt; | 必須 | maxItems=1000 | Operations |
| parameters | array&lt;CanonicalParameter&gt; | 必須 | maxItems=1000 | Parameters |
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |

```json
{
  "additionalProperties": false,
  "properties": {
    "family_id": {
      "format": "uuid",
      "title": "Family Id",
      "type": "string"
    },
    "ingredient_ratios": {
      "items": {
        "$ref": "#/components/schemas/IngredientRatio-Input"
      },
      "maxItems": 1000,
      "title": "Ingredient Ratios",
      "type": "array"
    },
    "operations": {
      "items": {
        "format": "uuid",
        "type": "string"
      },
      "maxItems": 1000,
      "title": "Operations",
      "type": "array"
    },
    "parameters": {
      "items": {
        "$ref": "#/components/schemas/CanonicalParameter"
      },
      "maxItems": 1000,
      "title": "Parameters",
      "type": "array"
    },
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    }
  },
  "required": [
    "ingredient_ratios",
    "operations",
    "parameters",
    "family_id"
  ],
  "title": "CanonicalRecipe",
  "type": "object"
}
```

## CanonicalRecipe-Output



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| family_id | string (uuid) | 必須 | 追加制約なし | Family Id |
| ingredient_ratios | array&lt;IngredientRatio-Output&gt; | 必須 | maxItems=1000 | Ingredient Ratios |
| operations | array&lt;string (uuid)&gt; | 必須 | maxItems=1000 | Operations |
| parameters | array&lt;CanonicalParameter&gt; | 必須 | maxItems=1000 | Parameters |
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |

```json
{
  "additionalProperties": false,
  "properties": {
    "family_id": {
      "format": "uuid",
      "title": "Family Id",
      "type": "string"
    },
    "ingredient_ratios": {
      "items": {
        "$ref": "#/components/schemas/IngredientRatio-Output"
      },
      "maxItems": 1000,
      "title": "Ingredient Ratios",
      "type": "array"
    },
    "operations": {
      "items": {
        "format": "uuid",
        "type": "string"
      },
      "maxItems": 1000,
      "title": "Operations",
      "type": "array"
    },
    "parameters": {
      "items": {
        "$ref": "#/components/schemas/CanonicalParameter"
      },
      "maxItems": 1000,
      "title": "Parameters",
      "type": "array"
    },
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    }
  },
  "required": [
    "ingredient_ratios",
    "operations",
    "parameters",
    "family_id"
  ],
  "title": "CanonicalRecipe",
  "type": "object"
}
```

## CatalogReleaseRow

カタログ公開版のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| manifest_hash | string | 必須 | minLength=64; maxLength=64 | 採用したID・内容のハッシュ |
| owner_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 私有カタログの所有者。NULLは共通カタログ |
| published_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 公開日時 |
| version | string | 必須 | minLength=1; maxLength=20000 | カタログ版番号 |

```json
{
  "additionalProperties": false,
  "description": "カタログ公開版のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "manifest_hash": {
      "description": "採用したID・内容のハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Manifest Hash",
      "type": "string"
    },
    "owner_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "私有カタログの所有者。NULLは共通カタログ",
      "title": "Owner Id"
    },
    "published_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "公開日時",
      "title": "Published At"
    },
    "version": {
      "description": "カタログ版番号",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Version",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "version",
    "manifest_hash",
    "published_at",
    "owner_id",
    "etag"
  ],
  "title": "CatalogReleaseRow",
  "type": "object"
}
```

## CatalogReleaseWrite

カタログ公開版の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| manifest_hash | string | 必須 | minLength=64; maxLength=64 | 採用したID・内容のハッシュ |
| published_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 公開日時 |
| version | string | 必須 | minLength=1; maxLength=20000 | カタログ版番号 |

```json
{
  "additionalProperties": false,
  "description": "カタログ公開版の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "manifest_hash": {
      "description": "採用したID・内容のハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Manifest Hash",
      "type": "string"
    },
    "published_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "公開日時",
      "title": "Published At"
    },
    "version": {
      "description": "カタログ版番号",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Version",
      "type": "string"
    }
  },
  "required": [
    "version",
    "manifest_hash"
  ],
  "title": "CatalogReleaseWrite",
  "type": "object"
}
```

## CompatibilityRuleRow

組み合わせ・公開ルールのDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | 規則コード |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| message | string | 必須 | minLength=1; maxLength=20000 | 理由 |
| predicate | Predicate-Output | 必須 | 追加制約なし | 型付き条件式 |
| severity | string | 必須 | enum=["block", "review", "score"] | 除外/保留/順位 |
| source_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 根拠 |
| status | string | 必須 | enum=["active", "retired"] | 利用状態 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 規則版 |

```json
{
  "additionalProperties": false,
  "description": "組み合わせ・公開ルールのDB応答。",
  "properties": {
    "code": {
      "description": "規則コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "message": {
      "description": "理由",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Message",
      "type": "string"
    },
    "predicate": {
      "$ref": "#/components/schemas/Predicate-Output",
      "description": "型付き条件式"
    },
    "severity": {
      "description": "除外/保留/順位",
      "enum": [
        "block",
        "review",
        "score"
      ],
      "title": "Severity",
      "type": "string"
    },
    "source_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "根拠",
      "title": "Source Id"
    },
    "status": {
      "description": "利用状態",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    },
    "version": {
      "description": "規則版",
      "exclusiveMinimum": 0.0,
      "title": "Version",
      "type": "integer"
    }
  },
  "required": [
    "id",
    "created_at",
    "code",
    "version",
    "severity",
    "predicate",
    "message",
    "source_id",
    "status",
    "etag"
  ],
  "title": "CompatibilityRuleRow",
  "type": "object"
}
```

## CompatibilityRuleWrite

組み合わせ・公開ルールの編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | 規則コード |
| message | string | 必須 | minLength=1; maxLength=20000 | 理由 |
| predicate | Predicate-Input | 必須 | 追加制約なし | 型付き条件式 |
| severity | string | 必須 | enum=["block", "review", "score"] | 除外/保留/順位 |
| source_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 根拠 |
| status | string | 必須 | enum=["active", "retired"] | 利用状態 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 規則版 |

```json
{
  "additionalProperties": false,
  "description": "組み合わせ・公開ルールの編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "code": {
      "description": "規則コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "message": {
      "description": "理由",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Message",
      "type": "string"
    },
    "predicate": {
      "$ref": "#/components/schemas/Predicate-Input",
      "description": "型付き条件式"
    },
    "severity": {
      "description": "除外/保留/順位",
      "enum": [
        "block",
        "review",
        "score"
      ],
      "title": "Severity",
      "type": "string"
    },
    "source_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "根拠",
      "title": "Source Id"
    },
    "status": {
      "description": "利用状態",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    },
    "version": {
      "description": "規則版",
      "exclusiveMinimum": 0.0,
      "title": "Version",
      "type": "integer"
    }
  },
  "required": [
    "code",
    "version",
    "severity",
    "predicate",
    "message",
    "status"
  ],
  "title": "CompatibilityRuleWrite",
  "type": "object"
}
```

## ConsumptionResult



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| applied | boolean | 必須 | 追加制約なし | Applied |
| foodId | string | 必須 | minLength=1; maxLength=128 | Foodid |
| form | string | 必須 | maxLength=500 | Form |
| lotIds | array&lt;string&gt; | 必須 | maxItems=1000; 要素の制約=minLength=1; maxLength=128 | Lotids |
| quantity | Quantity | 必須 | 追加制約なし |  |
| reason | string | 必須 | maxLength=500 | Reason |

```json
{
  "additionalProperties": false,
  "properties": {
    "applied": {
      "title": "Applied",
      "type": "boolean"
    },
    "foodId": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Foodid",
      "type": "string"
    },
    "form": {
      "maxLength": 500,
      "title": "Form",
      "type": "string"
    },
    "lotIds": {
      "items": {
        "maxLength": 128,
        "minLength": 1,
        "type": "string"
      },
      "maxItems": 1000,
      "title": "Lotids",
      "type": "array"
    },
    "quantity": {
      "$ref": "#/components/schemas/Quantity"
    },
    "reason": {
      "maxLength": 500,
      "title": "Reason",
      "type": "string"
    }
  },
  "required": [
    "foodId",
    "quantity",
    "form",
    "applied",
    "reason",
    "lotIds"
  ],
  "title": "ConsumptionResult",
  "type": "object"
}
```

## ConversionRow

食材形態別換算のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| conditions | string | 必須 | minLength=1; maxLength=20000 | サイズ・温度・すり切り等 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| factor | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 出力量=入力量x倍率 |
| form_id | string (uuid) | 必須 | 追加制約なし | 換算対象形態 |
| from_unit_id | string (uuid) | 必須 | 追加制約なし | 入力単位 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| quality | string | 必須 | enum=["measured", "manufacturer", "reference", "estimated", "unknown"] | 実測・推定区別 |
| release_id | string (uuid) | 必須 | 追加制約なし | 換算版 |
| source_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 換算根拠 |
| to_unit_id | string (uuid) | 必須 | 追加制約なし | 出力単位 |

```json
{
  "additionalProperties": false,
  "description": "食材形態別換算のDB応答。",
  "properties": {
    "conditions": {
      "description": "サイズ・温度・すり切り等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Conditions",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "factor": {
      "description": "出力量=入力量x倍率",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Factor",
      "type": "string"
    },
    "form_id": {
      "description": "換算対象形態",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "from_unit_id": {
      "description": "入力単位",
      "format": "uuid",
      "title": "From Unit Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "quality": {
      "description": "実測・推定区別",
      "enum": [
        "measured",
        "manufacturer",
        "reference",
        "estimated",
        "unknown"
      ],
      "title": "Quality",
      "type": "string"
    },
    "release_id": {
      "description": "換算版",
      "format": "uuid",
      "title": "Release Id",
      "type": "string"
    },
    "source_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "換算根拠",
      "title": "Source Id"
    },
    "to_unit_id": {
      "description": "出力単位",
      "format": "uuid",
      "title": "To Unit Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "form_id",
    "from_unit_id",
    "to_unit_id",
    "factor",
    "quality",
    "source_id",
    "conditions",
    "release_id",
    "etag"
  ],
  "title": "ConversionRow",
  "type": "object"
}
```

## ConversionWrite

食材形態別換算の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| conditions | string | 必須 | minLength=1; maxLength=20000 | サイズ・温度・すり切り等 |
| factor | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 出力量=入力量x倍率 |
| form_id | string (uuid) | 必須 | 追加制約なし | 換算対象形態 |
| from_unit_id | string (uuid) | 必須 | 追加制約なし | 入力単位 |
| quality | string | 必須 | enum=["measured", "manufacturer", "reference", "estimated", "unknown"] | 実測・推定区別 |
| release_id | string (uuid) | 必須 | 追加制約なし | 換算版 |
| source_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 換算根拠 |
| to_unit_id | string (uuid) | 必須 | 追加制約なし | 出力単位 |

```json
{
  "additionalProperties": false,
  "description": "食材形態別換算の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "conditions": {
      "description": "サイズ・温度・すり切り等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Conditions",
      "type": "string"
    },
    "factor": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "出力量=入力量x倍率",
      "title": "Factor"
    },
    "form_id": {
      "description": "換算対象形態",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "from_unit_id": {
      "description": "入力単位",
      "format": "uuid",
      "title": "From Unit Id",
      "type": "string"
    },
    "quality": {
      "description": "実測・推定区別",
      "enum": [
        "measured",
        "manufacturer",
        "reference",
        "estimated",
        "unknown"
      ],
      "title": "Quality",
      "type": "string"
    },
    "release_id": {
      "description": "換算版",
      "format": "uuid",
      "title": "Release Id",
      "type": "string"
    },
    "source_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "換算根拠",
      "title": "Source Id"
    },
    "to_unit_id": {
      "description": "出力単位",
      "format": "uuid",
      "title": "To Unit Id",
      "type": "string"
    }
  },
  "required": [
    "form_id",
    "from_unit_id",
    "to_unit_id",
    "factor",
    "quality",
    "conditions",
    "release_id"
  ],
  "title": "ConversionWrite",
  "type": "object"
}
```

## CookingInput-Input



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| ingredients | array&lt;FrozenIngredient-Input&gt; | 必須 | maxItems=1000 | Ingredients |
| items | array&lt;FrozenMenuItem-Input&gt; | 必須 | maxItems=100 | Items |
| menu_revision | integer | 必須 | minimum=1.0 | Menu Revision |
| planner_config | PlannerConfig | 必須 | 追加制約なし |  |
| resources | array&lt;FrozenResource-Input&gt; | 必須 | maxItems=100 | Resources |
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |

```json
{
  "additionalProperties": false,
  "properties": {
    "ingredients": {
      "items": {
        "$ref": "#/components/schemas/FrozenIngredient-Input"
      },
      "maxItems": 1000,
      "title": "Ingredients",
      "type": "array"
    },
    "items": {
      "items": {
        "$ref": "#/components/schemas/FrozenMenuItem-Input"
      },
      "maxItems": 100,
      "title": "Items",
      "type": "array"
    },
    "menu_revision": {
      "minimum": 1.0,
      "title": "Menu Revision",
      "type": "integer"
    },
    "planner_config": {
      "$ref": "#/components/schemas/PlannerConfig"
    },
    "resources": {
      "items": {
        "$ref": "#/components/schemas/FrozenResource-Input"
      },
      "maxItems": 100,
      "title": "Resources",
      "type": "array"
    },
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    }
  },
  "required": [
    "menu_revision",
    "items",
    "ingredients",
    "resources",
    "planner_config"
  ],
  "title": "CookingInput",
  "type": "object"
}
```

## CookingInput-Output



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| ingredients | array&lt;FrozenIngredient-Output&gt; | 必須 | maxItems=1000 | Ingredients |
| items | array&lt;FrozenMenuItem-Output&gt; | 必須 | maxItems=100 | Items |
| menu_revision | integer | 必須 | minimum=1.0 | Menu Revision |
| planner_config | PlannerConfig | 必須 | 追加制約なし |  |
| resources | array&lt;FrozenResource-Output&gt; | 必須 | maxItems=100 | Resources |
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |

```json
{
  "additionalProperties": false,
  "properties": {
    "ingredients": {
      "items": {
        "$ref": "#/components/schemas/FrozenIngredient-Output"
      },
      "maxItems": 1000,
      "title": "Ingredients",
      "type": "array"
    },
    "items": {
      "items": {
        "$ref": "#/components/schemas/FrozenMenuItem-Output"
      },
      "maxItems": 100,
      "title": "Items",
      "type": "array"
    },
    "menu_revision": {
      "minimum": 1.0,
      "title": "Menu Revision",
      "type": "integer"
    },
    "planner_config": {
      "$ref": "#/components/schemas/PlannerConfig"
    },
    "resources": {
      "items": {
        "$ref": "#/components/schemas/FrozenResource-Output"
      },
      "maxItems": 100,
      "title": "Resources",
      "type": "array"
    },
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    }
  },
  "required": [
    "menu_revision",
    "items",
    "ingredients",
    "resources",
    "planner_config"
  ],
  "title": "CookingInput",
  "type": "object"
}
```

## CookingRequest



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| deduct | boolean | 任意 | default=false | Deduct |
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9007199254740990.0 | Expectedversion |
| session | CookingSession | 必須 | 追加制約なし |  |

```json
{
  "additionalProperties": false,
  "properties": {
    "deduct": {
      "default": false,
      "title": "Deduct",
      "type": "boolean"
    },
    "expectedVersion": {
      "maximum": 9007199254740990.0,
      "minimum": 0.0,
      "title": "Expectedversion",
      "type": "integer"
    },
    "session": {
      "$ref": "#/components/schemas/CookingSession"
    }
  },
  "required": [
    "expectedVersion",
    "session"
  ],
  "title": "CookingRequest",
  "type": "object"
}
```

## CookingSession



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| completedStepIds | array&lt;string&gt; | 必須 | maxItems=500; 要素の制約=minLength=1; maxLength=128 | Completedstepids |
| consumptionResults | array&lt;ConsumptionResult&gt; | 必須 | maxItems=1000 | Consumptionresults |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| index | integer | 必須 | minimum=0.0; maximum=500.0 | Index |
| mealSnapshot | array&lt;MealItem&gt; | 必須 | maxItems=50 | Mealsnapshot |
| plan | array&lt;PlannedStep&gt; | 必須 | maxItems=500 | Plan |
| status | string | 必須 | enum=["active", "paused", "completed"] | Status |
| timers | array&lt;CookingTimer&gt; | 必須 | maxItems=50 | Timers |

```json
{
  "additionalProperties": false,
  "properties": {
    "completedStepIds": {
      "items": {
        "maxLength": 128,
        "minLength": 1,
        "type": "string"
      },
      "maxItems": 500,
      "title": "Completedstepids",
      "type": "array"
    },
    "consumptionResults": {
      "items": {
        "$ref": "#/components/schemas/ConsumptionResult"
      },
      "maxItems": 1000,
      "title": "Consumptionresults",
      "type": "array"
    },
    "id": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Id",
      "type": "string"
    },
    "index": {
      "maximum": 500.0,
      "minimum": 0.0,
      "title": "Index",
      "type": "integer"
    },
    "mealSnapshot": {
      "items": {
        "$ref": "#/components/schemas/MealItem"
      },
      "maxItems": 50,
      "title": "Mealsnapshot",
      "type": "array"
    },
    "plan": {
      "items": {
        "$ref": "#/components/schemas/PlannedStep"
      },
      "maxItems": 500,
      "title": "Plan",
      "type": "array"
    },
    "status": {
      "enum": [
        "active",
        "paused",
        "completed"
      ],
      "title": "Status",
      "type": "string"
    },
    "timers": {
      "items": {
        "$ref": "#/components/schemas/CookingTimer"
      },
      "maxItems": 50,
      "title": "Timers",
      "type": "array"
    }
  },
  "required": [
    "id",
    "mealSnapshot",
    "plan",
    "index",
    "completedStepIds",
    "timers",
    "status",
    "consumptionResults"
  ],
  "title": "CookingSession",
  "type": "object"
}
```

## CookingSessionRow

調理計画実行のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| current_task_index | integer | 必須 | 追加制約なし | 調理画面の現在の工程位置(0始まり) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| input_hash | string | 必須 | minLength=64; maxLength=64 | 入力ハッシュ |
| input_snapshot | CookingInput-Output | 必須 | 追加制約なし | 材料・資源・人数の固定入力 |
| menu_id | string (uuid) | 必須 | 追加制約なし | 対象献立 |
| menu_revision | integer | 必須 | exclusiveMinimum=0.0 | 献立版 |
| planner_version | string | 必須 | minLength=1; maxLength=20000 | 計画器の版 |
| status | string | 必須 | enum=["planned", "cooking", "completed", "cancelled"] | 実行状態 |
| target_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 完成希望時刻 |

```json
{
  "additionalProperties": false,
  "description": "調理計画実行のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "current_task_index": {
      "description": "調理画面の現在の工程位置(0始まり)",
      "title": "Current Task Index",
      "type": "integer"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "input_hash": {
      "description": "入力ハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Input Hash",
      "type": "string"
    },
    "input_snapshot": {
      "$ref": "#/components/schemas/CookingInput-Output",
      "description": "材料・資源・人数の固定入力"
    },
    "menu_id": {
      "description": "対象献立",
      "format": "uuid",
      "title": "Menu Id",
      "type": "string"
    },
    "menu_revision": {
      "description": "献立版",
      "exclusiveMinimum": 0.0,
      "title": "Menu Revision",
      "type": "integer"
    },
    "planner_version": {
      "description": "計画器の版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Planner Version",
      "type": "string"
    },
    "status": {
      "description": "実行状態",
      "enum": [
        "planned",
        "cooking",
        "completed",
        "cancelled"
      ],
      "title": "Status",
      "type": "string"
    },
    "target_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "完成希望時刻",
      "title": "Target At"
    }
  },
  "required": [
    "id",
    "created_at",
    "menu_id",
    "menu_revision",
    "status",
    "target_at",
    "planner_version",
    "input_snapshot",
    "input_hash",
    "current_task_index",
    "etag"
  ],
  "title": "CookingSessionRow",
  "type": "object"
}
```

## CookingSessionWrite

調理計画実行の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| current_task_index | integer | 必須 | 追加制約なし | 調理画面の現在の工程位置(0始まり) |
| input_hash | string | 必須 | minLength=64; maxLength=64 | 入力ハッシュ |
| input_snapshot | CookingInput-Input | 必須 | 追加制約なし | 材料・資源・人数の固定入力 |
| menu_id | string (uuid) | 必須 | 追加制約なし | 対象献立 |
| menu_revision | integer | 必須 | exclusiveMinimum=0.0 | 献立版 |
| planner_version | string | 必須 | minLength=1; maxLength=20000 | 計画器の版 |
| status | string | 必須 | enum=["planned", "cooking", "completed", "cancelled"] | 実行状態 |
| target_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 完成希望時刻 |

```json
{
  "additionalProperties": false,
  "description": "調理計画実行の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "current_task_index": {
      "description": "調理画面の現在の工程位置(0始まり)",
      "title": "Current Task Index",
      "type": "integer"
    },
    "input_hash": {
      "description": "入力ハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Input Hash",
      "type": "string"
    },
    "input_snapshot": {
      "$ref": "#/components/schemas/CookingInput-Input",
      "description": "材料・資源・人数の固定入力"
    },
    "menu_id": {
      "description": "対象献立",
      "format": "uuid",
      "title": "Menu Id",
      "type": "string"
    },
    "menu_revision": {
      "description": "献立版",
      "exclusiveMinimum": 0.0,
      "title": "Menu Revision",
      "type": "integer"
    },
    "planner_version": {
      "description": "計画器の版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Planner Version",
      "type": "string"
    },
    "status": {
      "description": "実行状態",
      "enum": [
        "planned",
        "cooking",
        "completed",
        "cancelled"
      ],
      "title": "Status",
      "type": "string"
    },
    "target_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "完成希望時刻",
      "title": "Target At"
    }
  },
  "required": [
    "menu_id",
    "menu_revision",
    "status",
    "planner_version",
    "input_snapshot",
    "input_hash",
    "current_task_index"
  ],
  "title": "CookingSessionWrite",
  "type": "object"
}
```

## CookingTimer



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| durationSeconds | number | 必須 | minimum=0.0; maximum=1000000.0 | Durationseconds |
| startedAt | number | 必須 | minimum=0.0 | Startedat |
| stepKey | string | 必須 | maxLength=500 | Stepkey |

```json
{
  "additionalProperties": false,
  "properties": {
    "durationSeconds": {
      "maximum": 1000000.0,
      "minimum": 0.0,
      "title": "Durationseconds",
      "type": "number"
    },
    "startedAt": {
      "minimum": 0.0,
      "title": "Startedat",
      "type": "number"
    },
    "stepKey": {
      "maxLength": 500,
      "title": "Stepkey",
      "type": "string"
    }
  },
  "required": [
    "stepKey",
    "startedAt",
    "durationSeconds"
  ],
  "title": "CookingTimer",
  "type": "object"
}
```

## CreatePantryRequest



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9007199254740990.0 | Expectedversion |
| expiresOn | anyOf(string, null) | 任意 | anyOfの制約=string: pattern="^\\d{4}-\\d{2}-\\d{2}$" | Expireson |
| foodId | string | 必須 | minLength=1; maxLength=128 | Foodid |
| form | string | 任意 | default="標準"; maxLength=500 | Form |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| location | string | 任意 | enum=["冷蔵", "冷凍", "常温"]; default="冷蔵" | Location |
| priority | boolean | 任意 | default=false | Priority |
| quantity | Quantity | 必須 | 追加制約なし |  |

```json
{
  "additionalProperties": false,
  "properties": {
    "expectedVersion": {
      "maximum": 9007199254740990.0,
      "minimum": 0.0,
      "title": "Expectedversion",
      "type": "integer"
    },
    "expiresOn": {
      "anyOf": [
        {
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Expireson"
    },
    "foodId": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Foodid",
      "type": "string"
    },
    "form": {
      "default": "標準",
      "maxLength": 500,
      "title": "Form",
      "type": "string"
    },
    "id": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Id",
      "type": "string"
    },
    "location": {
      "default": "冷蔵",
      "enum": [
        "冷蔵",
        "冷凍",
        "常温"
      ],
      "title": "Location",
      "type": "string"
    },
    "priority": {
      "default": false,
      "title": "Priority",
      "type": "boolean"
    },
    "quantity": {
      "$ref": "#/components/schemas/Quantity"
    }
  },
  "required": [
    "foodId",
    "quantity",
    "expectedVersion",
    "id"
  ],
  "title": "CreatePantryRequest",
  "type": "object"
}
```

## CustomFoodRequest



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9007199254740990.0 | Expectedversion |
| food | Food | 必須 | 追加制約なし |  |

```json
{
  "additionalProperties": false,
  "properties": {
    "expectedVersion": {
      "maximum": 9007199254740990.0,
      "minimum": 0.0,
      "title": "Expectedversion",
      "type": "integer"
    },
    "food": {
      "$ref": "#/components/schemas/Food"
    }
  },
  "required": [
    "expectedVersion",
    "food"
  ],
  "title": "CustomFoodRequest",
  "type": "object"
}
```

## Food



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| aliases | array&lt;string&gt; | 必須 | maxItems=100; 要素の制約=maxLength=500 | Aliases |
| category | string | 必須 | maxLength=500 | Category |
| componentFoodIds | array&lt;string&gt; | 必須 | maxItems=100; 要素の制約=minLength=1; maxLength=128 | Componentfoodids |
| componentsKnown | boolean | 必須 | 追加制約なし | Componentsknown |
| defaultUnit | string | 必須 | enum=["g", "ml", "個", "パック", "袋", "缶", "本", "枚", "点"] | Defaultunit |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| imageIndex | anyOf(integer, null) | 必須 | anyOfの制約=integer: minimum=0.0 | Imageindex |
| location | string | 必須 | enum=["冷蔵", "冷凍", "常温"] | Location |
| name | string | 必須 | minLength=1; maxLength=100 | Name |
| pantry | boolean | 必須 | 追加制約なし | Pantry |

```json
{
  "additionalProperties": false,
  "properties": {
    "aliases": {
      "items": {
        "maxLength": 500,
        "type": "string"
      },
      "maxItems": 100,
      "title": "Aliases",
      "type": "array"
    },
    "category": {
      "maxLength": 500,
      "title": "Category",
      "type": "string"
    },
    "componentFoodIds": {
      "items": {
        "maxLength": 128,
        "minLength": 1,
        "type": "string"
      },
      "maxItems": 100,
      "title": "Componentfoodids",
      "type": "array"
    },
    "componentsKnown": {
      "title": "Componentsknown",
      "type": "boolean"
    },
    "defaultUnit": {
      "enum": [
        "g",
        "ml",
        "個",
        "パック",
        "袋",
        "缶",
        "本",
        "枚",
        "点"
      ],
      "title": "Defaultunit",
      "type": "string"
    },
    "id": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Id",
      "type": "string"
    },
    "imageIndex": {
      "anyOf": [
        {
          "minimum": 0.0,
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "title": "Imageindex"
    },
    "location": {
      "enum": [
        "冷蔵",
        "冷凍",
        "常温"
      ],
      "title": "Location",
      "type": "string"
    },
    "name": {
      "maxLength": 100,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "pantry": {
      "title": "Pantry",
      "type": "boolean"
    }
  },
  "required": [
    "id",
    "name",
    "aliases",
    "category",
    "defaultUnit",
    "location",
    "pantry",
    "imageIndex",
    "componentsKnown",
    "componentFoodIds"
  ],
  "title": "Food",
  "type": "object"
}
```

## FoodAliasRow

食材別名のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| alias | string | 必須 | minLength=1; maxLength=500 | 別名・かな |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| food_id | string (uuid) | 必須 | 追加制約なし | 正規食材 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| locale | string | 必須 | minLength=1; maxLength=20000 | 言語・地域 |

```json
{
  "additionalProperties": false,
  "description": "食材別名のDB応答。",
  "properties": {
    "alias": {
      "description": "別名・かな",
      "maxLength": 500,
      "minLength": 1,
      "title": "Alias",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "food_id": {
      "description": "正規食材",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "locale": {
      "description": "言語・地域",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Locale",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "food_id",
    "alias",
    "locale",
    "etag"
  ],
  "title": "FoodAliasRow",
  "type": "object"
}
```

## FoodAliasWrite

食材別名の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| alias | string | 必須 | minLength=1; maxLength=500 | 別名・かな |
| food_id | string (uuid) | 必須 | 追加制約なし | 正規食材 |
| locale | string | 必須 | minLength=1; maxLength=20000 | 言語・地域 |

```json
{
  "additionalProperties": false,
  "description": "食材別名の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "alias": {
      "description": "別名・かな",
      "maxLength": 500,
      "minLength": 1,
      "title": "Alias",
      "type": "string"
    },
    "food_id": {
      "description": "正規食材",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "locale": {
      "description": "言語・地域",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Locale",
      "type": "string"
    }
  },
  "required": [
    "food_id",
    "alias",
    "locale"
  ],
  "title": "FoodAliasWrite",
  "type": "object"
}
```

## FoodAllergenRow

食材アレルゲン知識のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| allergen_id | string (uuid) | 必須 | 追加制約なし | 対象物質 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| form_id | string (uuid) | 必須 | 追加制約なし | 食材形態 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| presence | string | 必須 | enum=["contains", "may_contain", "absent_verified", "unknown"] | 含有・不明 |
| source_id | string (uuid) | 必須 | 追加制約なし | 判断根拠 |

```json
{
  "additionalProperties": false,
  "description": "食材アレルゲン知識のDB応答。",
  "properties": {
    "allergen_id": {
      "description": "対象物質",
      "format": "uuid",
      "title": "Allergen Id",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "form_id": {
      "description": "食材形態",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "presence": {
      "description": "含有・不明",
      "enum": [
        "contains",
        "may_contain",
        "absent_verified",
        "unknown"
      ],
      "title": "Presence",
      "type": "string"
    },
    "source_id": {
      "description": "判断根拠",
      "format": "uuid",
      "title": "Source Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "form_id",
    "allergen_id",
    "presence",
    "source_id",
    "etag"
  ],
  "title": "FoodAllergenRow",
  "type": "object"
}
```

## FoodAllergenWrite

食材アレルゲン知識の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| allergen_id | string (uuid) | 必須 | 追加制約なし | 対象物質 |
| form_id | string (uuid) | 必須 | 追加制約なし | 食材形態 |
| presence | string | 必須 | enum=["contains", "may_contain", "absent_verified", "unknown"] | 含有・不明 |
| source_id | string (uuid) | 必須 | 追加制約なし | 判断根拠 |

```json
{
  "additionalProperties": false,
  "description": "食材アレルゲン知識の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "allergen_id": {
      "description": "対象物質",
      "format": "uuid",
      "title": "Allergen Id",
      "type": "string"
    },
    "form_id": {
      "description": "食材形態",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "presence": {
      "description": "含有・不明",
      "enum": [
        "contains",
        "may_contain",
        "absent_verified",
        "unknown"
      ],
      "title": "Presence",
      "type": "string"
    },
    "source_id": {
      "description": "判断根拠",
      "format": "uuid",
      "title": "Source Id",
      "type": "string"
    }
  },
  "required": [
    "form_id",
    "allergen_id",
    "presence",
    "source_id"
  ],
  "title": "FoodAllergenWrite",
  "type": "object"
}
```

## FoodAxisOptionRow

食材の分類属性のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| food_id | string (uuid) | 必須 | 追加制約なし | 食材 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| option_id | string (uuid) | 必須 | 追加制約なし | カテゴリ・入手性等の値 |

```json
{
  "additionalProperties": false,
  "description": "食材の分類属性のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "food_id": {
      "description": "食材",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "option_id": {
      "description": "カテゴリ・入手性等の値",
      "format": "uuid",
      "title": "Option Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "food_id",
    "option_id",
    "etag"
  ],
  "title": "FoodAxisOptionRow",
  "type": "object"
}
```

## FoodAxisOptionWrite

食材の分類属性の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| food_id | string (uuid) | 必須 | 追加制約なし | 食材 |
| option_id | string (uuid) | 必須 | 追加制約なし | カテゴリ・入手性等の値 |

```json
{
  "additionalProperties": false,
  "description": "食材の分類属性の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "food_id": {
      "description": "食材",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "option_id": {
      "description": "カテゴリ・入手性等の値",
      "format": "uuid",
      "title": "Option Id",
      "type": "string"
    }
  },
  "required": [
    "food_id",
    "option_id"
  ],
  "title": "FoodAxisOptionWrite",
  "type": "object"
}
```

## FoodFormRow

食材形態のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| base_unit_id | string (uuid) | 必須 | 追加制約なし | 計算基準単位 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| food_id | string (uuid) | 必須 | 追加制約なし | 対応食材 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| name | string | 必須 | minLength=1; maxLength=500 | 生皮付き・冷凍刻み等 |
| quantity_basis | string | 必須 | enum=["edible", "as_purchased", "drained", "prepared"] | 数量の対象部分 |
| state | string | 必須 | enum=["raw", "dry", "frozen", "cooked", "rehydrated", "drained", "peeled", "ready"] | 処理状態 |
| status | string | 必須 | enum=["active", "retired"] | 利用状態 |

```json
{
  "additionalProperties": false,
  "description": "食材形態のDB応答。",
  "properties": {
    "base_unit_id": {
      "description": "計算基準単位",
      "format": "uuid",
      "title": "Base Unit Id",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "food_id": {
      "description": "対応食材",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "name": {
      "description": "生皮付き・冷凍刻み等",
      "maxLength": 500,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "quantity_basis": {
      "description": "数量の対象部分",
      "enum": [
        "edible",
        "as_purchased",
        "drained",
        "prepared"
      ],
      "title": "Quantity Basis",
      "type": "string"
    },
    "state": {
      "description": "処理状態",
      "enum": [
        "raw",
        "dry",
        "frozen",
        "cooked",
        "rehydrated",
        "drained",
        "peeled",
        "ready"
      ],
      "title": "State",
      "type": "string"
    },
    "status": {
      "description": "利用状態",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "food_id",
    "name",
    "state",
    "base_unit_id",
    "quantity_basis",
    "status",
    "etag"
  ],
  "title": "FoodFormRow",
  "type": "object"
}
```

## FoodFormWrite

食材形態の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| base_unit_id | string (uuid) | 必須 | 追加制約なし | 計算基準単位 |
| food_id | string (uuid) | 必須 | 追加制約なし | 対応食材 |
| name | string | 必須 | minLength=1; maxLength=500 | 生皮付き・冷凍刻み等 |
| quantity_basis | string | 必須 | enum=["edible", "as_purchased", "drained", "prepared"] | 数量の対象部分 |
| state | string | 必須 | enum=["raw", "dry", "frozen", "cooked", "rehydrated", "drained", "peeled", "ready"] | 処理状態 |
| status | string | 必須 | enum=["active", "retired"] | 利用状態 |

```json
{
  "additionalProperties": false,
  "description": "食材形態の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "base_unit_id": {
      "description": "計算基準単位",
      "format": "uuid",
      "title": "Base Unit Id",
      "type": "string"
    },
    "food_id": {
      "description": "対応食材",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "name": {
      "description": "生皮付き・冷凍刻み等",
      "maxLength": 500,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "quantity_basis": {
      "description": "数量の対象部分",
      "enum": [
        "edible",
        "as_purchased",
        "drained",
        "prepared"
      ],
      "title": "Quantity Basis",
      "type": "string"
    },
    "state": {
      "description": "処理状態",
      "enum": [
        "raw",
        "dry",
        "frozen",
        "cooked",
        "rehydrated",
        "drained",
        "peeled",
        "ready"
      ],
      "title": "State",
      "type": "string"
    },
    "status": {
      "description": "利用状態",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "food_id",
    "name",
    "state",
    "base_unit_id",
    "quantity_basis",
    "status"
  ],
  "title": "FoodFormWrite",
  "type": "object"
}
```

## FoodIdentityMemberRow

購買食品から同一性への対応のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| food_id | string (uuid) | 必須 | 追加制約なし | 元の食品 |
| id | string (uuid) | 必須 | 追加制約なし | 不変ID |
| identity_id | string (uuid) | 必須 | 追加制約なし | 同一性ID |
| normalizer_version | string | 必須 | minLength=1; maxLength=20000 | 正規化器版 |
| reason | string | 必須 | minLength=1; maxLength=20000 | 同一視の理由 |

```json
{
  "additionalProperties": false,
  "description": "購買食品から同一性への対応のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "food_id": {
      "description": "元の食品",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "id": {
      "description": "不変ID",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "identity_id": {
      "description": "同一性ID",
      "format": "uuid",
      "title": "Identity Id",
      "type": "string"
    },
    "normalizer_version": {
      "description": "正規化器版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Normalizer Version",
      "type": "string"
    },
    "reason": {
      "description": "同一視の理由",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Reason",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "food_id",
    "identity_id",
    "normalizer_version",
    "reason",
    "etag"
  ],
  "title": "FoodIdentityMemberRow",
  "type": "object"
}
```

## FoodIdentityMemberWrite

購買食品から同一性への対応の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| food_id | string (uuid) | 必須 | 追加制約なし | 元の食品 |
| identity_id | string (uuid) | 必須 | 追加制約なし | 同一性ID |
| normalizer_version | string | 必須 | minLength=1; maxLength=20000 | 正規化器版 |
| reason | string | 必須 | minLength=1; maxLength=20000 | 同一視の理由 |

```json
{
  "additionalProperties": false,
  "description": "購買食品から同一性への対応の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "food_id": {
      "description": "元の食品",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "identity_id": {
      "description": "同一性ID",
      "format": "uuid",
      "title": "Identity Id",
      "type": "string"
    },
    "normalizer_version": {
      "description": "正規化器版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Normalizer Version",
      "type": "string"
    },
    "reason": {
      "description": "同一視の理由",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Reason",
      "type": "string"
    }
  },
  "required": [
    "food_id",
    "identity_id",
    "normalizer_version",
    "reason"
  ],
  "title": "FoodIdentityMemberWrite",
  "type": "object"
}
```

## FoodIdentityRow

料理同一性上の食品のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | 形態を横断した食品コード |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変ID |
| name | string | 必須 | minLength=1; maxLength=20000 | 食品名 |
| normalizer_version | string | 必須 | minLength=1; maxLength=20000 | 正規化器の版 |

```json
{
  "additionalProperties": false,
  "description": "料理同一性上の食品のDB応答。",
  "properties": {
    "code": {
      "description": "形態を横断した食品コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変ID",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "name": {
      "description": "食品名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "normalizer_version": {
      "description": "正規化器の版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Normalizer Version",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "code",
    "name",
    "normalizer_version",
    "etag"
  ],
  "title": "FoodIdentityRow",
  "type": "object"
}
```

## FoodIdentityWrite

料理同一性上の食品の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | 形態を横断した食品コード |
| name | string | 必須 | minLength=1; maxLength=20000 | 食品名 |
| normalizer_version | string | 必須 | minLength=1; maxLength=20000 | 正規化器の版 |

```json
{
  "additionalProperties": false,
  "description": "料理同一性上の食品の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "code": {
      "description": "形態を横断した食品コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "name": {
      "description": "食品名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "normalizer_version": {
      "description": "正規化器の版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Normalizer Version",
      "type": "string"
    }
  },
  "required": [
    "code",
    "name",
    "normalizer_version"
  ],
  "title": "FoodIdentityWrite",
  "type": "object"
}
```

## FoodRow

購入・利用食材概念のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | 固定食材コード |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| kind | string | 必須 | enum=["basic", "processed", "ready_meal", "kit", "utility"] | 基本食材か加工食品か |
| name | string | 必須 | minLength=1; maxLength=100 | 食材名・加工品種別 |
| owner_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 私有食材の所有者。NULLは共通カタログ食材 |
| parent_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | カテゴリ親 |
| release_id | string (uuid) | 必須 | 追加制約なし | 所属公開版 |
| status | string | 必須 | enum=["active", "retired"] | 新規使用可否 |

```json
{
  "additionalProperties": false,
  "description": "購入・利用食材概念のDB応答。",
  "properties": {
    "code": {
      "description": "固定食材コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "kind": {
      "description": "基本食材か加工食品か",
      "enum": [
        "basic",
        "processed",
        "ready_meal",
        "kit",
        "utility"
      ],
      "title": "Kind",
      "type": "string"
    },
    "name": {
      "description": "食材名・加工品種別",
      "maxLength": 100,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "owner_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "私有食材の所有者。NULLは共通カタログ食材",
      "title": "Owner Id"
    },
    "parent_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "カテゴリ親",
      "title": "Parent Id"
    },
    "release_id": {
      "description": "所属公開版",
      "format": "uuid",
      "title": "Release Id",
      "type": "string"
    },
    "status": {
      "description": "新規使用可否",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "code",
    "name",
    "kind",
    "parent_id",
    "release_id",
    "status",
    "owner_id",
    "etag"
  ],
  "title": "FoodRow",
  "type": "object"
}
```

## FoodWrite

購入・利用食材概念の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | 固定食材コード |
| kind | string | 必須 | enum=["basic", "processed", "ready_meal", "kit", "utility"] | 基本食材か加工食品か |
| name | string | 必須 | minLength=1; maxLength=100 | 食材名・加工品種別 |
| parent_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | カテゴリ親 |
| release_id | string (uuid) | 必須 | 追加制約なし | 所属公開版 |
| status | string | 必須 | enum=["active", "retired"] | 新規使用可否 |

```json
{
  "additionalProperties": false,
  "description": "購入・利用食材概念の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "code": {
      "description": "固定食材コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "kind": {
      "description": "基本食材か加工食品か",
      "enum": [
        "basic",
        "processed",
        "ready_meal",
        "kit",
        "utility"
      ],
      "title": "Kind",
      "type": "string"
    },
    "name": {
      "description": "食材名・加工品種別",
      "maxLength": 100,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "parent_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "カテゴリ親",
      "title": "Parent Id"
    },
    "release_id": {
      "description": "所属公開版",
      "format": "uuid",
      "title": "Release Id",
      "type": "string"
    },
    "status": {
      "description": "新規使用可否",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "code",
    "name",
    "kind",
    "release_id",
    "status"
  ],
  "title": "FoodWrite",
  "type": "object"
}
```

## FoodsResponse



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| items | array&lt;Food&gt; | 必須 | 追加制約なし | Items |
| total | integer | 必須 | 追加制約なし | Total |

```json
{
  "additionalProperties": false,
  "properties": {
    "items": {
      "items": {
        "$ref": "#/components/schemas/Food"
      },
      "title": "Items",
      "type": "array"
    },
    "total": {
      "title": "Total",
      "type": "integer"
    }
  },
  "required": [
    "items",
    "total"
  ],
  "title": "FoodsResponse",
  "type": "object"
}
```

## FormYieldRow

処理歩留まりのDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| conditions | string | 必須 | minLength=1; maxLength=20000 | 皮むき・水戻し等の条件 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| input_form_id | string (uuid) | 必須 | 追加制約なし | 処理前形態 |
| output_form_id | string (uuid) | 必須 | 追加制約なし | 処理後形態 |
| quality | string | 必須 | enum=["measured", "manufacturer", "reference", "estimated", "unknown"] | 精度区分 |
| source_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 根拠 |
| yield_ratio | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 出力量/入力量 |

```json
{
  "additionalProperties": false,
  "description": "処理歩留まりのDB応答。",
  "properties": {
    "conditions": {
      "description": "皮むき・水戻し等の条件",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Conditions",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "input_form_id": {
      "description": "処理前形態",
      "format": "uuid",
      "title": "Input Form Id",
      "type": "string"
    },
    "output_form_id": {
      "description": "処理後形態",
      "format": "uuid",
      "title": "Output Form Id",
      "type": "string"
    },
    "quality": {
      "description": "精度区分",
      "enum": [
        "measured",
        "manufacturer",
        "reference",
        "estimated",
        "unknown"
      ],
      "title": "Quality",
      "type": "string"
    },
    "source_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "根拠",
      "title": "Source Id"
    },
    "yield_ratio": {
      "description": "出力量/入力量",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Yield Ratio",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "input_form_id",
    "output_form_id",
    "yield_ratio",
    "source_id",
    "quality",
    "conditions",
    "etag"
  ],
  "title": "FormYieldRow",
  "type": "object"
}
```

## FormYieldWrite

処理歩留まりの編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| conditions | string | 必須 | minLength=1; maxLength=20000 | 皮むき・水戻し等の条件 |
| input_form_id | string (uuid) | 必須 | 追加制約なし | 処理前形態 |
| output_form_id | string (uuid) | 必須 | 追加制約なし | 処理後形態 |
| quality | string | 必須 | enum=["measured", "manufacturer", "reference", "estimated", "unknown"] | 精度区分 |
| source_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 根拠 |
| yield_ratio | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 出力量/入力量 |

```json
{
  "additionalProperties": false,
  "description": "処理歩留まりの編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "conditions": {
      "description": "皮むき・水戻し等の条件",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Conditions",
      "type": "string"
    },
    "input_form_id": {
      "description": "処理前形態",
      "format": "uuid",
      "title": "Input Form Id",
      "type": "string"
    },
    "output_form_id": {
      "description": "処理後形態",
      "format": "uuid",
      "title": "Output Form Id",
      "type": "string"
    },
    "quality": {
      "description": "精度区分",
      "enum": [
        "measured",
        "manufacturer",
        "reference",
        "estimated",
        "unknown"
      ],
      "title": "Quality",
      "type": "string"
    },
    "source_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "根拠",
      "title": "Source Id"
    },
    "yield_ratio": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "出力量/入力量",
      "title": "Yield Ratio"
    }
  },
  "required": [
    "input_form_id",
    "output_form_id",
    "yield_ratio",
    "quality",
    "conditions"
  ],
  "title": "FormYieldWrite",
  "type": "object"
}
```

## FrozenIngredient-Input



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(number, string, null) | 任意 | anyOfの制約=number: minimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Amount |
| conversion_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | Conversion Id |
| form_id | string (uuid) | 必須 | 追加制約なし | Form Id |
| id | string (uuid) | 必須 | 追加制約なし | Id |
| unit_id | string (uuid) | 必須 | 追加制約なし | Unit Id |

```json
{
  "additionalProperties": false,
  "properties": {
    "amount": {
      "anyOf": [
        {
          "minimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Amount"
    },
    "conversion_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Conversion Id"
    },
    "form_id": {
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "id": {
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "unit_id": {
      "format": "uuid",
      "title": "Unit Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "form_id",
    "unit_id"
  ],
  "title": "FrozenIngredient",
  "type": "object"
}
```

## FrozenIngredient-Output



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Amount |
| conversion_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | Conversion Id |
| form_id | string (uuid) | 必須 | 追加制約なし | Form Id |
| id | string (uuid) | 必須 | 追加制約なし | Id |
| unit_id | string (uuid) | 必須 | 追加制約なし | Unit Id |

```json
{
  "additionalProperties": false,
  "properties": {
    "amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Amount"
    },
    "conversion_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Conversion Id"
    },
    "form_id": {
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "id": {
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "unit_id": {
      "format": "uuid",
      "title": "Unit Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "form_id",
    "unit_id"
  ],
  "title": "FrozenIngredient",
  "type": "object"
}
```

## FrozenMenuItem-Input



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| id | string (uuid) | 必須 | 追加制約なし | Id |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | Recipe Version Id |
| servings | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Servings |

```json
{
  "additionalProperties": false,
  "properties": {
    "id": {
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "recipe_version_id": {
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "servings": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
          "type": "string"
        }
      ],
      "title": "Servings"
    }
  },
  "required": [
    "id",
    "recipe_version_id",
    "servings"
  ],
  "title": "FrozenMenuItem",
  "type": "object"
}
```

## FrozenMenuItem-Output



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| id | string (uuid) | 必須 | 追加制約なし | Id |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | Recipe Version Id |
| servings | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Servings |

```json
{
  "additionalProperties": false,
  "properties": {
    "id": {
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "recipe_version_id": {
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "servings": {
      "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
      "title": "Servings",
      "type": "string"
    }
  },
  "required": [
    "id",
    "recipe_version_id",
    "servings"
  ],
  "title": "FrozenMenuItem",
  "type": "object"
}
```

## FrozenResource-Input



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| capacity | anyOf(number, string, null) | 任意 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Capacity |
| id | string (uuid) | 必須 | 追加制約なし | Id |
| quantity | integer | 必須 | exclusiveMinimum=0.0 | Quantity |
| resource_type_id | string (uuid) | 必須 | 追加制約なし | Resource Type Id |

```json
{
  "additionalProperties": false,
  "properties": {
    "capacity": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Capacity"
    },
    "id": {
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "quantity": {
      "exclusiveMinimum": 0.0,
      "title": "Quantity",
      "type": "integer"
    },
    "resource_type_id": {
      "format": "uuid",
      "title": "Resource Type Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "resource_type_id",
    "quantity"
  ],
  "title": "FrozenResource",
  "type": "object"
}
```

## FrozenResource-Output



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| capacity | anyOf(string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Capacity |
| id | string (uuid) | 必須 | 追加制約なし | Id |
| quantity | integer | 必須 | exclusiveMinimum=0.0 | Quantity |
| resource_type_id | string (uuid) | 必須 | 追加制約なし | Resource Type Id |

```json
{
  "additionalProperties": false,
  "properties": {
    "capacity": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Capacity"
    },
    "id": {
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "quantity": {
      "exclusiveMinimum": 0.0,
      "title": "Quantity",
      "type": "integer"
    },
    "resource_type_id": {
      "format": "uuid",
      "title": "Resource Type Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "resource_type_id",
    "quantity"
  ],
  "title": "FrozenResource",
  "type": "object"
}
```

## GenerationChoiceRow

生成軸の選択値のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| job_id | string (uuid) | 必須 | 追加制約なし | 実行 |
| option_id | string (uuid) | 必須 | 追加制約なし | 選択した軸候補 |

```json
{
  "additionalProperties": false,
  "description": "生成軸の選択値のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "job_id": {
      "description": "実行",
      "format": "uuid",
      "title": "Job Id",
      "type": "string"
    },
    "option_id": {
      "description": "選択した軸候補",
      "format": "uuid",
      "title": "Option Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "job_id",
    "option_id",
    "etag"
  ],
  "title": "GenerationChoiceRow",
  "type": "object"
}
```

## GenerationChoiceWrite

生成軸の選択値の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| job_id | string (uuid) | 必須 | 追加制約なし | 実行 |
| option_id | string (uuid) | 必須 | 追加制約なし | 選択した軸候補 |

```json
{
  "additionalProperties": false,
  "description": "生成軸の選択値の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "job_id": {
      "description": "実行",
      "format": "uuid",
      "title": "Job Id",
      "type": "string"
    },
    "option_id": {
      "description": "選択した軸候補",
      "format": "uuid",
      "title": "Option Id",
      "type": "string"
    }
  },
  "required": [
    "job_id",
    "option_id"
  ],
  "title": "GenerationChoiceWrite",
  "type": "object"
}
```

## GenerationFoodRow

生成の食材入力のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| form_id | string (uuid) | 必須 | 追加制約なし | 食材形態 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| job_id | string (uuid) | 必須 | 追加制約なし | 実行 |
| role | string | 必須 | enum=["main", "support", "seasoning", "aroma", "texture", "garnish", "medium"] | 役割 |

```json
{
  "additionalProperties": false,
  "description": "生成の食材入力のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "form_id": {
      "description": "食材形態",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "job_id": {
      "description": "実行",
      "format": "uuid",
      "title": "Job Id",
      "type": "string"
    },
    "role": {
      "description": "役割",
      "enum": [
        "main",
        "support",
        "seasoning",
        "aroma",
        "texture",
        "garnish",
        "medium"
      ],
      "title": "Role",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "job_id",
    "form_id",
    "role",
    "etag"
  ],
  "title": "GenerationFoodRow",
  "type": "object"
}
```

## GenerationFoodWrite

生成の食材入力の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| form_id | string (uuid) | 必須 | 追加制約なし | 食材形態 |
| job_id | string (uuid) | 必須 | 追加制約なし | 実行 |
| role | string | 必須 | enum=["main", "support", "seasoning", "aroma", "texture", "garnish", "medium"] | 役割 |

```json
{
  "additionalProperties": false,
  "description": "生成の食材入力の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "form_id": {
      "description": "食材形態",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "job_id": {
      "description": "実行",
      "format": "uuid",
      "title": "Job Id",
      "type": "string"
    },
    "role": {
      "description": "役割",
      "enum": [
        "main",
        "support",
        "seasoning",
        "aroma",
        "texture",
        "garnish",
        "medium"
      ],
      "title": "Role",
      "type": "string"
    }
  },
  "required": [
    "job_id",
    "form_id",
    "role"
  ],
  "title": "GenerationFoodWrite",
  "type": "object"
}
```

## GenerationInput



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| catalog_release_id | string (uuid) | 必須 | 追加制約なし | Catalog Release Id |
| form_ids | array&lt;string (uuid)&gt; | 必須 | maxItems=1024 | Form Ids |
| option_ids | array&lt;string (uuid)&gt; | 必須 | maxItems=1024 | Option Ids |
| policy_version | string | 必須 | minLength=1; maxLength=200 | Policy Version |
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |

```json
{
  "additionalProperties": false,
  "properties": {
    "catalog_release_id": {
      "format": "uuid",
      "title": "Catalog Release Id",
      "type": "string"
    },
    "form_ids": {
      "items": {
        "format": "uuid",
        "type": "string"
      },
      "maxItems": 1024,
      "title": "Form Ids",
      "type": "array"
    },
    "option_ids": {
      "items": {
        "format": "uuid",
        "type": "string"
      },
      "maxItems": 1024,
      "title": "Option Ids",
      "type": "array"
    },
    "policy_version": {
      "maxLength": 200,
      "minLength": 1,
      "title": "Policy Version",
      "type": "string"
    },
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    }
  },
  "required": [
    "option_ids",
    "form_ids",
    "catalog_release_id",
    "policy_version"
  ],
  "title": "GenerationInput",
  "type": "object"
}
```

## GenerationJobRow

事前生成ジョブのDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| attempt_count | integer | 必須 | minimum=0.0 | 試行回数 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| error_code | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | 失敗分類 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| finished_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 終了 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| idempotency_key | string | 必須 | minLength=64; maxLength=64 | 入力と方針から作る重複キー |
| policy_id | string (uuid) | 必須 | 追加制約なし | 実行方針 |
| seed | anyOf(integer, null) | 必須 | 追加制約なし | 再現用seed |
| started_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 開始 |
| status | string | 必須 | enum=["queued", "running", "succeeded", "failed", "cancelled"] | 進行状態 |

```json
{
  "additionalProperties": false,
  "description": "事前生成ジョブのDB応答。",
  "properties": {
    "attempt_count": {
      "description": "試行回数",
      "minimum": 0.0,
      "title": "Attempt Count",
      "type": "integer"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "error_code": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "失敗分類",
      "title": "Error Code"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "finished_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "終了",
      "title": "Finished At"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "idempotency_key": {
      "description": "入力と方針から作る重複キー",
      "maxLength": 64,
      "minLength": 64,
      "title": "Idempotency Key",
      "type": "string"
    },
    "policy_id": {
      "description": "実行方針",
      "format": "uuid",
      "title": "Policy Id",
      "type": "string"
    },
    "seed": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "description": "再現用seed",
      "title": "Seed"
    },
    "started_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "開始",
      "title": "Started At"
    },
    "status": {
      "description": "進行状態",
      "enum": [
        "queued",
        "running",
        "succeeded",
        "failed",
        "cancelled"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "policy_id",
    "idempotency_key",
    "status",
    "started_at",
    "finished_at",
    "seed",
    "error_code",
    "attempt_count",
    "etag"
  ],
  "title": "GenerationJobRow",
  "type": "object"
}
```

## GenerationJobWrite

事前生成ジョブの編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| attempt_count | integer | 必須 | minimum=0.0 | 試行回数 |
| error_code | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | 失敗分類 |
| finished_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 終了 |
| idempotency_key | string | 必須 | minLength=64; maxLength=64 | 入力と方針から作る重複キー |
| policy_id | string (uuid) | 必須 | 追加制約なし | 実行方針 |
| seed | anyOf(integer, null) | 任意 | 追加制約なし | 再現用seed |
| started_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 開始 |
| status | string | 必須 | enum=["queued", "running", "succeeded", "failed", "cancelled"] | 進行状態 |

```json
{
  "additionalProperties": false,
  "description": "事前生成ジョブの編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "attempt_count": {
      "description": "試行回数",
      "minimum": 0.0,
      "title": "Attempt Count",
      "type": "integer"
    },
    "error_code": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "失敗分類",
      "title": "Error Code"
    },
    "finished_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "終了",
      "title": "Finished At"
    },
    "idempotency_key": {
      "description": "入力と方針から作る重複キー",
      "maxLength": 64,
      "minLength": 64,
      "title": "Idempotency Key",
      "type": "string"
    },
    "policy_id": {
      "description": "実行方針",
      "format": "uuid",
      "title": "Policy Id",
      "type": "string"
    },
    "seed": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "description": "再現用seed",
      "title": "Seed"
    },
    "started_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "開始",
      "title": "Started At"
    },
    "status": {
      "description": "進行状態",
      "enum": [
        "queued",
        "running",
        "succeeded",
        "failed",
        "cancelled"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "policy_id",
    "idempotency_key",
    "status",
    "attempt_count"
  ],
  "title": "GenerationJobWrite",
  "type": "object"
}
```

## GenerationParameters



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| max_output_tokens | integer | 必須 | maximum=1000000.0; exclusiveMinimum=0.0 | Max Output Tokens |
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |
| seed | anyOf(integer, null) | 任意 | 追加制約なし | Seed |
| temperature | number | 必須 | minimum=0.0; maximum=2.0 | Temperature |

```json
{
  "additionalProperties": false,
  "properties": {
    "max_output_tokens": {
      "exclusiveMinimum": 0.0,
      "maximum": 1000000.0,
      "title": "Max Output Tokens",
      "type": "integer"
    },
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    },
    "seed": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "title": "Seed"
    },
    "temperature": {
      "maximum": 2.0,
      "minimum": 0.0,
      "title": "Temperature",
      "type": "number"
    }
  },
  "required": [
    "temperature",
    "max_output_tokens"
  ],
  "title": "GenerationParameters",
  "type": "object"
}
```

## GenerationPolicyRow

AI生成方針版のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| model_identifier | string | 必須 | minLength=1; maxLength=20000 | 利用モデル名・版 |
| parameter_json | GenerationParameters | 必須 | 追加制約なし | temperature/seed等の記録 |
| prompt_template | string | 必須 | minLength=1; maxLength=20000 | 入力テンプレ |
| release_id | string (uuid) | 必須 | 追加制約なし | 候補カタログ版 |
| schema_version | string | 必須 | minLength=1; maxLength=20000 | 出力JSON契約 |
| version | string | 必須 | minLength=1; maxLength=20000 | 方針識別子 |

```json
{
  "additionalProperties": false,
  "description": "AI生成方針版のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "model_identifier": {
      "description": "利用モデル名・版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Model Identifier",
      "type": "string"
    },
    "parameter_json": {
      "$ref": "#/components/schemas/GenerationParameters",
      "description": "temperature/seed等の記録"
    },
    "prompt_template": {
      "description": "入力テンプレ",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Prompt Template",
      "type": "string"
    },
    "release_id": {
      "description": "候補カタログ版",
      "format": "uuid",
      "title": "Release Id",
      "type": "string"
    },
    "schema_version": {
      "description": "出力JSON契約",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Schema Version",
      "type": "string"
    },
    "version": {
      "description": "方針識別子",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Version",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "version",
    "prompt_template",
    "model_identifier",
    "parameter_json",
    "schema_version",
    "release_id",
    "etag"
  ],
  "title": "GenerationPolicyRow",
  "type": "object"
}
```

## GenerationPolicyWrite

AI生成方針版の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| model_identifier | string | 必須 | minLength=1; maxLength=20000 | 利用モデル名・版 |
| parameter_json | GenerationParameters | 必須 | 追加制約なし | temperature/seed等の記録 |
| prompt_template | string | 必須 | minLength=1; maxLength=20000 | 入力テンプレ |
| release_id | string (uuid) | 必須 | 追加制約なし | 候補カタログ版 |
| schema_version | string | 必須 | minLength=1; maxLength=20000 | 出力JSON契約 |
| version | string | 必須 | minLength=1; maxLength=20000 | 方針識別子 |

```json
{
  "additionalProperties": false,
  "description": "AI生成方針版の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "model_identifier": {
      "description": "利用モデル名・版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Model Identifier",
      "type": "string"
    },
    "parameter_json": {
      "$ref": "#/components/schemas/GenerationParameters",
      "description": "temperature/seed等の記録"
    },
    "prompt_template": {
      "description": "入力テンプレ",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Prompt Template",
      "type": "string"
    },
    "release_id": {
      "description": "候補カタログ版",
      "format": "uuid",
      "title": "Release Id",
      "type": "string"
    },
    "schema_version": {
      "description": "出力JSON契約",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Schema Version",
      "type": "string"
    },
    "version": {
      "description": "方針識別子",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Version",
      "type": "string"
    }
  },
  "required": [
    "version",
    "prompt_template",
    "model_identifier",
    "parameter_json",
    "schema_version",
    "release_id"
  ],
  "title": "GenerationPolicyWrite",
  "type": "object"
}
```

## GenerationResultRow

生成結果の出自のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| input_snapshot | GenerationInput | 必須 | 追加制約なし | 確定入力をschema_versionで検証 |
| job_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 短期ジョブ参照 |
| policy_id | string (uuid) | 必須 | 追加制約なし | 恒久方針参照 |
| raw_output_hash | string | 必須 | minLength=64; maxLength=64 | 原出力ハッシュ |
| raw_output_uri | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | 原出力保存先 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 生成した版 |

```json
{
  "additionalProperties": false,
  "description": "生成結果の出自のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "input_snapshot": {
      "$ref": "#/components/schemas/GenerationInput",
      "description": "確定入力をschema_versionで検証"
    },
    "job_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "短期ジョブ参照",
      "title": "Job Id"
    },
    "policy_id": {
      "description": "恒久方針参照",
      "format": "uuid",
      "title": "Policy Id",
      "type": "string"
    },
    "raw_output_hash": {
      "description": "原出力ハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Raw Output Hash",
      "type": "string"
    },
    "raw_output_uri": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "原出力保存先",
      "title": "Raw Output Uri"
    },
    "recipe_version_id": {
      "description": "生成した版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "recipe_version_id",
    "job_id",
    "policy_id",
    "input_snapshot",
    "raw_output_uri",
    "raw_output_hash",
    "etag"
  ],
  "title": "GenerationResultRow",
  "type": "object"
}
```

## GenerationResultWrite

生成結果の出自の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| input_snapshot | GenerationInput | 必須 | 追加制約なし | 確定入力をschema_versionで検証 |
| job_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 短期ジョブ参照 |
| policy_id | string (uuid) | 必須 | 追加制約なし | 恒久方針参照 |
| raw_output_hash | string | 必須 | minLength=64; maxLength=64 | 原出力ハッシュ |
| raw_output_uri | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | 原出力保存先 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 生成した版 |

```json
{
  "additionalProperties": false,
  "description": "生成結果の出自の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "input_snapshot": {
      "$ref": "#/components/schemas/GenerationInput",
      "description": "確定入力をschema_versionで検証"
    },
    "job_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "短期ジョブ参照",
      "title": "Job Id"
    },
    "policy_id": {
      "description": "恒久方針参照",
      "format": "uuid",
      "title": "Policy Id",
      "type": "string"
    },
    "raw_output_hash": {
      "description": "原出力ハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Raw Output Hash",
      "type": "string"
    },
    "raw_output_uri": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "原出力保存先",
      "title": "Raw Output Uri"
    },
    "recipe_version_id": {
      "description": "生成した版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    }
  },
  "required": [
    "recipe_version_id",
    "policy_id",
    "input_snapshot",
    "raw_output_hash"
  ],
  "title": "GenerationResultWrite",
  "type": "object"
}
```

## GenerationShardRow

列挙範囲・リース管理のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時 |
| end_ordinal | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 終了序数(排他的) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| fence_token | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 古い所有者の書込みを拒否 |
| id | string (uuid) | 必須 | 追加制約なし | 不変ID |
| lease_expires_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 有効期限 |
| lease_owner | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | ワーカー識別子 |
| next_ordinal | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 再開位置 |
| start_ordinal | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 開始序数 |
| state | string | 必須 | enum=["queued", "running", "done", "failed"] | 待機/実行/完了/停止 |
| template_id | string (uuid) | 必須 | 追加制約なし | テンプレート版 |

```json
{
  "additionalProperties": false,
  "description": "列挙範囲・リース管理のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "end_ordinal": {
      "description": "終了序数(排他的)",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "End Ordinal",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "fence_token": {
      "description": "古い所有者の書込みを拒否",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Fence Token",
      "type": "string"
    },
    "id": {
      "description": "不変ID",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "lease_expires_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "有効期限",
      "title": "Lease Expires At"
    },
    "lease_owner": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "ワーカー識別子",
      "title": "Lease Owner"
    },
    "next_ordinal": {
      "description": "再開位置",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Next Ordinal",
      "type": "string"
    },
    "start_ordinal": {
      "description": "開始序数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Start Ordinal",
      "type": "string"
    },
    "state": {
      "description": "待機/実行/完了/停止",
      "enum": [
        "queued",
        "running",
        "done",
        "failed"
      ],
      "title": "State",
      "type": "string"
    },
    "template_id": {
      "description": "テンプレート版",
      "format": "uuid",
      "title": "Template Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "template_id",
    "start_ordinal",
    "end_ordinal",
    "next_ordinal",
    "lease_owner",
    "lease_expires_at",
    "fence_token",
    "state",
    "etag"
  ],
  "title": "GenerationShardRow",
  "type": "object"
}
```

## GenerationShardWrite

列挙範囲・リース管理の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| end_ordinal | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 終了序数(排他的) |
| fence_token | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 古い所有者の書込みを拒否 |
| lease_expires_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 有効期限 |
| lease_owner | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | ワーカー識別子 |
| next_ordinal | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 再開位置 |
| start_ordinal | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 開始序数 |
| state | string | 必須 | enum=["queued", "running", "done", "failed"] | 待機/実行/完了/停止 |
| template_id | string (uuid) | 必須 | 追加制約なし | テンプレート版 |

```json
{
  "additionalProperties": false,
  "description": "列挙範囲・リース管理の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "end_ordinal": {
      "description": "終了序数(排他的)",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "End Ordinal",
      "type": "string"
    },
    "fence_token": {
      "description": "古い所有者の書込みを拒否",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Fence Token",
      "type": "string"
    },
    "lease_expires_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "有効期限",
      "title": "Lease Expires At"
    },
    "lease_owner": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "ワーカー識別子",
      "title": "Lease Owner"
    },
    "next_ordinal": {
      "description": "再開位置",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Next Ordinal",
      "type": "string"
    },
    "start_ordinal": {
      "description": "開始序数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Start Ordinal",
      "type": "string"
    },
    "state": {
      "description": "待機/実行/完了/停止",
      "enum": [
        "queued",
        "running",
        "done",
        "failed"
      ],
      "title": "State",
      "type": "string"
    },
    "template_id": {
      "description": "テンプレート版",
      "format": "uuid",
      "title": "Template Id",
      "type": "string"
    }
  },
  "required": [
    "template_id",
    "start_ordinal",
    "end_ordinal",
    "next_ordinal",
    "fence_token",
    "state"
  ],
  "title": "GenerationShardWrite",
  "type": "object"
}
```

## GenerationStratumMetricRow

採用率・飽和度の実測のDB応答。

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

```json
{
  "additionalProperties": false,
  "description": "採用率・飽和度の実測のDB応答。",
  "properties": {
    "attempted": {
      "description": "試行数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Attempted",
      "type": "string"
    },
    "cost_amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "同一通貨の費用",
      "title": "Cost Amount"
    },
    "created_at": {
      "description": "作成日時",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "currency": {
      "anyOf": [
        {
          "maxLength": 3,
          "minLength": 3,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "JPY/USD等",
      "title": "Currency"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変ID",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "input_tokens": {
      "description": "入力トークン合計",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Input Tokens",
      "type": "string"
    },
    "output_tokens": {
      "description": "出力トークン合計",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Output Tokens",
      "type": "string"
    },
    "publishable": {
      "description": "公開基準通過数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Publishable",
      "type": "string"
    },
    "stratum_key": {
      "description": "層の安定キー(料理構造x食品カテゴリx入手性)。集計定義はテンプレート版に固定",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Stratum Key",
      "type": "string"
    },
    "template_id": {
      "description": "対象テンプレート",
      "format": "uuid",
      "title": "Template Id",
      "type": "string"
    },
    "unique_count": {
      "description": "既存集合との差分数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Unique Count",
      "type": "string"
    },
    "valid": {
      "description": "適合生成数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Valid",
      "type": "string"
    },
    "window_end": {
      "description": "計測窓終了",
      "format": "date-time",
      "title": "Window End",
      "type": "string"
    },
    "window_start": {
      "description": "計測窓開始",
      "format": "date-time",
      "title": "Window Start",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "template_id",
    "window_start",
    "window_end",
    "attempted",
    "valid",
    "unique_count",
    "publishable",
    "input_tokens",
    "output_tokens",
    "cost_amount",
    "currency",
    "stratum_key",
    "etag"
  ],
  "title": "GenerationStratumMetricRow",
  "type": "object"
}
```

## GenerationStratumMetricWrite

採用率・飽和度の実測の編集可能列。未指定NULL列はNULLにする。

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

```json
{
  "additionalProperties": false,
  "description": "採用率・飽和度の実測の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "attempted": {
      "description": "試行数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Attempted",
      "type": "string"
    },
    "cost_amount": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "同一通貨の費用",
      "title": "Cost Amount"
    },
    "currency": {
      "anyOf": [
        {
          "maxLength": 3,
          "minLength": 3,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "JPY/USD等",
      "title": "Currency"
    },
    "input_tokens": {
      "description": "入力トークン合計",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Input Tokens",
      "type": "string"
    },
    "output_tokens": {
      "description": "出力トークン合計",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Output Tokens",
      "type": "string"
    },
    "publishable": {
      "description": "公開基準通過数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Publishable",
      "type": "string"
    },
    "stratum_key": {
      "description": "層の安定キー(料理構造x食品カテゴリx入手性)。集計定義はテンプレート版に固定",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Stratum Key",
      "type": "string"
    },
    "template_id": {
      "description": "対象テンプレート",
      "format": "uuid",
      "title": "Template Id",
      "type": "string"
    },
    "unique_count": {
      "description": "既存集合との差分数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Unique Count",
      "type": "string"
    },
    "valid": {
      "description": "適合生成数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Valid",
      "type": "string"
    },
    "window_end": {
      "description": "計測窓終了",
      "format": "date-time",
      "title": "Window End",
      "type": "string"
    },
    "window_start": {
      "description": "計測窓開始",
      "format": "date-time",
      "title": "Window Start",
      "type": "string"
    }
  },
  "required": [
    "template_id",
    "window_start",
    "window_end",
    "attempted",
    "valid",
    "unique_count",
    "publishable",
    "input_tokens",
    "output_tokens",
    "stratum_key"
  ],
  "title": "GenerationStratumMetricWrite",
  "type": "object"
}
```

## GenerationTemplateContract



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| flavor_codes | array&lt;string&gt; | 必須 | maxItems=1000 | Flavor Codes |
| normalizer_version | string | 必須 | minLength=1; maxLength=200 | Normalizer Version |
| primary_identity_ids | array&lt;string (uuid)&gt; | 必須 | maxItems=10000 | Primary Identity Ids |
| route_codes | array&lt;string&gt; | 必須 | maxItems=1000 | Route Codes |
| schema_version | integer | 任意 | const=2; default=2 | Schema Version |
| support_identity_ids | array&lt;string (uuid)&gt; | 必須 | maxItems=10000 | Support Identity Ids |
| support_identity_sets | anyOf(array&lt;array&lt;string (uuid)&gt;&gt;, null) | 任意 | anyOfの制約=array&lt;array&lt;string (uuid)&gt;&gt;: maxItems=10000; 要素の制約=maxItems=3 | Support Identity Sets |
| support_k | array&lt;integer&gt; | 必須 | maxItems=4; 要素の制約=enum=[0, 1, 2, 3] | Support K |

```json
{
  "additionalProperties": false,
  "properties": {
    "flavor_codes": {
      "items": {
        "type": "string"
      },
      "maxItems": 1000,
      "title": "Flavor Codes",
      "type": "array"
    },
    "normalizer_version": {
      "maxLength": 200,
      "minLength": 1,
      "title": "Normalizer Version",
      "type": "string"
    },
    "primary_identity_ids": {
      "items": {
        "format": "uuid",
        "type": "string"
      },
      "maxItems": 10000,
      "title": "Primary Identity Ids",
      "type": "array"
    },
    "route_codes": {
      "items": {
        "type": "string"
      },
      "maxItems": 1000,
      "title": "Route Codes",
      "type": "array"
    },
    "schema_version": {
      "const": 2,
      "default": 2,
      "title": "Schema Version",
      "type": "integer"
    },
    "support_identity_ids": {
      "items": {
        "format": "uuid",
        "type": "string"
      },
      "maxItems": 10000,
      "title": "Support Identity Ids",
      "type": "array"
    },
    "support_identity_sets": {
      "anyOf": [
        {
          "items": {
            "items": {
              "format": "uuid",
              "type": "string"
            },
            "maxItems": 3,
            "type": "array"
          },
          "maxItems": 10000,
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "title": "Support Identity Sets"
    },
    "support_k": {
      "items": {
        "enum": [
          0,
          1,
          2,
          3
        ],
        "type": "integer"
      },
      "maxItems": 4,
      "title": "Support K",
      "type": "array"
    }
  },
  "required": [
    "primary_identity_ids",
    "support_identity_ids",
    "support_k",
    "flavor_codes",
    "route_codes",
    "normalizer_version"
  ],
  "title": "GenerationTemplateContract",
  "type": "object"
}
```

## GenerationTemplateRow

列挙テンプレート版のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| candidate_count | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | この定義の正確な設計点数 |
| code | string | 必須 | minLength=1; maxLength=20000 | テンプレートコード |
| contract | GenerationTemplateContract | 必須 | 追加制約なし | 主副材の許可集合・k・味付・経路 |
| contract_hash | string | 必須 | minLength=64; maxLength=64 | 定義ハッシュ |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変ID |
| release_id | string (uuid) | 必須 | 追加制約なし | カタログ版 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 定義版 |

```json
{
  "additionalProperties": false,
  "description": "列挙テンプレート版のDB応答。",
  "properties": {
    "candidate_count": {
      "description": "この定義の正確な設計点数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Candidate Count",
      "type": "string"
    },
    "code": {
      "description": "テンプレートコード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "contract": {
      "$ref": "#/components/schemas/GenerationTemplateContract",
      "description": "主副材の許可集合・k・味付・経路"
    },
    "contract_hash": {
      "description": "定義ハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Contract Hash",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変ID",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "release_id": {
      "description": "カタログ版",
      "format": "uuid",
      "title": "Release Id",
      "type": "string"
    },
    "version": {
      "description": "定義版",
      "exclusiveMinimum": 0.0,
      "title": "Version",
      "type": "integer"
    }
  },
  "required": [
    "id",
    "created_at",
    "code",
    "version",
    "release_id",
    "contract",
    "candidate_count",
    "contract_hash",
    "etag"
  ],
  "title": "GenerationTemplateRow",
  "type": "object"
}
```

## GenerationTemplateWrite

列挙テンプレート版の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| candidate_count | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | この定義の正確な設計点数 |
| code | string | 必須 | minLength=1; maxLength=20000 | テンプレートコード |
| contract | GenerationTemplateContract | 必須 | 追加制約なし | 主副材の許可集合・k・味付・経路 |
| contract_hash | string | 必須 | minLength=64; maxLength=64 | 定義ハッシュ |
| release_id | string (uuid) | 必須 | 追加制約なし | カタログ版 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 定義版 |

```json
{
  "additionalProperties": false,
  "description": "列挙テンプレート版の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "candidate_count": {
      "description": "この定義の正確な設計点数",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Candidate Count",
      "type": "string"
    },
    "code": {
      "description": "テンプレートコード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "contract": {
      "$ref": "#/components/schemas/GenerationTemplateContract",
      "description": "主副材の許可集合・k・味付・経路"
    },
    "contract_hash": {
      "description": "定義ハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Contract Hash",
      "type": "string"
    },
    "release_id": {
      "description": "カタログ版",
      "format": "uuid",
      "title": "Release Id",
      "type": "string"
    },
    "version": {
      "description": "定義版",
      "exclusiveMinimum": 0.0,
      "title": "Version",
      "type": "integer"
    }
  },
  "required": [
    "code",
    "version",
    "release_id",
    "contract",
    "candidate_count",
    "contract_hash"
  ],
  "title": "GenerationTemplateWrite",
  "type": "object"
}
```

## HTTPValidationError



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| detail | array&lt;ValidationError&gt; | 任意 | 追加制約なし | Detail |

```json
{
  "properties": {
    "detail": {
      "items": {
        "$ref": "#/components/schemas/ValidationError"
      },
      "title": "Detail",
      "type": "array"
    }
  },
  "title": "HTTPValidationError",
  "type": "object"
}
```

## HealthResponse



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| catalog | string | 任意 | const="sample"; default="sample" | Catalog |
| cloudSync | string | 任意 | const="not-deployed"; default="not-deployed" | Cloudsync |
| status | string | 任意 | const="ok"; default="ok" | Status |

```json
{
  "additionalProperties": false,
  "properties": {
    "catalog": {
      "const": "sample",
      "default": "sample",
      "title": "Catalog",
      "type": "string"
    },
    "cloudSync": {
      "const": "not-deployed",
      "default": "not-deployed",
      "title": "Cloudsync",
      "type": "string"
    },
    "status": {
      "const": "ok",
      "default": "ok",
      "title": "Status",
      "type": "string"
    }
  },
  "title": "HealthResponse",
  "type": "object"
}
```

## IngredientRatio-Input



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount_per_serving | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Amount Per Serving |
| form_id | string (uuid) | 必須 | 追加制約なし | Form Id |
| unit_id | string (uuid) | 必須 | 追加制約なし | Unit Id |

```json
{
  "additionalProperties": false,
  "properties": {
    "amount_per_serving": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
          "type": "string"
        }
      ],
      "title": "Amount Per Serving"
    },
    "form_id": {
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "unit_id": {
      "format": "uuid",
      "title": "Unit Id",
      "type": "string"
    }
  },
  "required": [
    "form_id",
    "amount_per_serving",
    "unit_id"
  ],
  "title": "IngredientRatio",
  "type": "object"
}
```

## IngredientRatio-Output



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount_per_serving | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Amount Per Serving |
| form_id | string (uuid) | 必須 | 追加制約なし | Form Id |
| unit_id | string (uuid) | 必須 | 追加制約なし | Unit Id |

```json
{
  "additionalProperties": false,
  "properties": {
    "amount_per_serving": {
      "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
      "title": "Amount Per Serving",
      "type": "string"
    },
    "form_id": {
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "unit_id": {
      "format": "uuid",
      "title": "Unit Id",
      "type": "string"
    }
  },
  "required": [
    "form_id",
    "amount_per_serving",
    "unit_id"
  ],
  "title": "IngredientRatio",
  "type": "object"
}
```

## IngredientTotalRow

献立材料集計結果のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| actual_amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 利用者が確定した実使用量。不明はNULL |
| calculation_version | string | 必須 | minLength=1; maxLength=20000 | 計算器版 |
| consumption_outcome | string | 必須 | minLength=1; maxLength=20000 | 未要求・反映済み・在庫不足・数量不明・単位不一致の結果 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| form_id | string (uuid) | 必須 | 追加制約なし | 合算可能な形態 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| product_version_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 商品固定 |
| quality | string | 必須 | enum=["measured", "manufacturer", "reference", "estimated", "unknown"] | 最も低い入力精度 |
| required_amount | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 必要量 |
| session_id | string (uuid) | 必須 | 追加制約なし | 固定計算対象 |
| unit_id | string (uuid) | 必須 | 追加制約なし | 基準単位 |

```json
{
  "additionalProperties": false,
  "description": "献立材料集計結果のDB応答。",
  "properties": {
    "actual_amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "利用者が確定した実使用量。不明はNULL",
      "title": "Actual Amount"
    },
    "calculation_version": {
      "description": "計算器版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Calculation Version",
      "type": "string"
    },
    "consumption_outcome": {
      "description": "未要求・反映済み・在庫不足・数量不明・単位不一致の結果",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Consumption Outcome",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "form_id": {
      "description": "合算可能な形態",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "product_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "商品固定",
      "title": "Product Version Id"
    },
    "quality": {
      "description": "最も低い入力精度",
      "enum": [
        "measured",
        "manufacturer",
        "reference",
        "estimated",
        "unknown"
      ],
      "title": "Quality",
      "type": "string"
    },
    "required_amount": {
      "description": "必要量",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Required Amount",
      "type": "string"
    },
    "session_id": {
      "description": "固定計算対象",
      "format": "uuid",
      "title": "Session Id",
      "type": "string"
    },
    "unit_id": {
      "description": "基準単位",
      "format": "uuid",
      "title": "Unit Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "session_id",
    "form_id",
    "product_version_id",
    "unit_id",
    "required_amount",
    "quality",
    "calculation_version",
    "actual_amount",
    "consumption_outcome",
    "etag"
  ],
  "title": "IngredientTotalRow",
  "type": "object"
}
```

## KitchenResourceRow

キッチンの実資源のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| active | boolean | 必須 | 追加制約なし | 新規の調理計画で利用する資源か |
| capacity | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 容量 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| name | string | 必須 | minLength=1; maxLength=20000 | 左コンロ・26cmフライパン等 |
| quantity | integer | 必須 | exclusiveMinimum=0.0 | 同等資源数 |
| resource_type_id | string (uuid) | 必須 | 追加制約なし | コンロ・鍋・人等 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "キッチンの実資源のDB応答。",
  "properties": {
    "active": {
      "description": "新規の調理計画で利用する資源か",
      "title": "Active",
      "type": "boolean"
    },
    "capacity": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "容量",
      "title": "Capacity"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "name": {
      "description": "左コンロ・26cmフライパン等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "quantity": {
      "description": "同等資源数",
      "exclusiveMinimum": 0.0,
      "title": "Quantity",
      "type": "integer"
    },
    "resource_type_id": {
      "description": "コンロ・鍋・人等",
      "format": "uuid",
      "title": "Resource Type Id",
      "type": "string"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "user_id",
    "resource_type_id",
    "name",
    "capacity",
    "quantity",
    "active",
    "etag"
  ],
  "title": "KitchenResourceRow",
  "type": "object"
}
```

## KitchenResourceWrite

キッチンの実資源の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| active | boolean | 必須 | 追加制約なし | 新規の調理計画で利用する資源か |
| capacity | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 容量 |
| name | string | 必須 | minLength=1; maxLength=20000 | 左コンロ・26cmフライパン等 |
| quantity | integer | 必須 | exclusiveMinimum=0.0 | 同等資源数 |
| resource_type_id | string (uuid) | 必須 | 追加制約なし | コンロ・鍋・人等 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "キッチンの実資源の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "active": {
      "description": "新規の調理計画で利用する資源か",
      "title": "Active",
      "type": "boolean"
    },
    "capacity": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "容量",
      "title": "Capacity"
    },
    "name": {
      "description": "左コンロ・26cmフライパン等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "quantity": {
      "description": "同等資源数",
      "exclusiveMinimum": 0.0,
      "title": "Quantity",
      "type": "integer"
    },
    "resource_type_id": {
      "description": "コンロ・鍋・人等",
      "format": "uuid",
      "title": "Resource Type Id",
      "type": "string"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "user_id",
    "resource_type_id",
    "name",
    "quantity",
    "active"
  ],
  "title": "KitchenResourceWrite",
  "type": "object"
}
```

## LoginRequest



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| password | string | 必須 | minLength=1; maxLength=200 | Password |
| username | string | 必須 | minLength=1; maxLength=50 | Username |

```json
{
  "additionalProperties": false,
  "properties": {
    "password": {
      "maxLength": 200,
      "minLength": 1,
      "title": "Password",
      "type": "string"
    },
    "username": {
      "maxLength": 50,
      "minLength": 1,
      "title": "Username",
      "type": "string"
    }
  },
  "required": [
    "username",
    "password"
  ],
  "title": "LoginRequest",
  "type": "object"
}
```

## LoginResponse



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| access_token | string | 必須 | 追加制約なし | Access Token |
| token_type | string | 任意 | default="bearer" | Token Type |
| user | UserProfile | 必須 | 追加制約なし |  |

```json
{
  "properties": {
    "access_token": {
      "title": "Access Token",
      "type": "string"
    },
    "token_type": {
      "default": "bearer",
      "title": "Token Type",
      "type": "string"
    },
    "user": {
      "$ref": "#/components/schemas/UserProfile"
    }
  },
  "required": [
    "access_token",
    "user"
  ],
  "title": "LoginResponse",
  "type": "object"
}
```

## MaterialNodeRow

材料・中間物節点のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 予定生成量 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| ingredient_line_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 原材料明細 |
| kind | string | 必須 | enum=["ingredient", "intermediate", "dish", "waste"] | 入力/中間/完成/廃棄 |
| name | string | 必須 | minLength=1; maxLength=20000 | 切ったにんじん・合わせ調味料等 |
| producer_step_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 生成工程 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 親版 |
| unit_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 生成量単位 |

```json
{
  "additionalProperties": false,
  "description": "材料・中間物節点のDB応答。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "予定生成量",
      "title": "Amount"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "ingredient_line_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "原材料明細",
      "title": "Ingredient Line Id"
    },
    "kind": {
      "description": "入力/中間/完成/廃棄",
      "enum": [
        "ingredient",
        "intermediate",
        "dish",
        "waste"
      ],
      "title": "Kind",
      "type": "string"
    },
    "name": {
      "description": "切ったにんじん・合わせ調味料等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "producer_step_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "生成工程",
      "title": "Producer Step Id"
    },
    "recipe_version_id": {
      "description": "親版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "生成量単位",
      "title": "Unit Id"
    }
  },
  "required": [
    "id",
    "created_at",
    "recipe_version_id",
    "name",
    "kind",
    "ingredient_line_id",
    "producer_step_id",
    "amount",
    "unit_id",
    "etag"
  ],
  "title": "MaterialNodeRow",
  "type": "object"
}
```

## MaterialNodeWrite

材料・中間物節点の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 予定生成量 |
| ingredient_line_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 原材料明細 |
| kind | string | 必須 | enum=["ingredient", "intermediate", "dish", "waste"] | 入力/中間/完成/廃棄 |
| name | string | 必須 | minLength=1; maxLength=20000 | 切ったにんじん・合わせ調味料等 |
| producer_step_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 生成工程 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 親版 |
| unit_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 生成量単位 |

```json
{
  "additionalProperties": false,
  "description": "材料・中間物節点の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "予定生成量",
      "title": "Amount"
    },
    "ingredient_line_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "原材料明細",
      "title": "Ingredient Line Id"
    },
    "kind": {
      "description": "入力/中間/完成/廃棄",
      "enum": [
        "ingredient",
        "intermediate",
        "dish",
        "waste"
      ],
      "title": "Kind",
      "type": "string"
    },
    "name": {
      "description": "切ったにんじん・合わせ調味料等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "producer_step_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "生成工程",
      "title": "Producer Step Id"
    },
    "recipe_version_id": {
      "description": "親版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "生成量単位",
      "title": "Unit Id"
    }
  },
  "required": [
    "recipe_version_id",
    "name",
    "kind"
  ],
  "title": "MaterialNodeWrite",
  "type": "object"
}
```

## MealItem



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| adjusted | boolean | 必須 | 追加制約なし | Adjusted |
| amounts | object | 必須 | additionalProperties={"$ref": "#/components/schemas/Quantity"} | Amounts |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| recipeId | string | 必須 | minLength=1; maxLength=128 | Recipeid |
| recipeVersionId | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=128 | Recipeversionid |
| servings | number | 必須 | maximum=1000.0; exclusiveMinimum=0.0 | Servings |

```json
{
  "additionalProperties": false,
  "properties": {
    "adjusted": {
      "title": "Adjusted",
      "type": "boolean"
    },
    "amounts": {
      "additionalProperties": {
        "$ref": "#/components/schemas/Quantity"
      },
      "propertyNames": {
        "maxLength": 128,
        "minLength": 1
      },
      "title": "Amounts",
      "type": "object"
    },
    "id": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Id",
      "type": "string"
    },
    "recipeId": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Recipeid",
      "type": "string"
    },
    "recipeVersionId": {
      "anyOf": [
        {
          "maxLength": 128,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Recipeversionid"
    },
    "servings": {
      "exclusiveMinimum": 0.0,
      "maximum": 1000.0,
      "title": "Servings",
      "type": "number"
    }
  },
  "required": [
    "recipeId",
    "servings",
    "amounts",
    "adjusted",
    "id"
  ],
  "title": "MealItem",
  "type": "object"
}
```

## MediaAssetRow

教育用動画等の版のDB応答。

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

```json
{
  "additionalProperties": false,
  "description": "教育用動画等の版のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "locale": {
      "description": "字幕言語",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Locale",
      "type": "string"
    },
    "media_type": {
      "description": "動画/アニメ/画像",
      "enum": [
        "video",
        "animation",
        "image"
      ],
      "title": "Media Type",
      "type": "string"
    },
    "operation_id": {
      "description": "説明する標準動作",
      "format": "uuid",
      "title": "Operation Id",
      "type": "string"
    },
    "parameter_contract": {
      "$ref": "#/components/schemas/MediaParameters-Output",
      "description": "対応厚み・食材形状・視点"
    },
    "sha256": {
      "description": "資産ハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Sha256",
      "type": "string"
    },
    "source_id": {
      "description": "権利・作成根拠",
      "format": "uuid",
      "title": "Source Id",
      "type": "string"
    },
    "uri": {
      "description": "オブジェクト格納先",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Uri",
      "type": "string"
    },
    "validation": {
      "description": "内容検証",
      "enum": [
        "pending",
        "passed",
        "failed",
        "needs_review"
      ],
      "title": "Validation",
      "type": "string"
    },
    "version": {
      "description": "媒体版",
      "exclusiveMinimum": 0.0,
      "title": "Version",
      "type": "integer"
    }
  },
  "required": [
    "id",
    "created_at",
    "operation_id",
    "media_type",
    "uri",
    "sha256",
    "locale",
    "version",
    "parameter_contract",
    "source_id",
    "validation",
    "etag"
  ],
  "title": "MediaAssetRow",
  "type": "object"
}
```

## MediaAssetWrite

教育用動画等の版の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| locale | string | 必須 | minLength=1; maxLength=20000 | 字幕言語 |
| media_type | string | 必須 | enum=["video", "animation", "image"] | 動画/アニメ/画像 |
| operation_id | string (uuid) | 必須 | 追加制約なし | 説明する標準動作 |
| parameter_contract | MediaParameters-Input | 必須 | 追加制約なし | 対応厚み・食材形状・視点 |
| sha256 | string | 必須 | minLength=64; maxLength=64 | 資産ハッシュ |
| source_id | string (uuid) | 必須 | 追加制約なし | 権利・作成根拠 |
| uri | string | 必須 | minLength=1; maxLength=20000 | オブジェクト格納先 |
| validation | string | 必須 | enum=["pending", "passed", "failed", "needs_review"] | 内容検証 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 媒体版 |

```json
{
  "additionalProperties": false,
  "description": "教育用動画等の版の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "locale": {
      "description": "字幕言語",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Locale",
      "type": "string"
    },
    "media_type": {
      "description": "動画/アニメ/画像",
      "enum": [
        "video",
        "animation",
        "image"
      ],
      "title": "Media Type",
      "type": "string"
    },
    "operation_id": {
      "description": "説明する標準動作",
      "format": "uuid",
      "title": "Operation Id",
      "type": "string"
    },
    "parameter_contract": {
      "$ref": "#/components/schemas/MediaParameters-Input",
      "description": "対応厚み・食材形状・視点"
    },
    "sha256": {
      "description": "資産ハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Sha256",
      "type": "string"
    },
    "source_id": {
      "description": "権利・作成根拠",
      "format": "uuid",
      "title": "Source Id",
      "type": "string"
    },
    "uri": {
      "description": "オブジェクト格納先",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Uri",
      "type": "string"
    },
    "validation": {
      "description": "内容検証",
      "enum": [
        "pending",
        "passed",
        "failed",
        "needs_review"
      ],
      "title": "Validation",
      "type": "string"
    },
    "version": {
      "description": "媒体版",
      "exclusiveMinimum": 0.0,
      "title": "Version",
      "type": "integer"
    }
  },
  "required": [
    "operation_id",
    "media_type",
    "uri",
    "sha256",
    "locale",
    "version",
    "parameter_contract",
    "source_id",
    "validation"
  ],
  "title": "MediaAssetWrite",
  "type": "object"
}
```

## MediaParameters-Input



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |
| shape | string | 必須 | enum=["cylinder", "leaf", "block", "irregular"] | Shape |
| thickness_mm | anyOf(RangeValue-Input, null) | 任意 | 追加制約なし |  |
| view | string | 必須 | enum=["overhead", "side", "close_up"] | View |

```json
{
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    },
    "shape": {
      "enum": [
        "cylinder",
        "leaf",
        "block",
        "irregular"
      ],
      "title": "Shape",
      "type": "string"
    },
    "thickness_mm": {
      "anyOf": [
        {
          "$ref": "#/components/schemas/RangeValue-Input"
        },
        {
          "type": "null"
        }
      ]
    },
    "view": {
      "enum": [
        "overhead",
        "side",
        "close_up"
      ],
      "title": "View",
      "type": "string"
    }
  },
  "required": [
    "shape",
    "view"
  ],
  "title": "MediaParameters",
  "type": "object"
}
```

## MediaParameters-Output



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |
| shape | string | 必須 | enum=["cylinder", "leaf", "block", "irregular"] | Shape |
| thickness_mm | anyOf(RangeValue-Output, null) | 任意 | 追加制約なし |  |
| view | string | 必須 | enum=["overhead", "side", "close_up"] | View |

```json
{
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    },
    "shape": {
      "enum": [
        "cylinder",
        "leaf",
        "block",
        "irregular"
      ],
      "title": "Shape",
      "type": "string"
    },
    "thickness_mm": {
      "anyOf": [
        {
          "$ref": "#/components/schemas/RangeValue-Output"
        },
        {
          "type": "null"
        }
      ]
    },
    "view": {
      "enum": [
        "overhead",
        "side",
        "close_up"
      ],
      "title": "View",
      "type": "string"
    }
  },
  "required": [
    "shape",
    "view"
  ],
  "title": "MediaParameters",
  "type": "object"
}
```

## MenuIngredientOverrideRow

献立別材料確定のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 適量等の確定基準量 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| form_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 明示的代替形態 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| ingredient_line_id | string (uuid) | 必須 | 追加制約なし | 元材料行 |
| menu_item_id | string (uuid) | 必須 | 追加制約なし | 対象料理 |
| product_version_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 購入商品指定 |
| selected | boolean | 必須 | 追加制約なし | 任意材料を使うか |

```json
{
  "additionalProperties": false,
  "description": "献立別材料確定のDB応答。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "適量等の確定基準量",
      "title": "Amount"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "form_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "明示的代替形態",
      "title": "Form Id"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "ingredient_line_id": {
      "description": "元材料行",
      "format": "uuid",
      "title": "Ingredient Line Id",
      "type": "string"
    },
    "menu_item_id": {
      "description": "対象料理",
      "format": "uuid",
      "title": "Menu Item Id",
      "type": "string"
    },
    "product_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入商品指定",
      "title": "Product Version Id"
    },
    "selected": {
      "description": "任意材料を使うか",
      "title": "Selected",
      "type": "boolean"
    }
  },
  "required": [
    "id",
    "created_at",
    "menu_item_id",
    "ingredient_line_id",
    "selected",
    "amount",
    "form_id",
    "product_version_id",
    "etag"
  ],
  "title": "MenuIngredientOverrideRow",
  "type": "object"
}
```

## MenuIngredientOverrideWrite

献立別材料確定の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 適量等の確定基準量 |
| form_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 明示的代替形態 |
| ingredient_line_id | string (uuid) | 必須 | 追加制約なし | 元材料行 |
| menu_item_id | string (uuid) | 必須 | 追加制約なし | 対象料理 |
| product_version_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 購入商品指定 |
| selected | boolean | 必須 | 追加制約なし | 任意材料を使うか |

```json
{
  "additionalProperties": false,
  "description": "献立別材料確定の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "適量等の確定基準量",
      "title": "Amount"
    },
    "form_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "明示的代替形態",
      "title": "Form Id"
    },
    "ingredient_line_id": {
      "description": "元材料行",
      "format": "uuid",
      "title": "Ingredient Line Id",
      "type": "string"
    },
    "menu_item_id": {
      "description": "対象料理",
      "format": "uuid",
      "title": "Menu Item Id",
      "type": "string"
    },
    "product_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入商品指定",
      "title": "Product Version Id"
    },
    "selected": {
      "description": "任意材料を使うか",
      "title": "Selected",
      "type": "boolean"
    }
  },
  "required": [
    "menu_item_id",
    "ingredient_line_id",
    "selected"
  ],
  "title": "MenuIngredientOverrideWrite",
  "type": "object"
}
```

## MenuItemRequest



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9007199254740990.0 | Expectedversion |
| item | MealItem | 必須 | 追加制約なし |  |

```json
{
  "additionalProperties": false,
  "properties": {
    "expectedVersion": {
      "maximum": 9007199254740990.0,
      "minimum": 0.0,
      "title": "Expectedversion",
      "type": "integer"
    },
    "item": {
      "$ref": "#/components/schemas/MealItem"
    }
  },
  "required": [
    "expectedVersion",
    "item"
  ],
  "title": "MenuItemRequest",
  "type": "object"
}
```

## MenuItemRow

献立の料理のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| menu_id | string (uuid) | 必須 | 追加制約なし | 献立 |
| position | integer | 必須 | exclusiveMinimum=0.0 | 表示順 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 固定レシピ版 |
| role_option_id | string (uuid) | 必須 | 追加制約なし | 主菜等 |
| servings | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | その料理を作る人数 |

```json
{
  "additionalProperties": false,
  "description": "献立の料理のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "menu_id": {
      "description": "献立",
      "format": "uuid",
      "title": "Menu Id",
      "type": "string"
    },
    "position": {
      "description": "表示順",
      "exclusiveMinimum": 0.0,
      "title": "Position",
      "type": "integer"
    },
    "recipe_version_id": {
      "description": "固定レシピ版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "role_option_id": {
      "description": "主菜等",
      "format": "uuid",
      "title": "Role Option Id",
      "type": "string"
    },
    "servings": {
      "description": "その料理を作る人数",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Servings",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "menu_id",
    "recipe_version_id",
    "servings",
    "role_option_id",
    "position",
    "etag"
  ],
  "title": "MenuItemRow",
  "type": "object"
}
```

## MenuItemWrite

献立の料理の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| menu_id | string (uuid) | 必須 | 追加制約なし | 献立 |
| position | integer | 必須 | exclusiveMinimum=0.0 | 表示順 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 固定レシピ版 |
| role_option_id | string (uuid) | 必須 | 追加制約なし | 主菜等 |
| servings | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | その料理を作る人数 |

```json
{
  "additionalProperties": false,
  "description": "献立の料理の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "menu_id": {
      "description": "献立",
      "format": "uuid",
      "title": "Menu Id",
      "type": "string"
    },
    "position": {
      "description": "表示順",
      "exclusiveMinimum": 0.0,
      "title": "Position",
      "type": "integer"
    },
    "recipe_version_id": {
      "description": "固定レシピ版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "role_option_id": {
      "description": "主菜等",
      "format": "uuid",
      "title": "Role Option Id",
      "type": "string"
    },
    "servings": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "その料理を作る人数",
      "title": "Servings"
    }
  },
  "required": [
    "menu_id",
    "recipe_version_id",
    "servings",
    "role_option_id",
    "position"
  ],
  "title": "MenuItemWrite",
  "type": "object"
}
```

## MenuRow

献立のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| name | string | 必須 | minLength=1; maxLength=20000 | 献立名 |
| revision | integer | 必須 | exclusiveMinimum=0.0 | 楽観ロック版 |
| servings | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 標準人数 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "献立のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "name": {
      "description": "献立名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "revision": {
      "description": "楽観ロック版",
      "exclusiveMinimum": 0.0,
      "title": "Revision",
      "type": "integer"
    },
    "servings": {
      "description": "標準人数",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Servings",
      "type": "string"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "user_id",
    "name",
    "servings",
    "revision",
    "etag"
  ],
  "title": "MenuRow",
  "type": "object"
}
```

## MenuWrite

献立の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| name | string | 必須 | minLength=1; maxLength=20000 | 献立名 |
| servings | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 標準人数 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "献立の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "name": {
      "description": "献立名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "servings": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "標準人数",
      "title": "Servings"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "user_id",
    "name",
    "servings"
  ],
  "title": "MenuWrite",
  "type": "object"
}
```

## NutrientRow

栄養成分種別のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | energy_kcal等 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| name | string | 必須 | minLength=1; maxLength=20000 | エネルギー等 |
| unit_label | string | 必須 | minLength=1; maxLength=20000 | kcal/g/mg/μg |

```json
{
  "additionalProperties": false,
  "description": "栄養成分種別のDB応答。",
  "properties": {
    "code": {
      "description": "energy_kcal等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "name": {
      "description": "エネルギー等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "unit_label": {
      "description": "kcal/g/mg/μg",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Unit Label",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "code",
    "name",
    "unit_label",
    "etag"
  ],
  "title": "NutrientRow",
  "type": "object"
}
```

## NutrientWrite

栄養成分種別の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | energy_kcal等 |
| name | string | 必須 | minLength=1; maxLength=20000 | エネルギー等 |
| unit_label | string | 必須 | minLength=1; maxLength=20000 | kcal/g/mg/μg |

```json
{
  "additionalProperties": false,
  "description": "栄養成分種別の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "code": {
      "description": "energy_kcal等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "name": {
      "description": "エネルギー等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "unit_label": {
      "description": "kcal/g/mg/μg",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Unit Label",
      "type": "string"
    }
  },
  "required": [
    "code",
    "name",
    "unit_label"
  ],
  "title": "NutrientWrite",
  "type": "object"
}
```

## NutritionFactRow

形態・商品別栄養値のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 基準量あたり成分量 |
| basis_amount | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 基準量 |
| basis_unit_id | string (uuid) | 必須 | 追加制約なし | 基準単位 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| form_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 汎用形態 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| nutrient_id | string (uuid) | 必須 | 追加制約なし | 栄養成分 |
| product_version_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 商品仕様 |
| source_id | string (uuid) | 必須 | 追加制約なし | 出典 |

```json
{
  "additionalProperties": false,
  "description": "形態・商品別栄養値のDB応答。",
  "properties": {
    "amount": {
      "description": "基準量あたり成分量",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Amount",
      "type": "string"
    },
    "basis_amount": {
      "description": "基準量",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Basis Amount",
      "type": "string"
    },
    "basis_unit_id": {
      "description": "基準単位",
      "format": "uuid",
      "title": "Basis Unit Id",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "form_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "汎用形態",
      "title": "Form Id"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "nutrient_id": {
      "description": "栄養成分",
      "format": "uuid",
      "title": "Nutrient Id",
      "type": "string"
    },
    "product_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "商品仕様",
      "title": "Product Version Id"
    },
    "source_id": {
      "description": "出典",
      "format": "uuid",
      "title": "Source Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "form_id",
    "product_version_id",
    "nutrient_id",
    "amount",
    "basis_amount",
    "basis_unit_id",
    "source_id",
    "etag"
  ],
  "title": "NutritionFactRow",
  "type": "object"
}
```

## NutritionFactWrite

形態・商品別栄養値の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(number, string) | 必須 | anyOfの制約=number: minimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 基準量あたり成分量 |
| basis_amount | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 基準量 |
| basis_unit_id | string (uuid) | 必須 | 追加制約なし | 基準単位 |
| form_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 汎用形態 |
| nutrient_id | string (uuid) | 必須 | 追加制約なし | 栄養成分 |
| product_version_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 商品仕様 |
| source_id | string (uuid) | 必須 | 追加制約なし | 出典 |

```json
{
  "additionalProperties": false,
  "description": "形態・商品別栄養値の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "minimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "基準量あたり成分量",
      "title": "Amount"
    },
    "basis_amount": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "基準量",
      "title": "Basis Amount"
    },
    "basis_unit_id": {
      "description": "基準単位",
      "format": "uuid",
      "title": "Basis Unit Id",
      "type": "string"
    },
    "form_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "汎用形態",
      "title": "Form Id"
    },
    "nutrient_id": {
      "description": "栄養成分",
      "format": "uuid",
      "title": "Nutrient Id",
      "type": "string"
    },
    "product_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "商品仕様",
      "title": "Product Version Id"
    },
    "source_id": {
      "description": "出典",
      "format": "uuid",
      "title": "Source Id",
      "type": "string"
    }
  },
  "required": [
    "nutrient_id",
    "amount",
    "basis_amount",
    "basis_unit_id",
    "source_id"
  ],
  "title": "NutritionFactWrite",
  "type": "object"
}
```

## OperationParameterRow

動作パラメータ定義のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| allowed_values | anyOf(array&lt;string&gt;, null) | 必須 | 追加制約なし | option型の具体値配列 |
| code | string | 必須 | minLength=1; maxLength=20000 | thickness_mm等 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| max_value | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 許容上限 |
| min_value | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 許容下限 |
| name | string | 必須 | minLength=1; maxLength=20000 | 厚さ等 |
| operation_id | string (uuid) | 必須 | 追加制約なし | 動作 |
| required | boolean | 必須 | 追加制約なし | 必須か |
| unit_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 単位 |
| value_type | string | 必須 | enum=["decimal", "integer", "boolean", "text", "option"] | 値型 |

```json
{
  "additionalProperties": false,
  "description": "動作パラメータ定義のDB応答。",
  "properties": {
    "allowed_values": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "description": "option型の具体値配列",
      "title": "Allowed Values"
    },
    "code": {
      "description": "thickness_mm等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "max_value": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "許容上限",
      "title": "Max Value"
    },
    "min_value": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "許容下限",
      "title": "Min Value"
    },
    "name": {
      "description": "厚さ等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "operation_id": {
      "description": "動作",
      "format": "uuid",
      "title": "Operation Id",
      "type": "string"
    },
    "required": {
      "description": "必須か",
      "title": "Required",
      "type": "boolean"
    },
    "unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "単位",
      "title": "Unit Id"
    },
    "value_type": {
      "description": "値型",
      "enum": [
        "decimal",
        "integer",
        "boolean",
        "text",
        "option"
      ],
      "title": "Value Type",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "operation_id",
    "code",
    "name",
    "value_type",
    "unit_id",
    "required",
    "min_value",
    "max_value",
    "allowed_values",
    "etag"
  ],
  "title": "OperationParameterRow",
  "type": "object"
}
```

## OperationParameterWrite

動作パラメータ定義の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| allowed_values | anyOf(array&lt;string&gt;, null) | 任意 | 追加制約なし | option型の具体値配列 |
| code | string | 必須 | minLength=1; maxLength=20000 | thickness_mm等 |
| max_value | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 許容上限 |
| min_value | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 許容下限 |
| name | string | 必須 | minLength=1; maxLength=20000 | 厚さ等 |
| operation_id | string (uuid) | 必須 | 追加制約なし | 動作 |
| required | boolean | 必須 | 追加制約なし | 必須か |
| unit_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 単位 |
| value_type | string | 必須 | enum=["decimal", "integer", "boolean", "text", "option"] | 値型 |

```json
{
  "additionalProperties": false,
  "description": "動作パラメータ定義の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "allowed_values": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "description": "option型の具体値配列",
      "title": "Allowed Values"
    },
    "code": {
      "description": "thickness_mm等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "max_value": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "許容上限",
      "title": "Max Value"
    },
    "min_value": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "許容下限",
      "title": "Min Value"
    },
    "name": {
      "description": "厚さ等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "operation_id": {
      "description": "動作",
      "format": "uuid",
      "title": "Operation Id",
      "type": "string"
    },
    "required": {
      "description": "必須か",
      "title": "Required",
      "type": "boolean"
    },
    "unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "単位",
      "title": "Unit Id"
    },
    "value_type": {
      "description": "値型",
      "enum": [
        "decimal",
        "integer",
        "boolean",
        "text",
        "option"
      ],
      "title": "Value Type",
      "type": "string"
    }
  },
  "required": [
    "operation_id",
    "code",
    "name",
    "value_type",
    "required"
  ],
  "title": "OperationParameterWrite",
  "type": "object"
}
```

## OperationRow

標準調理動作のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | cut_ginkgo等 |
| completion_cue | string | 必須 | minLength=1; maxLength=20000 | 完了確認方法 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| definition | string | 必須 | minLength=1; maxLength=20000 | 動作の意味 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| name | string | 必須 | minLength=1; maxLength=20000 | いちょう切り等 |
| precondition | string | 必須 | minLength=1; maxLength=20000 | 入力食材・必要状態 |
| status | string | 必須 | enum=["active", "retired"] | 使用状態 |

```json
{
  "additionalProperties": false,
  "description": "標準調理動作のDB応答。",
  "properties": {
    "code": {
      "description": "cut_ginkgo等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "completion_cue": {
      "description": "完了確認方法",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Completion Cue",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "definition": {
      "description": "動作の意味",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Definition",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "name": {
      "description": "いちょう切り等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "precondition": {
      "description": "入力食材・必要状態",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Precondition",
      "type": "string"
    },
    "status": {
      "description": "使用状態",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "code",
    "name",
    "definition",
    "precondition",
    "completion_cue",
    "status",
    "etag"
  ],
  "title": "OperationRow",
  "type": "object"
}
```

## OperationWrite

標準調理動作の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | cut_ginkgo等 |
| completion_cue | string | 必須 | minLength=1; maxLength=20000 | 完了確認方法 |
| definition | string | 必須 | minLength=1; maxLength=20000 | 動作の意味 |
| name | string | 必須 | minLength=1; maxLength=20000 | いちょう切り等 |
| precondition | string | 必須 | minLength=1; maxLength=20000 | 入力食材・必要状態 |
| status | string | 必須 | enum=["active", "retired"] | 使用状態 |

```json
{
  "additionalProperties": false,
  "description": "標準調理動作の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "code": {
      "description": "cut_ginkgo等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "completion_cue": {
      "description": "完了確認方法",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Completion Cue",
      "type": "string"
    },
    "definition": {
      "description": "動作の意味",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Definition",
      "type": "string"
    },
    "name": {
      "description": "いちょう切り等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "precondition": {
      "description": "入力食材・必要状態",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Precondition",
      "type": "string"
    },
    "status": {
      "description": "使用状態",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "code",
    "name",
    "definition",
    "precondition",
    "completion_cue",
    "status"
  ],
  "title": "OperationWrite",
  "type": "object"
}
```

## OutboxEventRow

検索・キャッシュ更新配信のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| aggregate_id | string (uuid) | 必須 | 追加制約なし | 対象ID(配信対象でありFKでない) |
| attempt_count | integer | 必須 | minimum=0.0 | 再試行数 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| delivered_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 配送完了 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| event_type | string | 必須 | minLength=1; maxLength=20000 | recipe_published/withdrawn/user_erased等 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| payload | OutboxPayload | 必須 | 追加制約なし | schema_version付き最小通知 |

```json
{
  "additionalProperties": false,
  "description": "検索・キャッシュ更新配信のDB応答。",
  "properties": {
    "aggregate_id": {
      "description": "対象ID(配信対象でありFKでない)",
      "format": "uuid",
      "title": "Aggregate Id",
      "type": "string"
    },
    "attempt_count": {
      "description": "再試行数",
      "minimum": 0.0,
      "title": "Attempt Count",
      "type": "integer"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "delivered_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "配送完了",
      "title": "Delivered At"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "event_type": {
      "description": "recipe_published/withdrawn/user_erased等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Event Type",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "payload": {
      "$ref": "#/components/schemas/OutboxPayload",
      "description": "schema_version付き最小通知"
    }
  },
  "required": [
    "id",
    "created_at",
    "event_type",
    "aggregate_id",
    "payload",
    "delivered_at",
    "attempt_count",
    "etag"
  ],
  "title": "OutboxEventRow",
  "type": "object"
}
```

## OutboxPayload



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| aggregate_id | string (uuid) | 必須 | 追加制約なし | Aggregate Id |
| event_id | string (uuid) | 必須 | 追加制約なし | Event Id |
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |
| version | integer | 必須 | minimum=1.0 | Version |

```json
{
  "additionalProperties": false,
  "properties": {
    "aggregate_id": {
      "format": "uuid",
      "title": "Aggregate Id",
      "type": "string"
    },
    "event_id": {
      "format": "uuid",
      "title": "Event Id",
      "type": "string"
    },
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    },
    "version": {
      "minimum": 1.0,
      "title": "Version",
      "type": "integer"
    }
  },
  "required": [
    "event_id",
    "aggregate_id",
    "version"
  ],
  "title": "OutboxPayload",
  "type": "object"
}
```

## PantryConsumptionRow

調理による在庫消費の冪等台帳のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 消費数量 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| lot_id | string (uuid) | 必須 | 追加制約なし | 消費元ロット |
| session_id | string (uuid) | 必須 | 追加制約なし | 消費した調理セッション |
| unit_id | string (uuid) | 必須 | 追加制約なし | 消費数量の単位 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "調理による在庫消費の冪等台帳のDB応答。",
  "properties": {
    "amount": {
      "description": "消費数量",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Amount",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "lot_id": {
      "description": "消費元ロット",
      "format": "uuid",
      "title": "Lot Id",
      "type": "string"
    },
    "session_id": {
      "description": "消費した調理セッション",
      "format": "uuid",
      "title": "Session Id",
      "type": "string"
    },
    "unit_id": {
      "description": "消費数量の単位",
      "format": "uuid",
      "title": "Unit Id",
      "type": "string"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "user_id",
    "session_id",
    "lot_id",
    "amount",
    "unit_id",
    "etag"
  ],
  "title": "PantryConsumptionRow",
  "type": "object"
}
```

## PantryLotRow

手持ち食材ロットのDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 残量 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| edited | boolean | 必須 | 追加制約なし | 登録後の編集有無 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| expires_on | anyOf(string (date), null) | 必須 | 追加制約なし | 表示期限 |
| form_id | string (uuid) | 必須 | 追加制約なし | 食材形態 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| location | string | 必須 | minLength=1; maxLength=20000 | 冷蔵・冷凍・常温の保管場所 |
| opened_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 開封時点 |
| original_amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 登録時数量。不明はNULL |
| original_form_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 登録時の食材形態 |
| original_unit_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 登録時単位 |
| priority | string | 必須 | minLength=1; maxLength=20000 | 先に使う優先指定 |
| product_version_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 商品版 |
| quantity_quality | string | 必須 | minLength=1; maxLength=20000 | 数量の確定・不明 |
| source_import_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 登録元レシート |
| status | string | 必須 | minLength=1; maxLength=20000 | 在庫の有効・削除・レシート取消状態 |
| unit_id | string (uuid) | 必須 | 追加制約なし | 単位 |
| updated_at | string (date-time) | 必須 | 追加制約なし | 最終編集日時 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "手持ち食材ロットのDB応答。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "残量",
      "title": "Amount"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "edited": {
      "description": "登録後の編集有無",
      "title": "Edited",
      "type": "boolean"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "expires_on": {
      "anyOf": [
        {
          "format": "date",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "表示期限",
      "title": "Expires On"
    },
    "form_id": {
      "description": "食材形態",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "location": {
      "description": "冷蔵・冷凍・常温の保管場所",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Location",
      "type": "string"
    },
    "opened_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "開封時点",
      "title": "Opened At"
    },
    "original_amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録時数量。不明はNULL",
      "title": "Original Amount"
    },
    "original_form_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録時の食材形態",
      "title": "Original Form Id"
    },
    "original_unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録時単位",
      "title": "Original Unit Id"
    },
    "priority": {
      "description": "先に使う優先指定",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Priority",
      "type": "string"
    },
    "product_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "商品版",
      "title": "Product Version Id"
    },
    "quantity_quality": {
      "description": "数量の確定・不明",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Quantity Quality",
      "type": "string"
    },
    "source_import_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録元レシート",
      "title": "Source Import Id"
    },
    "status": {
      "description": "在庫の有効・削除・レシート取消状態",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Status",
      "type": "string"
    },
    "unit_id": {
      "description": "単位",
      "format": "uuid",
      "title": "Unit Id",
      "type": "string"
    },
    "updated_at": {
      "description": "最終編集日時",
      "format": "date-time",
      "title": "Updated At",
      "type": "string"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "user_id",
    "form_id",
    "product_version_id",
    "amount",
    "unit_id",
    "expires_on",
    "opened_at",
    "location",
    "priority",
    "status",
    "source_import_id",
    "quantity_quality",
    "original_form_id",
    "original_amount",
    "original_unit_id",
    "updated_at",
    "edited",
    "etag"
  ],
  "title": "PantryLotRow",
  "type": "object"
}
```

## PantryLotWrite

手持ち食材ロットの編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(number, string, null) | 任意 | anyOfの制約=number: minimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 残量 |
| edited | boolean | 必須 | 追加制約なし | 登録後の編集有無 |
| expires_on | anyOf(string (date), null) | 任意 | 追加制約なし | 表示期限 |
| form_id | string (uuid) | 必須 | 追加制約なし | 食材形態 |
| location | string | 必須 | minLength=1; maxLength=20000 | 冷蔵・冷凍・常温の保管場所 |
| opened_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 開封時点 |
| original_amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 登録時数量。不明はNULL |
| original_form_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 登録時の食材形態 |
| original_unit_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 登録時単位 |
| priority | string | 必須 | minLength=1; maxLength=20000 | 先に使う優先指定 |
| product_version_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 商品版 |
| quantity_quality | string | 必須 | minLength=1; maxLength=20000 | 数量の確定・不明 |
| source_import_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 登録元レシート |
| status | string | 必須 | minLength=1; maxLength=20000 | 在庫の有効・削除・レシート取消状態 |
| unit_id | string (uuid) | 必須 | 追加制約なし | 単位 |
| updated_at | string (date-time) | 必須 | 追加制約なし | 最終編集日時 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "手持ち食材ロットの編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "minimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "残量",
      "title": "Amount"
    },
    "edited": {
      "description": "登録後の編集有無",
      "title": "Edited",
      "type": "boolean"
    },
    "expires_on": {
      "anyOf": [
        {
          "format": "date",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "表示期限",
      "title": "Expires On"
    },
    "form_id": {
      "description": "食材形態",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "location": {
      "description": "冷蔵・冷凍・常温の保管場所",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Location",
      "type": "string"
    },
    "opened_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "開封時点",
      "title": "Opened At"
    },
    "original_amount": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録時数量。不明はNULL",
      "title": "Original Amount"
    },
    "original_form_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録時の食材形態",
      "title": "Original Form Id"
    },
    "original_unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録時単位",
      "title": "Original Unit Id"
    },
    "priority": {
      "description": "先に使う優先指定",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Priority",
      "type": "string"
    },
    "product_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "商品版",
      "title": "Product Version Id"
    },
    "quantity_quality": {
      "description": "数量の確定・不明",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Quantity Quality",
      "type": "string"
    },
    "source_import_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録元レシート",
      "title": "Source Import Id"
    },
    "status": {
      "description": "在庫の有効・削除・レシート取消状態",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Status",
      "type": "string"
    },
    "unit_id": {
      "description": "単位",
      "format": "uuid",
      "title": "Unit Id",
      "type": "string"
    },
    "updated_at": {
      "description": "最終編集日時",
      "format": "date-time",
      "title": "Updated At",
      "type": "string"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "user_id",
    "form_id",
    "unit_id",
    "location",
    "priority",
    "status",
    "quantity_quality",
    "updated_at",
    "edited"
  ],
  "title": "PantryLotWrite",
  "type": "object"
}
```

## PlanRequest

未保存の分量調整も、明示した料理版の材料行だけへ適用する。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| items | array&lt;MealItem&gt; | 必須 | minItems=1; maxItems=50 | Items |

```json
{
  "additionalProperties": false,
  "description": "未保存の分量調整も、明示した料理版の材料行だけへ適用する。",
  "properties": {
    "items": {
      "items": {
        "$ref": "#/components/schemas/MealItem"
      },
      "maxItems": 50,
      "minItems": 1,
      "title": "Items",
      "type": "array"
    }
  },
  "required": [
    "items"
  ],
  "title": "PlanRequest",
  "type": "object"
}
```

## PlanResponse

保存済みの調理タスクと共通の表示形式。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| plan | array&lt;PlannedStep&gt; | 必須 | 追加制約なし | Plan |

```json
{
  "additionalProperties": false,
  "description": "保存済みの調理タスクと共通の表示形式。",
  "properties": {
    "plan": {
      "items": {
        "$ref": "#/components/schemas/PlannedStep"
      },
      "title": "Plan",
      "type": "array"
    }
  },
  "required": [
    "plan"
  ],
  "title": "PlanResponse",
  "type": "object"
}
```

## PlannedStep



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| endMinute | number | 必須 | minimum=0.0; maximum=1000000.0 | Endminute |
| equipment | array&lt;string&gt; | 必須 | maxItems=50; 要素の制約=maxLength=500 | Equipment |
| guide | anyOf(string, null) | 必須 | anyOfの制約=string: maxLength=500 | Guide |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| instruction | string | 必須 | maxLength=5000 | Instruction |
| key | string | 必須 | maxLength=500 | Key |
| mealItemId | string | 必須 | minLength=1; maxLength=128 | Mealitemid |
| minutes | number | 必須 | minimum=0.0; maximum=1000000.0 | Minutes |
| mode | string | 必須 | enum=["active", "passive", "monitored"] | Mode |
| recipeId | string | 必須 | minLength=1; maxLength=128 | Recipeid |
| recipeName | string | 必須 | maxLength=500 | Recipename |
| startMinute | number | 必須 | minimum=0.0; maximum=1000000.0 | Startminute |
| title | string | 必須 | maxLength=500 | Title |

```json
{
  "additionalProperties": false,
  "properties": {
    "endMinute": {
      "maximum": 1000000.0,
      "minimum": 0.0,
      "title": "Endminute",
      "type": "number"
    },
    "equipment": {
      "items": {
        "maxLength": 500,
        "type": "string"
      },
      "maxItems": 50,
      "title": "Equipment",
      "type": "array"
    },
    "guide": {
      "anyOf": [
        {
          "maxLength": 500,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Guide"
    },
    "id": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Id",
      "type": "string"
    },
    "instruction": {
      "maxLength": 5000,
      "title": "Instruction",
      "type": "string"
    },
    "key": {
      "maxLength": 500,
      "title": "Key",
      "type": "string"
    },
    "mealItemId": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Mealitemid",
      "type": "string"
    },
    "minutes": {
      "maximum": 1000000.0,
      "minimum": 0.0,
      "title": "Minutes",
      "type": "number"
    },
    "mode": {
      "enum": [
        "active",
        "passive",
        "monitored"
      ],
      "title": "Mode",
      "type": "string"
    },
    "recipeId": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Recipeid",
      "type": "string"
    },
    "recipeName": {
      "maxLength": 500,
      "title": "Recipename",
      "type": "string"
    },
    "startMinute": {
      "maximum": 1000000.0,
      "minimum": 0.0,
      "title": "Startminute",
      "type": "number"
    },
    "title": {
      "maxLength": 500,
      "title": "Title",
      "type": "string"
    }
  },
  "required": [
    "id",
    "title",
    "instruction",
    "minutes",
    "mode",
    "equipment",
    "guide",
    "key",
    "mealItemId",
    "recipeId",
    "recipeName",
    "startMinute",
    "endMinute"
  ],
  "title": "PlannedStep",
  "type": "object"
}
```

## PlannerConfig



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| concurrent_active_tasks | integer | 必須 | minimum=1.0; maximum=10.0 | Concurrent Active Tasks |
| planner_version | string | 必須 | minLength=1; maxLength=200 | Planner Version |

```json
{
  "additionalProperties": false,
  "properties": {
    "concurrent_active_tasks": {
      "maximum": 10.0,
      "minimum": 1.0,
      "title": "Concurrent Active Tasks",
      "type": "integer"
    },
    "planner_version": {
      "maxLength": 200,
      "minLength": 1,
      "title": "Planner Version",
      "type": "string"
    }
  },
  "required": [
    "planner_version",
    "concurrent_active_tasks"
  ],
  "title": "PlannerConfig",
  "type": "object"
}
```

## Predicate-Input



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| all | anyOf(array&lt;Predicate-Input&gt;, null) | 任意 | anyOfの制約=array&lt;Predicate-Input&gt;: maxItems=100 | All |
| any | anyOf(array&lt;Predicate-Input&gt;, null) | 任意 | anyOfの制約=array&lt;Predicate-Input&gt;: maxItems=100 | Any |
| field | anyOf(string, null) | 任意 | anyOfの制約=string: enum=["product.microwave_allowed", "step.operation_code", "recipe.validation", "allergen.presence", "resource.capacity", "ingredient.amount_mode"] | Field |
| not | anyOf(Predicate-Input, null) | 任意 | 追加制約なし |  |
| op | anyOf(string, null) | 任意 | anyOfの制約=string: enum=["eq", "in", "gt", "exists"] | Op |
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |
| value | anyOf(string, boolean, number, array&lt;string&gt;, null) | 任意 | 追加制約なし | Value |

```json
{
  "additionalProperties": false,
  "properties": {
    "all": {
      "anyOf": [
        {
          "items": {
            "$ref": "#/components/schemas/Predicate-Input"
          },
          "maxItems": 100,
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "title": "All"
    },
    "any": {
      "anyOf": [
        {
          "items": {
            "$ref": "#/components/schemas/Predicate-Input"
          },
          "maxItems": 100,
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "title": "Any"
    },
    "field": {
      "anyOf": [
        {
          "enum": [
            "product.microwave_allowed",
            "step.operation_code",
            "recipe.validation",
            "allergen.presence",
            "resource.capacity",
            "ingredient.amount_mode"
          ],
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Field"
    },
    "not": {
      "anyOf": [
        {
          "$ref": "#/components/schemas/Predicate-Input"
        },
        {
          "type": "null"
        }
      ]
    },
    "op": {
      "anyOf": [
        {
          "enum": [
            "eq",
            "in",
            "gt",
            "exists"
          ],
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Op"
    },
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    },
    "value": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "boolean"
        },
        {
          "type": "number"
        },
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "title": "Value"
    }
  },
  "title": "Predicate",
  "type": "object"
}
```

## Predicate-Output



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| all | anyOf(array&lt;Predicate-Output&gt;, null) | 任意 | anyOfの制約=array&lt;Predicate-Output&gt;: maxItems=100 | All |
| any | anyOf(array&lt;Predicate-Output&gt;, null) | 任意 | anyOfの制約=array&lt;Predicate-Output&gt;: maxItems=100 | Any |
| field | anyOf(string, null) | 任意 | anyOfの制約=string: enum=["product.microwave_allowed", "step.operation_code", "recipe.validation", "allergen.presence", "resource.capacity", "ingredient.amount_mode"] | Field |
| not | anyOf(Predicate-Output, null) | 任意 | 追加制約なし |  |
| op | anyOf(string, null) | 任意 | anyOfの制約=string: enum=["eq", "in", "gt", "exists"] | Op |
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |
| value | anyOf(string, boolean, number, array&lt;string&gt;, null) | 任意 | 追加制約なし | Value |

```json
{
  "additionalProperties": false,
  "properties": {
    "all": {
      "anyOf": [
        {
          "items": {
            "$ref": "#/components/schemas/Predicate-Output"
          },
          "maxItems": 100,
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "title": "All"
    },
    "any": {
      "anyOf": [
        {
          "items": {
            "$ref": "#/components/schemas/Predicate-Output"
          },
          "maxItems": 100,
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "title": "Any"
    },
    "field": {
      "anyOf": [
        {
          "enum": [
            "product.microwave_allowed",
            "step.operation_code",
            "recipe.validation",
            "allergen.presence",
            "resource.capacity",
            "ingredient.amount_mode"
          ],
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Field"
    },
    "not": {
      "anyOf": [
        {
          "$ref": "#/components/schemas/Predicate-Output"
        },
        {
          "type": "null"
        }
      ]
    },
    "op": {
      "anyOf": [
        {
          "enum": [
            "eq",
            "in",
            "gt",
            "exists"
          ],
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Op"
    },
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    },
    "value": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "boolean"
        },
        {
          "type": "number"
        },
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "title": "Value"
    }
  },
  "title": "Predicate",
  "type": "object"
}
```

## ProductAllergenRow

商品表示アレルゲンのDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| allergen_id | string (uuid) | 必須 | 追加制約なし | 物質 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| presence | string | 必須 | enum=["contains", "may_contain", "absent_verified", "unknown"] | 表示状態 |
| product_version_id | string (uuid) | 必須 | 追加制約なし | 商品仕様版 |
| source_id | string (uuid) | 必須 | 追加制約なし | ラベル等 |

```json
{
  "additionalProperties": false,
  "description": "商品表示アレルゲンのDB応答。",
  "properties": {
    "allergen_id": {
      "description": "物質",
      "format": "uuid",
      "title": "Allergen Id",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "presence": {
      "description": "表示状態",
      "enum": [
        "contains",
        "may_contain",
        "absent_verified",
        "unknown"
      ],
      "title": "Presence",
      "type": "string"
    },
    "product_version_id": {
      "description": "商品仕様版",
      "format": "uuid",
      "title": "Product Version Id",
      "type": "string"
    },
    "source_id": {
      "description": "ラベル等",
      "format": "uuid",
      "title": "Source Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "product_version_id",
    "allergen_id",
    "presence",
    "source_id",
    "etag"
  ],
  "title": "ProductAllergenRow",
  "type": "object"
}
```

## ProductAllergenWrite

商品表示アレルゲンの編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| allergen_id | string (uuid) | 必須 | 追加制約なし | 物質 |
| presence | string | 必須 | enum=["contains", "may_contain", "absent_verified", "unknown"] | 表示状態 |
| product_version_id | string (uuid) | 必須 | 追加制約なし | 商品仕様版 |
| source_id | string (uuid) | 必須 | 追加制約なし | ラベル等 |

```json
{
  "additionalProperties": false,
  "description": "商品表示アレルゲンの編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "allergen_id": {
      "description": "物質",
      "format": "uuid",
      "title": "Allergen Id",
      "type": "string"
    },
    "presence": {
      "description": "表示状態",
      "enum": [
        "contains",
        "may_contain",
        "absent_verified",
        "unknown"
      ],
      "title": "Presence",
      "type": "string"
    },
    "product_version_id": {
      "description": "商品仕様版",
      "format": "uuid",
      "title": "Product Version Id",
      "type": "string"
    },
    "source_id": {
      "description": "ラベル等",
      "format": "uuid",
      "title": "Source Id",
      "type": "string"
    }
  },
  "required": [
    "product_version_id",
    "allergen_id",
    "presence",
    "source_id"
  ],
  "title": "ProductAllergenWrite",
  "type": "object"
}
```

## ProductComponentRow

セット内構成品のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 量(不明はNULL) |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| form_id | string (uuid) | 必須 | 追加制約なし | 麺・ソース・かやく等 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| name | string | 必須 | minLength=1; maxLength=20000 | 構成品名 |
| product_version_id | string (uuid) | 必須 | 追加制約なし | 親商品版 |
| quality | string | 必須 | enum=["measured", "manufacturer", "reference", "estimated", "unknown"] | 数量の根拠 |
| unit_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 構成品量単位 |

```json
{
  "additionalProperties": false,
  "description": "セット内構成品のDB応答。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "量(不明はNULL)",
      "title": "Amount"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "form_id": {
      "description": "麺・ソース・かやく等",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "name": {
      "description": "構成品名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "product_version_id": {
      "description": "親商品版",
      "format": "uuid",
      "title": "Product Version Id",
      "type": "string"
    },
    "quality": {
      "description": "数量の根拠",
      "enum": [
        "measured",
        "manufacturer",
        "reference",
        "estimated",
        "unknown"
      ],
      "title": "Quality",
      "type": "string"
    },
    "unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "構成品量単位",
      "title": "Unit Id"
    }
  },
  "required": [
    "id",
    "created_at",
    "product_version_id",
    "form_id",
    "name",
    "amount",
    "unit_id",
    "quality",
    "etag"
  ],
  "title": "ProductComponentRow",
  "type": "object"
}
```

## ProductComponentWrite

セット内構成品の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 量(不明はNULL) |
| form_id | string (uuid) | 必須 | 追加制約なし | 麺・ソース・かやく等 |
| name | string | 必須 | minLength=1; maxLength=20000 | 構成品名 |
| product_version_id | string (uuid) | 必須 | 追加制約なし | 親商品版 |
| quality | string | 必須 | enum=["measured", "manufacturer", "reference", "estimated", "unknown"] | 数量の根拠 |
| unit_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 構成品量単位 |

```json
{
  "additionalProperties": false,
  "description": "セット内構成品の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "量(不明はNULL)",
      "title": "Amount"
    },
    "form_id": {
      "description": "麺・ソース・かやく等",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "name": {
      "description": "構成品名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "product_version_id": {
      "description": "親商品版",
      "format": "uuid",
      "title": "Product Version Id",
      "type": "string"
    },
    "quality": {
      "description": "数量の根拠",
      "enum": [
        "measured",
        "manufacturer",
        "reference",
        "estimated",
        "unknown"
      ],
      "title": "Quality",
      "type": "string"
    },
    "unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "構成品量単位",
      "title": "Unit Id"
    }
  },
  "required": [
    "product_version_id",
    "form_id",
    "name",
    "quality"
  ],
  "title": "ProductComponentWrite",
  "type": "object"
}
```

## ProductPreparation-Input



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| duration_s | anyOf(integer, null) | 任意 | anyOfの制約=integer: exclusiveMinimum=0.0 | Duration S |
| lid | string | 必須 | enum=["open", "closed", "vented", "per_label"] | Lid |
| power_w | anyOf(number, string, null) | 任意 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Power W |
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |
| water_ml | anyOf(number, string, null) | 任意 | anyOfの制約=number: minimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Water Ml |

```json
{
  "additionalProperties": false,
  "properties": {
    "duration_s": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "title": "Duration S"
    },
    "lid": {
      "enum": [
        "open",
        "closed",
        "vented",
        "per_label"
      ],
      "title": "Lid",
      "type": "string"
    },
    "power_w": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Power W"
    },
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    },
    "water_ml": {
      "anyOf": [
        {
          "minimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Water Ml"
    }
  },
  "required": [
    "lid"
  ],
  "title": "ProductPreparation",
  "type": "object"
}
```

## ProductPreparation-Output



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| duration_s | anyOf(integer, null) | 任意 | anyOfの制約=integer: exclusiveMinimum=0.0 | Duration S |
| lid | string | 必須 | enum=["open", "closed", "vented", "per_label"] | Lid |
| power_w | anyOf(string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Power W |
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |
| water_ml | anyOf(string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Water Ml |

```json
{
  "additionalProperties": false,
  "properties": {
    "duration_s": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "title": "Duration S"
    },
    "lid": {
      "enum": [
        "open",
        "closed",
        "vented",
        "per_label"
      ],
      "title": "Lid",
      "type": "string"
    },
    "power_w": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Power W"
    },
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    },
    "water_ml": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Water Ml"
    }
  },
  "required": [
    "lid"
  ],
  "title": "ProductPreparation",
  "type": "object"
}
```

## ProductPreparationRuleRow

商品固有の調理条件のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| allowed | boolean | 必須 | 追加制約なし | 表示で許可される方法か |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| operation_id | string (uuid) | 必須 | 追加制約なし | 対象標準動作 |
| parameter_contract | ProductPreparation-Output | 必須 | 追加制約なし | 電力・注湯量・時間・蓋などの確定条件 |
| product_version_id | string (uuid) | 必須 | 追加制約なし | 対象商品仕様 |
| source_id | string (uuid) | 必須 | 追加制約なし | 商品表示根拠 |
| use_original_container | boolean | 必須 | 追加制約なし | 付属容器で調理するか |

```json
{
  "additionalProperties": false,
  "description": "商品固有の調理条件のDB応答。",
  "properties": {
    "allowed": {
      "description": "表示で許可される方法か",
      "title": "Allowed",
      "type": "boolean"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "operation_id": {
      "description": "対象標準動作",
      "format": "uuid",
      "title": "Operation Id",
      "type": "string"
    },
    "parameter_contract": {
      "$ref": "#/components/schemas/ProductPreparation-Output",
      "description": "電力・注湯量・時間・蓋などの確定条件"
    },
    "product_version_id": {
      "description": "対象商品仕様",
      "format": "uuid",
      "title": "Product Version Id",
      "type": "string"
    },
    "source_id": {
      "description": "商品表示根拠",
      "format": "uuid",
      "title": "Source Id",
      "type": "string"
    },
    "use_original_container": {
      "description": "付属容器で調理するか",
      "title": "Use Original Container",
      "type": "boolean"
    }
  },
  "required": [
    "id",
    "created_at",
    "product_version_id",
    "operation_id",
    "allowed",
    "use_original_container",
    "parameter_contract",
    "source_id",
    "etag"
  ],
  "title": "ProductPreparationRuleRow",
  "type": "object"
}
```

## ProductPreparationRuleWrite

商品固有の調理条件の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| allowed | boolean | 必須 | 追加制約なし | 表示で許可される方法か |
| operation_id | string (uuid) | 必須 | 追加制約なし | 対象標準動作 |
| parameter_contract | ProductPreparation-Input | 必須 | 追加制約なし | 電力・注湯量・時間・蓋などの確定条件 |
| product_version_id | string (uuid) | 必須 | 追加制約なし | 対象商品仕様 |
| source_id | string (uuid) | 必須 | 追加制約なし | 商品表示根拠 |
| use_original_container | boolean | 必須 | 追加制約なし | 付属容器で調理するか |

```json
{
  "additionalProperties": false,
  "description": "商品固有の調理条件の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "allowed": {
      "description": "表示で許可される方法か",
      "title": "Allowed",
      "type": "boolean"
    },
    "operation_id": {
      "description": "対象標準動作",
      "format": "uuid",
      "title": "Operation Id",
      "type": "string"
    },
    "parameter_contract": {
      "$ref": "#/components/schemas/ProductPreparation-Input",
      "description": "電力・注湯量・時間・蓋などの確定条件"
    },
    "product_version_id": {
      "description": "対象商品仕様",
      "format": "uuid",
      "title": "Product Version Id",
      "type": "string"
    },
    "source_id": {
      "description": "商品表示根拠",
      "format": "uuid",
      "title": "Source Id",
      "type": "string"
    },
    "use_original_container": {
      "description": "付属容器で調理するか",
      "title": "Use Original Container",
      "type": "boolean"
    }
  },
  "required": [
    "product_version_id",
    "operation_id",
    "allowed",
    "use_original_container",
    "parameter_contract",
    "source_id"
  ],
  "title": "ProductPreparationRuleWrite",
  "type": "object"
}
```

## ProductRow

市販商品識別のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| brand | string | 必須 | minLength=1; maxLength=20000 | ブランド |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| food_id | string (uuid) | 必須 | 追加制約なし | 汎用食材との対応 |
| gtin | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | JAN等(先頭0保持) |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| name | string | 必須 | minLength=1; maxLength=20000 | 商品名 |
| status | string | 必須 | enum=["active", "retired"] | 終売はretired |

```json
{
  "additionalProperties": false,
  "description": "市販商品識別のDB応答。",
  "properties": {
    "brand": {
      "description": "ブランド",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Brand",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "food_id": {
      "description": "汎用食材との対応",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "gtin": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "JAN等(先頭0保持)",
      "title": "Gtin"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "name": {
      "description": "商品名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "status": {
      "description": "終売はretired",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "food_id",
    "brand",
    "name",
    "gtin",
    "status",
    "etag"
  ],
  "title": "ProductRow",
  "type": "object"
}
```

## ProductVersionRow

商品仕様版のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| drain_amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 固形量 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| form_id | string (uuid) | 必須 | 追加制約なし | 販売形態 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| net_amount | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 1包装の内容量 |
| preparation_note | string | 必須 | minLength=1; maxLength=20000 | 容器・加熱方式・表示手順 |
| product_id | string (uuid) | 必須 | 追加制約なし | 商品 |
| source_id | string (uuid) | 必須 | 追加制約なし | メーカー表示根拠 |
| unit_id | string (uuid) | 必須 | 追加制約なし | 内容量単位 |
| valid_from | string (date) | 必須 | 追加制約なし | 適用開始日 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 仕様版 |

```json
{
  "additionalProperties": false,
  "description": "商品仕様版のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "drain_amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "固形量",
      "title": "Drain Amount"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "form_id": {
      "description": "販売形態",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "net_amount": {
      "description": "1包装の内容量",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Net Amount",
      "type": "string"
    },
    "preparation_note": {
      "description": "容器・加熱方式・表示手順",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Preparation Note",
      "type": "string"
    },
    "product_id": {
      "description": "商品",
      "format": "uuid",
      "title": "Product Id",
      "type": "string"
    },
    "source_id": {
      "description": "メーカー表示根拠",
      "format": "uuid",
      "title": "Source Id",
      "type": "string"
    },
    "unit_id": {
      "description": "内容量単位",
      "format": "uuid",
      "title": "Unit Id",
      "type": "string"
    },
    "valid_from": {
      "description": "適用開始日",
      "format": "date",
      "title": "Valid From",
      "type": "string"
    },
    "version": {
      "description": "仕様版",
      "exclusiveMinimum": 0.0,
      "title": "Version",
      "type": "integer"
    }
  },
  "required": [
    "id",
    "created_at",
    "product_id",
    "version",
    "form_id",
    "net_amount",
    "unit_id",
    "drain_amount",
    "source_id",
    "preparation_note",
    "valid_from",
    "etag"
  ],
  "title": "ProductVersionRow",
  "type": "object"
}
```

## ProductVersionWrite

商品仕様版の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| drain_amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 固形量 |
| form_id | string (uuid) | 必須 | 追加制約なし | 販売形態 |
| net_amount | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 1包装の内容量 |
| preparation_note | string | 必須 | minLength=1; maxLength=20000 | 容器・加熱方式・表示手順 |
| product_id | string (uuid) | 必須 | 追加制約なし | 商品 |
| source_id | string (uuid) | 必須 | 追加制約なし | メーカー表示根拠 |
| unit_id | string (uuid) | 必須 | 追加制約なし | 内容量単位 |
| valid_from | string (date) | 必須 | 追加制約なし | 適用開始日 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 仕様版 |

```json
{
  "additionalProperties": false,
  "description": "商品仕様版の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "drain_amount": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "固形量",
      "title": "Drain Amount"
    },
    "form_id": {
      "description": "販売形態",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "net_amount": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "1包装の内容量",
      "title": "Net Amount"
    },
    "preparation_note": {
      "description": "容器・加熱方式・表示手順",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Preparation Note",
      "type": "string"
    },
    "product_id": {
      "description": "商品",
      "format": "uuid",
      "title": "Product Id",
      "type": "string"
    },
    "source_id": {
      "description": "メーカー表示根拠",
      "format": "uuid",
      "title": "Source Id",
      "type": "string"
    },
    "unit_id": {
      "description": "内容量単位",
      "format": "uuid",
      "title": "Unit Id",
      "type": "string"
    },
    "valid_from": {
      "description": "適用開始日",
      "format": "date",
      "title": "Valid From",
      "type": "string"
    },
    "version": {
      "description": "仕様版",
      "exclusiveMinimum": 0.0,
      "title": "Version",
      "type": "integer"
    }
  },
  "required": [
    "product_id",
    "version",
    "form_id",
    "net_amount",
    "unit_id",
    "source_id",
    "preparation_note",
    "valid_from"
  ],
  "title": "ProductVersionWrite",
  "type": "object"
}
```

## ProductWrite

市販商品識別の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| brand | string | 必須 | minLength=1; maxLength=20000 | ブランド |
| food_id | string (uuid) | 必須 | 追加制約なし | 汎用食材との対応 |
| gtin | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | JAN等(先頭0保持) |
| name | string | 必須 | minLength=1; maxLength=20000 | 商品名 |
| status | string | 必須 | enum=["active", "retired"] | 終売はretired |

```json
{
  "additionalProperties": false,
  "description": "市販商品識別の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "brand": {
      "description": "ブランド",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Brand",
      "type": "string"
    },
    "food_id": {
      "description": "汎用食材との対応",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "gtin": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "JAN等(先頭0保持)",
      "title": "Gtin"
    },
    "name": {
      "description": "商品名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "status": {
      "description": "終売はretired",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "food_id",
    "brand",
    "name",
    "status"
  ],
  "title": "ProductWrite",
  "type": "object"
}
```

## Quantity



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| unit | string | 必須 | enum=["g", "ml", "個", "パック", "袋", "缶", "本", "枚", "点"] | Unit |
| value | anyOf(number, null) | 必須 | anyOfの制約=number: minimum=0.0; maximum=1000000.0 | Value |

```json
{
  "additionalProperties": false,
  "properties": {
    "unit": {
      "enum": [
        "g",
        "ml",
        "個",
        "パック",
        "袋",
        "缶",
        "本",
        "枚",
        "点"
      ],
      "title": "Unit",
      "type": "string"
    },
    "value": {
      "anyOf": [
        {
          "maximum": 1000000.0,
          "minimum": 0.0,
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Value"
    }
  },
  "required": [
    "value",
    "unit"
  ],
  "title": "Quantity",
  "type": "object"
}
```

## RandomRecipeResponse



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| item | anyOf(Recipe, null) | 必須 | 追加制約なし |  |
| total | integer | 必須 | 追加制約なし | Total |

```json
{
  "additionalProperties": false,
  "properties": {
    "item": {
      "anyOf": [
        {
          "$ref": "#/components/schemas/Recipe"
        },
        {
          "type": "null"
        }
      ]
    },
    "total": {
      "title": "Total",
      "type": "integer"
    }
  },
  "required": [
    "item",
    "total"
  ],
  "title": "RandomRecipeResponse",
  "type": "object"
}
```

## RangeValue-Input



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| max | anyOf(number, string) | 必須 | anyOfの制約=number: minimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Max |
| min | anyOf(number, string) | 必須 | anyOfの制約=number: minimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Min |

```json
{
  "additionalProperties": false,
  "properties": {
    "max": {
      "anyOf": [
        {
          "minimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
          "type": "string"
        }
      ],
      "title": "Max"
    },
    "min": {
      "anyOf": [
        {
          "minimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
          "type": "string"
        }
      ],
      "title": "Min"
    }
  },
  "required": [
    "min",
    "max"
  ],
  "title": "RangeValue",
  "type": "object"
}
```

## RangeValue-Output



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| max | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Max |
| min | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$" | Min |

```json
{
  "additionalProperties": false,
  "properties": {
    "max": {
      "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
      "title": "Max",
      "type": "string"
    },
    "min": {
      "pattern": "^(?!^[-+.]*$)[+-]?0*\\d*\\.?\\d*$",
      "title": "Min",
      "type": "string"
    }
  },
  "required": [
    "min",
    "max"
  ],
  "title": "RangeValue",
  "type": "object"
}
```

## ReceiptCandidate



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| foodId | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=128 | Foodid |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| quantity | Quantity | 必須 | 追加制約なし |  |
| rawText | string | 必須 | maxLength=500 | Rawtext |
| reason | string | 必須 | maxLength=500 | Reason |
| selected | boolean | 必須 | 追加制約なし | Selected |
| status | string | 必須 | enum=["matched", "review", "excluded"] | Status |

```json
{
  "additionalProperties": false,
  "properties": {
    "foodId": {
      "anyOf": [
        {
          "maxLength": 128,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Foodid"
    },
    "id": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Id",
      "type": "string"
    },
    "quantity": {
      "$ref": "#/components/schemas/Quantity"
    },
    "rawText": {
      "maxLength": 500,
      "title": "Rawtext",
      "type": "string"
    },
    "reason": {
      "maxLength": 500,
      "title": "Reason",
      "type": "string"
    },
    "selected": {
      "title": "Selected",
      "type": "boolean"
    },
    "status": {
      "enum": [
        "matched",
        "review",
        "excluded"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "id",
    "rawText",
    "foodId",
    "quantity",
    "selected",
    "status",
    "reason"
  ],
  "title": "ReceiptCandidate",
  "type": "object"
}
```

## ReceiptImport



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| createdAt | string | 必須 | maxLength=500 | Createdat |
| createdLotIds | array&lt;string&gt; | 必須 | maxItems=200; 要素の制約=minLength=1; maxLength=128 | Createdlotids |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| imageHash | string | 必須 | pattern="^[a-f0-9]{64}$" | Imagehash |
| purchaseSignature | string | 必須 | pattern="^[a-f0-9]{64}$" | Purchasesignature |
| state | string | 必須 | enum=["registered", "undone"] | State |
| undoneAt | anyOf(string, null) | 必須 | anyOfの制約=string: maxLength=500 | Undoneat |

```json
{
  "additionalProperties": false,
  "properties": {
    "createdAt": {
      "maxLength": 500,
      "title": "Createdat",
      "type": "string"
    },
    "createdLotIds": {
      "items": {
        "maxLength": 128,
        "minLength": 1,
        "type": "string"
      },
      "maxItems": 200,
      "title": "Createdlotids",
      "type": "array"
    },
    "id": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Id",
      "type": "string"
    },
    "imageHash": {
      "pattern": "^[a-f0-9]{64}$",
      "title": "Imagehash",
      "type": "string"
    },
    "purchaseSignature": {
      "pattern": "^[a-f0-9]{64}$",
      "title": "Purchasesignature",
      "type": "string"
    },
    "state": {
      "enum": [
        "registered",
        "undone"
      ],
      "title": "State",
      "type": "string"
    },
    "undoneAt": {
      "anyOf": [
        {
          "maxLength": 500,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Undoneat"
    }
  },
  "required": [
    "id",
    "imageHash",
    "purchaseSignature",
    "createdAt",
    "state",
    "createdLotIds",
    "undoneAt"
  ],
  "title": "ReceiptImport",
  "type": "object"
}
```

## ReceiptImportRow

レシート読取・在庫登録の処理単位のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| committed_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 在庫へ登録した日時 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| file_sha256 | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=64; maxLength=64 | 画像本文のSHA256。本文はDBに保存しない |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| idempotency_key | string | 必須 | minLength=1; maxLength=20000 | 本人内で一意の再送防止キー |
| reverted_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 登録取消日時 |
| revision | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 楽観ロック版 |
| status | string | 必須 | enum=["draft", "committed", "reverted"] | draft/committed/revertedの状態 |
| undo_preserved_count | integer | 必須 | 追加制約なし | レシート取消時に編集・消費済みとして残した在庫件数 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "レシート読取・在庫登録の処理単位のDB応答。",
  "properties": {
    "committed_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "在庫へ登録した日時",
      "title": "Committed At"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "file_sha256": {
      "anyOf": [
        {
          "maxLength": 64,
          "minLength": 64,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "画像本文のSHA256。本文はDBに保存しない",
      "title": "File Sha256"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "idempotency_key": {
      "description": "本人内で一意の再送防止キー",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Idempotency Key",
      "type": "string"
    },
    "reverted_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録取消日時",
      "title": "Reverted At"
    },
    "revision": {
      "description": "楽観ロック版",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Revision",
      "type": "string"
    },
    "status": {
      "description": "draft/committed/revertedの状態",
      "enum": [
        "draft",
        "committed",
        "reverted"
      ],
      "title": "Status",
      "type": "string"
    },
    "undo_preserved_count": {
      "description": "レシート取消時に編集・消費済みとして残した在庫件数",
      "title": "Undo Preserved Count",
      "type": "integer"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "user_id",
    "file_sha256",
    "idempotency_key",
    "status",
    "revision",
    "committed_at",
    "reverted_at",
    "undo_preserved_count",
    "etag"
  ],
  "title": "ReceiptImportRow",
  "type": "object"
}
```

## ReceiptImportWrite

レシート読取・在庫登録の処理単位の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| committed_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 在庫へ登録した日時 |
| file_sha256 | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=64; maxLength=64 | 画像本文のSHA256。本文はDBに保存しない |
| idempotency_key | string | 必須 | minLength=1; maxLength=20000 | 本人内で一意の再送防止キー |
| reverted_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 登録取消日時 |
| revision | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 楽観ロック版 |
| status | string | 必須 | enum=["draft", "committed", "reverted"] | draft/committed/revertedの状態 |
| undo_preserved_count | integer | 必須 | 追加制約なし | レシート取消時に編集・消費済みとして残した在庫件数 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "レシート読取・在庫登録の処理単位の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "committed_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "在庫へ登録した日時",
      "title": "Committed At"
    },
    "file_sha256": {
      "anyOf": [
        {
          "maxLength": 64,
          "minLength": 64,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "画像本文のSHA256。本文はDBに保存しない",
      "title": "File Sha256"
    },
    "idempotency_key": {
      "description": "本人内で一意の再送防止キー",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Idempotency Key",
      "type": "string"
    },
    "reverted_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録取消日時",
      "title": "Reverted At"
    },
    "revision": {
      "description": "楽観ロック版",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Revision",
      "type": "string"
    },
    "status": {
      "description": "draft/committed/revertedの状態",
      "enum": [
        "draft",
        "committed",
        "reverted"
      ],
      "title": "Status",
      "type": "string"
    },
    "undo_preserved_count": {
      "description": "レシート取消時に編集・消費済みとして残した在庫件数",
      "title": "Undo Preserved Count",
      "type": "integer"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "user_id",
    "idempotency_key",
    "status",
    "revision",
    "undo_preserved_count"
  ],
  "title": "ReceiptImportWrite",
  "type": "object"
}
```

## ReceiptLineRow

レシートの商品候補と確定した在庫の対応のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 数量。不明はNULL |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| decision | string | 必須 | enum=["accepted", "skipped", "unresolved"] | accepted/skipped/unresolved |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| form_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 確定した食材形態 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| import_id | string (uuid) | 必須 | 追加制約なし | レシート処理 |
| line_no | integer | 必須 | exclusiveMinimum=0.0 | レシート内の表示順 |
| pantry_lot_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 登録したロット |
| product_version_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 確定した商品版 |
| raw_name | string | 必須 | minLength=1; maxLength=20000 | 利用者が確認できる商品原表記 |
| unit_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 確定数量の単位 |

```json
{
  "additionalProperties": false,
  "description": "レシートの商品候補と確定した在庫の対応のDB応答。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "数量。不明はNULL",
      "title": "Amount"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "decision": {
      "description": "accepted/skipped/unresolved",
      "enum": [
        "accepted",
        "skipped",
        "unresolved"
      ],
      "title": "Decision",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "form_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "確定した食材形態",
      "title": "Form Id"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "import_id": {
      "description": "レシート処理",
      "format": "uuid",
      "title": "Import Id",
      "type": "string"
    },
    "line_no": {
      "description": "レシート内の表示順",
      "exclusiveMinimum": 0.0,
      "title": "Line No",
      "type": "integer"
    },
    "pantry_lot_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録したロット",
      "title": "Pantry Lot Id"
    },
    "product_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "確定した商品版",
      "title": "Product Version Id"
    },
    "raw_name": {
      "description": "利用者が確認できる商品原表記",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Raw Name",
      "type": "string"
    },
    "unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "確定数量の単位",
      "title": "Unit Id"
    }
  },
  "required": [
    "id",
    "created_at",
    "import_id",
    "line_no",
    "raw_name",
    "form_id",
    "product_version_id",
    "amount",
    "unit_id",
    "decision",
    "pantry_lot_id",
    "etag"
  ],
  "title": "ReceiptLineRow",
  "type": "object"
}
```

## ReceiptLineWrite

レシートの商品候補と確定した在庫の対応の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 数量。不明はNULL |
| decision | string | 必須 | enum=["accepted", "skipped", "unresolved"] | accepted/skipped/unresolved |
| form_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 確定した食材形態 |
| import_id | string (uuid) | 必須 | 追加制約なし | レシート処理 |
| line_no | integer | 必須 | exclusiveMinimum=0.0 | レシート内の表示順 |
| pantry_lot_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 登録したロット |
| product_version_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 確定した商品版 |
| raw_name | string | 必須 | minLength=1; maxLength=20000 | 利用者が確認できる商品原表記 |
| unit_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 確定数量の単位 |

```json
{
  "additionalProperties": false,
  "description": "レシートの商品候補と確定した在庫の対応の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "数量。不明はNULL",
      "title": "Amount"
    },
    "decision": {
      "description": "accepted/skipped/unresolved",
      "enum": [
        "accepted",
        "skipped",
        "unresolved"
      ],
      "title": "Decision",
      "type": "string"
    },
    "form_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "確定した食材形態",
      "title": "Form Id"
    },
    "import_id": {
      "description": "レシート処理",
      "format": "uuid",
      "title": "Import Id",
      "type": "string"
    },
    "line_no": {
      "description": "レシート内の表示順",
      "exclusiveMinimum": 0.0,
      "title": "Line No",
      "type": "integer"
    },
    "pantry_lot_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録したロット",
      "title": "Pantry Lot Id"
    },
    "product_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "確定した商品版",
      "title": "Product Version Id"
    },
    "raw_name": {
      "description": "利用者が確認できる商品原表記",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Raw Name",
      "type": "string"
    },
    "unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "確定数量の単位",
      "title": "Unit Id"
    }
  },
  "required": [
    "import_id",
    "line_no",
    "raw_name",
    "decision"
  ],
  "title": "ReceiptLineWrite",
  "type": "object"
}
```

## ReceiptRequest



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| allowDuplicate | boolean | 任意 | default=false | Allowduplicate |
| candidates | array&lt;ReceiptCandidate&gt; | 必須 | minItems=1; maxItems=200 | Candidates |
| customFoods | array&lt;Food&gt; | 任意 | maxItems=200 | Customfoods |
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9007199254740990.0 | Expectedversion |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| imageHash | string | 必須 | pattern="^[a-f0-9]{64}$" | Imagehash |
| purchaseSignature | string | 必須 | pattern="^[a-f0-9]{64}$" | Purchasesignature |

```json
{
  "additionalProperties": false,
  "properties": {
    "allowDuplicate": {
      "default": false,
      "title": "Allowduplicate",
      "type": "boolean"
    },
    "candidates": {
      "items": {
        "$ref": "#/components/schemas/ReceiptCandidate"
      },
      "maxItems": 200,
      "minItems": 1,
      "title": "Candidates",
      "type": "array"
    },
    "customFoods": {
      "items": {
        "$ref": "#/components/schemas/Food"
      },
      "maxItems": 200,
      "title": "Customfoods",
      "type": "array"
    },
    "expectedVersion": {
      "maximum": 9007199254740990.0,
      "minimum": 0.0,
      "title": "Expectedversion",
      "type": "integer"
    },
    "id": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Id",
      "type": "string"
    },
    "imageHash": {
      "pattern": "^[a-f0-9]{64}$",
      "title": "Imagehash",
      "type": "string"
    },
    "purchaseSignature": {
      "pattern": "^[a-f0-9]{64}$",
      "title": "Purchasesignature",
      "type": "string"
    }
  },
  "required": [
    "expectedVersion",
    "id",
    "imageHash",
    "purchaseSignature",
    "candidates"
  ],
  "title": "ReceiptRequest",
  "type": "object"
}
```

## Recipe



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| arrangementIds | array&lt;string&gt; | 必須 | maxItems=100; 要素の制約=minLength=1; maxLength=128 | Arrangementids |
| description | string | 必須 | maxLength=5000 | Description |
| equipment | array&lt;string&gt; | 必須 | maxItems=50; 要素の制約=maxLength=500 | Equipment |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| imageUrl | anyOf(string, null) | 任意 | anyOfの制約=string: maxLength=500 | Imageurl |
| ingredients | array&lt;RecipeIngredient&gt; | 必須 | maxItems=100 | Ingredients |
| minutes | number | 必須 | minimum=0.0; maximum=1000000.0 | Minutes |
| name | string | 必須 | maxLength=500 | Name |
| publicationStatus | string | 任意 | enum=["draft", "published", "withdrawn"]; default="draft" | Publicationstatus |
| sample | boolean | 必須 | 追加制約なし | Sample |
| servings | number | 必須 | maximum=1000.0; exclusiveMinimum=0.0 | Servings |
| steps | array&lt;RecipeStep&gt; | 必須 | maxItems=100 | Steps |
| tags | array&lt;string&gt; | 必須 | maxItems=100; 要素の制約=maxLength=500 | Tags |
| versionId | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=128 | Versionid |
| withdrawalReason | anyOf(string, null) | 任意 | anyOfの制約=string: maxLength=20000 | Withdrawalreason |

```json
{
  "additionalProperties": false,
  "properties": {
    "arrangementIds": {
      "items": {
        "maxLength": 128,
        "minLength": 1,
        "type": "string"
      },
      "maxItems": 100,
      "title": "Arrangementids",
      "type": "array"
    },
    "description": {
      "maxLength": 5000,
      "title": "Description",
      "type": "string"
    },
    "equipment": {
      "items": {
        "maxLength": 500,
        "type": "string"
      },
      "maxItems": 50,
      "title": "Equipment",
      "type": "array"
    },
    "id": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Id",
      "type": "string"
    },
    "imageUrl": {
      "anyOf": [
        {
          "maxLength": 500,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Imageurl"
    },
    "ingredients": {
      "items": {
        "$ref": "#/components/schemas/RecipeIngredient"
      },
      "maxItems": 100,
      "title": "Ingredients",
      "type": "array"
    },
    "minutes": {
      "maximum": 1000000.0,
      "minimum": 0.0,
      "title": "Minutes",
      "type": "number"
    },
    "name": {
      "maxLength": 500,
      "title": "Name",
      "type": "string"
    },
    "publicationStatus": {
      "default": "draft",
      "enum": [
        "draft",
        "published",
        "withdrawn"
      ],
      "title": "Publicationstatus",
      "type": "string"
    },
    "sample": {
      "title": "Sample",
      "type": "boolean"
    },
    "servings": {
      "exclusiveMinimum": 0.0,
      "maximum": 1000.0,
      "title": "Servings",
      "type": "number"
    },
    "steps": {
      "items": {
        "$ref": "#/components/schemas/RecipeStep"
      },
      "maxItems": 100,
      "title": "Steps",
      "type": "array"
    },
    "tags": {
      "items": {
        "maxLength": 500,
        "type": "string"
      },
      "maxItems": 100,
      "title": "Tags",
      "type": "array"
    },
    "versionId": {
      "anyOf": [
        {
          "maxLength": 128,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Versionid"
    },
    "withdrawalReason": {
      "anyOf": [
        {
          "maxLength": 20000,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Withdrawalreason"
    }
  },
  "required": [
    "id",
    "name",
    "description",
    "servings",
    "minutes",
    "equipment",
    "ingredients",
    "steps",
    "arrangementIds",
    "tags",
    "sample"
  ],
  "title": "Recipe",
  "type": "object"
}
```

## RecipeDraft



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| adjusted | boolean | 必須 | 追加制約なし | Adjusted |
| amounts | object | 必須 | additionalProperties={"$ref": "#/components/schemas/Quantity"} | Amounts |
| recipeId | string | 必須 | minLength=1; maxLength=128 | Recipeid |
| recipeVersionId | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=128 | Recipeversionid |
| servings | number | 必須 | maximum=1000.0; exclusiveMinimum=0.0 | Servings |

```json
{
  "additionalProperties": false,
  "properties": {
    "adjusted": {
      "title": "Adjusted",
      "type": "boolean"
    },
    "amounts": {
      "additionalProperties": {
        "$ref": "#/components/schemas/Quantity"
      },
      "propertyNames": {
        "maxLength": 128,
        "minLength": 1
      },
      "title": "Amounts",
      "type": "object"
    },
    "recipeId": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Recipeid",
      "type": "string"
    },
    "recipeVersionId": {
      "anyOf": [
        {
          "maxLength": 128,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Recipeversionid"
    },
    "servings": {
      "exclusiveMinimum": 0.0,
      "maximum": 1000.0,
      "title": "Servings",
      "type": "number"
    }
  },
  "required": [
    "recipeId",
    "servings",
    "amounts",
    "adjusted"
  ],
  "title": "RecipeDraft",
  "type": "object"
}
```

## RecipeEmbeddingRow

近似検索用特徴量のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| content_hash | string | 必須 | minLength=64; maxLength=64 | 入力内容ハッシュ |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時 |
| created_for_index | string | 必須 | minLength=1; maxLength=20000 | 検索索引版 |
| embedding | array&lt;number&gt; | 必須 | minItems=768; maxItems=768 | 仮定768次元float32 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変ID |
| model_version | string | 必須 | minLength=1; maxLength=20000 | 埋め込みモデル固定版 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 対象版 |

```json
{
  "additionalProperties": false,
  "description": "近似検索用特徴量のDB応答。",
  "properties": {
    "content_hash": {
      "description": "入力内容ハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Content Hash",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "created_for_index": {
      "description": "検索索引版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Created For Index",
      "type": "string"
    },
    "embedding": {
      "description": "仮定768次元float32",
      "items": {
        "type": "number"
      },
      "maxItems": 768,
      "minItems": 768,
      "title": "Embedding",
      "type": "array"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変ID",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "model_version": {
      "description": "埋め込みモデル固定版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Model Version",
      "type": "string"
    },
    "recipe_version_id": {
      "description": "対象版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "recipe_version_id",
    "model_version",
    "content_hash",
    "embedding",
    "created_for_index",
    "etag"
  ],
  "title": "RecipeEmbeddingRow",
  "type": "object"
}
```

## RecipeEmbeddingWrite

近似検索用特徴量の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| content_hash | string | 必須 | minLength=64; maxLength=64 | 入力内容ハッシュ |
| created_for_index | string | 必須 | minLength=1; maxLength=20000 | 検索索引版 |
| embedding | array&lt;number&gt; | 必須 | minItems=768; maxItems=768 | 仮定768次元float32 |
| model_version | string | 必須 | minLength=1; maxLength=20000 | 埋め込みモデル固定版 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 対象版 |

```json
{
  "additionalProperties": false,
  "description": "近似検索用特徴量の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "content_hash": {
      "description": "入力内容ハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Content Hash",
      "type": "string"
    },
    "created_for_index": {
      "description": "検索索引版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Created For Index",
      "type": "string"
    },
    "embedding": {
      "description": "仮定768次元float32",
      "items": {
        "type": "number"
      },
      "maxItems": 768,
      "minItems": 768,
      "title": "Embedding",
      "type": "array"
    },
    "model_version": {
      "description": "埋め込みモデル固定版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Model Version",
      "type": "string"
    },
    "recipe_version_id": {
      "description": "対象版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    }
  },
  "required": [
    "recipe_version_id",
    "model_version",
    "content_hash",
    "embedding",
    "created_for_index"
  ],
  "title": "RecipeEmbeddingWrite",
  "type": "object"
}
```

## RecipeIngredient



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| foodId | string | 必須 | minLength=1; maxLength=128 | Foodid |
| form | string | 必須 | maxLength=500 | Form |
| formId | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=128 | Formid |
| ingredientId | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=128 | Ingredientid |
| note | string | 必須 | maxLength=500 | Note |
| productVersionId | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=128 | Productversionid |
| quantity | Quantity | 必須 | 追加制約なし |  |

```json
{
  "additionalProperties": false,
  "properties": {
    "foodId": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Foodid",
      "type": "string"
    },
    "form": {
      "maxLength": 500,
      "title": "Form",
      "type": "string"
    },
    "formId": {
      "anyOf": [
        {
          "maxLength": 128,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Formid"
    },
    "ingredientId": {
      "anyOf": [
        {
          "maxLength": 128,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Ingredientid"
    },
    "note": {
      "maxLength": 500,
      "title": "Note",
      "type": "string"
    },
    "productVersionId": {
      "anyOf": [
        {
          "maxLength": 128,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Productversionid"
    },
    "quantity": {
      "$ref": "#/components/schemas/Quantity"
    }
  },
  "required": [
    "foodId",
    "quantity",
    "form",
    "note"
  ],
  "title": "RecipeIngredient",
  "type": "object"
}
```

## RecipeIngredientRow

レシピ材料明細のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 確定値または範囲下限 |
| amount_max | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 範囲上限 |
| amount_mode | string | 必須 | enum=["exact", "range", "to_taste"] | 確定/範囲/適量 |
| canonical_amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 登録版の基準量 |
| component_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | セット内構成品を使う場合 |
| conversion_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 非基準単位の換算根拠 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| demand_kind | string | 必須 | enum=["purchase", "utility", "kit_component"] | 購入対象区分 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| form_id | string (uuid) | 必須 | 追加制約なし | 使用形態 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| kit_parent_line_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 購入対象となるセットの親行 |
| line_no | integer | 必須 | exclusiveMinimum=0.0 | 表示順 |
| note | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=500 | 材料の補足 |
| optional | boolean | 必須 | 追加制約なし | 任意追加材料 |
| product_version_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 商品指定時の仕様版 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 親版 |
| role | string | 必須 | enum=["main", "support", "seasoning", "aroma", "texture", "garnish", "medium"] | 料理での役割 |
| scaling_rule_id | string (uuid) | 必須 | 追加制約なし | 人数変換規則 |
| unit_id | string (uuid) | 必須 | 追加制約なし | 登録単位 |

```json
{
  "additionalProperties": false,
  "description": "レシピ材料明細のDB応答。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "確定値または範囲下限",
      "title": "Amount"
    },
    "amount_max": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "範囲上限",
      "title": "Amount Max"
    },
    "amount_mode": {
      "description": "確定/範囲/適量",
      "enum": [
        "exact",
        "range",
        "to_taste"
      ],
      "title": "Amount Mode",
      "type": "string"
    },
    "canonical_amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録版の基準量",
      "title": "Canonical Amount"
    },
    "component_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "セット内構成品を使う場合",
      "title": "Component Id"
    },
    "conversion_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "非基準単位の換算根拠",
      "title": "Conversion Id"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "demand_kind": {
      "description": "購入対象区分",
      "enum": [
        "purchase",
        "utility",
        "kit_component"
      ],
      "title": "Demand Kind",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "form_id": {
      "description": "使用形態",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "kit_parent_line_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入対象となるセットの親行",
      "title": "Kit Parent Line Id"
    },
    "line_no": {
      "description": "表示順",
      "exclusiveMinimum": 0.0,
      "title": "Line No",
      "type": "integer"
    },
    "note": {
      "anyOf": [
        {
          "maxLength": 500,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "材料の補足",
      "title": "Note"
    },
    "optional": {
      "description": "任意追加材料",
      "title": "Optional",
      "type": "boolean"
    },
    "product_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "商品指定時の仕様版",
      "title": "Product Version Id"
    },
    "recipe_version_id": {
      "description": "親版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "role": {
      "description": "料理での役割",
      "enum": [
        "main",
        "support",
        "seasoning",
        "aroma",
        "texture",
        "garnish",
        "medium"
      ],
      "title": "Role",
      "type": "string"
    },
    "scaling_rule_id": {
      "description": "人数変換規則",
      "format": "uuid",
      "title": "Scaling Rule Id",
      "type": "string"
    },
    "unit_id": {
      "description": "登録単位",
      "format": "uuid",
      "title": "Unit Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "recipe_version_id",
    "line_no",
    "form_id",
    "product_version_id",
    "component_id",
    "kit_parent_line_id",
    "role",
    "demand_kind",
    "amount_mode",
    "amount",
    "amount_max",
    "unit_id",
    "canonical_amount",
    "conversion_id",
    "scaling_rule_id",
    "optional",
    "note",
    "etag"
  ],
  "title": "RecipeIngredientRow",
  "type": "object"
}
```

## RecipeIngredientWrite

レシピ材料明細の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 確定値または範囲下限 |
| amount_max | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 範囲上限 |
| amount_mode | string | 必須 | enum=["exact", "range", "to_taste"] | 確定/範囲/適量 |
| canonical_amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 登録版の基準量 |
| component_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | セット内構成品を使う場合 |
| conversion_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 非基準単位の換算根拠 |
| demand_kind | string | 必須 | enum=["purchase", "utility", "kit_component"] | 購入対象区分 |
| form_id | string (uuid) | 必須 | 追加制約なし | 使用形態 |
| kit_parent_line_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 購入対象となるセットの親行 |
| line_no | integer | 必須 | exclusiveMinimum=0.0 | 表示順 |
| note | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=500 | 材料の補足 |
| optional | boolean | 必須 | 追加制約なし | 任意追加材料 |
| product_version_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 商品指定時の仕様版 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 親版 |
| role | string | 必須 | enum=["main", "support", "seasoning", "aroma", "texture", "garnish", "medium"] | 料理での役割 |
| scaling_rule_id | string (uuid) | 必須 | 追加制約なし | 人数変換規則 |
| unit_id | string (uuid) | 必須 | 追加制約なし | 登録単位 |

```json
{
  "additionalProperties": false,
  "description": "レシピ材料明細の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "確定値または範囲下限",
      "title": "Amount"
    },
    "amount_max": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "範囲上限",
      "title": "Amount Max"
    },
    "amount_mode": {
      "description": "確定/範囲/適量",
      "enum": [
        "exact",
        "range",
        "to_taste"
      ],
      "title": "Amount Mode",
      "type": "string"
    },
    "canonical_amount": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "登録版の基準量",
      "title": "Canonical Amount"
    },
    "component_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "セット内構成品を使う場合",
      "title": "Component Id"
    },
    "conversion_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "非基準単位の換算根拠",
      "title": "Conversion Id"
    },
    "demand_kind": {
      "description": "購入対象区分",
      "enum": [
        "purchase",
        "utility",
        "kit_component"
      ],
      "title": "Demand Kind",
      "type": "string"
    },
    "form_id": {
      "description": "使用形態",
      "format": "uuid",
      "title": "Form Id",
      "type": "string"
    },
    "kit_parent_line_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入対象となるセットの親行",
      "title": "Kit Parent Line Id"
    },
    "line_no": {
      "description": "表示順",
      "exclusiveMinimum": 0.0,
      "title": "Line No",
      "type": "integer"
    },
    "note": {
      "anyOf": [
        {
          "maxLength": 500,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "材料の補足",
      "title": "Note"
    },
    "optional": {
      "description": "任意追加材料",
      "title": "Optional",
      "type": "boolean"
    },
    "product_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "商品指定時の仕様版",
      "title": "Product Version Id"
    },
    "recipe_version_id": {
      "description": "親版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "role": {
      "description": "料理での役割",
      "enum": [
        "main",
        "support",
        "seasoning",
        "aroma",
        "texture",
        "garnish",
        "medium"
      ],
      "title": "Role",
      "type": "string"
    },
    "scaling_rule_id": {
      "description": "人数変換規則",
      "format": "uuid",
      "title": "Scaling Rule Id",
      "type": "string"
    },
    "unit_id": {
      "description": "登録単位",
      "format": "uuid",
      "title": "Unit Id",
      "type": "string"
    }
  },
  "required": [
    "recipe_version_id",
    "line_no",
    "form_id",
    "role",
    "demand_kind",
    "amount_mode",
    "unit_id",
    "scaling_rule_id",
    "optional"
  ],
  "title": "RecipeIngredientWrite",
  "type": "object"
}
```

## RecipeOptionRow

版の分類・特徴のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| option_id | string (uuid) | 必須 | 追加制約なし | 特徴値 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 対象版 |

```json
{
  "additionalProperties": false,
  "description": "版の分類・特徴のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "option_id": {
      "description": "特徴値",
      "format": "uuid",
      "title": "Option Id",
      "type": "string"
    },
    "recipe_version_id": {
      "description": "対象版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "recipe_version_id",
    "option_id",
    "etag"
  ],
  "title": "RecipeOptionRow",
  "type": "object"
}
```

## RecipeOptionWrite

版の分類・特徴の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| option_id | string (uuid) | 必須 | 追加制約なし | 特徴値 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 対象版 |

```json
{
  "additionalProperties": false,
  "description": "版の分類・特徴の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "option_id": {
      "description": "特徴値",
      "format": "uuid",
      "title": "Option Id",
      "type": "string"
    },
    "recipe_version_id": {
      "description": "対象版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    }
  },
  "required": [
    "recipe_version_id",
    "option_id"
  ],
  "title": "RecipeOptionWrite",
  "type": "object"
}
```

## RecipeRow

レシピ同一性のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| family_option_id | string (uuid) | 必須 | 追加制約なし | 料理ファミリ |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| status | string | 必須 | enum=["draft", "published", "withdrawn"] | 公開状態 |
| title | string | 必須 | minLength=1; maxLength=500 | 代表名 |
| withdrawal_reason | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | 取下げ理由 |

```json
{
  "additionalProperties": false,
  "description": "レシピ同一性のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "family_option_id": {
      "description": "料理ファミリ",
      "format": "uuid",
      "title": "Family Option Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "status": {
      "description": "公開状態",
      "enum": [
        "draft",
        "published",
        "withdrawn"
      ],
      "title": "Status",
      "type": "string"
    },
    "title": {
      "description": "代表名",
      "maxLength": 500,
      "minLength": 1,
      "title": "Title",
      "type": "string"
    },
    "withdrawal_reason": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "取下げ理由",
      "title": "Withdrawal Reason"
    }
  },
  "required": [
    "id",
    "created_at",
    "title",
    "family_option_id",
    "status",
    "withdrawal_reason",
    "etag"
  ],
  "title": "RecipeRow",
  "type": "object"
}
```

## RecipeSearchDocumentRow

公開検索用文書のDB応答。

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

```json
{
  "additionalProperties": false,
  "description": "公開検索用文書のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "display_title": {
      "description": "表示タイトル",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Display Title",
      "type": "string"
    },
    "eligible": {
      "description": "公開可能か",
      "title": "Eligible",
      "type": "boolean"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "facet_option_ids": {
      "description": "料理・味等の検索軸",
      "items": {
        "format": "uuid",
        "type": "string"
      },
      "maxItems": 1024,
      "title": "Facet Option Ids",
      "type": "array"
    },
    "food_identity_ids": {
      "description": "検索用食品ID集合",
      "items": {
        "format": "uuid",
        "type": "string"
      },
      "maxItems": 1024,
      "title": "Food Identity Ids",
      "type": "array"
    },
    "id": {
      "description": "不変ID",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "projected_at": {
      "description": "更新時点",
      "format": "date-time",
      "title": "Projected At",
      "type": "string"
    },
    "projection_version": {
      "description": "検索文書の生成器版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Projection Version",
      "type": "string"
    },
    "published_version_id": {
      "description": "検索対象の公開版",
      "format": "uuid",
      "title": "Published Version Id",
      "type": "string"
    },
    "recipe_id": {
      "description": "同一性単位で1件",
      "format": "uuid",
      "title": "Recipe Id",
      "type": "string"
    },
    "search_text": {
      "description": "検索用本文",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Search Text",
      "type": "string"
    },
    "source_hash": {
      "description": "正本一致確認",
      "maxLength": 64,
      "minLength": 64,
      "title": "Source Hash",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "recipe_id",
    "published_version_id",
    "projection_version",
    "display_title",
    "food_identity_ids",
    "facet_option_ids",
    "search_text",
    "eligible",
    "source_hash",
    "projected_at",
    "etag"
  ],
  "title": "RecipeSearchDocumentRow",
  "type": "object"
}
```

## RecipeSignatureRow

内容重複判定署名のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| algorithm_version | string | 必須 | minLength=1; maxLength=20000 | 正規化アルゴリズム版 |
| canonical_payload | CanonicalRecipe-Output | 必須 | 追加制約なし | 正規化対象の監査用内容 |
| cluster_key | string | 必須 | minLength=1; maxLength=20000 | 料理近似群キー |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| exact_hash | string | 必須 | minLength=64; maxLength=64 | 材料比率・工程・主要条件のハッシュ |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 対象版 |

```json
{
  "additionalProperties": false,
  "description": "内容重複判定署名のDB応答。",
  "properties": {
    "algorithm_version": {
      "description": "正規化アルゴリズム版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Algorithm Version",
      "type": "string"
    },
    "canonical_payload": {
      "$ref": "#/components/schemas/CanonicalRecipe-Output",
      "description": "正規化対象の監査用内容"
    },
    "cluster_key": {
      "description": "料理近似群キー",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Cluster Key",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "exact_hash": {
      "description": "材料比率・工程・主要条件のハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Exact Hash",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "recipe_version_id": {
      "description": "対象版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "recipe_version_id",
    "algorithm_version",
    "exact_hash",
    "canonical_payload",
    "cluster_key",
    "etag"
  ],
  "title": "RecipeSignatureRow",
  "type": "object"
}
```

## RecipeSignatureWrite

内容重複判定署名の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| algorithm_version | string | 必須 | minLength=1; maxLength=20000 | 正規化アルゴリズム版 |
| canonical_payload | CanonicalRecipe-Input | 必須 | 追加制約なし | 正規化対象の監査用内容 |
| cluster_key | string | 必須 | minLength=1; maxLength=20000 | 料理近似群キー |
| exact_hash | string | 必須 | minLength=64; maxLength=64 | 材料比率・工程・主要条件のハッシュ |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 対象版 |

```json
{
  "additionalProperties": false,
  "description": "内容重複判定署名の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "algorithm_version": {
      "description": "正規化アルゴリズム版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Algorithm Version",
      "type": "string"
    },
    "canonical_payload": {
      "$ref": "#/components/schemas/CanonicalRecipe-Input",
      "description": "正規化対象の監査用内容"
    },
    "cluster_key": {
      "description": "料理近似群キー",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Cluster Key",
      "type": "string"
    },
    "exact_hash": {
      "description": "材料比率・工程・主要条件のハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Exact Hash",
      "type": "string"
    },
    "recipe_version_id": {
      "description": "対象版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    }
  },
  "required": [
    "recipe_version_id",
    "algorithm_version",
    "exact_hash",
    "canonical_payload",
    "cluster_key"
  ],
  "title": "RecipeSignatureWrite",
  "type": "object"
}
```

## RecipeSimilarityRow

近似レシピ関係のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| algorithm_version | string | 必須 | minLength=1; maxLength=20000 | 評価器版 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| explanation | string | 必須 | minLength=1; maxLength=20000 | 材料/味付/工程の一致差分 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| left_version_id | string (uuid) | 必須 | 追加制約なし | 左版 |
| right_version_id | string (uuid) | 必須 | 追加制約なし | 右版 |
| score | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 類似度0..1 |

```json
{
  "additionalProperties": false,
  "description": "近似レシピ関係のDB応答。",
  "properties": {
    "algorithm_version": {
      "description": "評価器版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Algorithm Version",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "explanation": {
      "description": "材料/味付/工程の一致差分",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Explanation",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "left_version_id": {
      "description": "左版",
      "format": "uuid",
      "title": "Left Version Id",
      "type": "string"
    },
    "right_version_id": {
      "description": "右版",
      "format": "uuid",
      "title": "Right Version Id",
      "type": "string"
    },
    "score": {
      "description": "類似度0..1",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Score",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "left_version_id",
    "right_version_id",
    "algorithm_version",
    "score",
    "explanation",
    "etag"
  ],
  "title": "RecipeSimilarityRow",
  "type": "object"
}
```

## RecipeSimilarityWrite

近似レシピ関係の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| algorithm_version | string | 必須 | minLength=1; maxLength=20000 | 評価器版 |
| explanation | string | 必須 | minLength=1; maxLength=20000 | 材料/味付/工程の一致差分 |
| left_version_id | string (uuid) | 必須 | 追加制約なし | 左版 |
| right_version_id | string (uuid) | 必須 | 追加制約なし | 右版 |
| score | anyOf(number, string) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 類似度0..1 |

```json
{
  "additionalProperties": false,
  "description": "近似レシピ関係の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "algorithm_version": {
      "description": "評価器版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Algorithm Version",
      "type": "string"
    },
    "explanation": {
      "description": "材料/味付/工程の一致差分",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Explanation",
      "type": "string"
    },
    "left_version_id": {
      "description": "左版",
      "format": "uuid",
      "title": "Left Version Id",
      "type": "string"
    },
    "right_version_id": {
      "description": "右版",
      "format": "uuid",
      "title": "Right Version Id",
      "type": "string"
    },
    "score": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "類似度0..1",
      "title": "Score"
    }
  },
  "required": [
    "left_version_id",
    "right_version_id",
    "algorithm_version",
    "score",
    "explanation"
  ],
  "title": "RecipeSimilarityWrite",
  "type": "object"
}
```

## RecipeStep



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| equipment | array&lt;string&gt; | 必須 | maxItems=50; 要素の制約=maxLength=500 | Equipment |
| guide | anyOf(string, null) | 必須 | anyOfの制約=string: maxLength=500 | Guide |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| instruction | string | 必須 | maxLength=5000 | Instruction |
| minutes | number | 必須 | minimum=0.0; maximum=1000000.0 | Minutes |
| mode | string | 必須 | enum=["active", "passive", "monitored"] | Mode |
| title | string | 必須 | maxLength=500 | Title |

```json
{
  "additionalProperties": false,
  "properties": {
    "equipment": {
      "items": {
        "maxLength": 500,
        "type": "string"
      },
      "maxItems": 50,
      "title": "Equipment",
      "type": "array"
    },
    "guide": {
      "anyOf": [
        {
          "maxLength": 500,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Guide"
    },
    "id": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Id",
      "type": "string"
    },
    "instruction": {
      "maxLength": 5000,
      "title": "Instruction",
      "type": "string"
    },
    "minutes": {
      "maximum": 1000000.0,
      "minimum": 0.0,
      "title": "Minutes",
      "type": "number"
    },
    "mode": {
      "enum": [
        "active",
        "passive",
        "monitored"
      ],
      "title": "Mode",
      "type": "string"
    },
    "title": {
      "maxLength": 500,
      "title": "Title",
      "type": "string"
    }
  },
  "required": [
    "id",
    "title",
    "instruction",
    "minutes",
    "mode",
    "equipment",
    "guide"
  ],
  "title": "RecipeStep",
  "type": "object"
}
```

## RecipeStepRow

調理工程節点のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| attention | string | 必須 | enum=["active", "monitored", "passive"] | 作業者拘束 |
| completion_cue | string | 必須 | minLength=1; maxLength=20000 | 実測・目視の終了条件 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| duration_max_s | integer | 必須 | 追加制約なし | 所要秒上限 |
| duration_min_s | integer | 必須 | minimum=0.0 | 所要秒下限 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| instruction | string | 必須 | minLength=1; maxLength=5000 | 個別補足 |
| operation_id | string (uuid) | 必須 | 追加制約なし | 標準動作 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 所属版 |
| scaling_rule_id | string (uuid) | 必須 | 追加制約なし | 時間の人数変更規則 |
| step_no | integer | 必須 | exclusiveMinimum=0.0 | 表示順(依存順とは別) |
| title | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=500 | 工程の短い見出し |

```json
{
  "additionalProperties": false,
  "description": "調理工程節点のDB応答。",
  "properties": {
    "attention": {
      "description": "作業者拘束",
      "enum": [
        "active",
        "monitored",
        "passive"
      ],
      "title": "Attention",
      "type": "string"
    },
    "completion_cue": {
      "description": "実測・目視の終了条件",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Completion Cue",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "duration_max_s": {
      "description": "所要秒上限",
      "title": "Duration Max S",
      "type": "integer"
    },
    "duration_min_s": {
      "description": "所要秒下限",
      "minimum": 0.0,
      "title": "Duration Min S",
      "type": "integer"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "instruction": {
      "description": "個別補足",
      "maxLength": 5000,
      "minLength": 1,
      "title": "Instruction",
      "type": "string"
    },
    "operation_id": {
      "description": "標準動作",
      "format": "uuid",
      "title": "Operation Id",
      "type": "string"
    },
    "recipe_version_id": {
      "description": "所属版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "scaling_rule_id": {
      "description": "時間の人数変更規則",
      "format": "uuid",
      "title": "Scaling Rule Id",
      "type": "string"
    },
    "step_no": {
      "description": "表示順(依存順とは別)",
      "exclusiveMinimum": 0.0,
      "title": "Step No",
      "type": "integer"
    },
    "title": {
      "anyOf": [
        {
          "maxLength": 500,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "工程の短い見出し",
      "title": "Title"
    }
  },
  "required": [
    "id",
    "created_at",
    "recipe_version_id",
    "step_no",
    "operation_id",
    "instruction",
    "attention",
    "duration_min_s",
    "duration_max_s",
    "scaling_rule_id",
    "completion_cue",
    "title",
    "etag"
  ],
  "title": "RecipeStepRow",
  "type": "object"
}
```

## RecipeStepWrite

調理工程節点の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| attention | string | 必須 | enum=["active", "monitored", "passive"] | 作業者拘束 |
| completion_cue | string | 必須 | minLength=1; maxLength=20000 | 実測・目視の終了条件 |
| duration_max_s | integer | 必須 | 追加制約なし | 所要秒上限 |
| duration_min_s | integer | 必須 | minimum=0.0 | 所要秒下限 |
| instruction | string | 必須 | minLength=1; maxLength=5000 | 個別補足 |
| operation_id | string (uuid) | 必須 | 追加制約なし | 標準動作 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 所属版 |
| scaling_rule_id | string (uuid) | 必須 | 追加制約なし | 時間の人数変更規則 |
| step_no | integer | 必須 | exclusiveMinimum=0.0 | 表示順(依存順とは別) |
| title | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=500 | 工程の短い見出し |

```json
{
  "additionalProperties": false,
  "description": "調理工程節点の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "attention": {
      "description": "作業者拘束",
      "enum": [
        "active",
        "monitored",
        "passive"
      ],
      "title": "Attention",
      "type": "string"
    },
    "completion_cue": {
      "description": "実測・目視の終了条件",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Completion Cue",
      "type": "string"
    },
    "duration_max_s": {
      "description": "所要秒上限",
      "title": "Duration Max S",
      "type": "integer"
    },
    "duration_min_s": {
      "description": "所要秒下限",
      "minimum": 0.0,
      "title": "Duration Min S",
      "type": "integer"
    },
    "instruction": {
      "description": "個別補足",
      "maxLength": 5000,
      "minLength": 1,
      "title": "Instruction",
      "type": "string"
    },
    "operation_id": {
      "description": "標準動作",
      "format": "uuid",
      "title": "Operation Id",
      "type": "string"
    },
    "recipe_version_id": {
      "description": "所属版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "scaling_rule_id": {
      "description": "時間の人数変更規則",
      "format": "uuid",
      "title": "Scaling Rule Id",
      "type": "string"
    },
    "step_no": {
      "description": "表示順(依存順とは別)",
      "exclusiveMinimum": 0.0,
      "title": "Step No",
      "type": "integer"
    },
    "title": {
      "anyOf": [
        {
          "maxLength": 500,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "工程の短い見出し",
      "title": "Title"
    }
  },
  "required": [
    "recipe_version_id",
    "step_no",
    "operation_id",
    "instruction",
    "attention",
    "duration_min_s",
    "duration_max_s",
    "scaling_rule_id",
    "completion_cue"
  ],
  "title": "RecipeStepWrite",
  "type": "object"
}
```

## RecipeVersionRow

レシピ内容版のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| base_servings | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 登録分量が何人前か |
| content_hash | string | 必須 | minLength=64; maxLength=64 | 内容ハッシュ |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| description | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=5000 | 料理の紹介文 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| output_amount | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 完成量 |
| output_unit_id | string (uuid) | 必須 | 追加制約なし | 完成量単位 |
| published_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 公開日時 |
| recipe_id | string (uuid) | 必須 | 追加制約なし | 所属レシピ |
| release_id | string (uuid) | 必須 | 追加制約なし | 採用カタログ版 |
| status | string | 必須 | enum=["draft", "published", "withdrawn"] | 版の状態 |
| validation | string | 必須 | enum=["pending", "passed", "failed", "needs_review"] | 公開審査 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 版番号 |

```json
{
  "additionalProperties": false,
  "description": "レシピ内容版のDB応答。",
  "properties": {
    "base_servings": {
      "description": "登録分量が何人前か",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Base Servings",
      "type": "string"
    },
    "content_hash": {
      "description": "内容ハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Content Hash",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "description": {
      "anyOf": [
        {
          "maxLength": 5000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "料理の紹介文",
      "title": "Description"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "output_amount": {
      "description": "完成量",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Output Amount",
      "type": "string"
    },
    "output_unit_id": {
      "description": "完成量単位",
      "format": "uuid",
      "title": "Output Unit Id",
      "type": "string"
    },
    "published_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "公開日時",
      "title": "Published At"
    },
    "recipe_id": {
      "description": "所属レシピ",
      "format": "uuid",
      "title": "Recipe Id",
      "type": "string"
    },
    "release_id": {
      "description": "採用カタログ版",
      "format": "uuid",
      "title": "Release Id",
      "type": "string"
    },
    "status": {
      "description": "版の状態",
      "enum": [
        "draft",
        "published",
        "withdrawn"
      ],
      "title": "Status",
      "type": "string"
    },
    "validation": {
      "description": "公開審査",
      "enum": [
        "pending",
        "passed",
        "failed",
        "needs_review"
      ],
      "title": "Validation",
      "type": "string"
    },
    "version": {
      "description": "版番号",
      "exclusiveMinimum": 0.0,
      "title": "Version",
      "type": "integer"
    }
  },
  "required": [
    "id",
    "created_at",
    "recipe_id",
    "version",
    "release_id",
    "base_servings",
    "output_amount",
    "output_unit_id",
    "status",
    "validation",
    "content_hash",
    "published_at",
    "description",
    "etag"
  ],
  "title": "RecipeVersionRow",
  "type": "object"
}
```

## RecipeVersionWrite

レシピ内容版の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| base_servings | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 登録分量が何人前か |
| content_hash | string | 必須 | minLength=64; maxLength=64 | 内容ハッシュ |
| description | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=5000 | 料理の紹介文 |
| output_amount | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 完成量 |
| output_unit_id | string (uuid) | 必須 | 追加制約なし | 完成量単位 |
| published_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 公開日時 |
| recipe_id | string (uuid) | 必須 | 追加制約なし | 所属レシピ |
| release_id | string (uuid) | 必須 | 追加制約なし | 採用カタログ版 |
| status | string | 必須 | enum=["draft", "published", "withdrawn"] | 版の状態 |
| validation | string | 必須 | enum=["pending", "passed", "failed", "needs_review"] | 公開審査 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 版番号 |

```json
{
  "additionalProperties": false,
  "description": "レシピ内容版の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "base_servings": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "登録分量が何人前か",
      "title": "Base Servings"
    },
    "content_hash": {
      "description": "内容ハッシュ",
      "maxLength": 64,
      "minLength": 64,
      "title": "Content Hash",
      "type": "string"
    },
    "description": {
      "anyOf": [
        {
          "maxLength": 5000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "料理の紹介文",
      "title": "Description"
    },
    "output_amount": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "完成量",
      "title": "Output Amount"
    },
    "output_unit_id": {
      "description": "完成量単位",
      "format": "uuid",
      "title": "Output Unit Id",
      "type": "string"
    },
    "published_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "公開日時",
      "title": "Published At"
    },
    "recipe_id": {
      "description": "所属レシピ",
      "format": "uuid",
      "title": "Recipe Id",
      "type": "string"
    },
    "release_id": {
      "description": "採用カタログ版",
      "format": "uuid",
      "title": "Release Id",
      "type": "string"
    },
    "status": {
      "description": "版の状態",
      "enum": [
        "draft",
        "published",
        "withdrawn"
      ],
      "title": "Status",
      "type": "string"
    },
    "validation": {
      "description": "公開審査",
      "enum": [
        "pending",
        "passed",
        "failed",
        "needs_review"
      ],
      "title": "Validation",
      "type": "string"
    },
    "version": {
      "description": "版番号",
      "exclusiveMinimum": 0.0,
      "title": "Version",
      "type": "integer"
    }
  },
  "required": [
    "recipe_id",
    "version",
    "release_id",
    "base_servings",
    "output_amount",
    "output_unit_id",
    "status",
    "validation",
    "content_hash"
  ],
  "title": "RecipeVersionWrite",
  "type": "object"
}
```

## RecipeWrite

レシピ同一性の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| family_option_id | string (uuid) | 必須 | 追加制約なし | 料理ファミリ |
| status | string | 必須 | enum=["draft", "published", "withdrawn"] | 公開状態 |
| title | string | 必須 | minLength=1; maxLength=500 | 代表名 |
| withdrawal_reason | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | 取下げ理由 |

```json
{
  "additionalProperties": false,
  "description": "レシピ同一性の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "family_option_id": {
      "description": "料理ファミリ",
      "format": "uuid",
      "title": "Family Option Id",
      "type": "string"
    },
    "status": {
      "description": "公開状態",
      "enum": [
        "draft",
        "published",
        "withdrawn"
      ],
      "title": "Status",
      "type": "string"
    },
    "title": {
      "description": "代表名",
      "maxLength": 500,
      "minLength": 1,
      "title": "Title",
      "type": "string"
    },
    "withdrawal_reason": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "取下げ理由",
      "title": "Withdrawal Reason"
    }
  },
  "required": [
    "title",
    "family_option_id",
    "status"
  ],
  "title": "RecipeWrite",
  "type": "object"
}
```

## RecipesResponse



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| items | array&lt;Recipe&gt; | 必須 | 追加制約なし | Items |
| limit | integer | 必須 | 追加制約なし | Limit |
| offset | integer | 必須 | 追加制約なし | Offset |
| total | integer | 必須 | 追加制約なし | Total |

```json
{
  "additionalProperties": false,
  "properties": {
    "items": {
      "items": {
        "$ref": "#/components/schemas/Recipe"
      },
      "title": "Items",
      "type": "array"
    },
    "limit": {
      "title": "Limit",
      "type": "integer"
    },
    "offset": {
      "title": "Offset",
      "type": "integer"
    },
    "total": {
      "title": "Total",
      "type": "integer"
    }
  },
  "required": [
    "items",
    "total",
    "limit",
    "offset"
  ],
  "title": "RecipesResponse",
  "type": "object"
}
```

## ResourceReservationRow

資源の予約のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| end_s | integer | 必須 | 追加制約なし | 占有終了 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| quantity | integer | 必須 | exclusiveMinimum=0.0 | 占有量 |
| resource_id | string (uuid) | 必須 | 追加制約なし | 実資源 |
| start_s | integer | 必須 | minimum=0.0 | 占有開始 |
| task_id | string (uuid) | 必須 | 追加制約なし | 使用タスク |

```json
{
  "additionalProperties": false,
  "description": "資源の予約のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "end_s": {
      "description": "占有終了",
      "title": "End S",
      "type": "integer"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "quantity": {
      "description": "占有量",
      "exclusiveMinimum": 0.0,
      "title": "Quantity",
      "type": "integer"
    },
    "resource_id": {
      "description": "実資源",
      "format": "uuid",
      "title": "Resource Id",
      "type": "string"
    },
    "start_s": {
      "description": "占有開始",
      "minimum": 0.0,
      "title": "Start S",
      "type": "integer"
    },
    "task_id": {
      "description": "使用タスク",
      "format": "uuid",
      "title": "Task Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "task_id",
    "resource_id",
    "start_s",
    "end_s",
    "quantity",
    "etag"
  ],
  "title": "ResourceReservationRow",
  "type": "object"
}
```

## ResourceReservationWrite

資源の予約の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| end_s | integer | 必須 | 追加制約なし | 占有終了 |
| quantity | integer | 必須 | exclusiveMinimum=0.0 | 占有量 |
| resource_id | string (uuid) | 必須 | 追加制約なし | 実資源 |
| start_s | integer | 必須 | minimum=0.0 | 占有開始 |
| task_id | string (uuid) | 必須 | 追加制約なし | 使用タスク |

```json
{
  "additionalProperties": false,
  "description": "資源の予約の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "end_s": {
      "description": "占有終了",
      "title": "End S",
      "type": "integer"
    },
    "quantity": {
      "description": "占有量",
      "exclusiveMinimum": 0.0,
      "title": "Quantity",
      "type": "integer"
    },
    "resource_id": {
      "description": "実資源",
      "format": "uuid",
      "title": "Resource Id",
      "type": "string"
    },
    "start_s": {
      "description": "占有開始",
      "minimum": 0.0,
      "title": "Start S",
      "type": "integer"
    },
    "task_id": {
      "description": "使用タスク",
      "format": "uuid",
      "title": "Task Id",
      "type": "string"
    }
  },
  "required": [
    "task_id",
    "resource_id",
    "start_s",
    "end_s",
    "quantity"
  ],
  "title": "ResourceReservationWrite",
  "type": "object"
}
```

## ResourceTypeRow

道具・設備・作業者種別のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| capacity_unit_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 鍋容量等の単位 |
| code | string | 必須 | minLength=1; maxLength=20000 | burner/pan/person等 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| name | string | 必須 | minLength=1; maxLength=500 | 道具名 |
| status | string | 必須 | enum=["active", "retired"] | 使用状態 |

```json
{
  "additionalProperties": false,
  "description": "道具・設備・作業者種別のDB応答。",
  "properties": {
    "capacity_unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "鍋容量等の単位",
      "title": "Capacity Unit Id"
    },
    "code": {
      "description": "burner/pan/person等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "name": {
      "description": "道具名",
      "maxLength": 500,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "status": {
      "description": "使用状態",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "code",
    "name",
    "capacity_unit_id",
    "status",
    "etag"
  ],
  "title": "ResourceTypeRow",
  "type": "object"
}
```

## ResourceTypeWrite

道具・設備・作業者種別の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| capacity_unit_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 鍋容量等の単位 |
| code | string | 必須 | minLength=1; maxLength=20000 | burner/pan/person等 |
| name | string | 必須 | minLength=1; maxLength=500 | 道具名 |
| status | string | 必須 | enum=["active", "retired"] | 使用状態 |

```json
{
  "additionalProperties": false,
  "description": "道具・設備・作業者種別の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "capacity_unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "鍋容量等の単位",
      "title": "Capacity Unit Id"
    },
    "code": {
      "description": "burner/pan/person等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "name": {
      "description": "道具名",
      "maxLength": 500,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "status": {
      "description": "使用状態",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "code",
    "name",
    "status"
  ],
  "title": "ResourceTypeWrite",
  "type": "object"
}
```

## RevisionRequest



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9007199254740990.0 | Expectedversion |

```json
{
  "additionalProperties": false,
  "properties": {
    "expectedVersion": {
      "maximum": 9007199254740990.0,
      "minimum": 0.0,
      "title": "Expectedversion",
      "type": "integer"
    }
  },
  "required": [
    "expectedVersion"
  ],
  "title": "RevisionRequest",
  "type": "object"
}
```

## ScalingPointRow

検証済み換算点のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| multiplier | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 登録量への倍率 |
| rule_id | string (uuid) | 必須 | 追加制約なし | 曲線規則 |
| servings | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 人数 |

```json
{
  "additionalProperties": false,
  "description": "検証済み換算点のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "multiplier": {
      "description": "登録量への倍率",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Multiplier",
      "type": "string"
    },
    "rule_id": {
      "description": "曲線規則",
      "format": "uuid",
      "title": "Rule Id",
      "type": "string"
    },
    "servings": {
      "description": "人数",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Servings",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "rule_id",
    "servings",
    "multiplier",
    "etag"
  ],
  "title": "ScalingPointRow",
  "type": "object"
}
```

## ScalingPointWrite

検証済み換算点の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| multiplier | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 登録量への倍率 |
| rule_id | string (uuid) | 必須 | 追加制約なし | 曲線規則 |
| servings | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 人数 |

```json
{
  "additionalProperties": false,
  "description": "検証済み換算点の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "multiplier": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "登録量への倍率",
      "title": "Multiplier"
    },
    "rule_id": {
      "description": "曲線規則",
      "format": "uuid",
      "title": "Rule Id",
      "type": "string"
    },
    "servings": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "人数",
      "title": "Servings"
    }
  },
  "required": [
    "rule_id",
    "servings",
    "multiplier"
  ],
  "title": "ScalingPointWrite",
  "type": "object"
}
```

## ScalingRuleRow

人数変更規則のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| batch_capacity | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 1バッチ上限 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| max_servings | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 検証済み人数上限 |
| min_servings | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 検証済み人数下限 |
| mode | string | 必須 | enum=["linear", "fixed_batch", "capacity_batch", "validated_curve", "manual"] | 比例・バッチ等 |
| name | string | 必須 | minLength=1; maxLength=20000 | 規則名 |
| round_increment | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 表示・購入の刻み |
| round_mode | string | 必須 | enum=["none", "half_up", "ceil"] | 表示丸め |
| source_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 検証根拠 |

```json
{
  "additionalProperties": false,
  "description": "人数変更規則のDB応答。",
  "properties": {
    "batch_capacity": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "1バッチ上限",
      "title": "Batch Capacity"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "max_servings": {
      "description": "検証済み人数上限",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Max Servings",
      "type": "string"
    },
    "min_servings": {
      "description": "検証済み人数下限",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Min Servings",
      "type": "string"
    },
    "mode": {
      "description": "比例・バッチ等",
      "enum": [
        "linear",
        "fixed_batch",
        "capacity_batch",
        "validated_curve",
        "manual"
      ],
      "title": "Mode",
      "type": "string"
    },
    "name": {
      "description": "規則名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "round_increment": {
      "description": "表示・購入の刻み",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Round Increment",
      "type": "string"
    },
    "round_mode": {
      "description": "表示丸め",
      "enum": [
        "none",
        "half_up",
        "ceil"
      ],
      "title": "Round Mode",
      "type": "string"
    },
    "source_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "検証根拠",
      "title": "Source Id"
    }
  },
  "required": [
    "id",
    "created_at",
    "name",
    "mode",
    "min_servings",
    "max_servings",
    "batch_capacity",
    "round_mode",
    "round_increment",
    "source_id",
    "etag"
  ],
  "title": "ScalingRuleRow",
  "type": "object"
}
```

## ScalingRuleWrite

人数変更規則の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| batch_capacity | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 1バッチ上限 |
| max_servings | anyOf(number, string) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 検証済み人数上限 |
| min_servings | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 検証済み人数下限 |
| mode | string | 必須 | enum=["linear", "fixed_batch", "capacity_batch", "validated_curve", "manual"] | 比例・バッチ等 |
| name | string | 必須 | minLength=1; maxLength=20000 | 規則名 |
| round_increment | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 表示・購入の刻み |
| round_mode | string | 必須 | enum=["none", "half_up", "ceil"] | 表示丸め |
| source_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 検証根拠 |

```json
{
  "additionalProperties": false,
  "description": "人数変更規則の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "batch_capacity": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "1バッチ上限",
      "title": "Batch Capacity"
    },
    "max_servings": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "検証済み人数上限",
      "title": "Max Servings"
    },
    "min_servings": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "検証済み人数下限",
      "title": "Min Servings"
    },
    "mode": {
      "description": "比例・バッチ等",
      "enum": [
        "linear",
        "fixed_batch",
        "capacity_batch",
        "validated_curve",
        "manual"
      ],
      "title": "Mode",
      "type": "string"
    },
    "name": {
      "description": "規則名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "round_increment": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "表示・購入の刻み",
      "title": "Round Increment"
    },
    "round_mode": {
      "description": "表示丸め",
      "enum": [
        "none",
        "half_up",
        "ceil"
      ],
      "title": "Round Mode",
      "type": "string"
    },
    "source_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "検証根拠",
      "title": "Source Id"
    }
  },
  "required": [
    "name",
    "mode",
    "min_servings",
    "max_servings",
    "round_mode",
    "round_increment"
  ],
  "title": "ScalingRuleWrite",
  "type": "object"
}
```

## SearchFilters



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| equipment | array&lt;string&gt; | 必須 | maxItems=50; 要素の制約=maxLength=500 | Equipment |
| match | string | 必須 | enum=["all", "any"] | Match |
| maxMinutes | anyOf(number, null) | 必須 | anyOfの制約=number: minimum=0.0; maximum=1000000.0 | Maxminutes |
| noShopping | boolean | 必須 | 追加制約なし | Noshopping |
| selectedFoodIds | array&lt;string&gt; | 必須 | maxItems=100; 要素の制約=minLength=1; maxLength=128 | Selectedfoodids |

```json
{
  "additionalProperties": false,
  "properties": {
    "equipment": {
      "items": {
        "maxLength": 500,
        "type": "string"
      },
      "maxItems": 50,
      "title": "Equipment",
      "type": "array"
    },
    "match": {
      "enum": [
        "all",
        "any"
      ],
      "title": "Match",
      "type": "string"
    },
    "maxMinutes": {
      "anyOf": [
        {
          "maximum": 1000000.0,
          "minimum": 0.0,
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Maxminutes"
    },
    "noShopping": {
      "title": "Noshopping",
      "type": "boolean"
    },
    "selectedFoodIds": {
      "items": {
        "maxLength": 128,
        "minLength": 1,
        "type": "string"
      },
      "maxItems": 100,
      "title": "Selectedfoodids",
      "type": "array"
    }
  },
  "required": [
    "selectedFoodIds",
    "match",
    "maxMinutes",
    "noShopping",
    "equipment"
  ],
  "title": "SearchFilters",
  "type": "object"
}
```

## SessionTaskRow

展開済み工程のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| actual_end_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 実完了 |
| actual_start_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 実開始 |
| batch_no | integer | 必須 | exclusiveMinimum=0.0 | 容量分割した回 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| menu_item_id | string (uuid) | 必須 | 追加制約なし | 料理 |
| planned_end_s | integer | 必須 | 追加制約なし | 終了相対秒 |
| planned_start_s | integer | 必須 | minimum=0.0 | 開始相対秒 |
| session_id | string (uuid) | 必須 | 追加制約なし | 実行 |
| status | string | 必須 | enum=["pending", "running", "completed", "skipped"] | 進捗 |
| step_id | string (uuid) | 必須 | 追加制約なし | 元工程 |
| timer_duration_s | anyOf(integer, null) | 必須 | 追加制約なし | 利用者が設定したタイマー秒数 |
| timer_started_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 稼働中タイマーの開始日時 |

```json
{
  "additionalProperties": false,
  "description": "展開済み工程のDB応答。",
  "properties": {
    "actual_end_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "実完了",
      "title": "Actual End At"
    },
    "actual_start_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "実開始",
      "title": "Actual Start At"
    },
    "batch_no": {
      "description": "容量分割した回",
      "exclusiveMinimum": 0.0,
      "title": "Batch No",
      "type": "integer"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "menu_item_id": {
      "description": "料理",
      "format": "uuid",
      "title": "Menu Item Id",
      "type": "string"
    },
    "planned_end_s": {
      "description": "終了相対秒",
      "title": "Planned End S",
      "type": "integer"
    },
    "planned_start_s": {
      "description": "開始相対秒",
      "minimum": 0.0,
      "title": "Planned Start S",
      "type": "integer"
    },
    "session_id": {
      "description": "実行",
      "format": "uuid",
      "title": "Session Id",
      "type": "string"
    },
    "status": {
      "description": "進捗",
      "enum": [
        "pending",
        "running",
        "completed",
        "skipped"
      ],
      "title": "Status",
      "type": "string"
    },
    "step_id": {
      "description": "元工程",
      "format": "uuid",
      "title": "Step Id",
      "type": "string"
    },
    "timer_duration_s": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "description": "利用者が設定したタイマー秒数",
      "title": "Timer Duration S"
    },
    "timer_started_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "稼働中タイマーの開始日時",
      "title": "Timer Started At"
    }
  },
  "required": [
    "id",
    "created_at",
    "session_id",
    "menu_item_id",
    "step_id",
    "batch_no",
    "planned_start_s",
    "planned_end_s",
    "status",
    "actual_start_at",
    "actual_end_at",
    "timer_started_at",
    "timer_duration_s",
    "etag"
  ],
  "title": "SessionTaskRow",
  "type": "object"
}
```

## SessionTaskWrite

展開済み工程の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| actual_end_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 実完了 |
| actual_start_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 実開始 |
| batch_no | integer | 必須 | exclusiveMinimum=0.0 | 容量分割した回 |
| menu_item_id | string (uuid) | 必須 | 追加制約なし | 料理 |
| planned_end_s | integer | 必須 | 追加制約なし | 終了相対秒 |
| planned_start_s | integer | 必須 | minimum=0.0 | 開始相対秒 |
| session_id | string (uuid) | 必須 | 追加制約なし | 実行 |
| status | string | 必須 | enum=["pending", "running", "completed", "skipped"] | 進捗 |
| step_id | string (uuid) | 必須 | 追加制約なし | 元工程 |
| timer_duration_s | anyOf(integer, null) | 任意 | 追加制約なし | 利用者が設定したタイマー秒数 |
| timer_started_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 稼働中タイマーの開始日時 |

```json
{
  "additionalProperties": false,
  "description": "展開済み工程の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "actual_end_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "実完了",
      "title": "Actual End At"
    },
    "actual_start_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "実開始",
      "title": "Actual Start At"
    },
    "batch_no": {
      "description": "容量分割した回",
      "exclusiveMinimum": 0.0,
      "title": "Batch No",
      "type": "integer"
    },
    "menu_item_id": {
      "description": "料理",
      "format": "uuid",
      "title": "Menu Item Id",
      "type": "string"
    },
    "planned_end_s": {
      "description": "終了相対秒",
      "title": "Planned End S",
      "type": "integer"
    },
    "planned_start_s": {
      "description": "開始相対秒",
      "minimum": 0.0,
      "title": "Planned Start S",
      "type": "integer"
    },
    "session_id": {
      "description": "実行",
      "format": "uuid",
      "title": "Session Id",
      "type": "string"
    },
    "status": {
      "description": "進捗",
      "enum": [
        "pending",
        "running",
        "completed",
        "skipped"
      ],
      "title": "Status",
      "type": "string"
    },
    "step_id": {
      "description": "元工程",
      "format": "uuid",
      "title": "Step Id",
      "type": "string"
    },
    "timer_duration_s": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "description": "利用者が設定したタイマー秒数",
      "title": "Timer Duration S"
    },
    "timer_started_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "稼働中タイマーの開始日時",
      "title": "Timer Started At"
    }
  },
  "required": [
    "session_id",
    "menu_item_id",
    "step_id",
    "batch_no",
    "planned_start_s",
    "planned_end_s",
    "status"
  ],
  "title": "SessionTaskWrite",
  "type": "object"
}
```

## Settings



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| equipment | array&lt;string&gt; | 必須 | maxItems=50; 要素の制約=maxLength=500 | Equipment |
| excludedFoodIds | array&lt;string&gt; | 必須 | maxItems=1000; 要素の制約=minLength=1; maxLength=128 | Excludedfoodids |
| pantryFoodIds | array&lt;string&gt; | 必須 | maxItems=1000; 要素の制約=minLength=1; maxLength=128 | Pantryfoodids |

```json
{
  "additionalProperties": false,
  "properties": {
    "equipment": {
      "items": {
        "maxLength": 500,
        "type": "string"
      },
      "maxItems": 50,
      "title": "Equipment",
      "type": "array"
    },
    "excludedFoodIds": {
      "items": {
        "maxLength": 128,
        "minLength": 1,
        "type": "string"
      },
      "maxItems": 1000,
      "title": "Excludedfoodids",
      "type": "array"
    },
    "pantryFoodIds": {
      "items": {
        "maxLength": 128,
        "minLength": 1,
        "type": "string"
      },
      "maxItems": 1000,
      "title": "Pantryfoodids",
      "type": "array"
    }
  },
  "required": [
    "excludedFoodIds",
    "pantryFoodIds",
    "equipment"
  ],
  "title": "Settings",
  "type": "object"
}
```

## SettingsRequest



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9007199254740990.0 | Expectedversion |
| settings | Settings | 必須 | 追加制約なし |  |

```json
{
  "additionalProperties": false,
  "properties": {
    "expectedVersion": {
      "maximum": 9007199254740990.0,
      "minimum": 0.0,
      "title": "Expectedversion",
      "type": "integer"
    },
    "settings": {
      "$ref": "#/components/schemas/Settings"
    }
  },
  "required": [
    "expectedVersion",
    "settings"
  ],
  "title": "SettingsRequest",
  "type": "object"
}
```

## ShoppingCheck



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| archived | boolean | 必須 | 追加制約なし | Archived |
| checkedAt | string | 必須 | maxLength=500 | Checkedat |
| foodId | string | 必須 | minLength=1; maxLength=128 | Foodid |
| key | string | 必須 | maxLength=500 | Key |
| quantity | Quantity | 必須 | 追加制約なし |  |
| signature | string | 必須 | maxLength=500 | Signature |

```json
{
  "additionalProperties": false,
  "properties": {
    "archived": {
      "title": "Archived",
      "type": "boolean"
    },
    "checkedAt": {
      "maxLength": 500,
      "title": "Checkedat",
      "type": "string"
    },
    "foodId": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Foodid",
      "type": "string"
    },
    "key": {
      "maxLength": 500,
      "title": "Key",
      "type": "string"
    },
    "quantity": {
      "$ref": "#/components/schemas/Quantity"
    },
    "signature": {
      "maxLength": 500,
      "title": "Signature",
      "type": "string"
    }
  },
  "required": [
    "key",
    "signature",
    "foodId",
    "quantity",
    "checkedAt",
    "archived"
  ],
  "title": "ShoppingCheck",
  "type": "object"
}
```

## ShoppingItemRow

買い物行のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| archived | boolean | 必須 | 追加制約なし | 完了した買い物の保管状態 |
| checked | boolean | 必須 | 追加制約なし | 購入済み |
| checked_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 購入確認日時 |
| client_key | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | 画面操作の安定キー |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| net_shortage | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 在庫控除後の不足量 |
| package_count | anyOf(integer, null) | 必須 | 追加制約なし | 購入包装数 |
| product_version_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 購入SKU |
| session_id | string (uuid) | 必須 | 追加制約なし | 対象調理 |
| surplus_amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 購入後余剰 |
| total_id | string (uuid) | 必須 | 追加制約なし | 需要行 |

```json
{
  "additionalProperties": false,
  "description": "買い物行のDB応答。",
  "properties": {
    "archived": {
      "description": "完了した買い物の保管状態",
      "title": "Archived",
      "type": "boolean"
    },
    "checked": {
      "description": "購入済み",
      "title": "Checked",
      "type": "boolean"
    },
    "checked_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入確認日時",
      "title": "Checked At"
    },
    "client_key": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "画面操作の安定キー",
      "title": "Client Key"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "net_shortage": {
      "description": "在庫控除後の不足量",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Net Shortage",
      "type": "string"
    },
    "package_count": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入包装数",
      "title": "Package Count"
    },
    "product_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入SKU",
      "title": "Product Version Id"
    },
    "session_id": {
      "description": "対象調理",
      "format": "uuid",
      "title": "Session Id",
      "type": "string"
    },
    "surplus_amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入後余剰",
      "title": "Surplus Amount"
    },
    "total_id": {
      "description": "需要行",
      "format": "uuid",
      "title": "Total Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "session_id",
    "total_id",
    "product_version_id",
    "net_shortage",
    "package_count",
    "surplus_amount",
    "checked",
    "client_key",
    "checked_at",
    "archived",
    "etag"
  ],
  "title": "ShoppingItemRow",
  "type": "object"
}
```

## ShoppingItemWrite

買い物行の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| archived | boolean | 必須 | 追加制約なし | 完了した買い物の保管状態 |
| checked | boolean | 必須 | 追加制約なし | 購入済み |
| checked_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 購入確認日時 |
| client_key | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | 画面操作の安定キー |
| net_shortage | anyOf(number, string) | 必須 | anyOfの制約=number: minimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 在庫控除後の不足量 |
| package_count | anyOf(integer, null) | 任意 | 追加制約なし | 購入包装数 |
| product_version_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 購入SKU |
| session_id | string (uuid) | 必須 | 追加制約なし | 対象調理 |
| surplus_amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 購入後余剰 |
| total_id | string (uuid) | 必須 | 追加制約なし | 需要行 |

```json
{
  "additionalProperties": false,
  "description": "買い物行の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "archived": {
      "description": "完了した買い物の保管状態",
      "title": "Archived",
      "type": "boolean"
    },
    "checked": {
      "description": "購入済み",
      "title": "Checked",
      "type": "boolean"
    },
    "checked_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入確認日時",
      "title": "Checked At"
    },
    "client_key": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "画面操作の安定キー",
      "title": "Client Key"
    },
    "net_shortage": {
      "anyOf": [
        {
          "minimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "在庫控除後の不足量",
      "title": "Net Shortage"
    },
    "package_count": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入包装数",
      "title": "Package Count"
    },
    "product_version_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入SKU",
      "title": "Product Version Id"
    },
    "session_id": {
      "description": "対象調理",
      "format": "uuid",
      "title": "Session Id",
      "type": "string"
    },
    "surplus_amount": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入後余剰",
      "title": "Surplus Amount"
    },
    "total_id": {
      "description": "需要行",
      "format": "uuid",
      "title": "Total Id",
      "type": "string"
    }
  },
  "required": [
    "session_id",
    "total_id",
    "net_shortage",
    "checked",
    "archived"
  ],
  "title": "ShoppingItemWrite",
  "type": "object"
}
```

## ShoppingRequest



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| checks | array&lt;ShoppingCheck&gt; | 必須 | maxItems=1000 | Checks |
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9007199254740990.0 | Expectedversion |

```json
{
  "additionalProperties": false,
  "properties": {
    "checks": {
      "items": {
        "$ref": "#/components/schemas/ShoppingCheck"
      },
      "maxItems": 1000,
      "title": "Checks",
      "type": "array"
    },
    "expectedVersion": {
      "maximum": 9007199254740990.0,
      "minimum": 0.0,
      "title": "Expectedversion",
      "type": "integer"
    }
  },
  "required": [
    "expectedVersion",
    "checks"
  ],
  "title": "ShoppingRequest",
  "type": "object"
}
```

## SourceRecordRow

根拠資料のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| content_hash | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=64; maxLength=64 | 参照内容のハッシュ |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| license_note | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | 利用条件・権利確認 |
| locator | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | 資料内位置 |
| retrieved_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 取得時点 |
| title | string | 必須 | minLength=1; maxLength=20000 | 根拠名 |
| url | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | 公式資料URL |

```json
{
  "additionalProperties": false,
  "description": "根拠資料のDB応答。",
  "properties": {
    "content_hash": {
      "anyOf": [
        {
          "maxLength": 64,
          "minLength": 64,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "参照内容のハッシュ",
      "title": "Content Hash"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "license_note": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "利用条件・権利確認",
      "title": "License Note"
    },
    "locator": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "資料内位置",
      "title": "Locator"
    },
    "retrieved_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "取得時点",
      "title": "Retrieved At"
    },
    "title": {
      "description": "根拠名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Title",
      "type": "string"
    },
    "url": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "公式資料URL",
      "title": "Url"
    }
  },
  "required": [
    "id",
    "created_at",
    "title",
    "url",
    "locator",
    "retrieved_at",
    "content_hash",
    "license_note",
    "etag"
  ],
  "title": "SourceRecordRow",
  "type": "object"
}
```

## SourceRecordWrite

根拠資料の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| content_hash | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=64; maxLength=64 | 参照内容のハッシュ |
| license_note | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | 利用条件・権利確認 |
| locator | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | 資料内位置 |
| retrieved_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 取得時点 |
| title | string | 必須 | minLength=1; maxLength=20000 | 根拠名 |
| url | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | 公式資料URL |

```json
{
  "additionalProperties": false,
  "description": "根拠資料の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "content_hash": {
      "anyOf": [
        {
          "maxLength": 64,
          "minLength": 64,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "参照内容のハッシュ",
      "title": "Content Hash"
    },
    "license_note": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "利用条件・権利確認",
      "title": "License Note"
    },
    "locator": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "資料内位置",
      "title": "Locator"
    },
    "retrieved_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "取得時点",
      "title": "Retrieved At"
    },
    "title": {
      "description": "根拠名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Title",
      "type": "string"
    },
    "url": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "公式資料URL",
      "title": "Url"
    }
  },
  "required": [
    "title"
  ],
  "title": "SourceRecordWrite",
  "type": "object"
}
```

## StepDependencyRow

工程依存辺のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| after_step_id | string (uuid) | 必須 | 追加制約なし | 後続工程 |
| before_step_id | string (uuid) | 必須 | 追加制約なし | 先行工程 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| kind | string | 必須 | enum=["material", "sequence", "safety", "quality"] | 依存理由 |
| max_lag_s | anyOf(integer, null) | 必須 | 追加制約なし | 品質上の最大待機 |
| min_lag_s | integer | 必須 | minimum=0.0 | 完了後最低待機 |

```json
{
  "additionalProperties": false,
  "description": "工程依存辺のDB応答。",
  "properties": {
    "after_step_id": {
      "description": "後続工程",
      "format": "uuid",
      "title": "After Step Id",
      "type": "string"
    },
    "before_step_id": {
      "description": "先行工程",
      "format": "uuid",
      "title": "Before Step Id",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "kind": {
      "description": "依存理由",
      "enum": [
        "material",
        "sequence",
        "safety",
        "quality"
      ],
      "title": "Kind",
      "type": "string"
    },
    "max_lag_s": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "description": "品質上の最大待機",
      "title": "Max Lag S"
    },
    "min_lag_s": {
      "description": "完了後最低待機",
      "minimum": 0.0,
      "title": "Min Lag S",
      "type": "integer"
    }
  },
  "required": [
    "id",
    "created_at",
    "before_step_id",
    "after_step_id",
    "kind",
    "min_lag_s",
    "max_lag_s",
    "etag"
  ],
  "title": "StepDependencyRow",
  "type": "object"
}
```

## StepDependencyWrite

工程依存辺の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| after_step_id | string (uuid) | 必須 | 追加制約なし | 後続工程 |
| before_step_id | string (uuid) | 必須 | 追加制約なし | 先行工程 |
| kind | string | 必須 | enum=["material", "sequence", "safety", "quality"] | 依存理由 |
| max_lag_s | anyOf(integer, null) | 任意 | 追加制約なし | 品質上の最大待機 |
| min_lag_s | integer | 必須 | minimum=0.0 | 完了後最低待機 |

```json
{
  "additionalProperties": false,
  "description": "工程依存辺の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "after_step_id": {
      "description": "後続工程",
      "format": "uuid",
      "title": "After Step Id",
      "type": "string"
    },
    "before_step_id": {
      "description": "先行工程",
      "format": "uuid",
      "title": "Before Step Id",
      "type": "string"
    },
    "kind": {
      "description": "依存理由",
      "enum": [
        "material",
        "sequence",
        "safety",
        "quality"
      ],
      "title": "Kind",
      "type": "string"
    },
    "max_lag_s": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "description": "品質上の最大待機",
      "title": "Max Lag S"
    },
    "min_lag_s": {
      "description": "完了後最低待機",
      "minimum": 0.0,
      "title": "Min Lag S",
      "type": "integer"
    }
  },
  "required": [
    "before_step_id",
    "after_step_id",
    "kind",
    "min_lag_s"
  ],
  "title": "StepDependencyWrite",
  "type": "object"
}
```

## StepInputRow

工程への材料受渡しのDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| fraction | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 当該節点生成量の利用割合 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| material_id | string (uuid) | 必須 | 追加制約なし | 受け渡す材料 |
| step_id | string (uuid) | 必須 | 追加制約なし | 受取工程 |

```json
{
  "additionalProperties": false,
  "description": "工程への材料受渡しのDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "fraction": {
      "description": "当該節点生成量の利用割合",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Fraction",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "material_id": {
      "description": "受け渡す材料",
      "format": "uuid",
      "title": "Material Id",
      "type": "string"
    },
    "step_id": {
      "description": "受取工程",
      "format": "uuid",
      "title": "Step Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "step_id",
    "material_id",
    "fraction",
    "etag"
  ],
  "title": "StepInputRow",
  "type": "object"
}
```

## StepInputWrite

工程への材料受渡しの編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| fraction | anyOf(number, string) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 当該節点生成量の利用割合 |
| material_id | string (uuid) | 必須 | 追加制約なし | 受け渡す材料 |
| step_id | string (uuid) | 必須 | 追加制約なし | 受取工程 |

```json
{
  "additionalProperties": false,
  "description": "工程への材料受渡しの編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "fraction": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "当該節点生成量の利用割合",
      "title": "Fraction"
    },
    "material_id": {
      "description": "受け渡す材料",
      "format": "uuid",
      "title": "Material Id",
      "type": "string"
    },
    "step_id": {
      "description": "受取工程",
      "format": "uuid",
      "title": "Step Id",
      "type": "string"
    }
  },
  "required": [
    "step_id",
    "material_id",
    "fraction"
  ],
  "title": "StepInputWrite",
  "type": "object"
}
```

## StepMediaRow

工程別メディア選択のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| end_ms | integer | 必須 | 追加制約なし | 終了点 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| media_id | string (uuid) | 必須 | 追加制約なし | 適用メディア |
| start_ms | integer | 必須 | minimum=0.0 | 表示開始点 |
| step_id | string (uuid) | 必須 | 追加制約なし | 対象工程 |

```json
{
  "additionalProperties": false,
  "description": "工程別メディア選択のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "end_ms": {
      "description": "終了点",
      "title": "End Ms",
      "type": "integer"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "media_id": {
      "description": "適用メディア",
      "format": "uuid",
      "title": "Media Id",
      "type": "string"
    },
    "start_ms": {
      "description": "表示開始点",
      "minimum": 0.0,
      "title": "Start Ms",
      "type": "integer"
    },
    "step_id": {
      "description": "対象工程",
      "format": "uuid",
      "title": "Step Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "step_id",
    "media_id",
    "start_ms",
    "end_ms",
    "etag"
  ],
  "title": "StepMediaRow",
  "type": "object"
}
```

## StepMediaWrite

工程別メディア選択の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| end_ms | integer | 必須 | 追加制約なし | 終了点 |
| media_id | string (uuid) | 必須 | 追加制約なし | 適用メディア |
| start_ms | integer | 必須 | minimum=0.0 | 表示開始点 |
| step_id | string (uuid) | 必須 | 追加制約なし | 対象工程 |

```json
{
  "additionalProperties": false,
  "description": "工程別メディア選択の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "end_ms": {
      "description": "終了点",
      "title": "End Ms",
      "type": "integer"
    },
    "media_id": {
      "description": "適用メディア",
      "format": "uuid",
      "title": "Media Id",
      "type": "string"
    },
    "start_ms": {
      "description": "表示開始点",
      "minimum": 0.0,
      "title": "Start Ms",
      "type": "integer"
    },
    "step_id": {
      "description": "対象工程",
      "format": "uuid",
      "title": "Step Id",
      "type": "string"
    }
  },
  "required": [
    "step_id",
    "media_id",
    "start_ms",
    "end_ms"
  ],
  "title": "StepMediaWrite",
  "type": "object"
}
```

## StepParameterRow

工程の型付きパラメータのDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| bool_value | anyOf(boolean, null) | 必須 | 追加制約なし | 真偽 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| number_value | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 数値 |
| parameter_id | string (uuid) | 必須 | 追加制約なし | 動作パラメータ |
| step_id | string (uuid) | 必須 | 追加制約なし | 対象工程 |
| text_value | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | 文字・optionコード |

```json
{
  "additionalProperties": false,
  "description": "工程の型付きパラメータのDB応答。",
  "properties": {
    "bool_value": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "description": "真偽",
      "title": "Bool Value"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "number_value": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "数値",
      "title": "Number Value"
    },
    "parameter_id": {
      "description": "動作パラメータ",
      "format": "uuid",
      "title": "Parameter Id",
      "type": "string"
    },
    "step_id": {
      "description": "対象工程",
      "format": "uuid",
      "title": "Step Id",
      "type": "string"
    },
    "text_value": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "文字・optionコード",
      "title": "Text Value"
    }
  },
  "required": [
    "id",
    "created_at",
    "step_id",
    "parameter_id",
    "number_value",
    "text_value",
    "bool_value",
    "etag"
  ],
  "title": "StepParameterRow",
  "type": "object"
}
```

## StepParameterWrite

工程の型付きパラメータの編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| bool_value | anyOf(boolean, null) | 任意 | 追加制約なし | 真偽 |
| number_value | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 数値 |
| parameter_id | string (uuid) | 必須 | 追加制約なし | 動作パラメータ |
| step_id | string (uuid) | 必須 | 追加制約なし | 対象工程 |
| text_value | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | 文字・optionコード |

```json
{
  "additionalProperties": false,
  "description": "工程の型付きパラメータの編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "bool_value": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "description": "真偽",
      "title": "Bool Value"
    },
    "number_value": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "数値",
      "title": "Number Value"
    },
    "parameter_id": {
      "description": "動作パラメータ",
      "format": "uuid",
      "title": "Parameter Id",
      "type": "string"
    },
    "step_id": {
      "description": "対象工程",
      "format": "uuid",
      "title": "Step Id",
      "type": "string"
    },
    "text_value": {
      "anyOf": [
        {
          "maxLength": 20000,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "文字・optionコード",
      "title": "Text Value"
    }
  },
  "required": [
    "step_id",
    "parameter_id"
  ],
  "title": "StepParameterWrite",
  "type": "object"
}
```

## StepResourceRow

工程の資源要求のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| capacity_min | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 必要最低容量 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| exclusive | boolean | 必須 | 追加制約なし | 占有するか |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| quantity | integer | 必須 | exclusiveMinimum=0.0 | 必要台数・人数 |
| resource_type_id | string (uuid) | 必須 | 追加制約なし | 要求種別 |
| step_id | string (uuid) | 必須 | 追加制約なし | 対象工程 |

```json
{
  "additionalProperties": false,
  "description": "工程の資源要求のDB応答。",
  "properties": {
    "capacity_min": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "必要最低容量",
      "title": "Capacity Min"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "exclusive": {
      "description": "占有するか",
      "title": "Exclusive",
      "type": "boolean"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "quantity": {
      "description": "必要台数・人数",
      "exclusiveMinimum": 0.0,
      "title": "Quantity",
      "type": "integer"
    },
    "resource_type_id": {
      "description": "要求種別",
      "format": "uuid",
      "title": "Resource Type Id",
      "type": "string"
    },
    "step_id": {
      "description": "対象工程",
      "format": "uuid",
      "title": "Step Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "step_id",
    "resource_type_id",
    "quantity",
    "capacity_min",
    "exclusive",
    "etag"
  ],
  "title": "StepResourceRow",
  "type": "object"
}
```

## StepResourceWrite

工程の資源要求の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| capacity_min | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 必要最低容量 |
| exclusive | boolean | 必須 | 追加制約なし | 占有するか |
| quantity | integer | 必須 | exclusiveMinimum=0.0 | 必要台数・人数 |
| resource_type_id | string (uuid) | 必須 | 追加制約なし | 要求種別 |
| step_id | string (uuid) | 必須 | 追加制約なし | 対象工程 |

```json
{
  "additionalProperties": false,
  "description": "工程の資源要求の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "capacity_min": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "必要最低容量",
      "title": "Capacity Min"
    },
    "exclusive": {
      "description": "占有するか",
      "title": "Exclusive",
      "type": "boolean"
    },
    "quantity": {
      "description": "必要台数・人数",
      "exclusiveMinimum": 0.0,
      "title": "Quantity",
      "type": "integer"
    },
    "resource_type_id": {
      "description": "要求種別",
      "format": "uuid",
      "title": "Resource Type Id",
      "type": "string"
    },
    "step_id": {
      "description": "対象工程",
      "format": "uuid",
      "title": "Step Id",
      "type": "string"
    }
  },
  "required": [
    "step_id",
    "resource_type_id",
    "quantity",
    "exclusive"
  ],
  "title": "StepResourceWrite",
  "type": "object"
}
```

## StockLot



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| consumed | array&lt;Quantity&gt; | 必須 | maxItems=1000 | Consumed |
| createdAt | string | 必須 | maxLength=500 | Createdat |
| edited | boolean | 必須 | 追加制約なし | Edited |
| expiresOn | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^\\d{4}-\\d{2}-\\d{2}$" | Expireson |
| foodId | string | 必須 | minLength=1; maxLength=128 | Foodid |
| form | string | 必須 | maxLength=500 | Form |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| location | string | 必須 | enum=["冷蔵", "冷凍", "常温"] | Location |
| originalFoodId | string | 必須 | minLength=1; maxLength=128 | Originalfoodid |
| originalQuantity | Quantity | 必須 | 追加制約なし |  |
| priority | boolean | 必須 | 追加制約なし | Priority |
| quantity | Quantity | 必須 | 追加制約なし |  |
| sourceImportId | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=128 | Sourceimportid |
| status | string | 必須 | enum=["active", "deleted", "undone"] | Status |
| updatedAt | string | 必須 | maxLength=500 | Updatedat |

```json
{
  "additionalProperties": false,
  "properties": {
    "consumed": {
      "items": {
        "$ref": "#/components/schemas/Quantity"
      },
      "maxItems": 1000,
      "title": "Consumed",
      "type": "array"
    },
    "createdAt": {
      "maxLength": 500,
      "title": "Createdat",
      "type": "string"
    },
    "edited": {
      "title": "Edited",
      "type": "boolean"
    },
    "expiresOn": {
      "anyOf": [
        {
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Expireson"
    },
    "foodId": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Foodid",
      "type": "string"
    },
    "form": {
      "maxLength": 500,
      "title": "Form",
      "type": "string"
    },
    "id": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Id",
      "type": "string"
    },
    "location": {
      "enum": [
        "冷蔵",
        "冷凍",
        "常温"
      ],
      "title": "Location",
      "type": "string"
    },
    "originalFoodId": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Originalfoodid",
      "type": "string"
    },
    "originalQuantity": {
      "$ref": "#/components/schemas/Quantity"
    },
    "priority": {
      "title": "Priority",
      "type": "boolean"
    },
    "quantity": {
      "$ref": "#/components/schemas/Quantity"
    },
    "sourceImportId": {
      "anyOf": [
        {
          "maxLength": 128,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Sourceimportid"
    },
    "status": {
      "enum": [
        "active",
        "deleted",
        "undone"
      ],
      "title": "Status",
      "type": "string"
    },
    "updatedAt": {
      "maxLength": 500,
      "title": "Updatedat",
      "type": "string"
    }
  },
  "required": [
    "id",
    "foodId",
    "originalFoodId",
    "quantity",
    "originalQuantity",
    "form",
    "location",
    "priority",
    "expiresOn",
    "createdAt",
    "updatedAt",
    "sourceImportId",
    "status",
    "consumed",
    "edited"
  ],
  "title": "StockLot",
  "type": "object"
}
```

## TaskDependencyRow

献立展開後依存のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| after_task_id | string (uuid) | 必須 | 追加制約なし | 後続タスク |
| before_task_id | string (uuid) | 必須 | 追加制約なし | 先行タスク |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| max_lag_s | anyOf(integer, null) | 必須 | 追加制約なし | 最大間隔 |
| min_lag_s | integer | 必須 | minimum=0.0 | 最小間隔 |
| reason | string | 必須 | minLength=1; maxLength=20000 | 元DAG/洗浄/設備切替等 |

```json
{
  "additionalProperties": false,
  "description": "献立展開後依存のDB応答。",
  "properties": {
    "after_task_id": {
      "description": "後続タスク",
      "format": "uuid",
      "title": "After Task Id",
      "type": "string"
    },
    "before_task_id": {
      "description": "先行タスク",
      "format": "uuid",
      "title": "Before Task Id",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "max_lag_s": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "description": "最大間隔",
      "title": "Max Lag S"
    },
    "min_lag_s": {
      "description": "最小間隔",
      "minimum": 0.0,
      "title": "Min Lag S",
      "type": "integer"
    },
    "reason": {
      "description": "元DAG/洗浄/設備切替等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Reason",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "before_task_id",
    "after_task_id",
    "min_lag_s",
    "max_lag_s",
    "reason",
    "etag"
  ],
  "title": "TaskDependencyRow",
  "type": "object"
}
```

## TaskDependencyWrite

献立展開後依存の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| after_task_id | string (uuid) | 必須 | 追加制約なし | 後続タスク |
| before_task_id | string (uuid) | 必須 | 追加制約なし | 先行タスク |
| max_lag_s | anyOf(integer, null) | 任意 | 追加制約なし | 最大間隔 |
| min_lag_s | integer | 必須 | minimum=0.0 | 最小間隔 |
| reason | string | 必須 | minLength=1; maxLength=20000 | 元DAG/洗浄/設備切替等 |

```json
{
  "additionalProperties": false,
  "description": "献立展開後依存の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "after_task_id": {
      "description": "後続タスク",
      "format": "uuid",
      "title": "After Task Id",
      "type": "string"
    },
    "before_task_id": {
      "description": "先行タスク",
      "format": "uuid",
      "title": "Before Task Id",
      "type": "string"
    },
    "max_lag_s": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "description": "最大間隔",
      "title": "Max Lag S"
    },
    "min_lag_s": {
      "description": "最小間隔",
      "minimum": 0.0,
      "title": "Min Lag S",
      "type": "integer"
    },
    "reason": {
      "description": "元DAG/洗浄/設備切替等",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Reason",
      "type": "string"
    }
  },
  "required": [
    "before_task_id",
    "after_task_id",
    "min_lag_s",
    "reason"
  ],
  "title": "TaskDependencyWrite",
  "type": "object"
}
```

## UnitRow

単位のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | 単位コード |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| dimension | string | 必須 | enum=["mass", "volume", "count", "time", "temperature", "length", "power"] | 物理次元 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| factor | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 同一次元の基準単位への倍率 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| name | string | 必須 | minLength=1; maxLength=20000 | 表示名 |
| offset | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 温度等のオフセット |
| status | string | 必須 | enum=["active", "retired"] | 利用状態 |

```json
{
  "additionalProperties": false,
  "description": "単位のDB応答。",
  "properties": {
    "code": {
      "description": "単位コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "dimension": {
      "description": "物理次元",
      "enum": [
        "mass",
        "volume",
        "count",
        "time",
        "temperature",
        "length",
        "power"
      ],
      "title": "Dimension",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "factor": {
      "description": "同一次元の基準単位への倍率",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Factor",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "name": {
      "description": "表示名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "offset": {
      "description": "温度等のオフセット",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Offset",
      "type": "string"
    },
    "status": {
      "description": "利用状態",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "code",
    "name",
    "dimension",
    "factor",
    "offset",
    "status",
    "etag"
  ],
  "title": "UnitRow",
  "type": "object"
}
```

## UnitWrite

単位の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| code | string | 必須 | minLength=1; maxLength=20000 | 単位コード |
| dimension | string | 必須 | enum=["mass", "volume", "count", "time", "temperature", "length", "power"] | 物理次元 |
| factor | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 同一次元の基準単位への倍率 |
| name | string | 必須 | minLength=1; maxLength=20000 | 表示名 |
| offset | anyOf(number, string) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 温度等のオフセット |
| status | string | 必須 | enum=["active", "retired"] | 利用状態 |

```json
{
  "additionalProperties": false,
  "description": "単位の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "code": {
      "description": "単位コード",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Code",
      "type": "string"
    },
    "dimension": {
      "description": "物理次元",
      "enum": [
        "mass",
        "volume",
        "count",
        "time",
        "temperature",
        "length",
        "power"
      ],
      "title": "Dimension",
      "type": "string"
    },
    "factor": {
      "anyOf": [
        {
          "exclusiveMinimum": 0.0,
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "同一次元の基準単位への倍率",
      "title": "Factor"
    },
    "name": {
      "description": "表示名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Name",
      "type": "string"
    },
    "offset": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "温度等のオフセット",
      "title": "Offset"
    },
    "status": {
      "description": "利用状態",
      "enum": [
        "active",
        "retired"
      ],
      "title": "Status",
      "type": "string"
    }
  },
  "required": [
    "code",
    "name",
    "dimension",
    "factor",
    "offset",
    "status"
  ],
  "title": "UnitWrite",
  "type": "object"
}
```

## UpdatePantryRequest



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9007199254740990.0 | Expectedversion |
| expiresOn | anyOf(string, null) | 任意 | anyOfの制約=string: pattern="^\\d{4}-\\d{2}-\\d{2}$" | Expireson |
| foodId | string | 必須 | minLength=1; maxLength=128 | Foodid |
| form | string | 任意 | default="標準"; maxLength=500 | Form |
| location | string | 任意 | enum=["冷蔵", "冷凍", "常温"]; default="冷蔵" | Location |
| priority | boolean | 任意 | default=false | Priority |
| quantity | Quantity | 必須 | 追加制約なし |  |
| restore | boolean | 任意 | default=false | Restore |

```json
{
  "additionalProperties": false,
  "properties": {
    "expectedVersion": {
      "maximum": 9007199254740990.0,
      "minimum": 0.0,
      "title": "Expectedversion",
      "type": "integer"
    },
    "expiresOn": {
      "anyOf": [
        {
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Expireson"
    },
    "foodId": {
      "maxLength": 128,
      "minLength": 1,
      "title": "Foodid",
      "type": "string"
    },
    "form": {
      "default": "標準",
      "maxLength": 500,
      "title": "Form",
      "type": "string"
    },
    "location": {
      "default": "冷蔵",
      "enum": [
        "冷蔵",
        "冷凍",
        "常温"
      ],
      "title": "Location",
      "type": "string"
    },
    "priority": {
      "default": false,
      "title": "Priority",
      "type": "boolean"
    },
    "quantity": {
      "$ref": "#/components/schemas/Quantity"
    },
    "restore": {
      "default": false,
      "title": "Restore",
      "type": "boolean"
    }
  },
  "required": [
    "foodId",
    "quantity",
    "expectedVersion"
  ],
  "title": "UpdatePantryRequest",
  "type": "object"
}
```

## UserExclusionRow

避けたい食材・物質のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| allergen_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | アレルゲン |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| food_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 食材 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| strict | boolean | 必須 | 追加制約なし | 不明も除外するか |
| user_id | string (uuid) | 必須 | 追加制約なし | 利用者 |

```json
{
  "additionalProperties": false,
  "description": "避けたい食材・物質のDB応答。",
  "properties": {
    "allergen_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "アレルゲン",
      "title": "Allergen Id"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "food_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "食材",
      "title": "Food Id"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "strict": {
      "description": "不明も除外するか",
      "title": "Strict",
      "type": "boolean"
    },
    "user_id": {
      "description": "利用者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "user_id",
    "food_id",
    "allergen_id",
    "strict",
    "etag"
  ],
  "title": "UserExclusionRow",
  "type": "object"
}
```

## UserExclusionWrite

避けたい食材・物質の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| allergen_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | アレルゲン |
| food_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 食材 |
| strict | boolean | 必須 | 追加制約なし | 不明も除外するか |
| user_id | string (uuid) | 必須 | 追加制約なし | 利用者 |

```json
{
  "additionalProperties": false,
  "description": "避けたい食材・物質の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "allergen_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "アレルゲン",
      "title": "Allergen Id"
    },
    "food_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "食材",
      "title": "Food Id"
    },
    "strict": {
      "description": "不明も除外するか",
      "title": "Strict",
      "type": "boolean"
    },
    "user_id": {
      "description": "利用者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "user_id",
    "strict"
  ],
  "title": "UserExclusionWrite",
  "type": "object"
}
```

## UserFoodRow

利用者が追加した独自食材の所有のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| food_id | string (uuid) | 必須 | 追加制約なし | 独自食材 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "利用者が追加した独自食材の所有のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "food_id": {
      "description": "独自食材",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "user_id",
    "food_id",
    "etag"
  ],
  "title": "UserFoodRow",
  "type": "object"
}
```

## UserFoodWrite

利用者が追加した独自食材の所有の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| food_id | string (uuid) | 必須 | 追加制約なし | 独自食材 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "利用者が追加した独自食材の所有の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "food_id": {
      "description": "独自食材",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "user_id",
    "food_id"
  ],
  "title": "UserFoodWrite",
  "type": "object"
}
```

## UserPantryFoodRow

利用者が常備すると設定した食材のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| food_id | string (uuid) | 必須 | 追加制約なし | 常備食材 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "利用者が常備すると設定した食材のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "food_id": {
      "description": "常備食材",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "user_id",
    "food_id",
    "etag"
  ],
  "title": "UserPantryFoodRow",
  "type": "object"
}
```

## UserPantryFoodWrite

利用者が常備すると設定した食材の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| food_id | string (uuid) | 必須 | 追加制約なし | 常備食材 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "利用者が常備すると設定した食材の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "food_id": {
      "description": "常備食材",
      "format": "uuid",
      "title": "Food Id",
      "type": "string"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "user_id",
    "food_id"
  ],
  "title": "UserPantryFoodWrite",
  "type": "object"
}
```

## UserPreferenceRow

ユーザーの嗜好のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| option_id | string (uuid) | 必須 | 追加制約なし | 味・料理等 |
| user_id | string (uuid) | 必須 | 追加制約なし | 利用者 |
| weight | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 好みの重み |

```json
{
  "additionalProperties": false,
  "description": "ユーザーの嗜好のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "option_id": {
      "description": "味・料理等",
      "format": "uuid",
      "title": "Option Id",
      "type": "string"
    },
    "user_id": {
      "description": "利用者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    },
    "weight": {
      "description": "好みの重み",
      "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
      "title": "Weight",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "user_id",
    "option_id",
    "weight",
    "etag"
  ],
  "title": "UserPreferenceRow",
  "type": "object"
}
```

## UserPreferenceWrite

ユーザーの嗜好の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| option_id | string (uuid) | 必須 | 追加制約なし | 味・料理等 |
| user_id | string (uuid) | 必須 | 追加制約なし | 利用者 |
| weight | anyOf(number, string) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 好みの重み |

```json
{
  "additionalProperties": false,
  "description": "ユーザーの嗜好の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "option_id": {
      "description": "味・料理等",
      "format": "uuid",
      "title": "Option Id",
      "type": "string"
    },
    "user_id": {
      "description": "利用者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    },
    "weight": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        }
      ],
      "description": "好みの重み",
      "title": "Weight"
    }
  },
  "required": [
    "user_id",
    "option_id",
    "weight"
  ],
  "title": "UserPreferenceWrite",
  "type": "object"
}
```

## UserProfile



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| display_name | string | 必須 | 追加制約なし | Display Name |
| id | string | 必須 | 追加制約なし | Id |
| role | string | 必須 | 追加制約なし | Role |

```json
{
  "properties": {
    "display_name": {
      "title": "Display Name",
      "type": "string"
    },
    "id": {
      "title": "Id",
      "type": "string"
    },
    "role": {
      "title": "Role",
      "type": "string"
    }
  },
  "required": [
    "id",
    "display_name",
    "role"
  ],
  "title": "UserProfile",
  "type": "object"
}
```

## UserRecipeEventRow

提案・調理履歴のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| kind | string | 必須 | enum=["shown", "cooked", "liked", "disliked"] | 提示/調理/評価 |
| occurred_at | string (date-time) | 必須 | 追加制約なし | 発生時刻 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 提案版 |
| request_key | string | 必須 | minLength=1; maxLength=20000 | リクエスト識別子 |
| user_id | string (uuid) | 必須 | 追加制約なし | 利用者 |

```json
{
  "additionalProperties": false,
  "description": "提案・調理履歴のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "kind": {
      "description": "提示/調理/評価",
      "enum": [
        "shown",
        "cooked",
        "liked",
        "disliked"
      ],
      "title": "Kind",
      "type": "string"
    },
    "occurred_at": {
      "description": "発生時刻",
      "format": "date-time",
      "title": "Occurred At",
      "type": "string"
    },
    "recipe_version_id": {
      "description": "提案版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "request_key": {
      "description": "リクエスト識別子",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Request Key",
      "type": "string"
    },
    "user_id": {
      "description": "利用者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "user_id",
    "recipe_version_id",
    "kind",
    "occurred_at",
    "request_key",
    "etag"
  ],
  "title": "UserRecipeEventRow",
  "type": "object"
}
```

## UserRecipeEventWrite

提案・調理履歴の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| kind | string | 必須 | enum=["shown", "cooked", "liked", "disliked"] | 提示/調理/評価 |
| occurred_at | string (date-time) | 必須 | 追加制約なし | 発生時刻 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 提案版 |
| request_key | string | 必須 | minLength=1; maxLength=20000 | リクエスト識別子 |
| user_id | string (uuid) | 必須 | 追加制約なし | 利用者 |

```json
{
  "additionalProperties": false,
  "description": "提案・調理履歴の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "kind": {
      "description": "提示/調理/評価",
      "enum": [
        "shown",
        "cooked",
        "liked",
        "disliked"
      ],
      "title": "Kind",
      "type": "string"
    },
    "occurred_at": {
      "description": "発生時刻",
      "format": "date-time",
      "title": "Occurred At",
      "type": "string"
    },
    "recipe_version_id": {
      "description": "提案版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "request_key": {
      "description": "リクエスト識別子",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Request Key",
      "type": "string"
    },
    "user_id": {
      "description": "利用者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "user_id",
    "recipe_version_id",
    "kind",
    "occurred_at",
    "request_key"
  ],
  "title": "UserRecipeEventWrite",
  "type": "object"
}
```

## UserShoppingCheckRow

調理前の買い物確認のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 必要数量。不明はNULL |
| archived | boolean | 必須 | 追加制約なし | 保管済みか |
| checked_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 購入確認日時 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| food_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 対象食材 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| key | string | 必須 | minLength=1; maxLength=20000 | 買い物対象の安定キー |
| signature | string | 必須 | minLength=1; maxLength=20000 | 数量・商品条件の一致確認用署名 |
| unit_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 数量単位 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "調理前の買い物確認のDB応答。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "必要数量。不明はNULL",
      "title": "Amount"
    },
    "archived": {
      "description": "保管済みか",
      "title": "Archived",
      "type": "boolean"
    },
    "checked_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入確認日時",
      "title": "Checked At"
    },
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "food_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "対象食材",
      "title": "Food Id"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "key": {
      "description": "買い物対象の安定キー",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Key",
      "type": "string"
    },
    "signature": {
      "description": "数量・商品条件の一致確認用署名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Signature",
      "type": "string"
    },
    "unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "数量単位",
      "title": "Unit Id"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "user_id",
    "key",
    "signature",
    "food_id",
    "amount",
    "unit_id",
    "checked_at",
    "archived",
    "etag"
  ],
  "title": "UserShoppingCheckRow",
  "type": "object"
}
```

## UserShoppingCheckWrite

調理前の買い物確認の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 必要数量。不明はNULL |
| archived | boolean | 必須 | 追加制約なし | 保管済みか |
| checked_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 購入確認日時 |
| food_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 対象食材 |
| key | string | 必須 | minLength=1; maxLength=20000 | 買い物対象の安定キー |
| signature | string | 必須 | minLength=1; maxLength=20000 | 数量・商品条件の一致確認用署名 |
| unit_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 数量単位 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "調理前の買い物確認の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "pattern": "^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}|(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "必要数量。不明はNULL",
      "title": "Amount"
    },
    "archived": {
      "description": "保管済みか",
      "title": "Archived",
      "type": "boolean"
    },
    "checked_at": {
      "anyOf": [
        {
          "format": "date-time",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "購入確認日時",
      "title": "Checked At"
    },
    "food_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "対象食材",
      "title": "Food Id"
    },
    "key": {
      "description": "買い物対象の安定キー",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Key",
      "type": "string"
    },
    "signature": {
      "description": "数量・商品条件の一致確認用署名",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Signature",
      "type": "string"
    },
    "unit_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "description": "数量単位",
      "title": "Unit Id"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "user_id",
    "key",
    "signature",
    "archived"
  ],
  "title": "UserShoppingCheckWrite",
  "type": "object"
}
```

## ValidationError



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| ctx | object | 任意 | 追加制約なし | Context |
| input | 任意のJSON | 任意 | 追加制約なし | Input |
| loc | array&lt;anyOf(string, integer)&gt; | 必須 | 追加制約なし | Location |
| msg | string | 必須 | 追加制約なし | Message |
| type | string | 必須 | 追加制約なし | Error Type |

```json
{
  "properties": {
    "ctx": {
      "title": "Context",
      "type": "object"
    },
    "input": {
      "title": "Input"
    },
    "loc": {
      "items": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "integer"
          }
        ]
      },
      "title": "Location",
      "type": "array"
    },
    "msg": {
      "title": "Message",
      "type": "string"
    },
    "type": {
      "title": "Error Type",
      "type": "string"
    }
  },
  "required": [
    "loc",
    "msg",
    "type"
  ],
  "title": "ValidationError",
  "type": "object"
}
```

## ValidationEvidence



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| actual | anyOf(string, boolean, number, null) | 必須 | 追加制約なし | Actual |
| expected | anyOf(string, boolean, number, null) | 必須 | 追加制約なし | Expected |
| path | string | 必須 | minLength=1; maxLength=500 | Path |
| schema_version | integer | 任意 | const=1; default=1 | Schema Version |
| source_ids | array&lt;string (uuid)&gt; | 必須 | maxItems=100 | Source Ids |

```json
{
  "additionalProperties": false,
  "properties": {
    "actual": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "boolean"
        },
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Actual"
    },
    "expected": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "boolean"
        },
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Expected"
    },
    "path": {
      "maxLength": 500,
      "minLength": 1,
      "title": "Path",
      "type": "string"
    },
    "schema_version": {
      "const": 1,
      "default": 1,
      "title": "Schema Version",
      "type": "integer"
    },
    "source_ids": {
      "items": {
        "format": "uuid",
        "type": "string"
      },
      "maxItems": 100,
      "title": "Source Ids",
      "type": "array"
    }
  },
  "required": [
    "path",
    "expected",
    "actual",
    "source_ids"
  ],
  "title": "ValidationEvidence",
  "type": "object"
}
```

## ValidationResultRow

公開前評価結果のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| evaluated_at | string (date-time) | 必須 | 追加制約なし | 検査日時 |
| evidence | ValidationEvidence | 必須 | 追加制約なし | 検査箇所・値・根拠 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 対象版 |
| rule_id | string (uuid) | 必須 | 追加制約なし | 適用規則版 |
| state | string | 必須 | enum=["pending", "passed", "failed", "needs_review"] | 結果 |
| validator_version | string | 必須 | minLength=1; maxLength=20000 | 検証器版 |

```json
{
  "additionalProperties": false,
  "description": "公開前評価結果のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "evaluated_at": {
      "description": "検査日時",
      "format": "date-time",
      "title": "Evaluated At",
      "type": "string"
    },
    "evidence": {
      "$ref": "#/components/schemas/ValidationEvidence",
      "description": "検査箇所・値・根拠"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "recipe_version_id": {
      "description": "対象版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "rule_id": {
      "description": "適用規則版",
      "format": "uuid",
      "title": "Rule Id",
      "type": "string"
    },
    "state": {
      "description": "結果",
      "enum": [
        "pending",
        "passed",
        "failed",
        "needs_review"
      ],
      "title": "State",
      "type": "string"
    },
    "validator_version": {
      "description": "検証器版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Validator Version",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "recipe_version_id",
    "rule_id",
    "state",
    "evidence",
    "validator_version",
    "evaluated_at",
    "etag"
  ],
  "title": "ValidationResultRow",
  "type": "object"
}
```

## ValidationResultWrite

公開前評価結果の編集可能列。未指定NULL列はNULLにする。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| evaluated_at | string (date-time) | 必須 | 追加制約なし | 検査日時 |
| evidence | ValidationEvidence | 必須 | 追加制約なし | 検査箇所・値・根拠 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 対象版 |
| rule_id | string (uuid) | 必須 | 追加制約なし | 適用規則版 |
| state | string | 必須 | enum=["pending", "passed", "failed", "needs_review"] | 結果 |
| validator_version | string | 必須 | minLength=1; maxLength=20000 | 検証器版 |

```json
{
  "additionalProperties": false,
  "description": "公開前評価結果の編集可能列。未指定NULL列はNULLにする。",
  "properties": {
    "evaluated_at": {
      "description": "検査日時",
      "format": "date-time",
      "title": "Evaluated At",
      "type": "string"
    },
    "evidence": {
      "$ref": "#/components/schemas/ValidationEvidence",
      "description": "検査箇所・値・根拠"
    },
    "recipe_version_id": {
      "description": "対象版",
      "format": "uuid",
      "title": "Recipe Version Id",
      "type": "string"
    },
    "rule_id": {
      "description": "適用規則版",
      "format": "uuid",
      "title": "Rule Id",
      "type": "string"
    },
    "state": {
      "description": "結果",
      "enum": [
        "pending",
        "passed",
        "failed",
        "needs_review"
      ],
      "title": "State",
      "type": "string"
    },
    "validator_version": {
      "description": "検証器版",
      "maxLength": 20000,
      "minLength": 1,
      "title": "Validator Version",
      "type": "string"
    }
  },
  "required": [
    "recipe_version_id",
    "rule_id",
    "state",
    "evidence",
    "validator_version",
    "evaluated_at"
  ],
  "title": "ValidationResultWrite",
  "type": "object"
}
```

## WorkspaceRevisionRow

利用者ワークスペースの原子的更新版のDB応答。

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| revision | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 全体のCAS版 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

```json
{
  "additionalProperties": false,
  "description": "利用者ワークスペースの原子的更新版のDB応答。",
  "properties": {
    "created_at": {
      "description": "作成日時(UTC)",
      "format": "date-time",
      "title": "Created At",
      "type": "string"
    },
    "etag": {
      "description": "更新・削除時のIf-Matchに使う行版",
      "pattern": "^[0-9]+$",
      "title": "Etag",
      "type": "string"
    },
    "id": {
      "description": "不変の行識別子",
      "format": "uuid",
      "title": "Id",
      "type": "string"
    },
    "revision": {
      "description": "全体のCAS版",
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Revision",
      "type": "string"
    },
    "user_id": {
      "description": "所有者",
      "format": "uuid",
      "title": "User Id",
      "type": "string"
    }
  },
  "required": [
    "id",
    "created_at",
    "user_id",
    "revision",
    "etag"
  ],
  "title": "WorkspaceRevisionRow",
  "type": "object"
}
```

## app__apis__generation__advance_shard__schemas__Request



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| expected_fence | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | Expected Fence |
| next_ordinal | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | Next Ordinal |
| state | string | 必須 | enum=["running", "done"] | State |

```json
{
  "additionalProperties": false,
  "properties": {
    "expected_fence": {
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Expected Fence",
      "type": "string"
    },
    "next_ordinal": {
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Next Ordinal",
      "type": "string"
    },
    "state": {
      "enum": [
        "running",
        "done"
      ],
      "title": "State",
      "type": "string"
    }
  },
  "required": [
    "expected_fence",
    "next_ordinal",
    "state"
  ],
  "title": "Request",
  "type": "object"
}
```

## app__apis__generation__claim_shard__schemas__Request



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| lease_seconds | integer | 任意 | default=120; minimum=30.0; maximum=3600.0 | Lease Seconds |
| template_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | Template Id |

```json
{
  "additionalProperties": false,
  "properties": {
    "lease_seconds": {
      "default": 120,
      "maximum": 3600.0,
      "minimum": 30.0,
      "title": "Lease Seconds",
      "type": "integer"
    },
    "template_id": {
      "anyOf": [
        {
          "format": "uuid",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Template Id"
    }
  },
  "title": "Request",
  "type": "object"
}
```

## app__apis__generation__renew_shard__schemas__Request



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| expected_fence | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | Expected Fence |
| lease_seconds | integer | 任意 | default=120; minimum=30.0; maximum=3600.0 | Lease Seconds |

```json
{
  "additionalProperties": false,
  "properties": {
    "expected_fence": {
      "pattern": "^-?(0|[1-9][0-9]{0,18})$",
      "title": "Expected Fence",
      "type": "string"
    },
    "lease_seconds": {
      "default": 120,
      "maximum": 3600.0,
      "minimum": 30.0,
      "title": "Lease Seconds",
      "type": "integer"
    }
  },
  "required": [
    "expected_fence"
  ],
  "title": "Request",
  "type": "object"
}
```
