---
title: "共通エラー応答の実装仕様"
---

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

実際の例外handlerと本文サイズ制限から生成する。OpenAPIにschemaがないエラーも実装で確認する。

## authentication_error

```python
async def authentication_error(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse({'detail': 'access token required or invalid'}, status_code=401, headers={'WWW-Authenticate': 'Bearer'})
```

## service_error

```python
async def service_error(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse({'detail': 'service unavailable'}, status_code=503)
```

## conflict_error

```python
async def conflict_error(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse({'detail': 'state version conflict'}, status_code=409)
```

## validation_error

```python
async def validation_error(_request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, RequestValidationError):
        raise exc
    errors = [{'loc': list(error['loc']), 'type': error['type']} for error in exc.errors()]
    return JSONResponse({'detail': errors}, status_code=422)
```

## 本文サイズ制限

```python
"""チャンク転送を含め、JSON解析前にリクエストのバイト数を制限する。"""

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class BodySizeLimit:
    def __init__(self, app: ASGIApp, max_bytes: int) -> None:
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or scope["method"] not in {"PUT", "POST", "PATCH"}:
            await self.app(scope, receive, send)
            return
        chunks: list[bytes] = []
        size = 0
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            body = message.get("body", b"")
            size += len(body)
            if size > self.max_bytes:
                await JSONResponse({"detail": "request too large"}, status_code=413)(
                    scope, receive, send
                )
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
```
