"""カタログの境界で、現在のサンプル保存方式を呼出側から分離する。"""

from typing import Protocol

from app.core.models import Food, Recipe


class CatalogPort(Protocol):
    def foods(self) -> list[Food]: ...

    def recipes(self) -> list[Recipe]: ...
