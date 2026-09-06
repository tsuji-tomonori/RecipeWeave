"""開発用の下書き許可を認証方式から分離し、本番では常に無効にする。"""

import pytest

from app.core.catalog_preview import catalog_preview_enabled
from app.core.dependencies import get_settings
from app.core.identity import local_auth_enabled


@pytest.mark.parametrize(
    ("environment", "allowed", "expected"),
    [
        ("dev", True, True),
        ("dev", False, False),
        ("local", True, True),
        ("test", True, True),
        ("production", True, False),
        ("production", False, False),
    ],
)
def test_explicit_preview_setting_never_opens_production(
    monkeypatch: pytest.MonkeyPatch, environment: str, allowed: bool, expected: bool
) -> None:
    monkeypatch.setenv("AUTH_MODE", "cognito")
    monkeypatch.setenv("ENVIRONMENT", environment)
    monkeypatch.setenv("ALLOW_CATALOG_PREVIEW", str(allowed).lower())
    monkeypatch.setenv("AWS_LAMBDA_FUNCTION_NAME", "recipeweave-dev")
    get_settings.cache_clear()
    try:
        assert local_auth_enabled() is False
        assert catalog_preview_enabled() is expected
    finally:
        get_settings.cache_clear()


def test_existing_local_development_preview_is_preserved(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AUTH_MODE", "local")
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("ALLOW_CATALOG_PREVIEW", "false")
    monkeypatch.setenv("LOCAL_AUTH_SECRET", "local-boundary-test-secret-of-over-32-characters")
    monkeypatch.setenv("LOCAL_AUTH_PASSWORD", "local-boundary-test-password")
    monkeypatch.delenv("AWS_LAMBDA_FUNCTION_NAME", raising=False)
    get_settings.cache_clear()
    try:
        assert local_auth_enabled() is True
        assert catalog_preview_enabled() is True
    finally:
        get_settings.cache_clear()
