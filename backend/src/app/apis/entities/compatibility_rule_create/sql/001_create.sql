-- 組み合わせ・公開ルールを作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.compatibility_rule AS t (
    id,
    code,
    version,
    severity,
    predicate,
    message,
    source_id,
    status
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(version)s,
    %(severity)s,
    %(predicate)s,
    %(message)s,
    %(source_id)s,
    %(status)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.version,
    t.severity,
    t.predicate,
    t.message,
    t.source_id,
    t.status,
    t.xmin::TEXT AS etag;
