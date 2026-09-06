from app.core.models import Food, WireModel


class FoodsResponse(WireModel):
    items: list[Food]
    total: int
