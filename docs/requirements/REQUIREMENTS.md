<!-- tools/quintflow.pyによる自動生成。spec/requirements/requirements.qntを編集すること。 -->
# RecipeWeave 要件一覧

- スキーマ版: 1
- カタログ版: 1
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
