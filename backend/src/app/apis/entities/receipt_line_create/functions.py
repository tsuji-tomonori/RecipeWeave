# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.entity_service import EntityService
from app.entities.models import ReceiptLineRow, ReceiptLineWrite
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, payload: ReceiptLineWrite) -> ReceiptLineRow:
    """レシートの商品候補と確定した在庫の対応の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_receipt_line_create"],
        payload=payload.model_dump(mode="python", by_alias=True),
    )
    return ReceiptLineRow.model_validate(rows[0])
