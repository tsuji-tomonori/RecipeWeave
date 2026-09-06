from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="update_menu_item",
    slug="workspace/update_menu_item",
    method="PATCH",
    path="/api/menus/current/items/{row_id}",
    summary="献立の人数・分量を変更する",
    authentication="検証済みBearerトークンと本人所有権",
    errors=(401, 403, 404, 409, 422, 503),
    idempotency="要求のexpectedVersionで再送・同時更新を検出する",
    transaction="本人のworkspace_revisionをロックし、各正規化行・監査・版を原子的に確定する",
    effects="正規化された本人の業務データを更新する",
)
