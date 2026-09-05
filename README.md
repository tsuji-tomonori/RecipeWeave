# RecipeWeave

食材・料理構造・味付け・調理経路から、レシピ生成に渡す組み合わせを決定的に列挙するプロジェクトです。
Python 3.12以上をuv workspace、プロジェクトとタスクをmoonrepoで管理します。

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
| `frontend`, `backend`, `database` | Web UI、API、DBの配置先を確保。製品機能は未実装 |
| `infra`, `batch`, `scripts` | インフラ、バッチ運用、補助スクリプトの配置先を確保 |
| `spec`, `docs`, `tools` | 要件正本、生成設計書、dev-standardの管理ツール |

## セットアップと検証

リポジトリのルートで実行します。

```bash
uv sync --locked
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
現在の設計は [`docs/design/generated/generator.md`](docs/design/generated/generator.md) に実装から生成します。

```bash
uv run python -m recipeweave_generator.design
uv run python -m recipeweave_generator.design --check
```

変更は要件・実装・関連する検証を対応させ、日本語のConventional Commits形式で記録します。
確認用標本を見て同じ版の規則を修正せず、次版・新しい標本・停止規則を事前固定して評価を続けます。
