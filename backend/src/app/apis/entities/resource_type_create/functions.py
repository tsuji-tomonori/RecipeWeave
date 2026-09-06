# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.entity_service import EntityService
from app.entities.models import ResourceTypeRow, ResourceTypeWrite
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, payload: ResourceTypeWrite) -> ResourceTypeRow:
    """道具・設備・作業者種別の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_resource_type_create"],
        payload=payload.model_dump(mode="python", by_alias=True),
    )
    return ResourceTypeRow.model_validate(rows[0])
