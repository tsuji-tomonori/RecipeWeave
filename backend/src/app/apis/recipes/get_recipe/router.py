from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials

from app.core.catalog import CatalogDependency
from app.core.db import DatabaseDependency
from app.core.dependencies import bearer
from app.integrations.catalog.preview import authorize_preview

from . import functions as api_functions
from .contract import CONTRACT
from .schemas import Recipe

router = APIRouter()


@router.get(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    openapi_extra={"security": [{}, {"HTTPBearer": []}]},
    responses={
        401: {"description": "下書き閲覧にはログインが必要"},
        403: {"description": "下書き閲覧が許可されていない環境"},
        404: {"description": "料理が見つからない"},
        503: {"description": "DB接続が利用できない"},
    },
)
def get_recipe(
    database: DatabaseDependency,
    catalog: CatalogDependency,
    recipe_id: UUID,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    preview: Annotated[bool, Query()] = False,
) -> Recipe:
    authorize_preview(preview, credentials, database)
    recipe = api_functions.get_recipe(catalog, recipe_id, preview)
    if recipe is None:
        raise HTTPException(status_code=404, detail="料理が見つかりません")
    return recipe
