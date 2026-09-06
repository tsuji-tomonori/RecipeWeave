from uuid import UUID

from fastapi import APIRouter

from app.apis.workspace.unsave_recipe.contract import CONTRACT
from app.apis.workspace.unsave_recipe.functions import execute
from app.apis.workspace.unsave_recipe.schemas import AppSnapshot, RevisionRequest
from app.core.db import DatabaseDependency
from app.core.identity import IdentityDependency
from app.core.workspace_service import WorkspaceService

router = APIRouter(tags=["利用者の操作"])


@router.delete(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=AppSnapshot,
    responses={
        code: {"description": "認証・所有権・版・入力の検証失敗"} for code in CONTRACT.errors
    },
)
def handle(
    identity: IdentityDependency,
    database: DatabaseDependency,
    request: RevisionRequest,
    row_id: UUID,
) -> AppSnapshot:
    """料理の保存を解除する。呼出元が送った利用者IDは使用しない。"""
    return execute(WorkspaceService(database, identity), request, row_id)
