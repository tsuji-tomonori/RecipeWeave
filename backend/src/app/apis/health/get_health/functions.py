from .schemas import HealthResponse


def get_health() -> HealthResponse:
    """Describe this API without implying AWS deployment or catalog completeness."""
    return HealthResponse()
