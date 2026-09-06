"""Lambda実行時にだけDB資格情報を解決し、値をログへ出さない。"""

import json
from collections.abc import Callable
from functools import lru_cache
from typing import Protocol, TypedDict, cast

import boto3
from botocore.config import Config

from app.core.settings import AppSettings


class ConnectionOptions(TypedDict):
    host: str
    dbname: str
    user: str
    password: str
    sslmode: str


class SecretClient(Protocol):
    def get_secret_value(self, *, SecretId: str) -> dict[str, object]: ...


@lru_cache(maxsize=4)
def client(region: str) -> SecretClient:
    """短いタイムアウトのSDKクライアントだけを共有し、secretは都度解決する。"""
    factory: Callable[..., SecretClient] = getattr(boto3, "client")  # noqa: B009 -- 動的SDKの型境界
    return factory(
        "secretsmanager",
        region_name=region,
        config=Config(
            connect_timeout=3,
            read_timeout=5,
            retries={"mode": "standard", "total_max_attempts": 2},
        ),
    )


def read_credentials(secret_arn: str, region: str) -> tuple[str, str]:
    """本番ランタイムのIAM権限内で解決する。応答や例外に資格情報を含めない。"""
    if not secret_arn.startswith("arn:") or ":secretsmanager:" not in secret_arn:
        raise ValueError("DB secretのARNが不正です")
    response = client(region).get_secret_value(SecretId=secret_arn)
    payload = response.get("SecretString")
    if not isinstance(payload, str):
        raise ValueError("DB資格情報の形式が不正です")
    parsed: object = json.loads(payload)
    if not isinstance(parsed, dict):
        raise ValueError("DB資格情報の形式が不正です")
    values = cast(dict[str, object], parsed)
    username, password = values.get("username"), values.get("password")
    if (
        not isinstance(username, str)
        or not username
        or not isinstance(password, str)
        or not password
    ):
        raise ValueError("DB資格情報の必須項目が不足しています")
    return username, password


def connection_kwargs(settings: AppSettings) -> ConnectionOptions:
    """アプリ用secretとTLS必須の接続属性を返す。DSNへの文字列連結は行わない。"""
    if not settings.database_host or not settings.database_secret_arn:
        raise ValueError("AWSデータベースの接続設定が不足しています")
    if settings.database_sslmode != "require":
        raise ValueError("AWSデータベースではTLSが必須です")
    username, password = read_credentials(settings.database_secret_arn, settings.aws_region)
    return {
        "host": settings.database_host,
        "dbname": settings.database_name,
        "user": username,
        "password": password,
        "sslmode": settings.database_sslmode,
    }
