# RecipeWeave

食材から料理を選び、分量・献立・調理を組み立てるWebアプリと、レシピ候補の列挙基盤です。
Devアプリは8品・35食品のサンプルで、レシートOCR、手持ち食材の検索、人数と材料量の変更、買い物集計、調理ガイドを扱います。
Devの個人データは利用中のブラウザに保存します。クラウド同期は提供していません。

- [Dev試用版を開く](https://tsuji-tomonori.github.io/RecipeWeave/)
- [サービス概要](docs/service/overview.md) / [図付き利用者マニュアル](docs/service/manual.md) / [Q&A](docs/service/faq.md)
- [画面と動線](docs/service/screens-and-flows.md) / [要件定義](docs/requirements/REQUIREMENTS.md)
- [採用構成と判断](docs/design/ADR-0001-service-dev.md) / [実装由来の設計一覧](docs/design/generated/README.md)
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
| `frontend` | 操作中心のWeb UI、日本語OCR、端末保存、数量計算 |
| `backend` | FastAPIの公開カタログAPIと認証付き状態API |
| `database` | DSQLの版付きマイグレーションと運用手順 |
| `infra` | CloudFront/S3、API Gateway/Lambda、DSQL、CognitoのCDK定義 |
| `data/samples` | Dev用8品・35食品。候補の全量出力とは別データ |
| `batch`, `scripts` | 将来のバッチ運用、補助スクリプトの配置先 |
| `spec`, `docs`, `tools` | 要件正本、生成設計書、dev-standardの管理ツール |

## セットアップと検証

リポジトリのルートで実行します。

Webアプリだけを試す場合は Node.js 24 で次を実行します。
レシートの認識データは初回ビルド時にnpmの固定依存から同梱し、画像をOCRサーバーへ送信しません。

```bash
npm ci --prefix frontend
npm run build --prefix frontend
npm run preview --prefix frontend
```

表示されたlocalhost URLを開きます。ZIP内のHTMLを直接開く方法ではOCRや端末保存は動作しません。
API・DSQL・AWSの起動と配備は [backend](backend/README.md)、[database](database/README.md)、[infra](infra/README.md) の手順を参照してください。
GitHub Actionsは型・テスト・生成差分・CDK合成を確認後にPagesへ配置します。AWSへは自動配備しません。

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
