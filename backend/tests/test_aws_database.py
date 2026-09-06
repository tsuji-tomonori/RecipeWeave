"""実資格情報を使わず、AWS接続設定の検証とsecret境界を確認する。"""

import json
import secrets

import pytest

from app.core.settings import AppSettings
from app.integrations.database import aws_provider


class FixedSecret:
    """AWSへ接続しない単体試験用のSDK応答。"""

    def __init__(self, value: object) -> None:
        self.value = value

    def get_secret_value(self, *, SecretId: str) -> dict[str, object]:
        assert SecretId == "arn:aws:secretsmanager:ap-northeast-1:111122223333:secret:unit-only"
        return {"SecretString": json.dumps(self.value)}


def test_tls_and_connection_attributes_use_runtime_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """前提:専用secretがある / 操作:接続属性を作る / 期待:TLSと個別属性を保持する。"""
    generated_password = secrets.token_urlsafe(32) + "://@"
    fake = FixedSecret({"username": "recipeweave_app", "password": generated_password})

    def fake_client(region: str) -> FixedSecret:
        return fake

    monkeypatch.setattr(aws_provider, "client", fake_client)
    arn = "arn:aws:secretsmanager:ap-northeast-1:111122223333:secret:unit-only"
    settings = AppSettings(
        database_host="unit-only.invalid",
        database_secret_arn=arn,
    )
    result = aws_provider.connection_kwargs(settings)
    assert result["sslmode"] == "require"
    assert result["user"] == "recipeweave_app"
    assert result["password"] == generated_password
    assert result["host"] == "unit-only.invalid"


@pytest.mark.parametrize("value", [None, [], {"username": "app"}, {"password": "value"}])
def test_malformed_secret_is_rejected_without_echoing_value(
    value: object, monkeypatch: pytest.MonkeyPatch
) -> None:
    """前提:必須項目が欠ける / 操作:secretを解釈 / 期待:資格情報を含まない例外。"""

    def fake_client(region: str) -> FixedSecret:
        return FixedSecret(value)

    monkeypatch.setattr(aws_provider, "client", fake_client)
    with pytest.raises(ValueError, match="DB資格情報"):
        aws_provider.read_credentials(
            "arn:aws:secretsmanager:ap-northeast-1:111122223333:secret:unit-only", "ap-northeast-1"
        )


def test_missing_aws_settings_do_not_attempt_credential_fetch() -> None:
    """前提:AWS接続設定なし / 操作:接続属性取得 / 期待:SDK呼出し前に拒否する。"""
    with pytest.raises(ValueError, match="接続設定"):
        aws_provider.connection_kwargs(AppSettings())
