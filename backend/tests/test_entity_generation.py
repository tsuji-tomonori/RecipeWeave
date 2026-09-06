"""生成リース操作の認可、フェンス値、失効時の応答を検証する。"""

from typing import Literal
from unittest.mock import MagicMock, patch
from uuid import UUID

import pytest
from fastapi import HTTPException

from app.core.entity_generation import run_lease_operation
from app.core.entity_service import EntityService
from app.core.identity import Identity

OPERATIONS: list[Literal["claim_shard", "renew_shard", "advance_shard"]] = [
    "claim_shard",
    "renew_shard",
    "advance_shard",
]


@pytest.mark.parametrize("operation", OPERATIONS)
def test_generation_lease_requires_admin(
    operation: Literal["claim_shard", "renew_shard", "advance_shard"],
) -> None:
    """Given一般利用者 Whenリース操作 ThenSQL前に403。"""
    service = EntityService(MagicMock(), Identity("user", UUID(int=1), "user"))
    with pytest.raises(HTTPException) as raised:
        run_lease_operation(service, operation, {})
    assert raised.value.status_code == 403


@pytest.mark.parametrize("operation", OPERATIONS)
def test_expired_or_superseded_lease_is_conflict(
    operation: Literal["claim_shard", "renew_shard", "advance_shard"],
) -> None:
    """Given有効フェンスに一致する行なし When更新 Then409で旧ワーカーを拒否。"""
    service = EntityService(MagicMock(), Identity("worker", UUID(int=1), "admin"))
    with patch("app.core.entity_generation.OperationQueries") as queries:
        queries.return_value.run.return_value = []
        with pytest.raises(HTTPException) as raised:
            run_lease_operation(
                service, operation, {"expected_fence": "9007199254740993", "lease_owner": "forged"}
            )
        assert raised.value.status_code == 409
        params = queries.return_value.run.call_args.kwargs
        assert params["expected_fence"] == 9007199254740993
        assert params["lease_owner"] == "worker"
