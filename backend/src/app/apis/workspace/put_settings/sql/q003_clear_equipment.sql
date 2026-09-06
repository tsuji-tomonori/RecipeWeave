-- 予約履歴が参照する設備IDを保持し、画面で選択する器具だけを無効にする。
UPDATE recipeweave.kitchen_resource AS k SET active = FALSE
WHERE k.user_id = %(user_id)s AND EXISTS (SELECT 1 FROM recipeweave.resource_type AS r
WHERE r.id = k.resource_type_id AND r.code NOT IN ('person', 'burner', 'bowl'));
