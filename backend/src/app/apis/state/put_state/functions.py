from app.core.models import PutStateRequest, StateEnvelope
from app.integrations.state.port import StateRepository


def put_state(repository: StateRepository, subject: str, body: PutStateRequest) -> StateEnvelope:
    """条件付きで保存する。競合時に新しい端末データを黙って上書きしない。"""
    return repository.put(subject, body.expected_version, body.snapshot)
