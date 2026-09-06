from concurrent.futures import ThreadPoolExecutor

import pytest
from pydantic import ValidationError

from app.core.errors import StateConflictError
from app.core.models import AppSnapshot
from app.integrations.state.memory_provider import MemoryStateRepository


def test_parallel_first_writes_have_one_winner(snapshot: AppSnapshot) -> None:
    repository = MemoryStateRepository()

    def write(_attempt: int) -> bool:
        try:
            repository.put("same-user", 0, snapshot)
            return True
        except StateConflictError:
            return False

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(write, range(4)))
    assert sum(results) == 1
    assert repository.get("same-user").version == 1


def test_read_copies_do_not_mutate_persisted_state(snapshot: AppSnapshot) -> None:
    repository = MemoryStateRepository()
    repository.put("user-a", 0, snapshot)
    read = repository.get("user-a")
    assert read.snapshot is not None
    read.snapshot.saved.append("changed-without-put")
    original = repository.get("user-a")
    assert original.snapshot is not None
    assert original.snapshot.saved == []


def test_bad_snapshot_types_and_schema_are_rejected(snapshot: AppSnapshot) -> None:
    body = snapshot.model_dump(by_alias=True)
    body["schemaVersion"] = 99
    with pytest.raises(ValidationError):
        AppSnapshot.model_validate(body)
    body["schemaVersion"] = 1
    body["lots"] = ["not a stock lot"]
    with pytest.raises(ValidationError):
        AppSnapshot.model_validate(body)
