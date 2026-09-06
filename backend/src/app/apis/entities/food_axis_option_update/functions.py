# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from app.core.entity_service import EntityService
from app.entities.models import FoodAxisOptionRow, FoodAxisOptionWrite
from app.entities.registry import SPECIFICATIONS


def execute(
    service: EntityService, row_id: UUID, payload: FoodAxisOptionWrite, if_match: str | None = None
) -> FoodAxisOptionRow:
    """食材の分類属性の更新を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_food_axis_option_update"],
        row_id=row_id,
        payload=payload.model_dump(mode="python", by_alias=True),
        if_match=if_match,
    )
    return FoodAxisOptionRow.model_validate(rows[0])
