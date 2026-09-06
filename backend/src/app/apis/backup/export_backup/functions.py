from app.core.backup_contracts import BackupDocument
from app.core.backup_service import BackupService


def execute(service: BackupService) -> BackupDocument:
    """バックアップを書き出す。認証済み本人と固定SQLを使う。"""
    return service.export_backup()
