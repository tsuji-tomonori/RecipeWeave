# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from app.core.entity_service import EntityService
from app.entities.models import RecipeSimilarityRow
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, row_id: UUID) -> RecipeSimilarityRow:
    """近似レシピ関係の取得を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(SPECIFICATIONS["entity_recipe_similarity_get"], row_id=row_id)
    return RecipeSimilarityRow.model_validate(rows[0])
