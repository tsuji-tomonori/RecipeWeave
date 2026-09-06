# app-docs による自動生成。直接編集しない。
# SQL の SHA256: 748eeff05720cb70a3fa4153bd49f4a4364c09383f44369f245aef0012fd4f4d
from psycopg import Connection
from psycopg.types.json import Jsonb
from pydantic import JsonValue

INSERT_STATE = """-- 最初の版を作成する。同時に作成された場合は版の競合として扱う。
INSERT INTO recipeweave.user_state (subject, revision, payload, updated_at)
VALUES (%(subject)s, 1, %(payload)s, CURRENT_TIMESTAMP);
"""
UPDATE_STATE = """-- 期待した版と一致する本人の保存状態だけを置換し、新しい版を返す。
UPDATE recipeweave.user_state
SET
    revision = revision + 1,
    payload = %(payload)s,
    updated_at = CURRENT_TIMESTAMP
WHERE subject = %(subject)s AND revision = %(revision)s
RETURNING revision;
"""


def insert_state(
    connection: Connection[tuple[object, ...]], subject: str, payload: dict[str, JsonValue]
) -> None:
    connection.execute(INSERT_STATE, {"subject": subject, "payload": Jsonb(payload)})


def update_state(
    connection: Connection[tuple[object, ...]],
    subject: str,
    revision: int,
    payload: dict[str, JsonValue],
) -> bool:
    cursor = connection.execute(
        UPDATE_STATE, {"subject": subject, "revision": revision, "payload": Jsonb(payload)}
    )
    return cursor.rowcount == 1
