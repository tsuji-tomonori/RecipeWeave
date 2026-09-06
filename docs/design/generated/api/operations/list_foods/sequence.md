# シーケンス: list_foods

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

対象はrouter.py・functions.pyの各関数。呼出元・関数・呼出先の3者で、関数内の分岐と反復を示す。関数間を推測で展開せず、呼出先の名前をそのまま記載する。内包表記・短絡評価は条件付き式のまま残す。ローカル関数は字句スコープ付きの別図にし、関数定義と本文の実行を区別する。エンティティAPIは共有EntityServiceも含める。FastAPIの依存解決、middleware、DBドライバー内部はこの図の対象外。try/except/else/finallyとcontext境界を保持する。continue/breakは注記位置で該当経路を終了し、次の反復/ループ外へ進む。

### router.py: `list_foods`

定義元: `backend/src/app/apis/foods/list_foods/router.py:28`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as list_foods
    participant Callee as 呼出先
    Caller->>Function: database: DatabaseDependency, catalog: CatalogDependency, credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)], q: Annotated[str, Query(max_length=100)]=#39;#39;
    alt credentials is not None
        Function->>Callee: require_identity(credentials, database)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    end
    Function->>Callee: api_functions.list_foods(catalog, q)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: api_functions.list_foods(catalog, q)
    end
```

### functions.py: `list_foods`

定義元: `backend/src/app/apis/foods/list_foods/functions.py:8`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as list_foods
    participant Callee as 呼出先
    Caller->>Function: catalog: CatalogPort, query: str
    Function->>Callee: unicodedata.normalize(#39;NFKC#39;, query)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: unicodedata.normalize(#39;NFKC#39;, query).casefold()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: unicodedata.normalize(#39;NFKC#39;, query).casefold().strip()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: catalog.foods(unicodedata.normalize(#39;NFKC#39;, query).casefold().strip())
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: items, total = catalog.foods(unicodedata.normalize(#39;NFKC#39;, query).casefold().strip())
    Function->>Callee: FoodsResponse(items=items, total=total)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: FoodsResponse(items=items, total=total)
    end
```

### postgres_provider.py: `foods`

定義元: `backend/src/app/integrations/catalog/postgres_provider.py:18`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as foods
    participant Callee as 呼出先
    Caller->>Function: self, query: str=#39;#39;
    Function->>Callee: OperationQueries(self.connection, #39;foods/list_foods#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: OperationQueries(self.connection, #39;foods/list_foods#39;).run(#39;q001_select_foods#39;, q=query)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: rows = OperationQueries(self.connection, #39;foods/list_foods#39;).run(#39;q001_select_foods#39;, q=query)
    Note over Function: 条件付き式を評価: ([Food.model_validate(row) for row in rows[0][#39;items#39;]], int(rows[0][#39;total#39;]))
    break この経路の関数終了: return
        Function-->>Caller: ([Food.model_validate(row) for row in rows[0][#39;items#39;]], int(rows[0][#39;total#39;]))
    end
```
