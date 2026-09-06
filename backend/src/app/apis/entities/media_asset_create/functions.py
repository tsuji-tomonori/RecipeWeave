# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.entity_service import EntityService
from app.entities.models import MediaAssetRow, MediaAssetWrite
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, payload: MediaAssetWrite) -> MediaAssetRow:
    """教育用動画等の版の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_media_asset_create"],
        payload=payload.model_dump(mode="python", by_alias=True),
    )
    return MediaAssetRow.model_validate(rows[0])
