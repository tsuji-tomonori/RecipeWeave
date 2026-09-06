from app.core.models import PutStateRequest, StateEnvelope
from app.integrations.state.port import StateRepository


def put_state(repository: StateRepository, subject: str, body: PutStateRequest) -> StateEnvelope:
    """Perform a conditional write; conflict never silently overwrites newer device data."""
    return repository.put(subject, body.expected_version, body.snapshot)
