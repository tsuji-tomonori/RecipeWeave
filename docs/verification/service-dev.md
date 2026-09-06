# RecipeWeave Dev の検証・公開状況

更新日: 2026-09-06。対象ブランチ: `feat/service-receipts-dev`。

## 状況

サービス概要・利用者マニュアル・Q&A・画面一覧を独立した評価者で2回確認し、
レシート訂正・重複・取消・数量・保存の規則を確定した。
正本QNTには計42要件・80受入条件を持つ。生成と整合チェックは成功。
机上の評価を実ユーザーの使いやすさ実測とは扱わない。

| 検証対象 | 状態と証跡 |
|---|---|
| 利用者文書 | `docs/service/reviews/novice-review.md`、`receipt-review.md` に反復記録 |
| 実装と動線 | `docs/service/reviews/implementation-ux-review.md` の指摘を修正中 |
| 数量・レシート・端末保存 | TypeScript strict、独立計算・保存23テスト成功 |
| Svelte画面 | 型検査・production build成功。疑似DOMの操作テストを修正中 |
| FastAPI | ローカルAPI・認証など21テスト成功。SQL生成を含む全体はCI確認待ち |
| AWS CDK | 型・lint・Data/OIDC/config 3テスト成功。実Lambdaを使う5テストと全体合成はCI待ち |
| 実装由来の設計 | OpenAPI生成済み。SQL wrapperとCDKを含む全体生成・差分確認はCI待ち |
| GitHub Pages | 初期設定未完了。現連携から設定を変更できないため未公開 |
| AWS実環境 | 接続が再認証を要求。未配備、Cognito/DSQL実接続は未受入 |
| 実ブラウザ・実機 | この作業環境のローカルURL制限により未実施。疑似DOMテストと区別 |
| OCR一般精度 | 実店舗の多様なレシートによる精度測定は未実施。必ず確認・訂正を通す |

## 再現

`.github/workflows/dev.yml` が、固定依存の導入、QNT整合、Svelte型・操作テスト、
Python lint/strict型/認証・CASテスト、Lambda梱包、CDK構造テスト・合成、
実装由来設計の差分確認、Pages配置を順に実行する。
検査が失敗したビルドは公開しない。AWSへの自動配備はこのworkflowに含めない。

生成物の差分検査は新規未追跡ファイルも検出する。初回CIの生成内容を確認して
コードと同じブランチへ記録した後、再検査で一致を確認する。

## 公開に必要な設定

リポジトリの **Settings → Pages → Build and deployment → Source → GitHub Actions** を選ぶ。
その後、失敗したpublishジョブを再実行する。通常の `GITHUB_TOKEN` はPages初期有効化用の
管理権限を持たず、接続中のGitHubツールにも設定変更操作がないため、この初回設定を必要とする。

AWSは接続を再認証した後、`infra/README.md` と `database/README.md` に沿って
対象アカウント・リージョン、CDK bootstrap、DB role mappingとmigrationを確認して進める。
合成テンプレートの成功をAWSでの動作確認済みとは記録しない。
