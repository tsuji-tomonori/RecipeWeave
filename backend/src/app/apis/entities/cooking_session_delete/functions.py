# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from app.core.entity_service import EntityService
from app.entities.models import CookingSessionRow
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, row_id: UUID, if_match: str | None = None) -> CookingSessionRow:
    """調理計画実行の削除を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_cooking_session_delete"], row_id=row_id, if_match=if_match
    )
    return CookingSessionRow.model_validate(rows[0])
