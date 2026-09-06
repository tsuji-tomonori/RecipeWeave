from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="get_me",
    slug="auth/get_me",
    method="GET",
    path="/api/me",
    summary="本人のプロフィールを取得する",
    authentication="検証済みBearerトークン",
    errors=(401, 404, 422, 503),
    idempotency="本人の初回行と版だけを冪等に初期化する",
    transaction="要求のPostgreSQLトランザクション",
    effects="本人のプロフィールと初回登録",
)
