# SQL仕様: get_recipe

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

このAPIはSQLを実行しない。データの取得元は下記関数・連携ポートを参照する。

SQLファイル→自動生成wrapper→連携adapter→functions→routerの境界で管理する。利用者入力はパラメーターとして渡し、SQL文字列へ連結しない。
