"""Versioned state storage is independent of identity verification and HTTP."""

from typing import Protocol

from app.core.models import AppSnapshot, StateEnvelope


class StateRepository(Protocol):
    def get(self, subject: str) -> StateEnvelope: ...

    def put(self, subject: str, expected_version: int, snapshot: AppSnapshot) -> StateEnvelope: ...
