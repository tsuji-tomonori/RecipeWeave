from fastapi import APIRouter

from app.core.dependencies import StateDependency, SubjectDependency

from . import functions as api_functions
from .contract import CONTRACT
from .schemas import PutStateRequest, StateEnvelope

router = APIRouter()


@router.put(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    responses={
        401: {"description": "Valid access token required"},
        409: {"description": "Version conflict; reload before retry"},
        413: {"description": "Request exceeds one MiB"},
        503: {"description": "Synchronization unavailable"},
    },
)
def put_state(
    subject: SubjectDependency, repository: StateDependency, body: PutStateRequest
) -> StateEnvelope:
    return api_functions.put_state(repository, subject, body)
