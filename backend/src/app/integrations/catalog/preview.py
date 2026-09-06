"""未試作レシピの閲覧を、許可された開発環境の署名検証済み利用者へ限定する。"""

from typing import Any

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from psycopg import Connection

from app.core.catalog_preview import catalog_preview_enabled
from app.core.identity import Identity, require_identity


def authorize_preview(
    preview: bool,
    credentials: HTTPAuthorizationCredentials | None,
    database: Connection[dict[str, Any]],
) -> Identity | None:
    if not preview:
        return None
    if not catalog_preview_enabled():
        raise HTTPException(
            status_code=403, detail="下書き閲覧は明示的に許可された開発環境に限定されています"
        )
    return require_identity(credentials, database)
