"""署名検証を済ませた認証主体だけをDBの行所有者へ対応付ける。"""

import os
from dataclasses import dataclass
from typing import Annotated, Any, Literal, cast
from uuid import NAMESPACE_URL, UUID, uuid5

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.core.db import DatabaseDependency
from app.core.dependencies import bearer, get_settings
from app.core.errors import AuthenticationError, ServiceUnavailableError
from app.core.operation_queries import OperationQueries
from app.integrations.auth.cognito_provider import CognitoVerifier


@dataclass(frozen=True)
class Identity:
    """利用者の指定値からは作成しない、検証済みの要求主体。"""

    subject: str
    user_id: UUID
    role: Literal["admin", "user"]


def local_auth_enabled() -> bool:
    """固定ログインは明示した開発環境だけに限定する。"""
    settings = get_settings()
    return (
        settings.auth_mode == "local"
        and settings.environment in {"local", "test"}
        and not os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
        and len(settings.local_auth_secret) >= 32
        and len(settings.local_auth_password) >= 12
    )


def verified_identity(token: str) -> Identity:
    """署名、発行者、受信者、期限、用途を検証してロールを確定する。"""
    settings = get_settings()
    try:
        if settings.auth_mode == "local":
            if not local_auth_enabled():
                raise ServiceUnavailableError("開発用認証の設定が不正です")
            payload = cast(
                dict[str, Any],
                jwt.decode(
                    token,
                    settings.local_auth_secret,
                    algorithms=["HS256"],
                    issuer="recipeweave-local",
                    audience="recipeweave-api",
                    options={"require": ["exp", "iat", "sub", "iss", "aud", "role"]},
                ),
            )
            subject = str(payload["sub"])
            if subject not in {"local:alice", "local:bob", "local:admin"}:
                raise AuthenticationError("未登録の開発用利用者です")
            expected_role = "admin" if subject == "local:admin" else "user"
            if payload["role"] != expected_role:
                raise AuthenticationError("ロールが一致しません")
            role: Literal["admin", "user"] = "admin" if expected_role == "admin" else "user"
        else:
            verifier = CognitoVerifier(settings.cognito_issuer, settings.cognito_client_id)
            payload = verifier.claims(token)
            subject = str(payload["sub"])
            groups = payload.get("cognito:groups", [])
            role = "admin" if isinstance(groups, list) and "recipeweave-admin" in groups else "user"
    except jwt.PyJWTError as exc:
        raise AuthenticationError("アクセストークンが無効です") from exc
    return Identity(subject, uuid5(NAMESPACE_URL, "recipeweave:user:" + subject), role)


def require_identity(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    database: DatabaseDependency,
) -> Identity:
    """本人の行だけを初期化し、同一トランザクションのRLSへ主体を設定する。"""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError("ログインが必要です")
    identity = verified_identity(credentials.credentials)
    queries = OperationQueries(database, "auth/get_me")
    queries.run("q001_set_identity", user_id=str(identity.user_id), role=identity.role)
    queries.run("q002_initialize_user", user_id=identity.user_id, subject=identity.subject)
    rows = queries.run("q003_select_user", user_id=identity.user_id, subject=identity.subject)
    if not rows or rows[0]["state"] != "active":
        raise AuthenticationError("この利用者は利用を終了しています")
    queries.run(
        "q004_initialize_revision",
        row_id=uuid5(identity.user_id, "workspace"),
        user_id=identity.user_id,
    )
    return identity


IdentityDependency = Annotated[Identity, Depends(require_identity, scope="function")]
