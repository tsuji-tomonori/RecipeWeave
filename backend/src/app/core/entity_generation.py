"""列挙ジョブのリースを取得し、古いワーカーによる進捗上書きを防ぐ。"""

import logging
from dataclasses import replace
from typing import Any, Literal

from fastapi import HTTPException

from app.core.entity_service import EntityService
from app.core.operation_queries import OperationQueries
from app.entities.models import GenerationShardRow
from app.entities.registry import SPECIFICATIONS

logger = logging.getLogger(__name__)


def run_lease_operation(
    service: EntityService,
    operation: Literal["claim_shard", "renew_shard", "advance_shard"],
    values: dict[str, Any],
) -> GenerationShardRow:
    """検証済みワーカーだけがリースを取得・更新でき、失効・交代後は409にする。"""
    if service.identity.role != "admin":
        raise HTTPException(status_code=403, detail="生成運用権限が必要です")
    params = {**values, "lease_owner": service.identity.subject}
    for name in ("expected_fence", "next_ordinal"):
        if name in params:
            params[name] = int(params[name])
    with service.connection.transaction():
        rows = OperationQueries(service.connection, "generation/" + operation).run(
            "q001_execute", **params
        )
        if not rows:
            raise HTTPException(status_code=409, detail="取得対象がないか、リースが失効しました")
        row = rows[0]
        for name in ("start_ordinal", "end_ordinal", "next_ordinal", "fence_token"):
            row[name] = str(row[name])
        spec = replace(
            SPECIFICATIONS["entity_generation_shard_create"],
            operation_id=operation,
            action="update",
        )
        service.record_change(spec, row["id"])
        logger.info("generation_lease_updated", extra={"operation_id": operation})
        return GenerationShardRow.model_validate(row)
