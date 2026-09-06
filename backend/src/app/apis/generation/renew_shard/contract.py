"""生成リースの延長の公開契約。"""

from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="renew_shard",
    slug="generation/renew_shard",
    method="PUT",
    path="/api/generation/shards/{row_id}/lease",
    summary="生成リースの延長",
    authentication="bearer",
    errors=(401, 403, 409, 422, 503),
    idempotency="フェンス・所有者・有効期限で条件付き更新する",
    transaction="リース変更と監査・outboxを同時確定する",
    effects="generation_shardのリースまたは進捗を更新する",
)
