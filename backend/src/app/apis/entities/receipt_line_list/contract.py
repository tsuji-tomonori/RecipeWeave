# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="entity_receipt_line_list",
    slug="entities/receipt_line_list",
    method="GET",
    path="/api/entities/receipt_line",
    summary="レシートの商品候補と確定した在庫の対応の一覧",
    authentication="bearer",
    errors=(401, 403, 409, 422, 503),
    idempotency="GETは副作用なし。POSTは新規IDを採番する。",
    transaction="本人所有権・参照・DB制約・監査・outboxを同じトランザクションで検査する",
    effects="読取りのみ",
)
