"""関数ごとの制御構造をPython ASTからシーケンス図へ投影する。"""

import ast
from pathlib import Path

from .common import DesignError, document, read_source, table


def label(value: str) -> str:
    return "".join(
        {
            ";": "#59;",
            "&": "#38;",
            "<": "#60;",
            ">": "#62;",
            '"': "#34;",
            "'": "#39;",
            "\n": " ",
        }.get(char, char)
        for char in value
    )


def expression(node: ast.AST | None) -> str:
    return ast.unparse(node) if node is not None else "None"


def validate_tree(node: ast.AST, source: str) -> None:
    rejected = (
        ast.Try,
        ast.TryStar,
        ast.With,
        ast.AsyncWith,
        ast.Match,
        ast.Yield,
        ast.YieldFrom,
        ast.Lambda,
        ast.NamedExpr,
        ast.AsyncFor,
    )
    for item in ast.walk(node):
        if isinstance(item, rejected):
            raise DesignError(f"未対応の制御構造: {source}:{item.lineno}: {type(item).__name__}")
        if isinstance(item, ast.Call) and not isinstance(item.func, ast.Name | ast.Attribute):
            raise DesignError(f"静的に解決できない呼出し: {source}:{item.lineno}")


def render_expression(node: ast.AST | None, indent: str = "    ") -> list[str]:
    if node is None:
        return []
    # 短絡評価・内包表記・条件式は呼出し列へ平坦化せず、式をそのまま記載する。
    conditional = (ast.BoolOp, ast.IfExp, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
    if any(isinstance(item, conditional) for item in ast.walk(node)):
        return [f"{indent}Note over Function: 条件付き式を評価: {label(expression(node))}"]
    lines = []
    for child in ast.iter_child_nodes(node):
        lines.extend(render_expression(child, indent))
    if isinstance(node, ast.Call):
        lines.extend(
            [
                f"{indent}Function->>Callee: {label(expression(node))}",
                f"{indent}Callee-->>Function: 呼出結果（例外は呼出元へ伝播）",
            ]
        )
    return lines


def block(statements: list[ast.stmt], source: str, indent: str = "    ") -> list[str]:
    lines = []
    for node in statements:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue
        if isinstance(node, ast.If):
            lines += render_expression(node.test, indent)
            lines.append(f"{indent}alt {label(expression(node.test))}")
            lines += block(node.body, source, indent + "    ")
            if node.orelse:
                lines.append(f"{indent}else 条件が偽")
                lines += block(node.orelse, source, indent + "    ")
            lines.append(f"{indent}end")
        elif isinstance(node, ast.For | ast.While):
            if isinstance(node, ast.For):
                title = f"{expression(node.target)} in {expression(node.iter)}"
                lines += render_expression(node.iter, indent)
            else:
                title = expression(node.test)
            lines.append(f"{indent}loop {label(title)}")
            if isinstance(node, ast.While):
                lines += render_expression(node.test, indent + "    ")
            lines += block(node.body, source, indent + "    ")
            lines.append(f"{indent}end")
            if node.orelse:
                lines.append(f"{indent}opt breakせずループを終了")
                lines += block(node.orelse, source, indent + "    ")
                lines.append(f"{indent}end")
        elif isinstance(node, ast.Return | ast.Raise):
            value = node.value if isinstance(node, ast.Return) else node.exc
            lines += render_expression(value, indent)
            kind = "return" if isinstance(node, ast.Return) else "raise"
            lines += [
                f"{indent}break この経路の関数終了: {kind}",
                f"{indent}    Function-->>Caller: {label(expression(value))}",
                f"{indent}end",
            ]
            break
        elif isinstance(node, ast.Assign | ast.AnnAssign | ast.AugAssign | ast.Expr):
            lines += render_expression(node.value, indent)
            if not isinstance(node, ast.Expr):
                lines.append(f"{indent}Note over Function: {label(expression(node))}")
        elif isinstance(node, ast.Continue | ast.Break | ast.Pass):
            action = {
                ast.Continue: "次の反復へ進む",
                ast.Break: "最内のループを終了する",
                ast.Pass: "処理なし",
            }[type(node)]
            lines.append(f"{indent}Note over Function: {action}")
            if not isinstance(node, ast.Pass):
                break
        elif isinstance(node, ast.Assert):
            lines += render_expression(node.test, indent)
            lines.append(f"{indent}Note over Function: 表明を確認: {label(expression(node.test))}")
        else:
            raise DesignError(f"未対応の文: {source}:{node.lineno}: {type(node).__name__}")
    return lines


def function_sections(path: Path, root: Path) -> tuple[list[str], list[list[object]]]:
    source = str(path.relative_to(root))
    parsed = ast.parse(read_source(path, root), filename=source)
    diagrams = []
    functions = []
    for fn in parsed.body:
        if not isinstance(fn, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        validate_tree(fn, source)
        if any(
            isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef)
            for stmt in fn.body
            for item in ast.walk(stmt)
        ):
            raise DesignError(f"入れ子の関数は未対応です: {source}:{fn.name}")
        doc = ast.get_docstring(fn) or "個別の説明なし。下記の実装を参照。"
        functions.append([fn.name, doc, f"{source}:{fn.lineno}"])
        signature = ast.unparse(fn.args)
        lines = [
            f"### {path.name}: `{fn.name}`",
            "",
            f"定義元: `{source}:{fn.lineno}`",
            "",
            "```mermaid",
            "sequenceDiagram",
            "    participant Caller as 呼出元",
            f"    participant Function as {fn.name}",
            "    participant Callee as 呼出先",
            f"    Caller->>Function: {label(signature)}",
        ]
        lines += block(fn.body, source)
        lines += ["```", "", "#### 対応する実装", "", "```python", ast.unparse(fn), "```"]
        diagrams.append("\n".join(lines))
    return diagrams, functions


def render_sequences(directory: Path, root: Path, operation_id: str) -> tuple[str, str]:
    diagrams = []
    functions = []
    for filename in ("router.py", "functions.py"):
        found, rows = function_sections(directory / filename, root)
        diagrams += found
        functions += rows
    sequence = document(
        f"シーケンス: {operation_id}",
        [
            "対象はrouter.py・functions.pyの各関数。呼出元・関数・呼出先の3者で、関数内の分岐と反復を示す。"
            "関数間を推測で展開せず、呼出先の名前をそのまま記載する。内包表記・短絡評価は条件付き式のまま残す。"
            "FastAPIの依存解決、middleware、連携ポートの実装内部はこの図の対象外で、詳細設計と定義元を参照する。"
            "continue/breakは注記位置で該当経路を終了し、次の反復/ループ外へ進む。",
            *diagrams,
        ],
    )
    return sequence, table(["関数", "責務", "定義元"], functions)
