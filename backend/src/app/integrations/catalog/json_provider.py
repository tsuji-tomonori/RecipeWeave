"""変更しないサンプルレコードを読む。組み合わせ列挙候補は対象にしない。"""

from pathlib import Path

from pydantic import TypeAdapter

from app.core.models import Food, Recipe


class JsonCatalog:
    def __init__(self, path: Path) -> None:
        self._foods = TypeAdapter(list[Food]).validate_json((path / "foods.json").read_text())
        self._recipes = TypeAdapter(list[Recipe]).validate_json((path / "recipes.json").read_text())

    def foods(self) -> list[Food]:
        return [food.model_copy(deep=True) for food in self._foods]

    def recipes(self) -> list[Recipe]:
        return [recipe.model_copy(deep=True) for recipe in self._recipes]
