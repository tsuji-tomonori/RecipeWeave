# API一覧

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

| operationId | HTTP | パス | 要約 | 認証 | 応答 |
|---|---|---|---|---|---|
| [list_foods](operations/list_foods/interface.md) | GET | /api/foods | 食材候補を検索する | public | 200, 422 |
| [get_health](operations/get_health/interface.md) | GET | /api/health | 稼働状況とサンプル公開範囲 | public | 200 |
| [list_recipes](operations/list_recipes/interface.md) | GET | /api/recipes | 食材・時間からサンプル料理を探す | public | 200, 422 |
| [get_recipe](operations/get_recipe/interface.md) | GET | /api/recipes/{recipe_id} | 料理の材料と工程を表示する | public | 200, 404, 422 |
| [get_state](operations/get_state/interface.md) | GET | /api/state | 認証した利用者自身の状態を読む | cognito-access-jwt | 200, 401, 503 |
| [put_state](operations/put_state/interface.md) | PUT | /api/state | 版を確認して利用者自身の状態を置き換える | cognito-access-jwt | 200, 401, 409, 413, 422, 503 |

[CRUD対応](CRUD.md) / [共有モデル](MODELS.md) / [共通エラー](ERRORS.md)
