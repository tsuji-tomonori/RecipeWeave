"""生成した全操作に対する権限、条件付き更新、列契約の要因別試験。"""

import json
import secrets
import time
from dataclasses import replace
from pathlib import Path
from typing import Any, cast
from unittest.mock import MagicMock
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

import jwt
import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.core.dependencies import get_settings
from app.core.entity_contracts import OperationSpec
from app.core.entity_service import EntityService, parse_etag
from app.core.errors import AuthenticationError
from app.core.identity import Identity, verified_identity
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


@pytest.mark.parametrize("role", ["user", "admin"])
def test_cross_user_payload_is_rejected(role: str) -> None:
    """Given別人user_id When献立作成 Then参照SQLより前に403。"""
    target = service(role)
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


def test_server_owned_columns_are_not_editable() -> None:
    """Given所有者・認証主体・献立版 When入力契約を検査 Then外部指定を許さない。"""
    from app.entities.models import AppUserWrite, CatalogReleaseWrite, FoodWrite

    for model in (CatalogReleaseWrite, FoodWrite):
        assert "owner_id" not in model.model_fields
    assert not {"auth_subject", "state"} & AppUserWrite.model_fields.keys()
    assert "revision" not in MenuWrite.model_fields
    with pytest.raises(ValidationError):
        CatalogReleaseWrite.model_validate(
            dict(version="private-test", manifest_hash="0" * 64, owner_id=uuid4())
        )


def test_signed_token_cannot_supply_database_owner_or_escalate_role(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Given署名済みの余剰user_idと偽装ロール When主体確定 Thensubだけから本人を導出。"""
    secret = secrets.token_urlsafe(32)
    monkeypatch.setenv("AUTH_MODE", "local")
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("LOCAL_AUTH_SECRET", secret)
    monkeypatch.setenv("LOCAL_AUTH_PASSWORD", "test-only-local-password")
    monkeypatch.delenv("AWS_LAMBDA_FUNCTION_NAME", raising=False)
    get_settings.cache_clear()
    now = int(time.time())
    payload = dict(
        sub="local:alice",
        user_id=str(UUID(int=2)),
        role="user",
        iss="recipeweave-local",
        aud="recipeweave-api",
        iat=now,
        exp=now + 300,
    )
    try:
        identity = verified_identity(jwt.encode(payload, secret, algorithm="HS256"))
        assert identity.user_id == uuid5(NAMESPACE_URL, "recipeweave:user:local:alice")
        assert identity.role == "user"
        with pytest.raises(AuthenticationError):
            verified_identity(jwt.encode({**payload, "role": "admin"}, secret, algorithm="HS256"))
    finally:
        get_settings.cache_clear()


@pytest.mark.parametrize(
    "operation_id",
    ["entity_menu_item_create", "entity_menu_item_update", "entity_user_recipe_event_create"],
)
def test_recipe_history_reference_is_verified_before_write(
    operation_id: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Given未公開版への参照権なし When履歴を書込 Then新規履歴で認可を作れない。"""
    monkeypatch.setattr("app.core.entity_service.local_auth_enabled", lambda: False)
    target = service("user")
    reference = MagicMock(return_value=[])
    query = MagicMock()
    original = SPECIFICATIONS[operation_id]
    assert "recipe_version_id" in dict(original.reference_queries)
    isolated = replace(
        original,
        input_columns=("recipe_version_id",),
        reference_queries=(("recipe_version_id", reference),),
        query=query,
    )
    with pytest.raises(HTTPException) as raised:
        target.execute(isolated, payload={"recipe_version_id": uuid4()}, if_match='"1"')
    assert raised.value.status_code == 403
    query.assert_not_called()
    assert reference.call_args.args[1]["actor_id"] == target.identity.user_id
    assert reference.call_args.args[1]["preview"] is False


@pytest.mark.parametrize(
    "groups",
    [
        [[1, 1]],
        [[2, 1]],
        [[1], [1]],
        [[3]],
        [[1, 2]],
        [[1, 2, 3, 4]],
    ],
)
def test_template_rejects_unsupported_or_duplicate_groups(groups: list[list[int]]) -> None:
    """Given重複・未許可ID・要素数違い When生成契約を検証 Then候補件数の水増しを拒否。"""
    from app.entities.json_contracts import GenerationTemplateContract

    with pytest.raises(ValidationError):
        GenerationTemplateContract.model_validate(
            dict(
                primary_identity_ids=[UUID(int=10)],
                support_identity_ids=[UUID(int=1), UUID(int=2)],
                support_k=[1],
                support_identity_sets=[[UUID(int=item) for item in group] for group in groups],
                flavor_codes=["soy"],
                route_codes=["stir_fry"],
                normalizer_version="v2",
            )
        )
