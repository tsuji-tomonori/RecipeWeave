from fastapi import APIRouter

from app.apis.auth.get_me.contract import CONTRACT
from app.apis.auth.get_me.functions import execute
from app.apis.auth.get_me.schemas import UserProfile
from app.core.identity import IdentityDependency

router = APIRouter(tags=["認証"])


@router.get(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=UserProfile,
    responses={code: {"description": "認証または設定の検証失敗"} for code in CONTRACT.errors},
)
def handle(identity: IdentityDependency) -> UserProfile:
    """本人のプロフィールを取得する。"""
    return execute(identity)
