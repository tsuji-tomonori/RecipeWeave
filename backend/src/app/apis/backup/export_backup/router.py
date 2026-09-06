from fastapi import APIRouter

from app.apis.backup.export_backup.contract import CONTRACT
from app.apis.backup.export_backup.functions import execute
from app.apis.backup.export_backup.schemas import BackupDocument
from app.core.backup_service import BackupService
from app.core.db import DatabaseDependency
from app.core.identity import IdentityDependency

router = APIRouter(tags=["バックアップ"])


@router.post(
    CONTRACT.path,
    operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary,
    response_model=BackupDocument,
    responses={
        code: {"description": "本人・形式・版・確認・DB制約の検証失敗"} for code in CONTRACT.errors
    },
)
def handle(identity: IdentityDependency, database: DatabaseDependency) -> BackupDocument:
    """本人の現在データを書き出し、発行した本文の根拠だけを記録する。"""
    return execute(BackupService(database, identity))
