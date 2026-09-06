"""接続アダプターのテストは生成SQLを使い、AWSへ接続しない。"""

from unittest.mock import MagicMock, patch

import pytest
from psycopg.errors import SerializationFailure, UniqueViolation

pytest.importorskip(
    "app.apis.state.get_state.generated.queries",
    reason="SQL wrappers require the locked SQLGlot generator before adapter validation",
)

from app.core.errors import ServiceUnavailableError, StateConflictError
from app.core.models import AppSnapshot
from app.core.settings import AppSettings
from app.integrations.state.dsql_provider import DsqlStateRepository

PROVIDER = "app.integrations.state.dsql_provider."


def test_fresh_non_admin_tokens_and_verified_tls() -> None:
    token_client = MagicMock()
    token_client.generate_db_connect_auth_token.return_value = "test-only-generated-token"
    with (
        patch(PROVIDER + "boto3.client", return_value=token_client),
        patch(PROVIDER + "psycopg.connect") as connect,
        patch(PROVIDER + "select_state", return_value=None) as select,
    ):
        repository = DsqlStateRepository(
            AppSettings(dsql_host="example.dsql.ap-northeast-1.on.aws")
        )
        assert repository.get("user-a").version == 0
        assert repository.get("user-b").version == 0
        assert token_client.generate_db_connect_auth_token.call_count == 2
        assert connect.call_args.kwargs["sslmode"] == "verify-full"
        assert connect.call_args.kwargs["user"] == "recipeweave_app"
        assert select.call_args.args[1] == "user-b"
        assert not token_client.generate_db_connect_admin_auth_token.called


def test_admin_application_role_is_rejected_before_sdk_construction() -> None:
    with pytest.raises(ServiceUnavailableError):
        DsqlStateRepository(
            AppSettings(
                dsql_host="example.dsql.ap-northeast-1.on.aws",
                dsql_database_user="admin",
            )
        )


def test_occ_retry_is_bounded(snapshot: AppSnapshot) -> None:
    with (
        patch(PROVIDER + "boto3.client"),
        patch(PROVIDER + "psycopg.connect"),
        patch(PROVIDER + "time.sleep"),
        patch(PROVIDER + "update_state", side_effect=SerializationFailure()) as update,
    ):
        repository = DsqlStateRepository(
            AppSettings(dsql_host="example.dsql.ap-northeast-1.on.aws")
        )
        with pytest.raises(ServiceUnavailableError):
            repository.put("user-a", 3, snapshot)
        assert update.call_count == 3


def test_revision_conflicts_do_not_retry_or_overwrite(snapshot: AppSnapshot) -> None:
    with (
        patch(PROVIDER + "boto3.client"),
        patch(PROVIDER + "psycopg.connect"),
        patch(PROVIDER + "update_state", return_value=False) as update,
        patch(PROVIDER + "insert_state", side_effect=UniqueViolation()) as insert,
    ):
        repository = DsqlStateRepository(
            AppSettings(dsql_host="example.dsql.ap-northeast-1.on.aws")
        )
        with pytest.raises(StateConflictError):
            repository.put("user-a", 3, snapshot)
        with pytest.raises(StateConflictError):
            repository.put("user-a", 0, snapshot)
        assert update.call_count == 1
        assert insert.call_count == 1
