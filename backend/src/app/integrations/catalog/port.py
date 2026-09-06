"""Catalogue port hides the current sample storage implementation."""

from typing import Protocol

from app.core.models import Food, Recipe


class CatalogPort(Protocol):
    def foods(self) -> list[Food]: ...

    def recipes(self) -> list[Recipe]: ...
