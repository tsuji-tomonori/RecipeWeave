from app.core.models import AppSnapshot
from app.core.workspace_models import CustomFoodRequest
from app.core.workspace_service import WorkspaceService


def execute(service: WorkspaceService, request: CustomFoodRequest) -> AppSnapshot:
    """本人の独自食材を登録する。永続値は業務サービスが検証し、同一トランザクションで扱う。"""
    return service.create_custom_food(request)
