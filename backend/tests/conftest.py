"""個人状態のテストは実際のRSA署名を検証し、検証を省略するテスト用認証経路を作らない。"""

import time
from collections.abc import Iterator
from typing import Protocol, cast

import httpx
import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from app.core import dependencies
from app.integrations.auth.cognito_provider import CognitoVerifier
from app.main import create_app

ISSUER = "https://cognito-idp.ap-northeast-1.amazonaws.com/ap-northeast-1_TEST"
CLIENT_ID = "test-client"


class FixedKeys:
    def __init__(self, public_key: rsa.RSAPublicKey) -> None:
        self.public_key = public_key

    def key_for(self, token: str) -> rsa.RSAPublicKey:
        return self.public_key


@pytest.fixture(scope="session")
def private_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def access_token(
    private_key: rsa.RSAPrivateKey,
    subject: str = "user-a",
    overrides: dict[str, object] | None = None,
) -> str:
    claims: dict[str, object] = {
        "iss": ISSUER,
        "client_id": CLIENT_ID,
        "sub": subject,
        "token_use": "access",
        "exp": int(time.time()) + 300,
        "iat": int(time.time()) - 1,
    }
    claims.update(overrides or {})
    return jwt.encode(claims, private_key, algorithm="RS256", headers={"kid": "test"})


@pytest.fixture
def verifier(private_key: rsa.RSAPrivateKey) -> CognitoVerifier:
    return CognitoVerifier(ISSUER, CLIENT_ID, FixedKeys(private_key.public_key()))


class HttpTestClient(Protocol):
    """Starletteのhttpx/httpx2移行に対応する、小さなHTTPクライアント境界。"""

    def get(
        self,
        url: str,
        *,
        params: dict[str, str | list[str]] | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response: ...

    def post(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        json: object = None,
    ) -> httpx.Response: ...

    def delete(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response: ...

    def put(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        json: object = None,
        content: bytes | None = None,
    ) -> httpx.Response: ...


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch, verifier: CognitoVerifier) -> Iterator[HttpTestClient]:
    """署名検証は専用試験で確認し、このfixtureではHTTP入力境界を分離する。"""
    from unittest.mock import MagicMock

    from app.core.db import get_database

    monkeypatch.setattr(dependencies, "get_verifier", lambda: verifier)
    app = create_app()
    app.dependency_overrides[get_database] = MagicMock
    with TestClient(app) as test_client:
        yield cast(HttpTestClient, test_client)
