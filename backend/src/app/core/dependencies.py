"""プロバイダーの構築と依存のキャッシュ。必要になるまでインポートしない。"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.errors import AuthenticationError
from app.core.settings import AppSettings
from app.integrations.auth.port import IdentityVerifier

bearer = HTTPBearer(auto_error=False)


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()


@lru_cache
def get_verifier() -> IdentityVerifier:
    from app.integrations.auth.cognito_provider import CognitoVerifier

    settings = get_settings()
    return CognitoVerifier(settings.cognito_issuer, settings.cognito_client_id)


def require_subject(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> str:
    """利用者識別用のヘッダー・クエリ引数・未検証のJWTクレームを信頼しない。"""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError("access token required")
    return get_verifier().subject(credentials.credentials)


SubjectDependency = Annotated[str, Depends(require_subject)]
