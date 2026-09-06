---
title: "実装から自動生成した設計書"
---

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

2 テーブル・6 API・3 SQLを対象とする。

[テーブル一覧](/RecipeWeave/quality/design/database/) / [ER図](/RecipeWeave/quality/design/database/er/) / [API一覧](/RecipeWeave/quality/design/api/) / [CRUD](/RecipeWeave/quality/design/api/crud/)

[APIモデル・enum](/RecipeWeave/quality/design/api/models/) / [共通エラー](/RecipeWeave/quality/design/api/errors/) / [サービス・CDK](/RecipeWeave/quality/design/service/) / [レシピ生成](/RecipeWeave/quality/design/generator/)

[出力一覧](/RecipeWeave/quality/design/registry/) / [生成元・ハッシュ](/RecipeWeave/quality/design/manifest/)

APIごとのインターフェース・SQL・詳細・シーケンス・検証仕様はAPI一覧から参照できる。

生成方法と解析範囲は [開発者向け手順](/RecipeWeave/quality/design/automation/) を参照。実装の存在を示す資料であり、未実施の本番接続や受入を完了扱いしない。
