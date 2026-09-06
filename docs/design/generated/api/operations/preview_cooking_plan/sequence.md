# シーケンス: preview_cooking_plan

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

対象はrouter.py・functions.pyの各関数。呼出元・関数・呼出先の3者で、関数内の分岐と反復を示す。関数間を推測で展開せず、呼出先の名前をそのまま記載する。内包表記・短絡評価は条件付き式のまま残す。ローカル関数は字句スコープ付きの別図にし、関数定義と本文の実行を区別する。エンティティAPIは共有EntityServiceも含める。FastAPIの依存解決、middleware、DBドライバー内部はこの図の対象外。try/except/else/finallyとcontext境界を保持する。continue/breakは注記位置で該当経路を終了し、次の反復/ループ外へ進む。

### router.py: `handle`

定義元: `backend/src/app/apis/workspace/preview_cooking_plan/router.py:22`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as handle
    participant Callee as 呼出先
    Caller->>Function: identity: IdentityDependency, database: DatabaseDependency, request: PlanRequest
    Function->>Callee: CookingPlanService(database, identity)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: execute(CookingPlanService(database, identity), request)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: execute(CookingPlanService(database, identity), request)
    end
```

### functions.py: `execute`

定義元: `backend/src/app/apis/workspace/preview_cooking_plan/functions.py:4`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as execute
    participant Callee as 呼出先
    Caller->>Function: service: CookingPlanService, request: PlanRequest
    Function->>Callee: service.preview(request)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: service.preview(request)
    end
```

### cooking_plan_service.py: `_uuid`

定義元: `backend/src/app/core/cooking_plan_service.py:33`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as _uuid
    participant Callee as 呼出先
    Caller->>Function: value: str | None
    rect rgb(244, 247, 246)
    Note over Function: try: 例外発生時は一致するexceptへ移る
        Note over Function: 条件付き式を評価: UUID(value or #39;#39;)
        break この経路の関数終了: return
            Function-->>Caller: UUID(value or #39;#39;)
        end
    end
    opt 例外: ValueError
        Function->>Callee: HTTPException(422, #39;料理・材料・献立の識別子を確認してください#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(422, #39;料理・材料・献立の識別子を確認してください#39;)
        end
    end
```

### cooking_plan_service.py: `validate_item`

定義元: `backend/src/app/core/cooking_plan_service.py:40`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as validate_item
    participant Callee as 呼出先
    Caller->>Function: item: MealItem, recipe: Recipe
    Note over Function: 条件付き式を評価: {ingredient.ingredient_id for ingredient in recipe.ingredients}
    Note over Function: keys = {ingredient.ingredient_id for ingredient in recipe.ingredients}
    Note over Function: 条件付き式を評価: None in keys or set(item.amounts) != keys
    alt None in keys or set(item.amounts) != keys
        Function->>Callee: HTTPException(422, #39;指定した料理版と材料の構成が一致しません#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(422, #39;指定した料理版と材料の構成が一致しません#39;)
        end
    end
    loop ingredient in recipe.ingredients
        alt ingredient.ingredient_id is None
            Function->>Callee: HTTPException(422, #39;材料行の識別子が登録されていません#39;)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            break この経路の関数終了: raise
                Function-->>Caller: HTTPException(422, #39;材料行の識別子が登録されていません#39;)
            end
        end
        Note over Function: amount = item.amounts[ingredient.ingredient_id]
        Note over Function: 条件付き式を評価: amount.value is None or amount.unit != ingredient.quantity.unit
        alt amount.value is None or amount.unit != ingredient.quantity.unit
            Function->>Callee: HTTPException(422, #39;材料の量を確定し、登録済みの単位で指定してください#39;)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            break この経路の関数終了: raise
                Function-->>Caller: HTTPException(422, #39;材料の量を確定し、登録済みの単位で指定してください#39;)
            end
        end
    end
```

### cooking_plan_service.py: `preview`

定義元: `backend/src/app/core/cooking_plan_service.py:60`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as preview
    participant Callee as 呼出先
    Caller->>Function: self, request: PlanRequest
    Function->>Callee: PostgresCatalog(self.connection)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: catalog = PostgresCatalog(self.connection)
    Function->>Callee: OperationQueries(self.connection, #39;workspace/preview_cooking_plan#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: queries = OperationQueries(self.connection, #39;workspace/preview_cooking_plan#39;)
    Note over Function: recipes: dict[UUID, Recipe] = {}
    Note over Function: steps: list[dict[str, Any]] = []
    Note over Function: dependencies: list[dict[str, Any]] = []
    Note over Function: requirements: dict[tuple[UUID, UUID], dict[str, Any]] = {}
    Function->>Callee: enumerate(request.items)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    loop (position, item) in enumerate(request.items)
        Function->>Callee: _uuid(item.id)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: item_id = _uuid(item.id)
        alt item_id in recipes
            Function->>Callee: HTTPException(422, #39;同じ献立行が重複しています#39;)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            break この経路の関数終了: raise
                Function-->>Caller: HTTPException(422, #39;同じ献立行が重複しています#39;)
            end
        end
        Function->>Callee: _uuid(item.recipe_id)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: _uuid(item.recipe_version_id)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: catalog_preview_enabled()
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: catalog.recipes(operation=#39;get_recipe#39;, recipe_id=_uuid(item.recipe_id), version_id=_uuid(item.recipe_version_id), owner_id=self.identity.user_id, preview=catalog_preview_enabled())
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: recipe_rows, _ = catalog.recipes(operation=#39;get_recipe#39;, recipe_id=_uuid(item.recipe_id), version_id=_uuid(item.recipe_version_id), owner_id=self.identity.user_id, preview=catalog_preview_enabled())
        alt not recipe_rows
            Function->>Callee: HTTPException(404, #39;この料理版は利用できません#39;)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            break この経路の関数終了: raise
                Function-->>Caller: HTTPException(404, #39;この料理版は利用できません#39;)
            end
        end
        Note over Function: recipe = recipe_rows[0]
        Function->>Callee: validate_item(item, recipe)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: recipes[item_id] = recipe
        Function->>Callee: _uuid(recipe.version_id)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: version_id = _uuid(recipe.version_id)
        Function->>Callee: queries.run(#39;q001_steps#39;, item_id=item_id, position=position, servings=item.servings, version_id=version_id)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: steps.extend(queries.run(#39;q001_steps#39;, item_id=item_id, position=position, servings=item.servings, version_id=version_id))
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: queries.run(#39;q002_dependencies#39;, item_id=item_id, version_id=version_id)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: dependencies.extend(queries.run(#39;q002_dependencies#39;, item_id=item_id, version_id=version_id))
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: queries.run(#39;q003_requirements#39;, version_id=version_id)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        loop row in queries.run(#39;q003_requirements#39;, version_id=version_id)
            Note over Function: requirements[row[#39;step_id#39;], row[#39;resource_type_id#39;]] = row
        end
    end
    Function->>Callee: queries.run(#39;q004_resources#39;, user_id=self.identity.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: resources = queries.run(#39;q004_resources#39;, user_id=self.identity.user_id)
    rect rgb(244, 247, 246)
    Note over Function: try: 例外発生時は一致するexceptへ移る
        Note over Function: 条件付き式を評価: build_plan(steps, dependencies, list(requirements.values()), resources, duration_estimates=[estimate.model_dump() for estimate in request.duration_estimates])
        Note over Function: tasks = build_plan(steps, dependencies, list(requirements.values()), resources, duration_estimates=[estimate.model_dump() for estimate in request.duration_estimates])
    end
    opt 例外: ValueError
        Function->>Callee: str(exc)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: HTTPException(422, str(exc))
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(422, str(exc))
        end
    end
    Note over Function: 条件付き式を評価: {row[#39;id#39;]: row[#39;name#39;] for row in resources}
    Note over Function: resource_names = {row[#39;id#39;]: row[#39;name#39;] for row in resources}
    Note over Function: result: list[PlannedStep] = []
    loop task in tasks
        Note over Function: recipe = recipes[task.item_id]
        Note over Function: 条件付き式を評価: next((step for step in recipe.steps if step.id == str(task.step_id)))
        Note over Function: step = next((step for step in recipe.steps if step.id == str(task.step_id)))
        Note over Function: 条件付き式を評価: result.append(                 PlannedStep.model_validate(                     {                         **step.model_dump(),                         #34;key#34;: f#34;{task.item_id}:{task.step_id}#34;,                         #34;meal_item_id#34;: str(task.item_id),                         #34;recipe_id#34;: recipe.id,                         #34;recipe_name#34;: recipe.name,                         #34;duration_source#34;: task.duration_source,                         #34;confirmed_duration_seconds#34;: task.confirmed_duration_s,                         #34;minutes#34;: (task.end - task.start) / 60,                         #34;start_minute#34;: task.start / 60,                         #34;end_minute#34;: task.end / 60,                         #34;equipment#34;: [                             resource_names[resource_id] for resource_id, _ in task.reservations                         ],                     }                 )             )
    end
    Function->>Callee: PlanResponse(plan=result)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: PlanResponse(plan=result)
    end
```

### postgres_provider.py: `recipes`

定義元: `backend/src/app/integrations/catalog/postgres_provider.py:24`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as recipes
    participant Callee as 呼出先
    Caller->>Function: self, *, operation: Literal[#39;list_recipes#39;, #39;get_recipe#39;, #39;random_recipe#39;], query: str=#39;#39;, selected_food_ids: list[UUID] | None=None, excluded_food_ids: list[UUID] | None=None, match: Literal[#39;all#39;, #39;any#39;]=#39;all#39;, max_minutes: float | None=None, equipment: list[str] | None=None, limit: int=50, offset: int=0, preview: bool=False, recipe_id: UUID | None=None, exclude_id: UUID | None=None, version_id: UUID | None=None, owner_id: UUID | None=None
    Note over Function: queries = {#39;list_recipes#39;: (#39;recipes/list_recipes#39;, #39;q001_select_recipes#39;), #39;get_recipe#39;: (#39;recipes/get_recipe#39;, #39;q001_select_recipe#39;), #39;random_recipe#39;: (#39;recipes/random_recipe#39;, #39;q001_random_recipe#39;)}
    Note over Function: slug, statement = queries[operation]
    Note over Function: 条件付き式を評価: dict(q=query, selected_food_ids=selected_food_ids or [], excluded_food_ids=excluded_food_ids or [], match=match, max_minutes=max_minutes, equipment=equipment or [], limit=limit, offset=offset, preview=preview, recipe_id=recipe_id, exclude_id=exclude_id)
    Note over Function: parameters: dict[str, Any] = dict(q=query, selected_food_ids=selected_food_ids or [], excluded_food_ids=excluded_food_ids or [], match=match, max_minutes=max_minutes, equipment=equipment or [], limit=limit, offset=offset, preview=preview, recipe_id=recipe_id, exclude_id=exclude_id)
    alt operation == #39;get_recipe#39;
        Function->>Callee: parameters.update(version_id=version_id, owner_id=owner_id)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    end
    Function->>Callee: OperationQueries(self.connection, slug)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: OperationQueries(self.connection, slug).run(statement, **parameters)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: rows = OperationQueries(self.connection, slug).run(statement, **parameters)
    Note over Function: 条件付き式を評価: ([Recipe.model_validate(row) for row in rows[0][#39;items#39;]], int(rows[0][#39;total#39;]))
    break この経路の関数終了: return
        Function-->>Caller: ([Recipe.model_validate(row) for row in rows[0][#39;items#39;]], int(rows[0][#39;total#39;]))
    end
```
