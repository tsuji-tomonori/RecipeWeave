-- 人数変更時の利用者の時間見積りを、実測済みの調理時間と区別して固定する。
ALTER TABLE recipeweave.session_task
ADD COLUMN duration_source TEXT NOT NULL DEFAULT 'recipe_rule';

COMMENT ON COLUMN recipeweave.session_task.duration_source
IS '計画時間の根拠。料理の時間規則または利用者が確認した見積り';

ALTER TABLE recipeweave.session_task ADD COLUMN confirmed_duration_s INTEGER;

COMMENT ON COLUMN recipeweave.session_task.confirmed_duration_s
IS '利用者が確認した工程の見積り秒数。実測値ではなく、計画後は変更しない';

ALTER TABLE recipeweave.session_task ADD CONSTRAINT duration_source_values
CHECK (duration_source IN ('recipe_rule', 'user_estimate'));

ALTER TABLE recipeweave.session_task ADD CONSTRAINT confirmed_duration_bounds
CHECK (confirmed_duration_s IS NULL OR confirmed_duration_s BETWEEN 1 AND 86400);

ALTER TABLE recipeweave.session_task ADD CONSTRAINT duration_confirmation_matches_plan
CHECK (
    (duration_source = 'recipe_rule' AND confirmed_duration_s IS NULL)
    OR (
        duration_source = 'user_estimate' AND confirmed_duration_s IS NOT NULL
        AND planned_end_s - planned_start_s = confirmed_duration_s
    )
);

CREATE FUNCTION recipeweave.guard_confirmed_task_plan() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.duration_source = 'user_estimate' AND NOT EXISTS (
        SELECT 1 FROM recipeweave.recipe_step step
        JOIN recipeweave.scaling_rule rule ON rule.id = step.scaling_rule_id
        WHERE step.id = NEW.step_id AND rule.mode = 'manual'
    ) THEN
        RAISE EXCEPTION '利用者の時間見積りは手動確認が必要な工程だけに指定できます' USING ERRCODE = '23514';
    END IF;
    IF TG_OP = 'UPDATE' THEN
        IF NEW.duration_source IS DISTINCT FROM OLD.duration_source
           OR NEW.confirmed_duration_s IS DISTINCT FROM OLD.confirmed_duration_s
           OR NEW.planned_start_s IS DISTINCT FROM OLD.planned_start_s
           OR NEW.planned_end_s IS DISTINCT FROM OLD.planned_end_s THEN
            RAISE EXCEPTION '確定した工程の時間根拠・見積り・計画時刻は変更できません' USING ERRCODE = '23514';
        END IF;
        IF OLD.duration_source = 'user_estimate' AND (
            NEW.step_id <> OLD.step_id OR NEW.menu_item_id <> OLD.menu_item_id
            OR NEW.session_id <> OLD.session_id OR NEW.batch_no <> OLD.batch_no
        ) THEN
            RAISE EXCEPTION '時間を確認した工程・献立・実行・バッチは変更できません' USING ERRCODE = '23514';
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER confirmed_task_plan_immutable BEFORE INSERT OR UPDATE ON recipeweave.session_task
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_confirmed_task_plan();

-- 旧seedを適用済みの場合だけ新IDへ移す。旧規則・公開版・他の規則を変更しない。
-- 1000人は操作の入力範囲であり、試作結果や調理器具の物理容量を保証しない。
DO $$
DECLARE
    v_source_id uuid := '9decf898-19cd-5c03-b3e2-947d838c06bd';
    new_rule_id uuid := '9b2b5a4c-18db-5694-b175-96f9f2717e7c';
BEGIN
    IF NOT EXISTS (SELECT 1 FROM recipeweave.source_record WHERE id = v_source_id) THEN
        RETURN;
    END IF;
    INSERT INTO recipeweave.scaling_rule (
        id, name, mode, min_servings, max_servings, batch_capacity,
        round_mode, round_increment, source_id
    ) VALUES (
        new_rule_id,
        '人数変更時は利用者の時間見積りが必要（1〜1000は入力範囲・物理容量は別途確認）',
        'manual', 1, 1000, NULL, 'none', 0.01, v_source_id
    ) ON CONFLICT (id) DO NOTHING;
    IF NOT EXISTS (
        SELECT 1 FROM recipeweave.scaling_rule r
        WHERE r.id = new_rule_id AND r.mode = 'manual'
        AND r.name = '人数変更時は利用者の時間見積りが必要（1〜1000は入力範囲・物理容量は別途確認）'
        AND r.min_servings = 1 AND r.max_servings = 1000 AND r.batch_capacity IS NULL
        AND r.round_mode = 'none' AND r.round_increment = 0.01 AND r.source_id = v_source_id
    ) THEN
        RAISE EXCEPTION '移行先の時間規則IDに異なる定義があります' USING ERRCODE = '23514';
    END IF;
    UPDATE recipeweave.recipe_step step SET scaling_rule_id = new_rule_id
    FROM recipeweave.recipe_version version
    WHERE step.recipe_version_id = version.id AND version.status = 'draft'
    AND step.scaling_rule_id = 'aa59a90d-0a79-5f69-95a9-7857ffe94fad'
    AND version.id IN (
        'fcb0b2fa-f387-5a51-8bed-0b8f0a539e36', '0f3cb194-c9ef-5025-a738-227a3e712b0b',
        'bdcd3054-68c1-58f2-b544-bce1eda0b005', '5f21b805-9f20-508f-a7ca-a9cb7e4e1107',
        'f29a4fca-63ba-57be-8b93-a55e87132917', '519749b7-2259-56f0-ae91-840f24558453',
        '30509788-f24f-564e-8e32-70ced25efd69', '9a8ba1c3-7df7-5a7f-87dd-043538c39d37'
    );
END;
$$;
