import unicodedata

from app.integrations.catalog.port import CatalogPort

from .schemas import RecipeSearch, RecipesResponse


def list_recipes(catalog: CatalogPort, search: RecipeSearch) -> RecipesResponse:
    """人数を検索条件に入れず、DBで食材・器具・公開条件を絞り込む。"""
    query = unicodedata.normalize("NFKC", search.q).casefold().strip()
    items, total = catalog.recipes(
        operation="list_recipes",
        query=query,
        selected_food_ids=search.selected_food_ids,
        excluded_food_ids=search.excluded_food_ids,
        match=search.match,
        max_minutes=search.max_minutes,
        equipment=search.equipment,
        limit=search.limit,
        offset=search.offset,
        preview=search.preview,
    )
    return RecipesResponse(items=items, total=total, limit=search.limit, offset=search.offset)
