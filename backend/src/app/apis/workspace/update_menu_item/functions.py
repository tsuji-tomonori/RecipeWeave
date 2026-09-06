from uuid import UUID

from app.core.models import AppSnapshot
from app.core.workspace_models import MenuItemRequest
from app.core.workspace_service import WorkspaceService


def execute(service: WorkspaceService, request: MenuItemRequest, row_id: UUID) -> AppSnapshot:
    """献立の人数・分量を変更する。永続値は業務サービスが検証し、同一トランザクションで扱う。"""
    return service.update_menu_item(request, row_id)
