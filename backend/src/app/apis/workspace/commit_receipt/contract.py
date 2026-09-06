from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="commit_receipt",
    slug="workspace/commit_receipt",
    method="POST",
    path="/api/receipts/commit",
    summary="確認したレシートを在庫へ登録する",
    authentication="検証済みBearerトークンと本人所有権",
    errors=(401, 403, 404, 409, 422, 503),
    idempotency="要求のexpectedVersionで再送・同時更新を検出する",
    transaction="本人のworkspace_revisionをロックし、各正規化行・監査・版を原子的に確定する",
    effects="正規化された本人の業務データを更新する",
)
