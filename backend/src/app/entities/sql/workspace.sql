-- 本人の変更を端末間の競合判定に反映し、業務更新と同時に版を増やす。
INSERT INTO recipeweave.workspace_revision AS current_revision (
    id, user_id, revision
)
VALUES (
    %(row_id)s, %(actor_id)s, 1
)
ON CONFLICT (user_id)
DO UPDATE SET revision = current_revision.revision + 1
RETURNING revision;
