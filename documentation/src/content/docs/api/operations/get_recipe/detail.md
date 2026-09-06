---
title: "詳細設計: get_recipe"
---

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

| 項目 | 仕様 |
|---|---|
| authentication | public |
| idempotency | 読取専用 |
| transaction | なし |
| effects | なし |

## 関数の責務

| 関数 | 責務 | 定義元 |
|---|---|---|
| get_recipe | 個別の説明なし。下記の実装を参照。 | backend/src/app/apis/recipes/get_recipe/router.py:20 |
| get_recipe | 料理として完成したサンプルを取得する。構造だけの生成候補は対象にしない。 | backend/src/app/apis/recipes/get_recipe/functions.py:5 |

## 依存解決の定義

```python
"""プロバイダーの構築と依存のキャッシュ。必要になるまでインポートしない。"""

from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.errors import AuthenticationError, ServiceUnavailableError
from app.core.settings import AppSettings
from app.integrations.auth.port import IdentityVerifier
from app.integrations.catalog.port import CatalogPort
from app.integrations.state.port import StateRepository

bearer = HTTPBearer(auto_error=False)


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()


@lru_cache
def get_catalog() -> CatalogPort:
    from app.integrations.catalog.json_provider import JsonCatalog

    settings = get_settings()
    packaged = Path(__file__).resolve().parents[1] / "sample_data"
    path = Path(settings.catalog_path) if settings.catalog_path else packaged
    if not path.is_dir():
        path = Path(__file__).resolve().parents[4] / "data" / "samples"
    return JsonCatalog(path)


@lru_cache
def get_verifier() -> IdentityVerifier:
    from app.integrations.auth.cognito_provider import CognitoVerifier

    settings = get_settings()
    return CognitoVerifier(settings.cognito_issuer, settings.cognito_client_id)


def require_subject(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> str:
    """利用者識別用のヘッダー・クエリ引数・未検証のJWTクレームを信頼しない。"""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError("access token required")
    return get_verifier().subject(credentials.credentials)


@lru_cache
def get_state_repository() -> StateRepository:
    settings = get_settings()
    if settings.state_backend == "memory" and settings.allow_memory_state:
        from app.integrations.state.memory_provider import MemoryStateRepository

        return MemoryStateRepository()
    if settings.state_backend == "dsql":
        from app.integrations.state.dsql_provider import DsqlStateRepository

        return DsqlStateRepository(settings)
    raise ServiceUnavailableError("state synchronization unavailable")


CatalogDependency = Annotated[CatalogPort, Depends(get_catalog)]
StateDependency = Annotated[StateRepository, Depends(get_state_repository)]
SubjectDependency = Annotated[str, Depends(require_subject)]
```

## 関連する仕様

[インターフェース](/RecipeWeave/quality/design/api/operations/get_recipe/interface/) / [シーケンス](/RecipeWeave/quality/design/api/operations/get_recipe/sequence/) / [SQL](/RecipeWeave/quality/design/api/operations/get_recipe/queries/) / [検証](/RecipeWeave/quality/design/api/operations/get_recipe/tests/)
