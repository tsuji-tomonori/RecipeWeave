# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from app.core.entity_service import EntityService
from app.entities.models import StepParameterRow
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, row_id: UUID) -> StepParameterRow:
    """工程の型付きパラメータの取得を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(SPECIFICATIONS["entity_step_parameter_get"], row_id=row_id)
    return StepParameterRow.model_validate(rows[0])
