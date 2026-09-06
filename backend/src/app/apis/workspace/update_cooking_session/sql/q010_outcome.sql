-- 計画量を上書きせず、実際に確認した使用量と適用結果を保存する。
UPDATE recipeweave.ingredient_total SET
    actual_amount = %(amount)s, consumption_outcome = %(outcome)s
WHERE id = %(total_id)s AND session_id = %(session_id)s;
