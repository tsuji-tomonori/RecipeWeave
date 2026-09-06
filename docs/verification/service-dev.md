# RecipeWeave Dev の検証・公開状況

更新日: 2026-09-06。対象ブランチ: `feat/service-receipts-dev`、PRの取り込み先: `dev`。

## 今回の実装

元スプレッドシートの71表をDDLへ実装した。レシート・在庫消費・復元確認等の運用9表、旧互換表と移行台帳を含む物理82表から、設計書を自動生成する。業務80表の型付き操作と認証・検索・画面用の業務APIを実OpenAPIから列挙し、330操作を生成した。

レシピ8品、食品1,018件、材料、工程、分類は初期投入用データであり、実行中のAPIはPostgreSQLから取得する。初期料理は未試作で、公開・検証済みへ変更していない。利用者の在庫・レシート・献立・調理履歴は、認証済み本人の正規化テーブルに保存する。

## 実行した検証

| 対象版と実行 | 結果と範囲 |
|---|---|
| `0ab65d9`・[実DB CI 34025093894](https://github.com/tsuji-tomonori/RecipeWeave/actions/runs/34025093894) | 初回の実PostgreSQL検証118件成功、スキップ0件。管理用接続で移行し、非管理者・RLS有効のアプリ接続でAPIを実行 |
| `dfeb67f5`・[実DB CI 34026452442](https://github.com/tsuji-tomonori/RecipeWeave/actions/runs/34026452442) | 142件成功・2件失敗。試験のHTTPメソッドと、献立内役割の保存不足を検出。後続版で修正 |
| `1acc6a4`・[実DB CI 34026790719](https://github.com/tsuji-tomonori/RecipeWeave/actions/runs/34026790719) | **145件成功・スキップ0件**。全表・外部キー・公開後不変・所有権・CRUD、初期データ、レシート取消、在庫、献立、調理完了、版を固定した履歴、Cognito初回登録を確認 |
| `1acc6a4`・[総合CI 34026790738](https://github.com/tsuji-tomonori/RecipeWeave/actions/runs/34026790738) | Python716件成功・1件失敗、Vitest48件成功、利用画面14件失敗・2件成功、品質画面4件成功・2件失敗。DB接続の試験差替え対象、ログイン後の読込、検索入力の待機条件を調査・修正。公開は失敗ゲートにより未実行 |
| ローカルの型・SQL・生成検査 | SQLFluff507ファイルで違反0件。Ruff・Pyright strict・mypy strict、Quint生成差分、API配置・生成差分を確認。実行ごとの最終結果はCI成果物を参照 |
| ローカルの設計・品質サイト検査 | 生成・証跡関連45試験成功。直前版の設計2,353ファイル、Starlight2,036ページ、70,758リンク・参照資源を検査。追加後の生成設計は2,404ファイル。閲覧UIの合格を静的検査から推測しない |
| `8fe62ae`・[独立ブラウザCI 34029055375](https://github.com/tsuji-tomonori/RecipeWeave/actions/runs/34029055375) | APIは200で本人データを返す一方、URLのみホームへ移動してDOMがログイン画面に残る不具合を確認。追跡により、ランダム料理APIの応答を料理本体と誤解して描画中に停止する直接原因を確認。応答の展開・候補ゼロ処理を修正。アプリ内遷移の同期も改善し、関連13単体試験成功。修正後の実ブラウザは次CIで確認 |
| `0a3a9bf`・[実DB CI 34029672097](https://github.com/tsuji-tomonori/RecipeWeave/actions/runs/34029672097) | 173件成功・2件失敗・14件setupエラー・スキップ0件。バックアップ5件はすべて成功。残りは試験用の旧参照名2件と、工程試験fixtureの必須役割設定漏れ14件を修正 |
| PC・モバイルの実ブラウザ | 現行版の全利用動線と品質サイトの成功はCIで確認中。ローカルChromiumはOSのsocket権限により起動前に停止し、そこで実画面検証に成功したとは記録しない |
| `0387ded`・[実DB CI 34031436919](https://github.com/tsuji-tomonori/RecipeWeave/actions/runs/34031436919) | **189件成功・スキップ0件**。34表のバックアップ復元、所有権、復元競合と原子性、人数変更時の工程時間確認を含む |
| `0387ded`・[独立ブラウザCI 34031436926](https://github.com/tsuji-tomonori/RecipeWeave/actions/runs/34031436926) | **PC・モバイル22件成功**。検索から3人分への変更、時間確認、調理完了、レシートOCR・取消、別タブ、復元を確認 |
| `0387ded`・[総合CI 34031436929](https://github.com/tsuji-tomonori/RecipeWeave/actions/runs/34031436929) | Python806件、Vitest57件、CDK9件、品質サイト6件成功。SQLFluff703ファイルで違反0件、生成設計2,404ファイル差分なし、Mermaid1,736図を検証。Ruffの生成説明文8行の長さ超過と、設定の器具返却順が揺れるE2E1件を検出し、公開を停止。後続修正は最新のPR・CI成果物で確認する |

## 証跡と再現

`.github/workflows/relational.yml` は、PostgreSQL16とpgvector、実DDL移行、初期投入、非管理者接続での制約・API試験を行う。CIで必要なDB設定がなければ失敗し、必須試験のスキップを成功として扱わない。

`.github/workflows/dev.yml` は、静的解析・型・単体/実DB試験の後、同じ移行と初期データを別のE2E用DBへ適用し、実APIと画面を起動する。PC・モバイルのGiven/When/Then、各操作の実画面、失敗trace、JUnit、カバレッジ、SQL診断、終了コードを品質成果物へ保存する。設計サイトの検索・ER/シーケンス描画・画像拡大もブラウザで検証する。

新しいPages成果物は必要な全検査が成功したときだけ公開する。公開配置はアプリをルート、品質証跡を `quality/`、検索可能な設計書を `quality/design/` とする。生成設計の元入力とSHA-256は `docs/design/generated/MANIFEST.md` を参照する。

## 実配備の境界

`dfeb67f5`、`1acc6a4`、`0387ded` のCIは、`DEV_API_BASE_URL`、`DEV_COGNITO_DOMAIN`、`DEV_COGNITO_CLIENT_ID`、`AWS_DEPLOY_ROLE_ARN`、`PRODUCTION_WEB_CALLBACK_URL` の全5設定が未設定だったことを記録した。値の内容は成果物へ出力しない。

AWS接続への読み取り専用STS照会は応答を取得できず、認証状態・アカウント・既存stack・実APIの存在を確認できていない。明示的な再認証要求や権限エラーも受け取っていない。AWS実配備を完了とは記録しない。

Pagesは静的画面と証跡の公開であり、DB/APIのホスティングではない。API未設定時は未接続状態を表示する。Cognito・Aurora PostgreSQL・APIの実配備、1,000万料理の負荷、料理の試作、実店舗レシートの一般精度、スマートフォン実機のカメラ/バックグラウンド動作は、それぞれ別の実測が必要である。

## 以前のPages公開記録

旧ブラウザ保存版 `bf8a0c3` の [CI run 34002028247・attempt3](https://github.com/tsuji-tomonori/RecipeWeave/actions/runs/34002028247/attempts/3) はverify・publishが成功した。当時の基本表示確認は、今回の正規化DB版の受入結果へ転用しない。

所有者がPagesのSourceをGitHub Actionsとし、公開許可に `feat/*` を追加した経緯がある。公開先は [RecipeWeave Dev](https://tsuji-tomonori.github.io/RecipeWeave/) 。環境保護の解除や回避は行わない。
