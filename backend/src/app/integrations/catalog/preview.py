"""未試作レシピの下書き閲覧を認証済みの明示的なローカル環境へ限定する。"""

from typing import Any

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from psycopg import Connection

from app.core.identity import local_auth_enabled, require_identity


def authorize_preview(
    preview: bool,
    credentials: HTTPAuthorizationCredentials | None,
    database: Connection[dict[str, Any]],
) -> None:
    if not preview:
        return
    if not local_auth_enabled():
        raise HTTPException(status_code=403, detail="下書き閲覧は開発環境に限定されています")
    require_identity(credentials, database)
