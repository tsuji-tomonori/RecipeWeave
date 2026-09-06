"""チャンク転送を含め、JSON解析前にリクエストのバイト数を制限する。"""

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class BodySizeLimit:
    def __init__(
        self, app: ASGIApp, max_bytes: int, path_limits: dict[str, int] | None = None
    ) -> None:
        self.app = app
        self.max_bytes = max_bytes
        self.path_limits = dict(path_limits or {})

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or scope["method"] not in {"PUT", "POST", "PATCH"}:
            await self.app(scope, receive, send)
            return
        limit = (
            self.path_limits.get(scope["path"], self.max_bytes)
            if scope["method"] == "POST"
            else self.max_bytes
        )
        chunks: list[bytes] = []
        size = 0
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            body = message.get("body", b"")
            size += len(body)
            if size > limit:
                await JSONResponse(
                    {"detail": "送信データの容量が上限を超えています"}, status_code=413
                )(scope, receive, send)
                return
            chunks.append(body)
            if not message.get("more_body", False):
                break
        consumed = False

        async def bounded_receive() -> Message:
            nonlocal consumed
            if consumed:
                return await receive()
            consumed = True
            return {"type": "http.request", "body": b"".join(chunks), "more_body": False}

        await self.app(scope, bounded_receive, send)
