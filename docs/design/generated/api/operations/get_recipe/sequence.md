# シーケンス: get_recipe

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

対象はrouter.py・functions.pyの各関数。呼出元・関数・呼出先の3者で、関数内の分岐と反復を示す。関数間を推測で展開せず、呼出先の名前をそのまま記載する。内包表記・短絡評価は条件付き式のまま残す。FastAPIの依存解決、middleware、連携ポートの実装内部はこの図の対象外で、詳細設計と定義元を参照する。continue/breakは注記位置で該当経路を終了し、次の反復/ループ外へ進む。

### router.py: `get_recipe`

定義元: `backend/src/app/apis/recipes/get_recipe/router.py:20`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as get_recipe
    participant Callee as 呼出先
    Caller->>Function: catalog: CatalogDependency, recipe_id: Annotated[str, Path(max_length=128)]
    Function->>Callee: api_functions.get_recipe(catalog, recipe_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: recipe = api_functions.get_recipe(catalog, recipe_id)
    alt recipe is None
        Function->>Callee: HTTPException(status_code=404, detail=#39;recipe not found#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(status_code=404, detail=#39;recipe not found#39;)
        end
    end
    break この経路の関数終了: return
        Function-->>Caller: recipe
    end
```

#### 対応する実装

```python
@router.get(CONTRACT.path, operation_id=CONTRACT.operation_id, summary=CONTRACT.summary, responses={404: {'description': '料理が見つからない'}})
def get_recipe(catalog: CatalogDependency, recipe_id: Annotated[str, Path(max_length=128)]) -> Recipe:
    recipe = api_functions.get_recipe(catalog, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail='recipe not found')
    return recipe
```

### functions.py: `get_recipe`

定義元: `backend/src/app/apis/recipes/get_recipe/functions.py:5`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as get_recipe
    participant Callee as 呼出先
    Caller->>Function: catalog: CatalogPort, recipe_id: str
    Note over Function: 条件付き式を評価: next((recipe for recipe in catalog.recipes() if recipe.id == recipe_id), None)
    break この経路の関数終了: return
        Function-->>Caller: next((recipe for recipe in catalog.recipes() if recipe.id == recipe_id), None)
    end
```

#### 対応する実装

```python
def get_recipe(catalog: CatalogPort, recipe_id: str) -> Recipe | None:
    """料理として完成したサンプルを取得する。構造だけの生成候補は対象にしない。"""
    return next((recipe for recipe in catalog.recipes() if recipe.id == recipe_id), None)
```
