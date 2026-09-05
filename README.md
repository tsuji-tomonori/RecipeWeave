# RecipeWeave

RecipeWeave is a Python 3.12+ workspace for deterministic recipe-combination generation and evaluation. The repository uses `uv` for Python dependency resolution and `moon` for project/task orchestration.

The initial implementation boundary is `packages/generator`. The directories `frontend`, `backend`, `database`, `infra`, `batch`, and `scripts` are reserved moon projects. Their READMEs describe future ownership; a reservation is not an implemented feature.

## Development

```bash
uv sync
uv run --package recipeweave-generator pytest packages/generator
uv run --package recipeweave-generator ruff check packages/generator
python3 tools/quintflow.py setup
python3 tools/quintflow.py generate
python3 tools/quintflow.py check
```

When moon 2.5.4 or later is installed, equivalent project tasks are available with `moon run generator:lint`, `moon run generator:test`, and `moon run generator:check`. The official moon release currently used for this bootstrap is 2.5.4; Python toolchain support remains marked unstable by moon, so commands explicitly invoke the repository's `uv`.

## Requirements and design authority

Durable requirements are authored only in [`spec/requirements/requirements.qnt`](spec/requirements/requirements.qnt). `tools/quintflow.py generate` derives `requirements.json` and `docs/requirements/REQUIREMENTS.md`; generated views must not be edited directly.

The as-built design entry point is [`docs/design/generated/README.md`](docs/design/generated/README.md). Future design output must be generated from implementation artifacts and checked for deterministic drift. Current requirements distinguish semantic food coverage from SKU concentration, require deterministic unique enumeration, full-output SHA256 manifests with resume state, raw-material quantities and process DAGs, train/holdout statistics, and blind independent Luna feasibility ratings kept separate from physical taste. The ten-million-item target is a future benchmark target and is not claimed as achieved.

Bulk external execution stays disabled by default. Any paid or large-scale run requires an explicit user-approved scope and a recorded cost estimate.
