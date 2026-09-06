# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.entity_service import EntityService
from app.entities.models import RecipeRow, RecipeWrite
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, payload: RecipeWrite) -> RecipeRow:
    """レシピ同一性の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_recipe_create"],
        payload=payload.model_dump(mode="python", by_alias=True),
    )
    return RecipeRow.model_validate(rows[0])
