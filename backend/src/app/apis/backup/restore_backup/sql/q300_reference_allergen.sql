-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.allergen AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (TRUE);
