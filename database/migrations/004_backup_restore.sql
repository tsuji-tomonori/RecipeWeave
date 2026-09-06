-- 本人へ発行したバックアップの真正性と、一度だけの復元確認を本文保存なしで保持する。
CREATE TABLE recipeweave.backup_artifact (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID,
    body_sha256 TEXT NOT NULL,
    format_version INTEGER NOT NULL,
    UNIQUE (user_id, body_sha256, format_version),
    CHECK (body_sha256 ~ '^[0-9a-f]{64}$'),
    CHECK (format_version = 2)
);

COMMENT ON TABLE recipeweave.backup_artifact IS '本人へ発行したバックアップの証拠。本文を保存せず、削除後も匿名化した発行記録を保持する';
COMMENT ON COLUMN recipeweave.backup_artifact.id IS 'バックアップ本文に含める不変の発行識別子';
COMMENT ON COLUMN recipeweave.backup_artifact.created_at IS 'サーバーによる発行日時（UTC）';
COMMENT ON COLUMN recipeweave.backup_artifact.user_id IS '発行先の本人。利用者消去後だけNULLへ匿名化する';
COMMENT ON COLUMN recipeweave.backup_artifact.body_sha256 IS '発行識別子を含む正規化済み本文全体のSHA-256';
COMMENT ON COLUMN recipeweave.backup_artifact.format_version IS '対応するバックアップの形式版。現在は2';

ALTER TABLE recipeweave.backup_artifact ADD CONSTRAINT fk_backup_artifact_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_backup_artifact_user_id ON recipeweave.backup_artifact (user_id);

CREATE TABLE recipeweave.backup_restore_intent (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID,
    artifact_id UUID NOT NULL,
    body_sha256 TEXT NOT NULL,
    current_revision BIGINT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    consumed_at TIMESTAMPTZ,
    CHECK (body_sha256 ~ '^[0-9a-f]{64}$'),
    CHECK (current_revision >= 0),
    CHECK (expires_at > created_at AND expires_at <= created_at + INTERVAL '15 minutes'),
    CHECK (consumed_at IS NULL OR (consumed_at >= created_at AND consumed_at < expires_at))
);

COMMENT ON TABLE recipeweave.backup_restore_intent IS '復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度だけ消費する';
COMMENT ON COLUMN recipeweave.backup_restore_intent.id IS '確認画面へ返す不変の復元確認識別子';
COMMENT ON COLUMN recipeweave.backup_restore_intent.created_at IS '復元内容を検証して確認記録を発行した日時（UTC）';
COMMENT ON COLUMN recipeweave.backup_restore_intent.user_id IS '復元する本人。利用者消去後だけNULLへ匿名化する';
COMMENT ON COLUMN recipeweave.backup_restore_intent.artifact_id IS '本人へ発行したバックアップ証拠の識別子';
COMMENT ON COLUMN recipeweave.backup_restore_intent.body_sha256 IS '確認した本文全体のSHA-256。発行記録と一致する';
COMMENT ON COLUMN recipeweave.backup_restore_intent.current_revision
IS '確認時の現在データの更新版。復元直前にも同じ値であることを検査する';
COMMENT ON COLUMN recipeweave.backup_restore_intent.expires_at IS '確認の有効期限。発行から最大15分';
COMMENT ON COLUMN recipeweave.backup_restore_intent.consumed_at
IS '復元と同一トランザクションで確定する使用日時。取消・再使用は不可';

ALTER TABLE recipeweave.backup_restore_intent ADD CONSTRAINT fk_backup_restore_intent_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE recipeweave.backup_restore_intent ADD CONSTRAINT fk_backup_restore_intent_artifact_id
FOREIGN KEY (artifact_id) REFERENCES recipeweave.backup_artifact (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_backup_restore_intent_user_id ON recipeweave.backup_restore_intent (user_id);
CREATE INDEX ix_backup_restore_intent_artifact_id ON recipeweave.backup_restore_intent (
    artifact_id
);
CREATE INDEX ix_backup_restore_intent_pending
ON recipeweave.backup_restore_intent (user_id, expires_at) WHERE consumed_at IS NULL;

CREATE FUNCTION recipeweave.guard_backup_artifact() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        IF NEW.user_id IS NULL THEN
            RAISE EXCEPTION 'バックアップの発行先を省略できません' USING ERRCODE = '23514';
        END IF;
        RETURN NEW;
    END IF;
    IF TG_OP = 'UPDATE' AND OLD.user_id IS NOT NULL AND NEW.user_id IS NULL
       AND (to_jsonb(NEW) - 'user_id') = (to_jsonb(OLD) - 'user_id')
       AND NOT EXISTS (SELECT 1 FROM recipeweave.app_user WHERE id = OLD.user_id) THEN
        RETURN NEW;
    END IF;
    RAISE EXCEPTION 'バックアップ発行記録は追記専用です' USING ERRCODE = '23514';
END;
$$;

CREATE FUNCTION recipeweave.guard_backup_restore_intent() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    issued recipeweave.backup_artifact%ROWTYPE;
    workspace_revision bigint;
BEGIN
    IF TG_OP = 'DELETE' THEN
        RAISE EXCEPTION '復元確認記録は削除できません' USING ERRCODE = '23514';
    END IF;
    IF TG_OP = 'UPDATE' AND OLD.user_id IS NOT NULL AND NEW.user_id IS NULL
       AND (to_jsonb(NEW) - 'user_id') = (to_jsonb(OLD) - 'user_id')
       AND NOT EXISTS (SELECT 1 FROM recipeweave.app_user WHERE id = OLD.user_id) THEN
        RETURN NEW;
    END IF;
    IF NEW.user_id IS NULL THEN
        RAISE EXCEPTION '復元する本人を省略できません' USING ERRCODE = '23514';
    END IF;
    SELECT * INTO issued FROM recipeweave.backup_artifact WHERE id = NEW.artifact_id FOR KEY SHARE;
    IF NOT FOUND OR issued.user_id IS DISTINCT FROM NEW.user_id
       OR issued.body_sha256 <> NEW.body_sha256 THEN
        RAISE EXCEPTION 'バックアップの本人または本文が発行記録と一致しません' USING ERRCODE = '23514';
    END IF;
    SELECT revision INTO workspace_revision FROM recipeweave.workspace_revision
    WHERE user_id = NEW.user_id FOR UPDATE;
    IF NOT FOUND OR workspace_revision <> NEW.current_revision THEN
        RAISE EXCEPTION '確認後に現在データが変更されています。もう一度確認してください' USING ERRCODE = '23514';
    END IF;
    IF clock_timestamp() >= NEW.expires_at THEN
        RAISE EXCEPTION '復元確認の有効期限が切れています' USING ERRCODE = '23514';
    END IF;
    IF TG_OP = 'INSERT' THEN
        IF NEW.consumed_at IS NOT NULL THEN
            RAISE EXCEPTION '復元確認を使用済みとして発行できません' USING ERRCODE = '23514';
        END IF;
        RETURN NEW;
    END IF;
    IF OLD.consumed_at IS NOT NULL OR NEW.consumed_at IS NULL
       OR NEW.consumed_at > clock_timestamp()
       OR (to_jsonb(NEW) - 'consumed_at') <> (to_jsonb(OLD) - 'consumed_at') THEN
        RAISE EXCEPTION '復元確認は変更できず、一度だけ使用できます' USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER backup_artifact_append_only BEFORE INSERT OR UPDATE OR DELETE
ON recipeweave.backup_artifact
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_backup_artifact();

CREATE TRIGGER backup_intent_single_use BEFORE INSERT OR UPDATE OR DELETE
ON recipeweave.backup_restore_intent
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_backup_restore_intent();

ALTER TABLE recipeweave.backup_artifact ENABLE ROW LEVEL SECURITY;
ALTER TABLE recipeweave.backup_artifact FORCE ROW LEVEL SECURITY;
CREATE POLICY backup_evidence_owner ON recipeweave.backup_artifact
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
);

ALTER TABLE recipeweave.backup_restore_intent ENABLE ROW LEVEL SECURITY;
ALTER TABLE recipeweave.backup_restore_intent FORCE ROW LEVEL SECURITY;
CREATE POLICY backup_evidence_owner ON recipeweave.backup_restore_intent
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
);
