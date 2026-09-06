# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.entity_service import EntityService
from app.entities.models import UserFoodRow, UserFoodWrite
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, payload: UserFoodWrite) -> UserFoodRow:
    """利用者が追加した独自食材の所有の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_user_food_create"],
        payload=payload.model_dump(mode="python", by_alias=True),
    )
    return UserFoodRow.model_validate(rows[0])
