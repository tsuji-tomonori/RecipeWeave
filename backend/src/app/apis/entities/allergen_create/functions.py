# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.entity_service import EntityService
from app.entities.models import AllergenRow, AllergenWrite
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, payload: AllergenWrite) -> AllergenRow:
    """アレルゲン概念の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_allergen_create"],
        payload=payload.model_dump(mode="python", by_alias=True),
    )
    return AllergenRow.model_validate(rows[0])
