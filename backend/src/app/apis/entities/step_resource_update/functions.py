# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from app.core.entity_service import EntityService
from app.entities.models import StepResourceRow, StepResourceWrite
from app.entities.registry import SPECIFICATIONS


def execute(
    service: EntityService, row_id: UUID, payload: StepResourceWrite, if_match: str | None = None
) -> StepResourceRow:
    """工程の資源要求の更新を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_step_resource_update"],
        row_id=row_id,
        payload=payload.model_dump(mode="python", by_alias=True),
        if_match=if_match,
    )
    return StepResourceRow.model_validate(rows[0])
