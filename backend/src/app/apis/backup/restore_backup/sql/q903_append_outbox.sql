-- 復元完了の本人IDと更新版だけをoutboxへ記録する。
INSERT INTO recipeweave.outbox_event
(id, event_type, aggregate_id, payload, attempt_count)
VALUES (
    %(event_id)s, 'workspace.restored', %(actor_id)s,
    JSONB_BUILD_OBJECT(
        'schema_version', 1, 'event_id', %(event_id)s::TEXT,
        'aggregate_id', %(actor_id)s::TEXT, 'version', %(version)s::BIGINT
    ),
    0
);
