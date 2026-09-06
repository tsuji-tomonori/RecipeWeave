from app.core.models import Recipe
from app.integrations.catalog.port import CatalogPort


def get_recipe(catalog: CatalogPort, recipe_id: str) -> Recipe | None:
    """Find a completed sample recipe, not a structural generation candidate."""
    return next((recipe for recipe in catalog.recipes() if recipe.id == recipe_id), None)
