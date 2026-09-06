# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.entity_service import EntityService
from app.entities.models import FoodAxisOptionRow, FoodAxisOptionWrite
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, payload: FoodAxisOptionWrite) -> FoodAxisOptionRow:
    """食材の分類属性の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_food_axis_option_create"],
        payload=payload.model_dump(mode="python", by_alias=True),
    )
    return FoodAxisOptionRow.model_validate(rows[0])
