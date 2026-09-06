# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="entity_shopping_item_list",
    slug="entities/shopping_item_list",
    method="GET",
    path="/api/entities/shopping_item",
    summary="買い物行の一覧",
    authentication="bearer",
    errors=(401, 403, 409, 422, 503),
    idempotency="GETは副作用なし。POSTは新規IDを採番する。",
    transaction="本人所有権・参照・DB制約・監査・outboxを同じトランザクションで検査する",
    effects="読取りのみ",
)
