-- 調理による在庫消費の冪等台帳を取得する。
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
    t.id = %(row_id)s
    AND t.user_id = %(actor_id)s;
