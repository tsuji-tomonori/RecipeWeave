# 共有モデル・enum・制約

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## AppSnapshot



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| cooking | anyOf(CookingSession, null) | 必須 | 追加制約なし |  |
| customFoods | array&lt;Food&gt; | 必須 | maxItems=1000 | Customfoods |
| drafts | object | 必須 | additionalProperties={"$ref": "#/components/schemas/RecipeDraft"} | Drafts |
| imports | array&lt;ReceiptImport&gt; | 必須 | maxItems=1000 | Imports |
| lots | array&lt;StockLot&gt; | 必須 | maxItems=5000 | Lots |
| meal | array&lt;MealItem&gt; | 必須 | maxItems=50 | Meal |
| saved | array&lt;string&gt; | 必須 | maxItems=10000 | Saved |
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

## ConsumptionResult



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| applied | boolean | 必須 | 追加制約なし | Applied |
| foodId | string | 必須 | minLength=1; maxLength=128 | Foodid |
| form | string | 必須 | maxLength=500 | Form |
| lotIds | array&lt;string&gt; | 必須 | maxItems=1000 | Lotids |
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

## CookingSession



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| completedStepIds | array&lt;string&gt; | 必須 | maxItems=500 | Completedstepids |
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

## Food



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| aliases | array&lt;string&gt; | 必須 | maxItems=100 | Aliases |
| category | string | 必須 | maxLength=500 | Category |
| componentFoodIds | array&lt;string&gt; | 必須 | maxItems=100 | Componentfoodids |
| componentsKnown | boolean | 必須 | 追加制約なし | Componentsknown |
| defaultUnit | string | 必須 | enum=["g", "ml", "個", "パック", "袋", "缶", "本", "枚", "点"] | Defaultunit |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| imageIndex | anyOf(integer, null) | 必須 | 追加制約なし | Imageindex |
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

## MealItem



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| adjusted | boolean | 必須 | 追加制約なし | Adjusted |
| amounts | object | 必須 | additionalProperties={"$ref": "#/components/schemas/Quantity"} | Amounts |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| recipeId | string | 必須 | minLength=1; maxLength=128 | Recipeid |
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

## PlannedStep



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| endMinute | number | 必須 | minimum=0.0; maximum=1000000.0 | Endminute |
| equipment | array&lt;string&gt; | 必須 | maxItems=50 | Equipment |
| guide | anyOf(string, null) | 必須 | 追加制約なし | Guide |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| instruction | string | 必須 | maxLength=5000 | Instruction |
| key | string | 必須 | maxLength=500 | Key |
| mealItemId | string | 必須 | minLength=1; maxLength=128 | Mealitemid |
| minutes | number | 必須 | minimum=0.0; maximum=1000000.0 | Minutes |
| mode | string | 必須 | enum=["active", "passive"] | Mode |
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
        "passive"
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

## PutStateRequest



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9.223372036854776e+18 | Expectedversion |
| snapshot | AppSnapshot | 必須 | 追加制約なし |  |

```json
{
  "additionalProperties": false,
  "properties": {
    "expectedVersion": {
      "maximum": 9.223372036854776e+18,
      "minimum": 0.0,
      "title": "Expectedversion",
      "type": "integer"
    },
    "snapshot": {
      "$ref": "#/components/schemas/AppSnapshot"
    }
  },
  "required": [
    "expectedVersion",
    "snapshot"
  ],
  "title": "PutStateRequest",
  "type": "object"
}
```

## Quantity



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| unit | string | 必須 | enum=["g", "ml", "個", "パック", "袋", "缶", "本", "枚", "点"] | Unit |
| value | anyOf(number, null) | 必須 | 追加制約なし | Value |

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

## ReceiptImport



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| createdAt | string | 必須 | maxLength=500 | Createdat |
| createdLotIds | array&lt;string&gt; | 必須 | maxItems=200 | Createdlotids |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| imageHash | string | 必須 | pattern="^[a-f0-9]{64}$" | Imagehash |
| purchaseSignature | string | 必須 | pattern="^[a-f0-9]{64}$" | Purchasesignature |
| state | string | 必須 | enum=["registered", "undone"] | State |
| undoneAt | anyOf(string, null) | 必須 | 追加制約なし | Undoneat |

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

## Recipe



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| arrangementIds | array&lt;string&gt; | 必須 | maxItems=100 | Arrangementids |
| description | string | 必須 | maxLength=5000 | Description |
| equipment | array&lt;string&gt; | 必須 | maxItems=50 | Equipment |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| ingredients | array&lt;RecipeIngredient&gt; | 必須 | maxItems=100 | Ingredients |
| minutes | number | 必須 | minimum=0.0; maximum=1000000.0 | Minutes |
| name | string | 必須 | maxLength=500 | Name |
| sample | boolean | 必須 | const=true | Sample |
| servings | number | 必須 | maximum=1000.0; exclusiveMinimum=0.0 | Servings |
| steps | array&lt;RecipeStep&gt; | 必須 | maxItems=100 | Steps |
| tags | array&lt;string&gt; | 必須 | maxItems=100 | Tags |

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
    "sample": {
      "const": true,
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

## RecipeIngredient



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| foodId | string | 必須 | minLength=1; maxLength=128 | Foodid |
| form | string | 必須 | maxLength=500 | Form |
| note | string | 必須 | maxLength=500 | Note |
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
    "note": {
      "maxLength": 500,
      "title": "Note",
      "type": "string"
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

## RecipeStep



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| equipment | array&lt;string&gt; | 必須 | maxItems=50 | Equipment |
| guide | anyOf(string, null) | 必須 | 追加制約なし | Guide |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| instruction | string | 必須 | maxLength=5000 | Instruction |
| minutes | number | 必須 | minimum=0.0; maximum=1000000.0 | Minutes |
| mode | string | 必須 | enum=["active", "passive"] | Mode |
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
        "passive"
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

## RecipesResponse



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| items | array&lt;Recipe&gt; | 必須 | 追加制約なし | Items |
| sample | boolean | 任意 | const=true; default=true | Sample |
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
    "sample": {
      "const": true,
      "default": true,
      "title": "Sample",
      "type": "boolean"
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
  "title": "RecipesResponse",
  "type": "object"
}
```

## SearchFilters



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| equipment | array&lt;string&gt; | 必須 | maxItems=50 | Equipment |
| match | string | 必須 | enum=["all", "any"] | Match |
| maxMinutes | anyOf(number, null) | 必須 | 追加制約なし | Maxminutes |
| noShopping | boolean | 必須 | 追加制約なし | Noshopping |
| selectedFoodIds | array&lt;string&gt; | 必須 | maxItems=100 | Selectedfoodids |

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

## Settings



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| equipment | array&lt;string&gt; | 必須 | maxItems=50 | Equipment |
| excludedFoodIds | array&lt;string&gt; | 必須 | maxItems=1000 | Excludedfoodids |
| pantryFoodIds | array&lt;string&gt; | 必須 | maxItems=1000 | Pantryfoodids |

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

## StateEnvelope



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| snapshot | anyOf(AppSnapshot, null) | 必須 | 追加制約なし |  |
| version | integer | 必須 | minimum=0.0 | Version |

```json
{
  "additionalProperties": false,
  "properties": {
    "snapshot": {
      "anyOf": [
        {
          "$ref": "#/components/schemas/AppSnapshot"
        },
        {
          "type": "null"
        }
      ]
    },
    "version": {
      "minimum": 0.0,
      "title": "Version",
      "type": "integer"
    }
  },
  "required": [
    "version",
    "snapshot"
  ],
  "title": "StateEnvelope",
  "type": "object"
}
```

## StockLot



| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| consumed | array&lt;Quantity&gt; | 必須 | maxItems=1000 | Consumed |
| createdAt | string | 必須 | maxLength=500 | Createdat |
| edited | boolean | 必須 | 追加制約なし | Edited |
| expiresOn | anyOf(string, null) | 必須 | 追加制約なし | Expireson |
| foodId | string | 必須 | minLength=1; maxLength=128 | Foodid |
| form | string | 必須 | maxLength=500 | Form |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| location | string | 必須 | enum=["冷蔵", "冷凍", "常温"] | Location |
| originalFoodId | string | 必須 | minLength=1; maxLength=128 | Originalfoodid |
| originalQuantity | Quantity | 必須 | 追加制約なし |  |
| priority | boolean | 必須 | 追加制約なし | Priority |
| quantity | Quantity | 必須 | 追加制約なし |  |
| sourceImportId | anyOf(string, null) | 必須 | 追加制約なし | Sourceimportid |
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
