-- Read only the verified subject's current revision and payload.
SELECT revision, payload FROM recipeweave.user_state WHERE subject = %(subject)s;
