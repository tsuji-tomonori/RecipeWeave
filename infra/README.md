# RecipeWeave AWS 基盤

CloudFront / 非公開 S3 → API Gateway HTTP API → Lambda 上の FastAPI → Aurora DSQL と、Cognito の認証基盤を定義します。今回の検査対象は、AWS に配備しない型・構造検査と CloudFormation 合成です。**AWS は再認証が必要なため、実配備・実 DB 接続・認証を含む統合動作は未受入です。**

GitHub Pages の Dev は、8 品のサンプル・端末内 OCR・同じブラウザへの保存で動く別の配布先です。AWS 基盤を合成できても、Dev のログインやクラウド同期が利用可能になるわけではありません。現在のフロントエンドを AWS に配信しても、ログイン・同期 UI はまだ提供しません。

## 構成

| Stack                          | 内容                                                                                | ライフサイクル                                                             |
| ------------------------------ | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `RecipeWeave-dev-Data`         | Aurora DSQL、Cognito User Pool / Client                                             | Stack の termination protection、DSQL / User Pool の削除保護と Retain      |
| `RecipeWeave-dev-Service`      | private S3、CloudFront OAC、HTTP API、Lambda、専用 migration role、静的ファイル配布 | S3 は暗号化・公開禁止・バージョニング・Retain                              |
| `RecipeWeave-dev-GitHubDeploy` | 既存 GitHub OIDC Provider を参照する deploy role                                    | `githubOidcProviderArn` 指定時だけ生成。Provider や bootstrap は作成しない |

DSQL / Cognito はサービスコードと分けます。再生成できる静的配布物の S3 は、OAC の Distribution ARN 制約と同じ Service stack に置き、相互参照の循環を避けます。S3 読み出しは、この CloudFront Distribution のサービス主体だけに許可します。

AWS CDK v2 ライブラリ `2.268.0`、CLI `2.1140.0` と関連ツールを `package.json` / `package-lock.json` に固定しています。TypeScript `strict` を有効にし、明示的 `any` を禁止します。CDK 自身の任意プロパティ型と互換性がない `exactOptionalPropertyTypes` は使用しません。

## API と認証

| Route                   | 認証               | CloudFront cache                                         |
| ----------------------- | ------------------ | -------------------------------------------------------- |
| `GET /api/health`       | 公開               | 無効                                                     |
| `GET /api/foods`        | 公開               | 既定 30 秒、最大 60 秒。query string を cache key に含む |
| `GET /api/recipes`      | 公開               | 同上                                                     |
| `GET /api/recipes/{id}` | 公開               | 同上                                                     |
| `GET /api/state`        | Cognito access JWT | 無効。`Authorization` を origin に転送                   |
| `PUT /api/state`        | Cognito access JWT | 無効。`Authorization` を origin に転送                   |

User Pool Client は secret を持たず、SRP 認証と refresh token を許可します。Gateway は issuer / client audience と `aws.cognito.signin.user.admin` scope を検証します。この scope は Cognito の SRP で得られる access token の scope です。バックエンドも署名・issuer・client・`token_use=access`・利用者の `sub` を検証します。ID token を API の代用にしません。Hosted login の callback / OAuth UI は、今後のクラウド認証画面と合わせて設定します。

state は `{ version, snapshot }` を返し、更新は `{ expectedVersion, snapshot }` を送ります。版が競合した場合は `409` を返します。利用者 ID は認証 token の `sub` から決まり、リクエストが指定した任意の ID を使いません。

CloudFront は API の viewer `Host` を origin host に置き換えます。private state は共有 cache に保存しません。エラー応答の独立した最小 TTL も 0 秒にし、元の status を保ちます。SPA は hash route を使い、認証エラーの `403` を HTML `200` に置き換える全体的な error fallback は設けません。同じ CloudFront origin からの API 利用を前提とし、CORS wildcard はありません。

## 検査と実アセット

Node.js 24 以上と、ルートの uv 環境が必要です。リポジトリルートで実行します。

```bash
uv sync --locked
npm --prefix frontend ci --no-audit --no-fund
npm --prefix frontend run build
uv run --package recipeweave-api python backend/tools/package_lambda.py --architecture x86_64
npm --prefix infra ci --no-audit --no-fund
npm --prefix infra run check
npm --prefix infra run synth
```

Lambda は `backend/.build/lambda` の **依存を含む実ビルド**をアセットにし、Python 3.12 / x86_64 / `app.handler.handler` で起動します。静的配布は `frontend/dist` を使います。成果物がなければ失敗し、placeholder には置き換えません。構造テストもこの実アセットを使います。

合成テンプレートは `infra/cdk.out/RecipeWeave-dev-Data.template.json` と `RecipeWeave-dev-Service.template.json`、OIDC 指定時だけ `RecipeWeave-dev-GitHubDeploy.template.json` です。コードから再生成するため Git 管理しません。実装由来の設計生成はこの JSON を入力にします。`cdk.context.json` に lookup 値はなく、合成のために AWS へ問い合わせません。

実アセットがまだない開発中は、`npm --prefix infra run test:core` で Data / OIDC / 設定の 3 検査だけを先行できます。これは Service stack を含む全構造検査や合成の成功には読み替えません。配布前の `check` / `synth` では実アセットが必須です。

## AWS 配備手順（今回未実行）

1. 対象アカウントへ認証し、`aws sts get-caller-identity` で配備先を確認します。DSQL 対応リージョンと既存 CDK bootstrap 状態を確認します。未設定での合成リージョンは `us-east-1` です。
2. `CDKToolkit` と qualifier を確認します。未導入なら、組織が承認した CloudFormation 実行 policy / permissions boundary で管理者が bootstrap します。本アプリは IAM / OIDC Provider の自動探索・自動作成や bootstrap 変更を行いません。
3. 実アセットと検査を完了し、`infra` で `npx cdk diff` を確認します。Data stack の replacement、削除保護、IAM 変更を確認します。
4. migration 実行を許可する既存 IAM role ARN を `MigrationOperatorArn` に明示して配備します。
5. Outputs の DSQL endpoint と IAM role ARN を使って migration を実行し、その後に認証・所有権・競合の統合検査を行います。

以下は手動配備例です。`MIGRATION_OPERATOR_ARN` は実在し、配備先で承認済みの role ARN に設定します。user / root / wildcard は受け付けません。

```bash
cd infra
npx cdk diff
npx cdk deploy RecipeWeave-dev-Data RecipeWeave-dev-Service \
  --parameters RecipeWeave-dev-Service:MigrationOperatorArn="$MIGRATION_OPERATOR_ARN" \
  --outputs-file cdk.out/deployed-outputs.json
```

`stage` を変える場合は全操作で同じ `-c stage=...` を指定し、環境ごとに独立した stack を作ります。利用者データを持つ stack の logical ID は気軽に変更しません。

### DSQL migration

Lambda の app role には、この cluster ARN に対する `dsql:DbConnect` だけを付与します。`dsql:DbConnectAdmin` は migration role のみです。migration role の trust は `MigrationOperatorArn` の role だけを対象とし、API runtime からは引き受けられません。DSQL 側の `recipeweave_app` への IAM 対応付けと schema 作成は migration が担当します。

| 実行設定                 | Output                                           |
| ------------------------ | ------------------------------------------------ |
| `DSQL_HOST`              | Data stack `DsqlHost`（DSQL の `Endpoint` 属性） |
| `AWS_REGION`             | 配備したリージョン                               |
| `DSQL_MIGRATION_IAM_ARN` | Service stack `DsqlMigrationIamArn`              |
| `DSQL_APP_IAM_ARN`       | Service stack `DsqlAppIamArn`                    |

migration role を assume したセッションで、ルートから `uv run --package recipeweave-api python database/migrate.py --apply` を実行します。資格情報や DSQL 認証 token をログや Git に残しません。正確なオプションと事前検査は [database/README.md](../database/README.md) を参照してください。migration 前の state API は使用可能として扱いません。

### GitHub OIDC 配備

既存 GitHub OIDC Provider ARN を確認してから `-c githubOidcProviderArn=...` を指定します。provider は参照し、新規作成しません。既定の trust は audience `sts.amazonaws.com`、subject `repo:tsuji-tomonori/RecipeWeave:ref:refs/heads/dev` だけです。

必要な場合だけ `-c githubBranch=実在するブランチ名` で一つの branch を指定します。wildcard は受け付けません。GitHub Environment を付けると token の subject 形式が変わるため、この branch 形式の role をそのまま使えません。環境を追加する際は branch と environment の保護条件も合わせて設計します。

GitHub role の権限は、同じ account / region / qualifier の既存 bootstrap `deploy` / `file-publishing` / `image-publishing` / `lookup` role の assume に限定します。bootstrap 側にもこの role を許可する trust と、承認した CloudFormation 実行権限が必要です。アプリの IAM 管理権限を GitHub role に直接 wildcard 付与しません。初回の OIDC role 配備は既存管理者の資格情報で行います。継続配備用 Actions では静的 AWS key を置かず、`id-token: write` による OIDC を使います。

## ログと負荷

API は 10 request/秒・burst 30、Lambda は同時実行 10・timeout 25 秒です。アクセスログは request ID、route key、status、応答サイズ、処理時間に限定し、token、query、画像、OCR 全文、リクエスト本文、IP を含めません。CloudWatch Logs は 30 日保持です。Dev OCR は端末内処理のため、レシート画像を受け取るクラウド endpoint 自体を設けていません。

## 一次資料

- [AWS CDK: DSQL CfnCluster と Endpoint 属性](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_dsql.CfnCluster.html)
- [DSQL: IAM と DB role の認証・認可](https://docs.aws.amazon.com/aurora-dsql/latest/userguide/authentication-authorization.html)
- [HTTP API: JWT の検証](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html)
- [Cognito access token](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-the-access-token.html)
- [CDK: S3BucketOrigin と OAC](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_cloudfront_origins.S3BucketOrigin.html)
- [CloudFront: エラー応答の独立した最小 TTL](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/custom-error-pages-expiration.html)
