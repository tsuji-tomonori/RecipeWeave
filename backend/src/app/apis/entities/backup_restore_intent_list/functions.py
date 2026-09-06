# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from app.core.entity_service import EntityService
from app.entities.models import BackupRestoreIntentRow
from app.entities.registry import SPECIFICATIONS


def execute(
    service: EntityService, limit: int = 50, after: UUID | None = None
) -> list[BackupRestoreIntentRow]:
    """復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度だけ消費するの一覧を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_backup_restore_intent_list"], limit=limit, after=after
    )
    return [BackupRestoreIntentRow.model_validate(row) for row in rows]
