"""環境設定。保存先や認証設定の不足時は処理を拒否する。"""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", case_sensitive=False)

    state_backend: Literal["disabled", "memory", "dsql"] = "disabled"
    allow_memory_state: bool = False
    cognito_issuer: str = ""
    cognito_client_id: str = ""
    dsql_host: str = ""
    dsql_database_user: str = "recipeweave_app"
    aws_region: str = "ap-northeast-1"
    catalog_path: str = ""
    allowed_origins: str = ""
    max_request_bytes: int = Field(default=1048576, ge=1024, le=5242880)
    database_url: str = ""
    database_secret_arn: str = ""
    database_host: str = ""
    database_name: str = "recipeweave"
    database_sslmode: Literal["require"] = "require"
    auth_mode: Literal["cognito", "local"] = "cognito"
    local_auth_secret: str = ""
    local_auth_password: str = ""
    environment: Literal["local", "test", "dev", "production"] = "production"
