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
    effects="正規化レシピの材料・工程を参照。指定版が非公開の場合は本人の献立・利用履歴に固定された版のみ復元",
)
