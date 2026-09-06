from fastapi import APIRouter

from app.apis.workspace.preview_cooking_plan.contract import CONTRACT
from app.apis.workspace.preview_cooking_plan.functions import execute
from app.apis.workspace.preview_cooking_plan.schemas import PlanRequest, PlanResponse
from app.core.cooking_plan_service import CookingPlanService
from app.core.db import DatabaseDependency
from app.core.identity import IdentityDependency

router = APIRouter(tags=["利用者の操作"])


@router.post(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=PlanResponse,
    responses={
        code: {"description": "認証・版・分量・設備・工程の検証失敗"} for code in CONTRACT.errors
    },
)
def handle(
    identity: IdentityDependency, database: DatabaseDependency, request: PlanRequest
) -> PlanResponse:
    """実際の調理開始と同じ規則で、表示する段取りを計算する。"""
    return execute(CookingPlanService(database, identity), request)
