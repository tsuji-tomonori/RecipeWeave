# 要因別単体テスト仕様: restore_backup

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

| 要因 | Given: 前提 | When: 操作 | Then: 期待結果 | 実在テストnode |
|---|---|---|---|---|
| 旧形式・欠落表・監査混入 | 形式1または必須表欠落の本文 | 形式2の型検証 | SQLを実行する前に入力を拒否する | backend/tests/test_backup_api.py::test_backup_requires_complete_table_set_and_current_format |
| numeric精度 | numeric(20,6)境界に近い小数 | 正規化JSON往復 | Decimalとdigestが完全一致する | backend/tests/test_backup_api.py::test_decimal_precision_survives_canonical_backup_round_trip |
| 真正性・本人限定 | 別人または未発行の本文 | 所有者と発行根拠を照合 | 管理者でも403を返す | backend/tests/test_backup_api.py::test_export_proof_and_owner_are_required_even_for_admin |
| 最終確認必須 | 未確認または現在版なしの入力 | 復元要求を型検証 | SQL前に拒否する | backend/tests/test_backup_api.py::test_restore_requires_explicit_confirmation_and_revision |
| 列の保持 | 34表のDDLメタデータ | 生成された復元列と照合 | ID・時刻・追加列を含む全列が一致する | backend/tests/test_backup_api.py::test_backup_column_sets_match_current_physical_schema |
| 全表往復・精度・隔離 | 私有食品・未知数量・大きい正確な小数 | preview後の全置換 | 全業務列が同値で共有・別人に変更がない | backend/tests/test_backup_database.py::test_backup_database_round_trip_preserves_complete_rows_and_decimal |
| 改竄・別人・競合・単回確認 | 発行済みバックアップと現在版 | 改竄・他人・古い版・再送で復元 | 現在データを変更せず拒否する | backend/tests/test_backup_database.py::test_backup_database_tamper_foreign_owner_cas_and_single_use |
| 原子的取消し | 置換・確認消費・版更新後 | 監査追記で実DB例外 | 全業務行・版・確認消費がロールバックされる | backend/tests/test_backup_database.py::test_backup_database_late_failure_rolls_back_rows_revision_and_intent |
| 過去調理と消費の完全保持 | レシート・手動時間・確定した調理と消費台帳 | 本人exportを確認後に全置換 | 元ID・入力hash・数量・時間根拠・台帳を全列同値で保持する | backend/tests/test_backup_database.py::test_backup_database_preserves_completed_cooking_receipts_and_consumption |
| 取下げ版と発行証跡 | 発行後に現在履歴が消失し料理版が取下げ | 発行根拠の一致する本人本文を復元 | 元履歴は回復し他人の本文や改竄は拒否する | backend/tests/test_backup_database.py::test_backup_database_export_proof_restores_withdrawn_history_without_self_grant |

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

| テストnode | 説明 | 表明 |
|---|---|---|
| backend/tests/test_backup_database.py::test_backup_database_round_trip_preserves_complete_rows_and_decimal | Given私有食品・未知数量・正確な小数 When確認後復元 Then全列同値で共有/別人不変。 | assert custom.status_code == 200, custom.text / assert option / assert confirmation['expectedVersion'] == changed['version'] / assert len(confirmation['counts']) == 34 / assert state(client) == changed / assert response.status_code == 200, response.text / assert response.json()['version'] == changed['version'] + 1 / assert after['tables'] == original['tables'] / assert after['profile'] == original['profile'] / assert any((row['amount'] is None for row in after['tables']['pantry_lot'])) / assert row['weight'] == str(exact) / assert actual and actual['weight'] == exact / assert export(client, 'bob')['tables'] == other_before['tables'] / assert db.execute('SELECT id, title, status FROM recipeweave.recipe ORDER BY id').fetchall() == catalog_before |
| backend/tests/test_backup_database.py::test_backup_database_tamper_foreign_owner_cas_and_single_use | Given発行済み本人ファイル When改竄/別人/更新競合/再送 Then変更せず拒否。 | assert rejected.status_code == 403 / assert foreign.status_code == 403 / assert stale.status_code == 409 / assert state(client) == changed / assert cancelled.status_code == 422 / assert accepted.status_code == 200, accepted.text / assert replay.status_code == 409 |
| backend/tests/test_backup_database.py::test_backup_database_late_failure_rolls_back_rows_revision_and_intent | Given置換/確認消費/版更新後のDB失敗 When監査追記 Then全部戻し確認も未使用。 | assert response.status_code == 409, response.text / assert state(client) == changed / assert export(client)['tables'] == before['tables'] / assert intent and intent['consumed_at'] is None |
| backend/tests/test_backup_database.py::test_backup_database_preserves_completed_cooking_receipts_and_consumption | Givenレシート・手動時間・調理完了 When全置換 Then原始ID/入力hash/消費台帳を保持。 | assert recipe_response.status_code == 200, recipe_response.text / assert receipt.status_code == 200, receipt.text / assert started.status_code == 200, started.text / assert completed.status_code == 200, completed.text / assert original_session['status'] == 'completed' / assert any((row['session_id'] == session['id'] for row in original['tables']['pantry_consumption'])) / assert tasks and all((row['duration_source'] == 'user_estimate' for row in tasks)) / assert all((row['confirmed_duration_s'] is not None for row in tasks)) / assert any((row['id'] == receipt_id for row in original['tables']['receipt_import'])) / assert restored.status_code == 200, restored.text / assert export(client)['tables'] == original['tables'] / assert completed_previous.status_code == 200, completed_previous.text |
| backend/tests/test_backup_database.py::test_backup_database_export_proof_restores_withdrawn_history_without_self_grant | Given正当に発行後に履歴消失/版取下げ When本人の同一本文を復元 Then元履歴だけ回復。 | assert not db.execute('SELECT id FROM recipeweave.user_recipe_event WHERE id=%s', (event_id,)).fetchall() / assert restored.status_code == 200, restored.text / assert after['tables'] == original['tables'] / assert foreign.status_code == 403 / assert tampered.status_code == 403 |

宣言応答: 200, 401, 403, 409, 413, 422, 503
