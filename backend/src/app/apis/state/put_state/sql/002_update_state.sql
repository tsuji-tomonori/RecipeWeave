-- Replace only the expected revision and return the new revision.
UPDATE recipeweave.user_state SET revision = revision + 1, payload = %(payload)s,
updated_at = CURRENT_TIMESTAMP WHERE subject = %(subject)s AND revision = %(revision)s
RETURNING revision;
