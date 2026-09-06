-- 正規化DBの実装。説明はCOMMENTと生成設計を参照する。

CREATE TABLE recipeweave.receipt_import (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    file_sha256 CHAR(64),
    idempotency_key TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    revision BIGINT NOT NULL DEFAULT 1,
    committed_at TIMESTAMPTZ,
    reverted_at TIMESTAMPTZ,
    UNIQUE (user_id, idempotency_key),
    CHECK (status IN ('draft', 'committed', 'reverted')),
    CHECK (revision >= 1),
    CHECK (status <> 'committed' OR committed_at IS NOT NULL),
    CHECK (status <> 'reverted' OR (committed_at IS NOT NULL AND reverted_at IS NOT NULL))
);

COMMENT ON TABLE recipeweave.receipt_import IS 'レシート読取・在庫登録の処理単位';

COMMENT ON COLUMN recipeweave.receipt_import.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.receipt_import.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.receipt_import.user_id IS '所有者';

COMMENT ON COLUMN recipeweave.receipt_import.file_sha256 IS '画像本文のSHA256。本文はDBに保存しない';

COMMENT ON COLUMN recipeweave.receipt_import.idempotency_key IS '本人内で一意の再送防止キー';

COMMENT ON COLUMN recipeweave.receipt_import.status IS 'draft/committed/revertedの状態';

COMMENT ON COLUMN recipeweave.receipt_import.revision IS '楽観ロック版';

COMMENT ON COLUMN recipeweave.receipt_import.committed_at IS '在庫へ登録した日時';

COMMENT ON COLUMN recipeweave.receipt_import.reverted_at IS '登録取消日時';

CREATE TABLE recipeweave.receipt_line (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    import_id UUID NOT NULL,
    line_no INTEGER NOT NULL,
    raw_name TEXT NOT NULL,
    form_id UUID,
    product_version_id UUID,
    amount NUMERIC(20, 6),
    unit_id UUID,
    decision TEXT NOT NULL DEFAULT 'unresolved',
    pantry_lot_id UUID,
    UNIQUE (import_id, line_no),
    CHECK (line_no > 0),
    CHECK (decision IN ('accepted', 'skipped', 'unresolved')),
    CHECK (amount IS NULL OR amount > 0),
    CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK ((amount IS NULL) OR unit_id IS NOT NULL),
    CHECK (decision <> 'accepted' OR form_id IS NOT NULL)
);

COMMENT ON TABLE recipeweave.receipt_line IS 'レシートの商品候補と確定した在庫の対応';

COMMENT ON COLUMN recipeweave.receipt_line.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.receipt_line.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.receipt_line.import_id IS 'レシート処理';

COMMENT ON COLUMN recipeweave.receipt_line.line_no IS 'レシート内の表示順';

COMMENT ON COLUMN recipeweave.receipt_line.raw_name IS '利用者が確認できる商品原表記';

COMMENT ON COLUMN recipeweave.receipt_line.form_id IS '確定した食材形態';

COMMENT ON COLUMN recipeweave.receipt_line.product_version_id IS '確定した商品版';

COMMENT ON COLUMN recipeweave.receipt_line.amount IS '数量。不明はNULL';

COMMENT ON COLUMN recipeweave.receipt_line.unit_id IS '確定数量の単位';

COMMENT ON COLUMN recipeweave.receipt_line.decision IS 'accepted/skipped/unresolved';

COMMENT ON COLUMN recipeweave.receipt_line.pantry_lot_id IS '登録したロット';

CREATE TABLE recipeweave.workspace_revision (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    revision BIGINT NOT NULL DEFAULT 0,
    UNIQUE (user_id),
    CHECK (revision >= 0)
);

COMMENT ON TABLE recipeweave.workspace_revision IS '利用者ワークスペースの原子的更新版';

COMMENT ON COLUMN recipeweave.workspace_revision.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.workspace_revision.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.workspace_revision.user_id IS '所有者';

COMMENT ON COLUMN recipeweave.workspace_revision.revision IS '全体のCAS版';

CREATE TABLE recipeweave.user_food (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    food_id UUID NOT NULL,
    UNIQUE (food_id),
    UNIQUE (user_id, food_id)
);

COMMENT ON TABLE recipeweave.user_food IS '利用者が追加した独自食材の所有';

COMMENT ON COLUMN recipeweave.user_food.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.user_food.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.user_food.user_id IS '所有者';

COMMENT ON COLUMN recipeweave.user_food.food_id IS '独自食材';

CREATE TABLE recipeweave.user_pantry_food (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    food_id UUID NOT NULL,
    UNIQUE (user_id, food_id)
);

COMMENT ON TABLE recipeweave.user_pantry_food IS '利用者が常備すると設定した食材';

COMMENT ON COLUMN recipeweave.user_pantry_food.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.user_pantry_food.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.user_pantry_food.user_id IS '所有者';

COMMENT ON COLUMN recipeweave.user_pantry_food.food_id IS '常備食材';

CREATE TABLE recipeweave.pantry_consumption (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    session_id UUID NOT NULL,
    lot_id UUID NOT NULL,
    amount NUMERIC(20, 6) NOT NULL,
    unit_id UUID NOT NULL,
    UNIQUE (session_id, lot_id),
    CHECK (amount > 0),
    CHECK (amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.pantry_consumption IS '調理による在庫消費の冪等台帳';

COMMENT ON COLUMN recipeweave.pantry_consumption.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.pantry_consumption.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.pantry_consumption.user_id IS '所有者';

COMMENT ON COLUMN recipeweave.pantry_consumption.session_id IS '消費した調理セッション';

COMMENT ON COLUMN recipeweave.pantry_consumption.lot_id IS '消費元ロット';

COMMENT ON COLUMN recipeweave.pantry_consumption.amount IS '消費数量';

COMMENT ON COLUMN recipeweave.pantry_consumption.unit_id IS '消費数量の単位';

ALTER TABLE recipeweave.recipe_version ADD COLUMN description TEXT;

COMMENT ON COLUMN recipeweave.recipe_version.description IS '料理の紹介文';

ALTER TABLE recipeweave.recipe_step ADD COLUMN title TEXT;

COMMENT ON COLUMN recipeweave.recipe_step.title IS '工程の短い見出し';

ALTER TABLE recipeweave.recipe_ingredient ADD COLUMN note TEXT;

COMMENT ON COLUMN recipeweave.recipe_ingredient.note IS '材料の補足';

ALTER TABLE recipeweave.pantry_lot ADD COLUMN location TEXT NOT NULL DEFAULT 'fridge';

COMMENT ON COLUMN recipeweave.pantry_lot.location IS '冷蔵・冷凍・常温の保管場所';

ALTER TABLE recipeweave.pantry_lot ADD COLUMN priority TEXT NOT NULL DEFAULT 'normal';

COMMENT ON COLUMN recipeweave.pantry_lot.priority IS '先に使う優先指定';

ALTER TABLE recipeweave.pantry_lot ADD COLUMN status TEXT NOT NULL DEFAULT 'active';

COMMENT ON COLUMN recipeweave.pantry_lot.status IS '在庫の有効・削除・レシート取消状態';

ALTER TABLE recipeweave.pantry_lot ADD COLUMN source_import_id UUID;

COMMENT ON COLUMN recipeweave.pantry_lot.source_import_id IS '登録元レシート';

ALTER TABLE recipeweave.pantry_lot ADD COLUMN quantity_quality TEXT NOT NULL DEFAULT 'known';

COMMENT ON COLUMN recipeweave.pantry_lot.quantity_quality IS '数量の確定・不明';

ALTER TABLE recipeweave.pantry_lot ADD COLUMN original_form_id UUID;

COMMENT ON COLUMN recipeweave.pantry_lot.original_form_id IS '登録時の食材形態';

ALTER TABLE recipeweave.pantry_lot ADD COLUMN original_amount NUMERIC(20, 6);

COMMENT ON COLUMN recipeweave.pantry_lot.original_amount IS '登録時数量。不明はNULL';

ALTER TABLE recipeweave.pantry_lot ADD COLUMN original_unit_id UUID;

COMMENT ON COLUMN recipeweave.pantry_lot.original_unit_id IS '登録時単位';

ALTER TABLE recipeweave.pantry_lot ADD COLUMN updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW();

COMMENT ON COLUMN recipeweave.pantry_lot.updated_at IS '最終編集日時';

ALTER TABLE recipeweave.pantry_lot ADD COLUMN edited BOOLEAN NOT NULL DEFAULT FALSE;

COMMENT ON COLUMN recipeweave.pantry_lot.edited IS '登録後の編集有無';

ALTER TABLE recipeweave.shopping_item ADD COLUMN client_key TEXT;

COMMENT ON COLUMN recipeweave.shopping_item.client_key IS '画面操作の安定キー';

ALTER TABLE recipeweave.shopping_item ADD COLUMN checked_at TIMESTAMPTZ;

COMMENT ON COLUMN recipeweave.shopping_item.checked_at IS '購入確認日時';

ALTER TABLE recipeweave.shopping_item ADD COLUMN archived BOOLEAN NOT NULL DEFAULT FALSE;

COMMENT ON COLUMN recipeweave.shopping_item.archived IS '完了した買い物の保管状態';

ALTER TABLE recipeweave.pantry_lot ALTER COLUMN amount DROP NOT NULL;

ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT pantry_location CHECK (
    location IN ('fridge', 'freezer', 'pantry')
);

ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT pantry_priority CHECK (
    priority IN ('normal', 'use_first')
);

ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT pantry_status CHECK (
    status IN ('active', 'deleted', 'undone')
);

ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT pantry_quantity CHECK (
    (quantity_quality = 'known' AND amount IS NOT NULL)
    OR (quantity_quality = 'unknown' AND amount IS NULL)
);

ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT pantry_original_amount CHECK (
    original_amount IS NULL
    OR (original_amount >= 0 AND original_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

ALTER TABLE recipeweave.cooking_session DROP CONSTRAINT cooking_session_status_check;

ALTER TABLE recipeweave.cooking_session ADD CONSTRAINT cooking_session_status_check CHECK (
    status IN ('planned', 'cooking', 'paused', 'completed', 'cancelled')
);

ALTER TABLE recipeweave.receipt_import ADD CONSTRAINT fk_receipt_import_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_receipt_import_user_id ON recipeweave.receipt_import (user_id);

ALTER TABLE recipeweave.receipt_line ADD CONSTRAINT fk_receipt_line_import_id
FOREIGN KEY (import_id) REFERENCES recipeweave.receipt_import (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_receipt_line_import_id ON recipeweave.receipt_line (import_id);

ALTER TABLE recipeweave.receipt_line ADD CONSTRAINT fk_receipt_line_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_receipt_line_form_id ON recipeweave.receipt_line (form_id);

ALTER TABLE recipeweave.receipt_line ADD CONSTRAINT fk_receipt_line_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_receipt_line_product_version_id ON recipeweave.receipt_line (product_version_id);

ALTER TABLE recipeweave.receipt_line ADD CONSTRAINT fk_receipt_line_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_receipt_line_unit_id ON recipeweave.receipt_line (unit_id);

ALTER TABLE recipeweave.receipt_line ADD CONSTRAINT fk_receipt_line_pantry_lot_id
FOREIGN KEY (pantry_lot_id) REFERENCES recipeweave.pantry_lot (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_receipt_line_pantry_lot_id ON recipeweave.receipt_line (pantry_lot_id);

ALTER TABLE recipeweave.workspace_revision ADD CONSTRAINT fk_workspace_revision_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_workspace_revision_user_id ON recipeweave.workspace_revision (user_id);

ALTER TABLE recipeweave.user_food ADD CONSTRAINT fk_user_food_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_user_food_user_id ON recipeweave.user_food (user_id);

ALTER TABLE recipeweave.user_food ADD CONSTRAINT fk_user_food_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_user_food_food_id ON recipeweave.user_food (food_id);

ALTER TABLE recipeweave.user_pantry_food ADD CONSTRAINT fk_user_pantry_food_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_user_pantry_food_user_id ON recipeweave.user_pantry_food (user_id);

ALTER TABLE recipeweave.user_pantry_food ADD CONSTRAINT fk_user_pantry_food_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_user_pantry_food_food_id ON recipeweave.user_pantry_food (food_id);

ALTER TABLE recipeweave.pantry_consumption ADD CONSTRAINT fk_pantry_consumption_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_pantry_consumption_user_id ON recipeweave.pantry_consumption (user_id);

ALTER TABLE recipeweave.pantry_consumption ADD CONSTRAINT fk_pantry_consumption_session_id
FOREIGN KEY (session_id) REFERENCES recipeweave.cooking_session (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_pantry_consumption_session_id ON recipeweave.pantry_consumption (session_id);

ALTER TABLE recipeweave.pantry_consumption ADD CONSTRAINT fk_pantry_consumption_lot_id
FOREIGN KEY (lot_id) REFERENCES recipeweave.pantry_lot (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_pantry_consumption_lot_id ON recipeweave.pantry_consumption (lot_id);

ALTER TABLE recipeweave.pantry_consumption ADD CONSTRAINT fk_pantry_consumption_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_pantry_consumption_unit_id ON recipeweave.pantry_consumption (unit_id);

ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_source_import_id
FOREIGN KEY (source_import_id) REFERENCES recipeweave.receipt_import (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_pantry_lot_source_import_id ON recipeweave.pantry_lot (source_import_id);

ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_original_form_id
FOREIGN KEY (original_form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_pantry_lot_original_form_id ON recipeweave.pantry_lot (original_form_id);

ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_original_unit_id
FOREIGN KEY (original_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_pantry_lot_original_unit_id ON recipeweave.pantry_lot (original_unit_id);

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.receipt_import
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

ALTER TABLE recipeweave.receipt_import ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.receipt_import FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.receipt_import
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR receipt_import.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR receipt_import.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
);

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.receipt_line
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

ALTER TABLE recipeweave.receipt_line ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.receipt_line FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.receipt_line
USING (
    CURRENT_SETTING(
        'recipeweave.role', TRUE
    ) = 'admin'
    OR (
        SELECT r.user_id FROM recipeweave.receipt_import AS r
        WHERE r.id = receipt_line.import_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), ''
    )::UUID
) WITH CHECK (CURRENT_SETTING(
    'recipeweave.role', TRUE) = 'admin' OR (
    SELECT r.user_id FROM recipeweave.receipt_import AS r
    WHERE r.id = receipt_line.import_id
) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), ''
)::UUID);

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.workspace_revision
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

ALTER TABLE recipeweave.workspace_revision ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.workspace_revision FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.workspace_revision
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR workspace_revision.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR workspace_revision.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
);

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.user_food
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

ALTER TABLE recipeweave.user_food ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.user_food FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.user_food
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR user_food.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR user_food.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.user_pantry_food
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

ALTER TABLE recipeweave.user_pantry_food ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.user_pantry_food FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.user_pantry_food
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR user_pantry_food.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR user_pantry_food.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.pantry_consumption
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

ALTER TABLE recipeweave.pantry_consumption ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.pantry_consumption FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.pantry_consumption
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR pantry_consumption.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR pantry_consumption.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

CREATE TABLE recipeweave.user_shopping_check (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    key TEXT NOT NULL,
    signature TEXT NOT NULL,
    food_id UUID,
    amount NUMERIC(20, 6),
    unit_id UUID,
    checked_at TIMESTAMPTZ,
    archived BOOLEAN NOT NULL DEFAULT false,
    UNIQUE (user_id, key),
    CHECK (
        amount IS null OR (amount >= 0 AND amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
    ),
    CHECK (amount IS null OR unit_id IS NOT null)
);

COMMENT ON TABLE recipeweave.user_shopping_check IS '調理前の買い物確認';

COMMENT ON COLUMN recipeweave.user_shopping_check.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.user_shopping_check.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.user_shopping_check.user_id IS '所有者';

COMMENT ON COLUMN recipeweave.user_shopping_check.key IS '買い物対象の安定キー';

COMMENT ON COLUMN recipeweave.user_shopping_check.signature IS '数量・商品条件の一致確認用署名';

COMMENT ON COLUMN recipeweave.user_shopping_check.food_id IS '対象食材';

COMMENT ON COLUMN recipeweave.user_shopping_check.amount IS '必要数量。不明はNULL';

COMMENT ON COLUMN recipeweave.user_shopping_check.unit_id IS '数量単位';

COMMENT ON COLUMN recipeweave.user_shopping_check.checked_at IS '購入確認日時';

COMMENT ON COLUMN recipeweave.user_shopping_check.archived IS '保管済みか';

ALTER TABLE recipeweave.user_shopping_check ADD CONSTRAINT fk_user_shopping_check_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE recipeweave.user_shopping_check ADD CONSTRAINT fk_user_shopping_check_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE recipeweave.user_shopping_check ADD CONSTRAINT fk_user_shopping_check_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_user_shopping_check_user_id ON recipeweave.user_shopping_check (user_id);

CREATE INDEX ix_user_shopping_check_food_id ON recipeweave.user_shopping_check (food_id);

CREATE INDEX ix_user_shopping_check_unit_id ON recipeweave.user_shopping_check (unit_id);

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.user_shopping_check
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

ALTER TABLE recipeweave.user_shopping_check ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.user_shopping_check FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.user_shopping_check
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
)
WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

CREATE FUNCTION recipeweave.check_receipt_reference() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    v_import_id uuid;
    current_import recipeweave.receipt_import%ROWTYPE;
    current_lot recipeweave.pantry_lot%ROWTYPE;
BEGIN

    EXECUTE format('SELECT * FROM recipeweave.%I WHERE id = $1', TG_TABLE_NAME) INTO NEW USING NEW.id;
    IF NEW.id IS NULL THEN RETURN NULL; END IF;
    IF TG_TABLE_NAME = 'receipt_import' THEN
        v_import_id := NEW.id;
    ELSIF TG_TABLE_NAME = 'receipt_line' THEN
        v_import_id := NEW.import_id;
        IF NEW.pantry_lot_id IS NOT NULL THEN
            SELECT * INTO current_lot FROM recipeweave.pantry_lot WHERE id = NEW.pantry_lot_id;
            SELECT * INTO current_import FROM recipeweave.receipt_import WHERE id = v_import_id;
            IF current_lot.user_id <> current_import.user_id OR current_lot.source_import_id IS DISTINCT FROM v_import_id
               OR current_lot.form_id IS DISTINCT FROM NEW.form_id THEN
                RAISE EXCEPTION 'レシート行と在庫ロットの所有者・登録元・食材が不一致です' USING ERRCODE = '23514';
            END IF;
        END IF;
        IF NEW.product_version_id IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM recipeweave.product_version WHERE id = NEW.product_version_id AND form_id = NEW.form_id
        ) THEN RAISE EXCEPTION 'レシートの商品と食材形態が不一致です' USING ERRCODE = '23514'; END IF;
    ELSIF TG_TABLE_NAME = 'pantry_lot' THEN
        v_import_id := NEW.source_import_id;
        IF v_import_id IS NULL THEN RETURN NULL; END IF;
        IF NOT EXISTS (SELECT 1 FROM recipeweave.receipt_import WHERE id = v_import_id AND user_id = NEW.user_id) THEN
            RAISE EXCEPTION '他人のレシートへ在庫を紐付けできません' USING ERRCODE = '23514';
        END IF;
    END IF;
    SELECT * INTO current_import FROM recipeweave.receipt_import WHERE id = v_import_id FOR UPDATE;
    IF NOT FOUND THEN RETURN NULL; END IF;
    IF current_import.status = 'committed' AND EXISTS (
        SELECT 1 FROM recipeweave.receipt_line line WHERE line.import_id = v_import_id
        AND (line.decision = 'unresolved' OR (line.decision = 'accepted' AND line.pantry_lot_id IS NULL))
    ) THEN RAISE EXCEPTION '未解決または未登録のレシート行が残っています' USING ERRCODE = '23514'; END IF;
    IF current_import.status = 'reverted' AND EXISTS (
        SELECT 1 FROM recipeweave.pantry_lot lot WHERE lot.source_import_id = v_import_id AND lot.status = 'active'
        AND NOT lot.edited AND NOT EXISTS (SELECT 1 FROM recipeweave.pantry_consumption c WHERE c.lot_id = lot.id)
    ) THEN RAISE EXCEPTION '取消後のレシートに未編集・未消費の有効な在庫が残っています' USING ERRCODE = '23514'; END IF;
    RETURN NULL;
END;
$$;

CREATE FUNCTION recipeweave.guard_receipt_lifecycle() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF OLD.user_id <> NEW.user_id OR OLD.idempotency_key <> NEW.idempotency_key
       OR NEW.revision <= OLD.revision
       OR (OLD.status = 'reverted' AND NEW.status <> 'reverted')
       OR (OLD.status = 'committed' AND NEW.status = 'draft') THEN
        RAISE EXCEPTION 'レシートの状態・所有者・版の遷移が不正です' USING ERRCODE = '23514';
    END IF;
    IF NEW.status = 'reverted' THEN
        SELECT COUNT(*) INTO NEW.undo_preserved_count FROM recipeweave.pantry_lot lot
        WHERE lot.source_import_id = OLD.id AND lot.status = 'active'
        AND (lot.edited OR EXISTS (SELECT 1 FROM recipeweave.pantry_consumption c WHERE c.lot_id = lot.id));
    END IF;
    RETURN NEW;
END;
$$;

CREATE FUNCTION recipeweave.check_consumption_owner() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN

    EXECUTE format('SELECT * FROM recipeweave.%I WHERE id = $1', TG_TABLE_NAME) INTO NEW USING NEW.id;
    IF NEW.id IS NULL THEN RETURN NULL; END IF;
    IF NOT EXISTS (
        SELECT 1 FROM recipeweave.pantry_lot lot, recipeweave.cooking_session session
        JOIN recipeweave.menu menu ON menu.id = session.menu_id
        WHERE lot.id = NEW.lot_id AND lot.user_id = NEW.user_id AND lot.unit_id = NEW.unit_id
        AND session.id = NEW.session_id AND menu.user_id = NEW.user_id
    ) THEN RAISE EXCEPTION '消費元と調理の所有者・単位が不一致です' USING ERRCODE = '23514'; END IF;
    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER receipt_integrity AFTER INSERT OR UPDATE ON recipeweave.receipt_import
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_receipt_reference();

CREATE CONSTRAINT TRIGGER receipt_integrity AFTER INSERT OR UPDATE ON recipeweave.receipt_line
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_receipt_reference();

CREATE CONSTRAINT TRIGGER receipt_integrity AFTER INSERT OR UPDATE ON recipeweave.pantry_lot
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_receipt_reference();

CREATE TRIGGER receipt_lifecycle BEFORE UPDATE ON recipeweave.receipt_import
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_receipt_lifecycle();

CREATE CONSTRAINT TRIGGER consumption_owner AFTER INSERT OR UPDATE ON recipeweave.pantry_consumption
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_consumption_owner();

COMMENT ON TABLE recipeweave.user_state IS '旧Devスナップショット。移行履歴専用でサービスのデータ正本には使用しない';

REVOKE INSERT, UPDATE, DELETE ON recipeweave.user_state FROM public;

ALTER TABLE recipeweave.food ADD COLUMN owner_id UUID;

COMMENT ON COLUMN recipeweave.food.owner_id IS '私有食材の所有者。NULLは共通カタログ食材';

ALTER TABLE recipeweave.food ADD CONSTRAINT fk_food_owner_id
FOREIGN KEY (owner_id) REFERENCES recipeweave.app_user (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_food_owner_id ON recipeweave.food (owner_id);

ALTER TABLE recipeweave.food ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.food FORCE ROW LEVEL SECURITY;

CREATE POLICY food_read ON recipeweave.food FOR SELECT
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin' OR owner_id IS null
    OR owner_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

CREATE POLICY food_write ON recipeweave.food FOR ALL
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR owner_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
)
WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR owner_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

CREATE FUNCTION recipeweave.food_visible(food_id UUID) RETURNS BOOLEAN
LANGUAGE sql STABLE SET search_path = pg_catalog, recipeweave AS $$
    SELECT EXISTS (SELECT 1 FROM recipeweave.food WHERE id = food_id);
$$;

CREATE FUNCTION recipeweave.food_writable(food_id UUID) RETURNS BOOLEAN
LANGUAGE sql STABLE SET search_path = pg_catalog, recipeweave AS $$
    SELECT current_setting('recipeweave.role', true) = 'admin' OR EXISTS (
        SELECT 1 FROM recipeweave.food WHERE id = food_id
        AND owner_id = nullif(current_setting('recipeweave.user_id', true), '')::uuid
    );
$$;

CREATE FUNCTION recipeweave.check_private_food_owner() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN

    EXECUTE format('SELECT * FROM recipeweave.%I WHERE id = $1', TG_TABLE_NAME) INTO NEW USING NEW.id;
    IF NEW.id IS NULL THEN RETURN NULL; END IF;
    IF TG_TABLE_NAME = 'user_food' AND NOT EXISTS (
        SELECT 1 FROM recipeweave.food WHERE id = NEW.food_id AND owner_id = NEW.user_id
    ) THEN RAISE EXCEPTION '独自食材と所有者が一致しません' USING ERRCODE = '23514'; END IF;
    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER private_food_owner AFTER INSERT OR UPDATE ON recipeweave.user_food
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_private_food_owner();

ALTER TABLE recipeweave.food_form ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.food_form FORCE ROW LEVEL SECURITY;

CREATE POLICY food_derived_read ON recipeweave.food_form FOR SELECT
USING (recipeweave.food_visible(food_id));

CREATE POLICY food_derived_write ON recipeweave.food_form FOR ALL
USING (recipeweave.food_writable(food_id)) WITH CHECK (recipeweave.food_writable(food_id));

ALTER TABLE recipeweave.food_alias ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.food_alias FORCE ROW LEVEL SECURITY;

CREATE POLICY food_derived_read ON recipeweave.food_alias FOR SELECT
USING (recipeweave.food_visible(food_id));

CREATE POLICY food_derived_write ON recipeweave.food_alias FOR ALL
USING (recipeweave.food_writable(food_id)) WITH CHECK (recipeweave.food_writable(food_id));

ALTER TABLE recipeweave.food_axis_option ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.food_axis_option FORCE ROW LEVEL SECURITY;

CREATE POLICY food_derived_read ON recipeweave.food_axis_option FOR SELECT
USING (recipeweave.food_visible(food_id));

CREATE POLICY food_derived_write ON recipeweave.food_axis_option FOR ALL
USING (recipeweave.food_writable(food_id)) WITH CHECK (recipeweave.food_writable(food_id));

ALTER TABLE recipeweave.product ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.product FORCE ROW LEVEL SECURITY;

CREATE POLICY food_derived_read ON recipeweave.product FOR SELECT
USING (recipeweave.food_visible(food_id));

CREATE POLICY food_derived_write ON recipeweave.product FOR ALL
USING (recipeweave.food_writable(food_id)) WITH CHECK (recipeweave.food_writable(food_id));

ALTER TABLE recipeweave.conversion ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.conversion FORCE ROW LEVEL SECURITY;

CREATE POLICY food_derived_read ON recipeweave.conversion FOR SELECT
USING (
    recipeweave.food_visible((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = conversion.form_id
    ))
);

CREATE POLICY food_derived_write ON recipeweave.conversion FOR ALL
USING (
    recipeweave.food_writable((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = conversion.form_id
    ))
) WITH CHECK (recipeweave.food_writable((
    SELECT food_form.food_id FROM recipeweave.food_form
    WHERE food_form.id = conversion.form_id
)));

ALTER TABLE recipeweave.food_allergen ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.food_allergen FORCE ROW LEVEL SECURITY;

CREATE POLICY food_derived_read ON recipeweave.food_allergen FOR SELECT
USING (
    recipeweave.food_visible((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = food_allergen.form_id
    ))
);

CREATE POLICY food_derived_write ON recipeweave.food_allergen FOR ALL
USING (
    recipeweave.food_writable((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = food_allergen.form_id
    ))
) WITH CHECK (recipeweave.food_writable((
    SELECT food_form.food_id FROM recipeweave.food_form
    WHERE food_form.id = food_allergen.form_id
)));

ALTER TABLE recipeweave.product_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.product_version FORCE ROW LEVEL SECURITY;

CREATE POLICY food_derived_read ON recipeweave.product_version FOR SELECT
USING (
    recipeweave.food_visible((
        SELECT product.food_id FROM recipeweave.product
        WHERE product.id = product_version.product_id
    ))
);

CREATE POLICY food_derived_write ON recipeweave.product_version FOR ALL
USING (
    recipeweave.food_writable((
        SELECT product.food_id FROM recipeweave.product
        WHERE product.id = product_version.product_id
    ))
) WITH CHECK (recipeweave.food_writable((
    SELECT product.food_id FROM recipeweave.product
    WHERE product.id = product_version.product_id
)));

ALTER TABLE recipeweave.product_component ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.product_component FORCE ROW LEVEL SECURITY;

CREATE POLICY food_derived_read ON recipeweave.product_component FOR SELECT
USING (
    recipeweave.food_visible(
        (
            SELECT product.food_id
            FROM recipeweave.product_version AS version
            INNER JOIN recipeweave.product AS product ON version.product_id = product.id
            WHERE version.id = product_component.product_version_id
        )
    )
);

CREATE POLICY food_derived_write ON recipeweave.product_component FOR ALL
USING (
    recipeweave.food_writable(
        (
            SELECT product.food_id
            FROM recipeweave.product_version AS version
            INNER JOIN recipeweave.product AS product ON version.product_id = product.id
            WHERE version.id = product_component.product_version_id
        )
    )
) WITH CHECK (
    recipeweave.food_writable((
        SELECT product.food_id
        FROM recipeweave.product_version AS version
        INNER JOIN recipeweave.product AS product ON version.product_id = product.id
        WHERE version.id = product_component.product_version_id
    ))
);

ALTER TABLE recipeweave.product_allergen ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.product_allergen FORCE ROW LEVEL SECURITY;

CREATE POLICY food_derived_read ON recipeweave.product_allergen FOR SELECT
USING (
    recipeweave.food_visible(
        (
            SELECT product.food_id
            FROM recipeweave.product_version AS version
            INNER JOIN recipeweave.product AS product ON version.product_id = product.id
            WHERE version.id = product_allergen.product_version_id
        )
    )
);

CREATE POLICY food_derived_write ON recipeweave.product_allergen FOR ALL
USING (
    recipeweave.food_writable(
        (
            SELECT product.food_id
            FROM recipeweave.product_version AS version
            INNER JOIN recipeweave.product AS product ON version.product_id = product.id
            WHERE version.id = product_allergen.product_version_id
        )
    )
) WITH CHECK (
    recipeweave.food_writable((
        SELECT product.food_id
        FROM recipeweave.product_version AS version
        INNER JOIN recipeweave.product AS product ON version.product_id = product.id
        WHERE version.id = product_allergen.product_version_id
    ))
);

ALTER TABLE recipeweave.product_preparation_rule ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.product_preparation_rule FORCE ROW LEVEL SECURITY;

CREATE POLICY food_derived_read ON recipeweave.product_preparation_rule FOR SELECT
USING (
    recipeweave.food_visible(
        (
            SELECT product.food_id
            FROM recipeweave.product_version AS version
            INNER JOIN recipeweave.product AS product ON version.product_id = product.id
            WHERE version.id = product_preparation_rule.product_version_id
        )
    )
);

CREATE POLICY food_derived_write ON recipeweave.product_preparation_rule FOR ALL
USING (
    recipeweave.food_writable(
        (
            SELECT product.food_id
            FROM recipeweave.product_version AS version
            INNER JOIN recipeweave.product AS product ON version.product_id = product.id
            WHERE version.id = product_preparation_rule.product_version_id
        )
    )
) WITH CHECK (
    recipeweave.food_writable((
        SELECT product.food_id
        FROM recipeweave.product_version AS version
        INNER JOIN recipeweave.product AS product ON version.product_id = product.id
        WHERE version.id = product_preparation_rule.product_version_id
    ))
);

ALTER TABLE recipeweave.nutrition_fact ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.nutrition_fact FORCE ROW LEVEL SECURITY;

CREATE POLICY food_derived_read ON recipeweave.nutrition_fact FOR SELECT
USING (
    recipeweave.food_visible(COALESCE((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = nutrition_fact.form_id
    ),
    (
        SELECT product.food_id
        FROM recipeweave.product_version AS version
        INNER JOIN recipeweave.product AS product ON version.product_id = product.id
        WHERE version.id = nutrition_fact.product_version_id
    )))
);

CREATE POLICY food_derived_write ON recipeweave.nutrition_fact FOR ALL
USING (
    recipeweave.food_writable(COALESCE((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = nutrition_fact.form_id
    ),
    (
        SELECT product.food_id
        FROM recipeweave.product_version AS version
        INNER JOIN recipeweave.product AS product ON version.product_id = product.id
        WHERE version.id = nutrition_fact.product_version_id
    )))
) WITH CHECK (recipeweave.food_writable(COALESCE((
    SELECT food_form.food_id FROM recipeweave.food_form
    WHERE food_form.id = nutrition_fact.form_id
),
(
    SELECT product.food_id
    FROM recipeweave.product_version AS version
    INNER JOIN recipeweave.product AS product ON version.product_id = product.id
    WHERE version.id = nutrition_fact.product_version_id
))));

ALTER TABLE recipeweave.form_yield ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.form_yield FORCE ROW LEVEL SECURITY;

CREATE POLICY food_derived_read ON recipeweave.form_yield FOR SELECT
USING (
    recipeweave.food_visible((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = form_yield.input_form_id
    ))
);

CREATE POLICY food_derived_write ON recipeweave.form_yield FOR ALL
USING (
    recipeweave.food_writable((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = form_yield.input_form_id
    ))
) WITH CHECK (recipeweave.food_writable((
    SELECT food_form.food_id FROM recipeweave.food_form
    WHERE food_form.id = form_yield.input_form_id
)));

ALTER TABLE recipeweave.cooking_session ADD COLUMN current_task_index INTEGER NOT NULL DEFAULT 0;

COMMENT ON COLUMN recipeweave.cooking_session.current_task_index IS '調理画面の現在の工程位置（0始まり）';

ALTER TABLE recipeweave.cooking_session ADD CONSTRAINT cooking_current_index CHECK (
    current_task_index >= 0
);

ALTER TABLE recipeweave.session_task ADD COLUMN timer_started_at TIMESTAMPTZ;

COMMENT ON COLUMN recipeweave.session_task.timer_started_at IS '稼働中タイマーの開始日時';

ALTER TABLE recipeweave.session_task ADD COLUMN timer_duration_s INTEGER;

COMMENT ON COLUMN recipeweave.session_task.timer_duration_s IS '利用者が設定したタイマー秒数';

ALTER TABLE recipeweave.session_task ADD CONSTRAINT timer_duration CHECK (
    timer_duration_s IS NULL OR timer_duration_s >= 0
);

ALTER TABLE recipeweave.session_task ADD CONSTRAINT timer_start_requires_duration CHECK (
    timer_started_at IS NULL OR timer_duration_s IS NOT NULL
);

ALTER TABLE recipeweave.ingredient_total ADD COLUMN actual_amount NUMERIC(20, 6);

COMMENT ON COLUMN recipeweave.ingredient_total.actual_amount IS '利用者が確定した実使用量。不明はNULL';

ALTER TABLE recipeweave.ingredient_total ADD COLUMN consumption_outcome TEXT NOT NULL DEFAULT 'not_requested';

COMMENT ON COLUMN recipeweave.ingredient_total.consumption_outcome IS '未要求・反映済み・在庫不足・数量不明・単位不一致の結果';

ALTER TABLE recipeweave.ingredient_total ADD CONSTRAINT actual_amount_finite CHECK (
    actual_amount IS NULL
    OR (actual_amount >= 0 AND actual_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

ALTER TABLE recipeweave.ingredient_total ADD CONSTRAINT consumption_outcome_values CHECK (
    consumption_outcome IN ('not_requested', 'applied', 'insufficient', 'unknown', 'incompatible')
);

-- 資源の過去予約を維持したまま、新規計画で使わない状態を表す。
ALTER TABLE recipeweave.kitchen_resource ADD COLUMN active BOOLEAN NOT NULL DEFAULT TRUE;
COMMENT ON COLUMN recipeweave.kitchen_resource.active IS '新規の調理計画で利用する資源か';

-- 取消しで残した編集済み・消費済みロットの件数を利用者へ説明する。
ALTER TABLE recipeweave.receipt_import ADD COLUMN undo_preserved_count INTEGER NOT NULL DEFAULT 0;
COMMENT ON COLUMN recipeweave.receipt_import.undo_preserved_count IS 'レシート取消時に編集・消費済みとして残した在庫件数';
ALTER TABLE recipeweave.receipt_import ADD CONSTRAINT undo_preserved_count_nonnegative CHECK (undo_preserved_count >= 0);

-- 私有食材の追加用カタログを共通カタログの公開ライフサイクルから分離する。
ALTER TABLE recipeweave.catalog_release ADD COLUMN owner_id UUID;
COMMENT ON COLUMN recipeweave.catalog_release.owner_id IS '私有カタログの所有者。NULLは共通カタログ';
ALTER TABLE recipeweave.catalog_release ADD CONSTRAINT fk_catalog_release_owner_id
FOREIGN KEY (owner_id) REFERENCES recipeweave.app_user (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX ix_catalog_release_owner_id ON recipeweave.catalog_release (owner_id);
ALTER TABLE recipeweave.catalog_release ADD CONSTRAINT private_catalog_unpublished CHECK (owner_id IS NULL OR published_at IS NULL);
ALTER TABLE recipeweave.catalog_release ENABLE ROW LEVEL SECURITY;
ALTER TABLE recipeweave.catalog_release FORCE ROW LEVEL SECURITY;
CREATE POLICY catalog_read ON recipeweave.catalog_release FOR SELECT
USING (CURRENT_SETTING('recipeweave.role', TRUE) = 'admin' OR owner_id IS NULL
    OR owner_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID);
CREATE POLICY catalog_write ON recipeweave.catalog_release FOR ALL
USING (CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR owner_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID)
WITH CHECK (CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR owner_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID);

CREATE FUNCTION recipeweave.guard_private_owner() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.owner_id IS DISTINCT FROM OLD.owner_id THEN
        RAISE EXCEPTION '所有者の付替えや私有データの共通公開への変更はできません' USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
END;
$$;
CREATE TRIGGER private_owner_immutable BEFORE UPDATE ON recipeweave.food
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_private_owner();
CREATE TRIGGER private_owner_immutable BEFORE UPDATE ON recipeweave.catalog_release
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_private_owner();

CREATE FUNCTION recipeweave.check_food_release_owner() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    catalog_owner uuid;
BEGIN
    SELECT owner_id INTO catalog_owner FROM recipeweave.catalog_release WHERE id = NEW.release_id;
    IF catalog_owner IS DISTINCT FROM NEW.owner_id THEN
        RAISE EXCEPTION '食材と所属カタログの所有者が一致しません' USING ERRCODE = '23514';
    END IF;
    RETURN NULL;
END;
$$;
CREATE CONSTRAINT TRIGGER food_release_owner AFTER INSERT OR UPDATE ON recipeweave.food
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_food_release_owner();
