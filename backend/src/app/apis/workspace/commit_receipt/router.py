from fastapi import APIRouter

from app.apis.workspace.commit_receipt.contract import CONTRACT
from app.apis.workspace.commit_receipt.functions import execute
from app.apis.workspace.commit_receipt.schemas import AppSnapshot, ReceiptRequest
from app.core.db import DatabaseDependency
from app.core.identity import IdentityDependency
from app.core.workspace_service import WorkspaceService

router = APIRouter(tags=["利用者の操作"])


@router.post(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=AppSnapshot,
    responses={
        code: {"description": "認証・所有権・版・入力の検証失敗"} for code in CONTRACT.errors
    },
)
def handle(
    identity: IdentityDependency, database: DatabaseDependency, request: ReceiptRequest
) -> AppSnapshot:
    """確認したレシートを在庫へ登録する。呼出元が送った利用者IDは使用しない。"""
    return execute(WorkspaceService(database, identity), request)
