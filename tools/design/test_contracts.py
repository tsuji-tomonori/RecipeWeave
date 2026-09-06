"""明示した要因別試験を実在するテスト関数へ対応づけ、成功実績と区別する。"""

import ast
import json
from pathlib import Path
from typing import Any

from .common import DesignError, read_source, table


def factor_rows(root: Path, operation: Any) -> list[list[object]]:
    path = root / "backend/tests/entity_test_contracts.json"
    if not path.exists():
        return []
    catalog = json.loads(read_source(path, root))
    entries = (
        catalog.get("cases", catalog.get("tests", [])) if isinstance(catalog, dict) else catalog
    )
    rows = []
    for entry in entries:
        ids = entry.get("operation_ids", [])
        actions = entry.get("actions", [])
        action = operation.id.rsplit("_", 1)[-1]
        if operation.id not in ids and not (
            operation.slug.startswith("entities/") and action in actions
        ):
            continue
        node = entry["test_node"]
        filename, separator, function = node.partition("::")
        if not separator or not filename.startswith("backend/tests/"):
            raise DesignError(f"テストnodeの形式が不正です: {node}")
        source = root / filename
        names = {
            item.name
            for item in ast.walk(ast.parse(read_source(source, root)))
            if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef)
        }
        if function not in names:
            raise DesignError(f"要因別試験の関数がありません: {node}")
        for key in ("factor", "given", "when", "then"):
            if not str(entry.get(key, "")).strip():
                raise DesignError(f"要因別試験の{key}が空です: {node}")
        rows.append([entry["factor"], entry["given"], entry["when"], entry["then"], node])
    return rows


def factor_section(root: Path, operation: Any) -> str:
    rows = factor_rows(root, operation)
    return (
        "## 要因別の試験仕様\n\n"
        + (
            table(["要因", "Given: 前提", "When: 操作", "Then: 期待結果", "実在テストnode"], rows)
            if rows
            else "要因別の明示対応は未登録。下の実URL試験のみを静的に確認できる。"
        )
        + "\n\nこの表は試験仕様であり、実行の成功を示さない。"
        "実行結果は品質サイトの単体・結合テストから確認する。"
    )
