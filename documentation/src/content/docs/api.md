---
title: "API一覧"
---

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

| operationId | HTTP | パス | 要約 | 認証 | 応答 |
|---|---|---|---|---|---|
| [list_foods](/RecipeWeave/quality/design/api/operations/list_foods/interface/) | GET | /api/foods | 食材候補を検索する | public | 200, 422 |
| [get_health](/RecipeWeave/quality/design/api/operations/get_health/interface/) | GET | /api/health | 稼働状況とサンプル公開範囲 | public | 200 |
| [list_recipes](/RecipeWeave/quality/design/api/operations/list_recipes/interface/) | GET | /api/recipes | 食材・時間からサンプル料理を探す | public | 200, 422 |
| [get_recipe](/RecipeWeave/quality/design/api/operations/get_recipe/interface/) | GET | /api/recipes/{recipe_id} | 料理の材料と工程を表示する | public | 200, 404, 422 |
| [get_state](/RecipeWeave/quality/design/api/operations/get_state/interface/) | GET | /api/state | 認証した利用者自身の状態を読む | cognito-access-jwt | 200, 401, 503 |
| [put_state](/RecipeWeave/quality/design/api/operations/put_state/interface/) | PUT | /api/state | 版を確認して利用者自身の状態を置き換える | cognito-access-jwt | 200, 401, 409, 413, 422, 503 |

[CRUD対応](/RecipeWeave/quality/design/api/crud/) / [共有モデル](/RecipeWeave/quality/design/api/models/) / [共通エラー](/RecipeWeave/quality/design/api/errors/)
