---
title: "自動生成ファイル一覧"
---

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

| ファイル | 区分 |
|---|---|
| [MANIFEST.md](/RecipeWeave/quality/design/manifest/) | MANIFEST.md |
| [README.md](/RecipeWeave/quality/design/) | README.md |
| [REGISTRY.md](/RecipeWeave/quality/design/registry/) | REGISTRY.md |
| [api/CRUD.md](/RecipeWeave/quality/design/api/crud/) | api |
| [api/ERRORS.md](/RecipeWeave/quality/design/api/errors/) | api |
| [api/MODELS.md](/RecipeWeave/quality/design/api/models/) | api |
| [api/README.md](/RecipeWeave/quality/design/api/) | api |
| [api/operations/get_health/detail.md](/RecipeWeave/quality/design/api/operations/get_health/detail/) | api |
| [api/operations/get_health/interface.md](/RecipeWeave/quality/design/api/operations/get_health/interface/) | api |
| [api/operations/get_health/queries.md](/RecipeWeave/quality/design/api/operations/get_health/queries/) | api |
| [api/operations/get_health/sequence.md](/RecipeWeave/quality/design/api/operations/get_health/sequence/) | api |
| [api/operations/get_health/tests.md](/RecipeWeave/quality/design/api/operations/get_health/tests/) | api |
| [api/operations/get_recipe/detail.md](/RecipeWeave/quality/design/api/operations/get_recipe/detail/) | api |
| [api/operations/get_recipe/interface.md](/RecipeWeave/quality/design/api/operations/get_recipe/interface/) | api |
| [api/operations/get_recipe/queries.md](/RecipeWeave/quality/design/api/operations/get_recipe/queries/) | api |
| [api/operations/get_recipe/sequence.md](/RecipeWeave/quality/design/api/operations/get_recipe/sequence/) | api |
| [api/operations/get_recipe/tests.md](/RecipeWeave/quality/design/api/operations/get_recipe/tests/) | api |
| [api/operations/get_state/detail.md](/RecipeWeave/quality/design/api/operations/get_state/detail/) | api |
| [api/operations/get_state/interface.md](/RecipeWeave/quality/design/api/operations/get_state/interface/) | api |
| [api/operations/get_state/queries.md](/RecipeWeave/quality/design/api/operations/get_state/queries/) | api |
| [api/operations/get_state/sequence.md](/RecipeWeave/quality/design/api/operations/get_state/sequence/) | api |
| [api/operations/get_state/tests.md](/RecipeWeave/quality/design/api/operations/get_state/tests/) | api |
| [api/operations/list_foods/detail.md](/RecipeWeave/quality/design/api/operations/list_foods/detail/) | api |
| [api/operations/list_foods/interface.md](/RecipeWeave/quality/design/api/operations/list_foods/interface/) | api |
| [api/operations/list_foods/queries.md](/RecipeWeave/quality/design/api/operations/list_foods/queries/) | api |
| [api/operations/list_foods/sequence.md](/RecipeWeave/quality/design/api/operations/list_foods/sequence/) | api |
| [api/operations/list_foods/tests.md](/RecipeWeave/quality/design/api/operations/list_foods/tests/) | api |
| [api/operations/list_recipes/detail.md](/RecipeWeave/quality/design/api/operations/list_recipes/detail/) | api |
| [api/operations/list_recipes/interface.md](/RecipeWeave/quality/design/api/operations/list_recipes/interface/) | api |
| [api/operations/list_recipes/queries.md](/RecipeWeave/quality/design/api/operations/list_recipes/queries/) | api |
| [api/operations/list_recipes/sequence.md](/RecipeWeave/quality/design/api/operations/list_recipes/sequence/) | api |
| [api/operations/list_recipes/tests.md](/RecipeWeave/quality/design/api/operations/list_recipes/tests/) | api |
| [api/operations/put_state/detail.md](/RecipeWeave/quality/design/api/operations/put_state/detail/) | api |
| [api/operations/put_state/interface.md](/RecipeWeave/quality/design/api/operations/put_state/interface/) | api |
| [api/operations/put_state/queries.md](/RecipeWeave/quality/design/api/operations/put_state/queries/) | api |
| [api/operations/put_state/sequence.md](/RecipeWeave/quality/design/api/operations/put_state/sequence/) | api |
| [api/operations/put_state/tests.md](/RecipeWeave/quality/design/api/operations/put_state/tests/) | api |
| [database/ER.md](/RecipeWeave/quality/design/database/er/) | database |
| [database/README.md](/RecipeWeave/quality/design/database/) | database |
| [database/tables/recipeweave.schema_migrations.md](/RecipeWeave/quality/design/database/tables/recipeweave.schema_migrations/) | database |
| [database/tables/recipeweave.user_state.md](/RecipeWeave/quality/design/database/tables/recipeweave.user_state/) | database |
| [service.md](/RecipeWeave/quality/design/service/) | service.md |

generator.mdは独立したレシピ生成器の設計生成コマンドが管理する。
