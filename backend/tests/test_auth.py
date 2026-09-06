import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from app.core.errors import AuthenticationError, ServiceUnavailableError
from app.integrations.auth.cognito_provider import CognitoVerifier

from .conftest import CLIENT_ID, ISSUER, FixedKeys, access_token


def test_valid_cognito_access_token(
    private_key: rsa.RSAPrivateKey, verifier: CognitoVerifier
) -> None:
    assert verifier.subject(access_token(private_key)) == "user-a"


@pytest.mark.parametrize(
    "overrides",
    [
        {"exp": int(time.time()) - 300},
        {"client_id": "attacker"},
        {"token_use": "id"},
        {"iss": "https://attacker.invalid"},
        {"sub": ""},
        {"sub": "x" * 129},
        {"iat": int(time.time()) + 3600},
    ],
)
def test_rejects_invalid_claims(
    private_key: rsa.RSAPrivateKey, verifier: CognitoVerifier, overrides: dict[str, object]
) -> None:
    with pytest.raises(AuthenticationError):
        verifier.subject(access_token(private_key, overrides=overrides))


def test_rejects_wrong_signature(verifier: CognitoVerifier) -> None:
    wrong_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with pytest.raises(AuthenticationError):
        verifier.subject(access_token(wrong_key))


def test_rejects_hmac_algorithm(verifier: CognitoVerifier) -> None:
    token = jwt.encode(
        {"sub": "user-a"},
        "test-only-key-long-enough-for-hs256",
        algorithm="HS256",
        headers={"kid": "test"},
    )
    with pytest.raises(AuthenticationError):
        verifier.subject(token)


def test_missing_auth_configuration_fails_closed(private_key: rsa.RSAPrivateKey) -> None:
    with pytest.raises(ServiceUnavailableError):
        CognitoVerifier("", CLIENT_ID, FixedKeys(private_key.public_key()))
    with pytest.raises(ServiceUnavailableError):
        CognitoVerifier(ISSUER, "", FixedKeys(private_key.public_key()))
