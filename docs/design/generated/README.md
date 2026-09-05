# 実装から生成する設計書

[generator.md](generator.md) はPython AST・ソースハッシュ・moonプロジェクト配置から生成します。
`uv run python -m recipeweave_generator.design` で更新し、`--check` で差分を検査します。
生成物を直接編集しません。未実装のWeb・DB・インフラ機能はその旨を明記します。
