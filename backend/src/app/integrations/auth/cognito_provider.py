"""Cognito access token verification independent of API Gateway authorizers."""

import re
from typing import Protocol, cast

import jwt
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from jwt import PyJWKClient

from app.core.errors import AuthenticationError, ServiceUnavailableError


class SigningKeys(Protocol):
    def key_for(self, token: str) -> RSAPublicKey: ...


class CognitoSigningKeys:
    def __init__(self, issuer: str) -> None:
        self._client = PyJWKClient(
            issuer + "/.well-known/jwks.json", cache_jwk_set=True, lifespan=300, timeout=5
        )

    def key_for(self, token: str) -> RSAPublicKey:
        key = self._client.get_signing_key_from_jwt(token).key
        if not isinstance(key, RSAPublicKey):
            raise AuthenticationError("invalid signing key type")
        return key


class CognitoVerifier:
    def __init__(self, issuer: str, client_id: str, keys: SigningKeys | None = None) -> None:
        if (
            not re.fullmatch(
                r"https://cognito-idp\.[a-z0-9-]+\.amazonaws\.com(?:\.cn)?/[A-Za-z0-9_-]+",
                issuer,
            )
            or not client_id
        ):
            raise ServiceUnavailableError("authentication configuration missing or invalid")
        self._issuer = issuer
        self._client_id = client_id
        self._keys = keys if keys is not None else CognitoSigningKeys(issuer)

    def subject(self, token: str) -> str:
        """Verify signature, issuer, expiry, access use and app client before sub."""
        try:
            header = jwt.get_unverified_header(token)
            if header.get("alg") != "RS256" or not isinstance(header.get("kid"), str):
                raise AuthenticationError("invalid token header")
            payload = cast(
                dict[str, object],
                jwt.decode(
                    token,
                    self._keys.key_for(token),
                    algorithms=["RS256"],
                    issuer=self._issuer,
                    options={
                        "require": ["exp", "iat", "iss", "sub", "token_use", "client_id"],
                        "verify_aud": False,
                    },
                ),
            )
        except jwt.PyJWKClientConnectionError as exc:
            raise ServiceUnavailableError("verification keys temporarily unavailable") from exc
        except jwt.PyJWTError as exc:
            raise AuthenticationError("invalid access token") from exc
        subject = payload.get("sub")
        if (
            payload.get("token_use") != "access"
            or payload.get("client_id") != self._client_id
            or not isinstance(subject, str)
            or not 1 <= len(subject) <= 128
        ):
            raise AuthenticationError("invalid access token claims")
        return subject
