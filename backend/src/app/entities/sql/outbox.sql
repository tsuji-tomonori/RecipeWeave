-- カタログ変更の配信要求を業務と同じトランザクションで追記する。
INSERT INTO recipeweave.outbox_event (
    id, event_type, aggregate_id, payload, attempt_count
)
VALUES (
    %(row_id)s, %(event_type)s, %(aggregate_id)s,
    JSONB_BUILD_OBJECT(
        'schema_version', 1,
        'event_id', %(row_id)s::TEXT,
        'aggregate_id', %(aggregate_id)s::TEXT,
        'version', 1
    ), 0
)
RETURNING id;
