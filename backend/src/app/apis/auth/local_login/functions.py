from app.core.auth_service import LoginRequest, LoginResponse, local_login


def execute(request: LoginRequest) -> LoginResponse:
    """開発環境へログインする。秘密情報はログへ出力しない。"""
    return local_login(request)
