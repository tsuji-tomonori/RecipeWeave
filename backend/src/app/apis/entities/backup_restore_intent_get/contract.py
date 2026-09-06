# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="entity_backup_restore_intent_get",
    slug="entities/backup_restore_intent_get",
    method="GET",
    path="/api/entities/backup_restore_intent/{row_id}",
    summary="復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度だけ消費するの取得",
    authentication="bearer",
    errors=(401, 403, 404, 409, 422, 503),
    idempotency="GETは副作用なし。POSTは新規IDを採番する。",
    transaction="本人所有権・参照・DB制約・監査・outboxを同じトランザクションで検査する",
    effects="読取りのみ",
)
