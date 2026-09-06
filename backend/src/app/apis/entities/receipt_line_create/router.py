# generate_entity_apis.py による自動生成。直接編集しない。
from fastapi import APIRouter, Response

from app.apis.entities.receipt_line_create.contract import CONTRACT
from app.apis.entities.receipt_line_create.functions import execute
from app.apis.entities.receipt_line_create.schemas import ReceiptLineRow, ReceiptLineWrite
from app.core.db import DatabaseDependency
from app.core.entity_service import EntityService
from app.core.identity import IdentityDependency

router = APIRouter(tags=["正規化データ: レシートの商品候補と確定した在庫の対応"])


@router.post(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=ReceiptLineRow,
    responses={
        401: {"description": "認証が必要"},
        403: {"description": "操作・参照権限なし"},
        409: {"description": "同時更新またはDB業務制約違反"},
        422: {"description": "入力不正"},
        503: {"description": "DB接続不可"},
    },
    status_code=201,
)
def handle(
    response: Response,
    identity: IdentityDependency,
    database: DatabaseDependency,
    payload: ReceiptLineWrite,
) -> ReceiptLineRow:
    """レシートの商品候補と確定した在庫の対応の作成。認証情報は依存から取得し、本人所有または管理者権限を検査する。"""
    result = execute(EntityService(database, identity), payload)
    response.headers["ETag"] = f'"{result.etag}"'
    return result
