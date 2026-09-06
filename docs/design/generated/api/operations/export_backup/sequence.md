# シーケンス: export_backup

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

対象はrouter.py・functions.pyの各関数。呼出元・関数・呼出先の3者で、関数内の分岐と反復を示す。関数間を推測で展開せず、呼出先の名前をそのまま記載する。内包表記・短絡評価は条件付き式のまま残す。ローカル関数は字句スコープ付きの別図にし、関数定義と本文の実行を区別する。エンティティAPIは共有EntityServiceも含める。FastAPIの依存解決、middleware、DBドライバー内部はこの図の対象外。try/except/else/finallyとcontext境界を保持する。continue/breakは注記位置で該当経路を終了し、次の反復/ループ外へ進む。

### router.py: `handle`

定義元: `backend/src/app/apis/backup/export_backup/router.py:22`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as handle
    participant Callee as 呼出先
    Caller->>Function: identity: IdentityDependency, database: DatabaseDependency
    Function->>Callee: BackupService(database, identity)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: execute(BackupService(database, identity))
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: execute(BackupService(database, identity))
    end
```

### functions.py: `execute`

定義元: `backend/src/app/apis/backup/export_backup/functions.py:5`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as execute
    participant Callee as 呼出先
    Caller->>Function: service: BackupService
    Function->>Callee: service.export_backup()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: service.export_backup()
    end
```

### backup_service.py: `canonical_backup`

定義元: `backend/src/app/core/backup_service.py:37`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as canonical_backup
    participant Callee as 呼出先
    Caller->>Function: document: BackupDocument
    Function->>Callee: document.model_dump(mode=#39;json#39;, by_alias=True)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: json.dumps(document.model_dump(mode=#39;json#39;, by_alias=True), ensure_ascii=False, sort_keys=True, separators=(#39;,#39;, #39;:#39;), allow_nan=False)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: json.dumps(document.model_dump(mode=#39;json#39;, by_alias=True), ensure_ascii=False, sort_keys=True, separators=(#39;,#39;, #39;:#39;), allow_nan=False).encode(#39;utf-8#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: json.dumps(document.model_dump(mode=#39;json#39;, by_alias=True), ensure_ascii=False, sort_keys=True, separators=(#39;,#39;, #39;:#39;), allow_nan=False).encode(#39;utf-8#39;)
    end
```

### backup_service.py: `queries`

定義元: `backend/src/app/core/backup_service.py:55`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as queries
    participant Callee as 呼出先
    Caller->>Function: self, operation: str
    Function->>Callee: OperationQueries(self.connection, #39;backup/#39; + operation)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: OperationQueries(self.connection, #39;backup/#39; + operation)
    end
```

### backup_service.py: `current_revision`

定義元: `backend/src/app/core/backup_service.py:58`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as current_revision
    participant Callee as 呼出先
    Caller->>Function: self, queries: OperationQueries
    Function->>Callee: queries.run(#39;q001_lock_revision#39;, actor_id=self.identity.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: rows = queries.run(#39;q001_lock_revision#39;, actor_id=self.identity.user_id)
    alt not rows
        Function->>Callee: HTTPException(409, #39;本人の更新版を取得できません#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(409, #39;本人の更新版を取得できません#39;)
        end
    end
    Function->>Callee: int(rows[0][#39;revision#39;])
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: int(rows[0][#39;revision#39;])
    end
```

### backup_service.py: `export_tables`

定義元: `backend/src/app/core/backup_service.py:64`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as export_tables
    participant Callee as 呼出先
    Caller->>Function: self, queries: OperationQueries
    Function->>Callee: queries.run(#39;q010_export_tables#39;, actor_id=self.identity.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: rows = queries.run(#39;q010_export_tables#39;, actor_id=self.identity.user_id)
    Note over Function: 条件付き式を評価: BackupTables.model_validate({key.removeprefix(#39;rows_#39;): value for key, value in rows[0].items()})
    break この経路の関数終了: return
        Function-->>Caller: BackupTables.model_validate({key.removeprefix(#39;rows_#39;): value for key, value in rows[0].items()})
    end
```

### backup_service.py: `checked_digest`

定義元: `backend/src/app/core/backup_service.py:70`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as checked_digest
    participant Callee as 呼出先
    Caller->>Function: self, document: BackupDocument
    alt document.owner_id != self.identity.user_id
        Function->>Callee: HTTPException(403, #39;別の利用者のバックアップは復元できません#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(403, #39;別の利用者のバックアップは復元できません#39;)
        end
    end
    Function->>Callee: canonical_backup(document)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: encoded = canonical_backup(document)
    Function->>Callee: len(encoded)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    alt len(encoded) #62; MAX_BACKUP_BYTES
        Function->>Callee: HTTPException(413, #39;バックアップの上限は5,000,000バイトです#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(413, #39;バックアップの上限は5,000,000バイトです#39;)
        end
    end
    Function->>Callee: hashlib.sha256(encoded)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: hashlib.sha256(encoded).hexdigest()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: hashlib.sha256(encoded).hexdigest()
    end
```

### backup_service.py: `export_backup`

定義元: `backend/src/app/core/backup_service.py:90`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as export_backup
    participant Callee as 呼出先
    Caller->>Function: self
    Function->>Callee: self.queries(#39;export_backup#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: queries = self.queries(#39;export_backup#39;)
    Function->>Callee: self.connection.transaction()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: context開始: self.connection.transaction()
    Function->>Callee: self.current_revision(queries)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: revision = self.current_revision(queries)
    Function->>Callee: queries.run(#39;q002_profile#39;, actor_id=self.identity.user_id)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: profile = queries.run(#39;q002_profile#39;, actor_id=self.identity.user_id)
    Function->>Callee: uuid4()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: datetime.now(UTC)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: BackupProfile.model_validate(profile[0])
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: self.export_tables(queries)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: BackupDocument(format=#39;recipeweave-relational#39;, formatVersion=2, artifactId=uuid4(), ownerId=self.identity.user_id, exportedAt=datetime.now(UTC), sourceVersion=revision, profile=BackupProfile.model_validate(profile[0]), tables=self.export_tables(queries))
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: document = BackupDocument(format=#39;recipeweave-relational#39;, formatVersion=2, artifactId=uuid4(), ownerId=self.identity.user_id, exportedAt=datetime.now(UTC), sourceVersion=revision, profile=BackupProfile.model_validate(profile[0]), tables=self.export_tables(queries))
    Function->>Callee: self.checked_digest(document)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: digest = self.checked_digest(document)
    Function->>Callee: queries.run(#39;q021_issue_artifact#39;, artifact_id=document.artifact_id, actor_id=self.identity.user_id, body_sha256=digest)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: logger.info(#39;backup_export_completed#39;, extra={#39;format_version#39;: 2})
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: document
    end
    Note over Function: context終了: return・例外時も終了処理
```
