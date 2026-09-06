-- 検証済みバックアップの調理による在庫消費の冪等台帳を元IDと全列で復元する。
INSERT INTO recipeweave.pantry_consumption (
    id,
    created_at,
    user_id,
    session_id,
    lot_id,
    amount,
    unit_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(session_id)s,
    %(lot_id)s,
    %(amount)s,
    %(unit_id)s
);
