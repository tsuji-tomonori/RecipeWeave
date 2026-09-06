# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from fastapi import APIRouter, Response

from app.apis.entities.generation_choice_get.contract import CONTRACT
from app.apis.entities.generation_choice_get.functions import execute
from app.apis.entities.generation_choice_get.schemas import GenerationChoiceRow
from app.core.db import DatabaseDependency
from app.core.entity_service import EntityService
from app.core.identity import IdentityDependency

router = APIRouter(tags=["正規化データ: 生成軸の選択値"])


@router.get(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=GenerationChoiceRow,
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
) -> GenerationChoiceRow:
    """生成軸の選択値の取得。認証情報は依存から取得し、本人所有または管理者権限を検査する。"""
    result = execute(EntityService(database, identity), row_id)
    response.headers["ETag"] = f'"{result.etag}"'
    return result
