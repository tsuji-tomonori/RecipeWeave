"""実際のSQLFluffで、名前付き引数と不正SQLの検出を確認する。"""

from app.tools.sql_lint import inspect_sql, run_sqlfluff


def test_repository_sql_passes_static_analysis() -> None:
    assert inspect_sql() == []


def test_psycopg_named_parameters_are_parsed_without_runtime_values() -> None:
    result = run_sqlfluff(
        ["parse", "--format", "json", "-"],
        source="SELECT revision FROM recipeweave.user_state WHERE subject = %(subject)s;\n",
    )
    assert result.returncode == 0, result.stderr


def test_sqlfluff_rejects_unparseable_statement() -> None:
    result = run_sqlfluff(
        ["parse", "--format", "json", "-"],
        source="SELECT revision FROM WHERE subject = %(subject)s;\n",
    )
    assert result.returncode != 0
