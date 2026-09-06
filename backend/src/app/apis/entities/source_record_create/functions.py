# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.entity_service import EntityService
from app.entities.models import SourceRecordRow, SourceRecordWrite
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, payload: SourceRecordWrite) -> SourceRecordRow:
    """根拠資料の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_source_record_create"],
        payload=payload.model_dump(mode="python", by_alias=True),
    )
    return SourceRecordRow.model_validate(rows[0])
