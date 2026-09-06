# app-docs による自動生成。直接編集しない。
# SQLのSHA256: c54b3e225e69d0936e2f5a1c0e1b4736fc9c5f826fc0b161a87bc1709e5964fb
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "q001_recipe": """\
-- 公開条件を満たす料理版を保存対象として確認する。
SELECT rv.id
FROM recipeweave.recipe_version AS rv
INNER JOIN recipeweave.recipe AS r ON rv.recipe_id = r.id
WHERE
    r.id = %(recipe_id)s AND (
        (rv.status = 'published' AND r.status = 'published' AND rv.validation = 'passed')
        OR (%(preview)s AND rv.status = 'draft' AND r.status = 'draft')
    )
ORDER BY rv.version DESC LIMIT 1;
""",
    "q002_event": """\
-- 保存・解除は本人の追記イベントとして残す。
INSERT INTO recipeweave.user_recipe_event (
    id, user_id, recipe_version_id, kind, occurred_at, request_key
)
VALUES (%(row_id)s, %(user_id)s, %(version_id)s, 'liked', CLOCK_TIMESTAMP(), %(request_key)s);
""",
    "q900_lock_revision": """\
-- 本人の集約版を排他ロックして並行操作の順序を確定する。
SELECT revision FROM recipeweave.workspace_revision
WHERE user_id = %(user_id)s FOR UPDATE;
""",
    "q901_advance_revision": """\
-- 業務行の更新と同じトランザクションで版を一度だけ進める。
UPDATE recipeweave.workspace_revision SET revision = revision + 1
WHERE user_id = %(user_id)s RETURNING revision;
""",
    "q902_append_audit": """\
-- 個人データ本文を複製せず操作と対象キーのハッシュを記録する。
INSERT INTO recipeweave.audit_event (
    id, actor_id, action, entity_type, entity_key_hash, reason, occurred_at
)
VALUES (
    %(row_id)s, %(user_id)s, %(action)s, 'workspace', %(key_hash)s,
    '本人の業務操作', CURRENT_TIMESTAMP
);
""",
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "q001_recipe": ("preview", "recipe_id"),
    "q002_event": ("request_key", "row_id", "user_id", "version_id"),
    "q900_lock_revision": ("user_id",),
    "q901_advance_revision": ("user_id",),
    "q902_append_audit": ("action", "key_hash", "row_id", "user_id"),
}


def execute(
    connection: Connection[dict[str, Any]], name: str, params: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """許可された固定SQLだけに、宣言と一致する束縛値を別渡しする。"""
    if name not in QUERIES or set(params) != set(PARAMETERS[name]):
        raise ValueError("SQL名または束縛パラメータが操作契約にありません")
    cursor = connection.execute(QUERIES[name], dict(params))
    return list(cursor.fetchall()) if cursor.description is not None else []
