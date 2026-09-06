# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from app.core.entity_service import EntityService
from app.entities.models import GenerationChoiceRow
from app.entities.registry import SPECIFICATIONS


def execute(
    service: EntityService, limit: int = 50, after: UUID | None = None
) -> list[GenerationChoiceRow]:
    """生成軸の選択値の一覧を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_generation_choice_list"], limit=limit, after=after
    )
    return [GenerationChoiceRow.model_validate(row) for row in rows]
