from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="put_settings",
    slug="workspace/put_settings",
    method="PUT",
    path="/api/settings",
    summary="好み・常備食材・器具を設定する",
    authentication="検証済みBearerトークンと本人所有権",
    errors=(401, 403, 404, 409, 422, 503),
    idempotency="要求のexpectedVersionで再送・同時更新を検出する",
    transaction="本人のworkspace_revisionをロックし、各正規化行・監査・版を原子的に確定する",
    effects="正規化された本人の業務データを更新する",
)
