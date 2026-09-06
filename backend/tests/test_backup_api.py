"""バックアップの厳密な形式・数量・所有者とSQL生成境界を検査する。"""

import hashlib
import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, cast
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.backup.inventory import TABLES
from app.backup.models import SessionTaskBackupRow, UserPreferenceBackupRow
from app.core.backup_contracts import BackupDocument, BackupRestoreRequest
from app.core.backup_service import BackupService, canonical_backup
from app.core.identity import Identity
from app.tools.generate import read_query


def empty_document(owner: UUID | None = None) -> BackupDocument:
    """全表を空として明示した最小の正規化バックアップを作る。"""
    return BackupDocument.model_validate(
        {
            "format": "recipeweave-relational",
            "formatVersion": 2,
            "artifactId": str(uuid4()),
            "ownerId": str(owner or UUID(int=1)),
            "exportedAt": datetime.now(UTC).isoformat(),
            "sourceVersion": 0,
            "profile": {"locale": "ja", "timezone": "Asia/Tokyo"},
            "tables": {name: [] for name in TABLES},
        }
    )


def test_backup_requires_complete_table_set_and_current_format() -> None:
    """Given旧形式・欠落表・監査混入 When形式検証 Then保存や削除より前に拒否。"""
    with pytest.raises(ValidationError):
        BackupDocument.model_validate({"version": 1, "lots": []})
    payload = empty_document().model_dump(mode="json", by_alias=True)
    payload["tables"].pop("pantry_consumption")
    with pytest.raises(ValidationError):
        BackupDocument.model_validate(payload)
    payload = empty_document().model_dump(mode="json", by_alias=True)
    payload["tables"]["audit_event"] = []
    with pytest.raises(ValidationError):
        BackupDocument.model_validate(payload)
    assert "ingredient_total" in TABLES
    assert {"duration_source", "confirmed_duration_s"} <= SessionTaskBackupRow.model_fields.keys()
    assert (
        not {"app_user", "workspace_revision", "backup_artifact", "backup_restore_intent"}
        & TABLES.keys()
    )


def test_decimal_precision_survives_canonical_backup_round_trip() -> None:
    """Givennumeric上限付近の小数 WhenJSONで往復 Then浮動小数点に丸めない。"""
    document = empty_document()
    amount = Decimal("12345678901234.123456")
    document.tables.user_preference.append(
        UserPreferenceBackupRow(
            id=uuid4(),
            created_at=datetime.now(UTC),
            user_id=document.owner_id,
            option_id=uuid4(),
            weight=amount,
        )
    )
    encoded = canonical_backup(document)
    assert b'"12345678901234.123456"' in encoded
    recovered = BackupDocument.model_validate_json(encoded)
    assert recovered.tables.user_preference[0].weight == amount
    assert hashlib.sha256(canonical_backup(recovered)).digest() == hashlib.sha256(encoded).digest()


def test_export_proof_and_owner_are_required_even_for_admin() -> None:
    """Given別人・未発行本文 When復元の根拠確認 Then管理者でも403。"""
    service = BackupService(MagicMock(), Identity("subject", UUID(int=1), "admin"))
    with pytest.raises(HTTPException) as owner_error:
        service.checked_digest(empty_document(UUID(int=2)))
    assert owner_error.value.status_code == 403
    query = MagicMock()
    query.run.return_value = []
    with pytest.raises(HTTPException) as proof_error:
        service.check_proof(query, empty_document())
    assert proof_error.value.status_code == 403


def test_restore_requires_explicit_confirmation_and_revision() -> None:
    """Given確認キャンセルまたは現在版なし When全置換要求 Then422。"""
    payload = dict(
        backup=empty_document().model_dump(mode="json", by_alias=True),
        intentId=str(uuid4()),
        expectedVersion=0,
        confirmed=False,
    )
    with pytest.raises(ValidationError):
        BackupRestoreRequest.model_validate(payload)
    payload.pop("expectedVersion")
    payload["confirmed"] = True
    with pytest.raises(ValidationError):
        BackupRestoreRequest.model_validate(payload)


@pytest.mark.parametrize("mode", ["IMMEDIATE", "DEFERRED"])
def test_constraint_mode_sql_has_explicit_single_statement_contract(
    tmp_path: Path, mode: str
) -> None:
    """Given制約検証タイミング WhenSQL解析 Then固定2文だけを許可する。"""
    path = tmp_path / "constraints.sql"
    text = "-- 復元の制約を検証する。\nSET CONSTRAINTS ALL " + mode + ";\n"
    path.write_text(text)
    assert read_query(path) == text
    path.write_text("-- 個別指定は未対応。\nSET CONSTRAINTS private_constraint IMMEDIATE;\n")
    with pytest.raises(ValueError):
        read_query(path)
    path.write_text(text + "SELECT 1;\n")
    with pytest.raises(ValueError):
        read_query(path)


def test_backup_column_sets_match_current_physical_schema() -> None:
    """Given元ID・作成日時・追加列 When全列照合 Then復元時に落とす業務列がない。"""
    root = Path(__file__).resolve().parents[2]
    source = json.loads((root / "database/schema_catalog.json").read_text())
    actual = {table["name"]: table for table in cast(list[dict[str, Any]], source["tables"])}
    for name, metadata in TABLES.items():
        assert set(metadata["columns"]) == {column["name"] for column in actual[name]["columns"]}
