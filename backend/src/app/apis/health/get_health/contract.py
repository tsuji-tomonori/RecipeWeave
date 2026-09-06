from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="get_health",
    slug="health/get_health",
    method="GET",
    path="/api/health",
    summary="稼働状況とサンプル公開範囲",
    authentication="public",
    errors=(),
    idempotency="読取専用",
    transaction="なし",
    effects="なし",
)
