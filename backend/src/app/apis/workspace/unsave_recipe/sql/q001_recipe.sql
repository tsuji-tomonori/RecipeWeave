-- 公開条件を満たす料理版を保存対象として確認する。
SELECT rv.id
FROM recipeweave.recipe_version AS rv
INNER JOIN recipeweave.recipe AS r ON rv.recipe_id = r.id
WHERE
    r.id = %(recipe_id)s AND (
        (rv.status = 'published' AND r.status = 'published' AND rv.validation = 'passed')
        OR (%(preview)s AND rv.status = 'draft')
    )
ORDER BY rv.version DESC LIMIT 1;
