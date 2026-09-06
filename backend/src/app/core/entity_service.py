"""正規化テーブルの認可、競合制御、監査を同じトランザクションで扱う。"""

import hashlib
import json
import logging
import re
from collections.abc import Mapping
from typing import Any
from uuid import UUID, uuid4

from fastapi import HTTPException
from psycopg import Connection, errors
from psycopg.types.json import Jsonb
from pydantic_core import to_jsonable_python

from app.core.catalog_preview import catalog_preview_enabled
from app.core.entity_contracts import OperationSpec, Row
from app.core.identity import Identity

logger = logging.getLogger(__name__)


def parse_etag(value: str | None) -> str:
    """ワイルドカードや複数指定を拒否し、読取り時の行版を必須にする。"""
    if value is None:
        raise HTTPException(status_code=428, detail="If-Matchが必要です")
    if re.fullmatch(r'"[0-9]+"', value) is None:
        raise HTTPException(status_code=422, detail="If-Matchの形式が不正です")
    return value[1:-1]


class EntityService:
    """検証済み認証情報と固定SQLだけを受け付ける操作サービス。"""

    def __init__(self, connection: Connection[Row], identity: Identity) -> None:
        self.connection = connection
        self.identity = identity

    def execute(
        self,
        spec: OperationSpec,
        payload: Mapping[str, Any] | None = None,
        row_id: UUID | None = None,
        if_match: str | None = None,
        limit: int = 50,
        after: UUID | None = None,
    ) -> list[Row]:
        """本人の行を絞り込み、更新前の版と親所有権を検証して実行する。"""
        if not spec.owned and self.identity.role != "admin":
            logger.warning("entity_operation_rejected", extra={"operation_id": spec.operation_id})
            raise HTTPException(status_code=403, detail="管理者権限が必要です")
        if not 1 <= limit <= 100:
            raise HTTPException(status_code=422, detail="取得件数は1から100です")
        values = dict(payload or {})
        if set(values) != set(spec.input_columns):
            raise HTTPException(status_code=422, detail="入力項目が操作契約と一致しません")
        if (
            spec.table == "app_user"
            and values.get("auth_subject", self.identity.subject) != self.identity.subject
        ):
            raise HTTPException(status_code=403, detail="認証主体は変更できません")
        if "user_id" in values and str(values["user_id"]) != str(self.identity.user_id):
            raise HTTPException(status_code=403, detail="別の利用者を指定できません")
        params: dict[str, Any] = {
            **values,
            "row_id": row_id or uuid4(),
            "actor_id": self.identity.user_id,
            "page_limit": limit,
            "after_id": after,
        }
        if spec.action in {"update", "delete"}:
            params["expected_etag"] = parse_etag(if_match)
        for column in spec.json_columns:
            if column in params and params[column] is not None:
                params[column] = Jsonb(to_jsonable_python(params[column]))
        for column in spec.bigint_columns:
            if column in params and params[column] is not None:
                params[column] = int(params[column])
        try:
            with self.connection.transaction():
                for column, query in spec.reference_queries:
                    value = values.get(column)
                    if value is not None and not query(
                        self.connection,
                        {
                            "reference_id": value,
                            "actor_id": self.identity.user_id,
                            "preview": catalog_preview_enabled(),
                        },
                    ):
                        raise HTTPException(status_code=403, detail="参照先を利用できません")
                rows = spec.query(self.connection, params)
                if not rows and spec.action in {"get", "update", "delete"}:
                    status = 404 if spec.action == "get" else 409
                    raise HTTPException(
                        status_code=status, detail="対象がないか行の版が変わりました"
                    )
                for row in rows:
                    if spec.table == "recipe_embedding" and isinstance(row.get("embedding"), str):
                        row["embedding"] = json.loads(row["embedding"])
                    for column in spec.bigint_columns:
                        if row.get(column) is not None:
                            row[column] = str(row[column])
                if spec.action in {"create", "update", "delete"}:
                    self.record_change(spec, params["row_id"])
                logger.info(
                    "entity_operation_completed",
                    extra={
                        "operation_id": spec.operation_id,
                        "table": spec.table,
                        "action": spec.action,
                        "row_count": len(rows),
                    },
                )
                return rows
        except errors.IntegrityError as exc:
            logger.warning(
                "entity_operation_rejected",
                extra={"operation_id": spec.operation_id, "sqlstate": exc.sqlstate},
            )
            raise HTTPException(
                status_code=409, detail="参照・一意性・業務制約により保存できません"
            ) from exc
        except errors.InsufficientPrivilege as exc:
            raise HTTPException(status_code=403, detail="操作権限がありません") from exc
        except errors.SerializationFailure as exc:
            raise HTTPException(
                status_code=409, detail="同時更新がありました。再取得してください"
            ) from exc

    def record_change(self, spec: OperationSpec, row_id: UUID) -> None:
        """本文を複製せず、行キーのハッシュと操作種別だけを監査へ残す。"""
        from app.entities.audit_queries import append_audit, append_outbox
        from app.entities.workspace_query import increment_workspace

        key_hash = hashlib.sha256(str(row_id).encode()).hexdigest()
        append_audit(
            self.connection,
            {
                "row_id": uuid4(),
                "actor_id": self.identity.user_id,
                "action": spec.action,
                "entity_type": spec.table,
                "entity_key_hash": key_hash,
            },
        )
        if spec.owned:
            increment_workspace(
                self.connection, {"row_id": uuid4(), "actor_id": self.identity.user_id}
            )
        else:
            append_outbox(
                self.connection,
                {
                    "row_id": uuid4(),
                    "event_type": f"{spec.table}.{spec.action}",
                    "aggregate_id": row_id,
                },
            )
