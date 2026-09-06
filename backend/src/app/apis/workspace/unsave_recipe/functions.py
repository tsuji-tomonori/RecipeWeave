from uuid import UUID

from app.core.models import AppSnapshot
from app.core.workspace_models import RevisionRequest
from app.core.workspace_service import WorkspaceService


def execute(service: WorkspaceService, request: RevisionRequest, row_id: UUID) -> AppSnapshot:
    """料理の保存を解除する。永続値は業務サービスが検証し、同一トランザクションで扱う。"""
    return service.unsave_recipe(request, row_id)
