"""生成範囲のリース取得のルート。"""

from fastapi import APIRouter

from app.core.db import DatabaseDependency
from app.core.entity_service import EntityService
from app.core.identity import IdentityDependency

from .contract import CONTRACT
from .functions import execute
from .schemas import GenerationShardRow, Request

router = APIRouter(tags=["生成運用"])


@router.post(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=GenerationShardRow,
    responses={
        401: {"description": "認証必須"},
        403: {"description": "運用権限なし"},
        409: {"description": "リース競合・対象なし"},
        422: {"description": "入力不正"},
        503: {"description": "DB接続不可"},
    },
)
def handle(
    payload: Request, identity: IdentityDependency, database: DatabaseDependency
) -> GenerationShardRow:
    return execute(payload, EntityService(database, identity))
