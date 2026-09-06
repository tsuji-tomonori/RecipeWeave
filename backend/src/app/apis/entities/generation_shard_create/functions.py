# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.entity_service import EntityService
from app.entities.models import GenerationShardRow, GenerationShardWrite
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, payload: GenerationShardWrite) -> GenerationShardRow:
    """列挙範囲・リース管理の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_generation_shard_create"],
        payload=payload.model_dump(mode="python", by_alias=True),
    )
    return GenerationShardRow.model_validate(rows[0])
