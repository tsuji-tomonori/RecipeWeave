from app.core.models import StateEnvelope
from app.integrations.state.port import StateRepository


def get_state(repository: StateRepository, subject: str) -> StateEnvelope:
    """Read only the verified subject's state; no caller-selected user identifier."""
    return repository.get(subject)
