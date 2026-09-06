# RecipeWeave

食材から料理を選び、分量・献立・調理を組み立てるWebアプリと、レシピ候補の列挙基盤です。
食材・レシピ・材料・工程・在庫・献立はPostgreSQLの各テーブルからAPIで読み書きします。
レシートOCR、手持ち食材の検索、人数と材料量の変更、買い物集計、設備と工程依存を考慮する調理ガイドを扱います。
個人データは認証した利用者に関連づけてDBへ保存し、更新版によって同時編集の上書きを防ぎます。
本人データの書出しと、内容・対象件数・全置換の確認を経た復元を提供します。
人数変更で時間確認が必要な工程は、基準人数の参考値と区別した利用者の目安を受け取り、段取りへ反映します。

原設計の71表に業務上の補完7表とバックアップ用台帳2表を実装し、旧移行互換表と移行台帳を含む物理表は82表です。
初期データ生成器の出力は食品1,018件、軸72件、軸候補995件、料理8品です。
8品は未試作の開発用下書きとしてDBへ投入し、試用を許可した開発環境へログインした場合だけ閲覧します。
Cognitoを使うDev環境ではAPIに `ALLOW_CATALOG_PREVIEW=true`、画面のビルドに `VITE_CATALOG_PREVIEW=true` を明示します。本番APIではこれらの設定に関係なく拒否します。
ローカル・テスト環境は既存の開発用認証設定でも試用できます。一般公開済みの品質を意味しません。

- [Pagesのフロント画面](https://tsuji-tomonori.github.io/RecipeWeave/)
- [品質レポート](https://tsuji-tomonori.github.io/RecipeWeave/quality/) / [検索できる生成設計書](https://tsuji-tomonori.github.io/RecipeWeave/quality/design/)
- [サービス概要](docs/service/overview.md) / [図付き利用者マニュアル](docs/service/manual.md) / [Q&A](docs/service/faq.md)
- [画面と動線](docs/service/screens-and-flows.md) / [要件定義](docs/requirements/REQUIREMENTS.md)
- [現行構成と判断](docs/design/ADR-0002-relational-service.md) / [実装由来の設計一覧](docs/design/generated/README.md)
- [Dev検証・公開状況](docs/verification/service-dev.md)

Svelte 5 / TypeScript / Vite、Python 3.12 / FastAPI、AWS CDKを使用します。
Python依存はuv workspace、プロジェクトとタスクはmoonrepoで管理します。

## レシピ候補の列挙基盤

現行v3は **12,069,539件の候補を全量出力**しています。めんつゆ2/3/4倍は1つの食品IDに統合し、濃縮倍率を商品属性として保持します。
食品1,005入力を936食品IDへ整理し、用途と適合規則を整備した248主材・副材と21料理テンプレートを採用しました。
カップ焼きそばなどの完成品アレンジも対象です。分量・工程を持つ完成レシピの1,000万件達成を意味しません。

- [食品カタログと適合規則](data/catalog/README.md)
- [全量CSV・辞書・検証マニフェスト](data/exports/README.md)
- [Luna複数評価者による統計確認結果と限界](docs/research/combination-feasibility-v3.md)
- [事前固定した評価プロトコル](experiments/PROTOCOL.md)

確認用に旧版・改良版から各400件を抽出し、各件を2つのLunaコンテキストで評価しました。
両者が成立見込みありとした割合は旧版41.0%、改良版99.5%です。これはモデル判定であり、実調理・人間評価・完成レシピ間の近似重複の検証は今後必要です。

## ディレクトリ

| パス | 役割と現在の状態 |
|---|---|
| `packages/generator` | 実装済みの正規化・列挙・全量出力・標本抽出・統計集計 |
| `data/catalog` | 組み合わせ元と適合規則、旧版・現行版定義 |
| `data/exports` | 全量出力と辞書・チェックサム |
| `experiments` | 開発用標本・独立確認標本・評価結果・再現情報 |
| `frontend` | 操作中心のWeb UI、日本語OCR、認証付きAPI接続、数量計算 |
| `backend` | FastAPIのカタログ・各表・在庫・献立・レシート・調理API |
| `database` | PostgreSQLの全表DDL、RLS、制約、版付き移行、正規化した初期データ |
| `infra` | Aurora PostgreSQL、API Gateway/Lambda、Cognito、移行専用LambdaのCDK定義 |
| `data/samples` | 初期料理の元データ。DB投入時に元カタログへ対応づけ、公開APIはこのJSONを直接読まない |
| `documentation` | CornellNoteWebv2に合わせたStarlight・全文検索付き設計サイト |
| `batch`, `scripts` | 将来のバッチ運用、補助スクリプトの配置先 |
| `spec`, `docs`, `tools` | 要件正本、生成設計書、dev-standardの管理ツール |

## セットアップと検証

リポジトリのルートで実行します。

ローカルでDB・API・画面をまとめて起動します。Docker Composeが必要です。

```bash
docker compose up --build
```

画面は `http://localhost:5173`、APIは `http://localhost:8000` です。
ComposeはDBの起動確認後、移行・初期データ投入を完了させてからAPIと画面を起動します。
ローカルではユーザー名 `alice`、共通パスワード `recipeweave-local` を入力してログインします。
Composeに固定した接続情報はローカル開発専用です。AWS環境の認証はCognitoの設定に従います。

レシートの認識データは固定npm依存から同梱し、画像はブラウザ内で認識します。
確認して登録した食材・数量等をAPIへ送り、元画像やOCR全文は保存しません。
初期データの再現件数は `uv run python database/seed.py --dry-run` で確認できます。

Pagesはフロント画面と品質・設計レポートを配信します。APIやDBは別の実行環境です。
API接続先・認証の設定と実配備が完了するまでは、Pagesの表示だけでサービス全体の利用開始を意味しません。
接続失敗時は画面にエラーを示し、ブラウザ内のサンプルへ切り替えて成功したようには表示しません。

詳しい実行・接続設定は [backend](backend/README.md)、[database](database/README.md)、[infra](infra/README.md) を参照してください。
GitHub Actionsは型検査・実DBテスト・E2E証跡・生成差分・CDK合成を検査し、成功した成果物をPagesへ公開します。
AWSへの実配備とCognito実ログインの受入結果は別途確認が必要です。合成成功を実配備成功として扱いません。

```bash
uv sync --locked --all-packages
npm ci --ignore-scripts
uv run pre-commit install
npm run moon:check
uv run pre-commit run --all-files
python3 tools/quintflow.py setup
python3 tools/quintflow.py generate
python3 tools/quintflow.py check
```

公式 `@moonrepo/cli` を2.5.4で固定しています。moonからuvを明示的に呼ぶ構成で、`generator:check` はlint・pytest・生成設計書の差分を確認します。

```bash
uv run recipeweave compile
uv run recipeweave count
uv run recipeweave show --ordinal 5182376
uv run recipeweave export --output data/exports/v3 --shard-size 1000000
uv run recipeweave verify-export --output data/exports/v3 --definition data/catalog/v3_reviewed.json
uv run python -m recipeweave_generator.report
```

exportは定義と完了シャードのチェックサムを照合して再開します。reportは保存された評価を集計し、モデル呼び出しは行いません。
探索にはordinalの直接復元を使い、旧候補空間をメモリ上に展開せず無作為抽出できます。

## 開発の正本

`dev-standard` のportable skillとpre-commit設定を取り込みました。適用記録は `.dev-standard/install/receipt.json` にあります。
要件は [`spec/requirements/requirements.qnt`](spec/requirements/requirements.qnt) を編集し、`quintflow.py generate` でJSONとMarkdownへ変換します。
生成器の設計は [`docs/design/generated/generator.md`](docs/design/generated/generator.md)、
サービス設計は [生成設計書一覧](docs/design/generated/README.md) に実装から生成します。
テーブル仕様・ER図・API別仕様・CRUD・シーケンスの生成方法は [自動生成手順](docs/design/AUTOMATION.md) を参照してください。

```bash
uv run python -m recipeweave_generator.design
uv run python -m recipeweave_generator.design --check
```

変更は要件・実装・関連する検証を対応させ、日本語のConventional Commits形式で記録します。
確認用標本を見て同じ版の規則を修正せず、次版・新しい標本・停止規則を事前固定して評価を続けます。
