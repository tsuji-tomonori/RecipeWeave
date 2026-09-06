"""生成範囲の進捗確定をリースの競合制約とともに実行する。"""

from uuid import UUID

from app.core.entity_generation import run_lease_operation
from app.core.entity_service import EntityService

from .schemas import GenerationShardRow, Request


def execute(payload: Request, service: EntityService, row_id: UUID) -> GenerationShardRow:
    """生成範囲の進捗確定の値を検証済み主体と固定SQLへ渡す。"""
    values = payload.model_dump(mode="python")
    values["row_id"] = row_id
    return run_lease_operation(service, "advance_shard", values)
