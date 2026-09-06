"""旧スナップショット境界を廃止し、正規化DBの失敗時保護へ回帰条件を移す。"""

from collections.abc import Generator
from typing import Any, cast
from unittest.mock import MagicMock, patch
from uuid import UUID

import pytest
from fastapi import HTTPException
from psycopg.errors import SerializationFailure

from app.core import db
from app.core.entity_service import EntityService
from app.core.errors import ServiceUnavailableError
from app.core.identity import Identity
from app.core.settings import AppSettings
from app.entities.registry import SPECIFICATIONS
from app.main import create_app

from .conftest import HttpTestClient


def test_legacy_snapshot_routes_are_absent() -> None:
    """旧状態JSONの全量上書きAPIを公開せず、テーブル単位のAPIへ置き換える。"""
    assert "/api/state" not in create_app().openapi()["paths"]


def test_database_configuration_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    """DB設定不足時にメモリーやサンプルJSONへ黙ってフォールバックしない。"""
    monkeypatch.setattr(db, "get_settings", lambda: AppSettings(database_url=""))
    with pytest.raises(ServiceUnavailableError):
        next(db.get_database())


def test_database_failure_rolls_back_outer_transaction(monkeypatch: pytest.MonkeyPatch) -> None:
    """要求処理の失敗を接続contextへ渡し、途中までのDB変更を確定しない。"""
    monkeypatch.setattr(db, "get_settings", lambda: AppSettings(database_url="postgresql://test"))
    with patch("app.core.db.psycopg.Connection.connect") as connect:
        generator = cast(Generator[Any, None, None], db.get_database())
        next(generator)
        with pytest.raises(ValueError, match="business failure"):
            generator.throw(ValueError("business failure"))
        assert connect.return_value.__exit__.call_args.args[0] is ValueError
        assert connect.call_args.kwargs["connect_timeout"] == 5


def test_serialization_failure_is_reported_without_overwriting() -> None:
    """同時変更の再試行で別の更新を上書きせず、呼出側へ再取得を求める。"""
    from dataclasses import replace

    query = MagicMock(side_effect=SerializationFailure())
    spec = replace(
        SPECIFICATIONS["entity_menu_update"], input_columns=(), reference_queries=(), query=query
    )
    target = EntityService(MagicMock(), Identity("verified", UUID(int=1), "user"))
    with pytest.raises(HTTPException) as raised:
        target.execute(spec, row_id=UUID(int=2), if_match='"42"')
    assert raised.value.status_code == 409
    query.assert_called_once()


def test_body_limit_precedes_validation(client: HttpTestClient) -> None:
    """過大本文はJSON解析やDB操作より先に拒否する。"""
    response = client.put(
        "/api/entities/menu/00000000-0000-0000-0000-000000000001", content=b"x" * (1048576 + 1)
    )
    assert response.status_code == 413
