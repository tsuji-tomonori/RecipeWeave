# シーケンス: add_menu_item

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

対象はrouter.py・functions.pyの各関数。呼出元・関数・呼出先の3者で、関数内の分岐と反復を示す。関数間を推測で展開せず、呼出先の名前をそのまま記載する。内包表記・短絡評価は条件付き式のまま残す。エンティティAPIは共有EntityServiceも含める。FastAPIの依存解決、middleware、DBドライバー内部はこの図の対象外。try/except/else/finallyとcontext境界を保持する。continue/breakは注記位置で該当経路を終了し、次の反復/ループ外へ進む。

### router.py: `handle`

定義元: `backend/src/app/apis/workspace/add_menu_item/router.py:22`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as handle
    participant Callee as 呼出先
    Caller->>Function: identity: IdentityDependency, database: DatabaseDependency, request: MenuItemRequest
    Function->>Callee: WorkspaceService(database, identity)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: execute(WorkspaceService(database, identity), request)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: execute(WorkspaceService(database, identity), request)
    end
```

### functions.py: `execute`

定義元: `backend/src/app/apis/workspace/add_menu_item/functions.py:6`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as execute
    participant Callee as 呼出先
    Caller->>Function: service: WorkspaceService, request: MenuItemRequest
    Function->>Callee: service.add_menu_item(request)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: service.add_menu_item(request)
    end
```

### workspace_service.py: `identifier`

定義元: `backend/src/app/core/workspace_service.py:32`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as identifier
    participant Callee as 呼出先
    Caller->>Function: value: str
    rect rgb(244, 247, 246)
    Note over Function: try: 例外発生時は一致するexceptへ移る
        Function->>Callee: UUID(value)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: return
            Function-->>Caller: UUID(value)
        end
    end
    opt 例外: ValueError
        Function->>Callee: HTTPException(422, #39;識別子の形式が不正です#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(422, #39;識別子の形式が不正です#39;)
        end
    end
```

### workspace_service.py: `quantity`

定義元: `backend/src/app/core/workspace_service.py:40`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as quantity
    participant Callee as 呼出先
    Caller->>Function: value: Any, unit: str
    Note over Function: 条件付き式を評価: {#39;value#39;: None if value is None else float(value), #39;unit#39;: unit}
    break この経路の関数終了: return
        Function-->>Caller: {#39;value#39;: None if value is None else float(value), #39;unit#39;: unit}
    end
```

### workspace_service.py: `iso`

定義元: `backend/src/app/core/workspace_service.py:45`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as iso
    participant Callee as 呼出先
    Caller->>Function: value: Any
    Note over Function: 条件付き式を評価: value.isoformat() if isinstance(value, date | datetime) else None
    break この経路の関数終了: return
        Function-->>Caller: value.isoformat() if isinstance(value, date | datetime) else None
    end
```

### workspace_service.py: `queries`

定義元: `backend/src/app/core/workspace_service.py:59`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as queries
    participant Callee as 呼出先
    Caller->>Function: self, name: str
    Function->>Callee: OperationQueries(self.connection, #39;workspace/#39; + name)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: OperationQueries(self.connection, #39;workspace/#39; + name)
    end
```

### workspace_service.py: `begin`

定義元: `backend/src/app/core/workspace_service.py:62`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as begin
    participant Callee as 呼出先
    Caller->>Function: self, name: str, request: RevisionRequest
    Function->>Callee: self.queries(name)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: queries = self.queries(name)
    Function->>Callee: queries.run(#39;q900_lock_revision#39;, user_id=self.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: rows = queries.run(#39;q900_lock_revision#39;, user_id=self.user_id)
    Note over Function: 条件付き式を評価: not rows or int(rows[0][#39;revision#39;]) != request.expected_version
    alt not rows or int(rows[0][#39;revision#39;]) != request.expected_version
        Function->>Callee: HTTPException(409, #39;他の画面で更新されています。最新の内容を読み込んでください#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(409, #39;他の画面で更新されています。最新の内容を読み込んでください#39;)
        end
    end
    break この経路の関数終了: return
        Function-->>Caller: queries
    end
```

### workspace_service.py: `finish`

定義元: `backend/src/app/core/workspace_service.py:69`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as finish
    participant Callee as 呼出先
    Caller->>Function: self, queries: OperationQueries
    Function->>Callee: queries.run(#39;q901_advance_revision#39;, user_id=self.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: uuid4()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: str(self.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: str(self.user_id).encode()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: hashlib.sha256(str(self.user_id).encode())
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: hashlib.sha256(str(self.user_id).encode()).hexdigest()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: queries.run(#39;q902_append_audit#39;, row_id=uuid4(), user_id=self.user_id, action=queries.operation, key_hash=hashlib.sha256(str(self.user_id).encode()).hexdigest())
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: self.get_workspace()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: self.get_workspace()
    end
```

### workspace_service.py: `get_workspace`

定義元: `backend/src/app/core/workspace_service.py:80`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as get_workspace
    participant Callee as 呼出先
    Caller->>Function: self
    Function->>Callee: self.queries(#39;get_workspace#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: q = self.queries(#39;get_workspace#39;)
    Function->>Callee: q.run(#39;q001_revision#39;, user_id=self.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: revision = q.run(#39;q001_revision#39;, user_id=self.user_id)
    Function->>Callee: q.run(#39;q003_consumption#39;, user_id=self.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: consumptions = q.run(#39;q003_consumption#39;, user_id=self.user_id)
    Note over Function: 条件付き式を評価: [{#39;id#39;: str(r[#39;id#39;]), #39;foodId#39;: str(r[#39;food_id#39;]), #39;originalFoodId#39;: str(r[#39;original_food_id#39;]), #39;quantity#39;: quantity(r[#39;amount#39;], r[#39;unit#39;]), #39;originalQuantity#39;: quantity(r[#39;original_amount#39;], r[#39;original_unit#39;]), #39;form#39;: r[#39;form#39;], #39;location#39;: DISPLAY_LOCATIONS[r[#39;location#39;]], #39;priority#39;: r[#39;priority#39;] == #39;use_first#39;, #39;expiresOn#39;: iso(r[#39;expires_on#39;]), #39;createdAt#39;: iso(r[#39;created_at#39;]), #39;updatedAt#39;: iso(r[#39;updated_at#39;]), #39;sourceImportId#39;: str(r[#39;source_import_id#39;]) if r[#39;source_import_id#39;] else None, #39;status#39;: r[#39;status#39;], #39;edited#39;: r[#39;edited#39;], #39;consumed#39;: [quantity(c[#39;amount#39;], c[#39;unit#39;]) for c in consumptions if c[#39;lot_id#39;] == r[#39;id#39;]]} for r in q.run(#39;q002_lots#39;, user_id=self.user_id)]
    Note over Function: lots = [{#39;id#39;: str(r[#39;id#39;]), #39;foodId#39;: str(r[#39;food_id#39;]), #39;originalFoodId#39;: str(r[#39;original_food_id#39;]), #39;quantity#39;: quantity(r[#39;amount#39;], r[#39;unit#39;]), #39;originalQuantity#39;: quantity(r[#39;original_amount#39;], r[#39;original_unit#39;]), #39;form#39;: r[#39;form#39;], #39;location#39;: DISPLAY_LOCATIONS[r[#39;location#39;]], #39;priority#39;: r[#39;priority#39;] == #39;use_first#39;, #39;expiresOn#39;: iso(r[#39;expires_on#39;]), #39;createdAt#39;: iso(r[#39;created_at#39;]), #39;updatedAt#39;: iso(r[#39;updated_at#39;]), #39;sourceImportId#39;: str(r[#39;source_import_id#39;]) if r[#39;source_import_id#39;] else None, #39;status#39;: r[#39;status#39;], #39;edited#39;: r[#39;edited#39;], #39;consumed#39;: [quantity(c[#39;amount#39;], c[#39;unit#39;]) for c in consumptions if c[#39;lot_id#39;] == r[#39;id#39;]]} for r in q.run(#39;q002_lots#39;, user_id=self.user_id)]
    Note over Function: 条件付き式を評価: [{#39;id#39;: str(r[#39;id#39;]), #39;imageHash#39;: r[#39;file_sha256#39;], #39;purchaseSignature#39;: r[#39;idempotency_key#39;].split(#39;:#39;)[0], #39;createdAt#39;: iso(r[#39;created_at#39;]), #39;state#39;: #39;registered#39; if r[#39;status#39;] == #39;committed#39; else #39;undone#39;, #39;createdLotIds#39;: [lot[#39;id#39;] for lot in lots if lot[#39;sourceImportId#39;] == str(r[#39;id#39;])], #39;undoneAt#39;: iso(r[#39;reverted_at#39;])} for r in q.run(#39;q004_receipts#39;, user_id=self.user_id)]
    Note over Function: imports = [{#39;id#39;: str(r[#39;id#39;]), #39;imageHash#39;: r[#39;file_sha256#39;], #39;purchaseSignature#39;: r[#39;idempotency_key#39;].split(#39;:#39;)[0], #39;createdAt#39;: iso(r[#39;created_at#39;]), #39;state#39;: #39;registered#39; if r[#39;status#39;] == #39;committed#39; else #39;undone#39;, #39;createdLotIds#39;: [lot[#39;id#39;] for lot in lots if lot[#39;sourceImportId#39;] == str(r[#39;id#39;])], #39;undoneAt#39;: iso(r[#39;reverted_at#39;])} for r in q.run(#39;q004_receipts#39;, user_id=self.user_id)]
    Function->>Callee: self.read_meal(q, self.menu_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: meal = self.read_meal(q, self.menu_id)
    Note over Function: settings: dict[str, list[str]] = {#39;excludedFoodIds#39;: [], #39;pantryFoodIds#39;: [], #39;equipment#39;: []}
    Note over Function: setting_keys = {#39;excluded#39;: #39;excludedFoodIds#39;, #39;pantry#39;: #39;pantryFoodIds#39;, #39;equipment#39;: #39;equipment#39;}
    Function->>Callee: q.run(#39;q008_settings#39;, user_id=self.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    loop r in q.run(#39;q008_settings#39;, user_id=self.user_id)
        Function->>Callee: settings[setting_keys[r[#39;kind#39;]]].append(r[#39;setting_value#39;])
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    end
    Note over Function: 条件付き式を評価: [{#39;id#39;: str(r[#39;id#39;]), #39;name#39;: r[#39;name#39;], #39;aliases#39;: [], #39;category#39;: #39;追加した食材#39;, #39;defaultUnit#39;: r[#39;unit#39;], #39;location#39;: #39;冷蔵#39;, #39;pantry#39;: False, #39;imageIndex#39;: None, #39;componentsKnown#39;: False, #39;componentFoodIds#39;: []} for r in q.run(#39;q009_custom_foods#39;, user_id=self.user_id)]
    Note over Function: customs: list[dict[str, Any]] = [{#39;id#39;: str(r[#39;id#39;]), #39;name#39;: r[#39;name#39;], #39;aliases#39;: [], #39;category#39;: #39;追加した食材#39;, #39;defaultUnit#39;: r[#39;unit#39;], #39;location#39;: #39;冷蔵#39;, #39;pantry#39;: False, #39;imageIndex#39;: None, #39;componentsKnown#39;: False, #39;componentFoodIds#39;: []} for r in q.run(#39;q009_custom_foods#39;, user_id=self.user_id)]
    Note over Function: 条件付き式を評価: [{#39;key#39;: r[#39;client_key#39;], #39;signature#39;: r[#39;signature#39;], #39;foodId#39;: str(r[#39;food_id#39;]), #39;quantity#39;: quantity(r[#39;amount#39;], r[#39;unit#39;]), #39;checkedAt#39;: iso(r[#39;checked_at#39;]), #39;archived#39;: r[#39;archived#39;]} for r in q.run(#39;q010_shopping#39;, user_id=self.user_id)]
    Note over Function: checks = [{#39;key#39;: r[#39;client_key#39;], #39;signature#39;: r[#39;signature#39;], #39;foodId#39;: str(r[#39;food_id#39;]), #39;quantity#39;: quantity(r[#39;amount#39;], r[#39;unit#39;]), #39;checkedAt#39;: iso(r[#39;checked_at#39;]), #39;archived#39;: r[#39;archived#39;]} for r in q.run(#39;q010_shopping#39;, user_id=self.user_id)]
    Note over Function: from app.core.cooking_service import CookingService
    Function->>Callee: CookingService(self)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: CookingService(self).read_current()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: cooking = CookingService(self).read_current()
    Note over Function: 条件付き式を評価: AppSnapshot.model_validate({#39;schemaVersion#39;: 1, #39;version#39;: int(revision[0][#39;revision#39;]) if revision else 0, #39;lots#39;: lots, #39;imports#39;: imports, #39;drafts#39;: {}, #39;meal#39;: meal, #39;saved#39;: [str(r[#39;recipe_id#39;]) for r in q.run(#39;q007_saved#39;, user_id=self.user_id)], #39;shoppingChecks#39;: checks, #39;cooking#39;: cooking, #39;settings#39;: settings, #39;customFoods#39;: customs, #39;search#39;: {#39;selectedFoodIds#39;: [], #39;match#39;: #39;all#39;, #39;maxMinutes#39;: None, #39;noShopping#39;: False, #39;equipment#39;: []}})
    break この経路の関数終了: return
        Function-->>Caller: AppSnapshot.model_validate({#39;schemaVersion#39;: 1, #39;version#39;: int(revision[0][#39;revision#39;]) if revision else 0, #39;lots#39;: lots, #39;imports#39;: imports, #39;drafts#39;: {}, #39;meal#39;: meal, #39;saved#39;: [str(r[#39;recipe_id#39;]) for r in q.run(#39;q007_saved#39;, user_id=self.user_id)], #39;shoppingChecks#39;: checks, #39;cooking#39;: cooking, #39;settings#39;: settings, #39;customFoods#39;: customs, #39;search#39;: {#39;selectedFoodIds#39;: [], #39;match#39;: #39;all#39;, #39;maxMinutes#39;: None, #39;noShopping#39;: False, #39;equipment#39;: []}})
    end
```

### workspace_service.py: `read_meal`

定義元: `backend/src/app/core/workspace_service.py:186`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as read_meal
    participant Callee as 呼出先
    Caller->>Function: self, q: OperationQueries, menu_id: UUID
    Function->>Callee: q.run(#39;q006_ingredients#39;, menu_id=menu_id, user_id=self.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: amounts = q.run(#39;q006_ingredients#39;, menu_id=menu_id, user_id=self.user_id)
    Note over Function: 条件付き式を評価: [{#39;id#39;: str(r[#39;id#39;]), #39;recipeId#39;: str(r[#39;recipe_id#39;]), #39;recipeVersionId#39;: str(r[#39;recipe_version_id#39;]), #39;servings#39;: float(r[#39;servings#39;]), #39;adjusted#39;: any((a[#39;override_id#39;] is not None for a in amounts if a[#39;menu_item_id#39;] == r[#39;id#39;])), #39;amounts#39;: {str(a[#39;ingredient_id#39;]): quantity(a[#39;override_amount#39;] if a[#39;override_id#39;] else a[#39;scaled_amount#39;], a[#39;unit#39;]) for a in amounts if a[#39;menu_item_id#39;] == r[#39;id#39;]}} for r in q.run(#39;q005_menu#39;, menu_id=menu_id, user_id=self.user_id)]
    break この経路の関数終了: return
        Function-->>Caller: [{#39;id#39;: str(r[#39;id#39;]), #39;recipeId#39;: str(r[#39;recipe_id#39;]), #39;recipeVersionId#39;: str(r[#39;recipe_version_id#39;]), #39;servings#39;: float(r[#39;servings#39;]), #39;adjusted#39;: any((a[#39;override_id#39;] is not None for a in amounts if a[#39;menu_item_id#39;] == r[#39;id#39;])), #39;amounts#39;: {str(a[#39;ingredient_id#39;]): quantity(a[#39;override_amount#39;] if a[#39;override_id#39;] else a[#39;scaled_amount#39;], a[#39;unit#39;]) for a in amounts if a[#39;menu_item_id#39;] == r[#39;id#39;]}} for r in q.run(#39;q005_menu#39;, menu_id=menu_id, user_id=self.user_id)]
    end
```

### workspace_service.py: `add_item`

定義元: `backend/src/app/core/workspace_service.py:262`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as add_item
    participant Callee as 呼出先
    Caller->>Function: self, q: OperationQueries, item: MealItem, menu_id: UUID, name: str
    Note over Function: 条件付き式を評価: q.run(#39;q010_recipe#39;, recipe_id=identifier(item.recipe_id), preview=local_auth_enabled(), requested_version_id=identifier(item.recipe_version_id) if item.recipe_version_id else None)
    Note over Function: version = q.run(#39;q010_recipe#39;, recipe_id=identifier(item.recipe_id), preview=local_auth_enabled(), requested_version_id=identifier(item.recipe_version_id) if item.recipe_version_id else None)
    alt not version
        Function->>Callee: HTTPException(404, #39;料理が公開されていません#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(404, #39;料理が公開されていません#39;)
        end
    end
    Function->>Callee: cast(list[UUID], version[0][#39;role_option_ids#39;])
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: roles = cast(list[UUID], version[0][#39;role_option_ids#39;])
    Function->>Callee: len(roles)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    alt len(roles) != 1
        Function->>Callee: HTTPException(422, #39;料理の献立内役割が未確定です。料理の分類を確認してください#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(422, #39;料理の献立内役割が未確定です。料理の分類を確認してください#39;)
        end
    end
    Function->>Callee: q.run(#39;q011_ingredients#39;, version_id=version[0][#39;id#39;])
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: ingredients = q.run(#39;q011_ingredients#39;, version_id=version[0][#39;id#39;])
    Note over Function: 条件付き式を評価: set(item.amounts) != {str(r[#39;id#39;]) for r in ingredients}
    alt set(item.amounts) != {str(r[#39;id#39;]) for r in ingredients}
        Function->>Callee: HTTPException(422, #39;材料の構成が料理版と一致しません#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(422, #39;材料の構成が料理版と一致しません#39;)
        end
    end
    Function->>Callee: q.run(#39;q012_menu#39;, menu_id=menu_id, user_id=self.user_id, name=name)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: identifier(item.id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: str(item.servings)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: Decimal(str(item.servings))
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: q.run(#39;q013_insert_item#39;, row_id=identifier(item.id), menu_id=menu_id, version_id=version[0][#39;id#39;], servings=Decimal(str(item.servings)), role_option_id=roles[0])
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    loop ingredient in ingredients
        Function->>Callee: str(ingredient[#39;id#39;])
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: amount = item.amounts[str(ingredient[#39;id#39;])]
        Note over Function: 条件付き式を評価: amount.value is None or amount.unit != ingredient[#39;unit#39;]
        alt amount.value is None or amount.unit != ingredient[#39;unit#39;]
            Function->>Callee: HTTPException(422, #39;確定した分量と料理の単位を指定してください#39;)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            break この経路の関数終了: raise
                Function-->>Caller: HTTPException(422, #39;確定した分量と料理の単位を指定してください#39;)
            end
        end
        Note over Function: 条件付き式を評価: amount.value == 0 and (not ingredient[#39;optional#39;])
        alt amount.value == 0 and (not ingredient[#39;optional#39;])
            Function->>Callee: HTTPException(422, #39;必須材料には0より大きい分量を指定してください#39;)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            break この経路の関数終了: raise
                Function-->>Caller: HTTPException(422, #39;必須材料には0より大きい分量を指定してください#39;)
            end
        end
        Note over Function: 条件付き式を評価: q.run(#39;q014_override#39;, row_id=uuid4(), item_id=identifier(item.id), ingredient_id=ingredient[#39;id#39;], amount=Decimal(str(amount.value)) if amount.value #62; 0 else None, selected=amount.value #62; 0)
    end
    Function->>Callee: q.run(#39;q015_advance_menu#39;, menu_id=menu_id, user_id=self.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
```

### workspace_service.py: `add_menu_item`

定義元: `backend/src/app/core/workspace_service.py:304`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as add_menu_item
    participant Callee as 呼出先
    Caller->>Function: self, request: MenuItemRequest
    Function->>Callee: self.begin(#39;add_menu_item#39;, request)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: q = self.begin(#39;add_menu_item#39;, request)
    Function->>Callee: self.add_item(q, request.item, self.menu_id, #39;現在の献立#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: self.finish(q)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: self.finish(q)
    end
```
