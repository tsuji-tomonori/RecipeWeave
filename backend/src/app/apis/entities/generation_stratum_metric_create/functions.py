# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.entity_service import EntityService
from app.entities.models import GenerationStratumMetricRow, GenerationStratumMetricWrite
from app.entities.registry import SPECIFICATIONS


def execute(
    service: EntityService, payload: GenerationStratumMetricWrite
) -> GenerationStratumMetricRow:
    """採用率・飽和度の実測の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_generation_stratum_metric_create"],
        payload=payload.model_dump(mode="python", by_alias=True),
    )
    return GenerationStratumMetricRow.model_validate(rows[0])
