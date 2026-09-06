# RecipeWeave API

Python 3.12 / FastAPI / Mangum のAPI実装です。GitHub Pages Devはブラウザー内の8品と端末データで動作し、このAPIへの接続やクラウド同期を提供しません。AWSには未デプロイです。

要件正本は `spec/requirements/requirements.qnt`。利用者の操作は `docs/service/manual.md` と `faq.md` を参照してください。

## API

| Method | Path | 動作 |
| --- | --- | --- |
| GET | `/api/health` | サンプルAPIの応答確認 |
| GET | `/api/foods?q=トマト` | 食材名・別名の検索 |
| GET | `/api/recipes` | 8品の検索。`selectedFoodIds`、`excludedFoodIds`、`equipment` は同名queryを繰り返す。`match=all/any`、`maxMinutes`、`q` |
| GET | `/api/recipes/{recipe_id}` | 材料・基準人数・工程 |
| GET | `/api/state` | JWT本人の保存状態。未保存は `{version:0,snapshot:null}` |
| PUT | `/api/state` | `{expectedVersion,snapshot}` をCAS更新。競合時409 |

人数・材料量は料理選択後に変更するため検索条件にはありません。買い足し計算は端末の確定在庫を使うdomain機能に置き、公開APIへ個人の在庫を送信しません。

stateは端末AppStateをクラウドへ移す第一段階の境界です。外側 `version` はサーバーCAS版、内側 `snapshot.version` は端末の編集版で意味が異なります。既存の料理・食材・工程の正規化モデルを廃止する設計ではありません。

## 実行と検査

repo rootから実行します。

```bash
uv sync --locked --all-packages
uv run --locked --package recipeweave-api app-docs
uv run --locked --package recipeweave-api uvicorn app.main:app --reload
uv run --locked ruff format --check backend database
uv run --locked ruff check backend database
uv run --locked pyright --project backend/pyproject.toml
uv run --locked mypy --config-file backend/pyproject.toml backend/src backend/tests backend/tools database
uv run --locked --package recipeweave-api app-archlint
uv run --locked --package recipeweave-api app-docs --check
uv run --locked pytest backend/tests --cov=app --cov-branch --cov-report=term-missing
uv run --locked --package recipeweave-api python backend/tools/package_lambda.py --architecture x86_64
```

契約・署名検証・利用者隔離・同時更新・過大要求・型検証・SQL再現性のテスト成功をgateとし、branch coverageを報告します。未接続AWSの動作はcoverage率で代替しません。SQLGlot未取得の環境ではSQL生成・adapter検査を実施できず、`app-docs --check`が通るまでbackend配布は完了扱いにしません。

生成物: `openapi.gen.json`、各state operationの `generated/queries.py`。`generators.manual.json` が入力と出力を定義します。OpenAPIのみなら `app-docs --openapi-only` で再生成できます。これはSQLの検証を行ったことにはなりません。

## 接続設定

`STATE_BACKEND=disabled` が既定。ローカルmemoryを使う場合も `STATE_BACKEND=memory` と `ALLOW_MEMORY_STATE=true` の両方が必要です。認証省略機能はありません。

AWS設定は `STATE_BACKEND=dsql`、`COGNITO_ISSUER`、`COGNITO_CLIENT_ID`、`DSQL_HOST`、`DSQL_DATABASE_USER=recipeweave_app`。`AWS_REGION` はLambdaの予約環境変数を読み取ります。CORSを有効にする場合のみ `ALLOWED_ORIGINS` に明示したoriginをカンマ区切りで指定します。

Cognito JWTはRS256署名・issuer・expiry・issued-at・token_use=access・client_id・subを検証します。未知の署名鍵はJWKS再取得、鍵取得失敗は503、無効tokenは401です。`X-User-Id`を信頼しません。要求上限は1MiBで、chunked bodyもJSON解析前に検査します。画像・OCR全文・未知fieldは保存型に含めず、型エラーにも入力値を反射しません。

DSQLは各接続でIAM tokenを生成し、verify-full TLS、非admin role、引数束縛SQLを使用します。OCC再試行は最大3回。CAS失敗は再試行で上書きせず409。runtime roleへmigration権限を与えません。

Lambda assetは `backend/.build/lambda`、handlerは `app.handler.handler`。lockからLinux x86_64のPython 3.12依存を取得し、サンプルJSONと実装を梱包します。DockerやAWS接続は不要です。

## 設計と検証の限界

operation単位のrouter→functions→Protocol→provider境界を採用しています。SQLGlotのAST検査とruntime OpenAPIは決定的に生成します。portable CFGが扱えないループ・Protocolの動的dispatchを無理に線形化したsequence図は生成しません。

Starlette 1.xのhttpx/httpx2移行に対してテストは小さなHTTP Protocolを境界に持ちます。SDKの自動stubにないDSQL token生成メソッドもprovider内のProtocolへ閉じ込めています。アプリケーション本体の型検査を緩和していません。

実AWSでのCognito鍵ローテーション、IAM role mapping、Aurora DSQL migration/OCC、CloudFront/API Gateway統合は、AWS Dev接続を復旧した後に確認する必要があります。
