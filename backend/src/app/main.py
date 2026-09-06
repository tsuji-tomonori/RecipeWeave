"""アプリケーションの構成起点。外部クライアントは依存の構築時だけ生成する。"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from psycopg import errors

from app.apis.auth.get_me.router import router as me_router
from app.apis.auth.local_login.router import router as local_login_router
from app.apis.foods.list_foods.router import router as list_foods_router
from app.apis.health.get_health.router import router as health_router
from app.apis.recipes.get_recipe.router import router as get_recipe_router
from app.apis.recipes.list_recipes.router import router as list_recipes_router
from app.apis.recipes.random_recipe.router import router as random_recipe_router
from app.apis.workspace.routes import register_workspace_routes
from app.core.dependencies import get_settings
from app.core.errors import AuthenticationError, ServiceUnavailableError, StateConflictError
from app.core.middleware import BodySizeLimit
from app.entities.routes import register_entity_routes


async def authentication_error(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(
        {"detail": "ログインが必要か、アクセストークンが無効です"},
        status_code=401,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def service_error(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(
        {"detail": "サービスへ接続できません。時間をおいて再試行してください"}, status_code=503
    )


async def conflict_error(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(
        {"detail": "他の画面で更新されています。最新の内容を読み込んでください"}, status_code=409
    )


async def database_constraint_error(_request: Request, _exc: Exception) -> JSONResponse:
    """制約名・SQL・個人データを外部へ返さず、処理の不成立を伝える。"""
    return JSONResponse(
        {"detail": "参照・数量・更新状態の制約により保存できません"}, status_code=409
    )


async def database_permission_error(_request: Request, _exc: Exception) -> JSONResponse:
    """DBの行権限違反を、情報を追加せず拒否する。"""
    return JSONResponse({"detail": "このデータを操作する権限がありません"}, status_code=403)


async def validation_error(_request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, RequestValidationError):
        raise exc
    # Pydanticの既定エラーには入力値が含まれるため、個人データやトークンを返さない。
    errors = [{"loc": list(error["loc"]), "type": error["type"]} for error in exc.errors()]
    return JSONResponse({"detail": errors}, status_code=422)


def create_app() -> FastAPI:
    """操作を明示してAPIを構築し、個人状態の認証・設定不足時は処理を拒否する。"""
    settings = get_settings()
    application = FastAPI(
        title="RecipeWeave API",
        version="0.2.0",
        description="食品・料理・工程・利用者操作を正規化したPostgreSQLから提供するAPI。",
    )
    application.add_middleware(BodySizeLimit, max_bytes=settings.max_request_bytes)
    origins = [origin.strip() for origin in settings.allowed_origins.split(",") if origin.strip()]
    if origins:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_methods=["GET", "PUT", "POST", "PATCH", "DELETE"],
            allow_headers=["Authorization", "Content-Type", "If-Match"],
            expose_headers=["ETag"],
            allow_credentials=False,
        )
    application.include_router(health_router)
    application.include_router(list_foods_router)
    application.include_router(list_recipes_router)
    application.include_router(random_recipe_router)
    application.include_router(get_recipe_router)
    application.include_router(local_login_router)
    application.include_router(me_router)
    register_workspace_routes(application)
    register_entity_routes(application)

    application.add_exception_handler(AuthenticationError, authentication_error)
    application.add_exception_handler(ServiceUnavailableError, service_error)
    application.add_exception_handler(StateConflictError, conflict_error)
    application.add_exception_handler(RequestValidationError, validation_error)
    application.add_exception_handler(errors.IntegrityError, database_constraint_error)
    application.add_exception_handler(errors.SerializationFailure, conflict_error)
    application.add_exception_handler(errors.InsufficientPrivilege, database_permission_error)

    return application


app = create_app()
