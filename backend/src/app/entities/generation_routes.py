"""生成運用の固定ルートを登録する。"""

from fastapi import FastAPI

from app.apis.generation.advance_shard.router import router as advance
from app.apis.generation.claim_shard.router import router as claim
from app.apis.generation.renew_shard.router import router as renew


def register_generation_routes(application: FastAPI) -> None:
    application.include_router(claim)
    application.include_router(renew)
    application.include_router(advance)
