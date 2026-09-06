"""APIと同じトランザクションを使うカタログプロバイダーを組み立てる。"""

from typing import Annotated

from fastapi import Depends

from app.core.db import DatabaseDependency
from app.integrations.catalog.port import CatalogPort
from app.integrations.catalog.postgres_provider import PostgresCatalog


def get_catalog(database: DatabaseDependency) -> CatalogPort:
    return PostgresCatalog(database)


CatalogDependency = Annotated[CatalogPort, Depends(get_catalog)]
