from app.core.models import AppSnapshot
from app.core.workspace_models import CookingRequest
from app.core.workspace_service import WorkspaceService


def execute(service: WorkspaceService, request: CookingRequest) -> AppSnapshot:
    """調理計画を確定して開始する。永続値は業務サービスが検証し、同一トランザクションで扱う。"""
    return service.create_cooking_session(request)
