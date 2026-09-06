# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="entity_receipt_line_delete",
    slug="entities/receipt_line_delete",
    method="DELETE",
    path="/api/entities/receipt_line/{row_id}",
    summary="レシートの商品候補と確定した在庫の対応の削除",
    authentication="bearer",
    errors=(401, 403, 409, 422, 428, 503),
    idempotency="If-Matchによる同一行版の条件付き操作",
    transaction="本人所有権・参照・DB制約・監査・outboxを同じトランザクションで検査する",
    effects="正規化行の変更。監査を追記しカタログ変更はoutboxへ通知する。",
)
