# 実装から自動生成した設計書

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

82 テーブル・330 API・698 SQLファイルを対象とする。共有呼出しを含むAPIとSQLの対応は 2836 件。

[原設計との対応](database/SOURCE-MAPPING.md) / [テーブル一覧](database/README.md) / [ER図](database/ER.md) / [API一覧](api/README.md) / [CRUD](api/CRUD.md)

[APIモデル・enum](api/MODELS.md) / [共通エラー](api/ERRORS.md) / [サービス・CDK](service.md) / [レシピ生成](generator.md)

[出力一覧](REGISTRY.md) / [生成元・ハッシュ](MANIFEST.md)

APIごとのインターフェース・詳細設計・ログ・SQL・シーケンス・要因別テストの6帳票と、単独のSwagger互換JSONはAPI一覧から参照できる。

生成方法と解析範囲は [開発者向け手順](../AUTOMATION.md) を参照。実装の存在を示す資料であり、未実施の本番接続や受入を完了扱いしない。
