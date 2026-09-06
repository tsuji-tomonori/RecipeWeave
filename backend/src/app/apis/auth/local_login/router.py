from fastapi import APIRouter

from app.apis.auth.local_login.contract import CONTRACT
from app.apis.auth.local_login.functions import execute
from app.apis.auth.local_login.schemas import LoginRequest, LoginResponse

router = APIRouter(tags=["認証"])


@router.post(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=LoginResponse,
    responses={code: {"description": "認証または設定の検証失敗"} for code in CONTRACT.errors},
)
def handle(request: LoginRequest) -> LoginResponse:
    """開発環境へログインする。"""
    return execute(request)
