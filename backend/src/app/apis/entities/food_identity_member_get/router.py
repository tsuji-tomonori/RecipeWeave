# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from fastapi import APIRouter, Response

from app.apis.entities.food_identity_member_get.contract import CONTRACT
from app.apis.entities.food_identity_member_get.functions import execute
from app.apis.entities.food_identity_member_get.schemas import FoodIdentityMemberRow
from app.core.db import DatabaseDependency
from app.core.entity_service import EntityService
from app.core.identity import IdentityDependency

router = APIRouter(tags=["正規化データ: 購買食品から同一性への対応"])


@router.get(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=FoodIdentityMemberRow,
    responses={
        401: {"description": "認証が必要"},
        403: {"description": "操作・参照権限なし"},
        404: {"description": "対象なし"},
        409: {"description": "同時更新またはDB業務制約違反"},
        422: {"description": "入力不正"},
        503: {"description": "DB接続不可"},
    },
    status_code=200,
)
def handle(
    response: Response, identity: IdentityDependency, database: DatabaseDependency, row_id: UUID
) -> FoodIdentityMemberRow:
    """購買食品から同一性への対応の取得。認証情報は依存から取得し、本人所有または管理者権限を検査する。"""
    result = execute(EntityService(database, identity), row_id)
    response.headers["ETag"] = f'"{result.etag}"'
    return result
