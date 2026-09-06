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
        401: {"description": "有効なアクセストークンが必要"},
        503: {"description": "同期を利用できない"},
    },
)
def get_state(subject: SubjectDependency, repository: StateDependency) -> StateEnvelope:
    return api_functions.get_state(repository, subject)
