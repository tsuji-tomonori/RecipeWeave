# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from fastapi import APIRouter, Response

from app.apis.entities.ingredient_total_get.contract import CONTRACT
from app.apis.entities.ingredient_total_get.functions import execute
from app.apis.entities.ingredient_total_get.schemas import IngredientTotalRow
from app.core.db import DatabaseDependency
from app.core.entity_service import EntityService
from app.core.identity import IdentityDependency

router = APIRouter(tags=["正規化データ: 献立材料集計結果"])


@router.get(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=IngredientTotalRow,
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
) -> IngredientTotalRow:
    """献立材料集計結果の取得。認証情報は依存から取得し、本人所有または管理者権限を検査する。"""
    result = execute(EntityService(database, identity), row_id)
    response.headers["ETag"] = f'"{result.etag}"'
    return result
