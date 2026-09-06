---
title: "検証仕様: get_state"
---

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_api.py::test_state_requires_real_bearer_and_ignores_user_header | 明示URLを呼び出すテスト | assert response.status_code == 401 / assert 'WWW-Authenticate' in response.headers |
| backend/tests/test_api.py::test_conditional_write_conflict_and_user_isolation | 明示URLを呼び出すテスト | assert response.status_code == 200 / assert response.json()['version'] == 1 / assert response.json()['snapshot']['version'] == 3 / assert client.put('/api/state', headers=headers, json=body).status_code == 409 / assert repository.get('user-a').version == 1 / assert client.get('/api/state', headers=other).json() == {'version': 0, 'snapshot': None} / assert client.get('/api/state', headers=headers).json()['version'] == 1 |

宣言応答: 200, 401, 503
