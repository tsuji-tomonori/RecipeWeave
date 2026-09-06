"""生成範囲のリース取得をリースの競合制約とともに実行する。"""

from app.core.entity_generation import run_lease_operation
from app.core.entity_service import EntityService

from .schemas import GenerationShardRow, Request


def execute(payload: Request, service: EntityService) -> GenerationShardRow:
    """生成範囲のリース取得の値を検証済み主体と固定SQLへ渡す。"""
    values = payload.model_dump(mode="python")
    return run_lease_operation(service, "claim_shard", values)
