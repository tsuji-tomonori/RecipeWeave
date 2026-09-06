from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="restore_backup",
    slug="backup/restore_backup",
    method="POST",
    path="/api/backups/restore",
    summary="確認したバックアップで本人のデータを全置換する",
    authentication="検証済みBearerトークンと本人所有権",
    errors=(401, 403, 409, 413, 422, 503),
    idempotency="本人・本文digest・未使用intent・expectedVersionを照合し、確認を一度だけ消費する",
    transaction="現在版をロックし、全行置換・確認消費・版増分・監査・outboxを一つのトランザクションで確定する",
    effects="本人の全業務行・私有食品を置換し、現在版・監査・outboxを記録する",
)
