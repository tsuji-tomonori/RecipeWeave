from app.integrations.catalog.port import CatalogPort

from .schemas import RandomRecipeResponse, RandomRecipeSearch


def random_recipe(catalog: CatalogPort, search: RandomRecipeSearch) -> RandomRecipeResponse:
    """除外食材と前回の一品を除いて選ぶ。候補ゼロならnullを返す。"""
    items, total = catalog.recipes(
        operation="random_recipe",
        excluded_food_ids=search.excluded_food_ids,
        exclude_id=search.exclude_id,
        preview=search.preview,
        limit=1,
    )
    return RandomRecipeResponse(item=items[0] if items else None, total=total)
