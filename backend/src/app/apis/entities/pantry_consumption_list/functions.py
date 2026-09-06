# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from app.core.entity_service import EntityService
from app.entities.models import PantryConsumptionRow
from app.entities.registry import SPECIFICATIONS


def execute(
    service: EntityService, limit: int = 50, after: UUID | None = None
) -> list[PantryConsumptionRow]:
    """調理による在庫消費の冪等台帳の一覧を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_pantry_consumption_list"], limit=limit, after=after
    )
    return [PantryConsumptionRow.model_validate(row) for row in rows]
