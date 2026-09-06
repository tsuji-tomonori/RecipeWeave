from app.core.models import AppSnapshot
from app.core.workspace_models import ReceiptRequest
from app.core.workspace_service import WorkspaceService


def execute(service: WorkspaceService, request: ReceiptRequest) -> AppSnapshot:
    """確認したレシートを在庫へ登録する。永続値は業務サービスが検証し、同一トランザクションで扱う。"""
    return service.commit_receipt(request)
