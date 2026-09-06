# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="entity_compatibility_rule_list",
    slug="entities/compatibility_rule_list",
    method="GET",
    path="/api/entities/compatibility_rule",
    summary="組み合わせ・公開ルールの一覧",
    authentication="bearer",
    errors=(401, 403, 409, 422, 503),
    idempotency="GETは副作用なし。POSTは新規IDを採番する。",
    transaction="本人所有権・参照・DB制約・監査・outboxを同じトランザクションで検査する",
    effects="読取りのみ",
)
