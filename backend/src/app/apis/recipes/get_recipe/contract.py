from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="get_recipe",
    slug="recipes/get_recipe",
    method="GET",
    path="/api/recipes/{recipe_id}",
    summary="料理の材料と工程を表示する",
    authentication="public",
    errors=(404, 422),
    idempotency="読取専用",
    transaction="なし",
    effects="なし",
)
