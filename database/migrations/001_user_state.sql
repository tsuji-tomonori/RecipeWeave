-- Device snapshot migration boundary; normalized recipe tables remain a later migration.
CREATE TABLE recipeweave.user_state (
    subject TEXT PRIMARY KEY,
    revision BIGINT NOT NULL,
    payload JSONB NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
