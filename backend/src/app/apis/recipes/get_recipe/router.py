from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from app.core.dependencies import CatalogDependency

from . import functions as api_functions
from .contract import CONTRACT
from .schemas import Recipe

router = APIRouter()


@router.get(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    responses={404: {"description": "Recipe not found"}},
)
def get_recipe(
    catalog: CatalogDependency, recipe_id: Annotated[str, Path(max_length=128)]
) -> Recipe:
    recipe = api_functions.get_recipe(catalog, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="recipe not found")
    return recipe
