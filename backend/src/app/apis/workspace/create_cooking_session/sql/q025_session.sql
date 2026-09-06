-- 正規化した入力行の識別子・固定量だけを版付き入力契約へ保存する。
INSERT INTO recipeweave.cooking_session
(id, menu_id, menu_revision, status, target_at, planner_version, input_snapshot, input_hash)
VALUES (
    %(session_id)s,
    %(menu_id)s,
    %(revision)s,
    'cooking',
    NULL,
    'dag-resource-v1',
    %(snapshot)s,
    %(hash)s
);
