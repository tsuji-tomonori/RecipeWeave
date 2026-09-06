"""開発専用ログインと、検証済み利用者の公開プロフィール。"""

import secrets
from datetime import UTC, datetime, timedelta
from uuid import NAMESPACE_URL, uuid5

import jwt
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field

from app.core.dependencies import get_settings
from app.core.identity import Identity, local_auth_enabled


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=200)


class UserProfile(BaseModel):
    id: str
    display_name: str
    role: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
    user: UserProfile


def profile(identity: Identity) -> UserProfile:
    """トークン本文やDB内部設定を返さず、画面表示用の主体を返す。"""
    name = identity.subject.removeprefix("local:") if local_auth_enabled() else "利用者"
    return UserProfile(id=str(identity.user_id), display_name=name, role=identity.role)


def local_login(request: LoginRequest) -> LoginResponse:
    """本番とAWSでは常に無効な開発ログインを実行する。"""
    if not local_auth_enabled():
        raise HTTPException(404, "このログイン方法は利用できません")
    settings = get_settings()
    valid_password = secrets.compare_digest(request.password, settings.local_auth_password)
    if request.username not in {"alice", "bob", "admin"} or not valid_password:
        raise HTTPException(401, "利用者名またはパスワードが違います")
    subject = "local:" + request.username
    role = "admin" if request.username == "admin" else "user"
    now = datetime.now(UTC)
    token = jwt.encode(
        {
            "sub": subject,
            "role": role,
            "iat": now,
            "exp": now + timedelta(hours=1),
            "iss": "recipeweave-local",
            "aud": "recipeweave-api",
        },
        settings.local_auth_secret,
        algorithm="HS256",
    )
    return LoginResponse(
        access_token=token,
        user=UserProfile(
            id=str(uuid5(NAMESPACE_URL, "recipeweave:user:" + subject)),
            display_name=request.username,
            role=role,
        ),
    )
