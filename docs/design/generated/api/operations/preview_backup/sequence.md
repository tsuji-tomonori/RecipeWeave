# シーケンス: preview_backup

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

対象はrouter.py・functions.pyの各関数。呼出元・関数・呼出先の3者で、関数内の分岐と反復を示す。関数間を推測で展開せず、呼出先の名前をそのまま記載する。内包表記・短絡評価は条件付き式のまま残す。ローカル関数は字句スコープ付きの別図にし、関数定義と本文の実行を区別する。エンティティAPIは共有EntityServiceも含める。FastAPIの依存解決、middleware、DBドライバー内部はこの図の対象外。try/except/else/finallyとcontext境界を保持する。continue/breakは注記位置で該当経路を終了し、次の反復/ループ外へ進む。

### router.py: `handle`

定義元: `backend/src/app/apis/backup/preview_backup/router.py:22`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as handle
    participant Callee as 呼出先
    Caller->>Function: identity: IdentityDependency, database: DatabaseDependency, request: BackupPreviewRequest
    Function->>Callee: BackupService(database, identity)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: execute(BackupService(database, identity), request)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: execute(BackupService(database, identity), request)
    end
```

### functions.py: `execute`

定義元: `backend/src/app/apis/backup/preview_backup/functions.py:5`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as execute
    participant Callee as 呼出先
    Caller->>Function: service: BackupService, request: BackupPreviewRequest
    Function->>Callee: service.preview_backup(request)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: service.preview_backup(request)
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

### backup_service.py: `check_proof`

定義元: `backend/src/app/core/backup_service.py:78`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as check_proof
    participant Callee as 呼出先
    Caller->>Function: self, queries: OperationQueries, document: BackupDocument
    Function->>Callee: self.checked_digest(document)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: digest = self.checked_digest(document)
    Function->>Callee: queries.run(#39;q020_artifact#39;, artifact_id=document.artifact_id, actor_id=self.identity.user_id, body_sha256=digest)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: proof = queries.run(#39;q020_artifact#39;, artifact_id=document.artifact_id, actor_id=self.identity.user_id, body_sha256=digest)
    alt not proof
        Function->>Callee: HTTPException(403, #39;この本人へ発行したバックアップと内容が一致しません#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(403, #39;この本人へ発行したバックアップと内容が一致しません#39;)
        end
    end
    break この経路の関数終了: return
        Function-->>Caller: digest
    end
```

### backup_service.py: `check_references`

定義元: `backend/src/app/core/backup_service.py:116`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as check_references
    participant Callee as 呼出先
    Caller->>Function: self, queries: OperationQueries, document: BackupDocument
    Function->>Callee: document.tables.model_dump(mode=#39;python#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: cast(Rows, document.tables.model_dump(mode=#39;python#39;))
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: data = cast(Rows, document.tables.model_dump(mode=#39;python#39;))
    Note over Function: ids: dict[str, set[UUID]] = {}
    Function->>Callee: defaultdict(set)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: external: dict[str, set[UUID]] = defaultdict(set)
    Function->>Callee: data.items()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    loop (table, rows) in data.items()
        Note over Function: 条件付き式を評価: {row[#39;id#39;] for row in rows}
        Note over Function: ids[table] = {row[#39;id#39;] for row in rows}
        Function->>Callee: len(ids[table])
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: len(rows)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        alt len(ids[table]) != len(rows)
            Function->>Callee: HTTPException(422, #39;同じテーブルに重複した行IDがあります#39;)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            break この経路の関数終了: raise
                Function-->>Caller: HTTPException(422, #39;同じテーブルに重複した行IDがあります#39;)
            end
        end
        loop row in rows
            loop column in (#39;user_id#39;, #39;owner_id#39;)
                Note over Function: 条件付き式を評価: column in row and row[column] != self.identity.user_id
                alt column in row and row[column] != self.identity.user_id
                    Function->>Callee: HTTPException(403, #39;本人の業務行・私有食材だけを復元できます#39;)
                    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
                    break この経路の関数終了: raise
                        Function-->>Caller: HTTPException(403, #39;本人の業務行・私有食材だけを復元できます#39;)
                    end
                end
            end
        end
    end
    Note over Function: ローカル関数 require_reference を定義。本文は別図に示し、定義しただけでは実行しない。
    Function->>Callee: data.items()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    loop (table, rows) in data.items()
        loop reference in TABLES[table][#39;references#39;]
            loop row in rows
                Function->>Callee: require_reference(reference[#39;table#39;], row[reference[#39;column#39;]])
                Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            end
        end
    end
    loop session in data[#39;cooking_session#39;]
        Function->>Callee: CookingInput.model_validate(session[#39;input_snapshot#39;])
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: snapshot = CookingInput.model_validate(session[#39;input_snapshot#39;])
        Function->>Callee: snapshot.model_dump_json()
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: snapshot.model_dump_json().encode()
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: hashlib.sha256(snapshot.model_dump_json().encode())
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: hashlib.sha256(snapshot.model_dump_json().encode()).hexdigest()
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: actual_hash = hashlib.sha256(snapshot.model_dump_json().encode()).hexdigest()
        alt actual_hash != session[#39;input_hash#39;]
            Function->>Callee: HTTPException(409, #39;保存された調理入力とハッシュが一致しません#39;)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            break この経路の関数終了: raise
                Function-->>Caller: HTTPException(409, #39;保存された調理入力とハッシュが一致しません#39;)
            end
        end
        alt snapshot.menu_revision != session[#39;menu_revision#39;]
            Function->>Callee: HTTPException(409, #39;調理入力の献立版が保存した版と一致しません#39;)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            break この経路の関数終了: raise
                Function-->>Caller: HTTPException(409, #39;調理入力の献立版が保存した版と一致しません#39;)
            end
        end
        loop item in snapshot.items
            Function->>Callee: require_reference(#39;menu_item#39;, item.id)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            Function->>Callee: require_reference(#39;recipe_version#39;, item.recipe_version_id)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        end
        loop ingredient in snapshot.ingredients
            Function->>Callee: require_reference(#39;recipe_ingredient#39;, ingredient.id)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            Function->>Callee: require_reference(#39;food_form#39;, ingredient.form_id)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            Function->>Callee: require_reference(#39;unit#39;, ingredient.unit_id)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            Function->>Callee: require_reference(#39;conversion#39;, ingredient.conversion_id)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        end
        loop resource in snapshot.resources
            Function->>Callee: require_reference(#39;kitchen_resource#39;, resource.id)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            Function->>Callee: require_reference(#39;resource_type#39;, resource.resource_type_id)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        end
    end
    Function->>Callee: external.items()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    loop (target, values) in external.items()
        Function->>Callee: sorted(values)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: queries.run(#39;q300_reference_#39; + target, reference_ids=sorted(values))
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: actual = queries.run(#39;q300_reference_#39; + target, reference_ids=sorted(values))
        Note over Function: 条件付き式を評価: {row[#39;id#39;] for row in actual} != values
        alt {row[#39;id#39;] for row in actual} != values
            Function->>Callee: HTTPException(409, #39;必要な共有カタログがないか、参照先を利用できません#39;)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            break この経路の関数終了: raise
                Function-->>Caller: HTTPException(409, #39;必要な共有カタログがないか、参照先を利用できません#39;)
            end
        end
    end
    break この経路の関数終了: return
        Function-->>Caller: data
    end
```

### backup_service.py: `check_references.require_reference`

定義元: `backend/src/app/core/backup_service.py:130`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as check_references.require_reference
    participant Callee as 呼出先
    Caller->>Function: target: str, value: UUID | None
    alt value is None
        break この経路の関数終了: return
            Function-->>Caller: None
        end
    end
    alt target == #39;app_user#39;
        alt value != self.identity.user_id
            Function->>Callee: HTTPException(403, #39;本人以外のアカウントを参照できません#39;)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            break この経路の関数終了: raise
                Function-->>Caller: HTTPException(403, #39;本人以外のアカウントを参照できません#39;)
            end
        end
    else 条件が偽
        Note over Function: 条件付き式を評価: target in ids and value in ids[target]
        alt target in ids and value in ids[target]
            break この経路の関数終了: return
                Function-->>Caller: None
            end
        else 条件が偽
            alt target in OWNED
                Function->>Callee: HTTPException(422, #39;バックアップ内の本人データの参照が不足しています#39;)
                Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
                break この経路の関数終了: raise
                    Function-->>Caller: HTTPException(422, #39;バックアップ内の本人データの参照が不足しています#39;)
                end
            else 条件が偽
                Function->>Callee: external[target].add(value)
                Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            end
        end
    end
```

### backup_service.py: `replace_rows`

定義元: `backend/src/app/core/backup_service.py:171`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as replace_rows
    participant Callee as 呼出先
    Caller->>Function: self, queries: OperationQueries, document: BackupDocument, data: Rows
    Function->>Callee: queries.run(#39;q801_constraints_deferred#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    loop table in DELETE_ORDER
        Function->>Callee: queries.run(#39;q100_delete_#39; + table, actor_id=self.identity.user_id)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    end
    loop table in INSERT_ORDER
        loop row in data[table]
            Function->>Callee: dict(row)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
            Note over Function: values = dict(row)
            loop column in TABLES[table][#39;json_columns#39;]
                alt values[column] is not None
                    Function->>Callee: to_jsonable_python(values[column])
                    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
                    Function->>Callee: Jsonb(to_jsonable_python(values[column]))
                    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
                    Note over Function: values[column] = Jsonb(to_jsonable_python(values[column]))
                end
            end
            loop column in TABLES[table][#39;bigint_columns#39;]
                alt values[column] is not None
                    Function->>Callee: int(values[column])
                    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
                    Note over Function: values[column] = int(values[column])
                end
            end
            Function->>Callee: queries.run(#39;q200_insert_#39; + table, **values)
            Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        end
    end
    Function->>Callee: queries.run(#39;q802_restore_profile#39;, actor_id=self.identity.user_id, locale=document.profile.locale, timezone=document.profile.timezone)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Function->>Callee: queries.run(#39;q800_constraints_immediate#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
```

### backup_service.py: `preview_backup`

定義元: `backend/src/app/core/backup_service.py:194`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as preview_backup
    participant Callee as 呼出先
    Caller->>Function: self, request: BackupPreviewRequest
    Function->>Callee: self.queries(#39;preview_backup#39;)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    Note over Function: queries = self.queries(#39;preview_backup#39;)
    rect rgb(244, 247, 246)
    Note over Function: try: 例外発生時は一致するexceptへ移る
        Function->>Callee: self.connection.transaction()
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: context開始: self.connection.transaction()
        Function->>Callee: self.check_proof(queries, request.backup)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: digest = self.check_proof(queries, request.backup)
        Function->>Callee: self.current_revision(queries)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: revision = self.current_revision(queries)
        Function->>Callee: self.export_tables(queries)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: self.export_tables(queries).model_dump(mode=#39;python#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: cast(Rows, self.export_tables(queries).model_dump(mode=#39;python#39;))
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: current = cast(Rows, self.export_tables(queries).model_dump(mode=#39;python#39;))
        Function->>Callee: self.check_references(queries, request.backup)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: data = self.check_references(queries, request.backup)
        Function->>Callee: self.connection.transaction(force_rollback=True)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: context開始: self.connection.transaction(force_rollback=True)
        Function->>Callee: self.replace_rows(queries, request.backup, data)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: context終了: return・例外時も終了処理
        Function->>Callee: uuid4()
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: intent_id = uuid4()
        Function->>Callee: queries.run(#39;q022_issue_intent#39;, intent_id=intent_id, actor_id=self.identity.user_id, artifact_id=request.backup.artifact_id, body_sha256=digest, current_revision=revision)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: issued = queries.run(#39;q022_issue_intent#39;, intent_id=intent_id, actor_id=self.identity.user_id, artifact_id=request.backup.artifact_id, body_sha256=digest, current_revision=revision)
        Function->>Callee: len(TABLES)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Function->>Callee: logger.info(#39;backup_preview_completed#39;, extra={#39;table_count#39;: len(TABLES)})
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        Note over Function: 条件付き式を評価: BackupPreview(intentId=intent_id, expiresAt=issued[0][#39;expires_at#39;], expectedVersion=revision, backupSha256=digest, sourceVersion=request.backup.source_version, counts=[BackupCount(table=table, label=TABLES[table][#39;label#39;], currentCount=len(current[table]), restoreCount=len(data[table])) for table in TABLES], replaceTargets=[#39;冷蔵庫の在庫・レシート履歴#39;, #39;献立・保存した料理・過去の調理と消費履歴#39;, #39;自分で追加した食材・常備食材・除外条件・器具・買い物確認#39;, #39;言語・タイムゾーンの設定#39;], preservedTargets=[#39;公開レシピ・共通の食材カタログ#39;, #39;アカウントとログイン情報#39;, #39;監査記録・バックアップ発行記録#39;])
        break この経路の関数終了: return
            Function-->>Caller: BackupPreview(intentId=intent_id, expiresAt=issued[0][#39;expires_at#39;], expectedVersion=revision, backupSha256=digest, sourceVersion=request.backup.source_version, counts=[BackupCount(table=table, label=TABLES[table][#39;label#39;], currentCount=len(current[table]), restoreCount=len(data[table])) for table in TABLES], replaceTargets=[#39;冷蔵庫の在庫・レシート履歴#39;, #39;献立・保存した料理・過去の調理と消費履歴#39;, #39;自分で追加した食材・常備食材・除外条件・器具・買い物確認#39;, #39;言語・タイムゾーンの設定#39;], preservedTargets=[#39;公開レシピ・共通の食材カタログ#39;, #39;アカウントとログイン情報#39;, #39;監査記録・バックアップ発行記録#39;])
        end
        Note over Function: context終了: return・例外時も終了処理
    end
    opt 例外: errors.IntegrityError
        Function->>Callee: HTTPException(409, #39;参照・数量・業務制約が成立せず、現在データは変更していません#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(409, #39;参照・数量・業務制約が成立せず、現在データは変更していません#39;)
        end
    end
    opt 例外: errors.InsufficientPrivilege
        Function->>Callee: HTTPException(403, #39;このバックアップの対象を変更する権限がありません#39;)
        Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
        break この経路の関数終了: raise
            Function-->>Caller: HTTPException(403, #39;このバックアップの対象を変更する権限がありません#39;)
        end
    end
```
