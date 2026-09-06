---
title: "SQL仕様: get_state"
---

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## backend/src/app/apis/state/get_state/sql/001_select_state.sql

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_state | R | payload, revision, subject |

バインド変数: subject

```sql
-- 認証済み本人の現在の版と保存状態だけを取得する。
SELECT
    revision,
    payload
FROM recipeweave.user_state
WHERE subject = %(subject)s;
```

SQLファイル→自動生成wrapper→連携adapter→functions→routerの境界で管理する。利用者入力はパラメーターとして渡し、SQL文字列へ連結しない。
