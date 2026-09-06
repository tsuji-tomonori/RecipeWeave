# generate_entity_apis.py による自動生成。直接編集しない。
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Header, Response

from app.apis.entities.shopping_item_update.contract import CONTRACT
from app.apis.entities.shopping_item_update.functions import execute
from app.apis.entities.shopping_item_update.schemas import ShoppingItemRow, ShoppingItemWrite
from app.core.db import DatabaseDependency
from app.core.entity_service import EntityService
from app.core.identity import IdentityDependency

router = APIRouter(tags=["正規化データ: 買い物行"])


@router.put(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=ShoppingItemRow,
    responses={
        401: {"description": "認証が必要"},
        403: {"description": "操作・参照権限なし"},
        409: {"description": "同時更新またはDB業務制約違反"},
        422: {"description": "入力不正"},
        428: {"description": "If-Matchが必要"},
        503: {"description": "DB接続不可"},
    },
    status_code=200,
)
def handle(
    response: Response,
    identity: IdentityDependency,
    database: DatabaseDependency,
    row_id: UUID,
    payload: ShoppingItemWrite,
    if_match: Annotated[str | None, Header(alias="If-Match")] = None,
) -> ShoppingItemRow:
    """買い物行の更新。認証情報は依存から取得し、本人所有または管理者権限を検査する。"""
    result = execute(EntityService(database, identity), row_id, payload, if_match)
    response.headers["ETag"] = f'"{result.etag}"'
    return result
