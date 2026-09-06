# シーケンス: create_cooking_session

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

対象はrouter.py・functions.pyの各関数。呼出元・関数・呼出先の3者で、関数内の分岐と反復を示す。関数間を推測で展開せず、呼出先の名前をそのまま記載する。内包表記・短絡評価は条件付き式のまま残す。ローカル関数は字句スコープ付きの別図にし、関数定義と本文の実行を区別する。エンティティAPIは共有EntityServiceも含める。FastAPIの依存解決、middleware、DBドライバー内部はこの図の対象外。try/except/else/finallyとcontext境界を保持する。continue/breakは注記位置で該当経路を終了し、次の反復/ループ外へ進む。

### router.py: `handle`

定義元: `backend/src/app/apis/workspace/create_cooking_session/router.py:22`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as handle
    participant Callee as 呼出先
    Caller->>Function: identity: IdentityDependency, database: DatabaseDependency, request: CookingRequest
    Function->>Callee: WorkspaceService(database, identity)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: execute(WorkspaceService(database, identity), request)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: execute(WorkspaceService(database, identity), request)
    end
```

### functions.py: `execute`

定義元: `backend/src/app/apis/workspace/create_cooking_session/functions.py:6`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as execute
    participant Callee as 呼出先
    Caller->>Function: service: WorkspaceService, request: CookingRequest
    Function->>Callee: service.create_cooking_session(request)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: service.create_cooking_session(request)
    end
```

### workspace_service.py: `create_cooking_session`

定義元: `backend/src/app/core/workspace_service.py:491`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as create_cooking_session
    participant Callee as 呼出先
    Caller->>Function: self, request: CookingRequest
    Note over Function: from app.core.cooking_service import CookingService
    Function->>Callee: CookingService(self)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: CookingService(self).create(request)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: CookingService(self).create(request)
    end
```

### cooking_service.py: `create`

定義元: `backend/src/app/core/cooking_service.py:111`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as create
    participant Callee as 呼出先
    Caller->>Function: self, request: CookingRequest
    Note over Function: from app.core.cooking_planner import build_plan
    Function->>Callee: self.workspace.begin(#39;create_cooking_session#39;, request)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: q = self.workspace.begin(#39;create_cooking_session#39;, request)
    Function->>Callee: q.run(#39;q001_current#39;, user_id=self.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    alt q.run(#39;q001_current#39;, user_id=self.user_id)
        Function->>Callee: HTTPException(409, #39;調理中の料理を再開するか、完了してから始めてください#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(409, #39;調理中の料理を再開するか、完了してから始めてください#39;)
        end
    end
    alt not request.session.meal_snapshot
        Function->>Callee: HTTPException(422, #39;調理する料理を選んでください#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(422, #39;調理する料理を選んでください#39;)
        end
    end
    Function->>Callee: identifier(request.session.id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: session_id = identifier(request.session.id)
    Function->>Callee: uuid5(session_id, #39;frozen-menu#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: menu_id = uuid5(session_id, #39;frozen-menu#39;)
    Note over Function: frozen_ids: dict[str, UUID] = {}
    loop item in request.session.meal_snapshot
        Function->>Callee: uuid5(session_id, #39;item:#39; + item.id)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: str(uuid5(session_id, #39;item:#39; + item.id))
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: item.model_copy(update={#39;id#39;: str(uuid5(session_id, #39;item:#39; + item.id))})
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: frozen = item.model_copy(update={#39;id#39;: str(uuid5(session_id, #39;item:#39; + item.id))})
        Function->>Callee: identifier(frozen.id)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: frozen_ids[item.id] = identifier(frozen.id)
        Function->>Callee: self.workspace.add_item(q, frozen, menu_id, #39;調理開始時の献立#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    end
    Function->>Callee: q.run(#39;q020_steps#39;, menu_id=menu_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: steps = q.run(#39;q020_steps#39;, menu_id=menu_id)
    Function->>Callee: q.run(#39;q021_dependencies#39;, menu_id=menu_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: dependencies = q.run(#39;q021_dependencies#39;, menu_id=menu_id)
    Function->>Callee: q.run(#39;q022_requirements#39;, menu_id=menu_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: requirements = q.run(#39;q022_requirements#39;, menu_id=menu_id)
    Function->>Callee: q.run(#39;q023_resources#39;, user_id=self.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: resources = q.run(#39;q023_resources#39;, user_id=self.user_id)
    rect rgb(244, 247, 246)
    Note over Function: try: 例外発生時は一致するexceptへ移る
        Note over Function: estimates: list[dict[str, Any]] = []
        loop estimate in request.duration_estimates
            alt estimate.meal_item_id not in frozen_ids
                Function->>Callee: ValueError(#39;この献立に含まれない工程の見積りが指定されています。#39;)
                Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
                break この経路の関数終了: raise
                    Function-->>Caller: ValueError(#39;この献立に含まれない工程の見積りが指定されています。#39;)
                end
            end
            Function->>Callee: estimate.model_dump()
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            Function->>Callee: estimates.append({**estimate.model_dump(), #39;meal_item_id#39;: frozen_ids[estimate.meal_item_id]})
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        end
        Function->>Callee: build_plan(steps, dependencies, requirements, resources, duration_estimates=estimates)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: plan = build_plan(steps, dependencies, requirements, resources, duration_estimates=estimates)
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
    Function->>Callee: q.run(#39;q024_ingredients#39;, menu_id=menu_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: ingredients = q.run(#39;q024_ingredients#39;, menu_id=menu_id)
    Note over Function: 条件付き式を評価: any((r[#39;amount#39;] is None for r in ingredients))
    alt any((r[#39;amount#39;] is None for r in ingredients))
        Function->>Callee: HTTPException(422, #39;調理前に材料の量を確定してください#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(422, #39;調理前に材料の量を確定してください#39;)
        end
    end
    Function->>Callee: defaultdict(set)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: identities: dict[tuple[UUID, UUID], set[UUID | None]] = defaultdict(set)
    loop ingredient in ingredients
        Function->>Callee: identities[ingredient[#39;form_id#39;], ingredient[#39;unit_id#39;]].add(ingredient[#39;product_version_id#39;])
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    end
    Note over Function: 条件付き式を評価: any((len(values) #62; 1 for values in identities.values()))
    alt any((len(values) #62; 1 for values in identities.values()))
        Function->>Callee: HTTPException(422, #39;同じ食材の複数商品は、商品版ごとの調理APIで指定してください#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(422, #39;同じ食材の複数商品は、商品版ごとの調理APIで指定してください#39;)
        end
    end
    Function->>Callee: q.run(#39;q030_menu_revision#39;, menu_id=menu_id, user_id=self.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: revision = q.run(#39;q030_menu_revision#39;, menu_id=menu_id, user_id=self.user_id)[0][#39;revision#39;]
    Note over Function: item_values: dict[UUID, dict[str, Any]] = {}
    loop row in ingredients
        Note over Function: item_values[row[#39;item_id#39;]] = {#39;id#39;: row[#39;item_id#39;], #39;recipe_version_id#39;: row[#39;recipe_version_id#39;], #39;servings#39;: row[#39;servings#39;]}
    end
    Note over Function: 条件付き式を評価: CookingInput.model_validate({#39;schema_version#39;: 1, #39;menu_revision#39;: revision, #39;items#39;: list(item_values.values()), #39;ingredients#39;: [{#39;id#39;: r[#39;ingredient_id#39;], #39;form_id#39;: r[#39;form_id#39;], #39;amount#39;: r[#39;amount#39;], #39;unit_id#39;: r[#39;unit_id#39;], #39;conversion_id#39;: r[#39;conversion_id#39;]} for r in ingredients], #39;resources#39;: [{key: r[key] for key in [#39;id#39;, #39;resource_type_id#39;, #39;quantity#39;, #39;capacity#39;]} for r in resources], #39;planner_config#39;: {#39;planner_version#39;: #39;dag-resource-manual-v2#39;, #39;concurrent_active_tasks#39;: 1}})
    Note over Function: snapshot = CookingInput.model_validate({#39;schema_version#39;: 1, #39;menu_revision#39;: revision, #39;items#39;: list(item_values.values()), #39;ingredients#39;: [{#39;id#39;: r[#39;ingredient_id#39;], #39;form_id#39;: r[#39;form_id#39;], #39;amount#39;: r[#39;amount#39;], #39;unit_id#39;: r[#39;unit_id#39;], #39;conversion_id#39;: r[#39;conversion_id#39;]} for r in ingredients], #39;resources#39;: [{key: r[key] for key in [#39;id#39;, #39;resource_type_id#39;, #39;quantity#39;, #39;capacity#39;]} for r in resources], #39;planner_config#39;: {#39;planner_version#39;: #39;dag-resource-manual-v2#39;, #39;concurrent_active_tasks#39;: 1}})
    Function->>Callee: snapshot.model_dump_json()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: encoded = snapshot.model_dump_json()
    Function->>Callee: snapshot.model_dump(mode=#39;json#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: Jsonb(snapshot.model_dump(mode=#39;json#39;))
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: encoded.encode()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: hashlib.sha256(encoded.encode())
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: hashlib.sha256(encoded.encode()).hexdigest()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: q.run(#39;q025_session#39;, session_id=session_id, menu_id=menu_id, revision=revision, snapshot=Jsonb(snapshot.model_dump(mode=#39;json#39;)), hash=hashlib.sha256(encoded.encode()).hexdigest())
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: task_ids: dict[tuple[UUID, UUID], UUID] = {}
    loop task in plan
        Function->>Callee: uuid5(session_id, f#39;task:{task.item_id}:{task.step_id}#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: task_id = uuid5(session_id, f#39;task:{task.item_id}:{task.step_id}#39;)
        Note over Function: task_ids[task.item_id, task.step_id] = task_id
        Function->>Callee: q.run(#39;q026_task#39;, row_id=task_id, session_id=session_id, item_id=task.item_id, step_id=task.step_id, start=task.start, end=task.end, duration_source=task.duration_source, confirmed_duration_s=task.confirmed_duration_s)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        loop (resource_id, count) in task.reservations
            Function->>Callee: uuid4()
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            Function->>Callee: q.run(#39;q028_reservation#39;, row_id=uuid4(), task_id=task_id, resource_id=resource_id, start=task.start, end=task.end, quantity=count)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        end
    end
    loop dependency in dependencies
        Function->>Callee: uuid4()
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: q.run(#39;q027_dependency#39;, row_id=uuid4(), before_id=task_ids[dependency[#39;item_id#39;], dependency[#39;before_step_id#39;]], after_id=task_ids[dependency[#39;item_id#39;], dependency[#39;after_step_id#39;]], min_lag=dependency[#39;min_lag_s#39;], max_lag=dependency[#39;max_lag_s#39;], reason=dependency[#39;kind#39;])
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    end
    Function->>Callee: defaultdict(Decimal)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: totals: dict[tuple[UUID, UUID | None, UUID], Decimal] = defaultdict(Decimal)
    loop ingredient in ingredients
        Note over Function: key = (ingredient[#39;form_id#39;], ingredient[#39;product_version_id#39;], ingredient[#39;unit_id#39;])
        Note over Function: totals[key] += ingredient[#39;amount#39;]
    end
    Function->>Callee: totals.items()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    loop ((form_id, product_id, unit_id), amount) in totals.items()
        Function->>Callee: uuid4()
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: q.run(#39;q029_total#39;, row_id=uuid4(), session_id=session_id, form_id=form_id, product_id=product_id, unit_id=unit_id, amount=amount)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    end
    Function->>Callee: self.workspace.finish(q)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: self.workspace.finish(q)
    end
```
