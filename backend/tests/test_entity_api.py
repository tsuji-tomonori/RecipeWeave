"""生成した全操作に対する権限、条件付き更新、列契約の要因別試験。"""

import json
from dataclasses import replace
from pathlib import Path
from typing import Any, cast
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.core.entity_contracts import OperationSpec
from app.core.entity_service import EntityService, parse_etag
from app.core.identity import Identity
from app.entities.models import MenuWrite, UnitWrite
from app.entities.registry import SPECIFICATIONS

ROOT = Path(__file__).resolve().parents[2]
ALL = list(SPECIFICATIONS.values())
ADMIN = [spec for spec in ALL if not spec.owned]
UPDATE = [spec for spec in ALL if spec.action in {"update", "delete"}]
GET = [spec for spec in ALL if spec.action == "get"]


def service(role: str = "admin") -> EntityService:
    """DB接続の呼出を観測し、認証済み本人情報を固定する。"""
    identity = Identity(subject="verified-subject", user_id=UUID(int=1), role=cast(Any, role))
    return EntityService(MagicMock(), identity)


@pytest.mark.parametrize("spec", ADMIN, ids=lambda spec: spec.operation_id)
def test_catalog_requires_admin(spec: OperationSpec) -> None:
    """Given一般利用者 Whenカタログ・運用操作 ThenDB前に403。"""
    target = service("user")
    with pytest.raises(HTTPException) as raised:
        target.execute(spec)
    assert raised.value.status_code == 403
    cast(MagicMock, target.connection).transaction.assert_not_called()


@pytest.mark.parametrize("spec", UPDATE, ids=lambda spec: spec.operation_id)
def test_mutation_requires_if_match(spec: OperationSpec) -> None:
    """Given行版ヘッダーなし When更新・削除 ThenSQL前に428。"""
    target = service()
    isolated = replace(spec, input_columns=())
    with pytest.raises(HTTPException) as raised:
        target.execute(isolated, row_id=uuid4())
    assert raised.value.status_code == 428
    cast(MagicMock, target.connection).transaction.assert_not_called()


@pytest.mark.parametrize("spec", UPDATE, ids=lambda spec: spec.operation_id)
def test_stale_update_is_conflict(spec: OperationSpec) -> None:
    """Given一致行版なし When条件付き変更 Then409と監査なし。"""
    target = service()
    query = MagicMock(return_value=[])
    isolated = replace(spec, input_columns=(), reference_queries=(), query=query)
    with pytest.raises(HTTPException) as raised:
        target.execute(isolated, row_id=uuid4(), if_match='"32"')
    assert raised.value.status_code == 409
    assert query.call_args.args[1]["expected_etag"] == "32"


@pytest.mark.parametrize("spec", GET, ids=lambda spec: spec.operation_id)
def test_missing_or_invisible_row_returns_404(spec: OperationSpec) -> None:
    """Given未登録または本人が見られない行 When取得 Then区別せず404。"""
    target = service()
    isolated = replace(spec, query=MagicMock(return_value=[]))
    with pytest.raises(HTTPException) as raised:
        target.execute(isolated, row_id=uuid4())
    assert raised.value.status_code == 404


@pytest.mark.parametrize("value", ["*", 'W/"1"', '"1", "2"', "1", '"-1"', '"abc"'])
def test_etag_rejects_ambiguous_preconditions(value: str) -> None:
    """Given曖昧な競合条件 WhenIf-Match解析 Then422。"""
    with pytest.raises(HTTPException) as raised:
        parse_etag(value)
    assert raised.value.status_code == 422


def test_cross_user_payload_is_rejected() -> None:
    """Given別人user_id When献立作成 Then参照SQLより前に403。"""
    target = service("user")
    spec = SPECIFICATIONS["entity_menu_create"]
    values = dict(user_id=str(UUID(int=2)), name="別人", servings="2")
    with pytest.raises(HTTPException) as raised:
        target.execute(spec, payload=values)
    assert raised.value.status_code == 403
    cast(MagicMock, target.connection).transaction.assert_not_called()


def test_cross_user_child_reference_is_rejected() -> None:
    """Given別人の献立ID When子明細作成 Then主SQLを実行せず403。"""
    target = service("user")
    query = MagicMock()
    reference = MagicMock(return_value=[])
    spec = replace(
        SPECIFICATIONS["entity_menu_item_create"],
        input_columns=("menu_id",),
        reference_queries=(("menu_id", reference),),
        query=query,
    )
    with pytest.raises(HTTPException) as raised:
        target.execute(spec, payload={"menu_id": uuid4()})
    assert raised.value.status_code == 403
    query.assert_not_called()
    assert reference.call_args.args[1]["actor_id"] == target.identity.user_id


def test_query_binding_keeps_hostile_text_as_value() -> None:
    """GivenSQL記号を含む名称 WhenSQL呼出 Then固定SQL本文は変化しない。"""
    from app.apis.entities.menu_create.generated.queries import SQL, execute

    connection = MagicMock()
    connection.execute.return_value.fetchall.return_value = []
    hostile = "'); DROP TABLE recipeweave.menu; --"
    execute(connection, dict(row_id=uuid4(), user_id=uuid4(), name=hostile, servings="2"))
    actual_sql, params = connection.execute.call_args.args
    assert actual_sql == SQL
    assert hostile not in actual_sql
    assert params["name"] == hostile


def test_typed_input_rejects_enum_extra_negative_quantity() -> None:
    """Given未知列・列挙外値・負人数 When入力検証 Then保存前に拒否。"""
    with pytest.raises(ValidationError):
        UnitWrite.model_validate(
            dict(
                code="g",
                name="グラム",
                dimension="unknown",
                factor="1",
                offset="0",
                status="active",
            )
        )
    with pytest.raises(ValidationError):
        MenuWrite.model_validate(dict(user_id=uuid4(), name="夕食", servings="-1"))
    with pytest.raises(ValidationError):
        MenuWrite.model_validate(dict(user_id=str(uuid4()), name="夕食", servings="2", hidden=True))


def test_all_source_tables_have_operations_and_explicit_columns() -> None:
    """Given正本71表 When操作・応答契約を照合 Then全表全列を保持。"""
    from app.entities import models

    source = json.loads((ROOT / "spec/database/source-sheet.json").read_text())["tabs"]
    table_names = {row[2] for row in source["01_テーブル一覧"][1:]}
    assert table_names <= {spec.table for spec in ALL}
    for table in table_names:
        expected = {row[2] for row in source["02_カラム辞書"][1:] if row[0] == table}
        name = "".join(word.title() for word in table.split("_")) + "Row"
        model = getattr(models, name)
        assert expected | {"etag"} <= set(model.model_fields)
        assert model.model_config["extra"] == "forbid"


def test_retention_does_not_expose_destructive_operations() -> None:
    """Given監査・公開版・派生表 WhenAPI一覧 Then無制約CRUDを公開しない。"""
    for spec in ALL:
        if spec.table in {
            "audit_event",
            "outbox_event",
            "recipe_search_document",
            "ingredient_total",
        }:
            assert spec.action in {"get", "list"}
        if spec.immutable:
            assert spec.action not in {"update", "delete"}
        if spec.action == "delete":
            assert spec.owned
