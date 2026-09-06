# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="entity_user_shopping_check_list",
    slug="entities/user_shopping_check_list",
    method="GET",
    path="/api/entities/user_shopping_check",
    summary="調理前の買い物確認の一覧",
    authentication="bearer",
    errors=(401, 403, 409, 422, 503),
    idempotency="GETは副作用なし。POSTは新規IDを採番する。",
    transaction="本人所有権・参照・DB制約・監査・outboxを同じトランザクションで検査する",
    effects="読取りのみ",
)
