# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.entity_service import EntityService
from app.entities.models import MenuItemRow, MenuItemWrite
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, payload: MenuItemWrite) -> MenuItemRow:
    """献立の料理の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_menu_item_create"],
        payload=payload.model_dump(mode="python", by_alias=True),
    )
    return MenuItemRow.model_validate(rows[0])
