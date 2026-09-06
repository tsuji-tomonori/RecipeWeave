"""Composition root; provider clients are constructed only in dependencies."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.apis.foods.list_foods.router import router as list_foods_router
from app.apis.health.get_health.router import router as health_router
from app.apis.recipes.get_recipe.router import router as get_recipe_router
from app.apis.recipes.list_recipes.router import router as list_recipes_router
from app.apis.state.get_state.router import router as get_state_router
from app.apis.state.put_state.router import router as put_state_router
from app.core.dependencies import get_settings
from app.core.errors import AuthenticationError, ServiceUnavailableError, StateConflictError
from app.core.middleware import BodySizeLimit


async def authentication_error(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(
        {"detail": "access token required or invalid"},
        status_code=401,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def service_error(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse({"detail": "service unavailable"}, status_code=503)


async def conflict_error(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse({"detail": "state version conflict"}, status_code=409)


async def validation_error(_request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, RequestValidationError):
        raise exc
    # Pydantic's default error includes input values; never echo personal state or tokens.
    errors = [{"loc": list(error["loc"]), "type": error["type"]} for error in exc.errors()]
    return JSONResponse({"detail": errors}, status_code=422)


def create_app() -> FastAPI:
    """Create the API with explicit operations and fail-closed personal state."""
    settings = get_settings()
    application = FastAPI(
        title="RecipeWeave API",
        version="0.1.0",
        description="Sample recipes and authenticated device-state migration boundary.",
    )
    application.add_middleware(BodySizeLimit, max_bytes=settings.max_request_bytes)
    origins = [origin.strip() for origin in settings.allowed_origins.split(",") if origin.strip()]
    if origins:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_methods=["GET", "PUT"],
            allow_headers=["Authorization", "Content-Type"],
            allow_credentials=False,
        )
    application.include_router(health_router)
    application.include_router(list_foods_router)
    application.include_router(list_recipes_router)
    application.include_router(get_recipe_router)
    application.include_router(get_state_router)
    application.include_router(put_state_router)

    application.add_exception_handler(AuthenticationError, authentication_error)
    application.add_exception_handler(ServiceUnavailableError, service_error)
    application.add_exception_handler(StateConflictError, conflict_error)
    application.add_exception_handler(RequestValidationError, validation_error)

    return application


app = create_app()
