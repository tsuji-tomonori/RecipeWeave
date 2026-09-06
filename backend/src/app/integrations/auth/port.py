"""Only a verified identity may address personal state."""

from typing import Protocol


class IdentityVerifier(Protocol):
    def subject(self, token: str) -> str: ...
