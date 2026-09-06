from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="list_foods",
    slug="foods/list_foods",
    method="GET",
    path="/api/foods",
    summary="食材候補を検索する",
    authentication="public",
    errors=(422,),
    idempotency="read-only",
    transaction="none",
    effects="none",
)
