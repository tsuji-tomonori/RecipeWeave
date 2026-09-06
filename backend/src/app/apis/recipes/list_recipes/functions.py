import unicodedata

from app.core.models import Food, Recipe
from app.integrations.catalog.port import CatalogPort

from .schemas import RecipeSearch, RecipesResponse


def has_matching_ingredients(recipe: Recipe, search: RecipeSearch) -> bool:
    """Apply all/any selected ingredients; portion count is deliberately absent."""
    present = {item.food_id for item in recipe.ingredients}
    selected = set(search.selected_food_ids)
    return not selected or (
        selected <= present if search.match == "all" else bool(selected & present)
    )


def has_excluded_food(recipe: Recipe, excluded: set[str], foods: dict[str, Food]) -> bool:
    """Exclude composite foods with a known excluded component; not an allergy guarantee."""
    pending = [item.food_id for item in recipe.ingredients]
    visited: set[str] = set()
    while pending:
        food_id = pending.pop()
        if food_id in excluded:
            return True
        if food_id in visited:
            continue
        visited.add(food_id)
        food = foods.get(food_id)
        if food is not None:
            pending.extend(food.component_food_ids)
    return False


def list_recipes(catalog: CatalogPort, search: RecipeSearch) -> RecipesResponse:
    """Search the bounded sample collection without inflating recipe counts."""
    foods = {food.id: food for food in catalog.foods()}
    query = unicodedata.normalize("NFKC", search.q).casefold().strip()
    items: list[Recipe] = []
    for recipe in catalog.recipes():
        text = unicodedata.normalize("NFKC", recipe.name + recipe.description).casefold()
        if query and query not in text:
            continue
        if not has_matching_ingredients(recipe, search):
            continue
        if has_excluded_food(recipe, set(search.excluded_food_ids), foods):
            continue
        if search.max_minutes is not None and recipe.minutes > search.max_minutes:
            continue
        if search.equipment and not set(recipe.equipment) <= set(search.equipment):
            continue
        items.append(recipe)
    return RecipesResponse(items=items, total=len(items))
