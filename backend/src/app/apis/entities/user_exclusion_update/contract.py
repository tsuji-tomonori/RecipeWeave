# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="entity_user_exclusion_update",
    slug="entities/user_exclusion_update",
    method="PUT",
    path="/api/entities/user_exclusion/{row_id}",
    summary="避けたい食材・物質の更新",
    authentication="bearer",
    errors=(401, 403, 409, 422, 428, 503),
    idempotency="If-Matchによる同一行版の条件付き操作",
    transaction="本人所有権・参照・DB制約・監査・outboxを同じトランザクションで検査する",
    effects="正規化行の変更。監査を追記しカタログ変更はoutboxへ通知する。",
)
