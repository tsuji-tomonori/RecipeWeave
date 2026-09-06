from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="export_backup",
    slug="backup/export_backup",
    method="POST",
    path="/api/backups/export",
    summary="バックアップを書き出す",
    authentication="検証済みBearerトークンと本人所有権",
    errors=(401, 403, 409, 413, 422, 503),
    idempotency="呼出しごとに新しい発行記録を作成し、本文は保存しない",
    transaction="本人の現在版をロックし、一つのSQLで全業務表を一貫して読み、発行根拠を同時に記録する",
    effects="本人のバックアップ発行記録を追加する",
)
