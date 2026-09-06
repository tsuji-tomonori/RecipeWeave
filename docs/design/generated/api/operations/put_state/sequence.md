# シーケンス: put_state

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

対象はrouter.py・functions.pyの各関数。呼出元・関数・呼出先の3者で、関数内の分岐と反復を示す。関数間を推測で展開せず、呼出先の名前をそのまま記載する。内包表記・短絡評価は条件付き式のまま残す。FastAPIの依存解決、middleware、連携ポートの実装内部はこの図の対象外で、詳細設計と定義元を参照する。continue/breakは注記位置で該当経路を終了し、次の反復/ループ外へ進む。

### router.py: `put_state`

定義元: `backend/src/app/apis/state/put_state/router.py:23`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as put_state
    participant Callee as 呼出先
    Caller->>Function: subject: SubjectDependency, repository: StateDependency, body: PutStateRequest
    Function->>Callee: api_functions.put_state(repository, subject, body)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: api_functions.put_state(repository, subject, body)
    end
```

#### 対応する実装

```python
@router.put(CONTRACT.path, operation_id=CONTRACT.operation_id, summary=CONTRACT.summary, responses={401: {'description': '有効なアクセストークンが必要'}, 409: {'description': '版が競合したため、再読込後にやり直す'}, 413: {'description': 'リクエストが1MiBを超えている'}, 503: {'description': '同期を利用できない'}})
def put_state(subject: SubjectDependency, repository: StateDependency, body: PutStateRequest) -> StateEnvelope:
    return api_functions.put_state(repository, subject, body)
```

### functions.py: `put_state`

定義元: `backend/src/app/apis/state/put_state/functions.py:5`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as put_state
    participant Callee as 呼出先
    Caller->>Function: repository: StateRepository, subject: str, body: PutStateRequest
    Function->>Callee: repository.put(subject, body.expected_version, body.snapshot)
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: repository.put(subject, body.expected_version, body.snapshot)
    end
```

#### 対応する実装

```python
def put_state(repository: StateRepository, subject: str, body: PutStateRequest) -> StateEnvelope:
    """条件付きで保存する。競合時に新しい端末データを黙って上書きしない。"""
    return repository.put(subject, body.expected_version, body.snapshot)
```
