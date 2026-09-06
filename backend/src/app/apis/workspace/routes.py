"""登録済みの業務操作をアプリケーションへ追加する。"""

from importlib import import_module

from fastapi import FastAPI

OPERATIONS = [
    "get_workspace",
    "create_pantry_lot",
    "update_pantry_lot",
    "delete_pantry_lot",
    "add_menu_item",
    "update_menu_item",
    "delete_menu_item",
    "save_recipe",
    "unsave_recipe",
    "put_settings",
    "put_shopping_checks",
    "create_custom_food",
    "commit_receipt",
    "undo_receipt",
    "create_cooking_session",
    "update_cooking_session",
]


def register_workspace_routes(application: FastAPI) -> None:
    """固定した操作だけを登録する。"""
    for name in OPERATIONS:
        application.include_router(import_module(f"app.apis.workspace.{name}.router").router)
