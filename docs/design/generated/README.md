# 実装から自動生成した設計書

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

2 テーブル・6 API・3 SQLを対象とする。

[テーブル一覧](database/README.md) / [ER図](database/ER.md) / [API一覧](api/README.md) / [CRUD](api/CRUD.md)

[APIモデル・enum](api/MODELS.md) / [共通エラー](api/ERRORS.md) / [サービス・CDK](service.md) / [レシピ生成](generator.md)

[出力一覧](REGISTRY.md) / [生成元・ハッシュ](MANIFEST.md)

APIごとのインターフェース・SQL・詳細・シーケンス・検証仕様はAPI一覧から参照できる。

生成方法と解析範囲は [開発者向け手順](../AUTOMATION.md) を参照。実装の存在を示す資料であり、未実施の本番接続や受入を完了扱いしない。
