"""本人による全置換の確認を、発行済みバックアップと現在版へ結び付ける。"""

from typing import Annotated, Literal
from uuid import UUID

from pydantic import AwareDatetime, ConfigDict, Field

from app.backup.models import BackupTables
from app.entities.json_contracts import ContractModel

MAX_BACKUP_BYTES = 5_000_000


class BackupProfile(ContractModel):
    locale: str = Field(min_length=1, max_length=20000)
    timezone: str = Field(min_length=1, max_length=20000)


class BackupDocument(ContractModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False, populate_by_name=True)

    format: Literal["recipeweave-relational"]
    format_version: Literal[2] = Field(alias="formatVersion")
    artifact_id: UUID = Field(alias="artifactId")
    owner_id: UUID = Field(alias="ownerId")
    exported_at: AwareDatetime = Field(alias="exportedAt")
    source_version: int = Field(alias="sourceVersion", ge=0)
    profile: BackupProfile
    tables: BackupTables


class BackupPreviewRequest(ContractModel):
    backup: BackupDocument


class BackupCount(ContractModel):
    table: str
    label: str
    current_count: int = Field(alias="currentCount", ge=0)
    restore_count: int = Field(alias="restoreCount", ge=0)

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class BackupPreview(ContractModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    intent_id: UUID = Field(alias="intentId")
    expires_at: AwareDatetime = Field(alias="expiresAt")
    expected_version: int = Field(alias="expectedVersion", ge=0)
    backup_sha256: str = Field(alias="backupSha256", pattern=r"^[0-9a-f]{64}$")
    source_version: int = Field(alias="sourceVersion", ge=0)
    counts: list[BackupCount]
    replace_targets: list[str] = Field(alias="replaceTargets")
    preserved_targets: list[str] = Field(alias="preservedTargets")


class BackupRestoreRequest(BackupPreviewRequest):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    intent_id: UUID = Field(alias="intentId")
    expected_version: int = Field(alias="expectedVersion", ge=0)
    confirmed: Annotated[Literal[True], Field(description="全置換の最終確認を明示した場合だけtrue")]
