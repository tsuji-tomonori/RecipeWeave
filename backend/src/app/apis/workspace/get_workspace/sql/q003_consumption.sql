-- 二重消費を防ぐ台帳からロットごとの使用履歴を読む。
SELECT
    c.lot_id,
    c.amount,
    u.code AS unit,
    c.session_id
FROM recipeweave.pantry_consumption AS c INNER JOIN recipeweave.unit AS u ON c.unit_id = u.id
WHERE c.user_id = %(user_id)s
ORDER BY c.created_at, c.id;
