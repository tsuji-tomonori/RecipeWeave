from .schemas import HealthResponse


def get_health() -> HealthResponse:
    """AWSへの配備やカタログの網羅性を示唆せず、このAPIの状態を返す。"""
    return HealthResponse()
