from app.core.models import AppSnapshot
from app.core.workspace_models import ShoppingRequest
from app.core.workspace_service import WorkspaceService


def execute(service: WorkspaceService, request: ShoppingRequest) -> AppSnapshot:
    """買い物の確認状況を保存する。永続値は業務サービスが検証し、同一トランザクションで扱う。"""
    return service.put_shopping_checks(request)
