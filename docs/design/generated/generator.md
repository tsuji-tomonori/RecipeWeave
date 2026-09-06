# 実装由来の設計

生成元: Python AST。手編集禁止。

`uv run python -m recipeweave_generator.design` で再生成し、`--check` で差分検査。

| 実装ファイル | SHA-256 | 公開定義 |
|---|---|---|
| `packages/generator/src/recipeweave_generator/__init__.py` | `0e04a31a98b495307491f8911266b146988fc01e8f1132f29238fb01ff6a7c83` |  |
| `packages/generator/src/recipeweave_generator/catalog.py` | `0923eed508975051fc1efc39ca493af9e0227d1a365415ebb5dfafdae91d4ee7` | `compile_catalog`, `compile_files` |
| `packages/generator/src/recipeweave_generator/cli.py` | `e4d5efc18d8675cdc9a67bb00c31c66ac531520d23a3865e53d40b95a34e39cb` | `main` |
| `packages/generator/src/recipeweave_generator/design.py` | `95663bd8c2cbe809bdb9c3827b26861f4eb2b6abc3f764247194b68d062de50d` | `render`, `main` |
| `packages/generator/src/recipeweave_generator/experiment.py` | `249333ee87d705842e7406ae82911ad687776a32dccc101f91fbd32c80a43289` | `prepare` |
| `packages/generator/src/recipeweave_generator/export.py` | `647781545c109f11e67cddfab6903a51812326c59029a0e156b475aca6a37e9e` | `file_hash`, `atomic_json`, `export_all`, `verify_all` |
| `packages/generator/src/recipeweave_generator/report.py` | `be9ebd43d4ed052c474ee2b686c522ab282789d02feca9eb35bb9b98b7a58a47` | `build_report`, `main` |
| `packages/generator/src/recipeweave_generator/space.py` | `79f5bea99134631a7781775442ab14cbb9a8a3e50ca1807eb786df13bd1eddec` | `canonical`, `unrank`, `Segment`, `Space` |
| `packages/generator/src/recipeweave_generator/statistics.py` | `7a67a6bdfb7d57475f63f6e8f5a631665ca89f1a24ab7cf898ca5a5b8f5c16d2` | `wilson_interval`, `newcombe_difference_interval`, `compare_proportions`, `analyze` |

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
