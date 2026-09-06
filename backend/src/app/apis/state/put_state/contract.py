from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="put_state",
    slug="state/put_state",
    method="PUT",
    path="/api/state",
    summary="版を確認して利用者自身の状態を置き換える",
    authentication="cognito-access-jwt",
    errors=(401, 409, 413, 422, 503),
    idempotency="repeat with stale expectedVersion returns 409; reload to verify",
    transaction="one compare-and-swap transaction",
    effects="replace verified subject snapshot",
)
