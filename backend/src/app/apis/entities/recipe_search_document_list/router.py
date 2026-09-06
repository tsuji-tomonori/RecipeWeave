# generate_entity_apis.py による自動生成。直接編集しない。
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.apis.entities.recipe_search_document_list.contract import CONTRACT
from app.apis.entities.recipe_search_document_list.functions import execute
from app.apis.entities.recipe_search_document_list.schemas import RecipeSearchDocumentRow
from app.core.db import DatabaseDependency
from app.core.entity_service import EntityService
from app.core.identity import IdentityDependency

router = APIRouter(tags=["正規化データ: 公開検索用文書"])


@router.get(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=list[RecipeSearchDocumentRow],
    responses={
        401: {"description": "認証が必要"},
        403: {"description": "操作・参照権限なし"},
        409: {"description": "同時更新またはDB業務制約違反"},
        422: {"description": "入力不正"},
        503: {"description": "DB接続不可"},
    },
    status_code=200,
)
def handle(
    identity: IdentityDependency,
    database: DatabaseDependency,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    after: UUID | None = None,
) -> list[RecipeSearchDocumentRow]:
    """公開検索用文書の一覧。認証情報は依存から取得し、本人所有または管理者権限を検査する。"""
    result = execute(EntityService(database, identity), limit, after)
    return result
