from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="put_state",
    slug="state/put_state",
    method="PUT",
    path="/api/state",
    summary="版を確認して利用者自身の状態を置き換える",
    authentication="cognito-access-jwt",
    errors=(401, 409, 413, 422, 503),
    idempotency="古いexpectedVersionで再送すると409を返す。再読込して結果を確認する",
    transaction="版の比較と更新を行う単一トランザクション",
    effects="認証済み本人のスナップショットを置換する",
)
