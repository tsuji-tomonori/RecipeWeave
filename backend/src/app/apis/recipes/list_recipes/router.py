from typing import Annotated

from fastapi import APIRouter, Query

from app.core.dependencies import CatalogDependency

from . import functions as api_functions
from .contract import CONTRACT
from .schemas import RecipeSearch, RecipesResponse

router = APIRouter()


@router.get(CONTRACT.path, operation_id=CONTRACT.operation_id, summary=CONTRACT.summary)
def list_recipes(
    catalog: CatalogDependency, search: Annotated[RecipeSearch, Query()]
) -> RecipesResponse:
    return api_functions.list_recipes(catalog, search)
