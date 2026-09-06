from app.core.backup_contracts import BackupPreview, BackupPreviewRequest
from app.core.backup_service import BackupService


def execute(service: BackupService, request: BackupPreviewRequest) -> BackupPreview:
    """バックアップの全置換内容を検証する。認証済み本人と固定SQLを使う。"""
    return service.preview_backup(request)
