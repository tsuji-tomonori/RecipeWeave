"""操作ごとの配置、プロバイダー境界、ルートと契約の整合性を検査する。"""

import ast
import importlib
from pathlib import Path
from typing import cast

from app.core.contracts import OperationContract
from app.main import create_app

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {"router.py", "functions.py", "schemas.py", "samples.py", "contract.py"}
PROVIDERS = {"boto3", "botocore", "psycopg", "jwt", "httpx"}


def inspect_operations(root: Path = ROOT) -> list[str]:
    """採用したディレクトリ構成と、外部接続をプロバイダーへ限定する境界を検査する。"""
    errors: list[str] = []
    operation_ids: set[str] = set()
    openapi = create_app().openapi()
    for contract_path in sorted((root / "apis").rglob("contract.py")):
        directory = contract_path.parent
        missing = REQUIRED - {path.name for path in directory.iterdir()}
        errors.extend(f"{directory}: missing {name}" for name in sorted(missing))
        module_name = ".".join(contract_path.relative_to(root.parent).with_suffix("").parts)
        contract = cast(OperationContract, importlib.import_module(module_name).CONTRACT)
        if contract.operation_id in operation_ids:
            errors.append(f"duplicate operation id {contract.operation_id}")
        operation_ids.add(contract.operation_id)
        operation = openapi["paths"].get(contract.path, {}).get(contract.method.lower())
        if operation is None or operation["operationId"] != contract.operation_id:
            errors.append(f"route/contract mismatch {contract.operation_id}")
        elif not set(map(str, contract.errors)) <= set(operation["responses"]):
            errors.append(f"undeclared runtime error responses {contract.operation_id}")
        if contract.slug != "/".join(directory.relative_to(root / "apis").parts):
            errors.append(f"slug/path mismatch {contract.operation_id}")
        for filename in ("router.py", "functions.py"):
            path = directory / filename
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                names: list[str] = []
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module]
                for name in names:
                    if (
                        name.split(".")[0] in PROVIDERS
                        or "_provider" in name
                        or ".generated" in name
                    ):
                        errors.append(f"provider boundary violation {path}:{ast.dump(node)}")
            if filename == "functions.py":
                for function in tree.body:
                    if (
                        isinstance(function, ast.FunctionDef)
                        and not function.name.startswith("_")
                        and (not ast.get_docstring(function) or function.returns is None)
                    ):
                        errors.append(f"public function contract missing {path}:{function.lineno}")
    actual_ids = {
        operation["operationId"]
        for path in openapi["paths"].values()
        for method, operation in path.items()
        if method in {"get", "put", "post", "delete", "patch"}
    }
    if actual_ids != operation_ids:
        errors.append("registered routes and operation directories differ")
    main_tree = ast.parse((root / "main.py").read_text())
    if not any(
        isinstance(node, ast.FunctionDef) and node.name == "create_app" for node in main_tree.body
    ):
        errors.append("application factory missing")
    return errors


def main() -> int:
    errors = inspect_operations()
    if errors:
        print("\n".join(errors))
        return 1
    print("Operation layout, provider boundaries and route contracts passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
