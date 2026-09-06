# シーケンス: renew_shard

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

対象はrouter.py・functions.pyの各関数。呼出元・関数・呼出先の3者で、関数内の分岐と反復を示す。関数間を推測で展開せず、呼出先の名前をそのまま記載する。内包表記・短絡評価は条件付き式のまま残す。ローカル関数は字句スコープ付きの別図にし、関数定義と本文の実行を区別する。エンティティAPIは共有EntityServiceも含める。FastAPIの依存解決、middleware、DBドライバー内部はこの図の対象外。try/except/else/finallyとcontext境界を保持する。continue/breakは注記位置で該当経路を終了し、次の反復/ループ外へ進む。

### router.py: `handle`

定義元: `backend/src/app/apis/generation/renew_shard/router.py:31`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as handle
    participant Callee as 呼出先
    Caller->>Function: payload: Request, identity: IdentityDependency, database: DatabaseDependency, row_id: UUID
    Function->>Callee: EntityService(database, identity)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: execute(payload, EntityService(database, identity), row_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: execute(payload, EntityService(database, identity), row_id)
    end
```

### functions.py: `execute`

定義元: `backend/src/app/apis/generation/renew_shard/functions.py:11`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as execute
    participant Callee as 呼出先
    Caller->>Function: payload: Request, service: EntityService, row_id: UUID
    Function->>Callee: payload.model_dump(mode=#39;python#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: values = payload.model_dump(mode=#39;python#39;)
    Note over Function: values[#39;row_id#39;] = row_id
    Function->>Callee: run_lease_operation(service, #39;renew_shard#39;, values)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: run_lease_operation(service, #39;renew_shard#39;, values)
    end
```

### entity_generation.py: `run_lease_operation`

定義元: `backend/src/app/core/entity_generation.py:17`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as run_lease_operation
    participant Callee as 呼出先
    Caller->>Function: service: EntityService, operation: Literal[#39;claim_shard#39;, #39;renew_shard#39;, #39;advance_shard#39;], values: dict[str, Any]
    alt service.identity.role != #39;admin#39;
        Function->>Callee: HTTPException(status_code=403, detail=#39;生成運用権限が必要です#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(status_code=403, detail=#39;生成運用権限が必要です#39;)
        end
    end
    Note over Function: params = {**values, #39;lease_owner#39;: service.identity.subject}
    loop name in (#39;expected_fence#39;, #39;next_ordinal#39;)
        alt name in params
            Function->>Callee: int(params[name])
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            Note over Function: params[name] = int(params[name])
        end
    end
    Function->>Callee: service.connection.transaction()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: context開始: service.connection.transaction()
    Function->>Callee: OperationQueries(service.connection, #39;generation/#39; + operation)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: OperationQueries(service.connection, #39;generation/#39; + operation).run(#39;q001_execute#39;, **params)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: rows = OperationQueries(service.connection, #39;generation/#39; + operation).run(#39;q001_execute#39;, **params)
    alt not rows
        Function->>Callee: HTTPException(status_code=409, detail=#39;取得対象がないか、リースが失効しました#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(status_code=409, detail=#39;取得対象がないか、リースが失効しました#39;)
        end
    end
    Note over Function: row = rows[0]
    loop name in (#39;start_ordinal#39;, #39;end_ordinal#39;, #39;next_ordinal#39;, #39;fence_token#39;)
        Function->>Callee: str(row[name])
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: row[name] = str(row[name])
    end
    Function->>Callee: replace(SPECIFICATIONS[#39;entity_generation_shard_create#39;], operation_id=operation, action=#39;update#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: spec = replace(SPECIFICATIONS[#39;entity_generation_shard_create#39;], operation_id=operation, action=#39;update#39;)
    Function->>Callee: service.record_change(spec, row[#39;id#39;])
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: logger.info(#39;generation_lease_updated#39;, extra={#39;operation_id#39;: operation})
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: GenerationShardRow.model_validate(row)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: GenerationShardRow.model_validate(row)
    end
    Note over Function: context終了: return・例外時も終了処理
```

### entity_service.py: `record_change`

定義元: `backend/src/app/core/entity_service.py:131`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as record_change
    participant Callee as 呼出先
    Caller->>Function: self, spec: OperationSpec, row_id: UUID
    Note over Function: from app.entities.audit_queries import append_audit, append_outbox
    Note over Function: from app.entities.workspace_query import increment_workspace
    Function->>Callee: str(row_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: str(row_id).encode()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: hashlib.sha256(str(row_id).encode())
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: hashlib.sha256(str(row_id).encode()).hexdigest()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: key_hash = hashlib.sha256(str(row_id).encode()).hexdigest()
    Function->>Callee: uuid4()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: append_audit(self.connection, {#39;row_id#39;: uuid4(), #39;actor_id#39;: self.identity.user_id, #39;action#39;: spec.action, #39;entity_type#39;: spec.table, #39;entity_key_hash#39;: key_hash})
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    alt spec.owned
        Function->>Callee: uuid4()
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: increment_workspace(self.connection, {#39;row_id#39;: uuid4(), #39;actor_id#39;: self.identity.user_id})
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    else 条件が偽
        Function->>Callee: uuid4()
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: append_outbox(                 self.connection,                 {                     #34;row_id#34;: uuid4(),                     #34;event_type#34;: f#34;{spec.table}.{spec.action}#34;,                     #34;aggregate_id#34;: row_id,                 },             )
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    end
```
