# シーケンス: get_health

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

対象はrouter.py・functions.pyの各関数。呼出元・関数・呼出先の3者で、関数内の分岐と反復を示す。関数間を推測で展開せず、呼出先の名前をそのまま記載する。内包表記・短絡評価は条件付き式のまま残す。エンティティAPIは共有EntityServiceも含める。FastAPIの依存解決、middleware、DBドライバー内部はこの図の対象外。try/except/else/finallyとcontext境界を保持する。continue/breakは注記位置で該当経路を終了し、次の反復/ループ外へ進む。

### router.py: `get_health`

定義元: `backend/src/app/apis/health/get_health/router.py:11`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as get_health
    participant Callee as 呼出先
    Caller->>Function: 
    Function->>Callee: api_functions.get_health()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: api_functions.get_health()
    end
```

### functions.py: `get_health`

定義元: `backend/src/app/apis/health/get_health/functions.py:4`

```mermaid
sequenceDiagram
    participant Caller as 呼出元
    participant Function as get_health
    participant Callee as 呼出先
    Caller->>Function: 
    Function->>Callee: HealthResponse()
    Callee-->>Function: 呼出結果（例外は呼出元へ伝播）
    break この経路の関数終了: return
        Function-->>Caller: HealthResponse()
    end
```
