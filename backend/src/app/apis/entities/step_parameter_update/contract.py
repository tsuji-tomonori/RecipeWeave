# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="entity_step_parameter_update",
    slug="entities/step_parameter_update",
    method="PUT",
    path="/api/entities/step_parameter/{row_id}",
    summary="工程の型付きパラメータの更新",
    authentication="bearer",
    errors=(401, 403, 409, 422, 428, 503),
    idempotency="If-Matchによる同一行版の条件付き操作",
    transaction="本人所有権・参照・DB制約・監査・outboxを同じトランザクションで検査する",
    effects="正規化行の変更。監査を追記しカタログ変更はoutboxへ通知する。",
)
