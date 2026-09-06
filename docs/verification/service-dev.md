# RecipeWeave Dev の検証・公開状況

更新日: 2026-09-06。対象ブランチ: `feat/service-receipts-dev`。

実装コミット `576353a75f28f6af7253bcda2bba7ae643bfcb78` の
[CI run 34001846587](https://github.com/tsuji-tomonori/RecipeWeave/actions/runs/34001846587) で、
**verifyジョブが成功した**。84テスト、型・lint、実Lambda梱包、CDK strict合成、
生成設計の差分検査、Pages用artifactの作成まで完了した。
publishジョブはPages未有効による `Get Pages site failed / Not Found` で停止した。
workflow全体の成功や、公開・AWS配備の完了は表明しない。

## 状況

サービス概要・利用者マニュアル・Q&A・画面一覧を独立した評価者で2回確認し、
レシート訂正・重複・取消・数量・保存の規則を確定した。
正本QNTには計42要件・80受入条件を持つ。生成と整合チェックは成功。
机上の評価を実ユーザーの使いやすさ実測とは扱わない。

| 検証対象 | 状態と証跡 |
|---|---|
| 利用者文書 | `docs/service/reviews/novice-review.md`、`receipt-review.md` に反復記録 |
| 実装と動線 | 独立レビューの重大4件・中3件を修正し再確認。表示位置保持も追加 |
| 数量・レシート・端末保存 | TypeScript strict、独立計算・保存23テスト成功 |
| Svelte画面 | 型・build成功、svelte-checkは0 errors / 0 warnings。疑似DOM11件＋計算・保存23件が成功 |
| FastAPI・移行 | 30テスト成功（API等26件、移行契約4件）。Ruff・Pyright・mypy・operation境界検査成功。backend branch coverageを含む集計85% |
| 既存の生成処理 | Pythonの12テスト成功 |
| AWS CDK | 実Lambda梱包、8構造検査、strict合成成功。参照保護をstrongと明示し、既定証明書に効かない設定を除いた |
| 実装由来の設計 | OpenAPI・SQL wrapper・サービス構成・生成処理設計を再生成して追跡版と一致。未追跡ファイルも含め差分なし |
| GitHub Pages | site artifact作成成功。publishはPages初期設定がないためNot Foundで停止。未公開 |
| AWS実環境 | 接続が再認証を要求。未配備、Cognito/DSQL実接続は未受入 |
| 実ブラウザ・実機 | この作業環境のローカルURL制限により未実施。疑似DOMテストと区別 |
| OCR一般精度 | 実店舗の多様なレシートによる精度測定は未実施。必ず確認・訂正を通す |

NodeのTesseract日本語エンジンと同梱モデルは、生成済みの操作画像22を使った
スモーク検査で195文字（うち日本語77文字）を認識した。実ブラウザのworker読込みや
実レシートの認識精度を示す試験ではなく、認識全文は記録していない。
利用者マニュアル7 HTMLのリンク・画像・日本語見出しanchorは検査済み。

## 再現

`.github/workflows/dev.yml` が、固定依存の導入、QNT整合、Svelte型・操作テスト、
Python lint/strict型/認証・CASテスト、Lambda梱包、CDK構造テスト・合成、
実装由来設計の差分確認、Pages配置を順に実行する。
検査が失敗したビルドは公開しない。AWSへの自動配備はこのworkflowに含めない。

生成物の差分検査は新規未追跡ファイルも検出する。初回CIの生成内容はSHA-256を照合して
所定の5ファイルだけを取り込み、コードと同じブランチへ記録した。
再検査で一致し、サービス設計に記載した17の入力ファイルハッシュも照合した。

pytestは依存するStarlette/TestClient由来の非推奨警告2件を出すが、テスト失敗はない。
これは実機受入や将来の依存更新での互換性を保証するものではない。

## 公開に必要な設定

リポジトリの [Pages設定](https://github.com/tsuji-tomonori/RecipeWeave/settings/pages) で
**Settings → Pages → Build and deployment → Source → GitHub Actions** を選ぶ。
その後、失敗したpublishジョブを再実行する。通常の `GITHUB_TOKEN` はPages初期有効化用の
管理権限を持たず、接続中のGitHubツールにも設定変更操作がないため、この初回設定を必要とする。

AWSは接続を再認証した後、`infra/README.md` と `database/README.md` に沿って
対象アカウント・リージョン、CDK bootstrap、DB role mappingとmigrationを確認して進める。
合成テンプレートの成功をAWSでの動作確認済みとは記録しない。
