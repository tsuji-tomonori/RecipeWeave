"""本番公開と分離した、未試作カタログの開発環境許可。"""

from app.core.dependencies import get_settings
from app.core.identity import local_auth_enabled


def catalog_preview_enabled() -> bool:
    """環境の許可だけを判定する。呼出側は別途署名検証済み利用者を必須にする。"""
    settings = get_settings()
    if settings.environment not in {"dev", "local", "test"}:
        return False
    return settings.allow_catalog_preview or local_auth_enabled()
