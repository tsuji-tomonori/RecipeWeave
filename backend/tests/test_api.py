"""HTTP入力とDB設定不足の境界。実DBのカタログ検査はtest_catalog_databaseで行う。"""

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.apis.recipes.list_recipes.schemas import RecipeSearch
from app.core.dependencies import get_settings
from app.main import create_app


def test_catalogue_requires_database_configuration(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "")
    get_settings.cache_clear()
    with TestClient(create_app()) as client:
        assert client.get("/api/foods").status_code == 503
        assert client.get("/api/recipes").status_code == 503
    get_settings.cache_clear()


def test_filter_boundaries_and_no_portions_in_search() -> None:
    for value in (
        {"maxMinutes": -1},
        {"servings": 2},
        {"limit": 101},
        {"selectedFoodIds": ["tomato"]},
    ):
        with pytest.raises(ValidationError):
            RecipeSearch.model_validate(value)
