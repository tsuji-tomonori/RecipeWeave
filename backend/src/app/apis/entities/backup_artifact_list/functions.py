# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from app.core.entity_service import EntityService
from app.entities.models import BackupArtifactRow
from app.entities.registry import SPECIFICATIONS


def execute(
    service: EntityService, limit: int = 50, after: UUID | None = None
) -> list[BackupArtifactRow]:
    """本人へ発行したバックアップの証拠。本文を保存せず、削除後も匿名化した発行記録を保持するの一覧を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(SPECIFICATIONS["entity_backup_artifact_list"], limit=limit, after=after)
    return [BackupArtifactRow.model_validate(row) for row in rows]
