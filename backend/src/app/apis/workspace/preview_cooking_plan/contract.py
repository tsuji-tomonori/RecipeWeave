from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id="preview_cooking_plan",
    slug="workspace/preview_cooking_plan",
    method="POST",
    path="/api/cooking-plan",
    summary="保存せずに調理の段取りを確認する",
    authentication="検証済みBearerトークンと本人所有権",
    errors=(401, 403, 404, 422, 503),
    idempotency="読取専用。同じDB状態と入力は同じ計画を返す",
    transaction="要求単位の読取。献立・調理・監査・版の更新を行わない",
    effects="閲覧可能な指定料理版の材料と工程、依存関係、本人の設備を読み、開始時と共通の計画器で検証する",
)
