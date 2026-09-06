from typing import Annotated

from fastapi import APIRouter, Query

from app.core.dependencies import CatalogDependency

from . import functions as api_functions
from .contract import CONTRACT
from .schemas import FoodsResponse

router = APIRouter()


@router.get(CONTRACT.path, operation_id=CONTRACT.operation_id, summary=CONTRACT.summary)
def list_foods(
    catalog: CatalogDependency, q: Annotated[str, Query(max_length=100)] = ""
) -> FoodsResponse:
    return api_functions.list_foods(catalog, q)
