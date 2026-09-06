import unicodedata

from app.integrations.catalog.port import CatalogPort

from .schemas import FoodsResponse


def list_foods(catalog: CatalogPort, query: str) -> FoodsResponse:
    """正規化した検索語に一致するサンプル食材名と別名を返す。"""
    q = unicodedata.normalize("NFKC", query).casefold().strip()
    items = [
        f
        for f in catalog.foods()
        if not q
        or any(q in unicodedata.normalize("NFKC", term).casefold() for term in [f.name, *f.aliases])
    ]
    return FoodsResponse(items=items, total=len(items))
