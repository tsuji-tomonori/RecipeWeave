# テーブルとAPIのCRUD対応

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

C=INSERT、R=SELECT、U=UPDATE、D=DELETE。WHERE/RETURNINGを独立したRへ水増ししない。各APIのsql/配下を所有元とし、SQL ASTの対象表・副問い合わせから導出する。

| テーブル | list_foods | get_health | list_recipes | get_recipe | get_state | put_state |
|---|---|---|---|---|---|---|
| recipeweave.schema_migrations | — | — | — | — | — | — |
| recipeweave.user_state | — | — | — | — | R | CU |

SQLがないAPIはJSONサンプルまたは稼働確認を使う。移行台帳への運用処理はAPI CRUDと分ける。
