from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="preview_backup",
    slug="backup/preview_backup",
    method="POST",
    path="/api/backups/preview",
    summary="バックアップの全置換内容を検証する",
    authentication="検証済みBearerトークンと本人所有権",
    errors=(401, 403, 409, 413, 422, 503),
    idempotency="発行済み本人本文digestを照合し、呼出しごとに15分間の確認を発行する",
    transaction="現在版のロック下で実際に全置換と全制約検証を行い、savepointを必ず取消して確認だけを保存する",
    effects="試験置換を取消して確認intentだけを発行する",
)
