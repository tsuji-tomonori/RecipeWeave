# 共通エラー応答の実装仕様

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

実際の例外handlerと本文サイズ制限から生成する。OpenAPIにschemaがないエラーも実装で確認する。

## authentication_error

```python
async def authentication_error(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse({'detail': 'ログインが必要か、アクセストークンが無効です'}, status_code=401, headers={'WWW-Authenticate': 'Bearer'})
```

## service_error

```python
async def service_error(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse({'detail': 'サービスへ接続できません。時間をおいて再試行してください'}, status_code=503)
```

## conflict_error

```python
async def conflict_error(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse({'detail': '他の画面で更新されています。最新の内容を読み込んでください'}, status_code=409)
```

## database_constraint_error

```python
async def database_constraint_error(_request: Request, _exc: Exception) -> JSONResponse:
    """制約名・SQL・個人データを外部へ返さず、処理の不成立を伝える。"""
    return JSONResponse({'detail': '参照・数量・更新状態の制約により保存できません'}, status_code=409)
```

## database_permission_error

```python
async def database_permission_error(_request: Request, _exc: Exception) -> JSONResponse:
    """DBの行権限違反を、情報を追加せず拒否する。"""
    return JSONResponse({'detail': 'このデータを操作する権限がありません'}, status_code=403)
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
