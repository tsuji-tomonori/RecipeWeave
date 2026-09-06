from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="get_recipe",
    slug="recipes/get_recipe",
    method="GET",
    path="/api/recipes/{recipe_id}",
    summary="料理の材料と工程を表示する",
    authentication="public",
    errors=(401, 403, 404, 422, 503),
    idempotency="読取専用",
    transaction="要求単位の読取トランザクション",
    effects="正規化されたレシピ・材料・工程・分類の参照",
)
