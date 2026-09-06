from app.core.models import AppSnapshot
from app.core.workspace_models import SettingsRequest
from app.core.workspace_service import WorkspaceService


def execute(service: WorkspaceService, request: SettingsRequest) -> AppSnapshot:
    """好み・常備食材・器具を設定する。永続値は業務サービスが検証し、同一トランザクションで扱う。"""
    return service.put_settings(request)
