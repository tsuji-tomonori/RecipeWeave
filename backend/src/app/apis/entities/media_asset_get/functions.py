# generate_entity_apis.py による自動生成。直接編集しない。
from uuid import UUID

from app.core.entity_service import EntityService
from app.entities.models import MediaAssetRow
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, row_id: UUID) -> MediaAssetRow:
    """教育用動画等の版の取得を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(SPECIFICATIONS["entity_media_asset_get"], row_id=row_id)
    return MediaAssetRow.model_validate(rows[0])
