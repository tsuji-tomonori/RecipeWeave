# 実装由来の設計

生成元: Python AST。手編集禁止。

`uv run python -m recipeweave_generator.design` で再生成し、`--check` で差分検査。

| 実装ファイル | SHA-256 | 公開定義 |
|---|---|---|
| `packages/generator/src/recipeweave_generator/__init__.py` | `83a578037e405ccd42235c7b370d18b4066118f7ba202552f7c79d54ef7f8a07` |  |
| `packages/generator/src/recipeweave_generator/catalog.py` | `83e65847ea01781342c17b1dcee30cb9a1d511f01880d0dcdba28ce03fa3e444` | `compile_catalog`, `compile_files` |
| `packages/generator/src/recipeweave_generator/cli.py` | `efd21f79fc20f67471ffdc83d28142de941de4266c9e99eb2a439a27c20a6239` | `main` |
| `packages/generator/src/recipeweave_generator/design.py` | `1d7291ad32c2d6aa465282f03284574cc79b2f52ddd83580408f74565e18a228` | `render`, `main` |
| `packages/generator/src/recipeweave_generator/experiment.py` | `6fd7d332e301faae05b5ae359c6aa1cab9fe22cfd0aefa42469b7cbf9b513ca5` | `prepare` |
| `packages/generator/src/recipeweave_generator/export.py` | `798d1eb3318b9c3995914fafc470255ea5703a783170b9297c81607970e5ec1d` | `file_hash`, `atomic_json`, `export_all`, `verify_all` |
| `packages/generator/src/recipeweave_generator/report.py` | `1f08d827025a0000fcd0da40525853af0a8b0809ac994340fc9a96a5356a974d` | `build_report`, `main` |
| `packages/generator/src/recipeweave_generator/space.py` | `5e8c9720ce5c6158f9d6e15c29828f1fdef0640ea8059d97951a3cacc26cce2d` | `canonical`, `unrank`, `Segment`, `Space` |
| `packages/generator/src/recipeweave_generator/statistics.py` | `9f6d71d3570a128588e2958cf6bcf8e39c95911177d6ffe9ca208727968d3528` | `wilson_interval`, `newcombe_difference_interval`, `compare_proportions`, `analyze` |

## 境界

| ディレクトリ | 現在の役割 |
|---|---|
| `frontend` | moonプロジェクトの場所を確保。製品機能は未実装 |
| `backend` | moonプロジェクトの場所を確保。製品機能は未実装 |
| `database` | moonプロジェクトの場所を確保。製品機能は未実装 |
| `infra` | moonプロジェクトの場所を確保。製品機能は未実装 |
| `batch` | moonプロジェクトの場所を確保。製品機能は未実装 |
| `scripts` | moonプロジェクトの場所を確保。製品機能は未実装 |

実装の列挙であり、数量計算・工程DAG・検索API・インフラが実装済みという意味ではない。
