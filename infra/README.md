# RecipeWeaveの実DB基盤と検証・公開

明示的な `stage=dev` だけ `ALLOW_CATALOG_PREVIEW=true` を設定し、認証済み利用者が初期レシピを試用できます。`production` とその他のstageは無効です。未試作レシピのdraft状態や検証記録は変更せず、一般公開済みとして扱いません。

通常のアプリは PostgreSQL に保存した食品・レシピ・材料・工程・利用者データをAPIから操作します。ブラウザの固定レシピを検索結果として返す配布形態は終了しました。ローカルとCIで同じ実DBを使い、単体試験・DB統合・ブラウザE2Eの証跡を公開します。

## ローカル実行

```bash
docker compose up --build -d --wait
```

画面は `http://127.0.0.1:5173`、APIは `http://127.0.0.1:8000` です。移行コンテナは管理者接続でスキーマを適用し、`recipeweave_app` を `NOSUPERUSER NOBYPASSRLS` で作成してから初期データを投入します。APIコンテナに管理者接続は渡しません。DBボリュームは通常停止後も保持します。

ローカル専用利用者は `alice`・`bob`・`admin`、公開パスワードは `recipeweave-local` です。これらと `LOCAL_AUTH_SECRET` はローカル・CIだけの固定値です。本番はCognito認証を使い、local-loginを拒否します。レシート画像のOCRは端末内で処理し、確認した食品と数量をAPIへ登録します。

Dockerを使わず検査する場合は、PostgreSQL 16 + pgvector を準備したうえで次を実行します。

```bash
uv sync --locked --all-packages
npm ci
npm ci --prefix frontend
npm ci --prefix infra
npm ci --prefix documentation
uv run --locked python tools/start_database.py
uv run --locked --package recipeweave-api app-docs
npm run build --prefix frontend
uv run --locked --package recipeweave-api python backend/tools/package_lambda.py --architecture x86_64 --verify-reproducible
npm run synth --prefix infra
uv run --locked python -m recipeweave_generator.design
uv run --locked python tools/generate_service_design.py
uv run --locked python tools/quality.py
```

事前に `MIGRATION_DATABASE_URL` を管理者、`DATABASE_URL` と `TEST_DATABASE_URL` をアプリロール、`ENVIRONMENT=test` に設定します。公開ローカル資格情報の設定例は [compose.yaml](../compose.yaml) にあります。実DB試験で接続設定がなければ必須CIは失敗します。単体試験を成功させて実DB未実行を受入済みとは扱いません。

配備資材の構築にはCIと同じuv 0.11.33を使用します。Lambda構築はPython起動スクリプトの絶対パスを可搬なshebangへそろえ、wheelのRECORDも実バイトに合わせます。handlerの独立importはbytecodeを作らず、資材が変化しないことを検査します。`--verify-reproducible` は別ディレクトリへの再構築と全ファイルのSHA-256一致を必須にします。Dev用の設計を再生成するときは、画面の `VITE_AUTH_MODE=cognito`・`VITE_CATALOG_PREVIEW=true` とAPI/Cognitoの公開設定もCIにそろえます。構築したCDKテンプレートの全バイトhashは設計に残し、設定変更時も正規再生成してGitへ反映します。

## CIとGitHub Pages

[dev.yml](../.github/workflows/dev.yml) は dev と既存featureのpush、dev/main向けPRで、固定依存・実PostgreSQL移行・初期投入・静的解析・厳密な型検査・単体/実DB統合・実画面E2E・品質サイトE2Eを実行します。失敗時も取得できた証跡をartifactへ残します。検査がすべて成功したpushだけを既存の `github-pages` 環境へ公開します。環境保護や配備対象ブランチの許可は変更しません。

| 公開パス                       | 内容                                                         |
| ------------------------------ | ------------------------------------------------------------ |
| `/RecipeWeave/`                | 実APIへ接続するアプリ                                        |
| `/RecipeWeave/quality/`        | 日本語の品質結果・単体/DB統合・E2E画面・静的解析・カバレッジ |
| `/RecipeWeave/quality/design/` | 検索可能な実装由来設計、ER・API・SQL・シーケンス・Swagger    |

Pagesは静的ホストなので、PostgreSQLやFastAPI自体は実行できません。アプリのAPI接続先はGitHub変数 `DEV_API_BASE_URL` を `VITE_API_BASE_URL` に渡してビルドします。認証は `DEV_COGNITO_DOMAIN` と `DEV_COGNITO_CLIENT_ID` をビルド時に渡します。接続先未配備時は接続不能を表示し、固定サンプルを本物のDB結果に見せません。CIのE2Eでは同じrevisionのFastAPIとPostgreSQLへ接続します。単体・DB統合試験でcommitしたデータがブラウザE2Eへ混ざらないよう、E2E専用の新規DBへ同じ移行と初期データを適用します。

[browser.yml](../.github/workflows/browser.yml) は独立した実DBでPC・モバイルのブラウザシナリオだけを先行実行します。全体品質ゲートは維持します。ブラウザ失敗時は、合成データ専用のCIに限ってAPIログと画面のerror-contextを認証情報を除去してActionsログへも残し、artifactの取得に失敗しても原因を確認できます。

`reports/deployment-readiness.json` は公開接続の設定有無だけを保存し、実APIへの到達やAWS配備成功とは区別します。

`reports/quality.json` は各ゲートのコマンド・終了コード・実出力、JUnitは個別試験結果、Playwright JSONとPNGは Given/When/Then と画面証跡、coverage JSON/HTMLは実測値です。レポートの不足・未実行・スキップは区別します。生成設計は正本・実装から再生成し、手修正をしません。

## AWS本番構成

| Stack                              | 主なリソース                                                                                 |
| ---------------------------------- | -------------------------------------------------------------------------------------------- |
| `RecipeWeave-{stage}-Data`         | 2AZ VPC、Aurora PostgreSQL 16.6、Serverless v2 writer/reader、管理者/アプリ別secret、Cognito |
| `RecipeWeave-{stage}-Service`      | 非公開S3/OAC/CloudFront、HTTP API、FastAPI Lambda、移行専用Lambda                            |
| `RecipeWeave-{stage}-GitHubDeploy` | 明示された既存OIDC Providerと完全一致ブランチに限定した配備ロール                            |

今回のDDLはPL/pgSQLトリガーで公開後の変更禁止や工程DAG等を守ります。このためAurora PostgreSQLを採用しています。DSQLについて古い「外部キー非対応」を採用理由には使いません。[DSQLの移行ガイド](https://docs.aws.amazon.com/aurora-dsql/latest/userguide/working-with-postgresql-compatibility-migration-guide.html) はトリガーをアプリ層へ移す方針とPL/pgSQLの相違を説明しています。

Auroraは暗号化・削除保護・Retain・14日バックアップ、DBは隔離サブネット、API/移行は非公開サブネット、DBポートは専用セキュリティグループからだけ許可します。Cognito署名・認証・役割と利用者所有権はFastAPIで一元検査します。全APIはCloudFrontキャッシュを無効にし、Authorizationをoriginへ渡します。

APIはアプリ用secretだけを実行時に解決します。移行Lambdaだけに管理者secretを許可し、移行後にアプリロールの最小DML権限を設定します。secret値は出力・ソース・配備テンプレートへ埋めません。移行Lambdaはサンプルや利用者を自動生成しません。

旧DSQLのDataリソースを配備済みの場合は、既存データ移行・バックアップ・切替・Retainされた資源の扱いを明示した作業が必要です。CDKの変更を実データ移行の完了に読み替えません。新しいAWS資源の実配備は、この作業環境では実施していません。

Serverless writer/readerの最小容量、NAT Gateway、DB保存領域・バックアップ等には継続料金が発生します。資格情報がない状態で実AWS作成は実行しません。配備先のAurora対応バージョン、pgvector拡張、権限、バックアップ復元はAWS実環境の受入項目です。

## 検証済みdevからmainへの配備

[deploy.yml](../.github/workflows/deploy.yml) は main と現在devのツリーが一致し、成功済みdev pushの `verified-revision` artifactが source/commit/tree の3値を証明した場合だけ配備を進めます。未検証commit、別tree、古い証跡を拒否します。devの生成物もgitへ反映されたクリーンな状態で証跡を作ります。

`AWS_DEPLOY_ROLE_ARN` または `PRODUCTION_WEB_CALLBACK_URL` が未設定ならAWS配備jobは起動しません。後者は利用者向け画面の正確なHTTPS戻り先URLで、Cognito Authorization Code + PKCEのcallback/logout URLに使います。設定時は既存のGitHub OIDC Providerとmainの完全一致subjectを使うroleを用意し、CDK bootstrap roleへのassumeに限定します。既存GitHub環境を追加する場合、OIDC subject形式が変わるのでbranch trustを勝手に広げず、明示した環境保護と合わせて設定します。

配備は実アセット構築、`cdk synth --strict`、`cdk diff`、Data/Serviceの配備、専用移行Lambdaの実行、status確認、Cognitoの配備結果を設定した画面の再ビルド・Service再配備の順です。CloudFrontの既定ドメインを使用し、独自ACM証明書のTLS最低版を設定したと偽りません。

## 一次資料

- [pgvector公式リポジトリ](https://github.com/pgvector/pgvector)
- [Aurora PostgreSQLのpgvector](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html)
- [CDK DatabaseCluster](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_rds.DatabaseCluster.html)
