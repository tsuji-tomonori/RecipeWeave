# generate_entity_apis.py による自動生成。直接編集しない。
from app.core.entity_service import EntityService
from app.entities.models import TaskDependencyRow, TaskDependencyWrite
from app.entities.registry import SPECIFICATIONS


def execute(service: EntityService, payload: TaskDependencyWrite) -> TaskDependencyRow:
    """献立展開後依存の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute(
        SPECIFICATIONS["entity_task_dependency_create"],
        payload=payload.model_dump(mode="python", by_alias=True),
    )
    return TaskDependencyRow.model_validate(rows[0])
