from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="local_login",
    slug="auth/local_login",
    method="POST",
    path="/api/auth/local-login",
    summary="開発環境へログインする",
    authentication="public; 開発環境限定。本文の資格情報を検証",
    errors=(401, 404, 422, 503),
    idempotency="新しい期限のアクセストークンを発行する",
    transaction="要求のPostgreSQLトランザクション",
    effects="本人の開発用トークンを発行",
)
