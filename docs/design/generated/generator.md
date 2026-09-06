# 実装由来の設計

生成元: Python AST。手編集禁止。

`uv run python -m recipeweave_generator.design` で再生成し、`--check` で差分検査。

| 実装ファイル | SHA-256 | 公開定義 |
|---|---|---|
| `packages/generator/src/recipeweave_generator/__init__.py` | `83a578037e405ccd42235c7b370d18b4066118f7ba202552f7c79d54ef7f8a07` |  |
| `packages/generator/src/recipeweave_generator/catalog.py` | `83e65847ea01781342c17b1dcee30cb9a1d511f01880d0dcdba28ce03fa3e444` | `compile_catalog`, `compile_files` |
| `packages/generator/src/recipeweave_generator/cli.py` | `cd9a8b74526796acb515b896fe3714dd76a762bcb6015e24a15fdfc3c4d2bc3f` | `main` |
| `packages/generator/src/recipeweave_generator/design.py` | `5365a4a14fc2cc4e64ed0e6edaef2285eaa6778efb2e6a34b69e9fe6a160dda5` | `render`, `main` |
| `packages/generator/src/recipeweave_generator/experiment.py` | `6fd7d332e301faae05b5ae359c6aa1cab9fe22cfd0aefa42469b7cbf9b513ca5` | `prepare` |
| `packages/generator/src/recipeweave_generator/export.py` | `bb420d551476e5c701aa26b6280386dadb6d247184a0c6a631b3b8962e59d0fe` | `file_hash`, `atomic_json`, `export_all`, `verify_all` |
| `packages/generator/src/recipeweave_generator/report.py` | `f5dd90a0a62aff852495b4d8edf334c88087133fc252a9a2814c26ba5770fd0f` | `build_report`, `main` |
| `packages/generator/src/recipeweave_generator/space.py` | `5e8c9720ce5c6158f9d6e15c29828f1fdef0640ea8059d97951a3cacc26cce2d` | `canonical`, `unrank`, `Segment`, `Space` |
| `packages/generator/src/recipeweave_generator/statistics.py` | `9f6d71d3570a128588e2958cf6bcf8e39c95911177d6ffe9ca208727968d3528` | `wilson_interval`, `newcombe_difference_interval`, `compare_proportions`, `analyze` |

## 境界

| ディレクトリ | 現在の役割 |
|---|---|
| `frontend` | Svelte画面・端末保存・レシートOCR・数量計算 |
| `backend` | FastAPI・カタログAPI・認証付き状態API |
| `database` | DSQLマイグレーションと運用手順 |
| `infra` | AWS CDKによる配備定義 |
| `batch` | moonプロジェクトの場所を確保。製品機能は未実装 |
| `scripts` | moonプロジェクトの場所を確保。製品機能は未実装 |

コードの存在に基づく列挙。サービス詳細は [service.md](service.md)、
実際の検証・公開状況はサービス受入記録で確認する。
