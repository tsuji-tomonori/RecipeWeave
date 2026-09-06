from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="get_state",
    slug="state/get_state",
    method="GET",
    path="/api/state",
    summary="認証した利用者自身の状態を読む",
    authentication="cognito-access-jwt",
    errors=(401, 503),
    idempotency="read-only",
    transaction="read committed snapshot",
    effects="read personal state",
)
