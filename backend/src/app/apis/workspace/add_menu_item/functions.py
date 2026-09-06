from app.core.models import AppSnapshot
from app.core.workspace_models import MenuItemRequest
from app.core.workspace_service import WorkspaceService


def execute(service: WorkspaceService, request: MenuItemRequest) -> AppSnapshot:
    """献立へ料理を加える。永続値は業務サービスが検証し、同一トランザクションで扱う。"""
    return service.add_menu_item(request)
