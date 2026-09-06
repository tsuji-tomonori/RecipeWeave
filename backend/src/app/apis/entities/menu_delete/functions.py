# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from app.core.entity_service import EntityService
from app.entities.models import MenuRow
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, row_id: UUID, if_match: str | None = None) -> MenuRow:
    """献立の削除を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(SPECIFICATIONS["entity_menu_delete"], row_id=row_id, if_match=if_match)
    return MenuRow.model_validate(rows[0])
