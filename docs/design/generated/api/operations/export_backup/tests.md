# 要因別単体テスト仕様: export_backup

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## 要因別の試験仕様

| 要因 | Given: 前提 | When: 操作 | Then: 期待結果 | 実在テストnode |
|---|---|---|---|---|
| numeric精度 | numeric(20,6)境界に近い小数 | 正規化JSON往復 | Decimalとdigestが完全一致する | backend/tests/test_backup_api.py::test_decimal_precision_survives_canonical_backup_round_trip |
| 列の保持 | 34表のDDLメタデータ | 生成された復元列と照合 | ID・時刻・追加列を含む全列が一致する | backend/tests/test_backup_api.py::test_backup_column_sets_match_current_physical_schema |
| 全表往復・精度・隔離 | 私有食品・未知数量・大きい正確な小数 | preview後の全置換 | 全業務列が同値で共有・別人に変更がない | backend/tests/test_backup_database.py::test_backup_database_round_trip_preserves_complete_rows_and_decimal |
| 改竄・別人・競合・単回確認 | 発行済みバックアップと現在版 | 改竄・他人・古い版・再送で復元 | 現在データを変更せず拒否する | backend/tests/test_backup_database.py::test_backup_database_tamper_foreign_owner_cas_and_single_use |
| 原子的取消し | 置換・確認消費・版更新後 | 監査追記で実DB例外 | 全業務行・版・確認消費がロールバックされる | backend/tests/test_backup_database.py::test_backup_database_late_failure_rolls_back_rows_revision_and_intent |
| 過去調理と消費の完全保持 | レシート・手動時間・確定した調理と消費台帳 | 本人exportを確認後に全置換 | 元ID・入力hash・数量・時間根拠・台帳を全列同値で保持する | backend/tests/test_backup_database.py::test_backup_database_preserves_completed_cooking_receipts_and_consumption |
| 取下げ版と発行証跡 | 発行後に現在履歴が消失し料理版が取下げ | 発行根拠の一致する本人本文を復元 | 元履歴は回復し他人の本文や改竄は拒否する | backend/tests/test_backup_database.py::test_backup_database_export_proof_restores_withdrawn_history_without_self_grant |

この表は試験仕様であり、実行の成功を示さない。実行結果は品質サイトの単体・結合テストから確認する。

次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。

対象URLを直接呼ぶテストなし。間接的な検証は検証記録を参照する。

宣言応答: 200, 401, 403, 409, 413, 422, 503
