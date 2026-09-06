from fastapi import APIRouter

from . import functions as api_functions
from .contract import CONTRACT
from .schemas import HealthResponse

router = APIRouter()


@router.get(CONTRACT.path, operation_id=CONTRACT.operation_id, summary=CONTRACT.summary)
def get_health() -> HealthResponse:
    return api_functions.get_health()
