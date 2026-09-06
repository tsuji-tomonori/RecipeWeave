from app.core.models import Recipe
from app.integrations.catalog.port import CatalogPort


def get_recipe(catalog: CatalogPort, recipe_id: str) -> Recipe | None:
    """料理として完成したサンプルを取得する。構造だけの生成候補は対象にしない。"""
    return next((recipe for recipe in catalog.recipes() if recipe.id == recipe_id), None)
