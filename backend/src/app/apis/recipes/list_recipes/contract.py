from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="list_recipes",
    slug="recipes/list_recipes",
    method="GET",
    path="/api/recipes",
    summary="食材・時間から保存済みの料理を探す",
    authentication="public",
    errors=(401, 403, 422, 503),
    idempotency="読取専用",
    transaction="要求単位の読取トランザクション",
    effects="正規化されたレシピ・材料・工程・分類の参照",
)
