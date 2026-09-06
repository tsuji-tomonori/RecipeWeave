from app.core.models import AppSnapshot
from app.core.workspace_models import CreatePantryRequest
from app.core.workspace_service import WorkspaceService


def execute(service: WorkspaceService, request: CreatePantryRequest) -> AppSnapshot:
    """手持ち食材を登録する。永続値は業務サービスが検証し、同一トランザクションで扱う。"""
    return service.create_pantry_lot(request)
