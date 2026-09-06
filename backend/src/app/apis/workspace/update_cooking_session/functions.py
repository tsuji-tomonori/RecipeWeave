from uuid import UUID

from app.core.models import AppSnapshot
from app.core.workspace_models import CookingRequest
from app.core.workspace_service import WorkspaceService


def execute(service: WorkspaceService, request: CookingRequest, row_id: UUID) -> AppSnapshot:
    """工程・タイマー・調理完了を記録する。永続値は業務サービスが検証し、同一トランザクションで扱う。"""
    return service.update_cooking_session(request, row_id)
