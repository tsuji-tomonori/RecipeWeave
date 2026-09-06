from app.core.auth_service import UserProfile, profile
from app.core.identity import Identity


def execute(identity: Identity) -> UserProfile:
    """本人のプロフィールを取得する。秘密情報はログへ出力しない。"""
    return profile(identity)
