from app.core.backup_contracts import BackupRestoreRequest
from app.core.backup_service import BackupService
from app.core.models import AppSnapshot


def execute(service: BackupService, request: BackupRestoreRequest) -> AppSnapshot:
    """確認したバックアップで本人のデータを全置換する。認証済み本人と固定SQLを使う。"""
    return service.restore_backup(request)
