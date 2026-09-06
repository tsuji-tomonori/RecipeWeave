# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="entity_backup_artifact_get",
    slug="entities/backup_artifact_get",
    method="GET",
    path="/api/entities/backup_artifact/{row_id}",
    summary="本人へ発行したバックアップの証拠。本文を保存せず、削除後も匿名化した発行記録を保持するの取得",
    authentication="bearer",
    errors=(401, 403, 404, 409, 422, 503),
    idempotency="GETは副作用なし。POSTは新規IDを採番する。",
    transaction="本人所有権・参照・DB制約・監査・outboxを同じトランザクションで検査する",
    effects="読取りのみ",
)
