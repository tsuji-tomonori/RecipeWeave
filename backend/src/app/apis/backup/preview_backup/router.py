from fastapi import APIRouter

from app.apis.backup.preview_backup.contract import CONTRACT
from app.apis.backup.preview_backup.functions import execute
from app.apis.backup.preview_backup.schemas import BackupPreview, BackupPreviewRequest
from app.core.backup_service import BackupService
from app.core.db import DatabaseDependency
from app.core.identity import IdentityDependency

router = APIRouter(tags=["バックアップ"])


@router.post(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=BackupPreview,
    responses={
        code: {"description": "本人・形式・版・確認・DB制約の検証失敗"} for code in CONTRACT.errors
    },
)
def handle(
    identity: IdentityDependency, database: DatabaseDependency, request: BackupPreviewRequest
) -> BackupPreview:
    """バックアップの全置換内容を検証する。利用者の確認がない全置換を受け付けない。"""
    return execute(BackupService(database, identity), request)
