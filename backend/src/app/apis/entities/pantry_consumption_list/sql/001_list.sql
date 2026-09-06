-- 調理による在庫消費の冪等台帳を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.user_id,
    t.session_id,
    t.lot_id,
    t.amount,
    t.unit_id,
    t.xmin::TEXT AS etag
FROM recipeweave.pantry_consumption AS t
WHERE
    t.user_id = %(actor_id)s
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
