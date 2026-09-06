-- Create the first revision; a concurrent insert becomes a version conflict.
INSERT INTO recipeweave.user_state (subject, revision, payload, updated_at)
VALUES (%(subject)s, 1, %(payload)s, CURRENT_TIMESTAMP);
