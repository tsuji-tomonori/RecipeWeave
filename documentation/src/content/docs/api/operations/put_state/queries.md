---
title: "SQL仕様: put_state"
---

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## backend/src/app/apis/state/put_state/sql/001_insert_state.sql

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_state | C | payload, revision, subject, updated_at |

バインド変数: payload, subject

```sql
-- 最初の版を作成する。同時に作成された場合は版の競合として扱う。
INSERT INTO recipeweave.user_state (subject, revision, payload, updated_at)
VALUES (%(subject)s, 1, %(payload)s, CURRENT_TIMESTAMP);
```

## backend/src/app/apis/state/put_state/sql/002_update_state.sql

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_state | U | payload, revision, subject, updated_at |

バインド変数: payload, revision, subject

```sql
-- 期待した版と一致する本人の保存状態だけを置換し、新しい版を返す。
UPDATE recipeweave.user_state
SET
    revision = revision + 1,
    payload = %(payload)s,
    updated_at = CURRENT_TIMESTAMP
WHERE subject = %(subject)s AND revision = %(revision)s
RETURNING revision;
```

SQLファイル→自動生成wrapper→連携adapter→functions→routerの境界で管理する。利用者入力はパラメーターとして渡し、SQL文字列へ連結しない。
