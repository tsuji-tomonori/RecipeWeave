from fastapi import APIRouter

from app.core.dependencies import StateDependency, SubjectDependency

from . import functions as api_functions
from .contract import CONTRACT
from .schemas import StateEnvelope

router = APIRouter()


@router.get(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    responses={
        401: {"description": "Valid access token required"},
        503: {"description": "Synchronization unavailable"},
    },
)
def get_state(subject: SubjectDependency, repository: StateDependency) -> StateEnvelope:
    return api_functions.get_state(repository, subject)
