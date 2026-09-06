from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="list_recipes",
    slug="recipes/list_recipes",
    method="GET",
    path="/api/recipes",
    summary="食材・時間からサンプル料理を探す",
    authentication="public",
    errors=(422,),
    idempotency="読取専用",
    transaction="なし",
    effects="なし",
)
