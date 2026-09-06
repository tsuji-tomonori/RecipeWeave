from uuid import UUID

from app.core.models import Recipe
from app.integrations.catalog.port import CatalogPort


def get_recipe(
    catalog: CatalogPort,
    recipe_id: UUID,
    preview: bool = False,
    version_id: UUID | None = None,
    owner_id: UUID | None = None,
) -> Recipe | None:
    """実体テーブルに保存された版の材料・工程を取得する。"""
    items, _ = catalog.recipes(
        operation="get_recipe",
        recipe_id=recipe_id,
        preview=preview,
        limit=1,
        version_id=version_id,
        owner_id=owner_id,
    )
    return items[0] if items else None
