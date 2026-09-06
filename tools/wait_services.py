"""ローカルAPIと画面が応答するまで、上限付きで起動を待つ。"""

import time
import urllib.error
import urllib.request


def main() -> None:
    for url in ("http://127.0.0.1:8000/api/health", "http://127.0.0.1:5173"):
        deadline = time.monotonic() + 60
        while True:
            try:
                with urllib.request.urlopen(url, timeout=2) as response:
                    if response.status == 200:
                        break
            except (OSError, urllib.error.URLError):
                if time.monotonic() >= deadline:
                    raise RuntimeError("サービスが制限時間内に起動しませんでした") from None
                time.sleep(1)


if __name__ == "__main__":
    main()
