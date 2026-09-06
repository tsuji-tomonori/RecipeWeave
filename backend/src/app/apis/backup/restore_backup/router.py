from fastapi import APIRouter

from app.apis.backup.restore_backup.contract import CONTRACT
from app.apis.backup.restore_backup.functions import execute
from app.apis.backup.restore_backup.schemas import AppSnapshot, BackupRestoreRequest
from app.core.backup_service import BackupService
from app.core.db import DatabaseDependency
from app.core.identity import IdentityDependency

router = APIRouter(tags=["バックアップ"])


@router.post(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=AppSnapshot,
    responses={
        code: {"description": "本人・形式・版・確認・DB制約の検証失敗"} for code in CONTRACT.errors
    },
)
def handle(
    identity: IdentityDependency, database: DatabaseDependency, request: BackupRestoreRequest
) -> AppSnapshot:
    """確認したバックアップで本人のデータを全置換する。利用者の確認がない全置換を受け付けない。"""
    return execute(BackupService(database, identity), request)
