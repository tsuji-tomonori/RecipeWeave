-- 正規化DBの実装。説明はCOMMENTと生成設計を参照する。

CREATE EXTENSION IF NOT EXISTS vector;

CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE recipeweave.source_record (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    title TEXT NOT NULL,
    url TEXT,
    locator TEXT,
    retrieved_at TIMESTAMPTZ,
    content_hash CHAR(64),
    license_note TEXT,
    CHECK (LENGTH(BTRIM(title)) BETWEEN 1 AND 20000),
    CHECK (content_hash IS NULL OR content_hash ~ '^[0-9a-f]{64}$')
);

COMMENT ON TABLE recipeweave.source_record IS '根拠資料';

COMMENT ON COLUMN recipeweave.source_record.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.source_record.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.source_record.title IS '根拠名';

COMMENT ON COLUMN recipeweave.source_record.url IS '公式資料URL';

COMMENT ON COLUMN recipeweave.source_record.locator IS '資料内位置';

COMMENT ON COLUMN recipeweave.source_record.retrieved_at IS '取得時点';

COMMENT ON COLUMN recipeweave.source_record.content_hash IS '参照内容のハッシュ';

COMMENT ON COLUMN recipeweave.source_record.license_note IS '利用条件・権利確認';

CREATE TABLE recipeweave.catalog_release (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version TEXT NOT NULL,
    manifest_hash CHAR(64) NOT NULL,
    published_at TIMESTAMPTZ,
    UNIQUE (version),
    CHECK (LENGTH(BTRIM(version)) BETWEEN 1 AND 20000),
    CHECK (manifest_hash IS NULL OR manifest_hash ~ '^[0-9a-f]{64}$')
);

COMMENT ON TABLE recipeweave.catalog_release IS 'カタログ公開版';

COMMENT ON COLUMN recipeweave.catalog_release.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.catalog_release.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.catalog_release.version IS 'カタログ版番号';

COMMENT ON COLUMN recipeweave.catalog_release.manifest_hash IS '採用したID・内容のハッシュ';

COMMENT ON COLUMN recipeweave.catalog_release.published_at IS '公開日時';

CREATE TABLE recipeweave.unit (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    dimension TEXT NOT NULL,
    factor NUMERIC(20, 6) NOT NULL,
    "offset" NUMERIC(20, 6) NOT NULL,
    status TEXT NOT NULL,
    UNIQUE (code),
    CHECK (factor > 0),
    CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(dimension)) BETWEEN 1 AND 20000),
    CHECK (dimension IN ('mass', 'volume', 'count', 'time', 'temperature', 'length', 'power')),
    CHECK (factor IS NULL OR factor::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK ("offset" IS NULL OR "offset"::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('active', 'retired'))
);

COMMENT ON TABLE recipeweave.unit IS '単位';

COMMENT ON COLUMN recipeweave.unit.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.unit.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.unit.code IS '単位コード';

COMMENT ON COLUMN recipeweave.unit.name IS '表示名';

COMMENT ON COLUMN recipeweave.unit.dimension IS '物理次元';

COMMENT ON COLUMN recipeweave.unit.factor IS '同一次元の基準単位への倍率';

COMMENT ON COLUMN recipeweave.unit."offset" IS '温度等のオフセット';

COMMENT ON COLUMN recipeweave.unit.status IS '利用状態';

CREATE TABLE recipeweave.food (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    kind TEXT NOT NULL,
    parent_id UUID,
    release_id UUID NOT NULL,
    status TEXT NOT NULL,
    UNIQUE (code, release_id),
    CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(kind)) BETWEEN 1 AND 20000),
    CHECK (kind IN ('basic', 'processed', 'ready_meal', 'kit', 'utility')),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('active', 'retired'))
);

COMMENT ON TABLE recipeweave.food IS '購入・利用食材概念';

COMMENT ON COLUMN recipeweave.food.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.food.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.food.code IS '固定食材コード';

COMMENT ON COLUMN recipeweave.food.name IS '食材名・加工品種別';

COMMENT ON COLUMN recipeweave.food.kind IS '基本食材か加工食品か';

COMMENT ON COLUMN recipeweave.food.parent_id IS 'カテゴリ親';

COMMENT ON COLUMN recipeweave.food.release_id IS '所属公開版';

COMMENT ON COLUMN recipeweave.food.status IS '新規使用可否';

CREATE TABLE recipeweave.food_alias (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    food_id UUID NOT NULL,
    alias TEXT NOT NULL,
    locale TEXT NOT NULL,
    UNIQUE (food_id, alias, locale),
    CHECK (LENGTH(BTRIM(alias)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(locale)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.food_alias IS '食材別名';

COMMENT ON COLUMN recipeweave.food_alias.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.food_alias.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.food_alias.food_id IS '正規食材';

COMMENT ON COLUMN recipeweave.food_alias.alias IS '別名・かな';

COMMENT ON COLUMN recipeweave.food_alias.locale IS '言語・地域';

CREATE TABLE recipeweave.food_form (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    food_id UUID NOT NULL,
    name TEXT NOT NULL,
    state TEXT NOT NULL,
    base_unit_id UUID NOT NULL,
    quantity_basis TEXT NOT NULL,
    status TEXT NOT NULL,
    UNIQUE (food_id, name),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(state)) BETWEEN 1 AND 20000),
    CHECK (state IN ('raw', 'dry', 'frozen', 'cooked', 'rehydrated', 'drained', 'peeled', 'ready')),
    CHECK (LENGTH(BTRIM(quantity_basis)) BETWEEN 1 AND 20000),
    CHECK (quantity_basis IN ('edible', 'as_purchased', 'drained', 'prepared')),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('active', 'retired'))
);

COMMENT ON TABLE recipeweave.food_form IS '食材形態';

COMMENT ON COLUMN recipeweave.food_form.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.food_form.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.food_form.food_id IS '対応食材';

COMMENT ON COLUMN recipeweave.food_form.name IS '生皮付き・冷凍刻み等';

COMMENT ON COLUMN recipeweave.food_form.state IS '処理状態';

COMMENT ON COLUMN recipeweave.food_form.base_unit_id IS '計算基準単位';

COMMENT ON COLUMN recipeweave.food_form.quantity_basis IS '数量の対象部分';

COMMENT ON COLUMN recipeweave.food_form.status IS '利用状態';

CREATE TABLE recipeweave.conversion (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    form_id UUID NOT NULL,
    from_unit_id UUID NOT NULL,
    to_unit_id UUID NOT NULL,
    factor NUMERIC(20, 6) NOT NULL,
    quality TEXT NOT NULL,
    source_id UUID,
    conditions TEXT NOT NULL,
    release_id UUID NOT NULL,
    UNIQUE (form_id, from_unit_id, to_unit_id, release_id, conditions),
    CHECK (factor > 0),
    CHECK (from_unit_id <> to_unit_id),
    CHECK (factor IS NULL OR factor::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (LENGTH(BTRIM(quality)) BETWEEN 1 AND 20000),
    CHECK (quality IN ('measured', 'manufacturer', 'reference', 'estimated', 'unknown')),
    CHECK (LENGTH(BTRIM(conditions)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.conversion IS '食材形態別換算';

COMMENT ON COLUMN recipeweave.conversion.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.conversion.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.conversion.form_id IS '換算対象形態';

COMMENT ON COLUMN recipeweave.conversion.from_unit_id IS '入力単位';

COMMENT ON COLUMN recipeweave.conversion.to_unit_id IS '出力単位';

COMMENT ON COLUMN recipeweave.conversion.factor IS '出力量=入力量×倍率';

COMMENT ON COLUMN recipeweave.conversion.quality IS '実測・推定区別';

COMMENT ON COLUMN recipeweave.conversion.source_id IS '換算根拠';

COMMENT ON COLUMN recipeweave.conversion.conditions IS 'サイズ・温度・すり切り等';

COMMENT ON COLUMN recipeweave.conversion.release_id IS '換算版';

CREATE TABLE recipeweave.form_yield (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    input_form_id UUID NOT NULL,
    output_form_id UUID NOT NULL,
    yield_ratio NUMERIC(20, 6) NOT NULL,
    source_id UUID,
    quality TEXT NOT NULL,
    conditions TEXT NOT NULL,
    CHECK (yield_ratio > 0),
    CHECK (input_form_id <> output_form_id),
    CHECK (yield_ratio IS NULL OR yield_ratio::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (LENGTH(BTRIM(quality)) BETWEEN 1 AND 20000),
    CHECK (quality IN ('measured', 'manufacturer', 'reference', 'estimated', 'unknown')),
    CHECK (LENGTH(BTRIM(conditions)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.form_yield IS '処理歩留まり';

COMMENT ON COLUMN recipeweave.form_yield.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.form_yield.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.form_yield.input_form_id IS '処理前形態';

COMMENT ON COLUMN recipeweave.form_yield.output_form_id IS '処理後形態';

COMMENT ON COLUMN recipeweave.form_yield.yield_ratio IS '出力量/入力量';

COMMENT ON COLUMN recipeweave.form_yield.source_id IS '根拠';

COMMENT ON COLUMN recipeweave.form_yield.quality IS '精度区分';

COMMENT ON COLUMN recipeweave.form_yield.conditions IS '皮むき・水戻し等の条件';

CREATE TABLE recipeweave.product (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    food_id UUID NOT NULL,
    brand TEXT NOT NULL,
    name TEXT NOT NULL,
    gtin TEXT,
    status TEXT NOT NULL,
    CHECK (LENGTH(BTRIM(brand)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('active', 'retired'))
);

COMMENT ON TABLE recipeweave.product IS '市販商品識別';

COMMENT ON COLUMN recipeweave.product.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.product.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.product.food_id IS '汎用食材との対応';

COMMENT ON COLUMN recipeweave.product.brand IS 'ブランド';

COMMENT ON COLUMN recipeweave.product.name IS '商品名';

COMMENT ON COLUMN recipeweave.product.gtin IS 'JAN等（先頭0保持）';

COMMENT ON COLUMN recipeweave.product.status IS '終売はretired';

CREATE TABLE recipeweave.product_version (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    product_id UUID NOT NULL,
    version INTEGER NOT NULL,
    form_id UUID NOT NULL,
    net_amount NUMERIC(20, 6) NOT NULL,
    unit_id UUID NOT NULL,
    drain_amount NUMERIC(20, 6),
    source_id UUID NOT NULL,
    preparation_note TEXT NOT NULL,
    valid_from DATE NOT NULL,
    UNIQUE (product_id, version),
    CHECK (version > 0),
    CHECK (net_amount > 0),
    CHECK (drain_amount IS NULL OR (drain_amount > 0 AND drain_amount <= net_amount)),
    CHECK (net_amount IS NULL OR net_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (drain_amount IS NULL OR drain_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (LENGTH(BTRIM(preparation_note)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.product_version IS '商品仕様版';

COMMENT ON COLUMN recipeweave.product_version.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.product_version.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.product_version.product_id IS '商品';

COMMENT ON COLUMN recipeweave.product_version.version IS '仕様版';

COMMENT ON COLUMN recipeweave.product_version.form_id IS '販売形態';

COMMENT ON COLUMN recipeweave.product_version.net_amount IS '1包装の内容量';

COMMENT ON COLUMN recipeweave.product_version.unit_id IS '内容量単位';

COMMENT ON COLUMN recipeweave.product_version.drain_amount IS '固形量';

COMMENT ON COLUMN recipeweave.product_version.source_id IS 'メーカー表示根拠';

COMMENT ON COLUMN recipeweave.product_version.preparation_note IS '容器・加熱方式・表示手順';

COMMENT ON COLUMN recipeweave.product_version.valid_from IS '適用開始日';

CREATE TABLE recipeweave.product_component (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    product_version_id UUID NOT NULL,
    form_id UUID NOT NULL,
    name TEXT NOT NULL,
    amount NUMERIC(20, 6),
    unit_id UUID,
    quality TEXT NOT NULL,
    UNIQUE (product_version_id, name),
    CHECK ((amount IS NULL) = (unit_id IS NULL)),
    CHECK (amount IS NULL OR amount > 0),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (LENGTH(BTRIM(quality)) BETWEEN 1 AND 20000),
    CHECK (quality IN ('measured', 'manufacturer', 'reference', 'estimated', 'unknown'))
);

COMMENT ON TABLE recipeweave.product_component IS 'セット内構成品';

COMMENT ON COLUMN recipeweave.product_component.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.product_component.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.product_component.product_version_id IS '親商品版';

COMMENT ON COLUMN recipeweave.product_component.form_id IS '麺・ソース・かやく等';

COMMENT ON COLUMN recipeweave.product_component.name IS '構成品名';

COMMENT ON COLUMN recipeweave.product_component.amount IS '量（不明はNULL）';

COMMENT ON COLUMN recipeweave.product_component.unit_id IS '構成品量単位';

COMMENT ON COLUMN recipeweave.product_component.quality IS '数量の根拠';

CREATE TABLE recipeweave.allergen (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    source_id UUID,
    UNIQUE (code),
    CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.allergen IS 'アレルゲン概念';

COMMENT ON COLUMN recipeweave.allergen.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.allergen.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.allergen.code IS '固定コード';

COMMENT ON COLUMN recipeweave.allergen.name IS '名称';

COMMENT ON COLUMN recipeweave.allergen.source_id IS '分類出典';

CREATE TABLE recipeweave.food_allergen (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    form_id UUID NOT NULL,
    allergen_id UUID NOT NULL,
    presence TEXT NOT NULL,
    source_id UUID NOT NULL,
    UNIQUE (form_id, allergen_id),
    CHECK (LENGTH(BTRIM(presence)) BETWEEN 1 AND 20000),
    CHECK (presence IN ('contains', 'may_contain', 'absent_verified', 'unknown'))
);

COMMENT ON TABLE recipeweave.food_allergen IS '食材アレルゲン知識';

COMMENT ON COLUMN recipeweave.food_allergen.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.food_allergen.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.food_allergen.form_id IS '食材形態';

COMMENT ON COLUMN recipeweave.food_allergen.allergen_id IS '対象物質';

COMMENT ON COLUMN recipeweave.food_allergen.presence IS '含有・不明';

COMMENT ON COLUMN recipeweave.food_allergen.source_id IS '判断根拠';

CREATE TABLE recipeweave.product_allergen (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    product_version_id UUID NOT NULL,
    allergen_id UUID NOT NULL,
    presence TEXT NOT NULL,
    source_id UUID NOT NULL,
    UNIQUE (product_version_id, allergen_id),
    CHECK (LENGTH(BTRIM(presence)) BETWEEN 1 AND 20000),
    CHECK (presence IN ('contains', 'may_contain', 'absent_verified', 'unknown'))
);

COMMENT ON TABLE recipeweave.product_allergen IS '商品表示アレルゲン';

COMMENT ON COLUMN recipeweave.product_allergen.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.product_allergen.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.product_allergen.product_version_id IS '商品仕様版';

COMMENT ON COLUMN recipeweave.product_allergen.allergen_id IS '物質';

COMMENT ON COLUMN recipeweave.product_allergen.presence IS '表示状態';

COMMENT ON COLUMN recipeweave.product_allergen.source_id IS 'ラベル等';

CREATE TABLE recipeweave.nutrient (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    unit_label TEXT NOT NULL,
    UNIQUE (code),
    CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(unit_label)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.nutrient IS '栄養成分種別';

COMMENT ON COLUMN recipeweave.nutrient.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.nutrient.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.nutrient.code IS 'energy_kcal等';

COMMENT ON COLUMN recipeweave.nutrient.name IS 'エネルギー等';

COMMENT ON COLUMN recipeweave.nutrient.unit_label IS 'kcal/g/mg/μg';

CREATE TABLE recipeweave.nutrition_fact (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    form_id UUID,
    product_version_id UUID,
    nutrient_id UUID NOT NULL,
    amount NUMERIC(20, 6) NOT NULL,
    basis_amount NUMERIC(20, 6) NOT NULL,
    basis_unit_id UUID NOT NULL,
    source_id UUID NOT NULL,
    CHECK (NUM_NONNULLS(form_id, product_version_id) = 1),
    CHECK (amount >= 0),
    CHECK (basis_amount > 0),
    CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (basis_amount IS NULL OR basis_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.nutrition_fact IS '形態・商品別栄養値';

COMMENT ON COLUMN recipeweave.nutrition_fact.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.nutrition_fact.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.nutrition_fact.form_id IS '汎用形態';

COMMENT ON COLUMN recipeweave.nutrition_fact.product_version_id IS '商品仕様';

COMMENT ON COLUMN recipeweave.nutrition_fact.nutrient_id IS '栄養成分';

COMMENT ON COLUMN recipeweave.nutrition_fact.amount IS '基準量あたり成分量';

COMMENT ON COLUMN recipeweave.nutrition_fact.basis_amount IS '基準量';

COMMENT ON COLUMN recipeweave.nutrition_fact.basis_unit_id IS '基準単位';

COMMENT ON COLUMN recipeweave.nutrition_fact.source_id IS '出典';

CREATE TABLE recipeweave.axis (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    selection TEXT NOT NULL,
    release_id UUID NOT NULL,
    status TEXT NOT NULL,
    UNIQUE (code, release_id),
    CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(purpose)) BETWEEN 1 AND 20000),
    CHECK (purpose IN ('generation', 'search', 'constraint', 'derived', 'presentation')),
    CHECK (LENGTH(BTRIM(selection)) BETWEEN 1 AND 20000),
    CHECK (selection IN ('single', 'multiple')),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('active', 'retired'))
);

COMMENT ON TABLE recipeweave.axis IS '組み合わせ軸';

COMMENT ON COLUMN recipeweave.axis.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.axis.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.axis.code IS '軸コード';

COMMENT ON COLUMN recipeweave.axis.name IS '軸名';

COMMENT ON COLUMN recipeweave.axis.purpose IS '生成/検索/制約等';

COMMENT ON COLUMN recipeweave.axis.selection IS '単複';

COMMENT ON COLUMN recipeweave.axis.release_id IS '定義版';

COMMENT ON COLUMN recipeweave.axis.status IS '採用状態';

CREATE TABLE recipeweave.axis_option (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    axis_id UUID NOT NULL,
    code TEXT NOT NULL,
    label TEXT NOT NULL,
    definition TEXT NOT NULL,
    parent_id UUID,
    status TEXT NOT NULL,
    UNIQUE (axis_id, code),
    CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(label)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(definition)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('active', 'retired'))
);

COMMENT ON TABLE recipeweave.axis_option IS '軸候補値';

COMMENT ON COLUMN recipeweave.axis_option.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.axis_option.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.axis_option.axis_id IS '親軸';

COMMENT ON COLUMN recipeweave.axis_option.code IS '値コード';

COMMENT ON COLUMN recipeweave.axis_option.label IS '候補名';

COMMENT ON COLUMN recipeweave.axis_option.definition IS '値の意味';

COMMENT ON COLUMN recipeweave.axis_option.parent_id IS '同軸の階層親';

COMMENT ON COLUMN recipeweave.axis_option.status IS '選択可否';

CREATE TABLE recipeweave.food_axis_option (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    food_id UUID NOT NULL,
    option_id UUID NOT NULL,
    UNIQUE (food_id, option_id)
);

COMMENT ON TABLE recipeweave.food_axis_option IS '食材の分類属性';

COMMENT ON COLUMN recipeweave.food_axis_option.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.food_axis_option.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.food_axis_option.food_id IS '食材';

COMMENT ON COLUMN recipeweave.food_axis_option.option_id IS 'カテゴリ・入手性等の値';

CREATE TABLE recipeweave.recipe (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    title TEXT NOT NULL,
    family_option_id UUID NOT NULL,
    status TEXT NOT NULL,
    withdrawal_reason TEXT,
    CHECK (status <> 'withdrawn' OR NULLIF(BTRIM(withdrawal_reason), '') IS NOT NULL),
    CHECK (LENGTH(BTRIM(title)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('draft', 'published', 'withdrawn'))
);

COMMENT ON TABLE recipeweave.recipe IS 'レシピ同一性';

COMMENT ON COLUMN recipeweave.recipe.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.recipe.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.recipe.title IS '代表名';

COMMENT ON COLUMN recipeweave.recipe.family_option_id IS '料理ファミリ';

COMMENT ON COLUMN recipeweave.recipe.status IS '公開状態';

COMMENT ON COLUMN recipeweave.recipe.withdrawal_reason IS '取下げ理由';

CREATE TABLE recipeweave.recipe_version (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    recipe_id UUID NOT NULL,
    version INTEGER NOT NULL,
    release_id UUID NOT NULL,
    base_servings NUMERIC(20, 6) NOT NULL,
    output_amount NUMERIC(20, 6) NOT NULL,
    output_unit_id UUID NOT NULL,
    status TEXT NOT NULL,
    validation TEXT NOT NULL,
    content_hash CHAR(64) NOT NULL,
    published_at TIMESTAMPTZ,
    UNIQUE (recipe_id, version),
    CHECK (version > 0),
    CHECK (base_servings > 0),
    CHECK (output_amount > 0),
    CHECK (status <> 'published' OR (validation = 'passed' AND published_at IS NOT NULL)),
    CHECK (base_servings IS NULL OR base_servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (output_amount IS NULL OR output_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('draft', 'published', 'withdrawn')),
    CHECK (LENGTH(BTRIM(validation)) BETWEEN 1 AND 20000),
    CHECK (validation IN ('pending', 'passed', 'failed', 'needs_review')),
    CHECK (content_hash IS NULL OR content_hash ~ '^[0-9a-f]{64}$')
);

COMMENT ON TABLE recipeweave.recipe_version IS 'レシピ内容版';

COMMENT ON COLUMN recipeweave.recipe_version.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.recipe_version.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.recipe_version.recipe_id IS '所属レシピ';

COMMENT ON COLUMN recipeweave.recipe_version.version IS '版番号';

COMMENT ON COLUMN recipeweave.recipe_version.release_id IS '採用カタログ版';

COMMENT ON COLUMN recipeweave.recipe_version.base_servings IS '登録分量が何人前か';

COMMENT ON COLUMN recipeweave.recipe_version.output_amount IS '完成量';

COMMENT ON COLUMN recipeweave.recipe_version.output_unit_id IS '完成量単位';

COMMENT ON COLUMN recipeweave.recipe_version.status IS '版の状態';

COMMENT ON COLUMN recipeweave.recipe_version.validation IS '公開審査';

COMMENT ON COLUMN recipeweave.recipe_version.content_hash IS '内容ハッシュ';

COMMENT ON COLUMN recipeweave.recipe_version.published_at IS '公開日時';

CREATE TABLE recipeweave.recipe_option (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    recipe_version_id UUID NOT NULL,
    option_id UUID NOT NULL,
    UNIQUE (recipe_version_id, option_id)
);

COMMENT ON TABLE recipeweave.recipe_option IS '版の分類・特徴';

COMMENT ON COLUMN recipeweave.recipe_option.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.recipe_option.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.recipe_option.recipe_version_id IS '対象版';

COMMENT ON COLUMN recipeweave.recipe_option.option_id IS '特徴値';

CREATE TABLE recipeweave.scaling_rule (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    name TEXT NOT NULL,
    mode TEXT NOT NULL,
    min_servings NUMERIC(20, 6) NOT NULL,
    max_servings NUMERIC(20, 6) NOT NULL,
    batch_capacity NUMERIC(20, 6),
    round_mode TEXT NOT NULL,
    round_increment NUMERIC(20, 6) NOT NULL,
    source_id UUID,
    CHECK (min_servings > 0),
    CHECK (max_servings >= min_servings),
    CHECK (round_increment > 0),
    CHECK (batch_capacity IS NULL OR batch_capacity > 0),
    CHECK (mode NOT IN ('fixed_batch', 'capacity_batch') OR batch_capacity IS NOT NULL),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(mode)) BETWEEN 1 AND 20000),
    CHECK (mode IN ('linear', 'fixed_batch', 'capacity_batch', 'validated_curve', 'manual')),
    CHECK (min_servings IS NULL OR min_servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (max_servings IS NULL OR max_servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (batch_capacity IS NULL OR batch_capacity::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (LENGTH(BTRIM(round_mode)) BETWEEN 1 AND 20000),
    CHECK (round_mode IN ('none', 'half_up', 'ceil')),
    CHECK (round_increment IS NULL OR round_increment::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.scaling_rule IS '人数変更規則';

COMMENT ON COLUMN recipeweave.scaling_rule.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.scaling_rule.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.scaling_rule.name IS '規則名';

COMMENT ON COLUMN recipeweave.scaling_rule.mode IS '比例・バッチ等';

COMMENT ON COLUMN recipeweave.scaling_rule.min_servings IS '検証済み人数下限';

COMMENT ON COLUMN recipeweave.scaling_rule.max_servings IS '検証済み人数上限';

COMMENT ON COLUMN recipeweave.scaling_rule.batch_capacity IS '1バッチ上限';

COMMENT ON COLUMN recipeweave.scaling_rule.round_mode IS '表示丸め';

COMMENT ON COLUMN recipeweave.scaling_rule.round_increment IS '表示・購入の刻み';

COMMENT ON COLUMN recipeweave.scaling_rule.source_id IS '検証根拠';

CREATE TABLE recipeweave.scaling_point (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    rule_id UUID NOT NULL,
    servings NUMERIC(20, 6) NOT NULL,
    multiplier NUMERIC(20, 6) NOT NULL,
    UNIQUE (rule_id, servings),
    CHECK (servings > 0),
    CHECK (multiplier > 0),
    CHECK (servings IS NULL OR servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (multiplier IS NULL OR multiplier::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.scaling_point IS '検証済み換算点';

COMMENT ON COLUMN recipeweave.scaling_point.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.scaling_point.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.scaling_point.rule_id IS '曲線規則';

COMMENT ON COLUMN recipeweave.scaling_point.servings IS '人数';

COMMENT ON COLUMN recipeweave.scaling_point.multiplier IS '登録量への倍率';

CREATE TABLE recipeweave.recipe_ingredient (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    recipe_version_id UUID NOT NULL,
    line_no INTEGER NOT NULL,
    form_id UUID NOT NULL,
    product_version_id UUID,
    component_id UUID,
    kit_parent_line_id UUID,
    role TEXT NOT NULL,
    demand_kind TEXT NOT NULL,
    amount_mode TEXT NOT NULL,
    amount NUMERIC(20, 6),
    amount_max NUMERIC(20, 6),
    unit_id UUID NOT NULL,
    canonical_amount NUMERIC(20, 6),
    conversion_id UUID,
    scaling_rule_id UUID NOT NULL,
    optional BOOLEAN NOT NULL,
    UNIQUE (recipe_version_id, line_no),
    CHECK (line_no > 0),
    CHECK (amount IS NULL OR amount > 0),
    CHECK (amount_max IS NULL OR amount_max > 0),
    CHECK (canonical_amount IS NULL OR canonical_amount > 0),
    CHECK (
        (
            amount_mode = 'exact'
            AND amount IS NOT NULL
            AND canonical_amount IS NOT NULL
            AND amount_max IS NULL
        )
        OR (
            amount_mode = 'range'
            AND amount IS NOT NULL
            AND amount_max IS NOT NULL
            AND amount_max >= amount
            AND canonical_amount IS NULL
        )
        OR (
            amount_mode = 'to_taste'
            AND amount IS NULL
            AND amount_max IS NULL
            AND canonical_amount IS NULL
        )
    ),
    CHECK (
        (
            demand_kind = 'kit_component'
            AND component_id IS NOT NULL
            AND kit_parent_line_id IS NOT NULL
        )
        OR (demand_kind <> 'kit_component' AND component_id IS NULL AND kit_parent_line_id IS NULL)
    ),
    CHECK (kit_parent_line_id IS NULL OR kit_parent_line_id <> id),
    CHECK (LENGTH(BTRIM(role)) BETWEEN 1 AND 20000),
    CHECK (role IN ('main', 'support', 'seasoning', 'aroma', 'texture', 'garnish', 'medium')),
    CHECK (LENGTH(BTRIM(demand_kind)) BETWEEN 1 AND 20000),
    CHECK (demand_kind IN ('purchase', 'utility', 'kit_component')),
    CHECK (LENGTH(BTRIM(amount_mode)) BETWEEN 1 AND 20000),
    CHECK (amount_mode IN ('exact', 'range', 'to_taste')),
    CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (amount_max IS NULL OR amount_max::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (
        canonical_amount IS NULL OR canonical_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')
    )
);

COMMENT ON TABLE recipeweave.recipe_ingredient IS 'レシピ材料明細';

COMMENT ON COLUMN recipeweave.recipe_ingredient.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.recipe_ingredient.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.recipe_ingredient.recipe_version_id IS '親版';

COMMENT ON COLUMN recipeweave.recipe_ingredient.line_no IS '表示順';

COMMENT ON COLUMN recipeweave.recipe_ingredient.form_id IS '使用形態';

COMMENT ON COLUMN recipeweave.recipe_ingredient.product_version_id IS '商品指定時の仕様版';

COMMENT ON COLUMN recipeweave.recipe_ingredient.component_id IS 'セット内構成品を使う場合';

COMMENT ON COLUMN recipeweave.recipe_ingredient.kit_parent_line_id IS '購入対象となるセットの親行';

COMMENT ON COLUMN recipeweave.recipe_ingredient.role IS '料理での役割';

COMMENT ON COLUMN recipeweave.recipe_ingredient.demand_kind IS '購入対象区分';

COMMENT ON COLUMN recipeweave.recipe_ingredient.amount_mode IS '確定/範囲/適量';

COMMENT ON COLUMN recipeweave.recipe_ingredient.amount IS '確定値または範囲下限';

COMMENT ON COLUMN recipeweave.recipe_ingredient.amount_max IS '範囲上限';

COMMENT ON COLUMN recipeweave.recipe_ingredient.unit_id IS '登録単位';

COMMENT ON COLUMN recipeweave.recipe_ingredient.canonical_amount IS '登録版の基準量';

COMMENT ON COLUMN recipeweave.recipe_ingredient.conversion_id IS '非基準単位の換算根拠';

COMMENT ON COLUMN recipeweave.recipe_ingredient.scaling_rule_id IS '人数変換規則';

COMMENT ON COLUMN recipeweave.recipe_ingredient.optional IS '任意追加材料';

CREATE TABLE recipeweave.operation (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    definition TEXT NOT NULL,
    precondition TEXT NOT NULL,
    completion_cue TEXT NOT NULL,
    status TEXT NOT NULL,
    UNIQUE (code),
    CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(definition)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(precondition)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(completion_cue)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('active', 'retired'))
);

COMMENT ON TABLE recipeweave.operation IS '標準調理動作';

COMMENT ON COLUMN recipeweave.operation.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.operation.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.operation.code IS 'cut_ginkgo等';

COMMENT ON COLUMN recipeweave.operation.name IS 'いちょう切り等';

COMMENT ON COLUMN recipeweave.operation.definition IS '動作の意味';

COMMENT ON COLUMN recipeweave.operation.precondition IS '入力食材・必要状態';

COMMENT ON COLUMN recipeweave.operation.completion_cue IS '完了確認方法';

COMMENT ON COLUMN recipeweave.operation.status IS '使用状態';

CREATE TABLE recipeweave.operation_parameter (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    operation_id UUID NOT NULL,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    value_type TEXT NOT NULL,
    unit_id UUID,
    required BOOLEAN NOT NULL,
    min_value NUMERIC(20, 6),
    max_value NUMERIC(20, 6),
    allowed_values JSONB,
    UNIQUE (operation_id, code),
    CHECK (min_value IS NULL OR max_value IS NULL OR min_value <= max_value),
    CHECK (
        (
            value_type = 'option'
            AND allowed_values IS NOT NULL
            AND JSONB_TYPEOF(allowed_values) = 'array'
            AND JSONB_ARRAY_LENGTH(allowed_values) BETWEEN 1 AND 100
        )
        OR (value_type <> 'option' AND allowed_values IS NULL)
    ),
    CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(value_type)) BETWEEN 1 AND 20000),
    CHECK (value_type IN ('decimal', 'integer', 'boolean', 'text', 'option')),
    CHECK (min_value IS NULL OR min_value::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (max_value IS NULL OR max_value::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (allowed_values IS NULL OR PG_COLUMN_SIZE(allowed_values) <= 1048576)
);

COMMENT ON TABLE recipeweave.operation_parameter IS '動作パラメータ定義';

COMMENT ON COLUMN recipeweave.operation_parameter.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.operation_parameter.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.operation_parameter.operation_id IS '動作';

COMMENT ON COLUMN recipeweave.operation_parameter.code IS 'thickness_mm等';

COMMENT ON COLUMN recipeweave.operation_parameter.name IS '厚さ等';

COMMENT ON COLUMN recipeweave.operation_parameter.value_type IS '値型';

COMMENT ON COLUMN recipeweave.operation_parameter.unit_id IS '単位';

COMMENT ON COLUMN recipeweave.operation_parameter.required IS '必須か';

COMMENT ON COLUMN recipeweave.operation_parameter.min_value IS '許容下限';

COMMENT ON COLUMN recipeweave.operation_parameter.max_value IS '許容上限';

COMMENT ON COLUMN recipeweave.operation_parameter.allowed_values IS 'option型の具体値配列';

CREATE TABLE recipeweave.recipe_step (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    recipe_version_id UUID NOT NULL,
    step_no INTEGER NOT NULL,
    operation_id UUID NOT NULL,
    instruction TEXT NOT NULL,
    attention TEXT NOT NULL,
    duration_min_s INTEGER NOT NULL,
    duration_max_s INTEGER NOT NULL,
    scaling_rule_id UUID NOT NULL,
    completion_cue TEXT NOT NULL,
    UNIQUE (recipe_version_id, step_no),
    CHECK (step_no > 0),
    CHECK (duration_min_s >= 0),
    CHECK (duration_max_s >= duration_min_s),
    CHECK (LENGTH(BTRIM(instruction)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(attention)) BETWEEN 1 AND 20000),
    CHECK (attention IN ('active', 'monitored', 'passive')),
    CHECK (LENGTH(BTRIM(completion_cue)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.recipe_step IS '調理工程ノード';

COMMENT ON COLUMN recipeweave.recipe_step.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.recipe_step.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.recipe_step.recipe_version_id IS '所属版';

COMMENT ON COLUMN recipeweave.recipe_step.step_no IS '表示順（依存順とは別）';

COMMENT ON COLUMN recipeweave.recipe_step.operation_id IS '標準動作';

COMMENT ON COLUMN recipeweave.recipe_step.instruction IS '個別補足';

COMMENT ON COLUMN recipeweave.recipe_step.attention IS '作業者拘束';

COMMENT ON COLUMN recipeweave.recipe_step.duration_min_s IS '所要秒下限';

COMMENT ON COLUMN recipeweave.recipe_step.duration_max_s IS '所要秒上限';

COMMENT ON COLUMN recipeweave.recipe_step.scaling_rule_id IS '時間の人数変更規則';

COMMENT ON COLUMN recipeweave.recipe_step.completion_cue IS '実測・目視の終了条件';

CREATE TABLE recipeweave.step_parameter (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    step_id UUID NOT NULL,
    parameter_id UUID NOT NULL,
    number_value NUMERIC(20, 6),
    text_value TEXT,
    bool_value BOOLEAN,
    UNIQUE (step_id, parameter_id),
    CHECK (NUM_NONNULLS(number_value, text_value, bool_value) = 1),
    CHECK (number_value IS NULL OR number_value::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.step_parameter IS '工程の型付きパラメータ';

COMMENT ON COLUMN recipeweave.step_parameter.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.step_parameter.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.step_parameter.step_id IS '対象工程';

COMMENT ON COLUMN recipeweave.step_parameter.parameter_id IS '動作パラメータ';

COMMENT ON COLUMN recipeweave.step_parameter.number_value IS '数値';

COMMENT ON COLUMN recipeweave.step_parameter.text_value IS '文字・optionコード';

COMMENT ON COLUMN recipeweave.step_parameter.bool_value IS '真偽';

CREATE TABLE recipeweave.material_node (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    recipe_version_id UUID NOT NULL,
    name TEXT NOT NULL,
    kind TEXT NOT NULL,
    ingredient_line_id UUID,
    producer_step_id UUID,
    amount NUMERIC(20, 6),
    unit_id UUID,
    CHECK (
        (kind = 'ingredient' AND ingredient_line_id IS NOT NULL AND producer_step_id IS NULL)
        OR (kind <> 'ingredient' AND ingredient_line_id IS NULL AND producer_step_id IS NOT NULL)
    ),
    CHECK (amount IS NULL OR amount > 0),
    CHECK ((amount IS NULL) = (unit_id IS NULL)),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(kind)) BETWEEN 1 AND 20000),
    CHECK (kind IN ('ingredient', 'intermediate', 'dish', 'waste')),
    CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.material_node IS '材料・中間物ノード';

COMMENT ON COLUMN recipeweave.material_node.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.material_node.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.material_node.recipe_version_id IS '親版';

COMMENT ON COLUMN recipeweave.material_node.name IS '切ったにんじん・合わせ調味料等';

COMMENT ON COLUMN recipeweave.material_node.kind IS '入力/中間/完成/廃棄';

COMMENT ON COLUMN recipeweave.material_node.ingredient_line_id IS '原材料明細';

COMMENT ON COLUMN recipeweave.material_node.producer_step_id IS '生成工程';

COMMENT ON COLUMN recipeweave.material_node.amount IS '予定生成量';

COMMENT ON COLUMN recipeweave.material_node.unit_id IS '生成量単位';

CREATE TABLE recipeweave.step_input (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    step_id UUID NOT NULL,
    material_id UUID NOT NULL,
    fraction NUMERIC(20, 6) NOT NULL,
    UNIQUE (step_id, material_id),
    CHECK (fraction > 0 AND fraction <= 1),
    CHECK (fraction IS NULL OR fraction::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.step_input IS '工程への材料受渡し';

COMMENT ON COLUMN recipeweave.step_input.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.step_input.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.step_input.step_id IS '受取工程';

COMMENT ON COLUMN recipeweave.step_input.material_id IS '受け渡す材料';

COMMENT ON COLUMN recipeweave.step_input.fraction IS '当該ノード生成量の利用割合';

CREATE TABLE recipeweave.step_dependency (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    before_step_id UUID NOT NULL,
    after_step_id UUID NOT NULL,
    kind TEXT NOT NULL,
    min_lag_s INTEGER NOT NULL,
    max_lag_s INTEGER,
    UNIQUE (before_step_id, after_step_id, kind),
    CHECK (before_step_id <> after_step_id),
    CHECK (min_lag_s >= 0),
    CHECK (max_lag_s IS NULL OR max_lag_s >= min_lag_s),
    CHECK (LENGTH(BTRIM(kind)) BETWEEN 1 AND 20000),
    CHECK (kind IN ('material', 'sequence', 'safety', 'quality'))
);

COMMENT ON TABLE recipeweave.step_dependency IS '工程依存辺';

COMMENT ON COLUMN recipeweave.step_dependency.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.step_dependency.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.step_dependency.before_step_id IS '先行工程';

COMMENT ON COLUMN recipeweave.step_dependency.after_step_id IS '後続工程';

COMMENT ON COLUMN recipeweave.step_dependency.kind IS '依存理由';

COMMENT ON COLUMN recipeweave.step_dependency.min_lag_s IS '完了後最低待機';

COMMENT ON COLUMN recipeweave.step_dependency.max_lag_s IS '品質上の最大待機';

CREATE TABLE recipeweave.resource_type (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    capacity_unit_id UUID,
    status TEXT NOT NULL,
    UNIQUE (code),
    CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('active', 'retired'))
);

COMMENT ON TABLE recipeweave.resource_type IS '道具・設備・作業者種別';

COMMENT ON COLUMN recipeweave.resource_type.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.resource_type.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.resource_type.code IS 'burner/pan/person等';

COMMENT ON COLUMN recipeweave.resource_type.name IS '道具名';

COMMENT ON COLUMN recipeweave.resource_type.capacity_unit_id IS '鍋容量等の単位';

COMMENT ON COLUMN recipeweave.resource_type.status IS '使用状態';

CREATE TABLE recipeweave.step_resource (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    step_id UUID NOT NULL,
    resource_type_id UUID NOT NULL,
    quantity INTEGER NOT NULL,
    capacity_min NUMERIC(20, 6),
    exclusive BOOLEAN NOT NULL,
    UNIQUE (step_id, resource_type_id),
    CHECK (quantity > 0),
    CHECK (capacity_min IS NULL OR capacity_min > 0),
    CHECK (capacity_min IS NULL OR capacity_min::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.step_resource IS '工程の資源要求';

COMMENT ON COLUMN recipeweave.step_resource.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.step_resource.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.step_resource.step_id IS '対象工程';

COMMENT ON COLUMN recipeweave.step_resource.resource_type_id IS '要求種別';

COMMENT ON COLUMN recipeweave.step_resource.quantity IS '必要台数・人数';

COMMENT ON COLUMN recipeweave.step_resource.capacity_min IS '必要最低容量';

COMMENT ON COLUMN recipeweave.step_resource.exclusive IS '占有するか';

CREATE TABLE recipeweave.media_asset (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    operation_id UUID NOT NULL,
    media_type TEXT NOT NULL,
    uri TEXT NOT NULL,
    sha256 CHAR(64) NOT NULL,
    locale TEXT NOT NULL,
    version INTEGER NOT NULL,
    parameter_contract JSONB NOT NULL,
    source_id UUID NOT NULL,
    validation TEXT NOT NULL,
    UNIQUE (operation_id, locale, version, media_type),
    CHECK (version > 0),
    CHECK (LENGTH(BTRIM(media_type)) BETWEEN 1 AND 20000),
    CHECK (media_type IN ('video', 'animation', 'image')),
    CHECK (LENGTH(BTRIM(uri)) BETWEEN 1 AND 20000),
    CHECK (sha256 IS NULL OR sha256 ~ '^[0-9a-f]{64}$'),
    CHECK (LENGTH(BTRIM(locale)) BETWEEN 1 AND 20000),
    CHECK (parameter_contract IS NULL OR PG_COLUMN_SIZE(parameter_contract) <= 1048576),
    CHECK (LENGTH(BTRIM(validation)) BETWEEN 1 AND 20000),
    CHECK (validation IN ('pending', 'passed', 'failed', 'needs_review'))
);

COMMENT ON TABLE recipeweave.media_asset IS '教育用動画等の版';

COMMENT ON COLUMN recipeweave.media_asset.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.media_asset.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.media_asset.operation_id IS '説明する標準動作';

COMMENT ON COLUMN recipeweave.media_asset.media_type IS '動画/アニメ/画像';

COMMENT ON COLUMN recipeweave.media_asset.uri IS 'オブジェクト格納先';

COMMENT ON COLUMN recipeweave.media_asset.sha256 IS '資産ハッシュ';

COMMENT ON COLUMN recipeweave.media_asset.locale IS '字幕言語';

COMMENT ON COLUMN recipeweave.media_asset.version IS '媒体版';

COMMENT ON COLUMN recipeweave.media_asset.parameter_contract IS '対応厚み・食材形状・視点';

COMMENT ON COLUMN recipeweave.media_asset.source_id IS '権利・作成根拠';

COMMENT ON COLUMN recipeweave.media_asset.validation IS '内容検証';

CREATE TABLE recipeweave.step_media (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    step_id UUID NOT NULL,
    media_id UUID NOT NULL,
    start_ms INTEGER NOT NULL,
    end_ms INTEGER NOT NULL,
    UNIQUE (step_id, media_id),
    CHECK (start_ms >= 0),
    CHECK (end_ms > start_ms)
);

COMMENT ON TABLE recipeweave.step_media IS '工程別メディア選択';

COMMENT ON COLUMN recipeweave.step_media.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.step_media.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.step_media.step_id IS '対象工程';

COMMENT ON COLUMN recipeweave.step_media.media_id IS '適用メディア';

COMMENT ON COLUMN recipeweave.step_media.start_ms IS '表示開始点';

COMMENT ON COLUMN recipeweave.step_media.end_ms IS '終了点';

CREATE TABLE recipeweave.generation_policy (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version TEXT NOT NULL,
    prompt_template TEXT NOT NULL,
    model_identifier TEXT NOT NULL,
    parameter_json JSONB NOT NULL,
    schema_version TEXT NOT NULL,
    release_id UUID NOT NULL,
    UNIQUE (version),
    CHECK (LENGTH(BTRIM(version)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(prompt_template)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(model_identifier)) BETWEEN 1 AND 20000),
    CHECK (parameter_json IS NULL OR PG_COLUMN_SIZE(parameter_json) <= 1048576),
    CHECK (LENGTH(BTRIM(schema_version)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.generation_policy IS 'AI生成方針版';

COMMENT ON COLUMN recipeweave.generation_policy.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.generation_policy.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.generation_policy.version IS '方針識別子';

COMMENT ON COLUMN recipeweave.generation_policy.prompt_template IS '入力テンプレ';

COMMENT ON COLUMN recipeweave.generation_policy.model_identifier IS '利用モデル名・版';

COMMENT ON COLUMN recipeweave.generation_policy.parameter_json IS 'temperature/seed等の記録';

COMMENT ON COLUMN recipeweave.generation_policy.schema_version IS '出力JSON契約';

COMMENT ON COLUMN recipeweave.generation_policy.release_id IS '候補カタログ版';

CREATE TABLE recipeweave.generation_job (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    policy_id UUID NOT NULL,
    idempotency_key CHAR(64) NOT NULL,
    status TEXT NOT NULL,
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    seed INTEGER,
    error_code TEXT,
    attempt_count INTEGER NOT NULL,
    UNIQUE (idempotency_key),
    CHECK (attempt_count >= 0),
    CHECK (finished_at IS NULL OR (started_at IS NOT NULL AND finished_at >= started_at)),
    CHECK (idempotency_key IS NULL OR idempotency_key ~ '^[0-9a-f]{64}$'),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('queued', 'running', 'succeeded', 'failed', 'cancelled'))
);

COMMENT ON TABLE recipeweave.generation_job IS '事前生成ジョブ';

COMMENT ON COLUMN recipeweave.generation_job.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.generation_job.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.generation_job.policy_id IS '実行方針';

COMMENT ON COLUMN recipeweave.generation_job.idempotency_key IS '入力と方針から作る重複キー';

COMMENT ON COLUMN recipeweave.generation_job.status IS '進行状態';

COMMENT ON COLUMN recipeweave.generation_job.started_at IS '開始';

COMMENT ON COLUMN recipeweave.generation_job.finished_at IS '終了';

COMMENT ON COLUMN recipeweave.generation_job.seed IS '再現用seed';

COMMENT ON COLUMN recipeweave.generation_job.error_code IS '失敗分類';

COMMENT ON COLUMN recipeweave.generation_job.attempt_count IS '試行回数';

CREATE TABLE recipeweave.generation_choice (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    job_id UUID NOT NULL,
    option_id UUID NOT NULL,
    UNIQUE (job_id, option_id)
);

COMMENT ON TABLE recipeweave.generation_choice IS '生成軸の選択値';

COMMENT ON COLUMN recipeweave.generation_choice.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.generation_choice.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.generation_choice.job_id IS '実行';

COMMENT ON COLUMN recipeweave.generation_choice.option_id IS '選択した軸候補';

CREATE TABLE recipeweave.generation_food (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    job_id UUID NOT NULL,
    form_id UUID NOT NULL,
    role TEXT NOT NULL,
    UNIQUE (job_id, form_id, role),
    CHECK (LENGTH(BTRIM(role)) BETWEEN 1 AND 20000),
    CHECK (role IN ('main', 'support', 'seasoning', 'aroma', 'texture', 'garnish', 'medium'))
);

COMMENT ON TABLE recipeweave.generation_food IS '生成の食材入力';

COMMENT ON COLUMN recipeweave.generation_food.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.generation_food.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.generation_food.job_id IS '実行';

COMMENT ON COLUMN recipeweave.generation_food.form_id IS '食材形態';

COMMENT ON COLUMN recipeweave.generation_food.role IS '役割';

CREATE TABLE recipeweave.generation_result (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    recipe_version_id UUID NOT NULL,
    job_id UUID,
    policy_id UUID NOT NULL,
    input_snapshot JSONB NOT NULL,
    raw_output_uri TEXT,
    raw_output_hash CHAR(64) NOT NULL,
    UNIQUE (recipe_version_id),
    CHECK (input_snapshot IS NULL OR PG_COLUMN_SIZE(input_snapshot) <= 1048576),
    CHECK (raw_output_hash IS NULL OR raw_output_hash ~ '^[0-9a-f]{64}$')
);

COMMENT ON TABLE recipeweave.generation_result IS '生成結果の出自';

COMMENT ON COLUMN recipeweave.generation_result.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.generation_result.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.generation_result.recipe_version_id IS '生成した版';

COMMENT ON COLUMN recipeweave.generation_result.job_id IS '短期ジョブ参照';

COMMENT ON COLUMN recipeweave.generation_result.policy_id IS '恒久方針参照';

COMMENT ON COLUMN recipeweave.generation_result.input_snapshot IS '確定入力をschema_versionで検証';

COMMENT ON COLUMN recipeweave.generation_result.raw_output_uri IS '原出力保存先';

COMMENT ON COLUMN recipeweave.generation_result.raw_output_hash IS '原出力ハッシュ';

CREATE TABLE recipeweave.compatibility_rule (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    code TEXT NOT NULL,
    version INTEGER NOT NULL,
    severity TEXT NOT NULL,
    predicate JSONB NOT NULL,
    message TEXT NOT NULL,
    source_id UUID,
    status TEXT NOT NULL,
    UNIQUE (code, version),
    CHECK (version > 0),
    CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(severity)) BETWEEN 1 AND 20000),
    CHECK (severity IN ('block', 'review', 'score')),
    CHECK (predicate IS NULL OR PG_COLUMN_SIZE(predicate) <= 1048576),
    CHECK (LENGTH(BTRIM(message)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('active', 'retired'))
);

COMMENT ON TABLE recipeweave.compatibility_rule IS '組み合わせ・公開ルール';

COMMENT ON COLUMN recipeweave.compatibility_rule.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.compatibility_rule.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.compatibility_rule.code IS '規則コード';

COMMENT ON COLUMN recipeweave.compatibility_rule.version IS '規則版';

COMMENT ON COLUMN recipeweave.compatibility_rule.severity IS '除外/保留/順位';

COMMENT ON COLUMN recipeweave.compatibility_rule.predicate IS '型付き条件式';

COMMENT ON COLUMN recipeweave.compatibility_rule.message IS '理由';

COMMENT ON COLUMN recipeweave.compatibility_rule.source_id IS '根拠';

COMMENT ON COLUMN recipeweave.compatibility_rule.status IS '利用状態';

CREATE TABLE recipeweave.validation_result (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    recipe_version_id UUID NOT NULL,
    rule_id UUID NOT NULL,
    state TEXT NOT NULL,
    evidence JSONB NOT NULL,
    validator_version TEXT NOT NULL,
    evaluated_at TIMESTAMPTZ NOT NULL,
    CHECK (LENGTH(BTRIM(state)) BETWEEN 1 AND 20000),
    CHECK (state IN ('pending', 'passed', 'failed', 'needs_review')),
    CHECK (evidence IS NULL OR PG_COLUMN_SIZE(evidence) <= 1048576),
    CHECK (LENGTH(BTRIM(validator_version)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.validation_result IS '公開前評価結果';

COMMENT ON COLUMN recipeweave.validation_result.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.validation_result.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.validation_result.recipe_version_id IS '対象版';

COMMENT ON COLUMN recipeweave.validation_result.rule_id IS '適用規則版';

COMMENT ON COLUMN recipeweave.validation_result.state IS '結果';

COMMENT ON COLUMN recipeweave.validation_result.evidence IS '検査箇所・値・根拠';

COMMENT ON COLUMN recipeweave.validation_result.validator_version IS '検証器版';

COMMENT ON COLUMN recipeweave.validation_result.evaluated_at IS '検査日時';

CREATE TABLE recipeweave.recipe_signature (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    recipe_version_id UUID NOT NULL,
    algorithm_version TEXT NOT NULL,
    exact_hash CHAR(64) NOT NULL,
    canonical_payload JSONB NOT NULL,
    cluster_key TEXT NOT NULL,
    UNIQUE (recipe_version_id, algorithm_version),
    CHECK (LENGTH(BTRIM(algorithm_version)) BETWEEN 1 AND 20000),
    CHECK (exact_hash IS NULL OR exact_hash ~ '^[0-9a-f]{64}$'),
    CHECK (canonical_payload IS NULL OR PG_COLUMN_SIZE(canonical_payload) <= 1048576),
    CHECK (LENGTH(BTRIM(cluster_key)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.recipe_signature IS '内容重複判定署名';

COMMENT ON COLUMN recipeweave.recipe_signature.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.recipe_signature.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.recipe_signature.recipe_version_id IS '対象版';

COMMENT ON COLUMN recipeweave.recipe_signature.algorithm_version IS '正規化アルゴリズム版';

COMMENT ON COLUMN recipeweave.recipe_signature.exact_hash IS '材料比率・工程・主要条件のハッシュ';

COMMENT ON COLUMN recipeweave.recipe_signature.canonical_payload IS '正規化対象の監査用内容';

COMMENT ON COLUMN recipeweave.recipe_signature.cluster_key IS '料理近似群キー';

CREATE TABLE recipeweave.recipe_similarity (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    left_version_id UUID NOT NULL,
    right_version_id UUID NOT NULL,
    algorithm_version TEXT NOT NULL,
    score NUMERIC(20, 6) NOT NULL,
    explanation TEXT NOT NULL,
    UNIQUE (left_version_id, right_version_id, algorithm_version),
    CHECK (left_version_id < right_version_id),
    CHECK (score >= 0 AND score <= 1),
    CHECK (LENGTH(BTRIM(algorithm_version)) BETWEEN 1 AND 20000),
    CHECK (score IS NULL OR score::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (LENGTH(BTRIM(explanation)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.recipe_similarity IS '近似レシピ関係';

COMMENT ON COLUMN recipeweave.recipe_similarity.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.recipe_similarity.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.recipe_similarity.left_version_id IS '左版';

COMMENT ON COLUMN recipeweave.recipe_similarity.right_version_id IS '右版';

COMMENT ON COLUMN recipeweave.recipe_similarity.algorithm_version IS '評価器版';

COMMENT ON COLUMN recipeweave.recipe_similarity.score IS '類似度0..1';

COMMENT ON COLUMN recipeweave.recipe_similarity.explanation IS '材料/味付/工程の一致差分';

CREATE TABLE recipeweave.app_user (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    auth_subject TEXT NOT NULL,
    state TEXT NOT NULL,
    locale TEXT NOT NULL,
    timezone TEXT NOT NULL,
    UNIQUE (auth_subject),
    CHECK (LENGTH(BTRIM(auth_subject)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(state)) BETWEEN 1 AND 20000),
    CHECK (state IN ('active', 'erasure_pending')),
    CHECK (LENGTH(BTRIM(locale)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(timezone)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.app_user IS 'アプリ利用者';

COMMENT ON COLUMN recipeweave.app_user.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.app_user.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.app_user.auth_subject IS '認証基盤の不透明識別子';

COMMENT ON COLUMN recipeweave.app_user.state IS '利用/削除処理';

COMMENT ON COLUMN recipeweave.app_user.locale IS '表示言語';

COMMENT ON COLUMN recipeweave.app_user.timezone IS 'IANAタイムゾーン';

CREATE TABLE recipeweave.user_preference (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    option_id UUID NOT NULL,
    weight NUMERIC(20, 6) NOT NULL,
    UNIQUE (user_id, option_id),
    CHECK (weight IS NULL OR weight::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.user_preference IS 'ユーザーの嗜好';

COMMENT ON COLUMN recipeweave.user_preference.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.user_preference.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.user_preference.user_id IS '利用者';

COMMENT ON COLUMN recipeweave.user_preference.option_id IS '味・料理等';

COMMENT ON COLUMN recipeweave.user_preference.weight IS '好みの重み';

CREATE TABLE recipeweave.user_exclusion (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    food_id UUID,
    allergen_id UUID,
    strict BOOLEAN NOT NULL,
    CHECK (NUM_NONNULLS(food_id, allergen_id) = 1)
);

COMMENT ON TABLE recipeweave.user_exclusion IS '避けたい食材・物質';

COMMENT ON COLUMN recipeweave.user_exclusion.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.user_exclusion.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.user_exclusion.user_id IS '利用者';

COMMENT ON COLUMN recipeweave.user_exclusion.food_id IS '食材';

COMMENT ON COLUMN recipeweave.user_exclusion.allergen_id IS 'アレルゲン';

COMMENT ON COLUMN recipeweave.user_exclusion.strict IS '不明も除外するか';

CREATE TABLE recipeweave.user_recipe_event (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    recipe_version_id UUID NOT NULL,
    kind TEXT NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL,
    request_key TEXT NOT NULL,
    UNIQUE (user_id, request_key, recipe_version_id, kind),
    CHECK (LENGTH(BTRIM(kind)) BETWEEN 1 AND 20000),
    CHECK (kind IN ('shown', 'cooked', 'liked', 'disliked')),
    CHECK (LENGTH(BTRIM(request_key)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.user_recipe_event IS '提案・調理履歴';

COMMENT ON COLUMN recipeweave.user_recipe_event.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.user_recipe_event.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.user_recipe_event.user_id IS '利用者';

COMMENT ON COLUMN recipeweave.user_recipe_event.recipe_version_id IS '提案版';

COMMENT ON COLUMN recipeweave.user_recipe_event.kind IS '提示/調理/評価';

COMMENT ON COLUMN recipeweave.user_recipe_event.occurred_at IS '発生時刻';

COMMENT ON COLUMN recipeweave.user_recipe_event.request_key IS 'リクエスト識別子';

CREATE TABLE recipeweave.menu (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    name TEXT NOT NULL,
    servings NUMERIC(20, 6) NOT NULL,
    revision INTEGER NOT NULL,
    CHECK (servings > 0),
    CHECK (revision > 0),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (servings IS NULL OR servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.menu IS '献立';

COMMENT ON COLUMN recipeweave.menu.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.menu.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.menu.user_id IS '所有者';

COMMENT ON COLUMN recipeweave.menu.name IS '献立名';

COMMENT ON COLUMN recipeweave.menu.servings IS '標準人数';

COMMENT ON COLUMN recipeweave.menu.revision IS '楽観ロック版';

CREATE TABLE recipeweave.menu_item (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    menu_id UUID NOT NULL,
    recipe_version_id UUID NOT NULL,
    servings NUMERIC(20, 6) NOT NULL,
    role_option_id UUID NOT NULL,
    position INTEGER NOT NULL,
    UNIQUE (menu_id, position),
    CHECK (servings > 0),
    CHECK (position > 0),
    CHECK (servings IS NULL OR servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.menu_item IS '献立の料理';

COMMENT ON COLUMN recipeweave.menu_item.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.menu_item.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.menu_item.menu_id IS '献立';

COMMENT ON COLUMN recipeweave.menu_item.recipe_version_id IS '固定レシピ版';

COMMENT ON COLUMN recipeweave.menu_item.servings IS 'その料理を作る人数';

COMMENT ON COLUMN recipeweave.menu_item.role_option_id IS '主菜等';

COMMENT ON COLUMN recipeweave.menu_item.position IS '表示順';

CREATE TABLE recipeweave.menu_ingredient_override (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    menu_item_id UUID NOT NULL,
    ingredient_line_id UUID NOT NULL,
    selected BOOLEAN NOT NULL,
    amount NUMERIC(20, 6),
    form_id UUID,
    product_version_id UUID,
    UNIQUE (menu_item_id, ingredient_line_id),
    CHECK (amount IS NULL OR amount > 0),
    CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.menu_ingredient_override IS '献立別材料確定';

COMMENT ON COLUMN recipeweave.menu_ingredient_override.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.menu_ingredient_override.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.menu_ingredient_override.menu_item_id IS '対象料理';

COMMENT ON COLUMN recipeweave.menu_ingredient_override.ingredient_line_id IS '元材料行';

COMMENT ON COLUMN recipeweave.menu_ingredient_override.selected IS '任意材料を使うか';

COMMENT ON COLUMN recipeweave.menu_ingredient_override.amount IS '適量等の確定基準量';

COMMENT ON COLUMN recipeweave.menu_ingredient_override.form_id IS '明示的代替形態';

COMMENT ON COLUMN recipeweave.menu_ingredient_override.product_version_id IS '購入商品指定';

CREATE TABLE recipeweave.kitchen_resource (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    resource_type_id UUID NOT NULL,
    name TEXT NOT NULL,
    capacity NUMERIC(20, 6),
    quantity INTEGER NOT NULL,
    CHECK (quantity > 0),
    CHECK (capacity IS NULL OR capacity > 0),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (capacity IS NULL OR capacity::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.kitchen_resource IS 'キッチンの実資源';

COMMENT ON COLUMN recipeweave.kitchen_resource.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.kitchen_resource.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.kitchen_resource.user_id IS '所有者';

COMMENT ON COLUMN recipeweave.kitchen_resource.resource_type_id IS 'コンロ・鍋・人等';

COMMENT ON COLUMN recipeweave.kitchen_resource.name IS '左コンロ・26cmフライパン等';

COMMENT ON COLUMN recipeweave.kitchen_resource.capacity IS '容量';

COMMENT ON COLUMN recipeweave.kitchen_resource.quantity IS '同等資源数';

CREATE TABLE recipeweave.cooking_session (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    menu_id UUID NOT NULL,
    menu_revision INTEGER NOT NULL,
    status TEXT NOT NULL,
    target_at TIMESTAMPTZ,
    planner_version TEXT NOT NULL,
    input_snapshot JSONB NOT NULL,
    input_hash CHAR(64) NOT NULL,
    CHECK (menu_revision > 0),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('planned', 'cooking', 'completed', 'cancelled')),
    CHECK (LENGTH(BTRIM(planner_version)) BETWEEN 1 AND 20000),
    CHECK (input_snapshot IS NULL OR PG_COLUMN_SIZE(input_snapshot) <= 1048576),
    CHECK (input_hash IS NULL OR input_hash ~ '^[0-9a-f]{64}$')
);

COMMENT ON TABLE recipeweave.cooking_session IS '調理計画実行';

COMMENT ON COLUMN recipeweave.cooking_session.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.cooking_session.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.cooking_session.menu_id IS '対象献立';

COMMENT ON COLUMN recipeweave.cooking_session.menu_revision IS '献立版';

COMMENT ON COLUMN recipeweave.cooking_session.status IS '実行状態';

COMMENT ON COLUMN recipeweave.cooking_session.target_at IS '完成希望時刻';

COMMENT ON COLUMN recipeweave.cooking_session.planner_version IS '計画器の版';

COMMENT ON COLUMN recipeweave.cooking_session.input_snapshot IS '材料・資源・人数の固定入力';

COMMENT ON COLUMN recipeweave.cooking_session.input_hash IS '入力ハッシュ';

CREATE TABLE recipeweave.session_task (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    session_id UUID NOT NULL,
    menu_item_id UUID NOT NULL,
    step_id UUID NOT NULL,
    batch_no INTEGER NOT NULL,
    planned_start_s INTEGER NOT NULL,
    planned_end_s INTEGER NOT NULL,
    status TEXT NOT NULL,
    actual_start_at TIMESTAMPTZ,
    actual_end_at TIMESTAMPTZ,
    UNIQUE (session_id, menu_item_id, step_id, batch_no),
    CHECK (batch_no > 0),
    CHECK (planned_start_s >= 0),
    CHECK (planned_end_s >= planned_start_s),
    CHECK (
        actual_end_at IS NULL OR (actual_start_at IS NOT NULL AND actual_end_at >= actual_start_at)
    ),
    CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000),
    CHECK (status IN ('pending', 'running', 'completed', 'skipped'))
);

COMMENT ON TABLE recipeweave.session_task IS '展開済み工程';

COMMENT ON COLUMN recipeweave.session_task.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.session_task.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.session_task.session_id IS '実行';

COMMENT ON COLUMN recipeweave.session_task.menu_item_id IS '料理';

COMMENT ON COLUMN recipeweave.session_task.step_id IS '元工程';

COMMENT ON COLUMN recipeweave.session_task.batch_no IS '容量分割した回';

COMMENT ON COLUMN recipeweave.session_task.planned_start_s IS '開始相対秒';

COMMENT ON COLUMN recipeweave.session_task.planned_end_s IS '終了相対秒';

COMMENT ON COLUMN recipeweave.session_task.status IS '進捗';

COMMENT ON COLUMN recipeweave.session_task.actual_start_at IS '実開始';

COMMENT ON COLUMN recipeweave.session_task.actual_end_at IS '実完了';

CREATE TABLE recipeweave.task_dependency (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    before_task_id UUID NOT NULL,
    after_task_id UUID NOT NULL,
    min_lag_s INTEGER NOT NULL,
    max_lag_s INTEGER,
    reason TEXT NOT NULL,
    UNIQUE (before_task_id, after_task_id),
    CHECK (before_task_id <> after_task_id),
    CHECK (min_lag_s >= 0),
    CHECK (max_lag_s IS NULL OR max_lag_s >= min_lag_s),
    CHECK (LENGTH(BTRIM(reason)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.task_dependency IS '献立展開後依存';

COMMENT ON COLUMN recipeweave.task_dependency.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.task_dependency.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.task_dependency.before_task_id IS '先行タスク';

COMMENT ON COLUMN recipeweave.task_dependency.after_task_id IS '後続タスク';

COMMENT ON COLUMN recipeweave.task_dependency.min_lag_s IS '最小間隔';

COMMENT ON COLUMN recipeweave.task_dependency.max_lag_s IS '最大間隔';

COMMENT ON COLUMN recipeweave.task_dependency.reason IS '元DAG/洗浄/設備切替等';

CREATE TABLE recipeweave.resource_reservation (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    task_id UUID NOT NULL,
    resource_id UUID NOT NULL,
    start_s INTEGER NOT NULL,
    end_s INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    CHECK (start_s >= 0),
    CHECK (end_s > start_s),
    CHECK (quantity > 0)
);

COMMENT ON TABLE recipeweave.resource_reservation IS '資源の予約';

COMMENT ON COLUMN recipeweave.resource_reservation.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.resource_reservation.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.resource_reservation.task_id IS '使用タスク';

COMMENT ON COLUMN recipeweave.resource_reservation.resource_id IS '実資源';

COMMENT ON COLUMN recipeweave.resource_reservation.start_s IS '占有開始';

COMMENT ON COLUMN recipeweave.resource_reservation.end_s IS '占有終了';

COMMENT ON COLUMN recipeweave.resource_reservation.quantity IS '占有量';

CREATE TABLE recipeweave.ingredient_total (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    session_id UUID NOT NULL,
    form_id UUID NOT NULL,
    product_version_id UUID,
    unit_id UUID NOT NULL,
    required_amount NUMERIC(20, 6) NOT NULL,
    quality TEXT NOT NULL,
    calculation_version TEXT NOT NULL,
    UNIQUE NULLS NOT DISTINCT (session_id, form_id, product_version_id, unit_id),
    CHECK (required_amount >= 0),
    CHECK (
        required_amount IS NULL OR required_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')
    ),
    CHECK (LENGTH(BTRIM(quality)) BETWEEN 1 AND 20000),
    CHECK (quality IN ('measured', 'manufacturer', 'reference', 'estimated', 'unknown')),
    CHECK (LENGTH(BTRIM(calculation_version)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.ingredient_total IS '献立材料集計結果';

COMMENT ON COLUMN recipeweave.ingredient_total.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.ingredient_total.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.ingredient_total.session_id IS '固定計算対象';

COMMENT ON COLUMN recipeweave.ingredient_total.form_id IS '合算可能な形態';

COMMENT ON COLUMN recipeweave.ingredient_total.product_version_id IS '商品固定';

COMMENT ON COLUMN recipeweave.ingredient_total.unit_id IS '基準単位';

COMMENT ON COLUMN recipeweave.ingredient_total.required_amount IS '必要量';

COMMENT ON COLUMN recipeweave.ingredient_total.quality IS '最も低い入力精度';

COMMENT ON COLUMN recipeweave.ingredient_total.calculation_version IS '計算器版';

CREATE TABLE recipeweave.pantry_lot (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id UUID NOT NULL,
    form_id UUID NOT NULL,
    product_version_id UUID,
    amount NUMERIC(20, 6) NOT NULL,
    unit_id UUID NOT NULL,
    expires_on DATE,
    opened_at TIMESTAMPTZ,
    CHECK (amount >= 0),
    CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.pantry_lot IS '手持ち食材ロット';

COMMENT ON COLUMN recipeweave.pantry_lot.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.pantry_lot.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.pantry_lot.user_id IS '所有者';

COMMENT ON COLUMN recipeweave.pantry_lot.form_id IS '食材形態';

COMMENT ON COLUMN recipeweave.pantry_lot.product_version_id IS '商品版';

COMMENT ON COLUMN recipeweave.pantry_lot.amount IS '残量';

COMMENT ON COLUMN recipeweave.pantry_lot.unit_id IS '単位';

COMMENT ON COLUMN recipeweave.pantry_lot.expires_on IS '表示期限';

COMMENT ON COLUMN recipeweave.pantry_lot.opened_at IS '開封時点';

CREATE TABLE recipeweave.shopping_item (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    session_id UUID NOT NULL,
    total_id UUID NOT NULL,
    product_version_id UUID,
    net_shortage NUMERIC(20, 6) NOT NULL,
    package_count INTEGER,
    surplus_amount NUMERIC(20, 6),
    checked BOOLEAN NOT NULL,
    CHECK (net_shortage >= 0),
    CHECK (package_count IS NULL OR package_count >= 0),
    CHECK (surplus_amount IS NULL OR surplus_amount >= 0),
    CHECK (net_shortage IS NULL OR net_shortage::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (surplus_amount IS NULL OR surplus_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
);

COMMENT ON TABLE recipeweave.shopping_item IS '買い物行';

COMMENT ON COLUMN recipeweave.shopping_item.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.shopping_item.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.shopping_item.session_id IS '対象調理';

COMMENT ON COLUMN recipeweave.shopping_item.total_id IS '需要行';

COMMENT ON COLUMN recipeweave.shopping_item.product_version_id IS '購入SKU';

COMMENT ON COLUMN recipeweave.shopping_item.net_shortage IS '在庫控除後の不足量';

COMMENT ON COLUMN recipeweave.shopping_item.package_count IS '購入包装数';

COMMENT ON COLUMN recipeweave.shopping_item.surplus_amount IS '購入後余剰';

COMMENT ON COLUMN recipeweave.shopping_item.checked IS '購入済み';

CREATE TABLE recipeweave.audit_event (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actor_id UUID,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_key_hash CHAR(64) NOT NULL,
    reason TEXT NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL,
    CHECK (LENGTH(BTRIM(action)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(entity_type)) BETWEEN 1 AND 20000),
    CHECK (entity_key_hash IS NULL OR entity_key_hash ~ '^[0-9a-f]{64}$'),
    CHECK (LENGTH(BTRIM(reason)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.audit_event IS '変更・公開監査';

COMMENT ON COLUMN recipeweave.audit_event.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.audit_event.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.audit_event.actor_id IS '実行者（削除時匿名化）';

COMMENT ON COLUMN recipeweave.audit_event.action IS 'publish/withdraw/erase等';

COMMENT ON COLUMN recipeweave.audit_event.entity_type IS '対象テーブルの許可リスト';

COMMENT ON COLUMN recipeweave.audit_event.entity_key_hash IS '対象識別子のハッシュ';

COMMENT ON COLUMN recipeweave.audit_event.reason IS '理由（個人情報を含めない）';

COMMENT ON COLUMN recipeweave.audit_event.occurred_at IS '時刻';

CREATE TABLE recipeweave.outbox_event (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_type TEXT NOT NULL,
    aggregate_id UUID NOT NULL,
    payload JSONB NOT NULL,
    delivered_at TIMESTAMPTZ,
    attempt_count INTEGER NOT NULL,
    CHECK (attempt_count >= 0),
    CHECK (LENGTH(BTRIM(event_type)) BETWEEN 1 AND 20000),
    CHECK (payload IS NULL OR PG_COLUMN_SIZE(payload) <= 1048576)
);

COMMENT ON TABLE recipeweave.outbox_event IS '検索・キャッシュ更新配信';

COMMENT ON COLUMN recipeweave.outbox_event.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.outbox_event.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.outbox_event.event_type IS 'recipe_published/withdrawn/user_erased等';

COMMENT ON COLUMN recipeweave.outbox_event.aggregate_id IS '対象ID（配信対象でありFKでない）';

COMMENT ON COLUMN recipeweave.outbox_event.payload IS 'schema_version付き最小通知';

COMMENT ON COLUMN recipeweave.outbox_event.delivered_at IS '配送完了';

COMMENT ON COLUMN recipeweave.outbox_event.attempt_count IS '再試行数';

CREATE TABLE recipeweave.product_preparation_rule (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    product_version_id UUID NOT NULL,
    operation_id UUID NOT NULL,
    allowed BOOLEAN NOT NULL,
    use_original_container BOOLEAN NOT NULL,
    parameter_contract JSONB NOT NULL,
    source_id UUID NOT NULL,
    UNIQUE (product_version_id, operation_id, use_original_container),
    CHECK (parameter_contract IS NULL OR PG_COLUMN_SIZE(parameter_contract) <= 1048576)
);

COMMENT ON TABLE recipeweave.product_preparation_rule IS '商品固有の調理条件';

COMMENT ON COLUMN recipeweave.product_preparation_rule.id IS '不変の行識別子';

COMMENT ON COLUMN recipeweave.product_preparation_rule.created_at IS '作成日時（UTC）';

COMMENT ON COLUMN recipeweave.product_preparation_rule.product_version_id IS '対象商品仕様';

COMMENT ON COLUMN recipeweave.product_preparation_rule.operation_id IS '対象標準動作';

COMMENT ON COLUMN recipeweave.product_preparation_rule.allowed IS '表示で許可される方法か';

COMMENT ON COLUMN recipeweave.product_preparation_rule.use_original_container IS '付属容器で調理するか';

COMMENT ON COLUMN recipeweave.product_preparation_rule.parameter_contract IS '電力・注湯量・時間・蓋などの確定条件';

COMMENT ON COLUMN recipeweave.product_preparation_rule.source_id IS '商品表示根拠';

CREATE TABLE recipeweave.food_identity (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    normalizer_version TEXT NOT NULL,
    UNIQUE (code, normalizer_version),
    CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(normalizer_version)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.food_identity IS '料理同一性上の食品';

COMMENT ON COLUMN recipeweave.food_identity.id IS '不変ID';

COMMENT ON COLUMN recipeweave.food_identity.created_at IS '作成日時';

COMMENT ON COLUMN recipeweave.food_identity.code IS '形態を横断した食品コード';

COMMENT ON COLUMN recipeweave.food_identity.name IS '食品名';

COMMENT ON COLUMN recipeweave.food_identity.normalizer_version IS '正規化器の版';

CREATE TABLE recipeweave.food_identity_member (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    food_id UUID NOT NULL,
    identity_id UUID NOT NULL,
    normalizer_version TEXT NOT NULL,
    reason TEXT NOT NULL,
    UNIQUE (food_id, normalizer_version),
    CHECK (LENGTH(BTRIM(normalizer_version)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(reason)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.food_identity_member IS '購買食品から同一性への対応';

COMMENT ON COLUMN recipeweave.food_identity_member.id IS '不変ID';

COMMENT ON COLUMN recipeweave.food_identity_member.created_at IS '作成日時';

COMMENT ON COLUMN recipeweave.food_identity_member.food_id IS '元の食品';

COMMENT ON COLUMN recipeweave.food_identity_member.identity_id IS '同一性ID';

COMMENT ON COLUMN recipeweave.food_identity_member.normalizer_version IS '正規化器版';

COMMENT ON COLUMN recipeweave.food_identity_member.reason IS '同一視の理由';

CREATE TABLE recipeweave.generation_template (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    code TEXT NOT NULL,
    version INTEGER NOT NULL,
    release_id UUID NOT NULL,
    contract JSONB NOT NULL,
    candidate_count BIGINT NOT NULL,
    contract_hash CHAR(64) NOT NULL,
    UNIQUE (code, version),
    CHECK (version > 0),
    CHECK (candidate_count >= 0),
    CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000),
    CHECK (contract IS NULL OR PG_COLUMN_SIZE(contract) <= 1048576),
    CHECK (contract_hash IS NULL OR contract_hash ~ '^[0-9a-f]{64}$')
);

COMMENT ON TABLE recipeweave.generation_template IS '列挙テンプレート版';

COMMENT ON COLUMN recipeweave.generation_template.id IS '不変ID';

COMMENT ON COLUMN recipeweave.generation_template.created_at IS '作成日時';

COMMENT ON COLUMN recipeweave.generation_template.code IS 'テンプレートコード';

COMMENT ON COLUMN recipeweave.generation_template.version IS '定義版';

COMMENT ON COLUMN recipeweave.generation_template.release_id IS 'カタログ版';

COMMENT ON COLUMN recipeweave.generation_template.contract IS '主副材の許可集合・k・味付・経路';

COMMENT ON COLUMN recipeweave.generation_template.candidate_count IS 'この定義の正確な設計点数';

COMMENT ON COLUMN recipeweave.generation_template.contract_hash IS '定義ハッシュ';

CREATE TABLE recipeweave.generation_shard (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    template_id UUID NOT NULL,
    start_ordinal BIGINT NOT NULL,
    end_ordinal BIGINT NOT NULL,
    next_ordinal BIGINT NOT NULL,
    lease_owner TEXT,
    lease_expires_at TIMESTAMPTZ,
    fence_token BIGINT NOT NULL,
    state TEXT NOT NULL,
    UNIQUE (template_id, start_ordinal),
    CHECK (start_ordinal >= 0),
    CHECK (end_ordinal > start_ordinal),
    CHECK (next_ordinal >= start_ordinal AND next_ordinal <= end_ordinal),
    CHECK (fence_token >= 0),
    CHECK ((lease_owner IS NULL) = (lease_expires_at IS NULL)),
    CHECK (state <> 'running' OR lease_owner IS NOT NULL),
    CHECK (state <> 'done' OR next_ordinal = end_ordinal),
    CHECK (LENGTH(BTRIM(state)) BETWEEN 1 AND 20000),
    CHECK (state IN ('queued', 'running', 'done', 'failed'))
);

COMMENT ON TABLE recipeweave.generation_shard IS '列挙範囲・リース管理';

COMMENT ON COLUMN recipeweave.generation_shard.id IS '不変ID';

COMMENT ON COLUMN recipeweave.generation_shard.created_at IS '作成日時';

COMMENT ON COLUMN recipeweave.generation_shard.template_id IS 'テンプレート版';

COMMENT ON COLUMN recipeweave.generation_shard.start_ordinal IS '開始序数';

COMMENT ON COLUMN recipeweave.generation_shard.end_ordinal IS '終了序数（排他的）';

COMMENT ON COLUMN recipeweave.generation_shard.next_ordinal IS '再開位置';

COMMENT ON COLUMN recipeweave.generation_shard.lease_owner IS 'ワーカー識別子';

COMMENT ON COLUMN recipeweave.generation_shard.lease_expires_at IS '有効期限';

COMMENT ON COLUMN recipeweave.generation_shard.fence_token IS '古い所有者の書込みを拒否';

COMMENT ON COLUMN recipeweave.generation_shard.state IS '待機/実行/完了/停止';

CREATE TABLE recipeweave.candidate_attempt (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    template_id UUID NOT NULL,
    ordinal BIGINT NOT NULL,
    design_key CHAR(64) NOT NULL,
    job_id UUID,
    state TEXT NOT NULL,
    reason_code TEXT,
    recipe_version_id UUID,
    attempts INTEGER NOT NULL,
    UNIQUE (template_id, ordinal),
    UNIQUE (template_id, design_key),
    CHECK (ordinal >= 0),
    CHECK (attempts BETWEEN 0 AND 5),
    CHECK (state <> 'accepted' OR recipe_version_id IS NOT NULL),
    CHECK (design_key IS NULL OR design_key ~ '^[0-9a-f]{64}$'),
    CHECK (LENGTH(BTRIM(state)) BETWEEN 1 AND 20000),
    CHECK (state IN ('pending', 'invalid', 'generated', 'duplicate', 'accepted', 'failed'))
);

COMMENT ON TABLE recipeweave.candidate_attempt IS '試行済み設計点の台帳';

COMMENT ON COLUMN recipeweave.candidate_attempt.id IS '不変ID';

COMMENT ON COLUMN recipeweave.candidate_attempt.created_at IS '作成日時';

COMMENT ON COLUMN recipeweave.candidate_attempt.template_id IS '定義版';

COMMENT ON COLUMN recipeweave.candidate_attempt.ordinal IS '設計点の序数';

COMMENT ON COLUMN recipeweave.candidate_attempt.design_key IS '正規化した設計キー';

COMMENT ON COLUMN recipeweave.candidate_attempt.job_id IS '生成ジョブ';

COMMENT ON COLUMN recipeweave.candidate_attempt.state IS '候補の段階';

COMMENT ON COLUMN recipeweave.candidate_attempt.reason_code IS '棄却理由';

COMMENT ON COLUMN recipeweave.candidate_attempt.recipe_version_id IS '採用した版';

COMMENT ON COLUMN recipeweave.candidate_attempt.attempts IS '試行上限（暫定）';

CREATE TABLE recipeweave.recipe_search_document (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    recipe_id UUID NOT NULL,
    published_version_id UUID NOT NULL,
    projection_version TEXT NOT NULL,
    display_title TEXT NOT NULL,
    food_identity_ids UUID[] NOT NULL,
    facet_option_ids UUID[] NOT NULL,
    search_text TEXT NOT NULL,
    eligible BOOLEAN NOT NULL,
    source_hash CHAR(64) NOT NULL,
    projected_at TIMESTAMPTZ NOT NULL,
    UNIQUE (recipe_id),
    CHECK (LENGTH(BTRIM(projection_version)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(display_title)) BETWEEN 1 AND 20000),
    CHECK (LENGTH(BTRIM(search_text)) BETWEEN 1 AND 20000),
    CHECK (source_hash IS NULL OR source_hash ~ '^[0-9a-f]{64}$')
);

COMMENT ON TABLE recipeweave.recipe_search_document IS '公開検索用文書';

COMMENT ON COLUMN recipeweave.recipe_search_document.id IS '不変ID';

COMMENT ON COLUMN recipeweave.recipe_search_document.created_at IS '作成日時';

COMMENT ON COLUMN recipeweave.recipe_search_document.recipe_id IS '同一性単位で1件';

COMMENT ON COLUMN recipeweave.recipe_search_document.published_version_id IS '検索対象の公開版';

COMMENT ON COLUMN recipeweave.recipe_search_document.projection_version IS '検索文書の生成器版';

COMMENT ON COLUMN recipeweave.recipe_search_document.display_title IS '表示タイトル';

COMMENT ON COLUMN recipeweave.recipe_search_document.food_identity_ids IS '検索用食品ID集合';

COMMENT ON COLUMN recipeweave.recipe_search_document.facet_option_ids IS '料理・味等の検索軸';

COMMENT ON COLUMN recipeweave.recipe_search_document.search_text IS '検索用本文';

COMMENT ON COLUMN recipeweave.recipe_search_document.eligible IS '公開可能か';

COMMENT ON COLUMN recipeweave.recipe_search_document.source_hash IS '正本一致確認';

COMMENT ON COLUMN recipeweave.recipe_search_document.projected_at IS '更新時点';

CREATE TABLE recipeweave.recipe_embedding (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    recipe_version_id UUID NOT NULL,
    model_version TEXT NOT NULL,
    content_hash CHAR(64) NOT NULL,
    embedding VECTOR(768) NOT NULL,
    created_for_index TEXT NOT NULL,
    UNIQUE (recipe_version_id, model_version),
    CHECK (LENGTH(BTRIM(model_version)) BETWEEN 1 AND 20000),
    CHECK (content_hash IS NULL OR content_hash ~ '^[0-9a-f]{64}$'),
    CHECK (LENGTH(BTRIM(created_for_index)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.recipe_embedding IS '近似検索用特徴量';

COMMENT ON COLUMN recipeweave.recipe_embedding.id IS '不変ID';

COMMENT ON COLUMN recipeweave.recipe_embedding.created_at IS '作成日時';

COMMENT ON COLUMN recipeweave.recipe_embedding.recipe_version_id IS '対象版';

COMMENT ON COLUMN recipeweave.recipe_embedding.model_version IS '埋め込みモデル固定版';

COMMENT ON COLUMN recipeweave.recipe_embedding.content_hash IS '入力内容ハッシュ';

COMMENT ON COLUMN recipeweave.recipe_embedding.embedding IS '仮定768次元float32';

COMMENT ON COLUMN recipeweave.recipe_embedding.created_for_index IS '検索索引版';

CREATE TABLE recipeweave.generation_stratum_metric (
    id UUID NOT NULL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    template_id UUID NOT NULL,
    window_start TIMESTAMPTZ NOT NULL,
    window_end TIMESTAMPTZ NOT NULL,
    attempted BIGINT NOT NULL,
    valid BIGINT NOT NULL,
    unique_count BIGINT NOT NULL,
    publishable BIGINT NOT NULL,
    input_tokens BIGINT NOT NULL,
    output_tokens BIGINT NOT NULL,
    cost_amount NUMERIC(20, 6),
    currency CHAR(3),
    stratum_key TEXT NOT NULL,
    UNIQUE (template_id, stratum_key, window_start, window_end),
    CHECK (window_start < window_end),
    CHECK (attempted >= 0),
    CHECK (valid >= 0 AND valid <= attempted),
    CHECK (unique_count >= 0 AND unique_count <= valid),
    CHECK (publishable >= 0 AND publishable <= unique_count),
    CHECK (input_tokens >= 0),
    CHECK (output_tokens >= 0),
    CHECK (cost_amount IS NULL OR cost_amount >= 0),
    CHECK ((cost_amount IS NULL) = (currency IS NULL)),
    CHECK (currency IS NULL OR currency ~ '^[A-Z]{3}$'),
    CHECK (cost_amount IS NULL OR cost_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (LENGTH(BTRIM(stratum_key)) BETWEEN 1 AND 20000)
);

COMMENT ON TABLE recipeweave.generation_stratum_metric IS '採用率・飽和度の実測';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.id IS '不変ID';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.created_at IS '作成日時';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.template_id IS '対象テンプレート';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.window_start IS '計測窓開始';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.window_end IS '計測窓終了';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.attempted IS '試行数';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.valid IS '適合生成数';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.unique_count IS '既存集合との差分数';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.publishable IS '公開基準通過数';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.input_tokens IS '入力トークン合計';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.output_tokens IS '出力トークン合計';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.cost_amount IS '同一通貨の費用';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.currency IS 'JPY/USD等';

COMMENT ON COLUMN recipeweave.generation_stratum_metric.stratum_key IS '層の安定キー（料理構造×食品カテゴリ×入手性）。集計定義はテンプレート版に固定';

ALTER TABLE recipeweave.food ADD CONSTRAINT fk_food_parent_id
FOREIGN KEY (parent_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_food_parent_id ON recipeweave.food (parent_id);

ALTER TABLE recipeweave.food ADD CONSTRAINT fk_food_release_id
FOREIGN KEY (release_id) REFERENCES recipeweave.catalog_release (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_food_release_id ON recipeweave.food (release_id);

ALTER TABLE recipeweave.food_alias ADD CONSTRAINT fk_food_alias_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_food_alias_food_id ON recipeweave.food_alias (food_id);

ALTER TABLE recipeweave.food_form ADD CONSTRAINT fk_food_form_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_food_form_food_id ON recipeweave.food_form (food_id);

ALTER TABLE recipeweave.food_form ADD CONSTRAINT fk_food_form_base_unit_id
FOREIGN KEY (base_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_food_form_base_unit_id ON recipeweave.food_form (base_unit_id);

ALTER TABLE recipeweave.conversion ADD CONSTRAINT fk_conversion_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_conversion_form_id ON recipeweave.conversion (form_id);

ALTER TABLE recipeweave.conversion ADD CONSTRAINT fk_conversion_from_unit_id
FOREIGN KEY (from_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_conversion_from_unit_id ON recipeweave.conversion (from_unit_id);

ALTER TABLE recipeweave.conversion ADD CONSTRAINT fk_conversion_to_unit_id
FOREIGN KEY (to_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_conversion_to_unit_id ON recipeweave.conversion (to_unit_id);

ALTER TABLE recipeweave.conversion ADD CONSTRAINT fk_conversion_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_conversion_source_id ON recipeweave.conversion (source_id);

ALTER TABLE recipeweave.conversion ADD CONSTRAINT fk_conversion_release_id
FOREIGN KEY (release_id) REFERENCES recipeweave.catalog_release (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_conversion_release_id ON recipeweave.conversion (release_id);

ALTER TABLE recipeweave.form_yield ADD CONSTRAINT fk_form_yield_input_form_id
FOREIGN KEY (input_form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_form_yield_input_form_id ON recipeweave.form_yield (input_form_id);

ALTER TABLE recipeweave.form_yield ADD CONSTRAINT fk_form_yield_output_form_id
FOREIGN KEY (output_form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_form_yield_output_form_id ON recipeweave.form_yield (output_form_id);

ALTER TABLE recipeweave.form_yield ADD CONSTRAINT fk_form_yield_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_form_yield_source_id ON recipeweave.form_yield (source_id);

ALTER TABLE recipeweave.product ADD CONSTRAINT fk_product_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_food_id ON recipeweave.product (food_id);

ALTER TABLE recipeweave.product_version ADD CONSTRAINT fk_product_version_product_id
FOREIGN KEY (product_id) REFERENCES recipeweave.product (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_version_product_id ON recipeweave.product_version (product_id);

ALTER TABLE recipeweave.product_version ADD CONSTRAINT fk_product_version_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_version_form_id ON recipeweave.product_version (form_id);

ALTER TABLE recipeweave.product_version ADD CONSTRAINT fk_product_version_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_version_unit_id ON recipeweave.product_version (unit_id);

ALTER TABLE recipeweave.product_version ADD CONSTRAINT fk_product_version_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_version_source_id ON recipeweave.product_version (source_id);

ALTER TABLE recipeweave.product_component ADD CONSTRAINT fk_product_component_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_component_product_version_id ON recipeweave.product_component (
    product_version_id
);

ALTER TABLE recipeweave.product_component ADD CONSTRAINT fk_product_component_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_component_form_id ON recipeweave.product_component (form_id);

ALTER TABLE recipeweave.product_component ADD CONSTRAINT fk_product_component_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_component_unit_id ON recipeweave.product_component (unit_id);

ALTER TABLE recipeweave.allergen ADD CONSTRAINT fk_allergen_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_allergen_source_id ON recipeweave.allergen (source_id);

ALTER TABLE recipeweave.food_allergen ADD CONSTRAINT fk_food_allergen_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_food_allergen_form_id ON recipeweave.food_allergen (form_id);

ALTER TABLE recipeweave.food_allergen ADD CONSTRAINT fk_food_allergen_allergen_id
FOREIGN KEY (allergen_id) REFERENCES recipeweave.allergen (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_food_allergen_allergen_id ON recipeweave.food_allergen (allergen_id);

ALTER TABLE recipeweave.food_allergen ADD CONSTRAINT fk_food_allergen_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_food_allergen_source_id ON recipeweave.food_allergen (source_id);

ALTER TABLE recipeweave.product_allergen ADD CONSTRAINT fk_product_allergen_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_allergen_product_version_id ON recipeweave.product_allergen (
    product_version_id
);

ALTER TABLE recipeweave.product_allergen ADD CONSTRAINT fk_product_allergen_allergen_id
FOREIGN KEY (allergen_id) REFERENCES recipeweave.allergen (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_allergen_allergen_id ON recipeweave.product_allergen (allergen_id);

ALTER TABLE recipeweave.product_allergen ADD CONSTRAINT fk_product_allergen_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_allergen_source_id ON recipeweave.product_allergen (source_id);

ALTER TABLE recipeweave.nutrition_fact ADD CONSTRAINT fk_nutrition_fact_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_nutrition_fact_form_id ON recipeweave.nutrition_fact (form_id);

ALTER TABLE recipeweave.nutrition_fact ADD CONSTRAINT fk_nutrition_fact_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_nutrition_fact_product_version_id ON recipeweave.nutrition_fact (
    product_version_id
);

ALTER TABLE recipeweave.nutrition_fact ADD CONSTRAINT fk_nutrition_fact_nutrient_id
FOREIGN KEY (nutrient_id) REFERENCES recipeweave.nutrient (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_nutrition_fact_nutrient_id ON recipeweave.nutrition_fact (nutrient_id);

ALTER TABLE recipeweave.nutrition_fact ADD CONSTRAINT fk_nutrition_fact_basis_unit_id
FOREIGN KEY (basis_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_nutrition_fact_basis_unit_id ON recipeweave.nutrition_fact (basis_unit_id);

ALTER TABLE recipeweave.nutrition_fact ADD CONSTRAINT fk_nutrition_fact_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_nutrition_fact_source_id ON recipeweave.nutrition_fact (source_id);

ALTER TABLE recipeweave.axis ADD CONSTRAINT fk_axis_release_id
FOREIGN KEY (release_id) REFERENCES recipeweave.catalog_release (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_axis_release_id ON recipeweave.axis (release_id);

ALTER TABLE recipeweave.axis_option ADD CONSTRAINT fk_axis_option_axis_id
FOREIGN KEY (axis_id) REFERENCES recipeweave.axis (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_axis_option_axis_id ON recipeweave.axis_option (axis_id);

ALTER TABLE recipeweave.axis_option ADD CONSTRAINT fk_axis_option_parent_id
FOREIGN KEY (parent_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_axis_option_parent_id ON recipeweave.axis_option (parent_id);

ALTER TABLE recipeweave.food_axis_option ADD CONSTRAINT fk_food_axis_option_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_food_axis_option_food_id ON recipeweave.food_axis_option (food_id);

ALTER TABLE recipeweave.food_axis_option ADD CONSTRAINT fk_food_axis_option_option_id
FOREIGN KEY (option_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_food_axis_option_option_id ON recipeweave.food_axis_option (option_id);

ALTER TABLE recipeweave.recipe ADD CONSTRAINT fk_recipe_family_option_id
FOREIGN KEY (family_option_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_family_option_id ON recipeweave.recipe (family_option_id);

ALTER TABLE recipeweave.recipe_version ADD CONSTRAINT fk_recipe_version_recipe_id
FOREIGN KEY (recipe_id) REFERENCES recipeweave.recipe (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_version_recipe_id ON recipeweave.recipe_version (recipe_id);

ALTER TABLE recipeweave.recipe_version ADD CONSTRAINT fk_recipe_version_release_id
FOREIGN KEY (release_id) REFERENCES recipeweave.catalog_release (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_version_release_id ON recipeweave.recipe_version (release_id);

ALTER TABLE recipeweave.recipe_version ADD CONSTRAINT fk_recipe_version_output_unit_id
FOREIGN KEY (output_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_version_output_unit_id ON recipeweave.recipe_version (output_unit_id);

ALTER TABLE recipeweave.recipe_option ADD CONSTRAINT fk_recipe_option_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_option_recipe_version_id ON recipeweave.recipe_option (recipe_version_id);

ALTER TABLE recipeweave.recipe_option ADD CONSTRAINT fk_recipe_option_option_id
FOREIGN KEY (option_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_option_option_id ON recipeweave.recipe_option (option_id);

ALTER TABLE recipeweave.scaling_rule ADD CONSTRAINT fk_scaling_rule_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_scaling_rule_source_id ON recipeweave.scaling_rule (source_id);

ALTER TABLE recipeweave.scaling_point ADD CONSTRAINT fk_scaling_point_rule_id
FOREIGN KEY (rule_id) REFERENCES recipeweave.scaling_rule (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_scaling_point_rule_id ON recipeweave.scaling_point (rule_id);

ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_ingredient_recipe_version_id ON recipeweave.recipe_ingredient (
    recipe_version_id
);

ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_ingredient_form_id ON recipeweave.recipe_ingredient (form_id);

ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_ingredient_product_version_id ON recipeweave.recipe_ingredient (
    product_version_id
);

ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_component_id
FOREIGN KEY (component_id) REFERENCES recipeweave.product_component (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_ingredient_component_id ON recipeweave.recipe_ingredient (component_id);

ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_kit_parent_line_id
FOREIGN KEY (kit_parent_line_id) REFERENCES recipeweave.recipe_ingredient (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_ingredient_kit_parent_line_id ON recipeweave.recipe_ingredient (
    kit_parent_line_id
);

ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_ingredient_unit_id ON recipeweave.recipe_ingredient (unit_id);

ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_conversion_id
FOREIGN KEY (conversion_id) REFERENCES recipeweave.conversion (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_ingredient_conversion_id ON recipeweave.recipe_ingredient (conversion_id);

ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_scaling_rule_id
FOREIGN KEY (scaling_rule_id) REFERENCES recipeweave.scaling_rule (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_ingredient_scaling_rule_id ON recipeweave.recipe_ingredient (
    scaling_rule_id
);

ALTER TABLE recipeweave.operation_parameter ADD CONSTRAINT fk_operation_parameter_operation_id
FOREIGN KEY (operation_id) REFERENCES recipeweave.operation (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_operation_parameter_operation_id ON recipeweave.operation_parameter (operation_id);

ALTER TABLE recipeweave.operation_parameter ADD CONSTRAINT fk_operation_parameter_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_operation_parameter_unit_id ON recipeweave.operation_parameter (unit_id);

ALTER TABLE recipeweave.recipe_step ADD CONSTRAINT fk_recipe_step_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_step_recipe_version_id ON recipeweave.recipe_step (recipe_version_id);

ALTER TABLE recipeweave.recipe_step ADD CONSTRAINT fk_recipe_step_operation_id
FOREIGN KEY (operation_id) REFERENCES recipeweave.operation (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_step_operation_id ON recipeweave.recipe_step (operation_id);

ALTER TABLE recipeweave.recipe_step ADD CONSTRAINT fk_recipe_step_scaling_rule_id
FOREIGN KEY (scaling_rule_id) REFERENCES recipeweave.scaling_rule (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_step_scaling_rule_id ON recipeweave.recipe_step (scaling_rule_id);

ALTER TABLE recipeweave.step_parameter ADD CONSTRAINT fk_step_parameter_step_id
FOREIGN KEY (step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_step_parameter_step_id ON recipeweave.step_parameter (step_id);

ALTER TABLE recipeweave.step_parameter ADD CONSTRAINT fk_step_parameter_parameter_id
FOREIGN KEY (parameter_id) REFERENCES recipeweave.operation_parameter (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_step_parameter_parameter_id ON recipeweave.step_parameter (parameter_id);

ALTER TABLE recipeweave.material_node ADD CONSTRAINT fk_material_node_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_material_node_recipe_version_id ON recipeweave.material_node (recipe_version_id);

ALTER TABLE recipeweave.material_node ADD CONSTRAINT fk_material_node_ingredient_line_id
FOREIGN KEY (ingredient_line_id) REFERENCES recipeweave.recipe_ingredient (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_material_node_ingredient_line_id ON recipeweave.material_node (ingredient_line_id);

ALTER TABLE recipeweave.material_node ADD CONSTRAINT fk_material_node_producer_step_id
FOREIGN KEY (producer_step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_material_node_producer_step_id ON recipeweave.material_node (producer_step_id);

ALTER TABLE recipeweave.material_node ADD CONSTRAINT fk_material_node_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_material_node_unit_id ON recipeweave.material_node (unit_id);

ALTER TABLE recipeweave.step_input ADD CONSTRAINT fk_step_input_step_id
FOREIGN KEY (step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_step_input_step_id ON recipeweave.step_input (step_id);

ALTER TABLE recipeweave.step_input ADD CONSTRAINT fk_step_input_material_id
FOREIGN KEY (material_id) REFERENCES recipeweave.material_node (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_step_input_material_id ON recipeweave.step_input (material_id);

ALTER TABLE recipeweave.step_dependency ADD CONSTRAINT fk_step_dependency_before_step_id
FOREIGN KEY (before_step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_step_dependency_before_step_id ON recipeweave.step_dependency (before_step_id);

ALTER TABLE recipeweave.step_dependency ADD CONSTRAINT fk_step_dependency_after_step_id
FOREIGN KEY (after_step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_step_dependency_after_step_id ON recipeweave.step_dependency (after_step_id);

ALTER TABLE recipeweave.resource_type ADD CONSTRAINT fk_resource_type_capacity_unit_id
FOREIGN KEY (capacity_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_resource_type_capacity_unit_id ON recipeweave.resource_type (capacity_unit_id);

ALTER TABLE recipeweave.step_resource ADD CONSTRAINT fk_step_resource_step_id
FOREIGN KEY (step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_step_resource_step_id ON recipeweave.step_resource (step_id);

ALTER TABLE recipeweave.step_resource ADD CONSTRAINT fk_step_resource_resource_type_id
FOREIGN KEY (resource_type_id) REFERENCES recipeweave.resource_type (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_step_resource_resource_type_id ON recipeweave.step_resource (resource_type_id);

ALTER TABLE recipeweave.media_asset ADD CONSTRAINT fk_media_asset_operation_id
FOREIGN KEY (operation_id) REFERENCES recipeweave.operation (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_media_asset_operation_id ON recipeweave.media_asset (operation_id);

ALTER TABLE recipeweave.media_asset ADD CONSTRAINT fk_media_asset_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_media_asset_source_id ON recipeweave.media_asset (source_id);

ALTER TABLE recipeweave.step_media ADD CONSTRAINT fk_step_media_step_id
FOREIGN KEY (step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_step_media_step_id ON recipeweave.step_media (step_id);

ALTER TABLE recipeweave.step_media ADD CONSTRAINT fk_step_media_media_id
FOREIGN KEY (media_id) REFERENCES recipeweave.media_asset (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_step_media_media_id ON recipeweave.step_media (media_id);

ALTER TABLE recipeweave.generation_policy ADD CONSTRAINT fk_generation_policy_release_id
FOREIGN KEY (release_id) REFERENCES recipeweave.catalog_release (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_generation_policy_release_id ON recipeweave.generation_policy (release_id);

ALTER TABLE recipeweave.generation_job ADD CONSTRAINT fk_generation_job_policy_id
FOREIGN KEY (policy_id) REFERENCES recipeweave.generation_policy (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_generation_job_policy_id ON recipeweave.generation_job (policy_id);

ALTER TABLE recipeweave.generation_choice ADD CONSTRAINT fk_generation_choice_job_id
FOREIGN KEY (job_id) REFERENCES recipeweave.generation_job (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_generation_choice_job_id ON recipeweave.generation_choice (job_id);

ALTER TABLE recipeweave.generation_choice ADD CONSTRAINT fk_generation_choice_option_id
FOREIGN KEY (option_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_generation_choice_option_id ON recipeweave.generation_choice (option_id);

ALTER TABLE recipeweave.generation_food ADD CONSTRAINT fk_generation_food_job_id
FOREIGN KEY (job_id) REFERENCES recipeweave.generation_job (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_generation_food_job_id ON recipeweave.generation_food (job_id);

ALTER TABLE recipeweave.generation_food ADD CONSTRAINT fk_generation_food_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_generation_food_form_id ON recipeweave.generation_food (form_id);

ALTER TABLE recipeweave.generation_result ADD CONSTRAINT fk_generation_result_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_generation_result_recipe_version_id ON recipeweave.generation_result (
    recipe_version_id
);

ALTER TABLE recipeweave.generation_result ADD CONSTRAINT fk_generation_result_job_id
FOREIGN KEY (job_id) REFERENCES recipeweave.generation_job (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_generation_result_job_id ON recipeweave.generation_result (job_id);

ALTER TABLE recipeweave.generation_result ADD CONSTRAINT fk_generation_result_policy_id
FOREIGN KEY (policy_id) REFERENCES recipeweave.generation_policy (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_generation_result_policy_id ON recipeweave.generation_result (policy_id);

ALTER TABLE recipeweave.compatibility_rule ADD CONSTRAINT fk_compatibility_rule_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_compatibility_rule_source_id ON recipeweave.compatibility_rule (source_id);

ALTER TABLE recipeweave.validation_result ADD CONSTRAINT fk_validation_result_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_validation_result_recipe_version_id ON recipeweave.validation_result (
    recipe_version_id
);

ALTER TABLE recipeweave.validation_result ADD CONSTRAINT fk_validation_result_rule_id
FOREIGN KEY (rule_id) REFERENCES recipeweave.compatibility_rule (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_validation_result_rule_id ON recipeweave.validation_result (rule_id);

ALTER TABLE recipeweave.recipe_signature ADD CONSTRAINT fk_recipe_signature_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_signature_recipe_version_id ON recipeweave.recipe_signature (
    recipe_version_id
);

ALTER TABLE recipeweave.recipe_similarity ADD CONSTRAINT fk_recipe_similarity_left_version_id
FOREIGN KEY (left_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_similarity_left_version_id ON recipeweave.recipe_similarity (
    left_version_id
);

ALTER TABLE recipeweave.recipe_similarity ADD CONSTRAINT fk_recipe_similarity_right_version_id
FOREIGN KEY (right_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_similarity_right_version_id ON recipeweave.recipe_similarity (
    right_version_id
);

ALTER TABLE recipeweave.user_preference ADD CONSTRAINT fk_user_preference_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_user_preference_user_id ON recipeweave.user_preference (user_id);

ALTER TABLE recipeweave.user_preference ADD CONSTRAINT fk_user_preference_option_id
FOREIGN KEY (option_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_user_preference_option_id ON recipeweave.user_preference (option_id);

ALTER TABLE recipeweave.user_exclusion ADD CONSTRAINT fk_user_exclusion_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_user_exclusion_user_id ON recipeweave.user_exclusion (user_id);

ALTER TABLE recipeweave.user_exclusion ADD CONSTRAINT fk_user_exclusion_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_user_exclusion_food_id ON recipeweave.user_exclusion (food_id);

ALTER TABLE recipeweave.user_exclusion ADD CONSTRAINT fk_user_exclusion_allergen_id
FOREIGN KEY (allergen_id) REFERENCES recipeweave.allergen (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_user_exclusion_allergen_id ON recipeweave.user_exclusion (allergen_id);

ALTER TABLE recipeweave.user_recipe_event ADD CONSTRAINT fk_user_recipe_event_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_user_recipe_event_user_id ON recipeweave.user_recipe_event (user_id);

ALTER TABLE recipeweave.user_recipe_event ADD CONSTRAINT fk_user_recipe_event_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_user_recipe_event_recipe_version_id ON recipeweave.user_recipe_event (
    recipe_version_id
);

ALTER TABLE recipeweave.menu ADD CONSTRAINT fk_menu_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_menu_user_id ON recipeweave.menu (user_id);

ALTER TABLE recipeweave.menu_item ADD CONSTRAINT fk_menu_item_menu_id
FOREIGN KEY (menu_id) REFERENCES recipeweave.menu (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_menu_item_menu_id ON recipeweave.menu_item (menu_id);

ALTER TABLE recipeweave.menu_item ADD CONSTRAINT fk_menu_item_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_menu_item_recipe_version_id ON recipeweave.menu_item (recipe_version_id);

ALTER TABLE recipeweave.menu_item ADD CONSTRAINT fk_menu_item_role_option_id
FOREIGN KEY (role_option_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_menu_item_role_option_id ON recipeweave.menu_item (role_option_id);

ALTER TABLE recipeweave.menu_ingredient_override ADD CONSTRAINT fk_menu_ingredient_override_menu_item_id
FOREIGN KEY (menu_item_id) REFERENCES recipeweave.menu_item (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_menu_ingredient_override_menu_item_id ON recipeweave.menu_ingredient_override (
    menu_item_id
);

ALTER TABLE recipeweave.menu_ingredient_override ADD CONSTRAINT fk_menu_ingredient_override_ingredient_line_id
FOREIGN KEY (ingredient_line_id) REFERENCES recipeweave.recipe_ingredient (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_menu_ingredient_override_ingredient_line_id ON recipeweave.menu_ingredient_override (
    ingredient_line_id
);

ALTER TABLE recipeweave.menu_ingredient_override ADD CONSTRAINT fk_menu_ingredient_override_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_menu_ingredient_override_form_id ON recipeweave.menu_ingredient_override (form_id);

ALTER TABLE recipeweave.menu_ingredient_override ADD CONSTRAINT fk_menu_ingredient_override_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_menu_ingredient_override_product_version_id ON recipeweave.menu_ingredient_override (
    product_version_id
);

ALTER TABLE recipeweave.kitchen_resource ADD CONSTRAINT fk_kitchen_resource_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_kitchen_resource_user_id ON recipeweave.kitchen_resource (user_id);

ALTER TABLE recipeweave.kitchen_resource ADD CONSTRAINT fk_kitchen_resource_resource_type_id
FOREIGN KEY (resource_type_id) REFERENCES recipeweave.resource_type (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_kitchen_resource_resource_type_id ON recipeweave.kitchen_resource (
    resource_type_id
);

ALTER TABLE recipeweave.cooking_session ADD CONSTRAINT fk_cooking_session_menu_id
FOREIGN KEY (menu_id) REFERENCES recipeweave.menu (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_cooking_session_menu_id ON recipeweave.cooking_session (menu_id);

ALTER TABLE recipeweave.session_task ADD CONSTRAINT fk_session_task_session_id
FOREIGN KEY (session_id) REFERENCES recipeweave.cooking_session (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_session_task_session_id ON recipeweave.session_task (session_id);

ALTER TABLE recipeweave.session_task ADD CONSTRAINT fk_session_task_menu_item_id
FOREIGN KEY (menu_item_id) REFERENCES recipeweave.menu_item (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_session_task_menu_item_id ON recipeweave.session_task (menu_item_id);

ALTER TABLE recipeweave.session_task ADD CONSTRAINT fk_session_task_step_id
FOREIGN KEY (step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_session_task_step_id ON recipeweave.session_task (step_id);

ALTER TABLE recipeweave.task_dependency ADD CONSTRAINT fk_task_dependency_before_task_id
FOREIGN KEY (before_task_id) REFERENCES recipeweave.session_task (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_task_dependency_before_task_id ON recipeweave.task_dependency (before_task_id);

ALTER TABLE recipeweave.task_dependency ADD CONSTRAINT fk_task_dependency_after_task_id
FOREIGN KEY (after_task_id) REFERENCES recipeweave.session_task (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_task_dependency_after_task_id ON recipeweave.task_dependency (after_task_id);

ALTER TABLE recipeweave.resource_reservation ADD CONSTRAINT fk_resource_reservation_task_id
FOREIGN KEY (task_id) REFERENCES recipeweave.session_task (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_resource_reservation_task_id ON recipeweave.resource_reservation (task_id);

ALTER TABLE recipeweave.resource_reservation ADD CONSTRAINT fk_resource_reservation_resource_id
FOREIGN KEY (resource_id) REFERENCES recipeweave.kitchen_resource (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_resource_reservation_resource_id ON recipeweave.resource_reservation (resource_id);

ALTER TABLE recipeweave.ingredient_total ADD CONSTRAINT fk_ingredient_total_session_id
FOREIGN KEY (session_id) REFERENCES recipeweave.cooking_session (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_ingredient_total_session_id ON recipeweave.ingredient_total (session_id);

ALTER TABLE recipeweave.ingredient_total ADD CONSTRAINT fk_ingredient_total_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_ingredient_total_form_id ON recipeweave.ingredient_total (form_id);

ALTER TABLE recipeweave.ingredient_total ADD CONSTRAINT fk_ingredient_total_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_ingredient_total_product_version_id ON recipeweave.ingredient_total (
    product_version_id
);

ALTER TABLE recipeweave.ingredient_total ADD CONSTRAINT fk_ingredient_total_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_ingredient_total_unit_id ON recipeweave.ingredient_total (unit_id);

ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_pantry_lot_user_id ON recipeweave.pantry_lot (user_id);

ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_pantry_lot_form_id ON recipeweave.pantry_lot (form_id);

ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_pantry_lot_product_version_id ON recipeweave.pantry_lot (product_version_id);

ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_pantry_lot_unit_id ON recipeweave.pantry_lot (unit_id);

ALTER TABLE recipeweave.shopping_item ADD CONSTRAINT fk_shopping_item_session_id
FOREIGN KEY (session_id) REFERENCES recipeweave.cooking_session (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_shopping_item_session_id ON recipeweave.shopping_item (session_id);

ALTER TABLE recipeweave.shopping_item ADD CONSTRAINT fk_shopping_item_total_id
FOREIGN KEY (total_id) REFERENCES recipeweave.ingredient_total (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_shopping_item_total_id ON recipeweave.shopping_item (total_id);

ALTER TABLE recipeweave.shopping_item ADD CONSTRAINT fk_shopping_item_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_shopping_item_product_version_id ON recipeweave.shopping_item (product_version_id);

ALTER TABLE recipeweave.audit_event ADD CONSTRAINT fk_audit_event_actor_id
FOREIGN KEY (actor_id) REFERENCES recipeweave.app_user (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_audit_event_actor_id ON recipeweave.audit_event (actor_id);

ALTER TABLE recipeweave.product_preparation_rule ADD CONSTRAINT fk_product_preparation_rule_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_preparation_rule_product_version_id ON recipeweave.product_preparation_rule (
    product_version_id
);

ALTER TABLE recipeweave.product_preparation_rule ADD CONSTRAINT fk_product_preparation_rule_operation_id
FOREIGN KEY (operation_id) REFERENCES recipeweave.operation (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_preparation_rule_operation_id ON recipeweave.product_preparation_rule (
    operation_id
);

ALTER TABLE recipeweave.product_preparation_rule ADD CONSTRAINT fk_product_preparation_rule_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_product_preparation_rule_source_id ON recipeweave.product_preparation_rule (
    source_id
);

ALTER TABLE recipeweave.food_identity_member ADD CONSTRAINT fk_food_identity_member_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_food_identity_member_food_id ON recipeweave.food_identity_member (food_id);

ALTER TABLE recipeweave.food_identity_member ADD CONSTRAINT fk_food_identity_member_identity_id
FOREIGN KEY (identity_id) REFERENCES recipeweave.food_identity (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_food_identity_member_identity_id ON recipeweave.food_identity_member (identity_id);

ALTER TABLE recipeweave.generation_template ADD CONSTRAINT fk_generation_template_release_id
FOREIGN KEY (release_id) REFERENCES recipeweave.catalog_release (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_generation_template_release_id ON recipeweave.generation_template (release_id);

ALTER TABLE recipeweave.generation_shard ADD CONSTRAINT fk_generation_shard_template_id
FOREIGN KEY (template_id) REFERENCES recipeweave.generation_template (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_generation_shard_template_id ON recipeweave.generation_shard (template_id);

ALTER TABLE recipeweave.candidate_attempt ADD CONSTRAINT fk_candidate_attempt_template_id
FOREIGN KEY (template_id) REFERENCES recipeweave.generation_template (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_candidate_attempt_template_id ON recipeweave.candidate_attempt (template_id);

ALTER TABLE recipeweave.candidate_attempt ADD CONSTRAINT fk_candidate_attempt_job_id
FOREIGN KEY (job_id) REFERENCES recipeweave.generation_job (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_candidate_attempt_job_id ON recipeweave.candidate_attempt (job_id);

ALTER TABLE recipeweave.candidate_attempt ADD CONSTRAINT fk_candidate_attempt_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_candidate_attempt_recipe_version_id ON recipeweave.candidate_attempt (
    recipe_version_id
);

ALTER TABLE recipeweave.recipe_search_document ADD CONSTRAINT fk_recipe_search_document_recipe_id
FOREIGN KEY (recipe_id) REFERENCES recipeweave.recipe (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_search_document_recipe_id ON recipeweave.recipe_search_document (recipe_id);

ALTER TABLE recipeweave.recipe_search_document ADD CONSTRAINT fk_recipe_search_document_published_version_id
FOREIGN KEY (published_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_search_document_published_version_id ON recipeweave.recipe_search_document (
    published_version_id
);

ALTER TABLE recipeweave.recipe_embedding ADD CONSTRAINT fk_recipe_embedding_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_recipe_embedding_recipe_version_id ON recipeweave.recipe_embedding (
    recipe_version_id
);

ALTER TABLE recipeweave.generation_stratum_metric ADD CONSTRAINT fk_generation_stratum_metric_template_id
FOREIGN KEY (template_id) REFERENCES recipeweave.generation_template (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX ix_generation_stratum_metric_template_id ON recipeweave.generation_stratum_metric (
    template_id
);

CREATE UNIQUE INDEX uq_product_0 ON recipeweave.product (gtin) WHERE gtin IS NOT NULL;

CREATE UNIQUE INDEX uq_nutrition_fact_0 ON recipeweave.nutrition_fact (
    form_id, nutrient_id, source_id
) WHERE form_id IS NOT NULL;

CREATE UNIQUE INDEX uq_nutrition_fact_1 ON recipeweave.nutrition_fact (
    product_version_id, nutrient_id, source_id
) WHERE product_version_id IS NOT NULL;

CREATE UNIQUE INDEX uq_user_exclusion_0 ON recipeweave.user_exclusion (
    user_id, food_id
) WHERE food_id IS NOT NULL;

CREATE UNIQUE INDEX uq_user_exclusion_1 ON recipeweave.user_exclusion (
    user_id, allergen_id
) WHERE allergen_id IS NOT NULL;

CREATE UNIQUE INDEX uq_material_node_0 ON recipeweave.material_node (
    ingredient_line_id
) WHERE ingredient_line_id IS NOT NULL;

CREATE INDEX ix_food_alias_search_0 ON recipeweave.food_alias (alias, locale);

CREATE INDEX ix_recipe_version_search_0 ON recipeweave.recipe_version (
    recipe_id, version DESC
) WHERE status
= 'published';

CREATE INDEX ix_recipe_option_search_0 ON recipeweave.recipe_option (option_id, recipe_version_id);

CREATE INDEX ix_recipe_ingredient_search_0 ON recipeweave.recipe_ingredient (
    form_id, recipe_version_id
);

CREATE INDEX ix_recipe_signature_search_0 ON recipeweave.recipe_signature (
    algorithm_version, exact_hash
);

CREATE INDEX ix_user_recipe_event_search_0 ON recipeweave.user_recipe_event (
    user_id, kind, occurred_at DESC
);

CREATE INDEX ix_session_task_search_0 ON recipeweave.session_task (session_id, planned_start_s);

CREATE INDEX ix_audit_event_search_0 ON recipeweave.audit_event (occurred_at);

CREATE INDEX ix_outbox_event_search_0 ON recipeweave.outbox_event (
    created_at
) WHERE delivered_at IS NULL;

CREATE INDEX ix_recipe_search_document_search_0 ON recipeweave.recipe_search_document USING gin (
    food_identity_ids
);

CREATE INDEX ix_recipe_search_document_search_1 ON recipeweave.recipe_search_document USING gin (
    facet_option_ids
);

CREATE INDEX ix_recipe_search_document_search_2 ON recipeweave.recipe_search_document USING gin (
    TO_TSVECTOR('simple', search_text)
);

ALTER TABLE recipeweave.generation_shard ADD CONSTRAINT generation_shard_no_overlap
EXCLUDE USING gist (template_id WITH =, INT8RANGE(start_ordinal, end_ordinal, '[)') WITH &&);

CREATE FUNCTION recipeweave.reject_identity_change() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.id IS DISTINCT FROM OLD.id OR NEW.created_at IS DISTINCT FROM OLD.created_at THEN
        RAISE EXCEPTION '識別子と作成日時は変更できません' USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
END;
$$;

CREATE FUNCTION recipeweave.recipe_version_for(table_name TEXT, row_data JSONB) RETURNS UUID
LANGUAGE plpgsql STABLE AS $$
DECLARE
    target uuid;
BEGIN
    IF table_name = 'recipe_version' THEN
        RETURN (row_data->>'id')::uuid;
    ELSIF row_data ? 'recipe_version_id' THEN
        RETURN (row_data->>'recipe_version_id')::uuid;
    ELSIF table_name IN ('step_parameter', 'step_input', 'step_resource', 'step_media') THEN
        SELECT recipe_version_id INTO target FROM recipeweave.recipe_step
        WHERE id = (row_data->>'step_id')::uuid;
    ELSIF table_name = 'step_dependency' THEN
        SELECT recipe_version_id INTO target FROM recipeweave.recipe_step
        WHERE id = (row_data->>'before_step_id')::uuid;
    END IF;
    RETURN target;
END;
$$;

CREATE FUNCTION recipeweave.guard_recipe_content() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    row_data jsonb;
    version_id uuid;
    released boolean;
BEGIN
    row_data := CASE WHEN TG_OP = 'DELETE' THEN to_jsonb(OLD) ELSE to_jsonb(NEW) END;
    version_id := recipeweave.recipe_version_for(TG_TABLE_NAME, row_data);
    SELECT published_at IS NOT NULL INTO released FROM recipeweave.recipe_version WHERE id = version_id;
    IF TG_TABLE_NAME = 'recipe_version' AND TG_OP = 'UPDATE' AND to_jsonb(OLD)->>'published_at' IS NOT NULL THEN
        IF (to_jsonb(NEW) - 'status') IS DISTINCT FROM (to_jsonb(OLD) - 'status')
           OR NEW.status NOT IN ('published', 'withdrawn') THEN
            RAISE EXCEPTION '公開したレシピ版の内容は変更できません' USING ERRCODE = '23514';
        END IF;
    ELSIF released THEN
        RAISE EXCEPTION '公開したレシピ版とその子行は変更・削除できません' USING ERRCODE = '23514';
    END IF;
    IF TG_OP = 'UPDATE' AND TG_TABLE_NAME <> 'recipe_version' THEN
        version_id := recipeweave.recipe_version_for(TG_TABLE_NAME, to_jsonb(OLD));
        IF EXISTS (SELECT 1 FROM recipeweave.recipe_version WHERE id = version_id AND published_at IS NOT NULL) THEN
            RAISE EXCEPTION '公開版から子行を移動できません' USING ERRCODE = '23514';
        END IF;
    END IF;
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$;

CREATE FUNCTION recipeweave.validate_recipe_version(version_id UUID) RETURNS VOID
LANGUAGE plpgsql AS $$
DECLARE
    current_version recipeweave.recipe_version%ROWTYPE;
BEGIN
    SELECT * INTO current_version FROM recipeweave.recipe_version WHERE id = version_id FOR UPDATE;
    IF NOT FOUND THEN RETURN; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.recipe_ingredient i
        LEFT JOIN recipeweave.recipe_ingredient parent ON parent.id = i.kit_parent_line_id
        LEFT JOIN recipeweave.product_component component ON component.id = i.component_id
        LEFT JOIN recipeweave.product_version product ON product.id = i.product_version_id
        WHERE i.recipe_version_id = version_id AND (
            (i.product_version_id IS NOT NULL AND product.form_id <> i.form_id)
            OR (i.demand_kind = 'kit_component' AND (
                parent.recipe_version_id <> version_id OR parent.demand_kind <> 'purchase'
                OR parent.product_version_id IS NULL
                OR component.product_version_id <> parent.product_version_id
                OR component.form_id <> i.form_id
            ))
        )
    ) THEN RAISE EXCEPTION '商品・形態・セット親の所属が一致しません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.recipe_ingredient i
        JOIN recipeweave.food_form form ON form.id = i.form_id
        JOIN recipeweave.unit input_unit ON input_unit.id = i.unit_id
        JOIN recipeweave.unit base_unit ON base_unit.id = form.base_unit_id
        LEFT JOIN recipeweave.conversion c ON c.id = i.conversion_id
        WHERE i.recipe_version_id = version_id AND (
            (i.conversion_id IS NOT NULL AND (c.form_id <> i.form_id OR c.from_unit_id <> i.unit_id
                OR c.to_unit_id <> form.base_unit_id OR c.release_id <> current_version.release_id))
            OR (i.amount_mode = 'exact' AND (
                (i.conversion_id IS NULL AND input_unit.dimension <> base_unit.dimension)
                OR i.canonical_amount <> round(CASE WHEN c.id IS NOT NULL THEN i.amount * c.factor
                    ELSE (i.amount * input_unit.factor + input_unit.offset - base_unit.offset) / base_unit.factor END, 6)
            ))
        )
    ) THEN RAISE EXCEPTION '形態専用換算と登録基準量が一致しません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.material_node n
        LEFT JOIN recipeweave.recipe_ingredient i ON i.id = n.ingredient_line_id
        LEFT JOIN recipeweave.recipe_step s ON s.id = n.producer_step_id
        WHERE n.recipe_version_id = version_id
          AND (i.recipe_version_id <> version_id OR s.recipe_version_id <> version_id)
    ) OR EXISTS (
        SELECT 1 FROM recipeweave.step_input input
        JOIN recipeweave.recipe_step s ON s.id = input.step_id
        JOIN recipeweave.material_node n ON n.id = input.material_id
        WHERE (s.recipe_version_id = version_id OR n.recipe_version_id = version_id)
          AND s.recipe_version_id <> n.recipe_version_id
    ) OR EXISTS (
        SELECT 1 FROM recipeweave.step_dependency d
        JOIN recipeweave.recipe_step b ON b.id = d.before_step_id
        JOIN recipeweave.recipe_step a ON a.id = d.after_step_id
        WHERE (b.recipe_version_id = version_id OR a.recipe_version_id = version_id)
          AND b.recipe_version_id <> a.recipe_version_id
    ) THEN RAISE EXCEPTION '材料と工程を別のレシピ版へ接続できません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.step_input i JOIN recipeweave.material_node n ON n.id = i.material_id
        WHERE n.recipe_version_id = version_id GROUP BY n.id HAVING sum(i.fraction) > 1
    ) THEN RAISE EXCEPTION '材料の使用割合が全量を超えています' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        WITH RECURSIVE edges AS (
            SELECT d.before_step_id AS before_id, d.after_step_id AS after_id
            FROM recipeweave.step_dependency d JOIN recipeweave.recipe_step s ON s.id = d.before_step_id
            WHERE s.recipe_version_id = version_id
            UNION
            SELECT n.producer_step_id, i.step_id FROM recipeweave.material_node n
            JOIN recipeweave.step_input i ON i.material_id = n.id
            WHERE n.recipe_version_id = version_id AND n.producer_step_id IS NOT NULL
        ), reach(before_id, after_id) AS (
            SELECT before_id, after_id FROM edges
            UNION
            SELECT r.before_id, e.after_id FROM reach r JOIN edges e ON e.before_id = r.after_id
        ) SELECT 1 FROM reach WHERE before_id = after_id
    ) THEN RAISE EXCEPTION '工程・材料の依存に循環があります' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.step_parameter value
        JOIN recipeweave.recipe_step step ON step.id = value.step_id
        JOIN recipeweave.operation_parameter parameter ON parameter.id = value.parameter_id
        WHERE step.recipe_version_id = version_id AND (
            step.operation_id <> parameter.operation_id
            OR (parameter.value_type IN ('decimal', 'integer') AND (value.number_value IS NULL
                OR value.number_value < parameter.min_value OR value.number_value > parameter.max_value))
            OR (parameter.value_type = 'integer' AND value.number_value <> trunc(value.number_value))
            OR (parameter.value_type = 'boolean' AND value.bool_value IS NULL)
            OR (parameter.value_type IN ('text', 'option') AND value.text_value IS NULL)
            OR (parameter.value_type = 'option' AND NOT parameter.allowed_values ? value.text_value)
        )
    ) THEN RAISE EXCEPTION '工程パラメータの動作・型・範囲が不一致です' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.step_media mapping
        JOIN recipeweave.recipe_step step ON step.id = mapping.step_id
        JOIN recipeweave.media_asset media ON media.id = mapping.media_id
        WHERE step.recipe_version_id = version_id AND step.operation_id <> media.operation_id
    ) THEN RAISE EXCEPTION '工程と媒体の標準動作が一致しません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.recipe_option ro
        JOIN recipeweave.axis_option ao ON ao.id = ro.option_id JOIN recipeweave.axis axis ON axis.id = ao.axis_id
        WHERE ro.recipe_version_id = version_id AND axis.release_id <> current_version.release_id
    ) OR EXISTS (
        SELECT 1 FROM recipeweave.recipe_ingredient i JOIN recipeweave.food_form form ON form.id = i.form_id
        JOIN recipeweave.food food ON food.id = form.food_id
        WHERE i.recipe_version_id = version_id AND food.release_id <> current_version.release_id
    ) THEN RAISE EXCEPTION '食材・分類と採用カタログ版が一致しません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.recipe_option ro JOIN recipeweave.axis_option ao ON ao.id = ro.option_id
        JOIN recipeweave.axis axis ON axis.id = ao.axis_id
        WHERE ro.recipe_version_id = version_id AND axis.selection = 'single'
        GROUP BY axis.id HAVING count(*) > 1
    ) THEN RAISE EXCEPTION '単一選択軸に複数値を設定できません' USING ERRCODE = '23514'; END IF;
    IF current_version.status = 'published' THEN
        IF EXISTS (SELECT 1 FROM recipeweave.recipe_ingredient ingredient
            JOIN recipeweave.food_form form ON form.id = ingredient.form_id
            JOIN recipeweave.food food ON food.id = form.food_id
            WHERE ingredient.recipe_version_id = version_id AND food.owner_id IS NOT NULL) THEN
            RAISE EXCEPTION '私有食材を含むレシピは公開できません' USING ERRCODE = '23514';
        END IF;
        IF NOT EXISTS (SELECT 1 FROM recipeweave.recipe_ingredient WHERE recipe_version_id = version_id)
           OR NOT EXISTS (SELECT 1 FROM recipeweave.recipe_step WHERE recipe_version_id = version_id) THEN
            RAISE EXCEPTION '材料または工程のないレシピは公開できません' USING ERRCODE = '23514';
        END IF;
        IF EXISTS (
            SELECT 1 FROM recipeweave.recipe_step s JOIN recipeweave.operation_parameter p ON p.operation_id = s.operation_id
            WHERE s.recipe_version_id = version_id AND p.required
            AND NOT EXISTS (SELECT 1 FROM recipeweave.step_parameter v WHERE v.step_id = s.id AND v.parameter_id = p.id)
        ) THEN RAISE EXCEPTION '必須の工程パラメータがありません' USING ERRCODE = '23514'; END IF;
        IF EXISTS (
            SELECT 1 FROM recipeweave.material_node n JOIN recipeweave.step_input i ON i.material_id = n.id
            WHERE n.recipe_version_id = version_id AND n.producer_step_id IS NOT NULL
              AND NOT EXISTS (SELECT 1 FROM recipeweave.step_dependency d WHERE d.before_step_id = n.producer_step_id
                  AND d.after_step_id = i.step_id AND d.kind = 'material')
        ) THEN RAISE EXCEPTION '生成材料の受渡しに材料依存辺がありません' USING ERRCODE = '23514'; END IF;
    END IF;
END;
$$;

CREATE FUNCTION recipeweave.check_recipe_integrity() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    version_id uuid;
BEGIN
    IF TG_OP <> 'DELETE' THEN
        version_id := recipeweave.recipe_version_for(TG_TABLE_NAME, to_jsonb(NEW));
        PERFORM recipeweave.validate_recipe_version(version_id);
    END IF;
    IF TG_OP <> 'INSERT' THEN
        version_id := recipeweave.recipe_version_for(TG_TABLE_NAME, to_jsonb(OLD));
        PERFORM recipeweave.validate_recipe_version(version_id);
    END IF;
    RETURN NULL;
END;
$$;

CREATE FUNCTION recipeweave.check_hierarchy() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    cycle_found boolean;
    parent_release uuid;
BEGIN

    EXECUTE format('SELECT * FROM recipeweave.%I WHERE id = $1', TG_TABLE_NAME) INTO NEW USING NEW.id;
    IF NEW.id IS NULL THEN RETURN NULL; END IF;
    IF TG_TABLE_NAME = 'food' THEN
        PERFORM 1 FROM recipeweave.catalog_release WHERE id = NEW.release_id FOR UPDATE;
        SELECT release_id INTO parent_release FROM recipeweave.food WHERE id = NEW.parent_id;
        IF parent_release IS DISTINCT FROM NEW.release_id AND NEW.parent_id IS NOT NULL THEN
            RAISE EXCEPTION '食材の親は同じカタログ版に属する必要があります' USING ERRCODE = '23514';
        END IF;
        WITH RECURSIVE parents(id, parent_id) AS (
            SELECT id, parent_id FROM recipeweave.food WHERE id = NEW.parent_id
            UNION
            SELECT f.id, f.parent_id FROM recipeweave.food f JOIN parents p ON f.id = p.parent_id
        ) SELECT EXISTS (SELECT 1 FROM parents WHERE id = NEW.id) INTO cycle_found;
    ELSE
        PERFORM 1 FROM recipeweave.axis WHERE id = NEW.axis_id FOR UPDATE;
        SELECT axis_id INTO parent_release FROM recipeweave.axis_option WHERE id = NEW.parent_id;
        IF parent_release IS DISTINCT FROM NEW.axis_id AND NEW.parent_id IS NOT NULL THEN
            RAISE EXCEPTION '候補値の親は同じ軸に属する必要があります' USING ERRCODE = '23514';
        END IF;
        WITH RECURSIVE parents(id, parent_id) AS (
            SELECT id, parent_id FROM recipeweave.axis_option WHERE id = NEW.parent_id
            UNION
            SELECT f.id, f.parent_id FROM recipeweave.axis_option f JOIN parents p ON f.id = p.parent_id
        ) SELECT EXISTS (SELECT 1 FROM parents WHERE id = NEW.id) INTO cycle_found;
    END IF;
    IF cycle_found THEN RAISE EXCEPTION '分類階層に循環があります' USING ERRCODE = '23514'; END IF;
    RETURN NULL;
END;
$$;

CREATE FUNCTION recipeweave.check_cross_reference() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    valid boolean := true;
BEGIN

    EXECUTE format('SELECT * FROM recipeweave.%I WHERE id = $1', TG_TABLE_NAME) INTO NEW USING NEW.id;
    IF NEW.id IS NULL THEN RETURN NULL; END IF;
    CASE TG_TABLE_NAME
    WHEN 'product_version' THEN
        SELECT p.food_id = f.food_id INTO valid FROM recipeweave.product p, recipeweave.food_form f
        WHERE p.id = NEW.product_id AND f.id = NEW.form_id;
    WHEN 'food_axis_option' THEN
        SELECT f.release_id = a.release_id INTO valid FROM recipeweave.food f,
        recipeweave.axis_option o JOIN recipeweave.axis a ON a.id = o.axis_id
        WHERE f.id = NEW.food_id AND o.id = NEW.option_id;
    WHEN 'food_identity_member' THEN
        SELECT normalizer_version = NEW.normalizer_version INTO valid
        FROM recipeweave.food_identity WHERE id = NEW.identity_id;
    WHEN 'generation_choice' THEN
        SELECT p.release_id = a.release_id INTO valid
        FROM recipeweave.generation_job j JOIN recipeweave.generation_policy p ON p.id = j.policy_id,
        recipeweave.axis_option o JOIN recipeweave.axis a ON a.id = o.axis_id
        WHERE j.id = NEW.job_id AND o.id = NEW.option_id;
    WHEN 'generation_food' THEN
        SELECT p.release_id = f.release_id INTO valid
        FROM recipeweave.generation_job j JOIN recipeweave.generation_policy p ON p.id = j.policy_id,
        recipeweave.food_form form JOIN recipeweave.food f ON f.id = form.food_id
        WHERE j.id = NEW.job_id AND form.id = NEW.form_id;
    WHEN 'generation_result' THEN
        SELECT v.release_id = p.release_id AND (NEW.job_id IS NULL OR j.policy_id = p.id) INTO valid
        FROM recipeweave.recipe_version v, recipeweave.generation_policy p
        LEFT JOIN recipeweave.generation_job j ON j.id = NEW.job_id
        WHERE v.id = NEW.recipe_version_id AND p.id = NEW.policy_id;
    WHEN 'generation_shard' THEN
        SELECT NEW.end_ordinal <= candidate_count INTO valid FROM recipeweave.generation_template WHERE id = NEW.template_id;
    WHEN 'candidate_attempt' THEN
        SELECT NEW.ordinal < candidate_count INTO valid FROM recipeweave.generation_template WHERE id = NEW.template_id;
    WHEN 'recipe_search_document' THEN
        SELECT recipe_id = NEW.recipe_id AND status = 'published' INTO valid
        FROM recipeweave.recipe_version WHERE id = NEW.published_version_id;
        valid := valid AND NOT EXISTS (SELECT 1 FROM unnest(NEW.food_identity_ids) item WHERE NOT EXISTS (
            SELECT 1 FROM recipeweave.food_identity WHERE id = item))
            AND NOT EXISTS (SELECT 1 FROM unnest(NEW.facet_option_ids) item WHERE NOT EXISTS (
                SELECT 1 FROM recipeweave.axis_option WHERE id = item));
    ELSE
        RAISE EXCEPTION '未定義の関連検査対象です';
    END CASE;
    IF NOT coalesce(valid, false) THEN RAISE EXCEPTION '参照先と版・所属・序数が一致しません' USING ERRCODE = '23514'; END IF;
    RETURN NULL;
END;
$$;

CREATE FUNCTION recipeweave.release_for(table_name TEXT, row_data JSONB) RETURNS UUID
LANGUAGE plpgsql STABLE AS $$
DECLARE
    target uuid;
BEGIN
    IF table_name = 'catalog_release' THEN RETURN (row_data->>'id')::uuid;
    ELSIF row_data ? 'release_id' THEN RETURN (row_data->>'release_id')::uuid;
    ELSIF table_name IN ('food_alias', 'food_form', 'product', 'food_identity_member', 'food_axis_option') THEN
        SELECT release_id INTO target FROM recipeweave.food WHERE id = (row_data->>'food_id')::uuid;
    ELSIF table_name = 'axis_option' THEN
        SELECT release_id INTO target FROM recipeweave.axis WHERE id = (row_data->>'axis_id')::uuid;
    ELSIF table_name IN ('food_allergen', 'nutrition_fact') AND row_data->>'form_id' IS NOT NULL THEN
        SELECT food.release_id INTO target FROM recipeweave.food_form form
        JOIN recipeweave.food food ON food.id = form.food_id WHERE form.id = (row_data->>'form_id')::uuid;
    ELSIF table_name = 'product_version' THEN
        SELECT food.release_id INTO target FROM recipeweave.product product
        JOIN recipeweave.food food ON food.id = product.food_id WHERE product.id = (row_data->>'product_id')::uuid;
    ELSIF table_name IN ('product_component', 'product_allergen', 'product_preparation_rule', 'nutrition_fact') THEN
        SELECT food.release_id INTO target FROM recipeweave.product_version AS "version"
        JOIN recipeweave.product product ON product.id = version.product_id
        JOIN recipeweave.food food ON food.id = product.food_id WHERE version.id = (row_data->>'product_version_id')::uuid;
    END IF;
    RETURN target;
END;
$$;

CREATE FUNCTION recipeweave.guard_catalog_content() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    target uuid;
BEGIN
    IF TG_OP <> 'INSERT' THEN
        target := recipeweave.release_for(TG_TABLE_NAME, to_jsonb(OLD));
        IF EXISTS (SELECT 1 FROM recipeweave.catalog_release WHERE id = target AND published_at IS NOT NULL) THEN
            RAISE EXCEPTION '公開済みカタログの内容は変更・削除できません' USING ERRCODE = '23514';
        END IF;
    END IF;
    IF TG_OP <> 'DELETE' AND TG_TABLE_NAME <> 'catalog_release' THEN
        target := recipeweave.release_for(TG_TABLE_NAME, to_jsonb(NEW));
        PERFORM 1 FROM recipeweave.catalog_release WHERE id = target FOR UPDATE;
        IF EXISTS (SELECT 1 FROM recipeweave.catalog_release WHERE id = target AND published_at IS NOT NULL) THEN
            RAISE EXCEPTION '公開済みカタログへ内容を追加・移動できません' USING ERRCODE = '23514';
        END IF;
    END IF;
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$;

CREATE FUNCTION recipeweave.validate_cooking_session(target UUID) RETURNS VOID
LANGUAGE plpgsql AS $$
DECLARE
    session_menu uuid;
    session_owner uuid;
BEGIN
    SELECT s.menu_id, m.user_id INTO session_menu, session_owner FROM recipeweave.cooking_session s
    JOIN recipeweave.menu m ON m.id = s.menu_id WHERE s.id = target FOR UPDATE OF s;
    IF NOT FOUND THEN RETURN; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.session_task t
        JOIN recipeweave.menu_item item ON item.id = t.menu_item_id
        JOIN recipeweave.recipe_step step ON step.id = t.step_id
        WHERE t.session_id = target AND (item.menu_id <> session_menu OR item.recipe_version_id <> step.recipe_version_id)
    ) THEN RAISE EXCEPTION '調理タスクと献立・レシピ版が一致しません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.task_dependency d
        JOIN recipeweave.session_task b ON b.id = d.before_task_id
        JOIN recipeweave.session_task a ON a.id = d.after_task_id
        WHERE (b.session_id = target OR a.session_id = target) AND (
            b.session_id <> a.session_id OR a.planned_start_s < b.planned_end_s + d.min_lag_s
            OR a.planned_start_s > b.planned_end_s + d.max_lag_s
        )
    ) THEN RAISE EXCEPTION 'タスクの所属または待機時間を満たせません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        WITH RECURSIVE reach(before_id, after_id) AS (
            SELECT d.before_task_id, d.after_task_id FROM recipeweave.task_dependency d
            JOIN recipeweave.session_task t ON t.id = d.before_task_id WHERE t.session_id = target
            UNION
            SELECT r.before_id, d.after_task_id FROM reach r
            JOIN recipeweave.task_dependency d ON d.before_task_id = r.after_id
        ) SELECT 1 FROM reach WHERE before_id = after_id
    ) THEN RAISE EXCEPTION '調理タスクの依存に循環があります' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.resource_reservation r
        JOIN recipeweave.session_task t ON t.id = r.task_id
        JOIN recipeweave.kitchen_resource k ON k.id = r.resource_id
        WHERE t.session_id = target AND (k.user_id <> session_owner OR r.start_s < t.planned_start_s OR r.end_s > t.planned_end_s)
    ) THEN RAISE EXCEPTION '他人の資源またはタスク外の時間を予約できません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        WITH reservations AS (
            SELECT r.* FROM recipeweave.resource_reservation r JOIN recipeweave.session_task t ON t.id = r.task_id
            WHERE t.session_id = target
        ) SELECT 1 FROM reservations point JOIN recipeweave.kitchen_resource k ON k.id = point.resource_id
        WHERE (SELECT sum(overlap.quantity) FROM reservations overlap WHERE overlap.resource_id = point.resource_id
            AND overlap.start_s <= point.start_s AND point.start_s < overlap.end_s) > k.quantity
    ) THEN RAISE EXCEPTION '同時予約が利用可能な資源数を超えています' USING ERRCODE = '23514'; END IF;
END;
$$;

CREATE FUNCTION recipeweave.check_owned_reference() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    target uuid;
    valid boolean := true;
BEGIN

    EXECUTE format('SELECT * FROM recipeweave.%I WHERE id = $1', TG_TABLE_NAME) INTO NEW USING NEW.id;
    IF NEW.id IS NULL THEN RETURN NULL; END IF;
    CASE TG_TABLE_NAME
    WHEN 'menu_ingredient_override' THEN
        SELECT item.recipe_version_id = ingredient.recipe_version_id INTO valid
        FROM recipeweave.menu_item item, recipeweave.recipe_ingredient ingredient
        WHERE item.id = NEW.menu_item_id AND ingredient.id = NEW.ingredient_line_id;
    WHEN 'shopping_item' THEN
        SELECT session_id = NEW.session_id INTO valid FROM recipeweave.ingredient_total WHERE id = NEW.total_id;
    WHEN 'pantry_lot' THEN
        IF NEW.product_version_id IS NOT NULL THEN
            SELECT form_id = NEW.form_id INTO valid FROM recipeweave.product_version WHERE id = NEW.product_version_id;
        END IF;
    WHEN 'session_task' THEN target := NEW.session_id;
    WHEN 'cooking_session' THEN target := NEW.id;
    WHEN 'task_dependency' THEN
        SELECT session_id INTO target FROM recipeweave.session_task WHERE id = NEW.before_task_id;
    WHEN 'resource_reservation' THEN
        PERFORM 1 FROM recipeweave.kitchen_resource WHERE id = NEW.resource_id FOR UPDATE;
        SELECT session_id INTO target FROM recipeweave.session_task WHERE id = NEW.task_id;
    ELSE RAISE EXCEPTION '未定義の所有データ検査対象です';
    END CASE;
    IF NOT coalesce(valid, false) THEN RAISE EXCEPTION '所有データの親子関係が一致しません' USING ERRCODE = '23514'; END IF;
    PERFORM recipeweave.validate_cooking_session(target);
    RETURN NULL;
END;
$$;

CREATE FUNCTION recipeweave.guard_execution_progress() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF TG_TABLE_NAME = 'session_task' THEN
    IF OLD.status IN ('running', 'completed') AND (
        NEW.planned_start_s <> OLD.planned_start_s OR NEW.planned_end_s <> OLD.planned_end_s
        OR NEW.step_id <> OLD.step_id OR NEW.menu_item_id <> OLD.menu_item_id OR NEW.batch_no <> OLD.batch_no
        OR NEW.session_id <> OLD.session_id OR (OLD.status = 'completed' AND NEW.status <> 'completed')
    ) THEN RAISE EXCEPTION '実行中・完了済みタスクを再配置できません' USING ERRCODE = '23514'; END IF;
    END IF;
    IF TG_TABLE_NAME = 'generation_shard' THEN
    IF (
        NEW.template_id <> OLD.template_id OR NEW.start_ordinal <> OLD.start_ordinal OR NEW.end_ordinal <> OLD.end_ordinal
        OR NEW.next_ordinal < OLD.next_ordinal OR NEW.fence_token < OLD.fence_token
        OR (NEW.lease_owner IS DISTINCT FROM OLD.lease_owner AND NEW.lease_owner IS NOT NULL AND NEW.fence_token <= OLD.fence_token)
        OR (OLD.state = 'done' AND NEW.state <> 'done')
    ) THEN RAISE EXCEPTION '生成範囲・再開位置・リース世代の更新が不正です' USING ERRCODE = '23514'; END IF;
    END IF;
    RETURN NEW;
END;
$$;

CREATE FUNCTION recipeweave.guard_audit() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'UPDATE' AND NEW.actor_id IS NULL AND OLD.actor_id IS NOT NULL
       AND (to_jsonb(NEW) - 'actor_id') = (to_jsonb(OLD) - 'actor_id') THEN RETURN NEW; END IF;
    RAISE EXCEPTION '監査イベントは追記専用です' USING ERRCODE = '23514';
END;
$$;

CREATE FUNCTION recipeweave.publish_outbox() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    identifier uuid := gen_random_uuid();
    aggregate uuid;
    event_name text;
BEGIN
    IF TG_TABLE_NAME = 'app_user' THEN
        aggregate := OLD.id;
        event_name := 'user_erased';
    ELSIF TG_TABLE_NAME = 'recipe_version' THEN
        aggregate := NEW.recipe_id;
        IF NEW.status = 'published' AND (TG_OP = 'INSERT' OR OLD.status IS DISTINCT FROM NEW.status) THEN
            event_name := 'recipe_published';
        ELSIF NEW.status = 'withdrawn' AND OLD.status IS DISTINCT FROM NEW.status THEN
            event_name := 'recipe_withdrawn';
            DELETE FROM recipeweave.recipe_search_document WHERE published_version_id = NEW.id;
            DELETE FROM recipeweave.recipe_embedding WHERE recipe_version_id = NEW.id;
        ELSE RETURN NEW;
        END IF;
    ELSE
        aggregate := NEW.id;
        IF NEW.status <> 'withdrawn' OR OLD.status = NEW.status THEN RETURN NEW; END IF;
        event_name := 'recipe_withdrawn';
        DELETE FROM recipeweave.recipe_search_document WHERE recipe_id = NEW.id;
        DELETE FROM recipeweave.recipe_embedding WHERE recipe_version_id IN (
            SELECT id FROM recipeweave.recipe_version WHERE recipe_id = NEW.id
        );
    END IF;
    INSERT INTO recipeweave.outbox_event (id, event_type, aggregate_id, payload, attempt_count)
    VALUES (identifier, event_name, aggregate, jsonb_build_object(
        'schema_version', 1, 'event_id', identifier, 'aggregate_id', aggregate, 'version', 1
    ), 0);
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$;

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.source_record
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.catalog_release
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.unit
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food_alias
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food_form
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.conversion
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.form_yield
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.product
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.product_version
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.product_component
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.allergen
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food_allergen
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.product_allergen
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.nutrient
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.nutrition_fact
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.axis
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.axis_option
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food_axis_option
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_version
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_option
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.scaling_rule
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.scaling_point
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_ingredient
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.operation
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.operation_parameter
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_step
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.step_parameter
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.material_node
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.step_input
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.step_dependency
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.resource_type
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.step_resource
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.media_asset
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.step_media
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_policy
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_job
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_choice
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_food
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_result
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.compatibility_rule
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.validation_result
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_signature
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_similarity
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.app_user
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.user_preference
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.user_exclusion
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.user_recipe_event
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.menu
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.menu_item
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.menu_ingredient_override
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.kitchen_resource
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.cooking_session
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.session_task
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.task_dependency
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.resource_reservation
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.ingredient_total
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.pantry_lot
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.shopping_item
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.audit_event
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.outbox_event
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.product_preparation_rule
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food_identity
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food_identity_member
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_template
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_shard
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.candidate_attempt
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_search_document
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_embedding
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_stratum_metric
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change();

CREATE TRIGGER protect_recipe BEFORE UPDATE OR DELETE ON recipeweave.recipe_version
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content();

CREATE CONSTRAINT TRIGGER recipe_integrity AFTER INSERT OR UPDATE OR DELETE ON recipeweave.recipe_version
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity();

CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.recipe_ingredient
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content();

CREATE CONSTRAINT TRIGGER recipe_integrity AFTER INSERT OR UPDATE OR DELETE ON recipeweave.recipe_ingredient
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity();

CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.recipe_option
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content();

CREATE CONSTRAINT TRIGGER recipe_integrity AFTER INSERT OR UPDATE OR DELETE ON recipeweave.recipe_option
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity();

CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.recipe_step
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content();

CREATE CONSTRAINT TRIGGER recipe_integrity AFTER INSERT OR UPDATE OR DELETE ON recipeweave.recipe_step
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity();

CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.step_parameter
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content();

CREATE CONSTRAINT TRIGGER recipe_integrity AFTER INSERT OR UPDATE OR DELETE ON recipeweave.step_parameter
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity();

CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.material_node
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content();

CREATE CONSTRAINT TRIGGER recipe_integrity AFTER INSERT OR UPDATE OR DELETE ON recipeweave.material_node
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity();

CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.step_input
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content();

CREATE CONSTRAINT TRIGGER recipe_integrity AFTER INSERT OR UPDATE OR DELETE ON recipeweave.step_input
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity();

CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.step_dependency
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content();

CREATE CONSTRAINT TRIGGER recipe_integrity AFTER INSERT OR UPDATE OR DELETE ON recipeweave.step_dependency
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity();

CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.step_resource
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content();

CREATE CONSTRAINT TRIGGER recipe_integrity AFTER INSERT OR UPDATE OR DELETE ON recipeweave.step_resource
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity();

CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.step_media
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content();

CREATE CONSTRAINT TRIGGER recipe_integrity AFTER INSERT OR UPDATE OR DELETE ON recipeweave.step_media
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity();

CREATE CONSTRAINT TRIGGER hierarchy_integrity AFTER INSERT OR UPDATE ON recipeweave.food
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_hierarchy();

CREATE CONSTRAINT TRIGGER hierarchy_integrity AFTER INSERT OR UPDATE ON recipeweave.axis_option
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_hierarchy();

CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.product_version
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference();

CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.food_axis_option
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference();

CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.food_identity_member
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference();

CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.generation_choice
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference();

CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.generation_food
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference();

CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.generation_result
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference();

CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.generation_shard
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference();

CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.candidate_attempt
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference();

CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.recipe_search_document
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference();

CREATE TRIGGER protect_catalog BEFORE UPDATE OR DELETE ON recipeweave.catalog_release
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.food
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.food_alias
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.food_form
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.product
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.food_identity_member
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.food_axis_option
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.axis
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.axis_option
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.food_allergen
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.nutrition_fact
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.product_version
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.product_component
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.product_allergen
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.product_preparation_rule
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.conversion
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.generation_policy
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.generation_template
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content();

CREATE CONSTRAINT TRIGGER owned_integrity AFTER INSERT OR UPDATE ON recipeweave.menu_ingredient_override
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference();

CREATE CONSTRAINT TRIGGER owned_integrity AFTER INSERT OR UPDATE ON recipeweave.shopping_item
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference();

CREATE CONSTRAINT TRIGGER owned_integrity AFTER INSERT OR UPDATE ON recipeweave.pantry_lot
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference();

CREATE CONSTRAINT TRIGGER owned_integrity AFTER INSERT OR UPDATE ON recipeweave.session_task
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference();

CREATE CONSTRAINT TRIGGER owned_integrity AFTER INSERT OR UPDATE ON recipeweave.cooking_session
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference();

CREATE CONSTRAINT TRIGGER owned_integrity AFTER INSERT OR UPDATE ON recipeweave.task_dependency
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference();

CREATE CONSTRAINT TRIGGER owned_integrity AFTER INSERT OR UPDATE ON recipeweave.resource_reservation
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference();

CREATE TRIGGER execution_progress BEFORE UPDATE ON recipeweave.session_task
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_execution_progress();

CREATE TRIGGER execution_progress BEFORE UPDATE ON recipeweave.generation_shard
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_execution_progress();

CREATE TRIGGER audit_append_only BEFORE UPDATE OR DELETE ON recipeweave.audit_event
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_audit();

CREATE TRIGGER lifecycle_outbox AFTER INSERT OR UPDATE ON recipeweave.recipe_version
FOR EACH ROW EXECUTE FUNCTION recipeweave.publish_outbox();

CREATE TRIGGER lifecycle_outbox AFTER UPDATE ON recipeweave.recipe
FOR EACH ROW EXECUTE FUNCTION recipeweave.publish_outbox();

CREATE TRIGGER lifecycle_outbox AFTER DELETE ON recipeweave.app_user
FOR EACH ROW EXECUTE FUNCTION recipeweave.publish_outbox();

ALTER TABLE recipeweave.app_user ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.app_user FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.app_user
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR app_user.id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR app_user.id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

ALTER TABLE recipeweave.user_preference ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.user_preference FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.user_preference
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR user_preference.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR user_preference.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

ALTER TABLE recipeweave.user_exclusion ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.user_exclusion FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.user_exclusion
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR user_exclusion.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR user_exclusion.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

ALTER TABLE recipeweave.user_recipe_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.user_recipe_event FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.user_recipe_event
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR user_recipe_event.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR user_recipe_event.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

ALTER TABLE recipeweave.menu ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.menu FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.menu
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR menu.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR menu.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

ALTER TABLE recipeweave.menu_item ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.menu_item FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.menu_item
USING (
    CURRENT_SETTING(
        'recipeweave.role', true) = 'admin' OR (
        SELECT r0.user_id FROM recipeweave.menu AS r0
        WHERE r0.id = menu_item.menu_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), ''
    )::UUID
) WITH CHECK (CURRENT_SETTING(
    'recipeweave.role', true) = 'admin' OR (
    SELECT r0.user_id FROM recipeweave.menu AS r0
    WHERE r0.id = menu_item.menu_id
) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), ''
)::UUID);

ALTER TABLE recipeweave.menu_ingredient_override ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.menu_ingredient_override FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.menu_ingredient_override
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR (
        SELECT r1.user_id
        FROM recipeweave.menu_item AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = menu_ingredient_override.menu_item_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin' OR (
        SELECT r1.user_id
        FROM recipeweave.menu_item AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = menu_ingredient_override.menu_item_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

ALTER TABLE recipeweave.kitchen_resource ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.kitchen_resource FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.kitchen_resource
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR kitchen_resource.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR kitchen_resource.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

ALTER TABLE recipeweave.cooking_session ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.cooking_session FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.cooking_session
USING (
    CURRENT_SETTING(
        'recipeweave.role', true) = 'admin' OR (
        SELECT r0.user_id FROM recipeweave.menu AS r0
        WHERE r0.id = cooking_session.menu_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), ''
    )::UUID
) WITH CHECK (CURRENT_SETTING(
    'recipeweave.role', true) = 'admin' OR (
    SELECT r0.user_id FROM recipeweave.menu AS r0
    WHERE r0.id = cooking_session.menu_id
) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), ''
)::UUID);

ALTER TABLE recipeweave.session_task ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.session_task FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.session_task
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR (
        SELECT r1.user_id
        FROM recipeweave.cooking_session AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = session_task.session_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin' OR (
        SELECT r1.user_id
        FROM recipeweave.cooking_session AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = session_task.session_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

ALTER TABLE recipeweave.task_dependency ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.task_dependency FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.task_dependency
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR (
        SELECT r2.user_id
        FROM recipeweave.session_task AS r0
        INNER JOIN recipeweave.cooking_session AS r1 ON r0.session_id = r1.id
        INNER JOIN recipeweave.menu AS r2 ON r1.menu_id = r2.id
        WHERE r0.id = task_dependency.before_task_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin' OR (
        SELECT r2.user_id
        FROM recipeweave.session_task AS r0
        INNER JOIN recipeweave.cooking_session AS r1 ON r0.session_id = r1.id
        INNER JOIN recipeweave.menu AS r2 ON r1.menu_id = r2.id
        WHERE r0.id = task_dependency.before_task_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

ALTER TABLE recipeweave.resource_reservation ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.resource_reservation FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.resource_reservation
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR (
        SELECT r2.user_id
        FROM recipeweave.session_task AS r0
        INNER JOIN recipeweave.cooking_session AS r1 ON r0.session_id = r1.id
        INNER JOIN recipeweave.menu AS r2 ON r1.menu_id = r2.id
        WHERE r0.id = resource_reservation.task_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin' OR (
        SELECT r2.user_id
        FROM recipeweave.session_task AS r0
        INNER JOIN recipeweave.cooking_session AS r1 ON r0.session_id = r1.id
        INNER JOIN recipeweave.menu AS r2 ON r1.menu_id = r2.id
        WHERE r0.id = resource_reservation.task_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

ALTER TABLE recipeweave.ingredient_total ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.ingredient_total FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.ingredient_total
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR (
        SELECT r1.user_id
        FROM recipeweave.cooking_session AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = ingredient_total.session_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin' OR (
        SELECT r1.user_id
        FROM recipeweave.cooking_session AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = ingredient_total.session_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

ALTER TABLE recipeweave.pantry_lot ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.pantry_lot FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.pantry_lot
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR pantry_lot.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR pantry_lot.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

ALTER TABLE recipeweave.shopping_item ENABLE ROW LEVEL SECURITY;

ALTER TABLE recipeweave.shopping_item FORCE ROW LEVEL SECURITY;

CREATE POLICY owned_access ON recipeweave.shopping_item
USING (
    CURRENT_SETTING('recipeweave.role', true) = 'admin'
    OR (
        SELECT r1.user_id
        FROM recipeweave.cooking_session AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = shopping_item.session_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', true) = 'admin' OR (
        SELECT r1.user_id
        FROM recipeweave.cooking_session AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = shopping_item.session_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', true), '')::UUID
);

CREATE FUNCTION recipeweave.guard_adopted_definition() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    reference record;
    referenced boolean;
BEGIN
    FOR reference IN
        SELECT namespace.nspname AS schema_name, child.relname AS table_name, attribute.attname AS column_name
        FROM pg_constraint constraint_def
        JOIN pg_class child ON child.oid = constraint_def.conrelid
        JOIN pg_namespace namespace ON namespace.oid = child.relnamespace
        JOIN pg_attribute attribute ON attribute.attrelid = child.oid AND attribute.attnum = constraint_def.conkey[1]
        WHERE constraint_def.contype = 'f' AND constraint_def.confrelid = TG_RELID
          AND namespace.nspname = 'recipeweave' AND cardinality(constraint_def.conkey) = 1
    LOOP
        EXECUTE format('SELECT EXISTS (SELECT 1 FROM %I.%I WHERE %I = $1)',
            reference.schema_name, reference.table_name, reference.column_name) INTO referenced USING OLD.id;
        IF referenced THEN
            RAISE EXCEPTION '採用済みの定義版は変更・削除できません。新IDを作成してください' USING ERRCODE = '23514';
        END IF;
    END LOOP;
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$;

CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.product_version
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition();

CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.product_component
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition();

CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.conversion
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition();

CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.scaling_rule
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition();

CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.media_asset
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition();

CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.generation_policy
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition();

CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.food_identity
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition();

CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.generation_template
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition();

CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.operation_parameter
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition();
