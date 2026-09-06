"""本人確認済みの識別子だけで個人状態へアクセスする。"""

from typing import Protocol


class IdentityVerifier(Protocol):
    def subject(self, token: str) -> str: ...
