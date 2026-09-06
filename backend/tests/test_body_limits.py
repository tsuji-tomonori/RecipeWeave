"""バックアップ以外の上限を維持し、分割送信でも容量制限を適用する。"""

import asyncio
from typing import Any

import pytest
from starlette.types import Message, Receive, Scope, Send

from app.core.middleware import BodySizeLimit


@pytest.mark.parametrize(
    ("path", "method", "size", "expected"),
    [
        ("/api/backups/restore", "POST", 1800, 204),
        ("/api/backups/restore", "POST", 2100, 413),
        ("/api/backups/restore/extra", "POST", 1800, 413),
        ("/api/backups/restore", "PUT", 1800, 413),
        ("/api/workspace", "POST", 1800, 413),
    ],
)
def test_backup_limit_is_exact_and_counts_chunks(
    path: str, method: str, size: int, expected: int
) -> None:
    """前提:操作別上限 / 操作:複数チャンク送信 / 期待:正確なPOST経路だけ拡大する。"""
    responses: list[Message] = []
    received: list[int] = []
    parts = iter(
        [
            {"type": "http.request", "body": b"x" * 900, "more_body": True},
            {"type": "http.request", "body": b"x" * (size - 900), "more_body": False},
        ]
    )

    async def receive() -> Message:
        return next(parts)

    async def send(message: Message) -> None:
        responses.append(message)

    async def endpoint(_scope: Scope, source: Receive, target: Send) -> None:
        message = await source()
        received.append(len(message["body"]))
        await target({"type": "http.response.start", "status": 204, "headers": []})
        await target({"type": "http.response.body", "body": b""})

    target = BodySizeLimit(endpoint, 1024, {"/api/backups/restore": 2048})
    scope: dict[str, Any] = {"type": "http", "method": method, "path": path}
    asyncio.run(target(scope, receive, send))
    assert responses[0]["status"] == expected
    assert received == ([size] if expected == 204 else [])
