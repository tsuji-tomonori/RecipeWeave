# 実装から生成する設計書

[generator.md](generator.md) はPython AST・ソースハッシュ・moonプロジェクト配置から生成します。
`uv run python -m recipeweave_generator.design` で更新し、`--check` で差分を検査します。
生成物を直接編集しません。

[service.md](service.md) は画面実装・OpenAPI・SQL・サンプルJSON・CDK合成テンプレートから生成します。
`app-docs`、フロントとLambdaのビルド、CDK合成後に `uv run python tools/generate_service_design.py` で更新します。
コード・合成の確認と、実環境への配備・人による使いやすさ評価は区別します。
