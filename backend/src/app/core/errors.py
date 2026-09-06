"""アプリケーションエラーに外部サービスの応答や利用者データを含めない。"""


class StateConflictError(Exception):
    """期待した版が保存されている版と一致しない。"""


class ServiceUnavailableError(Exception):
    """必要なプロバイダーまたは安全な接続設定を利用できない。"""


class AuthenticationError(Exception):
    """アクセストークンが指定されていないか、検証に失敗した。"""
