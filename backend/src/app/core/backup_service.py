"""発行済み本人バックアップを検証し、確認後だけ正規化データを原子的に全置換する。"""

import hashlib
import json
import logging
from collections import defaultdict
from datetime import UTC, datetime
from typing import Any, cast
from uuid import UUID, uuid4

from fastapi import HTTPException
from psycopg import Connection, errors
from psycopg.types.json import Jsonb
from pydantic_core import to_jsonable_python

from app.backup.inventory import DELETE_ORDER, INSERT_ORDER, OWNED, TABLES
from app.backup.models import BackupTables
from app.core.backup_contracts import (
    MAX_BACKUP_BYTES,
    BackupCount,
    BackupDocument,
    BackupPreview,
    BackupPreviewRequest,
    BackupProfile,
    BackupRestoreRequest,
)
from app.core.identity import Identity
from app.core.models import AppSnapshot
from app.core.operation_queries import OperationQueries
from app.core.workspace_service import WorkspaceService
from app.entities.json_contracts import CookingInput

logger = logging.getLogger(__name__)
Rows = dict[str, list[dict[str, Any]]]


def canonical_backup(document: BackupDocument) -> bytes:
    """日時・UUID・十進数の正規表現を型で確定し、JSON項目の記述順と空白に依存しない本文へする。"""
    return json.dumps(
        document.model_dump(mode="json", by_alias=True),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


class BackupService:
    """全SQLを固定した操作へ閉じ、管理者であっても別人の状態を置換しない。"""

    def __init__(self, connection: Connection[dict[str, Any]], identity: Identity) -> None:
        self.connection = connection
        self.identity = identity

    def queries(self, operation: str) -> OperationQueries:
        return OperationQueries(self.connection, "backup/" + operation)

    def current_revision(self, queries: OperationQueries) -> int:
        rows = queries.run("q001_lock_revision", actor_id=self.identity.user_id)
        if not rows:
            raise HTTPException(409, "本人の更新版を取得できません")
        return int(rows[0]["revision"])

    def export_tables(self, queries: OperationQueries) -> BackupTables:
        rows = queries.run("q010_export_tables", actor_id=self.identity.user_id)
        return BackupTables.model_validate(
            {key.removeprefix("rows_"): value for key, value in rows[0].items()}
        )

    def checked_digest(self, document: BackupDocument) -> str:
        if document.owner_id != self.identity.user_id:
            raise HTTPException(403, "別の利用者のバックアップは復元できません")
        encoded = canonical_backup(document)
        if len(encoded) > MAX_BACKUP_BYTES:
            raise HTTPException(413, "バックアップの上限は5,000,000バイトです")
        return hashlib.sha256(encoded).hexdigest()

    def check_proof(self, queries: OperationQueries, document: BackupDocument) -> str:
        digest = self.checked_digest(document)
        proof = queries.run(
            "q020_artifact",
            artifact_id=document.artifact_id,
            actor_id=self.identity.user_id,
            body_sha256=digest,
        )
        if not proof:
            raise HTTPException(403, "この本人へ発行したバックアップと内容が一致しません")
        return digest

    def export_backup(self) -> BackupDocument:
        """一貫した全行と表示設定を取得し、本文を保存せず発行根拠だけを記録する。"""
        queries = self.queries("export_backup")
        with self.connection.transaction():
            revision = self.current_revision(queries)
            profile = queries.run("q002_profile", actor_id=self.identity.user_id)
            document = BackupDocument(
                format="recipeweave-relational",
                formatVersion=2,
                artifactId=uuid4(),
                ownerId=self.identity.user_id,
                exportedAt=datetime.now(UTC),
                sourceVersion=revision,
                profile=BackupProfile.model_validate(profile[0]),
                tables=self.export_tables(queries),
            )
            digest = self.checked_digest(document)
            queries.run(
                "q021_issue_artifact",
                artifact_id=document.artifact_id,
                actor_id=self.identity.user_id,
                body_sha256=digest,
            )
            logger.info("backup_export_completed", extra={"format_version": 2})
            return document

    def check_references(self, queries: OperationQueries, document: BackupDocument) -> Rows:
        """他人の行、欠落した本人行、消失した共有参照を、削除前にまとめて検査する。"""
        data = cast(Rows, document.tables.model_dump(mode="python"))
        ids: dict[str, set[UUID]] = {}
        external: dict[str, set[UUID]] = defaultdict(set)
        for table, rows in data.items():
            ids[table] = {row["id"] for row in rows}
            if len(ids[table]) != len(rows):
                raise HTTPException(422, "同じテーブルに重複した行IDがあります")
            for row in rows:
                for column in ("user_id", "owner_id"):
                    if column in row and row[column] != self.identity.user_id:
                        raise HTTPException(403, "本人の業務行・私有食材だけを復元できます")

        def require_reference(target: str, value: UUID | None) -> None:
            if value is None:
                return
            if target == "app_user":
                if value != self.identity.user_id:
                    raise HTTPException(403, "本人以外のアカウントを参照できません")
            elif target in ids and value in ids[target]:
                return
            elif target in OWNED:
                raise HTTPException(422, "バックアップ内の本人データの参照が不足しています")
            else:
                external[target].add(value)

        for table, rows in data.items():
            for reference in TABLES[table]["references"]:
                for row in rows:
                    require_reference(reference["table"], row[reference["column"]])
        for session in data["cooking_session"]:
            snapshot = CookingInput.model_validate(session["input_snapshot"])
            actual_hash = hashlib.sha256(snapshot.model_dump_json().encode()).hexdigest()
            if actual_hash != session["input_hash"]:
                raise HTTPException(409, "保存された調理入力とハッシュが一致しません")
            if snapshot.menu_revision != session["menu_revision"]:
                raise HTTPException(409, "調理入力の献立版が保存した版と一致しません")
            for item in snapshot.items:
                require_reference("menu_item", item.id)
                require_reference("recipe_version", item.recipe_version_id)
            for ingredient in snapshot.ingredients:
                require_reference("recipe_ingredient", ingredient.id)
                require_reference("food_form", ingredient.form_id)
                require_reference("unit", ingredient.unit_id)
                require_reference("conversion", ingredient.conversion_id)
            for resource in snapshot.resources:
                require_reference("kitchen_resource", resource.id)
                require_reference("resource_type", resource.resource_type_id)
        for target, values in external.items():
            actual = queries.run("q300_reference_" + target, reference_ids=sorted(values))
            if {row["id"] for row in actual} != values:
                raise HTTPException(409, "必要な共有カタログがないか、参照先を利用できません")
        return data

    def replace_rows(self, queries: OperationQueries, document: BackupDocument, data: Rows) -> None:
        """依存の子から削除し、元IDと全列で親から挿入して全遅延制約を検証する。"""
        queries.run("q801_constraints_deferred")
        for table in DELETE_ORDER:
            queries.run("q100_delete_" + table, actor_id=self.identity.user_id)
        for table in INSERT_ORDER:
            for row in data[table]:
                values = dict(row)
                for column in TABLES[table]["json_columns"]:
                    if values[column] is not None:
                        values[column] = Jsonb(to_jsonable_python(values[column]))
                for column in TABLES[table]["bigint_columns"]:
                    if values[column] is not None:
                        values[column] = int(values[column])
                queries.run("q200_insert_" + table, **values)
        queries.run(
            "q802_restore_profile",
            actor_id=self.identity.user_id,
            locale=document.profile.locale,
            timezone=document.profile.timezone,
        )
        queries.run("q800_constraints_immediate")

    def preview_backup(self, request: BackupPreviewRequest) -> BackupPreview:
        """実際の置換と全DB制約検証を必ず取り消し、15分間の最終確認だけを発行する。"""
        queries = self.queries("preview_backup")
        try:
            with self.connection.transaction():
                digest = self.check_proof(queries, request.backup)
                revision = self.current_revision(queries)
                current = cast(Rows, self.export_tables(queries).model_dump(mode="python"))
                data = self.check_references(queries, request.backup)
                with self.connection.transaction(force_rollback=True):
                    self.replace_rows(queries, request.backup, data)
                intent_id = uuid4()
                issued = queries.run(
                    "q022_issue_intent",
                    intent_id=intent_id,
                    actor_id=self.identity.user_id,
                    artifact_id=request.backup.artifact_id,
                    body_sha256=digest,
                    current_revision=revision,
                )
                logger.info("backup_preview_completed", extra={"table_count": len(TABLES)})
                return BackupPreview(
                    intentId=intent_id,
                    expiresAt=issued[0]["expires_at"],
                    expectedVersion=revision,
                    backupSha256=digest,
                    sourceVersion=request.backup.source_version,
                    counts=[
                        BackupCount(
                            table=table,
                            label=TABLES[table]["label"],
                            currentCount=len(current[table]),
                            restoreCount=len(data[table]),
                        )
                        for table in TABLES
                    ],
                    replaceTargets=[
                        "冷蔵庫の在庫・レシート履歴",
                        "献立・保存した料理・過去の調理と消費履歴",
                        "自分で追加した食材・常備食材・除外条件・器具・買い物確認",
                        "言語・タイムゾーンの設定",
                    ],
                    preservedTargets=[
                        "公開レシピ・共通の食材カタログ",
                        "アカウントとログイン情報",
                        "監査記録・バックアップ発行記録",
                    ],
                )
        except errors.IntegrityError as exc:
            raise HTTPException(
                409, "参照・数量・業務制約が成立せず、現在データは変更していません"
            ) from exc
        except errors.InsufficientPrivilege as exc:
            raise HTTPException(403, "このバックアップの対象を変更する権限がありません") from exc

    def restore_backup(self, request: BackupRestoreRequest) -> AppSnapshot:
        """同じ本人・本文・確認・現行版を再検証し、全置換と単回消費を一括確定する。"""
        queries = self.queries("restore_backup")
        try:
            with self.connection.transaction():
                digest = self.check_proof(queries, request.backup)
                revision = self.current_revision(queries)
                if request.expected_version != revision:
                    raise HTTPException(
                        409, "確認後に更新されています。内容をもう一度確認してください"
                    )
                intent = queries.run(
                    "q023_lock_intent",
                    intent_id=request.intent_id,
                    actor_id=self.identity.user_id,
                    artifact_id=request.backup.artifact_id,
                    body_sha256=digest,
                    current_revision=revision,
                )
                if not intent:
                    raise HTTPException(
                        409, "確認が期限切れ・使用済みです。もう一度内容を確認してください"
                    )
                data = self.check_references(queries, request.backup)
                self.replace_rows(queries, request.backup, data)
                consumed = queries.run(
                    "q024_consume_intent",
                    intent_id=request.intent_id,
                    actor_id=self.identity.user_id,
                    body_sha256=digest,
                    current_revision=revision,
                )
                if not consumed:
                    raise HTTPException(409, "確認が有効でなくなったため復元を取り消しました")
                queries.run("q901_advance_revision", actor_id=self.identity.user_id)
                queries.run(
                    "q902_append_audit",
                    row_id=uuid4(),
                    actor_id=self.identity.user_id,
                    key_hash=hashlib.sha256(str(self.identity.user_id).encode()).hexdigest(),
                )
                event_id = uuid4()
                queries.run(
                    "q903_append_outbox",
                    event_id=event_id,
                    actor_id=self.identity.user_id,
                    version=revision + 1,
                )
                result = WorkspaceService(self.connection, self.identity).get_workspace()
                logger.info("backup_restore_completed", extra={"table_count": len(TABLES)})
                return result
        except errors.IntegrityError as exc:
            raise HTTPException(
                409, "参照・数量・業務制約が成立せず、現在データは変更していません"
            ) from exc
        except errors.InsufficientPrivilege as exc:
            raise HTTPException(403, "このバックアップの対象を変更する権限がありません") from exc
        except errors.SerializationFailure as exc:
            raise HTTPException(
                409, "同時更新がありました。内容をもう一度確認してください"
            ) from exc
