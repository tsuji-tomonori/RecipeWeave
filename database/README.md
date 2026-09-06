# Aurora DSQL migration boundary

`recipeweave.user_state(subject,revision,payload,updated_at)` は端末データ同期の初期境界です。1000万料理向けの正規化モデル・候補生成データを置換しません。レシート画像、OCR全文、購入店情報はこのsnapshotへ保持しません。

`migrations/manifest.manual.json` とSQLを入力に、SQL構文・1ファイル1文・checksumを検査します。計画表示はAWS不要です。

```bash
uv run --locked --package recipeweave-api python database/migrate.py --plan
```

`--apply` は専用migration IAM roleを通常のAWS認証手順でassumeした後だけ実行します。必要設定は `DSQL_HOST`、`AWS_REGION`、`DSQL_APP_IAM_ARN`。runtime Lambdaと異なるroleに対象clusterへの `dsql:DbConnectAdmin` を付与します。runtime roleは `dsql:DbConnect` のみです。

```bash
uv run --locked --package recipeweave-api python database/migrate.py --apply
```

DDLをautocommitの1文1transactionで実行し、履歴DMLは別transactionへ分けます。再実行時はchecksum一致とpostconditionを検査し、途中でDDLのみ確定した場合も構造確認後に履歴を記録します。不一致は停止し、成功したmigrationを後から書き換えません。

将来 `kind=index` を追加した場合は `CREATE INDEX ASYNC` のjobを `sys.wait_for_job` で待ち、成功とpostconditionを確認してから記録します。現時点のアクセスはsubject主キーだけなので不要な副索引を作りません。新しい外部キーを使うmigrationは対応機能を確認して追加します。

application roleは `recipeweave_app`、`user_state` のSELECT/INSERT/UPDATEだけを付与します。migration ledgerへの書込み権限やadmin権限をアプリに渡しません。

実DSQLは未プロビジョニングです。DDL、role付与、OCC、障害復旧はAWS Devに対する適用試験を経る必要があります。

参照: [IAM認証と権限](https://docs.aws.amazon.com/aurora-dsql/latest/userguide/authentication-authorization.html)、[TLS検証](https://docs.aws.amazon.com/aurora-dsql/latest/userguide/configure-root-certificates.html)、[非同期索引](https://docs.aws.amazon.com/aurora-dsql/latest/userguide/working-with-create-index-async.html)、[Cognito JWT検証](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html)。
