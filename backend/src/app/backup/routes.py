"""確認付きバックアップの固定3操作を登録する。"""

from fastapi import FastAPI

from app.apis.backup.export_backup.router import router as export_router
from app.apis.backup.preview_backup.router import router as preview_router
from app.apis.backup.restore_backup.router import router as restore_router


def register_backup_routes(application: FastAPI) -> None:
    """発行・検証・復元を別の操作として公開する。"""
    application.include_router(export_router)
    application.include_router(preview_router)
    application.include_router(restore_router)
