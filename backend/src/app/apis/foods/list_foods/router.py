from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials

from app.core.catalog import CatalogDependency
from app.core.db import DatabaseDependency
from app.core.dependencies import bearer
from app.core.identity import require_identity

from . import functions as api_functions
from .contract import CONTRACT
from .schemas import FoodsResponse

router = APIRouter()


@router.get(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    openapi_extra={"security": [{}, {"HTTPBearer": []}]},
    responses={
        401: {"description": "指定された認証情報が無効"},
        503: {"description": "DB接続が利用できない"},
    },
)
def list_foods(
    database: DatabaseDependency,
    catalog: CatalogDependency,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    q: Annotated[str, Query(max_length=100)] = "",
) -> FoodsResponse:
    if credentials is not None:
        require_identity(credentials, database)
    return api_functions.list_foods(catalog, q)
