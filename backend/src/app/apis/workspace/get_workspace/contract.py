from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="get_workspace",
    slug="workspace/get_workspace",
    method="GET",
    path="/api/workspace",
    summary="ワークスペースを取得する",
    authentication="検証済みBearerトークンと本人所有権",
    errors=(401, 403, 404, 409, 422, 503),
    idempotency="要求のexpectedVersionで再送・同時更新を検出する",
    transaction="本人のworkspace_revisionをロックし、各正規化行・監査・版を原子的に確定する",
    effects="本人の正規化データを一貫した版で読む",
)
