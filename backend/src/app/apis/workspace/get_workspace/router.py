from fastapi import APIRouter

from app.apis.workspace.get_workspace.contract import CONTRACT
from app.apis.workspace.get_workspace.functions import execute
from app.apis.workspace.get_workspace.schemas import AppSnapshot
from app.core.db import DatabaseDependency
from app.core.identity import IdentityDependency
from app.core.workspace_service import WorkspaceService

router = APIRouter(tags=["利用者の操作"])


@router.get(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=AppSnapshot,
    responses={
        code: {"description": "認証・所有権・版・入力の検証失敗"} for code in CONTRACT.errors
    },
)
def handle(identity: IdentityDependency, database: DatabaseDependency) -> AppSnapshot:
    """ワークスペースを取得する。呼出元が送った利用者IDは使用しない。"""
    return execute(WorkspaceService(database, identity))
