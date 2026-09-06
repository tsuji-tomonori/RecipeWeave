"""Explicit test/local adapter. Never a fallback for a failed cloud database."""

from threading import Lock

from app.core.errors import StateConflictError
from app.core.models import AppSnapshot, StateEnvelope


class MemoryStateRepository:
    def __init__(self) -> None:
        self._states: dict[str, StateEnvelope] = {}
        self._lock = Lock()

    def get(self, subject: str) -> StateEnvelope:
        with self._lock:
            return self._states.get(subject, StateEnvelope(version=0, snapshot=None)).model_copy(
                deep=True
            )

    def put(self, subject: str, expected_version: int, snapshot: AppSnapshot) -> StateEnvelope:
        with self._lock:
            existing = self._states.get(subject, StateEnvelope(version=0, snapshot=None))
            if existing.version != expected_version:
                raise StateConflictError("state version conflict")
            result = StateEnvelope(
                version=expected_version + 1, snapshot=snapshot.model_copy(deep=True)
            )
            self._states[subject] = result
            return result.model_copy(deep=True)
