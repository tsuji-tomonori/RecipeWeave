<!-- tools/quintflow.pyによる自動生成。spec/requirements/requirements.qntを編集すること。 -->
# RecipeWeave 要件一覧

- スキーマ版: 1
- カタログ版: 3
- Product(JSON): <code>"RecipeWeave"</code>
- 更新日(JSON): <code>"2026-09-05"</code>
- 正本: `spec/requirements/requirements.qnt`
- 機械可読view: `spec/requirements/requirements.json`

| ID | 版 | 状態 | 種別 | 原子的な義務 | 検証方法 |
|---|---:|---|---|---|---|
| <code>"REQ-DOMAIN-001"</code> | 1 | 有効 | 機能 | 食品意味特徴量は、food semantic identityを**維持する**（<code>"preserve"</code>） | 自動検査とartifact review |
| <code>"REQ-ENUM-001"</code> | 1 | 有効 | 機能 | 組合せ列挙器は、重複のない決定的な組合せ列を**維持する**（<code>"preserve"</code>） | 自動検査とartifact review |
| <code>"REQ-OUTPUT-001"</code> | 1 | 有効 | 機能 | 出力器は、全量出力・SHA256 manifest・再開位置を**維持する**（<code>"preserve"</code>） | 自動検査とartifact review |
| <code>"REQ-PERF-001"</code> | 1 | 有効 | 機能 | 組合せ実行基盤は、将来一千万件規模へ拡張可能な実行契約を**維持する**（<code>"preserve"</code>） | 自動検査とartifact review |
| <code>"REQ-EVAL-001"</code> | 1 | 有効 | 機能 | 評価実験は、blind independent Luna標本評価を**維持する**（<code>"preserve"</code>） | 自動検査とartifact review |
| <code>"REQ-STATS-001"</code> | 1 | 有効 | 機能 | 統計評価は、train/holdout分離と漏洩検査を**維持する**（<code>"preserve"</code>） | 自動検査とartifact review |
| <code>"REQ-DAG-001"</code> | 1 | 有効 | 機能 | レシピ表現は、原始材料数量と工程DAGを**維持する**（<code>"preserve"</code>） | 自動検査とartifact review |
| <code>"REQ-COST-001"</code> | 1 | 有効 | 機能 | 実験実行は、ユーザー未承認の大量課金なしを**維持する**（<code>"preserve"</code>） | 自動検査とartifact review |
| <code>"REQ-BOUNDARY-001"</code> | 1 | 有効 | 機能 | workspaceは、frontend/backend/database/infra/batch/scriptsの境界を**維持する**（<code>"preserve"</code>） | 自動検査とartifact review |
| <code>"REQ-DESIGN-001"</code> | 1 | 有効 | 機能 | as-built設計は、実装artifact由来の決定的な設計導線を**維持する**（<code>"preserve"</code>） | 自動検査とartifact review |
| <code>"REQ-SVC-SELECT-001"</code> | 1 | 有効 | 機能 | 食材選択画面は、カード全体の押下による食材の選択状態を**選択する**（<code>"select"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-SEARCH-001"</code> | 1 | 有効 | 機能 | 料理検索は、選択した食材を用いる公開対象料理を**選択する**（<code>"select"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-DISCOVERY-001"</code> | 1 | 有効 | 機能 | ホームは、利用条件を満たすランダムな一品を**提供する**（<code>"provide"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-SAMPLE-001"</code> | 1 | 有効 | 機能 | Dev公開版は、試用可能と明示した初期料理セットを**提供する**（<code>"provide"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-SCALE-001"</code> | 1 | 有効 | 機能 | 料理詳細は、確定分量に対する人数比の材料量を**導出する**（<code>"derive"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-AMOUNT-001"</code> | 1 | 有効 | 機能 | 料理詳細は、利用者が個別調整した材料分量を**維持する**（<code>"preserve"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-LOCAL-001"</code> | 1 | 有効 | 機能 | Dev公開版は、冷蔵庫・献立・しおり・調理状態の端末内データを**維持する**（<code>"maintain"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-OCR-001"</code> | 1 | 有効 | 機能 | レシート読取は、画像内の日本語から得た登録候補を**生成する**（<code>"generate"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-RECEIPT-INPUT-001"</code> | 1 | 有効 | 機能 | レシート入力は、撮影または画像選択で渡された画像を**妥当性確認する**（<code>"validate"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-RECEIPT-REVIEW-001"</code> | 1 | 有効 | 機能 | 読取確認画面は、選択する食品候補と除外した行を**実現する**（<code>"enable"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-RECEIPT-CANCEL-001"</code> | 1 | 有効 | 機能 | レシート読取は、確定していない画像・全文・候補を**制約する**（<code>"constrain"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-QUANTITY-001"</code> | 1 | 有効 | 機能 | 数量管理は、数量不明・購入単位・使用量の区別を**維持する**（<code>"preserve"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-RECEIPT-COMMIT-001"</code> | 1 | 有効 | 機能 | レシート登録は、利用者が確認した食品候補の在庫追加を**生成する**（<code>"generate"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-RECEIPT-DUPLICATE-001"</code> | 1 | 有効 | 機能 | レシート登録は、重複の可能性がある買い物の確認を**提供する**（<code>"provide"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-RECEIPT-UNDO-001"</code> | 1 | 有効 | 機能 | レシート履歴は、指定した登録単位の未消費在庫の取消を**実現する**（<code>"enable"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-FOOD-EDIT-001"</code> | 1 | 有効 | 機能 | 冷蔵庫は、食材名と任意の数量・保存場所・優先状態を**維持する**（<code>"maintain"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-MEAL-001"</code> | 1 | 有効 | 機能 | 献立は、選んだ各料理と独立した人数・分量を**維持する**（<code>"preserve"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-MEAL-QUANTITY-001"</code> | 1 | 有効 | 機能 | 献立の材料集計は、各料理の確定した原材料必要量を**導出する**（<code>"derive"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-SHOPPING-001"</code> | 1 | 有効 | 機能 | 買い物リストは、購入チェックと変更後の必要量を**維持する**（<code>"maintain"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-COOK-PLAN-001"</code> | 1 | 有効 | 機能 | 調理の段取りは、確定した料理工程の実行順を**提供する**（<code>"provide"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-COOK-RESUME-001"</code> | 1 | 有効 | 機能 | 調理画面は、選んだ料理の工程位置と完了状態を**維持する**（<code>"preserve"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-COOK-TIMER-001"</code> | 1 | 有効 | 機能 | 調理タイマーは、起動したタイマーとその経過状態を**維持する**（<code>"preserve"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-STOCK-CONSENT-001"</code> | 1 | 有効 | 機能 | 調理完了は、同単位で量が足りる在庫への確認済み使用量の反映を**制約する**（<code>"constrain"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-EXCLUSION-001"</code> | 1 | 有効 | 機能 | 候補選定は、利用者が指定した食べられない食材の条件を**強制する**（<code>"enforce"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-BACKUP-001"</code> | 1 | 有効 | 機能 | データ管理は、利用者が指定したバックアップ内容による現在データの置換を**実現する**（<code>"enable"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-PRIVACY-001"</code> | 1 | 有効 | データ | レシートデータ管理は、確認のため一時的に保持した画像とOCR全文の保存期間を**制約する**（<code>"constrain"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-BOOKMARK-001"</code> | 1 | 有効 | 機能 | 保存機能は、料理IDに対するしおりを**維持する**（<code>"preserve"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-GUIDE-001"</code> | 1 | 有効 | 機能 | 技法ガイドは、調理工程で参照した切り方を**提供する**（<code>"provide"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-CAPABILITY-001"</code> | 1 | 有効 | 品質 | 提供状態表示は、実際に利用できる機能と未提供機能を**提供する**（<code>"provide"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-SVC-PAGES-001"</code> | 1 | 有効 | 運用 | 開発配布工程は、検査対象の変更版と対応したDevプレビューを**提供する**（<code>"provide"</code>） | 対応する受入条件の自動検査と画面操作確認 |
| <code>"REQ-DEV-ARCH-001"</code> | 1 | 有効 | 制約 | RecipeWeaveの開発基盤は、ADR-0001で採用した構成に従う実装プロファイルを**提供する**（<code>"provide"</code>） | 構成コード・API契約の検査、認証と利用者分離の対象試験、実配備記録の照合 |
| <code>"REQ-DEV-QUALITY-001"</code> | 1 | 有効 | 運用 | RecipeWeaveの開発工程は、採用した配備とデータ移行に対応する再現可能な検証証跡を**維持する**（<code>"maintain"</code>） | CDKと移行の対象検査、生成設計の再生成/drift確認、版に対応する受入証跡のレビュー |

## REQ-DOMAIN-001: semantic food identity

要件ID(JSON): <code>"REQ-DOMAIN-001"</code>
タイトル(JSON): <code>"semantic food identity"</code>
主体(JSON): <code>"食品意味特徴量"</code>
対象(JSON): <code>"food semantic identity"</code>
食品意味特徴量は、food semantic identityを**維持する**。
行為enum: <code>"preserve"</code>

根拠: 食材の意味的な多様性をSKU表記の多さと混同せず、組合せ設計の対象にする。
根拠(JSON): <code>"食材の意味的な多様性をSKU表記の多さと混同せず、組合せ設計の対象にする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"bootstrap:recipeweave"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-DOMAIN-001-1"</code> 前提: RecipeWeaveの宣言入力がある。条件: 受入検査を実行する。期待結果: SKU濃度を独立指標として保持し、food semantic coverageと分けて評価する。。
  - criterion(JSON Object): <code>{"given":"RecipeWeaveの宣言入力がある","id":"AC-REQ-DOMAIN-001-1","then":"SKU濃度を独立指標として保持し、food semantic coverageと分けて評価する。","when":"受入検査を実行する"}</code>

要求源(JSON List): <code>["user:2026-09-05","README.md"]</code>
検証方法: 自動検査とartifact review
検証証跡: moon task and targeted tests
検証(JSON Object): <code>{"evidence":"moon task and targeted tests","method":"自動検査とartifact review"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/design/generated/README.md"]</code>
- 実装: <code>["packages/generator/pyproject.toml"]</code>
- テスト: <code>["tests/README.md"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT","QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ENUM-001: deterministic unique enumeration

要件ID(JSON): <code>"REQ-ENUM-001"</code>
タイトル(JSON): <code>"deterministic unique enumeration"</code>
主体(JSON): <code>"組合せ列挙器"</code>
対象(JSON): <code>"重複のない決定的な組合せ列"</code>
組合せ列挙器は、重複のない決定的な組合せ列を**維持する**。
行為enum: <code>"preserve"</code>

根拠: 再実行・並列化・入力順の同値変換でも安定した順序と一意な識別子を得る必要がある。
根拠(JSON): <code>"再実行・並列化・入力順の同値変換でも安定した順序と一意な識別子を得る必要がある。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"bootstrap:recipeweave"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-ENUM-001-1"</code> 前提: RecipeWeaveの宣言入力がある。条件: 受入検査を実行する。期待結果: 列挙結果を正規化キーで重複排除し、同一入力の結果をバイト比較する。。
  - criterion(JSON Object): <code>{"given":"RecipeWeaveの宣言入力がある","id":"AC-REQ-ENUM-001-1","then":"列挙結果を正規化キーで重複排除し、同一入力の結果をバイト比較する。","when":"受入検査を実行する"}</code>

要求源(JSON List): <code>["user:2026-09-05","README.md"]</code>
検証方法: 自動検査とartifact review
検証証跡: moon task and targeted tests
検証(JSON Object): <code>{"evidence":"moon task and targeted tests","method":"自動検査とartifact review"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/design/generated/README.md"]</code>
- 実装: <code>["packages/generator/pyproject.toml"]</code>
- テスト: <code>["tests/README.md"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT","QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-OUTPUT-001: complete output manifest and resume

要件ID(JSON): <code>"REQ-OUTPUT-001"</code>
タイトル(JSON): <code>"complete output manifest and resume"</code>
主体(JSON): <code>"出力器"</code>
対象(JSON): <code>"全量出力・SHA256 manifest・再開位置"</code>
出力器は、全量出力・SHA256 manifest・再開位置を**維持する**。
行為enum: <code>"preserve"</code>

根拠: 大量結果は一部成功を成功扱いせず、欠落を検出して再開できなければならない。
根拠(JSON): <code>"大量結果は一部成功を成功扱いせず、欠落を検出して再開できなければならない。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"bootstrap:recipeweave"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-OUTPUT-001-1"</code> 前提: RecipeWeaveの宣言入力がある。条件: 受入検査を実行する。期待結果: 結果チャンク、件数、SHA256、入力digest、再開cursorをmanifestへ記録する。。
  - criterion(JSON Object): <code>{"given":"RecipeWeaveの宣言入力がある","id":"AC-REQ-OUTPUT-001-1","then":"結果チャンク、件数、SHA256、入力digest、再開cursorをmanifestへ記録する。","when":"受入検査を実行する"}</code>

要求源(JSON List): <code>["user:2026-09-05","README.md"]</code>
検証方法: 自動検査とartifact review
検証証跡: moon task and targeted tests
検証(JSON Object): <code>{"evidence":"moon task and targeted tests","method":"自動検査とartifact review"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/design/generated/README.md"]</code>
- 実装: <code>["packages/generator/pyproject.toml"]</code>
- テスト: <code>["tests/README.md"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT","QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-PERF-001: future ten million target

要件ID(JSON): <code>"REQ-PERF-001"</code>
タイトル(JSON): <code>"future ten million target"</code>
主体(JSON): <code>"組合せ実行基盤"</code>
対象(JSON): <code>"将来一千万件規模へ拡張可能な実行契約"</code>
組合せ実行基盤は、将来一千万件規模へ拡張可能な実行契約を**維持する**。
行為enum: <code>"preserve"</code>

根拠: 初期データでの実績と将来目標を混同せず、ボトルネックを測定可能にする。
根拠(JSON): <code>"初期データでの実績と将来目標を混同せず、ボトルネックを測定可能にする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"bootstrap:recipeweave"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-PERF-001-1"</code> 前提: RecipeWeaveの宣言入力がある。条件: 受入検査を実行する。期待結果: ベンチマークは件数と時間を記録し、10m目標は未達なら未実装・未達として報告する。。
  - criterion(JSON Object): <code>{"given":"RecipeWeaveの宣言入力がある","id":"AC-REQ-PERF-001-1","then":"ベンチマークは件数と時間を記録し、10m目標は未達なら未実装・未達として報告する。","when":"受入検査を実行する"}</code>

要求源(JSON List): <code>["user:2026-09-05","README.md"]</code>
検証方法: 自動検査とartifact review
検証証跡: moon task and targeted tests
検証(JSON Object): <code>{"evidence":"moon task and targeted tests","method":"自動検査とartifact review"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/design/generated/README.md"]</code>
- 実装: <code>["packages/generator/pyproject.toml"]</code>
- テスト: <code>["tests/README.md"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT","QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EVAL-001: blind independent Luna evaluation

要件ID(JSON): <code>"REQ-EVAL-001"</code>
タイトル(JSON): <code>"blind independent Luna evaluation"</code>
主体(JSON): <code>"評価実験"</code>
対象(JSON): <code>"blind independent Luna標本評価"</code>
評価実験は、blind independent Luna標本評価を**維持する**。
行為enum: <code>"preserve"</code>

根拠: 評価者の独立性と物理的な食味評価を、モデルの意味特徴やSKU評価と区別する。
根拠(JSON): <code>"評価者の独立性と物理的な食味評価を、モデルの意味特徴やSKU評価と区別する。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"bootstrap:recipeweave"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-EVAL-001-1"</code> 前提: RecipeWeaveの宣言入力がある。条件: 受入検査を実行する。期待結果: 標本割当を盲検化し、Luna標本の手順・識別子・評価を別artifactとして固定する。。
  - criterion(JSON Object): <code>{"given":"RecipeWeaveの宣言入力がある","id":"AC-REQ-EVAL-001-1","then":"標本割当を盲検化し、Luna標本の手順・識別子・評価を別artifactとして固定する。","when":"受入検査を実行する"}</code>

要求源(JSON List): <code>["user:2026-09-05","README.md"]</code>
検証方法: 自動検査とartifact review
検証証跡: moon task and targeted tests
検証(JSON Object): <code>{"evidence":"moon task and targeted tests","method":"自動検査とartifact review"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/design/generated/README.md"]</code>
- 実装: <code>["packages/generator/pyproject.toml"]</code>
- テスト: <code>["tests/README.md"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT","QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-STATS-001: train holdout separation

要件ID(JSON): <code>"REQ-STATS-001"</code>
タイトル(JSON): <code>"train holdout separation"</code>
主体(JSON): <code>"統計評価"</code>
対象(JSON): <code>"train/holdout分離と漏洩検査"</code>
統計評価は、train/holdout分離と漏洩検査を**維持する**。
行為enum: <code>"preserve"</code>

根拠: 探索結果を同じ標本で評価すると汎化性能を過大評価する。
根拠(JSON): <code>"探索結果を同じ標本で評価すると汎化性能を過大評価する。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"bootstrap:recipeweave"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-STATS-001-1"</code> 前提: RecipeWeaveの宣言入力がある。条件: 受入検査を実行する。期待結果: 分割seed、件数、除外条件、holdout固定状態をmanifestとレポートに残す。。
  - criterion(JSON Object): <code>{"given":"RecipeWeaveの宣言入力がある","id":"AC-REQ-STATS-001-1","then":"分割seed、件数、除外条件、holdout固定状態をmanifestとレポートに残す。","when":"受入検査を実行する"}</code>

要求源(JSON List): <code>["user:2026-09-05","README.md"]</code>
検証方法: 自動検査とartifact review
検証証跡: moon task and targeted tests
検証(JSON Object): <code>{"evidence":"moon task and targeted tests","method":"自動検査とartifact review"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/design/generated/README.md"]</code>
- 実装: <code>["packages/generator/pyproject.toml"]</code>
- テスト: <code>["tests/README.md"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT","QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DAG-001: raw material quantities and process DAG

要件ID(JSON): <code>"REQ-DAG-001"</code>
タイトル(JSON): <code>"raw material quantities and process DAG"</code>
主体(JSON): <code>"レシピ表現"</code>
対象(JSON): <code>"原始材料数量と工程DAG"</code>
レシピ表現は、原始材料数量と工程DAGを**維持する**。
行為enum: <code>"preserve"</code>

根拠: 完成料理名だけでは再現性や工程制約を表現できない。
根拠(JSON): <code>"完成料理名だけでは再現性や工程制約を表現できない。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"bootstrap:recipeweave"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-DAG-001-1"</code> 前提: RecipeWeaveの宣言入力がある。条件: 受入検査を実行する。期待結果: 各原始材料の単位付き数量と工程ノード・依存辺を検証可能な形式で保存する。。
  - criterion(JSON Object): <code>{"given":"RecipeWeaveの宣言入力がある","id":"AC-REQ-DAG-001-1","then":"各原始材料の単位付き数量と工程ノード・依存辺を検証可能な形式で保存する。","when":"受入検査を実行する"}</code>

要求源(JSON List): <code>["user:2026-09-05","README.md"]</code>
検証方法: 自動検査とartifact review
検証証跡: moon task and targeted tests
検証(JSON Object): <code>{"evidence":"moon task and targeted tests","method":"自動検査とartifact review"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/design/generated/README.md"]</code>
- 実装: <code>["packages/generator/pyproject.toml"]</code>
- テスト: <code>["tests/README.md"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT","QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-COST-001: approved spending boundary

要件ID(JSON): <code>"REQ-COST-001"</code>
タイトル(JSON): <code>"approved spending boundary"</code>
主体(JSON): <code>"実験実行"</code>
対象(JSON): <code>"ユーザー未承認の大量課金なし"</code>
実験実行は、ユーザー未承認の大量課金なしを**維持する**。
行為enum: <code>"preserve"</code>

根拠: 大量生成・外部評価・クラウド実行は費用を発生させうるため、承認境界を明示する。
根拠(JSON): <code>"大量生成・外部評価・クラウド実行は費用を発生させうるため、承認境界を明示する。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"bootstrap:recipeweave"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-COST-001-1"</code> 前提: RecipeWeaveの宣言入力がある。条件: 受入検査を実行する。期待結果: デフォルトはローカル・小規模dry-runとし、費用見積りと明示承認なしに外部大量処理を開始しない。。
  - criterion(JSON Object): <code>{"given":"RecipeWeaveの宣言入力がある","id":"AC-REQ-COST-001-1","then":"デフォルトはローカル・小規模dry-runとし、費用見積りと明示承認なしに外部大量処理を開始しない。","when":"受入検査を実行する"}</code>

要求源(JSON List): <code>["user:2026-09-05","README.md"]</code>
検証方法: 自動検査とartifact review
検証証跡: moon task and targeted tests
検証(JSON Object): <code>{"evidence":"moon task and targeted tests","method":"自動検査とartifact review"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/design/generated/README.md"]</code>
- 実装: <code>["packages/generator/pyproject.toml"]</code>
- テスト: <code>["tests/README.md"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT","QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-BOUNDARY-001: future project boundaries

要件ID(JSON): <code>"REQ-BOUNDARY-001"</code>
タイトル(JSON): <code>"future project boundaries"</code>
主体(JSON): <code>"workspace"</code>
対象(JSON): <code>"frontend/backend/database/infra/batch/scriptsの境界"</code>
workspaceは、frontend/backend/database/infra/batch/scriptsの境界を**維持する**。
行為enum: <code>"preserve"</code>

根拠: 将来の同居先を予約しつつ未実装機能を実装済みと表明しない。
根拠(JSON): <code>"将来の同居先を予約しつつ未実装機能を実装済みと表明しない。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"bootstrap:recipeweave"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-BOUNDARY-001-1"</code> 前提: RecipeWeaveの宣言入力がある。条件: 受入検査を実行する。期待結果: 各予約projectはREADMEとmoon設定を持ち、実装状態をplaceholderとして表示する。。
  - criterion(JSON Object): <code>{"given":"RecipeWeaveの宣言入力がある","id":"AC-REQ-BOUNDARY-001-1","then":"各予約projectはREADMEとmoon設定を持ち、実装状態をplaceholderとして表示する。","when":"受入検査を実行する"}</code>

要求源(JSON List): <code>["user:2026-09-05","README.md"]</code>
検証方法: 自動検査とartifact review
検証証跡: moon task and targeted tests
検証(JSON Object): <code>{"evidence":"moon task and targeted tests","method":"自動検査とartifact review"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/design/generated/README.md"]</code>
- 実装: <code>["packages/generator/pyproject.toml"]</code>
- テスト: <code>["tests/README.md"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT","QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-001: implementation-derived design

要件ID(JSON): <code>"REQ-DESIGN-001"</code>
タイトル(JSON): <code>"implementation-derived design"</code>
主体(JSON): <code>"as-built設計"</code>
対象(JSON): <code>"実装artifact由来の決定的な設計導線"</code>
as-built設計は、実装artifact由来の決定的な設計導線を**維持する**。
行為enum: <code>"preserve"</code>

根拠: 設計文書が実装と乖離すると受入判断を誤る。
根拠(JSON): <code>"設計文書が実装と乖離すると受入判断を誤る。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"bootstrap:recipeweave"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-DESIGN-001-1"</code> 前提: RecipeWeaveの宣言入力がある。条件: 受入検査を実行する。期待結果: generatorの同一入力再実行で生成設計がbyte一致し、drift checkが差分を報告する。。
  - criterion(JSON Object): <code>{"given":"RecipeWeaveの宣言入力がある","id":"AC-REQ-DESIGN-001-1","then":"generatorの同一入力再実行で生成設計がbyte一致し、drift checkが差分を報告する。","when":"受入検査を実行する"}</code>

要求源(JSON List): <code>["user:2026-09-05","README.md"]</code>
検証方法: 自動検査とartifact review
検証証跡: moon task and targeted tests
検証(JSON Object): <code>{"evidence":"moon task and targeted tests","method":"自動検査とartifact review"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/design/generated/README.md"]</code>
- 実装: <code>["packages/generator/pyproject.toml"]</code>
- テスト: <code>["tests/README.md"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT","QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-SELECT-001: 食材カードの選択状態を明示する

要件ID(JSON): <code>"REQ-SVC-SELECT-001"</code>
タイトル(JSON): <code>"食材カードの選択状態を明示する"</code>
主体(JSON): <code>"食材選択画面"</code>
対象(JSON): <code>"カード全体の押下による食材の選択状態"</code>
食材選択画面は、カード全体の押下による食材の選択状態を**選択する**。
行為enum: <code>"select"</code>

根拠: 小さな位置合わせを求めず、選択できる対象と選択済みを利用者が判別できるようにする。
根拠(JSON): <code>"小さな位置合わせを求めず、選択できる対象と選択済みを利用者が判別できるようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-SELECT-001-1"</code> 前提: 未選択の食材を表示している。条件: 食材カードを見る。期待結果: 空のチェックボックスが表示され、カード全体で選択できる。。
  - criterion(JSON Object): <code>{"given":"未選択の食材を表示している","id":"AC-REQ-SVC-SELECT-001-1","then":"空のチェックボックスが表示され、カード全体で選択できる。","when":"食材カードを見る"}</code>
- <code>"AC-REQ-SVC-SELECT-001-2"</code> 前提: 食材カードが表示されている。条件: カードを押し、もう一度押す。期待結果: 最初はチェックと枠で選択済みとなり、次の押下で解除される。色だけで状態を区別しない。。
  - criterion(JSON Object): <code>{"given":"食材カードが表示されている","id":"AC-REQ-SVC-SELECT-001-2","then":"最初はチェックと枠で選択済みとなり、次の押下で解除される。色だけで状態を区別しない。","when":"カードを押し、もう一度押す"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-SEARCH-001: 人数と分量を入力せず食材から探す

要件ID(JSON): <code>"REQ-SVC-SEARCH-001"</code>
タイトル(JSON): <code>"人数と分量を入力せず食材から探す"</code>
主体(JSON): <code>"料理検索"</code>
対象(JSON): <code>"選択した食材を用いる公開対象料理"</code>
料理検索は、選択した食材を用いる公開対象料理を**選択する**。
行為enum: <code>"select"</code>

根拠: 最初の料理選びを食材の選択だけで開始できるようにする。
根拠(JSON): <code>"最初の料理選びを食材の選択だけで開始できるようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-SEARCH-001-1"</code> 前提: ログインや冷蔵庫登録をしていない。条件: 食材を選んで検索する。期待結果: 人数・分量を要求せず検索でき、既定は選んだ食材をすべて使う候補になる。。
  - criterion(JSON Object): <code>{"given":"ログインや冷蔵庫登録をしていない","id":"AC-REQ-SVC-SEARCH-001-1","then":"人数・分量を要求せず検索でき、既定は選んだ食材をすべて使う候補になる。","when":"食材を選んで検索する"}</code>
- <code>"AC-REQ-SVC-SEARCH-001-2"</code> 前提: 検索条件または結果を表示している。条件: いずれかを使うへ明示的に切り替える、または結果から戻る。期待結果: 切替後の条件を結果に表示し、戻る際は選択・条件・表示位置を保持する。。
  - criterion(JSON Object): <code>{"given":"検索条件または結果を表示している","id":"AC-REQ-SVC-SEARCH-001-2","then":"切替後の条件を結果に表示し、戻る際は選択・条件・表示位置を保持する。","when":"いずれかを使うへ明示的に切り替える、または結果から戻る"}</code>
- <code>"AC-REQ-SVC-SEARCH-001-3"</code> 前提: 条件に合う候補がない、または取得に失敗した。条件: 検索結果を開く。期待結果: 0件または失敗を区別し、条件を無断で緩めず、入力を保持した選び直し・再試行の入口を示す。。
  - criterion(JSON Object): <code>{"given":"条件に合う候補がない、または取得に失敗した","id":"AC-REQ-SVC-SEARCH-001-3","then":"0件または失敗を区別し、条件を無断で緩めず、入力を保持した選び直し・再試行の入口を示す。","when":"検索結果を開く"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-DISCOVERY-001: ホームに偶然の一品を提示する

要件ID(JSON): <code>"REQ-SVC-DISCOVERY-001"</code>
タイトル(JSON): <code>"ホームに偶然の一品を提示する"</code>
主体(JSON): <code>"ホーム"</code>
対象(JSON): <code>"利用条件を満たすランダムな一品"</code>
ホームは、利用条件を満たすランダムな一品を**提供する**。
行為enum: <code>"provide"</code>

根拠: 検索語を考えなくても料理を発見できるようにする。
根拠(JSON): <code>"検索語を考えなくても料理を発見できるようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-DISCOVERY-001-1"</code> 前提: 条件に合う候補がある。条件: ホームを新しく開く、または別の一品を押す。期待結果: 偶然の一品を必ず提示し、複数候補がある場合は直近の同じ一品の連続表示を避ける。。
  - criterion(JSON Object): <code>{"given":"条件に合う候補がある","id":"AC-REQ-SVC-DISCOVERY-001-1","then":"偶然の一品を必ず提示し、複数候補がある場合は直近の同じ一品の連続表示を避ける。","when":"ホームを新しく開く、または別の一品を押す"}</code>
- <code>"AC-REQ-SVC-DISCOVERY-001-2"</code> 前提: 検索結果からホームへ戻る、または適合候補がない。条件: ホームを表示する。期待結果: 戻った場合は表示していた一品を保持し、候補がない場合は理由と条件変更入口を示して必須条件を守る。。
  - criterion(JSON Object): <code>{"given":"検索結果からホームへ戻る、または適合候補がない","id":"AC-REQ-SVC-DISCOVERY-001-2","then":"戻った場合は表示していた一品を保持し、候補がない場合は理由と条件変更入口を示して必須条件を守る。","when":"ホームを表示する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-SAMPLE-001: 初期Devで操作可能なサンプル料理を提供する

要件ID(JSON): <code>"REQ-SVC-SAMPLE-001"</code>
タイトル(JSON): <code>"初期Devで操作可能なサンプル料理を提供する"</code>
主体(JSON): <code>"Dev公開版"</code>
対象(JSON): <code>"試用可能と明示した初期料理セット"</code>
Dev公開版は、試用可能と明示した初期料理セットを**提供する**。
行為enum: <code>"provide"</code>

根拠: 将来の大量レシピ生成の完了を待たず、料理を探して作る操作を確認できるようにする。
根拠(JSON): <code>"将来の大量レシピ生成の完了を待たず、料理を探して作る操作を確認できるようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-SAMPLE-001-1"</code> 前提: 初期Dev版を公開する。条件: 利用できる料理一覧を確認する。期待結果: なす卵醤油・なす卵カレー・トマト卵・豆腐わかめスープ・キャベツツナ・カップ焼きそばチーズ・ツナコーンごはん・きのこバターの8品を操作用サンプルとして選べる。。
  - criterion(JSON Object): <code>{"given":"初期Dev版を公開する","id":"AC-REQ-SVC-SAMPLE-001-1","then":"なす卵醤油・なす卵カレー・トマト卵・豆腐わかめスープ・キャベツツナ・カップ焼きそばチーズ・ツナコーンごはん・きのこバターの8品を操作用サンプルとして選べる。","when":"利用できる料理一覧を確認する"}</code>
- <code>"AC-REQ-SVC-SAMPLE-001-2"</code> 前提: 試用料理を表示する。条件: 料理の説明と提供状態を見る。期待結果: 試用データであることと対象範囲を示し、将来目標件数を実際の公開件数や品質実証として表示しない。。
  - criterion(JSON Object): <code>{"given":"試用料理を表示する","id":"AC-REQ-SVC-SAMPLE-001-2","then":"試用データであることと対象範囲を示し、将来目標件数を実際の公開件数や品質実証として表示しない。","when":"料理の説明と提供状態を見る"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-SCALE-001: 料理選択後に人数に応じた分量へ変換する

要件ID(JSON): <code>"REQ-SVC-SCALE-001"</code>
タイトル(JSON): <code>"料理選択後に人数に応じた分量へ変換する"</code>
主体(JSON): <code>"料理詳細"</code>
対象(JSON): <code>"確定分量に対する人数比の材料量"</code>
料理詳細は、確定分量に対する人数比の材料量を**導出する**。
行為enum: <code>"derive"</code>

根拠: 同一料理の人数違いを別レシピとして探す手間をなくす。
根拠(JSON): <code>"同一料理の人数違いを別レシピとして探す手間をなくす。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-SCALE-001-1"</code> 前提: 2人分のなす160g・卵2個・油8gを表示している。条件: 人数を3人に変える。期待結果: 材料量がなす240g・卵3個・油12gになる。加熱時間は人数比で変更しない。。
  - criterion(JSON Object): <code>{"given":"2人分のなす160g・卵2個・油8gを表示している","id":"AC-REQ-SVC-SCALE-001-1","then":"材料量がなす240g・卵3個・油12gになる。加熱時間は人数比で変更しない。","when":"人数を3人に変える"}</code>
- <code>"AC-REQ-SVC-SCALE-001-2"</code> 前提: 個別変更を含む直前の確定分量がある。条件: 正の人数を直接入力または加減ボタンで変更する。期待結果: 各材料を新人数/旧人数の比で更新する。0以下・非数の人数は確定できず、更新前の分量で調理を開始させない。。
  - criterion(JSON Object): <code>{"given":"個別変更を含む直前の確定分量がある","id":"AC-REQ-SVC-SCALE-001-2","then":"各材料を新人数/旧人数の比で更新する。0以下・非数の人数は確定できず、更新前の分量で調理を開始させない。","when":"正の人数を直接入力または加減ボタンで変更する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-AMOUNT-001: 材料別の量を直接調整する

要件ID(JSON): <code>"REQ-SVC-AMOUNT-001"</code>
タイトル(JSON): <code>"材料別の量を直接調整する"</code>
主体(JSON): <code>"料理詳細"</code>
対象(JSON): <code>"利用者が個別調整した材料分量"</code>
料理詳細は、利用者が個別調整した材料分量を**維持する**。
行為enum: <code>"preserve"</code>

根拠: 手持ちの量や好みに合わせた変更を検索後に行い、次の操作へ引き継ぐ。
根拠(JSON): <code>"手持ちの量や好みに合わせた変更を検索後に行い、次の操作へ引き継ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-AMOUNT-001-1"</code> 前提: 料理詳細の材料量を表示している。条件: 材料の数量欄に値を直接入力する。期待結果: 対象材料だけを調整し、調整済みを表示する。負数・非数を確定せず、献立追加と調理開始に確定分量を引き継ぐ。。
  - criterion(JSON Object): <code>{"given":"料理詳細の材料量を表示している","id":"AC-REQ-SVC-AMOUNT-001-1","then":"対象材料だけを調整し、調整済みを表示する。負数・非数を確定せず、献立追加と調理開始に確定分量を引き継ぐ。","when":"材料の数量欄に値を直接入力する"}</code>
- <code>"AC-REQ-SVC-AMOUNT-001-2"</code> 前提: 人数や量を調整済みである。条件: 同じブラウザで料理を開き直す、または元の分量に戻す。期待結果: 調整は料理詳細の下書きとして維持され、リセットで標準分量に戻る。。
  - criterion(JSON Object): <code>{"given":"人数や量を調整済みである","id":"AC-REQ-SVC-AMOUNT-001-2","then":"調整は料理詳細の下書きとして維持され、リセットで標準分量に戻る。","when":"同じブラウザで料理を開き直す、または元の分量に戻す"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-LOCAL-001: 試用データを同じブラウザで継続利用する

要件ID(JSON): <code>"REQ-SVC-LOCAL-001"</code>
タイトル(JSON): <code>"試用データを同じブラウザで継続利用する"</code>
主体(JSON): <code>"Dev公開版"</code>
対象(JSON): <code>"冷蔵庫・献立・しおり・調理状態の端末内データ"</code>
Dev公開版は、冷蔵庫・献立・しおり・調理状態の端末内データを**維持する**。
行為enum: <code>"maintain"</code>

根拠: ログインなしで途中から使え、保存範囲を誤認しないようにする。
根拠(JSON): <code>"ログインなしで途中から使え、保存範囲を誤認しないようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-LOCAL-001-1"</code> 前提: 冷蔵庫・献立・しおり・分量下書き・調理状態を変更した。条件: 同じ端末の同じブラウザで開き直す。期待結果: 最後に確定したデータから利用を続けられる。保存に失敗したときは成功表示を出さない。。
  - criterion(JSON Object): <code>{"given":"冷蔵庫・献立・しおり・分量下書き・調理状態を変更した","id":"AC-REQ-SVC-LOCAL-001-1","then":"最後に確定したデータから利用を続けられる。保存に失敗したときは成功表示を出さない。","when":"同じ端末の同じブラウザで開き直す"}</code>
- <code>"AC-REQ-SVC-LOCAL-001-2"</code> 前提: 端末保存を使用している。条件: 保存先の説明を確認する。期待結果: 別端末や別ブラウザへの自動同期を行わないことと、バックアップなしの消失はサービス側で復元できないことが分かる。。
  - criterion(JSON Object): <code>{"given":"端末保存を使用している","id":"AC-REQ-SVC-LOCAL-001-2","then":"別端末や別ブラウザへの自動同期を行わないことと、バックアップなしの消失はサービス側で復元できないことが分かる。","when":"保存先の説明を確認する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-OCR-001: レシート画像を端末内で読み取る

要件ID(JSON): <code>"REQ-SVC-OCR-001"</code>
タイトル(JSON): <code>"レシート画像を端末内で読み取る"</code>
主体(JSON): <code>"レシート読取"</code>
対象(JSON): <code>"画像内の日本語から得た登録候補"</code>
レシート読取は、画像内の日本語から得た登録候補を**生成する**。
行為enum: <code>"generate"</code>

根拠: 実画像から入力候補を作り、個別手入力の手間を減らす。
根拠(JSON): <code>"実画像から入力候補を作り、個別手入力の手間を減らす。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-OCR-001-1"</code> 前提: 対応する実レシート画像を選んだ。条件: 読み取るを押す。期待結果: この端末内で日本語を読み取り、画像をサービスサーバーへ送信せず候補を表示する。読み取りだけでは在庫を変更しない。。
  - criterion(JSON Object): <code>{"given":"対応する実レシート画像を選んだ","id":"AC-REQ-SVC-OCR-001-1","then":"この端末内で日本語を読み取り、画像をサービスサーバーへ送信せず候補を表示する。読み取りだけでは在庫を変更しない。","when":"読み取るを押す"}</code>
- <code>"AC-REQ-SVC-OCR-001-2"</code> 前提: 読取処理に失敗した、またはサンプルを選んだ。条件: 結果画面を開く。期待結果: 失敗には再試行・画像の選び直し・手入力を示す。サンプル結果は実画像の読取成功と区別する。。
  - criterion(JSON Object): <code>{"given":"読取処理に失敗した、またはサンプルを選んだ","id":"AC-REQ-SVC-OCR-001-2","then":"失敗には再試行・画像の選び直し・手入力を示す。サンプル結果は実画像の読取成功と区別する。","when":"結果画面を開く"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-RECEIPT-INPUT-001: 対応するレシート画像だけを受け付ける

要件ID(JSON): <code>"REQ-SVC-RECEIPT-INPUT-001"</code>
タイトル(JSON): <code>"対応するレシート画像だけを受け付ける"</code>
主体(JSON): <code>"レシート入力"</code>
対象(JSON): <code>"撮影または画像選択で渡された画像"</code>
レシート入力は、撮影または画像選択で渡された画像を**妥当性確認する**。
行為enum: <code>"validate"</code>

根拠: 端末ごとの撮影条件と画像制限を明示し、失敗後も利用を続けられるようにする。
根拠(JSON): <code>"端末ごとの撮影条件と画像制限を明示し、失敗後も利用を続けられるようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-RECEIPT-INPUT-001-1"</code> 前提: レシートから追加を開いている。条件: 撮影するまたは画像を選ぶを使用する。期待結果: JPEG・PNG・WebPの1枚10×1024×1024バイト以下を受け付ける。カメラ拒否時も画像選択と手入力を使用できる。。
  - criterion(JSON Object): <code>{"given":"レシートから追加を開いている","id":"AC-REQ-SVC-RECEIPT-INPUT-001-1","then":"JPEG・PNG・WebPの1枚10×1024×1024バイト以下を受け付ける。カメラ拒否時も画像選択と手入力を使用できる。","when":"撮影するまたは画像を選ぶを使用する"}</code>
- <code>"AC-REQ-SVC-RECEIPT-INPUT-001-2"</code> 前提: HEIC等の非対応形式、容量超過または画像として壊れたファイルがある。条件: 画像を選ぶ。期待結果: 理由を表示して選び直せる。在庫を変更しない。。
  - criterion(JSON Object): <code>{"given":"HEIC等の非対応形式、容量超過または画像として壊れたファイルがある","id":"AC-REQ-SVC-RECEIPT-INPUT-001-2","then":"理由を表示して選び直せる。在庫を変更しない。","when":"画像を選ぶ"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-RECEIPT-REVIEW-001: 登録前に読取候補を訂正できる

要件ID(JSON): <code>"REQ-SVC-RECEIPT-REVIEW-001"</code>
タイトル(JSON): <code>"登録前に読取候補を訂正できる"</code>
主体(JSON): <code>"読取確認画面"</code>
対象(JSON): <code>"選択する食品候補と除外した行"</code>
読取確認画面は、選択する食品候補と除外した行を**実現する**。
行為enum: <code>"enable"</code>

根拠: OCRの誤読と誤除外から利用者が自力で復帰できるようにする。
根拠(JSON): <code>"OCRの誤読と誤除外から利用者が自力で復帰できるようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-RECEIPT-REVIEW-001-1"</code> 前提: 登録候補に食品名の誤りまたは不明な行がある。条件: 修正または食材を選ぶを押す。期待結果: 原文と候補を確認して食材名・数量・単位を訂正できる。自動判定済みの行も修正できる。。
  - criterion(JSON Object): <code>{"given":"登録候補に食品名の誤りまたは不明な行がある","id":"AC-REQ-SVC-RECEIPT-REVIEW-001-1","then":"原文と候補を確認して食材名・数量・単位を訂正できる。自動判定済みの行も修正できる。","when":"修正または食材を選ぶを押す"}</code>
- <code>"AC-REQ-SVC-RECEIPT-REVIEW-001-2"</code> 前提: 日用品・袋代・値引き・合計の行、または誤除外された食品がある。条件: 登録対象のチェックと除外した行を確認する。期待結果: 非食品行を外せ、誤除外した食品を選択と食材指定で戻せる。原文自体に欠けた食品は登録後に手入力で補える。。
  - criterion(JSON Object): <code>{"given":"日用品・袋代・値引き・合計の行、または誤除外された食品がある","id":"AC-REQ-SVC-RECEIPT-REVIEW-001-2","then":"非食品行を外せ、誤除外した食品を選択と食材指定で戻せる。原文自体に欠けた食品は登録後に手入力で補える。","when":"登録対象のチェックと除外した行を確認する"}</code>
- <code>"AC-REQ-SVC-RECEIPT-REVIEW-001-3"</code> 前提: 未確認の行は未選択で有効な2行が選択済みである。条件: この内容で登録へ進む。期待結果: 未選択の不明行は登録を妨げず2件を確定できる。同名商品という理由だけで別の購入行を削除しない。。
  - criterion(JSON Object): <code>{"given":"未確認の行は未選択で有効な2行が選択済みである","id":"AC-REQ-SVC-RECEIPT-REVIEW-001-3","then":"未選択の不明行は登録を妨げず2件を確定できる。同名商品という理由だけで別の購入行を削除しない。","when":"この内容で登録へ進む"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-RECEIPT-CANCEL-001: 確定前の読取を在庫変更なしで中止する

要件ID(JSON): <code>"REQ-SVC-RECEIPT-CANCEL-001"</code>
タイトル(JSON): <code>"確定前の読取を在庫変更なしで中止する"</code>
主体(JSON): <code>"レシート読取"</code>
対象(JSON): <code>"確定していない画像・全文・候補"</code>
レシート読取は、確定していない画像・全文・候補を**制約する**。
行為enum: <code>"constrain"</code>

根拠: 登録する前ならやめられ、取り消し作業を在庫へ持ち越さないようにする。
根拠(JSON): <code>"登録する前ならやめられ、取り消し作業を在庫へ持ち越さないようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-RECEIPT-CANCEL-001-1"</code> 前提: 読み取り中または候補を訂正中である。条件: キャンセルし、訂正中なら破棄を確認する。期待結果: 未確定の候補を破棄し、在庫・確定済み登録履歴を変更しない。。
  - criterion(JSON Object): <code>{"given":"読み取り中または候補を訂正中である","id":"AC-REQ-SVC-RECEIPT-CANCEL-001-1","then":"未確定の候補を破棄し、在庫・確定済み登録履歴を変更しない。","when":"キャンセルし、訂正中なら破棄を確認する"}</code>
- <code>"AC-REQ-SVC-RECEIPT-CANCEL-001-2"</code> 前提: 候補を訂正中に破棄確認が出た。条件: 破棄をやめる。期待結果: 訂正内容を保ったまま確認へ戻れる。。
  - criterion(JSON Object): <code>{"given":"候補を訂正中に破棄確認が出た","id":"AC-REQ-SVC-RECEIPT-CANCEL-001-2","then":"訂正内容を保ったまま確認へ戻れる。","when":"破棄をやめる"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-QUANTITY-001: 不明な食品量を推測せず保持する

要件ID(JSON): <code>"REQ-SVC-QUANTITY-001"</code>
タイトル(JSON): <code>"不明な食品量を推測せず保持する"</code>
主体(JSON): <code>"数量管理"</code>
対象(JSON): <code>"数量不明・購入単位・使用量の区別"</code>
数量管理は、数量不明・購入単位・使用量の区別を**維持する**。
行為enum: <code>"preserve"</code>

根拠: 価格やパック数を内容量へ取り違えることを防ぐ。
根拠(JSON): <code>"価格やパック数を内容量へ取り違えることを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-QUANTITY-001-1"</code> 前提: 価格198円だけ、または内容量不明の1パックを読み取った。条件: 食材候補を登録する。期待結果: 198円を198g等にせず、数量不明または1パック・内容量不明を保持する。数量不明を0と扱わない。。
  - criterion(JSON Object): <code>{"given":"価格198円だけ、または内容量不明の1パックを読み取った","id":"AC-REQ-SVC-QUANTITY-001-1","then":"198円を198g等にせず、数量不明または1パック・内容量不明を保持する。数量不明を0と扱わない。","when":"食材候補を登録する"}</code>
- <code>"AC-REQ-SVC-QUANTITY-001-2"</code> 前提: レシートの購入日や単位の異なる在庫がある。条件: 期限や必要量との差分を表示する。期待結果: 賞味期限・消費期限を購入日から推測せず、根拠のない個数/重量換算を行わず量を確認と表示する。。
  - criterion(JSON Object): <code>{"given":"レシートの購入日や単位の異なる在庫がある","id":"AC-REQ-SVC-QUANTITY-001-2","then":"賞味期限・消費期限を購入日から推測せず、根拠のない個数/重量換算を行わず量を確認と表示する。","when":"期限や必要量との差分を表示する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-RECEIPT-COMMIT-001: 選択済みの有効候補を一度だけ一括登録する

要件ID(JSON): <code>"REQ-SVC-RECEIPT-COMMIT-001"</code>
タイトル(JSON): <code>"選択済みの有効候補を一度だけ一括登録する"</code>
主体(JSON): <code>"レシート登録"</code>
対象(JSON): <code>"利用者が確認した食品候補の在庫追加"</code>
レシート登録は、利用者が確認した食品候補の在庫追加を**生成する**。
行為enum: <code>"generate"</code>

根拠: 確認操作と在庫変更を対応させ、二重押下や途中失敗による不整合を防ぐ。
根拠(JSON): <code>"確認操作と在庫変更を対応させ、二重押下や途中失敗による不整合を防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-RECEIPT-COMMIT-001-1"</code> 前提: 有効な食品候補を選択し件数が表示されている。条件: この内容で登録を押す。期待結果: 選択した候補だけを登録単位で一括追加し、登録日時と対象を追える。数量不明は許可し、選択中の食材名未確定は訂正または解除を求める。。
  - criterion(JSON Object): <code>{"given":"有効な食品候補を選択し件数が表示されている","id":"AC-REQ-SVC-RECEIPT-COMMIT-001-1","then":"選択した候補だけを登録単位で一括追加し、登録日時と対象を追える。数量不明は許可し、選択中の食材名未確定は訂正または解除を求める。","when":"この内容で登録を押す"}</code>
- <code>"AC-REQ-SVC-RECEIPT-COMMIT-001-2"</code> 前提: 同一の確定操作を再送する、または一括確定が失敗する。条件: 登録処理の結果を表示する。期待結果: 同じ登録は一度だけ追加し、一部成功を完了扱いしない。失敗時は再確認でき、成功時は追加件数と内容を表示する。。
  - criterion(JSON Object): <code>{"given":"同一の確定操作を再送する、または一括確定が失敗する","id":"AC-REQ-SVC-RECEIPT-COMMIT-001-2","then":"同じ登録は一度だけ追加し、一部成功を完了扱いしない。失敗時は再確認でき、成功時は追加件数と内容を表示する。","when":"登録処理の結果を表示する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-RECEIPT-DUPLICATE-001: 過去のレシート登録と重複を照合する

要件ID(JSON): <code>"REQ-SVC-RECEIPT-DUPLICATE-001"</code>
タイトル(JSON): <code>"過去のレシート登録と重複を照合する"</code>
主体(JSON): <code>"レシート登録"</code>
対象(JSON): <code>"重複の可能性がある買い物の確認"</code>
レシート登録は、重複の可能性がある買い物の確認を**提供する**。
行為enum: <code>"provide"</code>

根拠: 同じ画像の再登録と似た別の買い物を、利用者が区別できるようにする。
根拠(JSON): <code>"同じ画像の再登録と似た別の買い物を、利用者が区別できるようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-RECEIPT-DUPLICATE-001-1"</code> 前提: 同じ画像ハッシュまたは購入内容の署名に一致候補がある。条件: レシートを再度確定しようとする。期待結果: 登録済みの可能性と履歴入口を示し、登録日時・食品一覧・登録済み/取消済みを照合できる。。
  - criterion(JSON Object): <code>{"given":"同じ画像ハッシュまたは購入内容の署名に一致候補がある","id":"AC-REQ-SVC-RECEIPT-DUPLICATE-001-1","then":"登録済みの可能性と履歴入口を示し、登録日時・食品一覧・登録済み/取消済みを照合できる。","when":"レシートを再度確定しようとする"}</code>
- <code>"AC-REQ-SVC-RECEIPT-DUPLICATE-001-2"</code> 前提: 重複の可能性を表示している。条件: 利用者が同じ買い物、別の買い物、または判断できないと選ぶ。期待結果: 同じまたは不明なら登録をやめて在庫を確認でき、別なら明示確認で進める。取消済みの再登録でも現在の在庫確認を求め、全重複を検出する保証を表示しない。。
  - criterion(JSON Object): <code>{"given":"重複の可能性を表示している","id":"AC-REQ-SVC-RECEIPT-DUPLICATE-001-2","then":"同じまたは不明なら登録をやめて在庫を確認でき、別なら明示確認で進める。取消済みの再登録でも現在の在庫確認を求め、全重複を検出する保証を表示しない。","when":"利用者が同じ買い物、別の買い物、または判断できないと選ぶ"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-RECEIPT-UNDO-001: 今回登録の未消費残量だけを取り消す

要件ID(JSON): <code>"REQ-SVC-RECEIPT-UNDO-001"</code>
タイトル(JSON): <code>"今回登録の未消費残量だけを取り消す"</code>
主体(JSON): <code>"レシート履歴"</code>
対象(JSON): <code>"指定した登録単位の未消費在庫の取消"</code>
レシート履歴は、指定した登録単位の未消費在庫の取消を**実現する**。
行為enum: <code>"enable"</code>

根拠: 過去の在庫や使用履歴を壊さず、誤登録を後から戻せるようにする。
根拠(JSON): <code>"過去の在庫や使用履歴を壊さず、誤登録を後から戻せるようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-RECEIPT-UNDO-001-1"</code> 前提: 以前から500gあり、今回300gを別の登録単位で追加し今回分を100g使用した。条件: 履歴から今回の登録を取り消し、残量を確認して確定する。期待結果: 今回の残り200gだけを除去し、以前の500gと使用100gの履歴を保持する。。
  - criterion(JSON Object): <code>{"given":"以前から500gあり、今回300gを別の登録単位で追加し今回分を100g使用した","id":"AC-REQ-SVC-RECEIPT-UNDO-001-1","then":"今回の残り200gだけを除去し、以前の500gと使用100gの履歴を保持する。","when":"履歴から今回の登録を取り消し、残量を確認して確定する"}</code>
- <code>"AC-REQ-SVC-RECEIPT-UNDO-001-2"</code> 前提: 今回の追加分を編集済み、使い切り済み、削除済み、または数量不明である。条件: 取消前の内容を確認する。期待結果: 編集前後と現在残量を明示する。編集後250gなら250g、残量なしなら他在庫は変更せず、不明なら当該不明項目だけを外す。量を推測しない。。
  - criterion(JSON Object): <code>{"given":"今回の追加分を編集済み、使い切り済み、削除済み、または数量不明である","id":"AC-REQ-SVC-RECEIPT-UNDO-001-2","then":"編集前後と現在残量を明示する。編集後250gなら250g、残量なしなら他在庫は変更せず、不明なら当該不明項目だけを外す。量を推測しない。","when":"取消前の内容を確認する"}</code>
- <code>"AC-REQ-SVC-RECEIPT-UNDO-001-3"</code> 前提: 取消を確定した登録がある。条件: 同じ履歴を開いて再度取り消そうとする。期待結果: 取消済みの履歴を残し、同じ取消を再実行できない。取消対象は登録単位で一度だけ反映する。。
  - criterion(JSON Object): <code>{"given":"取消を確定した登録がある","id":"AC-REQ-SVC-RECEIPT-UNDO-001-3","then":"取消済みの履歴を残し、同じ取消を再実行できない。取消対象は登録単位で一度だけ反映する。","when":"同じ履歴を開いて再度取り消そうとする"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-FOOD-EDIT-001: 在庫の選択と編集を分ける

要件ID(JSON): <code>"REQ-SVC-FOOD-EDIT-001"</code>
タイトル(JSON): <code>"在庫の選択と編集を分ける"</code>
主体(JSON): <code>"冷蔵庫"</code>
対象(JSON): <code>"食材名と任意の数量・保存場所・優先状態"</code>
冷蔵庫は、食材名と任意の数量・保存場所・優先状態を**維持する**。
行為enum: <code>"maintain"</code>

根拠: 検索に使う食材を選ぶ操作と在庫を書き換える操作を混同しないようにする。
根拠(JSON): <code>"検索に使う食材を選ぶ操作と在庫を書き換える操作を混同しないようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-FOOD-EDIT-001-1"</code> 前提: 冷蔵庫に食材行がある。条件: 行本体または行内の編集を押す。期待結果: 行本体は検索用の選択を切り替え、独立した編集ボタンは選択を変えず編集画面を開く。。
  - criterion(JSON Object): <code>{"given":"冷蔵庫に食材行がある","id":"AC-REQ-SVC-FOOD-EDIT-001-1","then":"行本体は検索用の選択を切り替え、独立した編集ボタンは選択を変えず編集画面を開く。","when":"行本体または行内の編集を押す"}</code>
- <code>"AC-REQ-SVC-FOOD-EDIT-001-2"</code> 前提: 食材を手入力または編集する。条件: 名前と任意の数量、冷蔵/冷凍/常温、優先状態を確定する。期待結果: 名前だけでも登録でき、数量不明へ戻せる。削除は対象確認と取消導線を持ち、優先状態を期限切れと同義にしない。。
  - criterion(JSON Object): <code>{"given":"食材を手入力または編集する","id":"AC-REQ-SVC-FOOD-EDIT-001-2","then":"名前だけでも登録でき、数量不明へ戻せる。削除は対象確認と取消導線を持ち、優先状態を期限切れと同義にしない。","when":"名前と任意の数量、冷蔵/冷凍/常温、優先状態を確定する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-MEAL-001: 献立の料理ごとに人数を指定する

要件ID(JSON): <code>"REQ-SVC-MEAL-001"</code>
タイトル(JSON): <code>"献立の料理ごとに人数を指定する"</code>
主体(JSON): <code>"献立"</code>
対象(JSON): <code>"選んだ各料理と独立した人数・分量"</code>
献立は、選んだ各料理と独立した人数・分量を**維持する**。
行為enum: <code>"preserve"</code>

根拠: 主菜3人分と副菜2人分のように必要な量を料理ごとに決められるようにする。
根拠(JSON): <code>"主菜3人分と副菜2人分のように必要な量を料理ごとに決められるようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-MEAL-001-1"</code> 前提: 分量調整した料理を献立に加える。条件: 献立に追加を押す。期待結果: 料理と確定分量を引き継いで表示し、料理の追加・変更・除去を行える。。
  - criterion(JSON Object): <code>{"given":"分量調整した料理を献立に加える","id":"AC-REQ-SVC-MEAL-001-1","then":"料理と確定分量を引き継いで表示し、料理の追加・変更・除去を行える。","when":"献立に追加を押す"}</code>
- <code>"AC-REQ-SVC-MEAL-001-2"</code> 前提: 主菜と副菜を献立に入れている。条件: 主菜の加減ボタンまたは直接入力で3人、副菜を2人へ変更する。期待結果: 各料理に人数が表示され、変更していない料理の人数と分量は変わらない。。
  - criterion(JSON Object): <code>{"given":"主菜と副菜を献立に入れている","id":"AC-REQ-SVC-MEAL-001-2","then":"各料理に人数が表示され、変更していない料理の人数と分量は変わらない。","when":"主菜の加減ボタンまたは直接入力で3人、副菜を2人へ変更する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-MEAL-QUANTITY-001: 献立に必要な材料量を集計する

要件ID(JSON): <code>"REQ-SVC-MEAL-QUANTITY-001"</code>
タイトル(JSON): <code>"献立に必要な材料量を集計する"</code>
主体(JSON): <code>"献立の材料集計"</code>
対象(JSON): <code>"各料理の確定した原材料必要量"</code>
献立の材料集計は、各料理の確定した原材料必要量を**導出する**。
行為enum: <code>"derive"</code>

根拠: 別料理の同じ食材をまとめつつ、異なる単位や加工状態を根拠なく合算しないようにする。
根拠(JSON): <code>"別料理の同じ食材をまとめつつ、異なる単位や加工状態を根拠なく合算しないようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-MEAL-QUANTITY-001-1"</code> 前提: 料理別の人数・分量が確定している。条件: 買い物リストを開く、または献立を変更する。期待結果: 同一の食材・形態・換算可能な単位だけを合計し、必要量・手持ち・買う量を分けて更新する。付属材料を二重計上しない。。
  - criterion(JSON Object): <code>{"given":"料理別の人数・分量が確定している","id":"AC-REQ-SVC-MEAL-QUANTITY-001-1","then":"同一の食材・形態・換算可能な単位だけを合計し、必要量・手持ち・買う量を分けて更新する。付属材料を二重計上しない。","when":"買い物リストを開く、または献立を変更する"}</code>
- <code>"AC-REQ-SVC-MEAL-QUANTITY-001-2"</code> 前提: なす必要240gで手持ち不明、卵必要3個で手持ち1個、豆腐必要150gで手持ちなしである。条件: 不足表示を見る。期待結果: なすは量を確認、卵は買う2個、豆腐は買う150gと表示し、不明や換算不能を買い足し0と断定しない。。
  - criterion(JSON Object): <code>{"given":"なす必要240gで手持ち不明、卵必要3個で手持ち1個、豆腐必要150gで手持ちなしである","id":"AC-REQ-SVC-MEAL-QUANTITY-001-2","then":"なすは量を確認、卵は買う2個、豆腐は買う150gと表示し、不明や換算不能を買い足し0と断定しない。","when":"不足表示を見る"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-SHOPPING-001: 購入メモを在庫変更と分離する

要件ID(JSON): <code>"REQ-SVC-SHOPPING-001"</code>
タイトル(JSON): <code>"購入メモを在庫変更と分離する"</code>
主体(JSON): <code>"買い物リスト"</code>
対象(JSON): <code>"購入チェックと変更後の必要量"</code>
買い物リストは、購入チェックと変更後の必要量を**維持する**。
行為enum: <code>"maintain"</code>

根拠: 買い物中のメモ操作で在庫が二重追加されることを防ぐ。
根拠(JSON): <code>"買い物中のメモ操作で在庫が二重追加されることを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-SHOPPING-001-1"</code> 前提: 買い物項目が表示されている。条件: 行を押して購入チェックを付け外しする。期待結果: チェックだけを変更し、在庫は増減しない。在庫追加はレシートまたは実購入量を確認した手入力で行う。。
  - criterion(JSON Object): <code>{"given":"買い物項目が表示されている","id":"AC-REQ-SVC-SHOPPING-001-1","then":"チェックだけを変更し、在庫は増減しない。在庫追加はレシートまたは実購入量を確認した手入力で行う。","when":"行を押して購入チェックを付け外しする"}</code>
- <code>"AC-REQ-SVC-SHOPPING-001-2"</code> 前提: 購入チェック済みの項目がある。条件: 人数・献立変更で必要量が変わる、または項目がリストから外れる。期待結果: 必要量が変わった項目はチェックを解除し、外れた購入済み項目は以前の購入メモとして現行項目と分ける。。
  - criterion(JSON Object): <code>{"given":"購入チェック済みの項目がある","id":"AC-REQ-SVC-SHOPPING-001-2","then":"必要量が変わった項目はチェックを解除し、外れた購入済み項目は以前の購入メモとして現行項目と分ける。","when":"人数・献立変更で必要量が変わる、または項目がリストから外れる"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-COOK-PLAN-001: 作業可能な献立の段取りを示す

要件ID(JSON): <code>"REQ-SVC-COOK-PLAN-001"</code>
タイトル(JSON): <code>"作業可能な献立の段取りを示す"</code>
主体(JSON): <code>"調理の段取り"</code>
対象(JSON): <code>"確定した料理工程の実行順"</code>
調理の段取りは、確定した料理工程の実行順を**提供する**。
行為enum: <code>"provide"</code>

根拠: 複数料理を作るときに手順や器具の衝突を利用者へ押し付けないようにする。
根拠(JSON): <code>"複数料理を作るときに手順や器具の衝突を利用者へ押し付けないようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-COOK-PLAN-001-1"</code> 前提: 複数料理と使う器具の条件がある。条件: 段取りを見るを押す。期待結果: 材料量と各工程の依存順を守った調理順を提示し、同時使用できない器具や一人で両立しない作業を同時実行として指示しない。。
  - criterion(JSON Object): <code>{"given":"複数料理と使う器具の条件がある","id":"AC-REQ-SVC-COOK-PLAN-001-1","then":"材料量と各工程の依存順を守った調理順を提示し、同時使用できない器具や一人で両立しない作業を同時実行として指示しない。","when":"段取りを見るを押す"}</code>
- <code>"AC-REQ-SVC-COOK-PLAN-001-2"</code> 前提: 料理または人数・器具条件を変更した。条件: 段取りを確認する。期待結果: 変更後の条件で順番を再提示し、確定した段取りから調理を始められる。。
  - criterion(JSON Object): <code>{"given":"料理または人数・器具条件を変更した","id":"AC-REQ-SVC-COOK-PLAN-001-2","then":"変更後の条件で順番を再提示し、確定した段取りから調理を始められる。","when":"段取りを確認する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-COOK-RESUME-001: 中断した工程から調理を再開する

要件ID(JSON): <code>"REQ-SVC-COOK-RESUME-001"</code>
タイトル(JSON): <code>"中断した工程から調理を再開する"</code>
主体(JSON): <code>"調理画面"</code>
対象(JSON): <code>"選んだ料理の工程位置と完了状態"</code>
調理画面は、選んだ料理の工程位置と完了状態を**維持する**。
行為enum: <code>"preserve"</code>

根拠: 画面を離れても最初からやり直さず、誤って進めた工程へ戻れるようにする。
根拠(JSON): <code>"画面を離れても最初からやり直さず、誤って進めた工程へ戻れるようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-COOK-RESUME-001-1"</code> 前提: 調理中に次へ、戻る、中断を操作した。条件: ホーム上部または献立の調理を再開を押す。期待結果: 料理名と工程番号を示して保存した位置へ復帰し、完了済み状態を維持する。。
  - criterion(JSON Object): <code>{"given":"調理中に次へ、戻る、中断を操作した","id":"AC-REQ-SVC-COOK-RESUME-001-1","then":"料理名と工程番号を示して保存した位置へ復帰し、完了済み状態を維持する。","when":"ホーム上部または献立の調理を再開を押す"}</code>
- <code>"AC-REQ-SVC-COOK-RESUME-001-2"</code> 前提: 次へを押しすぎた。条件: 戻るで前の工程を表示する。期待結果: 前の工程へ戻り、工程を移動しただけでは在庫を増減しない。。
  - criterion(JSON Object): <code>{"given":"次へを押しすぎた","id":"AC-REQ-SVC-COOK-RESUME-001-2","then":"前の工程へ戻り、工程を移動しただけでは在庫を増減しない。","when":"戻るで前の工程を表示する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-COOK-TIMER-001: 起動済みタイマーを重複させず保持する

要件ID(JSON): <code>"REQ-SVC-COOK-TIMER-001"</code>
タイトル(JSON): <code>"起動済みタイマーを重複させず保持する"</code>
主体(JSON): <code>"調理タイマー"</code>
対象(JSON): <code>"起動したタイマーとその経過状態"</code>
調理タイマーは、起動したタイマーとその経過状態を**維持する**。
行為enum: <code>"preserve"</code>

根拠: 工程移動や再開で同じタイマーが増え、誤った残時間を伝えることを防ぐ。
根拠(JSON): <code>"工程移動や再開で同じタイマーが増え、誤った残時間を伝えることを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-COOK-TIMER-001-1"</code> 前提: 工程に起動済みタイマーがある。条件: 工程を戻る、再訪する、または調理を再開する。期待結果: 既存タイマーの状態を引き継ぎ、同じタイマーを自動で重複起動しない。。
  - criterion(JSON Object): <code>{"given":"工程に起動済みタイマーがある","id":"AC-REQ-SVC-COOK-TIMER-001-1","then":"既存タイマーの状態を引き継ぎ、同じタイマーを自動で重複起動しない。","when":"工程を戻る、再訪する、または調理を再開する"}</code>
- <code>"AC-REQ-SVC-COOK-TIMER-001-2"</code> 前提: タイマーを提供するDev版を使う。条件: 提供状態を確認し画面を閉じて再開する。期待結果: 画面外・再開時・音の動作条件が説明と一致し、終了していた場合に新しい全時間のタイマーとして再起動しない。。
  - criterion(JSON Object): <code>{"given":"タイマーを提供するDev版を使う","id":"AC-REQ-SVC-COOK-TIMER-001-2","then":"画面外・再開時・音の動作条件が説明と一致し、終了していた場合に新しい全時間のタイマーとして再起動しない。","when":"提供状態を確認し画面を閉じて再開する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-STOCK-CONSENT-001: 利用者が選んだ完了時だけ使用量を引く

要件ID(JSON): <code>"REQ-SVC-STOCK-CONSENT-001"</code>
タイトル(JSON): <code>"利用者が選んだ完了時だけ使用量を引く"</code>
主体(JSON): <code>"調理完了"</code>
対象(JSON): <code>"同単位で量が足りる在庫への確認済み使用量の反映"</code>
調理完了は、同単位で量が足りる在庫への確認済み使用量の反映を**制約する**。
行為enum: <code>"constrain"</code>

根拠: 完成操作だけで不明な在庫を推測して減らすことを防ぐ。
根拠(JSON): <code>"完成操作だけで不明な在庫を推測して減らすことを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-STOCK-CONSENT-001-1"</code> 前提: 調理完了画面を開いた。条件: 在庫から使用量を引くを選ばず完了する。期待結果: 減算チェックは初期OFFで、在庫を変更しない。。
  - criterion(JSON Object): <code>{"given":"調理完了画面を開いた","id":"AC-REQ-SVC-STOCK-CONSENT-001-1","then":"減算チェックは初期OFFで、在庫を変更しない。","when":"在庫から使用量を引くを選ばず完了する"}</code>
- <code>"AC-REQ-SVC-STOCK-CONSENT-001-2"</code> 前提: 利用者が実使用量を編集し減算へ明示同意した。条件: 完了を確定する。期待結果: 同じ単位で十分な在庫がある材料だけを一度引く。不明・不足・換算不可は理由を表示し変更しない。反映した材料と見送った材料を表示する。。
  - criterion(JSON Object): <code>{"given":"利用者が実使用量を編集し減算へ明示同意した","id":"AC-REQ-SVC-STOCK-CONSENT-001-2","then":"同じ単位で十分な在庫がある材料だけを一度引く。不明・不足・換算不可は理由を表示し変更しない。反映した材料と見送った材料を表示する。","when":"完了を確定する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-EXCLUSION-001: 除外食材を検索と偶然の一品へ適用する

要件ID(JSON): <code>"REQ-SVC-EXCLUSION-001"</code>
タイトル(JSON): <code>"除外食材を検索と偶然の一品へ適用する"</code>
主体(JSON): <code>"候補選定"</code>
対象(JSON): <code>"利用者が指定した食べられない食材の条件"</code>
候補選定は、利用者が指定した食べられない食材の条件を**強制する**。
行為enum: <code>"enforce"</code>

根拠: 入口によって除外条件が失われ、意図しない食品を提案することを防ぐ。
根拠(JSON): <code>"入口によって除外条件が失われ、意図しない食品を提案することを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-EXCLUSION-001-1"</code> 前提: 食べられない食材を設定している。条件: 検索・アレンジ・偶然の一品を開く。期待結果: すべての候補入口で除外条件を守り、候補0件でも無断解除しない。。
  - criterion(JSON Object): <code>{"given":"食べられない食材を設定している","id":"AC-REQ-SVC-EXCLUSION-001-1","then":"すべての候補入口で除外条件を守り、候補0件でも無断解除しない。","when":"検索・アレンジ・偶然の一品を開く"}</code>
- <code>"AC-REQ-SVC-EXCLUSION-001-2"</code> 前提: 加工食品の構成原料を確認できない。条件: 除外条件に対する候補の適合状態を見る。期待結果: 原材料未確認を示し、除外済み・安全確認済みと断定しない。。
  - criterion(JSON Object): <code>{"given":"加工食品の構成原料を確認できない","id":"AC-REQ-SVC-EXCLUSION-001-2","then":"原材料未確認を示し、除外済み・安全確認済みと断定しない。","when":"除外条件に対する候補の適合状態を見る"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-BACKUP-001: 検証したバックアップで端末データを復元する

要件ID(JSON): <code>"REQ-SVC-BACKUP-001"</code>
タイトル(JSON): <code>"検証したバックアップで端末データを復元する"</code>
主体(JSON): <code>"データ管理"</code>
対象(JSON): <code>"利用者が指定したバックアップ内容による現在データの置換"</code>
データ管理は、利用者が指定したバックアップ内容による現在データの置換を**実現する**。
行為enum: <code>"enable"</code>

根拠: 同期のない試用版でも持ち出しと復元を行い、不正ファイルによるデータ消失を防ぐ。
根拠(JSON): <code>"同期のない試用版でも持ち出しと復元を行い、不正ファイルによるデータ消失を防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-BACKUP-001-1"</code> 前提: このブラウザの利用データがある。条件: 設定からデータを書き出す。期待結果: 対応するJSONバックアップを保存でき、持ち出す内容と復元の方法が分かる。。
  - criterion(JSON Object): <code>{"given":"このブラウザの利用データがある","id":"AC-REQ-SVC-BACKUP-001-1","then":"対応するJSONバックアップを保存でき、持ち出す内容と復元の方法が分かる。","when":"設定からデータを書き出す"}</code>
- <code>"AC-REQ-SVC-BACKUP-001-2"</code> 前提: バックアップを選択した。条件: データを読み込む。期待結果: 形式・版・参照関係・数量を検証し、件数と置換対象を表示して確認後に全置換する。合算しない。不正ファイルや確認キャンセルでは現在データを変更しない。。
  - criterion(JSON Object): <code>{"given":"バックアップを選択した","id":"AC-REQ-SVC-BACKUP-001-2","then":"形式・版・参照関係・数量を検証し、件数と置換対象を表示して確認後に全置換する。合算しない。不正ファイルや確認キャンセルでは現在データを変更しない。","when":"データを読み込む"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-PRIVACY-001: 読取画像と全文を永続保存しない

要件ID(JSON): <code>"REQ-SVC-PRIVACY-001"</code>
タイトル(JSON): <code>"読取画像と全文を永続保存しない"</code>
主体(JSON): <code>"レシートデータ管理"</code>
対象(JSON): <code>"確認のため一時的に保持した画像とOCR全文の保存期間"</code>
レシートデータ管理は、確認のため一時的に保持した画像とOCR全文の保存期間を**制約する**。
行為enum: <code>"constrain"</code>

根拠: レシートの個人情報を在庫登録に不要な形で残さないようにする。
根拠(JSON): <code>"レシートの個人情報を在庫登録に不要な形で残さないようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `data`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-REQ-SVC-PRIVACY-001-1"</code> 前提: レシートを読み取っている。条件: 登録・キャンセル・画面終了が完了する。期待結果: 画像とOCR全文をメモリから破棄し、店舗名・レシート上の購入日時を永続保存しない。選択前から端末にある写真は削除しない。。
  - criterion(JSON Object): <code>{"given":"レシートを読み取っている","id":"AC-REQ-SVC-PRIVACY-001-1","then":"画像とOCR全文をメモリから破棄し、店舗名・レシート上の購入日時を永続保存しない。選択前から端末にある写真は削除しない。","when":"登録・キャンセル・画面終了が完了する"}</code>
- <code>"AC-REQ-SVC-PRIVACY-001-2"</code> 前提: 登録履歴と保存データを確認する。条件: 端末内の永続データを検査する。期待結果: 食材・数量・単位・登録日時・登録ID・画像ハッシュ・購入内容署名・必要な状態履歴だけを保存し、元画像や全文を復元できる形で保持しない。。
  - criterion(JSON Object): <code>{"given":"登録履歴と保存データを確認する","id":"AC-REQ-SVC-PRIVACY-001-2","then":"食材・数量・単位・登録日時・登録ID・画像ハッシュ・購入内容署名・必要な状態履歴だけを保存し、元画像や全文を復元できる形で保持しない。","when":"端末内の永続データを検査する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-BOOKMARK-001: 料理のしおりと分量下書きを区別する

要件ID(JSON): <code>"REQ-SVC-BOOKMARK-001"</code>
タイトル(JSON): <code>"料理のしおりと分量下書きを区別する"</code>
主体(JSON): <code>"保存機能"</code>
対象(JSON): <code>"料理IDに対するしおり"</code>
保存機能は、料理IDに対するしおりを**維持する**。
行為enum: <code>"preserve"</code>

根拠: 保存した料理と今回調整した量の意味を混同しないようにする。
根拠(JSON): <code>"保存した料理と今回調整した量の意味を混同しないようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-BOOKMARK-001-1"</code> 前提: 料理詳細を開いている。条件: 保存する、または保存済みを解除する。期待結果: 料理IDのしおりを付け外しし、解除直後に取り消せる。しおり操作だけで在庫や献立は変更しない。。
  - criterion(JSON Object): <code>{"given":"料理詳細を開いている","id":"AC-REQ-SVC-BOOKMARK-001-1","then":"料理IDのしおりを付け外しし、解除直後に取り消せる。しおり操作だけで在庫や献立は変更しない。","when":"保存する、または保存済みを解除する"}</code>
- <code>"AC-REQ-SVC-BOOKMARK-001-2"</code> 前提: 個別分量の下書きがある。条件: 保存一覧から料理を開き直す。期待結果: 同じブラウザの下書きは別に保持され、しおり自体が分量セットでないことが説明される。公開終了した料理は理由を表示する。。
  - criterion(JSON Object): <code>{"given":"個別分量の下書きがある","id":"AC-REQ-SVC-BOOKMARK-001-2","then":"同じブラウザの下書きは別に保持され、しおり自体が分量セットでないことが説明される。公開終了した料理は理由を表示する。","when":"保存一覧から料理を開き直す"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-GUIDE-001: 切り方ガイドから同じ工程へ戻す

要件ID(JSON): <code>"REQ-SVC-GUIDE-001"</code>
タイトル(JSON): <code>"切り方ガイドから同じ工程へ戻す"</code>
主体(JSON): <code>"技法ガイド"</code>
対象(JSON): <code>"調理工程で参照した切り方"</code>
技法ガイドは、調理工程で参照した切り方を**提供する**。
行為enum: <code>"provide"</code>

根拠: 用語が分からないため調理を中断したり、工程位置を見失うことを防ぐ。
根拠(JSON): <code>"用語が分からないため調理を中断したり、工程位置を見失うことを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-REQ-SVC-GUIDE-001-1"</code> 前提: 調理中の工程に切り方の説明がある。条件: 切り方を見るを押して閉じる。期待結果: 図・文章または提供済み動画で説明を確認でき、閉じると同じ料理の同じ工程へ戻る。。
  - criterion(JSON Object): <code>{"given":"調理中の工程に切り方の説明がある","id":"AC-REQ-SVC-GUIDE-001-1","then":"図・文章または提供済み動画で説明を確認でき、閉じると同じ料理の同じ工程へ戻る。","when":"切り方を見るを押して閉じる"}</code>
- <code>"AC-REQ-SVC-GUIDE-001-2"</code> 前提: 動画等の案内を取得できない。条件: ガイドを開く。期待結果: 図や文章の説明へ切り替えられ、未提供動画を再生済みや提供済みと表示しない。。
  - criterion(JSON Object): <code>{"given":"動画等の案内を取得できない","id":"AC-REQ-SVC-GUIDE-001-2","then":"図や文章の説明へ切り替えられ、未提供動画を再生済みや提供済みと表示しない。","when":"ガイドを開く"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-CAPABILITY-001: Devの提供範囲と将来のAWS同期を区別する

要件ID(JSON): <code>"REQ-SVC-CAPABILITY-001"</code>
タイトル(JSON): <code>"Devの提供範囲と将来のAWS同期を区別する"</code>
主体(JSON): <code>"提供状態表示"</code>
対象(JSON): <code>"実際に利用できる機能と未提供機能"</code>
提供状態表示は、実際に利用できる機能と未提供機能を**提供する**。
行為enum: <code>"provide"</code>

根拠: 仮想レビューや静的画像を実装成功と誤認せず、利用者が試せる範囲を判断できるようにする。
根拠(JSON): <code>"仮想レビューや静的画像を実装成功と誤認せず、利用者が試せる範囲を判断できるようにする。"</code>

項目版: 1 / 状態: `active` / 種別: `quality`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-REQ-SVC-CAPABILITY-001-1"</code> 前提: 初期Devを公開する。条件: 画面とマニュアルの提供表を確認する。期待結果: 8品のサンプル、端末内OCR、同じブラウザの保存範囲、タイマー等の実確認した動作を記載し、AWSによる認証・同期は未提供と明示する。。
  - criterion(JSON Object): <code>{"given":"初期Devを公開する","id":"AC-REQ-SVC-CAPABILITY-001-1","then":"8品のサンプル、端末内OCR、同じブラウザの保存範囲、タイマー等の実確認した動作を記載し、AWSによる認証・同期は未提供と明示する。","when":"画面とマニュアルの提供表を確認する"}</code>
- <code>"AC-REQ-SVC-CAPABILITY-001-2"</code> 前提: 設計図やエージェントの机上レビューだけがある。条件: 提供済み表示または受入記録を更新する。期待結果: 実装や実利用者テストの成功証拠へ読み替えない。設計対象・実装済み・検証済みを区別し、未提供ボタンで偽の完了を示さない。。
  - criterion(JSON Object): <code>{"given":"設計図やエージェントの机上レビューだけがある","id":"AC-REQ-SVC-CAPABILITY-001-2","then":"実装や実利用者テストの成功証拠へ読み替えない。設計対象・実装済み・検証済みを区別し、未提供ボタンで偽の完了を示さない。","when":"提供済み表示または受入記録を更新する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-service","docs/service/manual.md","docs/service/faq.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SVC-PAGES-001: 検査したDev版をGitHub Pagesで閲覧可能にする

要件ID(JSON): <code>"REQ-SVC-PAGES-001"</code>
タイトル(JSON): <code>"検査したDev版をGitHub Pagesで閲覧可能にする"</code>
主体(JSON): <code>"開発配布工程"</code>
対象(JSON): <code>"検査対象の変更版と対応したDevプレビュー"</code>
開発配布工程は、検査対象の変更版と対応したDevプレビューを**提供する**。
行為enum: <code>"provide"</code>

根拠: ユーザーが依頼したGitHub Pages上で、変更結果を継続して確認できる状態にする。
根拠(JSON): <code>"ユーザーが依頼したGitHub Pages上で、変更結果を継続して確認できる状態にする。"</code>

項目版: 1 / 状態: `active` / 種別: `operational`
変更識別子: <code>"service-spec:2026-09-05:review2"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-REQ-SVC-PAGES-001-1"</code> 前提: Dev版を配布する変更がある。条件: GitHubのCIを実行する。期待結果: 変更と受入条件に関係する検査、ビルド、生成要件のdrift確認を行い、失敗した版を成功した配布として報告しない。。
  - criterion(JSON Object): <code>{"given":"Dev版を配布する変更がある","id":"AC-REQ-SVC-PAGES-001-1","then":"変更と受入条件に関係する検査、ビルド、生成要件のdrift確認を行い、失敗した版を成功した配布として報告しない。","when":"GitHubのCIを実行する"}</code>
- <code>"AC-REQ-SVC-PAGES-001-2"</code> 前提: 必要な検査とビルドが成功した。条件: Dev版を公開しURLを確認する。期待結果: その変更版をGitHub Pagesで閲覧でき、配布版識別・URL・検査結果を追跡できる。公開を確認していなければ確認済みとしない。。
  - criterion(JSON Object): <code>{"given":"必要な検査とビルドが成功した","id":"AC-REQ-SVC-PAGES-001-2","then":"その変更版をGitHub Pagesで閲覧でき、配布版識別・URL・検査結果を追跡できる。公開を確認していなければ確認済みとしない。","when":"Dev版を公開しURLを確認する"}</code>

要求源(JSON List): <code>["user:2026-09-05:recipeweave-dev-pages","docs/service/manual.md"]</code>
検証方法: 対応する受入条件の自動検査と画面操作確認
検証証跡: docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。
検証(JSON Object): <code>{"evidence":"docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。","method":"対応する受入条件の自動検査と画面操作確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/service/manual.md","docs/service/screens-and-flows.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DEV-ARCH-001: 採用ADRに従うWeb・API・AWS構成を提供する

要件ID(JSON): <code>"REQ-DEV-ARCH-001"</code>
タイトル(JSON): <code>"採用ADRに従うWeb・API・AWS構成を提供する"</code>
主体(JSON): <code>"RecipeWeaveの開発基盤"</code>
対象(JSON): <code>"ADR-0001で採用した構成に従う実装プロファイル"</code>
RecipeWeaveの開発基盤は、ADR-0001で採用した構成に従う実装プロファイルを**提供する**。
行為enum: <code>"provide"</code>

根拠: CornellNoteWebの既知の開発方針へおおむね合わせるという依頼を、採用済みADRの構成として検証可能に固定する。未確認の別会話全体への完全準拠は主張しない。
根拠(JSON): <code>"CornellNoteWebの既知の開発方針へおおむね合わせるという依頼を、採用済みADRの構成として検証可能に固定する。未確認の別会話全体への完全準拠は主張しない。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"dev-profile:2026-09-05:adr0001"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-REQ-DEV-ARCH-001-1"</code> 前提: 採用ADRに従うWebとAPIの実装がある。条件: ビルドと構成を確認する。期待結果: フロントエンドはSvelte・TypeScriptによる静的Web、APIはFastAPIを基盤とし、CloudFront/S3からAPI Gateway HTTP API・Lambdaを経由してAurora DSQLへ接続する構成をコードとして提供する。。
  - criterion(JSON Object): <code>{"given":"採用ADRに従うWebとAPIの実装がある","id":"AC-REQ-DEV-ARCH-001-1","then":"フロントエンドはSvelte・TypeScriptによる静的Web、APIはFastAPIを基盤とし、CloudFront/S3からAPI Gateway HTTP API・Lambdaを経由してAurora DSQLへ接続する構成をコードとして提供する。","when":"ビルドと構成を確認する"}</code>
- <code>"AC-REQ-DEV-ARCH-001-2"</code> 前提: AWS向けの利用者状態APIを構成する。条件: 認証設定と利用者を変えて状態の読書きを検証する。期待結果: Cognito access JWTで利用者を特定し、署名・issuer・期限・token_use・client_idを検証する。任意の利用者IDヘッダーを信用せず、別利用者の状態を取得更新できない。認証未設定時は状態APIを閉じ、版競合は無条件上書きしない。。
  - criterion(JSON Object): <code>{"given":"AWS向けの利用者状態APIを構成する","id":"AC-REQ-DEV-ARCH-001-2","then":"Cognito access JWTで利用者を特定し、署名・issuer・期限・token_use・client_idを検証する。任意の利用者IDヘッダーを信用せず、別利用者の状態を取得更新できない。認証未設定時は状態APIを閉じ、版競合は無条件上書きしない。","when":"認証設定と利用者を変えて状態の読書きを検証する"}</code>
- <code>"AC-REQ-DEV-ARCH-001-3"</code> 前提: PagesのDev版とAWS向けコードが存在する。条件: 利用者への提供状態と配備状態を確認する。期待結果: Pagesはログイン不要・このブラウザの端末保存として提供する。AWS向けのコード・合成・検証の存在を実配備や同期提供の成功へ読み替えず、AWS未配備ならAWS実環境の受入は未完了と記録する。。
  - criterion(JSON Object): <code>{"given":"PagesのDev版とAWS向けコードが存在する","id":"AC-REQ-DEV-ARCH-001-3","then":"Pagesはログイン不要・このブラウザの端末保存として提供する。AWS向けのコード・合成・検証の存在を実配備や同期提供の成功へ読み替えず、AWS未配備ならAWS実環境の受入は未完了と記録する。","when":"利用者への提供状態と配備状態を確認する"}</code>

要求源(JSON List): <code>["user:2026-09-05:cornellnoteweb-architecture","docs/design/ADR-0001-service-dev.md","docs/service/overview.md"]</code>
検証方法: 構成コード・API契約の検査、認証と利用者分離の対象試験、実配備記録の照合
検証証跡: 採用済みADR-0001を要求源とする。構成の実装完成・対象試験・AWS実配備の受入証跡はこの要件追加時点では未登録。
検証(JSON Object): <code>{"evidence":"採用済みADR-0001を要求源とする。構成の実装完成・対象試験・AWS実配備の受入証跡はこの要件追加時点では未登録。","method":"構成コード・API契約の検査、認証と利用者分離の対象試験、実配備記録の照合"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/design/ADR-0001-service-dev.md","docs/service/overview.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DEV-QUALITY-001: 配備・移行・生成設計の検証契約を維持する

要件ID(JSON): <code>"REQ-DEV-QUALITY-001"</code>
タイトル(JSON): <code>"配備・移行・生成設計の検証契約を維持する"</code>
主体(JSON): <code>"RecipeWeaveの開発工程"</code>
対象(JSON): <code>"採用した配備とデータ移行に対応する再現可能な検証証跡"</code>
RecipeWeaveの開発工程は、採用した配備とデータ移行に対応する再現可能な検証証跡を**維持する**。
行為enum: <code>"maintain"</code>

根拠: インフラやDB移行をコードと検査で扱い、実装と設計文書の乖離、およびローカル検査と実環境受入の混同を防ぐ。
根拠(JSON): <code>"インフラやDB移行をコードと検査で扱い、実装と設計文書の乖離、およびローカル検査と実環境受入の混同を防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `operational`
変更識別子: <code>"dev-profile:2026-09-05:adr0001"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-REQ-DEV-QUALITY-001-1"</code> 前提: AWS構成を変更する。条件: CDK合成・配備パッケージ・権限を検査する。期待結果: CDKで構成を再現でき、必要な配布物を生成する。アプリ用とマイグレーション用のIAM/DB権限を分離し、用途に必要な権限に限定する。認証情報をコード・生成設計・ログへ埋め込まない。。
  - criterion(JSON Object): <code>{"given":"AWS構成を変更する","id":"AC-REQ-DEV-QUALITY-001-1","then":"CDKで構成を再現でき、必要な配布物を生成する。アプリ用とマイグレーション用のIAM/DB権限を分離し、用途に必要な権限に限定する。認証情報をコード・生成設計・ログへ埋め込まない。","when":"CDK合成・配備パッケージ・権限を検査する"}</code>
- <code>"AC-REQ-DEV-QUALITY-001-2"</code> 前提: DSQLのスキーマまたは利用する索引を変更する。条件: 版管理したマイグレーションを実行・再実行する。期待結果: 適用済み状態を追跡し、DDLを一文ずつ別トランザクションで扱いDMLと混在させない。非同期の索引作成は完了を確認し、競合の再試行を有界にして同じ業務操作を二重適用しない。。
  - criterion(JSON Object): <code>{"given":"DSQLのスキーマまたは利用する索引を変更する","id":"AC-REQ-DEV-QUALITY-001-2","then":"適用済み状態を追跡し、DDLを一文ずつ別トランザクションで扱いDMLと混在させない。非同期の索引作成は完了を確認し、競合の再試行を有界にして同じ業務操作を二重適用しない。","when":"版管理したマイグレーションを実行・再実行する"}</code>
- <code>"AC-REQ-DEV-QUALITY-001-3"</code> 前提: Web・API・DB・インフラの実装がある。条件: 設計文書の生成と差分検査を実行する。期待結果: 現存するコード・OpenAPI・SQL・CDK合成結果から現在状態の設計を決定的に生成し、同一入力の再生成で差分がなく、実装変更によるdriftを検出する。手編集の生成文書で差分を隠さない。。
  - criterion(JSON Object): <code>{"given":"Web・API・DB・インフラの実装がある","id":"AC-REQ-DEV-QUALITY-001-3","then":"現存するコード・OpenAPI・SQL・CDK合成結果から現在状態の設計を決定的に生成し、同一入力の再生成で差分がなく、実装変更によるdriftを検出する。手編集の生成文書で差分を隠さない。","when":"設計文書の生成と差分検査を実行する"}</code>
- <code>"AC-REQ-DEV-QUALITY-001-4"</code> 前提: 型検査・ローカル試験・CDK合成・マイグレーション試験または配備を行う。条件: 受入記録を更新する。期待結果: 対象版、検査内容、結果、実行環境を対応させる。コード検査・ローカル代替・AWS実配備・実環境認証同期を区別し、未配備または未実施の実環境項目を合格にしない。。
  - criterion(JSON Object): <code>{"given":"型検査・ローカル試験・CDK合成・マイグレーション試験または配備を行う","id":"AC-REQ-DEV-QUALITY-001-4","then":"対象版、検査内容、結果、実行環境を対応させる。コード検査・ローカル代替・AWS実配備・実環境認証同期を区別し、未配備または未実施の実環境項目を合格にしない。","when":"受入記録を更新する"}</code>

要求源(JSON List): <code>["user:2026-09-05:cornellnoteweb-development","docs/design/ADR-0001-service-dev.md","AGENTS.md"]</code>
検証方法: CDKと移行の対象検査、生成設計の再生成/drift確認、版に対応する受入証跡のレビュー
検証証跡: 採用済みADR-0001と既存AGENTSの三つの開発規約を要求源とする。実装・試験traceは実装完成後に存在と結果を確認して登録する。
検証(JSON Object): <code>{"evidence":"採用済みADR-0001と既存AGENTSの三つの開発規約を要求源とする。実装・試験traceは実装完成後に存在と結果を確認して登録する。","method":"CDKと移行の対象検査、生成設計の再生成/drift確認、版に対応する受入証跡のレビュー"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/design/ADR-0001-service-dev.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>
