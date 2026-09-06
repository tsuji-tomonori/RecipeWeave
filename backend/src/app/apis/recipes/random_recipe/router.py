from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials

from app.core.catalog import CatalogDependency
from app.core.db import DatabaseDependency
from app.core.dependencies import bearer
from app.integrations.catalog.preview import authorize_preview

from . import functions as api_functions
from .contract import CONTRACT
from .schemas import RandomRecipeResponse, RandomRecipeSearch

router = APIRouter()


@router.get(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    openapi_extra={"security": [{}, {"HTTPBearer": []}]},
    responses={
        401: {"description": "下書き閲覧にはログインが必要"},
        403: {"description": "下書き閲覧が許可されていない環境"},
        503: {"description": "DB接続が利用できない"},
    },
)
def random_recipe(
    database: DatabaseDependency,
    catalog: CatalogDependency,
    search: Annotated[RandomRecipeSearch, Query()],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> RandomRecipeResponse:
    authorize_preview(search.preview, credentials, database)
    return api_functions.random_recipe(catalog, search)
