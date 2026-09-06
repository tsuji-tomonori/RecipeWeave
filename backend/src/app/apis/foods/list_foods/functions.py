import unicodedata

from app.integrations.catalog.port import CatalogPort

from .schemas import FoodsResponse


def list_foods(catalog: CatalogPort, query: str) -> FoodsResponse:
    """入力を正規化し、DBの食品・別名に対して検索する。"""
    items, total = catalog.foods(unicodedata.normalize("NFKC", query).casefold().strip())
    return FoodsResponse(items=items, total=total)
