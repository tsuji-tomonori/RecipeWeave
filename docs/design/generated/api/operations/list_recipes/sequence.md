# シーケンス: list_recipes

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

対象はrouter.py・functions.pyの各関数。呼出元・関数・呼出先の3者で、関数内の分岐と反復を示す。関数間を推測で展開せず、呼出先の名前をそのまま記載する。内包表記・短絡評価は条件付き式のまま残す。FastAPIの依存解決、middleware、連携ポートの実装内部はこの図の対象外で、詳細設計と定義元を参照する。continue/breakは注記位置で該当経路を終了し、次の反復/ループ外へ進む。

### router.py: `list_recipes`

定義元: `backend/src/app/apis/recipes/list_recipes/router.py:15`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as list_recipes
    participant Callee as 呼出先
    Caller->>Function: catalog: CatalogDependency, search: Annotated[RecipeSearch, Query()]
    Function->>Callee: api_functions.list_recipes(catalog, search)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: api_functions.list_recipes(catalog, search)
    end
```

#### 対応する実装

```python
@router.get(CONTRACT.path, operation_id=CONTRACT.operation_id, summary=CONTRACT.summary)
def list_recipes(catalog: CatalogDependency, search: Annotated[RecipeSearch, Query()]) -> RecipesResponse:
    return api_functions.list_recipes(catalog, search)
```

### functions.py: `has_matching_ingredients`

定義元: `backend/src/app/apis/recipes/list_recipes/functions.py:9`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as has_matching_ingredients
    participant Callee as 呼出先
    Caller->>Function: recipe: Recipe, search: RecipeSearch
    Note over Function: 条件付き式を評価: {item.food_id for item in recipe.ingredients}
    Note over Function: present = {item.food_id for item in recipe.ingredients}
    Function->>Callee: set(search.selected_food_ids)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: selected = set(search.selected_food_ids)
    Note over Function: 条件付き式を評価: not selected or (selected #60;= present if search.match == #39;all#39; else bool(selected #38; present))
    break この経路の関数終了: return
        Function-->>Caller: not selected or (selected #60;= present if search.match == #39;all#39; else bool(selected #38; present))
    end
```

#### 対応する実装

```python
def has_matching_ingredients(recipe: Recipe, search: RecipeSearch) -> bool:
    """選択食材の全件一致・部分一致を適用する。人数は検索条件に含めない。"""
    present = {item.food_id for item in recipe.ingredients}
    selected = set(search.selected_food_ids)
    return not selected or (selected <= present if search.match == 'all' else bool(selected & present))
```

### functions.py: `has_excluded_food`

定義元: `backend/src/app/apis/recipes/list_recipes/functions.py:18`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as has_excluded_food
    participant Callee as 呼出先
    Caller->>Function: recipe: Recipe, excluded: set[str], foods: dict[str, Food]
    Note over Function: 条件付き式を評価: [item.food_id for item in recipe.ingredients]
    Note over Function: pending = [item.food_id for item in recipe.ingredients]
    Function->>Callee: set()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: visited: set[str] = set()
    loop pending
        Function->>Callee: pending.pop()
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: food_id = pending.pop()
        alt food_id in excluded
            break この経路の関数終了: return
                Function-->>Caller: True
            end
        end
        alt food_id in visited
            Note over Function: 次の反復へ進む
        end
        Function->>Callee: visited.add(food_id)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: foods.get(food_id)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: food = foods.get(food_id)
        alt food is not None
            Function->>Callee: pending.extend(food.component_food_ids)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        end
    end
    break この経路の関数終了: return
        Function-->>Caller: False
    end
```

#### 対応する実装

```python
def has_excluded_food(recipe: Recipe, excluded: set[str], foods: dict[str, Food]) -> bool:
    """判明している構成食材を含む複合食品を除外する。アレルギー対応を保証しない。"""
    pending = [item.food_id for item in recipe.ingredients]
    visited: set[str] = set()
    while pending:
        food_id = pending.pop()
        if food_id in excluded:
            return True
        if food_id in visited:
            continue
        visited.add(food_id)
        food = foods.get(food_id)
        if food is not None:
            pending.extend(food.component_food_ids)
    return False
```

### functions.py: `list_recipes`

定義元: `backend/src/app/apis/recipes/list_recipes/functions.py:35`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as list_recipes
    participant Callee as 呼出先
    Caller->>Function: catalog: CatalogPort, search: RecipeSearch
    Note over Function: 条件付き式を評価: {food.id: food for food in catalog.foods()}
    Note over Function: foods = {food.id: food for food in catalog.foods()}
    Function->>Callee: unicodedata.normalize(#39;NFKC#39;, search.q)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: unicodedata.normalize(#39;NFKC#39;, search.q).casefold()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: unicodedata.normalize(#39;NFKC#39;, search.q).casefold().strip()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: query = unicodedata.normalize(#39;NFKC#39;, search.q).casefold().strip()
    Note over Function: items: list[Recipe] = []
    Function->>Callee: catalog.recipes()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    loop recipe in catalog.recipes()
        Function->>Callee: unicodedata.normalize(#39;NFKC#39;, recipe.name + recipe.description)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: unicodedata.normalize(#39;NFKC#39;, recipe.name + recipe.description).casefold()
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: text = unicodedata.normalize(#39;NFKC#39;, recipe.name + recipe.description).casefold()
        Note over Function: 条件付き式を評価: query and query not in text
        alt query and query not in text
            Note over Function: 次の反復へ進む
        end
        Function->>Callee: has_matching_ingredients(recipe, search)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        alt not has_matching_ingredients(recipe, search)
            Note over Function: 次の反復へ進む
        end
        Function->>Callee: set(search.excluded_food_ids)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: has_excluded_food(recipe, set(search.excluded_food_ids), foods)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        alt has_excluded_food(recipe, set(search.excluded_food_ids), foods)
            Note over Function: 次の反復へ進む
        end
        Note over Function: 条件付き式を評価: search.max_minutes is not None and recipe.minutes #62; search.max_minutes
        alt search.max_minutes is not None and recipe.minutes #62; search.max_minutes
            Note over Function: 次の反復へ進む
        end
        Note over Function: 条件付き式を評価: search.equipment and (not set(recipe.equipment) #60;= set(search.equipment))
        alt search.equipment and (not set(recipe.equipment) #60;= set(search.equipment))
            Note over Function: 次の反復へ進む
        end
        Function->>Callee: items.append(recipe)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    end
    Function->>Callee: len(items)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: RecipesResponse(items=items, total=len(items))
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: RecipesResponse(items=items, total=len(items))
    end
```

#### 対応する実装

```python
def list_recipes(catalog: CatalogPort, search: RecipeSearch) -> RecipesResponse:
    """件数を水増しせず、対象を限定したサンプル料理を検索する。"""
    foods = {food.id: food for food in catalog.foods()}
    query = unicodedata.normalize('NFKC', search.q).casefold().strip()
    items: list[Recipe] = []
    for recipe in catalog.recipes():
        text = unicodedata.normalize('NFKC', recipe.name + recipe.description).casefold()
        if query and query not in text:
            continue
        if not has_matching_ingredients(recipe, search):
            continue
        if has_excluded_food(recipe, set(search.excluded_food_ids), foods):
            continue
        if search.max_minutes is not None and recipe.minutes > search.max_minutes:
            continue
        if search.equipment and (not set(recipe.equipment) <= set(search.equipment)):
            continue
        items.append(recipe)
    return RecipesResponse(items=items, total=len(items))
```
