from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="list_foods",
    slug="foods/list_foods",
    method="GET",
    path="/api/foods",
    summary="食材候補を検索する",
    authentication="public",
    errors=(401, 422, 503),
    idempotency="読取専用",
    transaction="要求単位の読取トランザクション",
    effects="食品・形態・分類・別名の参照",
)
