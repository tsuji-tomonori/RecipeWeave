# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from app.core.entity_service import EntityService
from app.entities.models import ProductAllergenRow
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, row_id: UUID) -> ProductAllergenRow:
    """商品表示アレルゲンの取得を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(SPECIFICATIONS["entity_product_allergen_get"], row_id=row_id)
    return ProductAllergenRow.model_validate(rows[0])
