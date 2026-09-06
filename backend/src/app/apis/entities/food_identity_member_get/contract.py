# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="entity_food_identity_member_get",
    slug="entities/food_identity_member_get",
    method="GET",
    path="/api/entities/food_identity_member/{row_id}",
    summary="購買食品から同一性への対応の取得",
    authentication="bearer",
    errors=(401, 403, 404, 409, 422, 503),
    idempotency="GETは副作用なし。POSTは新規IDを採番する。",
    transaction="本人所有権・参照・DB制約・監査・outboxを同じトランザクションで検査する",
    effects="読取りのみ",
)
