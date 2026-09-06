"""Manual API identity and behavior metadata."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationContract:
    operation_id: str
    slug: str
    method: str
    path: str
    summary: str
    authentication: str
    errors: tuple[int, ...]
    idempotency: str
    transaction: str
    effects: str
