# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="entity_conversion_create",
    slug="entities/conversion_create",
    method="POST",
    path="/api/entities/conversion",
    summary="食材形態別換算の作成",
    authentication="bearer",
    errors=(401, 403, 409, 422, 503),
    idempotency="GETは副作用なし。POSTは新規IDを採番する。",
    transaction="本人所有権・参照・DB制約・監査・outboxを同じトランザクションで検査する",
    effects="正規化行の変更。監査を追記しカタログ変更はoutboxへ通知する。",
)
