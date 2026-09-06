from uuid import UUID

from app.core.models import AppSnapshot
from app.core.workspace_models import UpdatePantryRequest
from app.core.workspace_service import WorkspaceService


def execute(service: WorkspaceService, request: UpdatePantryRequest, row_id: UUID) -> AppSnapshot:
    """手持ち食材を修正・復元する。永続値は業務サービスが検証し、同一トランザクションで扱う。"""
    return service.update_pantry_lot(request, row_id)
