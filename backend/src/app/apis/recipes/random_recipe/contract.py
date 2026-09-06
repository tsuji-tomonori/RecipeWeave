from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="random_recipe",
    slug="recipes/random_recipe",
    method="GET",
    path="/api/recipes/random",
    summary="保存済みの料理から一品を選ぶ",
    authentication="public; previewには開発環境の認証が必要",
    errors=(401, 403, 422, 503),
    idempotency="読取専用。再要求では別の候補になることがある",
    transaction="要求単位の読取トランザクション",
    effects="レシピと材料・工程・分類の参照",
)
