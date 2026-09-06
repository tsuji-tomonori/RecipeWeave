# 要因別単体テスト仕様: entity_menu_item_create

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

| 要因 | Given: 前提 | When: 操作 | Then: 期待結果 | 実在テストnode |
|---|---|---|---|---|
| 料理版参照の事前認可 | 未公開版への既存本人履歴がなくローカル試用条件もない | 献立明細・提案履歴を書き込む | 書込みSQLより前に403を返し履歴の後付けによる権限取得を防ぐ | backend/tests/test_entity_api.py::test_recipe_history_reference_is_verified_before_write |
| 実DBの履歴認可境界 | 署名済みの2利用者と未公開・取下げの料理版 | 履歴の追加・取下げ後の再参照を要求 | 新規の権限取得は拒否し既存本人履歴だけを復元できる | backend/tests/test_entity_api_db.py::test_history_cannot_be_created_to_gain_unpublished_recipe_access |

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_entity_api_db.py::test_real_child_reference_cannot_use_other_users_menu | Given別人の献立IDと有効なレシピ When明細作成 Then所有者FK経路で403。 | assert created.status_code == 201, created.text / assert versions.status_code == 200 and versions.json(), versions.text / assert recipe.status_code == 200, recipe.text / assert attempted.status_code == 403, attempted.text / assert deleted.status_code == 200 |

宣言応答: 201, 401, 403, 409, 422, 503
