# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from app.core.entity_service import EntityService
from app.entities.models import ResourceTypeRow
from app.entities.registry import SPECIFICATIONS


def execute(
    service: EntityService, limit: int = 50, after: UUID | None = None
) -> list[ResourceTypeRow]:
    """道具・設備・作業者種別の一覧を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(SPECIFICATIONS["entity_resource_type_list"], limit=limit, after=after)
    return [ResourceTypeRow.model_validate(row) for row in rows]
