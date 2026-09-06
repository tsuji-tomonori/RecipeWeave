# RecipeWeave API

Python 3.12 / FastAPI / psycopgによる、PostgreSQL 16とpgvectorを使うAPIです。元スプレッドシートの71テーブルをすべて実装し、レシート・私有食材・在庫消費などの追加9テーブルも扱います。食品、料理版、材料、工程、献立、在庫を正規化した行へ保存します。初期JSONはDBへのseed入力専用で、APIは実行時にDBを検索します。

要件正本は[requirements.qnt](../spec/requirements/requirements.qnt)、DB正本と移行手順は[database/README.md](../database/README.md)です。利用者向けの説明は[マニュアル](../docs/service/manual.md)と[Q&A](../docs/service/faq.md)、現在の配備・検証状況は[Dev検証記録](../docs/verification/service-dev.md)を参照してください。

追加9表は業務補完7表とバックアップ用台帳2表です。旧互換表と移行台帳を含め、物理表は82表です。

## APIの使い分け

| 分類 | 主な経路 | 動作 |
| --- | --- | --- |
| 認証 | `/api/auth/local-login`、`/api/me` | 開発用ログイン、検証済み本人情報 |
| カタログ | `/api/foods`、`/api/recipes`、`/api/recipes/random` | DBに保存した食品・料理の検索、ランダム提案 |
| 料理詳細 | `/api/recipes/{recipe_id}` | 数量・材料・工程。`versionId`で履歴と同じ料理版を指定 |
| 利用者の操作 | `/api/workspace`、在庫・献立・保存・設定の個別API | 本人の関係データを取得・変更 |
| レシート | `/api/receipts/commit`、`/api/receipts/{row_id}/undo` | 確認済み明細の在庫登録、再送検出、取消 |
| 調理 | `/api/cooking-plan`、`/api/cooking-sessions` | 読取専用の段取り確認、計画確定、進行・タイマー保存 |
| バックアップ | `/api/backups/export`、`/api/backups/preview`、`/api/backups/restore` | 本人の34表と表示設定を出力し、全制約の確認後に原子的に全置換 |
| 正規化データ | `/api/entities/{table}`、`/api/entities/{table}/{row_id}` | 登録済みの固定ルートで、全表に必要な型付き操作を提供 |
| 生成ワーカー | `/api/generation/shards/claim`ほか | リース取得・延長、フェンストークン付き進捗更新 |

正確なメソッド、経路、全入力・応答は[生成API一覧](../docs/design/generated/api/README.md)と[OpenAPI](openapi.gen.json)から確認できます。テーブル名や任意SQLを受け取って動的に操作を組み立てるAPIではありません。

人数・分量は料理を選んだ後で変更するため検索条件に含めません。通常の料理検索は公開・審査済み版を返します。初期8品は未試作の下書きとしてDBへ投入し、試用を許可した開発環境で署名検証済みの本人だけが閲覧できます。`ENVIRONMENT` が `dev/local/test` で、`ALLOW_CATALOG_PREVIEW=true` または既存の開発用認証設定が有効な場合に限ります。Cognitoを使うDevではフラグが必須です。`production` はフラグを有効にしても常に拒否します。取下げ版は既存の本人履歴から参照でき、新規履歴の後付けで閲覧権限を取得することはできません。

利用者の表は、子行から親へたどる所有権まで確認します。カタログ編集と生成運用は管理者権限が必要です。公開後の内容版、監査、outbox、派生集計には保持規則を適用し、無制約の更新・削除を公開しません。

## ローカルで起動する

リポジトリのルートから実行します。

```bash
docker compose up --build
```

ComposeはPostgreSQL、管理用移行、非管理者のAPI、フロントエンドを順に起動します。画面は `http://127.0.0.1:5173`、APIは `http://127.0.0.1:8000` です。Compose内の資格情報はこのローカル構成専用です。

Pythonを直接起動する場合は依存を準備し、移行済みの非管理者DB接続と認証設定を環境変数で指定します。

```bash
uv sync --locked --all-packages
uv run --locked --package recipeweave-api uvicorn app.main:app --reload
```

DBが未設定・接続不能の場合は503を返します。ブラウザ保存やサンプルJSONへ切り替えて成功したように見せる経路はありません。

## 接続と認証

| 設定 | 用途 |
| --- | --- |
| `DATABASE_URL` | API専用のPostgreSQL接続。移行所有者・superuser・BYPASSRLSロールを使わない |
| `MIGRATION_DATABASE_URL` | 起動準備・CIで使う管理用接続。通常のAPIへ配らない |
| `AUTH_MODE=cognito` | 通常の認証方式。`COGNITO_ISSUER`と`COGNITO_CLIENT_ID`を設定 |
| `AUTH_MODE=local` | `ENVIRONMENT=local/test`、32文字以上の`LOCAL_AUTH_SECRET`、12文字以上の`LOCAL_AUTH_PASSWORD`があるローカル開発に限定 |
| `DATABASE_SECRET_ARN`、`DATABASE_HOST`、`DATABASE_NAME` | AWS実行時にDB資格情報を解決する設定。TLSを必須とする |
| `ALLOWED_ORIGINS` | CORSを許可するoriginの明示的な一覧 |
| `MAX_REQUEST_BYTES` | 本文上限。既定1MiB、JSON解析前にも検査 |

Cognitoは署名、発行者、期限、用途、クライアント、主体を検証し、管理権限は検証済みのグループから導出します。本人のDB IDは検証済み主体から生成し、本文、`X-User-Id`、余剰のtoken claimで変更できません。要求単位のトランザクションに本人IDとロールを設定し、DBのRLSも同時に適用します。

汎用操作の更新・削除は取得時の `ETag` を `If-Match` に指定します。業務操作は `expectedVersion` で本人のワークスペース版を確認します。不一致は409、汎用操作でヘッダーがなければ428です。認可、正規化行、監査、更新版は同じトランザクションで確定し、失敗時はまとめてロールバックします。

## SQL・設計の生成

DB操作の正本は `src/app/apis/<resource>/<operation>/sql/*.sql` です。ORMを使わず、名前付きパラメータの値をSQL本文とは別に束縛します。共有の監査・outbox・更新版SQLも生成・検査対象です。

```bash
uv run --locked python database/schema_catalog.py
uv run --locked python tools/generate_entity_apis.py
uv run --locked python tools/generate_backup_api.py
uv run --locked --package recipeweave-api app-docs
uv run --locked python tools/generate_service_design.py
```

最初にDDLから列・制約を抽出し、全表のモデルと操作SQLを生成します。`app-docs`は各操作の型付きクエリと実ルートのOpenAPIを生成します。設計生成はDDL・SQL・OpenAPI・Pythonの実装からテーブル仕様、ER図、API仕様、CRUD対応、シーケンス、試験対応を作ります。インフラ設計を含む最終生成には、同じ版のCDK合成結果も必要です。

生成ファイルを手編集せず、入力を修正して再生成してください。`--check`は差分を検出し、ファイルを書き換えません。SQLGlotは構文と単文・明示列を検査し、SQLFluffはAPI別SQLと移行DDLを検査します。
復元の制約検証に使う固定の `SET CONSTRAINTS ALL IMMEDIATE/DEFERRED` はpglastで単文と対象を検証し、設計には制約の検証タイミングとして記録します。

## 検査とエビデンス

```bash
uv run --locked ruff format --check backend database
uv run --locked ruff check backend database
uv run --locked pyright --project backend/pyproject.toml
uv run --locked mypy --config-file backend/pyproject.toml backend/src backend/tests backend/tools database
uv run --locked --package recipeweave-api app-archlint
uv run --locked --package recipeweave-api app-sql-lint
uv run --locked python tools/generate_entity_apis.py --check
uv run --locked --package recipeweave-api app-docs --check
uv run --locked python tools/generate_service_design.py --check
uv run --locked pytest backend/tests tests/test_relational_schema.py --cov=app --cov-branch --junitxml=reports/backend-junit.xml
```

実DB試験には `TEST_DATABASE_URL` と `MIGRATION_DATABASE_URL` を設定します。全表のHTTP読取り、本人隔離、DBのRLS、競合、レシート処理、公開・履歴参照、業務制約を実際のPostgreSQLで確認します。CIは非特権のアプリロールを使用し、未実行・スキップを成功の代用にしません。JUnit、coverage、操作別画像を実行版へ対応付け、品質レポートとPagesの設計サイトへ載せます。

Lambda配布物は次のコマンドで作ります。実装と固定した依存を梱包し、実行時参照用の食品・レシピJSONは含めません。

```bash
uv run --locked --package recipeweave-api python backend/tools/package_lambda.py --architecture x86_64
```

Pagesは静的画面・設計・検証結果の配信です。Cognito、API Gateway、Lambda、PostgreSQLの実配備と接続確認は別の受入事項として、Dev検証記録に残します。

## DBバックアップの確認と復元

設定画面で取得する形式2のファイルは、本人の34表について元ID・全列・過去の調理・在庫消費・私有食品を保持します。数値列を十進文字列で出力し、JavaScriptの浮動小数点を経由しません。最大5,000,000バイトです。共有食品・公開料理版は参照を保持し、アカウントの認証情報・監査・outbox・現在版を古い内容へ置き換えません。

復元はファイル確認、サーバーで全制約を検証するプレビュー、利用者の最終確認、の順です。プレビューの試験書込みはすべてロールバックします。15分間・本人・本文ハッシュ・現在版に結び付いた確認を単回消費し、全34表の置換・版更新・監査追記を同一トランザクションで確定します。改竄・別人のファイル・旧形式・参照不整合・同時更新は拒否されます。確認取消しや処理途中の失敗では本人の現在データを保持します。

発行証跡と復元確認の2表には本文を保存せず、利用者が任意に作成・更新・削除する汎用操作も提供しません。失われた共有参照や外部から採用された私有定義がある場合は409で全体を戻します。`backend/tests/test_backup_database.py`で実DBの往復・所有権・精度・競合・全体取消しを検証します。
