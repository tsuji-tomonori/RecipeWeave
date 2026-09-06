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
        401: {"description": "有効なアクセストークンが必要"},
        409: {"description": "版が競合したため、再読込後にやり直す"},
        413: {"description": "リクエストが1MiBを超えている"},
        503: {"description": "同期を利用できない"},
    },
)
def put_state(
    subject: SubjectDependency, repository: StateDependency, body: PutStateRequest
) -> StateEnvelope:
    return api_functions.put_state(repository, subject, body)
