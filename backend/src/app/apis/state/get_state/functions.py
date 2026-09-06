from app.core.models import StateEnvelope
from app.integrations.state.port import StateRepository


def get_state(repository: StateRepository, subject: str) -> StateEnvelope:
    """認証済み本人の状態だけを読む。呼出側が他の利用者識別子を選ぶことはできない。"""
    return repository.get(subject)
