"""公開用の接続設定について、有無だけを残し未配備を実装済みと区別する。"""

import json
import os
from pathlib import Path

CHECKS = {
    "DEV_API_BASE_URL": ("VITE_API_BASE_URL", "Pagesから接続する実APIのHTTPS URL"),
    "DEV_COGNITO_DOMAIN": ("VITE_COGNITO_DOMAIN", "Dev用Cognitoログインドメイン"),
    "DEV_COGNITO_CLIENT_ID": ("VITE_COGNITO_CLIENT_ID", "Dev用Cognito公開クライアントID"),
    "AWS_DEPLOY_ROLE_ARN": ("AWS_DEPLOY_CONFIGURED", "既存のAWS配備ロール"),
    "PRODUCTION_WEB_CALLBACK_URL": (
        "PRODUCTION_CALLBACK_CONFIGURED",
        "本番画面の正確なHTTPS戻り先URL",
    ),
}


def main() -> None:
    results = []
    for name, (variable, purpose) in CHECKS.items():
        value = os.environ.get(variable, "")
        configured = value == "true" if variable.endswith("_CONFIGURED") else bool(value)
        results.append({"name": name, "configured": configured, "purpose": purpose})
    report = Path(__file__).resolve().parents[1] / "reports/deployment-readiness.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        json.dumps(
            {
                "commit": os.environ.get("GITHUB_SHA", "local"),
                "checks": results,
                "note": (
                    "設定値の存在を確認した記録です。実API到達・AWS配備成功の証明ではありません。"
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    missing = [str(item["name"]) for item in results if not item["configured"]]
    print("公開接続設定: " + ("未設定 " + ", ".join(missing) if missing else "すべて指定済み"))


if __name__ == "__main__":
    main()
