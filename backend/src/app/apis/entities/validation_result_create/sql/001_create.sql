-- 公開前評価結果を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.validation_result AS t (
    id,
    recipe_version_id,
    rule_id,
    state,
    evidence,
    validator_version,
    evaluated_at
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(rule_id)s,
    %(state)s,
    %(evidence)s,
    %(validator_version)s,
    %(evaluated_at)s
)
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.rule_id,
    t.state,
    t.evidence,
    t.validator_version,
    t.evaluated_at,
    t.xmin::TEXT AS etag;
