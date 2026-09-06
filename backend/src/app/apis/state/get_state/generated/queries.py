# app-docs による自動生成。直接編集しない。
# SQL の SHA256: 748eeff05720cb70a3fa4153bd49f4a4364c09383f44369f245aef0012fd4f4d
from dataclasses import dataclass

from psycopg import Connection
from psycopg.rows import class_row
from pydantic import JsonValue

SELECT_STATE = """-- 認証済み本人の現在の版と保存状態だけを取得する。
SELECT
    revision,
    payload
FROM recipeweave.user_state
WHERE subject = %(subject)s;
"""


@dataclass
class StoredState:
    revision: int
    payload: dict[str, JsonValue]


def select_state(connection: Connection[tuple[object, ...]], subject: str) -> StoredState | None:
    with connection.cursor(row_factory=class_row(StoredState)) as cursor:
        cursor.execute(SELECT_STATE, {"subject": subject})
        return cursor.fetchone()
