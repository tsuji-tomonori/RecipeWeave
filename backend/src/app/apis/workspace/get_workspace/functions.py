from app.core.models import AppSnapshot
from app.core.workspace_service import WorkspaceService


def execute(service: WorkspaceService) -> AppSnapshot:
    """ワークスペースを取得する。永続値は業務サービスが検証し、同一トランザクションで扱う。"""
    return service.get_workspace()
