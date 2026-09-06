# SQL仕様: list_foods

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## backend/src/app/apis/foods/list_foods/sql/001_select_foods.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.axis | R | code, id |
| recipeweave.axis_option | R | axis_id, code, id, label |
| recipeweave.food | R | id, kind, name, status |
| recipeweave.food_alias | R | alias, food_id, locale |
| recipeweave.food_axis_option | R | food_id, option_id |
| recipeweave.food_form | R | base_unit_id, food_id, id, name, state, status |
| recipeweave.unit | R | code, id |

バインド変数: q

```sql
-- 正規化した食品・形態・分類・別名から検索用の食品一覧を取得する。
WITH available AS (
    SELECT
        food.id,
        food.name,
        food.kind,
        form.state,
        unit.code AS unit_code,
        COALESCE(aliases.alias_names, '[]'::JSONB) AS aliases,
        COALESCE(attributes.category, 'その他') AS category,
        COALESCE(
            attributes.storage_location,
            CASE
                WHEN form.state = 'frozen' THEN '冷凍'
                WHEN form.state = 'raw' THEN '冷蔵' ELSE '常温'
            END
        ) AS storage_location,
        COALESCE(attributes.pantry, FALSE) AS pantry
    FROM recipeweave.food AS food
    INNER JOIN LATERAL (
        SELECT
            food_form.state,
            food_form.base_unit_id
        FROM recipeweave.food_form AS food_form
        WHERE food_form.food_id = food.id AND food_form.status = 'active'
        ORDER BY (food_form.name = '標準') DESC, food_form.id
        LIMIT 1
    ) AS form ON TRUE
    INNER JOIN recipeweave.unit AS unit ON form.base_unit_id = unit.id
    LEFT JOIN LATERAL (
        SELECT JSONB_AGG(food_alias.alias ORDER BY food_alias.alias) AS alias_names
        FROM recipeweave.food_alias AS food_alias
        WHERE food_alias.food_id = food.id AND food_alias.locale = 'ja'
    ) AS aliases ON TRUE
    LEFT JOIN LATERAL (
        SELECT
            MAX(axis_option.label) FILTER (WHERE axis.code = 'store_category') AS category,
            MAX(axis_option.label) FILTER (WHERE axis.code = 'storage_location')
                AS storage_location,
            BOOL_OR(axis_option.code = 'true') FILTER (WHERE axis.code = 'pantry_default') AS pantry
        FROM recipeweave.food_axis_option AS relation
        INNER JOIN recipeweave.axis_option AS axis_option ON relation.option_id = axis_option.id
        INNER JOIN recipeweave.axis AS axis ON axis_option.axis_id = axis.id
        WHERE relation.food_id = food.id
    ) AS attributes ON TRUE
    WHERE
        food.status = 'active'
        AND (
            %(q)s = '' OR STRPOS(LOWER(food.name), LOWER(%(q)s)) > 0
            OR EXISTS (
                SELECT 1 FROM recipeweave.food_alias AS alias_filter
                WHERE
                    alias_filter.food_id = food.id
                    AND STRPOS(LOWER(alias_filter.alias), LOWER(%(q)s)) > 0
            )
        )
)

SELECT
    COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
        'id', available.id::TEXT,
        'name', available.name,
        'aliases', available.aliases,
        'category', available.category,
        'defaultUnit', available.unit_code,
        'location', available.storage_location,
        'pantry', available.pantry,
        'imageIndex', NULL,
        'componentsKnown', available.kind IN ('basic', 'utility'),
        'componentFoodIds', '[]'::JSONB
    ) ORDER BY available.name, available.id), '[]'::JSONB) AS items,
    COUNT(available.id) AS total
FROM available;
```

SQLファイル→自動生成wrapper→連携adapter→functions→routerの境界で管理する。利用者入力はパラメーターとして渡し、SQL文字列へ連結しない。
