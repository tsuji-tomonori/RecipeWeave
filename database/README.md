# 正規化データベース

元スプレッドシートで定義した71テーブル・554カラムを、`002_relational_schema.sql`へ実装しています。DDLが物理構造の正本です。食品・商品・数量・レシピ版・工程・生成台帳・検索投影・利用者・献立・資源・在庫・監査をそれぞれの関係として保持します。レシピや利用者状態を1個のJSONへ格納しません。

`003_service_operations.sql`はレシート処理、ワークスペース更新版、私有食材の所有、常備食材、在庫消費、調理前の購入確認を補います。これらは原71表の実装数と区別します。料理の紹介文・材料補足、在庫の保管場所・元数量、タイマー状態も型付き列です。数量不明の在庫は `amount=NULL, quantity_quality='unknown'` とし、0として集計しません。この変更理由は `schema-policy.json` の `column_evolutions` から生成設計に引き継ぎます。

PostgreSQL 16とpgvector拡張を使用します。PL/pgSQL、遅延制約トリガー、行レベルセキュリティ、排他制約による整合を必要とするため、初期Devで使用したAurora DSQL向けの接続を本実装の移行先には使いません。移行接続は管理用 `DATABASE_URL`、通常APIは権限を制限した別の接続ロールとします。

```bash
uv run --locked python database/migrate.py --plan
uv run --locked python database/migrate.py --apply
uv run --locked python database/schema_catalog.py
uv run --locked python database/schema_catalog.py --check
uv run --locked pytest tests/test_relational_schema.py
```

`--plan` は接続不要です。`--apply` は管理用 `DATABASE_URL` を使い、移行単位のDDLと台帳記録を1トランザクションで確定します。並行適用はアドバイザリロックで直列化します。適用済み移行のchecksum不一致は停止します。既存 `001_user_state.sql` とその検証SQLのバイト列は維持します。`user_state` は旧データの移行記録としてのみ残し、新しいサービスAPIの正本にはしません。`schema_migrations` は運用台帳として引き続き維持します。

`schema_catalog.py` は CREATE TABLE、列ALTER、CHECK、UNIQUE、外部キー、索引、COMMENTをDDLから抽出します。原設計の全列と全外部キーを照合し、元の表数・列数と追加された運用モデルを区別します。型・NULL・既定値をスプレッドシートからそのまま転記して生成設計と称することはしません。全SQL文には入力ファイル・文番号・SHA256を対応付け、PL/pgSQL・RLS・トリガーのSQL原文も保持します。PostgreSQL構文解析と実DBへの適用試験が別に必要です。

APIトランザクションでは、検証済み認証情報に基づき `recipeweave.user_id` と `recipeweave.role` を `set_config(..., true)` で設定します。個人表は本人へたどるRLS、私有食材は `food.owner_id` と派生表のRLSで保護します。所有者削除によって私有食材を共通公開へ変換しません。利用者入力からDBロールを選ばせません。

主なDB制約は、数値の有限性、数量と単位、同版の材料・工程、セット付属品の同一商品版、材料使用割合、工程DAG、分類の循環、動作パラメータ、公開後不変、資源予約の同時数量、生成範囲の重複、レシート登録取消と消費の整合です。公開・取下げ・利用者消去は同じDBトランザクションでoutboxへ記録します。JSON列は個別の固定契約に限定し、API側でも厳密に検査します。

1,000万料理の性能、実クラウド配備、試作していないレシピの味・安全性は、DDLや自動テストだけで検証済みとは扱いません。構造検証と実測・試作の証跡を別に記録します。
