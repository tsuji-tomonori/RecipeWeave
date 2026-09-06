# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.entity_service import EntityService
from app.entities.models import CandidateAttemptRow, CandidateAttemptWrite
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, payload: CandidateAttemptWrite) -> CandidateAttemptRow:
    """試行済み設計点の台帳の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_candidate_attempt_create"],
        payload=payload.model_dump(mode="python", by_alias=True),
    )
    return CandidateAttemptRow.model_validate(rows[0])
