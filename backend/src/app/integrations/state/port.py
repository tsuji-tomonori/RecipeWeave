"""版を管理する状態保存を、本人確認とHTTP処理から分離する。"""

from typing import Protocol

from app.core.models import AppSnapshot, StateEnvelope


class StateRepository(Protocol):
    def get(self, subject: str) -> StateEnvelope: ...

    def put(self, subject: str, expected_version: int, snapshot: AppSnapshot) -> StateEnvelope: ...
