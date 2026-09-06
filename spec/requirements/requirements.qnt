// 永続要件の一次言語。JSONとMarkdownはこの仕様から生成する。
module requirements {
  type AcceptanceCriterion = { id: str, given: str, when_: str, expected: str }
  type Verification = { method: str, evidence: str }
  type Traces = {
    design: List[str],
    implementation: List[str],
    tests: List[str],
    standards: List[str],
  }
  type Requirement = {
    id: str,
    revision: int,
    status: str,
    kind: str,
    title: str,
    subject: str,
    actionName: str,
    objectName: str,
    rationale: str,
    sourceRefs: List[str],
    acceptanceCriteria: List[AcceptanceCriterion],
    verification: Verification,
    traces: Traces,
    lastChangedBy: str,
    retirementReason: str,
    supersededBy: str,
    scopeName: str,
    categoryName: str,
  }
  type Catalog = {
    schemaVersion: int,
    catalogRevision: int,
    product: str,
    updatedAt: str,
    requirements: List[Requirement],
  }
  type RequirementOperation = {
    kind: str,
    id: str,
    expectedRevision: int,
    replacement: Requirement,
  }
  type BatchFold = {
    requirements: List[Requirement],
    touchedIds: List[str],
    valid: bool,
  }
  type Lifecycle = {
    catalogRevision: int,
    itemRevision: int,
    itemPresent: bool,
    itemStatus: str,
    traceRevision: int,
    priorCatalogRevision: int,
    priorItemRevision: int,
    priorItemPresent: bool,
    priorItemStatus: str,
    priorTraceRevision: int,
    lastOperation: str,
  }

  pure val requirementsSource: Catalog = {
    schemaVersion: 1,
    catalogRevision: 4,
    product: "RecipeWeave",
    updatedAt: "2026-09-06",
    requirements: [
      {
        id: "REQ-DOMAIN-001",
        revision: 1,
        status: "active",
        kind: "functional",
        title: "semantic food identity",
        subject: "食品意味特徴量",
        actionName: "preserve",
        objectName: "food semantic identity",
        rationale: "食材の意味的な多様性をSKU表記の多さと混同せず、組合せ設計の対象にする。",
        sourceRefs: ["user:2026-09-05", "README.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-DOMAIN-001-1", given: "RecipeWeaveの宣言入力がある", when_: "受入検査を実行する", expected: "SKU濃度を独立指標として保持し、food semantic coverageと分けて評価する。" }
        ],
        verification: { method: "自動検査とartifact review", evidence: "moon task and targeted tests" },
        traces: {
          design: ["docs/design/generated/README.md"],
          implementation: ["packages/generator/pyproject.toml"],
          tests: ["tests/README.md"],
          standards: ["DEVSTD-AS-BUILT", "QUINT-0.32"],
        },
        lastChangedBy: "bootstrap:recipeweave",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "functional",
      },
      {
        id: "REQ-ENUM-001",
        revision: 1,
        status: "active",
        kind: "functional",
        title: "deterministic unique enumeration",
        subject: "組合せ列挙器",
        actionName: "preserve",
        objectName: "重複のない決定的な組合せ列",
        rationale: "再実行・並列化・入力順の同値変換でも安定した順序と一意な識別子を得る必要がある。",
        sourceRefs: ["user:2026-09-05", "README.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-ENUM-001-1", given: "RecipeWeaveの宣言入力がある", when_: "受入検査を実行する", expected: "列挙結果を正規化キーで重複排除し、同一入力の結果をバイト比較する。" }
        ],
        verification: { method: "自動検査とartifact review", evidence: "moon task and targeted tests" },
        traces: {
          design: ["docs/design/generated/README.md"],
          implementation: ["packages/generator/pyproject.toml"],
          tests: ["tests/README.md"],
          standards: ["DEVSTD-AS-BUILT", "QUINT-0.32"],
        },
        lastChangedBy: "bootstrap:recipeweave",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "functional",
      },
      {
        id: "REQ-OUTPUT-001",
        revision: 1,
        status: "active",
        kind: "functional",
        title: "complete output manifest and resume",
        subject: "出力器",
        actionName: "preserve",
        objectName: "全量出力・SHA256 manifest・再開位置",
        rationale: "大量結果は一部成功を成功扱いせず、欠落を検出して再開できなければならない。",
        sourceRefs: ["user:2026-09-05", "README.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-OUTPUT-001-1", given: "RecipeWeaveの宣言入力がある", when_: "受入検査を実行する", expected: "結果チャンク、件数、SHA256、入力digest、再開cursorをmanifestへ記録する。" }
        ],
        verification: { method: "自動検査とartifact review", evidence: "moon task and targeted tests" },
        traces: {
          design: ["docs/design/generated/README.md"],
          implementation: ["packages/generator/pyproject.toml"],
          tests: ["tests/README.md"],
          standards: ["DEVSTD-AS-BUILT", "QUINT-0.32"],
        },
        lastChangedBy: "bootstrap:recipeweave",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "functional",
      },
      {
        id: "REQ-PERF-001",
        revision: 1,
        status: "active",
        kind: "functional",
        title: "future ten million target",
        subject: "組合せ実行基盤",
        actionName: "preserve",
        objectName: "将来一千万件規模へ拡張可能な実行契約",
        rationale: "初期データでの実績と将来目標を混同せず、ボトルネックを測定可能にする。",
        sourceRefs: ["user:2026-09-05", "README.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-PERF-001-1", given: "RecipeWeaveの宣言入力がある", when_: "受入検査を実行する", expected: "ベンチマークは件数と時間を記録し、10m目標は未達なら未実装・未達として報告する。" }
        ],
        verification: { method: "自動検査とartifact review", evidence: "moon task and targeted tests" },
        traces: {
          design: ["docs/design/generated/README.md"],
          implementation: ["packages/generator/pyproject.toml"],
          tests: ["tests/README.md"],
          standards: ["DEVSTD-AS-BUILT", "QUINT-0.32"],
        },
        lastChangedBy: "bootstrap:recipeweave",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "functional",
      },
      {
        id: "REQ-EVAL-001",
        revision: 1,
        status: "active",
        kind: "functional",
        title: "blind independent Luna evaluation",
        subject: "評価実験",
        actionName: "preserve",
        objectName: "blind independent Luna標本評価",
        rationale: "評価者の独立性と物理的な食味評価を、モデルの意味特徴やSKU評価と区別する。",
        sourceRefs: ["user:2026-09-05", "README.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-EVAL-001-1", given: "RecipeWeaveの宣言入力がある", when_: "受入検査を実行する", expected: "標本割当を盲検化し、Luna標本の手順・識別子・評価を別artifactとして固定する。" }
        ],
        verification: { method: "自動検査とartifact review", evidence: "moon task and targeted tests" },
        traces: {
          design: ["docs/design/generated/README.md"],
          implementation: ["packages/generator/pyproject.toml"],
          tests: ["tests/README.md"],
          standards: ["DEVSTD-AS-BUILT", "QUINT-0.32"],
        },
        lastChangedBy: "bootstrap:recipeweave",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "functional",
      },
      {
        id: "REQ-STATS-001",
        revision: 1,
        status: "active",
        kind: "functional",
        title: "train holdout separation",
        subject: "統計評価",
        actionName: "preserve",
        objectName: "train/holdout分離と漏洩検査",
        rationale: "探索結果を同じ標本で評価すると汎化性能を過大評価する。",
        sourceRefs: ["user:2026-09-05", "README.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-STATS-001-1", given: "RecipeWeaveの宣言入力がある", when_: "受入検査を実行する", expected: "分割seed、件数、除外条件、holdout固定状態をmanifestとレポートに残す。" }
        ],
        verification: { method: "自動検査とartifact review", evidence: "moon task and targeted tests" },
        traces: {
          design: ["docs/design/generated/README.md"],
          implementation: ["packages/generator/pyproject.toml"],
          tests: ["tests/README.md"],
          standards: ["DEVSTD-AS-BUILT", "QUINT-0.32"],
        },
        lastChangedBy: "bootstrap:recipeweave",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "functional",
      },
      {
        id: "REQ-DAG-001",
        revision: 1,
        status: "active",
        kind: "functional",
        title: "raw material quantities and process DAG",
        subject: "レシピ表現",
        actionName: "preserve",
        objectName: "原始材料数量と工程DAG",
        rationale: "完成料理名だけでは再現性や工程制約を表現できない。",
        sourceRefs: ["user:2026-09-05", "README.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-DAG-001-1", given: "RecipeWeaveの宣言入力がある", when_: "受入検査を実行する", expected: "各原始材料の単位付き数量と工程ノード・依存辺を検証可能な形式で保存する。" }
        ],
        verification: { method: "自動検査とartifact review", evidence: "moon task and targeted tests" },
        traces: {
          design: ["docs/design/generated/README.md"],
          implementation: ["packages/generator/pyproject.toml"],
          tests: ["tests/README.md"],
          standards: ["DEVSTD-AS-BUILT", "QUINT-0.32"],
        },
        lastChangedBy: "bootstrap:recipeweave",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "functional",
      },
      {
        id: "REQ-COST-001",
        revision: 1,
        status: "active",
        kind: "functional",
        title: "approved spending boundary",
        subject: "実験実行",
        actionName: "preserve",
        objectName: "ユーザー未承認の大量課金なし",
        rationale: "大量生成・外部評価・クラウド実行は費用を発生させうるため、承認境界を明示する。",
        sourceRefs: ["user:2026-09-05", "README.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-COST-001-1", given: "RecipeWeaveの宣言入力がある", when_: "受入検査を実行する", expected: "デフォルトはローカル・小規模dry-runとし、費用見積りと明示承認なしに外部大量処理を開始しない。" }
        ],
        verification: { method: "自動検査とartifact review", evidence: "moon task and targeted tests" },
        traces: {
          design: ["docs/design/generated/README.md"],
          implementation: ["packages/generator/pyproject.toml"],
          tests: ["tests/README.md"],
          standards: ["DEVSTD-AS-BUILT", "QUINT-0.32"],
        },
        lastChangedBy: "bootstrap:recipeweave",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "functional",
      },
      {
        id: "REQ-BOUNDARY-001",
        revision: 1,
        status: "active",
        kind: "functional",
        title: "future project boundaries",
        subject: "workspace",
        actionName: "preserve",
        objectName: "frontend/backend/database/infra/batch/scriptsの境界",
        rationale: "将来の同居先を予約しつつ未実装機能を実装済みと表明しない。",
        sourceRefs: ["user:2026-09-05", "README.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-BOUNDARY-001-1", given: "RecipeWeaveの宣言入力がある", when_: "受入検査を実行する", expected: "各予約projectはREADMEとmoon設定を持ち、実装状態をplaceholderとして表示する。" }
        ],
        verification: { method: "自動検査とartifact review", evidence: "moon task and targeted tests" },
        traces: {
          design: ["docs/design/generated/README.md"],
          implementation: ["packages/generator/pyproject.toml"],
          tests: ["tests/README.md"],
          standards: ["DEVSTD-AS-BUILT", "QUINT-0.32"],
        },
        lastChangedBy: "bootstrap:recipeweave",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "functional",
      },
      {
        id: "REQ-DESIGN-001",
        revision: 1,
        status: "active",
        kind: "functional",
        title: "implementation-derived design",
        subject: "as-built設計",
        actionName: "preserve",
        objectName: "実装artifact由来の決定的な設計導線",
        rationale: "設計文書が実装と乖離すると受入判断を誤る。",
        sourceRefs: ["user:2026-09-05", "README.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-DESIGN-001-1", given: "RecipeWeaveの宣言入力がある", when_: "受入検査を実行する", expected: "generatorの同一入力再実行で生成設計がbyte一致し、drift checkが差分を報告する。" }
        ],
        verification: { method: "自動検査とartifact review", evidence: "moon task and targeted tests" },
        traces: {
          design: ["docs/design/generated/README.md"],
          implementation: ["packages/generator/pyproject.toml"],
          tests: ["tests/README.md"],
          standards: ["DEVSTD-AS-BUILT", "QUINT-0.32"],
        },
        lastChangedBy: "bootstrap:recipeweave",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-SELECT-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "食材カードの選択状態を明示する",
        subject: "食材選択画面",
        actionName: "select",
        objectName: "カード全体の押下による食材の選択状態",
        rationale: "小さな位置合わせを求めず、選択できる対象と選択済みを利用者が判別できるようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-SELECT-001-1", given: "未選択の食材を表示している", when_: "食材カードを見る", expected: "空のチェックボックスが表示され、カード全体で選択できる。" },
          { id: "AC-REQ-SVC-SELECT-001-2", given: "食材カードが表示されている", when_: "カードを押し、もう一度押す", expected: "最初はチェックと枠で選択済みとなり、次の押下で解除される。色だけで状態を区別しない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/FoodTile.svelte"],
          tests: ["frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-SEARCH-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "人数と分量を入力せず食材から探す",
        subject: "料理検索",
        actionName: "select",
        objectName: "選択した食材を用いる公開対象料理",
        rationale: "最初の料理選びを食材の選択だけで開始できるようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-SEARCH-001-1", given: "ログインや冷蔵庫登録をしていない", when_: "食材を選んで検索する", expected: "人数・分量を要求せず検索でき、既定は選んだ食材をすべて使う候補になる。" },
          { id: "AC-REQ-SVC-SEARCH-001-2", given: "検索条件または結果を表示している", when_: "いずれかを使うへ明示的に切り替える、または結果から戻る", expected: "切替後の条件を結果に表示し、戻る際は選択・条件・表示位置を保持する。" },
          { id: "AC-REQ-SVC-SEARCH-001-3", given: "条件に合う候補がない、または取得に失敗した", when_: "検索結果を開く", expected: "0件または失敗を区別し、条件を無断で緩めず、入力を保持した選び直し・再試行の入口を示す。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts"],
          tests: ["frontend/src/App.test.ts","frontend/src/lib/domain.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-DISCOVERY-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "ホームに偶然の一品を提示する",
        subject: "ホーム",
        actionName: "provide",
        objectName: "利用条件を満たすランダムな一品",
        rationale: "検索語を考えなくても料理を発見できるようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-DISCOVERY-001-1", given: "条件に合う候補がある", when_: "ホームを新しく開く、または別の一品を押す", expected: "偶然の一品を必ず提示し、複数候補がある場合は直近の同じ一品の連続表示を避ける。" },
          { id: "AC-REQ-SVC-DISCOVERY-001-2", given: "検索結果からホームへ戻る、または適合候補がない", when_: "ホームを表示する", expected: "戻った場合は表示していた一品を保持し、候補がない場合は理由と条件変更入口を示して必須条件を守る。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts"],
          tests: ["frontend/src/App.test.ts","frontend/src/lib/domain.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-SAMPLE-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "初期Devで操作可能なサンプル料理を提供する",
        subject: "Dev公開版",
        actionName: "provide",
        objectName: "試用可能と明示した初期料理セット",
        rationale: "将来の大量レシピ生成の完了を待たず、料理を探して作る操作を確認できるようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-SAMPLE-001-1", given: "初期Dev版を公開する", when_: "利用できる料理一覧を確認する", expected: "なす卵醤油・なす卵カレー・トマト卵・豆腐わかめスープ・キャベツツナ・カップ焼きそばチーズ・ツナコーンごはん・きのこバターの8品を操作用サンプルとして選べる。" },
          { id: "AC-REQ-SVC-SAMPLE-001-2", given: "試用料理を表示する", when_: "料理の説明と提供状態を見る", expected: "試用データであることと対象範囲を示し、将来目標件数を実際の公開件数や品質実証として表示しない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","data/samples/recipes.json","data/samples/foods.json","backend/src/app/integrations/catalog/json_provider.py"],
          tests: ["backend/tests/test_api.py"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-SCALE-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "料理選択後に人数に応じた分量へ変換する",
        subject: "料理詳細",
        actionName: "derive",
        objectName: "確定分量に対する人数比の材料量",
        rationale: "同一料理の人数違いを別レシピとして探す手間をなくす。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-SCALE-001-1", given: "2人分のなす160g・卵2個・油8gを表示している", when_: "人数を3人に変える", expected: "材料量がなす240g・卵3個・油12gになる。加熱時間は人数比で変更しない。" },
          { id: "AC-REQ-SVC-SCALE-001-2", given: "個別変更を含む直前の確定分量がある", when_: "正の人数を直接入力または加減ボタンで変更する", expected: "各材料を新人数/旧人数の比で更新する。0以下・非数の人数は確定できず、更新前の分量で調理を開始させない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts"],
          tests: ["frontend/src/lib/domain.test.ts","frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-AMOUNT-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "材料別の量を直接調整する",
        subject: "料理詳細",
        actionName: "preserve",
        objectName: "利用者が個別調整した材料分量",
        rationale: "手持ちの量や好みに合わせた変更を検索後に行い、次の操作へ引き継ぐ。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-AMOUNT-001-1", given: "料理詳細の材料量を表示している", when_: "材料の数量欄に値を直接入力する", expected: "対象材料だけを調整し、調整済みを表示する。負数・非数を確定せず、献立追加と調理開始に確定分量を引き継ぐ。" },
          { id: "AC-REQ-SVC-AMOUNT-001-2", given: "人数や量を調整済みである", when_: "同じブラウザで料理を開き直す、または元の分量に戻す", expected: "調整は料理詳細の下書きとして維持され、リセットで標準分量に戻る。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts","frontend/src/lib/persistence.ts"],
          tests: ["frontend/src/lib/domain.test.ts","frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-LOCAL-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "試用データを同じブラウザで継続利用する",
        subject: "Dev公開版",
        actionName: "maintain",
        objectName: "冷蔵庫・献立・しおり・調理状態の端末内データ",
        rationale: "ログインなしで途中から使え、保存範囲を誤認しないようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-LOCAL-001-1", given: "冷蔵庫・献立・しおり・分量下書き・調理状態を変更した", when_: "同じ端末の同じブラウザで開き直す", expected: "最後に確定したデータから利用を続けられる。保存に失敗したときは成功表示を出さない。" },
          { id: "AC-REQ-SVC-LOCAL-001-2", given: "端末保存を使用している", when_: "保存先の説明を確認する", expected: "別端末や別ブラウザへの自動同期を行わないことと、バックアップなしの消失はサービス側で復元できないことが分かる。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/persistence.ts"],
          tests: ["frontend/src/lib/domain.test.ts","frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-OCR-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "レシート画像を端末内で読み取る",
        subject: "レシート読取",
        actionName: "generate",
        objectName: "画像内の日本語から得た登録候補",
        rationale: "実画像から入力候補を作り、個別手入力の手間を減らす。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-OCR-001-1", given: "対応する実レシート画像を選んだ", when_: "読み取るを押す", expected: "この端末内で日本語を読み取り、画像をサービスサーバーへ送信せず候補を表示する。読み取りだけでは在庫を変更しない。" },
          { id: "AC-REQ-SVC-OCR-001-2", given: "読取処理に失敗した、またはサンプルを選んだ", when_: "結果画面を開く", expected: "失敗には再試行・画像の選び直し・手入力を示す。サンプル結果は実画像の読取成功と区別する。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/ocr.ts","frontend/scripts/prepare-ocr.mjs"],
          tests: ["frontend/scripts/ocr-smoke.mjs"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-RECEIPT-INPUT-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "対応するレシート画像だけを受け付ける",
        subject: "レシート入力",
        actionName: "validate",
        objectName: "撮影または画像選択で渡された画像",
        rationale: "端末ごとの撮影条件と画像制限を明示し、失敗後も利用を続けられるようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-RECEIPT-INPUT-001-1", given: "レシートから追加を開いている", when_: "撮影するまたは画像を選ぶを使用する", expected: "JPEG・PNG・WebPの1枚10×1024×1024バイト以下を受け付ける。カメラ拒否時も画像選択と手入力を使用できる。" },
          { id: "AC-REQ-SVC-RECEIPT-INPUT-001-2", given: "HEIC等の非対応形式、容量超過または画像として壊れたファイルがある", when_: "画像を選ぶ", expected: "理由を表示して選び直せる。在庫を変更しない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/receipt.ts","frontend/src/lib/ocr.ts"],
          tests: ["frontend/src/lib/domain.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-RECEIPT-REVIEW-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "登録前に読取候補を訂正できる",
        subject: "読取確認画面",
        actionName: "enable",
        objectName: "選択する食品候補と除外した行",
        rationale: "OCRの誤読と誤除外から利用者が自力で復帰できるようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-RECEIPT-REVIEW-001-1", given: "登録候補に食品名の誤りまたは不明な行がある", when_: "修正または食材を選ぶを押す", expected: "原文と候補を確認して食材名・数量・単位を訂正できる。自動判定済みの行も修正できる。" },
          { id: "AC-REQ-SVC-RECEIPT-REVIEW-001-2", given: "日用品・袋代・値引き・合計の行、または誤除外された食品がある", when_: "登録対象のチェックと除外した行を確認する", expected: "非食品行を外せ、誤除外した食品を選択と食材指定で戻せる。原文自体に欠けた食品は登録後に手入力で補える。" },
          { id: "AC-REQ-SVC-RECEIPT-REVIEW-001-3", given: "未確認の行は未選択で有効な2行が選択済みである", when_: "この内容で登録へ進む", expected: "未選択の不明行は登録を妨げず2件を確定できる。同名商品という理由だけで別の購入行を削除しない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/receipt.ts"],
          tests: ["frontend/src/lib/domain.test.ts","frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-RECEIPT-CANCEL-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "確定前の読取を在庫変更なしで中止する",
        subject: "レシート読取",
        actionName: "constrain",
        objectName: "確定していない画像・全文・候補",
        rationale: "登録する前ならやめられ、取り消し作業を在庫へ持ち越さないようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-RECEIPT-CANCEL-001-1", given: "読み取り中または候補を訂正中である", when_: "キャンセルし、訂正中なら破棄を確認する", expected: "未確定の候補を破棄し、在庫・確定済み登録履歴を変更しない。" },
          { id: "AC-REQ-SVC-RECEIPT-CANCEL-001-2", given: "候補を訂正中に破棄確認が出た", when_: "破棄をやめる", expected: "訂正内容を保ったまま確認へ戻れる。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/ocr.ts"],
          tests: ["frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-QUANTITY-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "不明な食品量を推測せず保持する",
        subject: "数量管理",
        actionName: "preserve",
        objectName: "数量不明・購入単位・使用量の区別",
        rationale: "価格やパック数を内容量へ取り違えることを防ぐ。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-QUANTITY-001-1", given: "価格198円だけ、または内容量不明の1パックを読み取った", when_: "食材候補を登録する", expected: "198円を198g等にせず、数量不明または1パック・内容量不明を保持する。数量不明を0と扱わない。" },
          { id: "AC-REQ-SVC-QUANTITY-001-2", given: "レシートの購入日や単位の異なる在庫がある", when_: "期限や必要量との差分を表示する", expected: "賞味期限・消費期限を購入日から推測せず、根拠のない個数/重量換算を行わず量を確認と表示する。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/lib/receipt.ts","frontend/src/lib/domain.ts","frontend/src/lib/types.ts"],
          tests: ["frontend/src/lib/domain.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-RECEIPT-COMMIT-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "選択済みの有効候補を一度だけ一括登録する",
        subject: "レシート登録",
        actionName: "generate",
        objectName: "利用者が確認した食品候補の在庫追加",
        rationale: "確認操作と在庫変更を対応させ、二重押下や途中失敗による不整合を防ぐ。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-RECEIPT-COMMIT-001-1", given: "有効な食品候補を選択し件数が表示されている", when_: "この内容で登録を押す", expected: "選択した候補だけを登録単位で一括追加し、登録日時と対象を追える。数量不明は許可し、選択中の食材名未確定は訂正または解除を求める。" },
          { id: "AC-REQ-SVC-RECEIPT-COMMIT-001-2", given: "同一の確定操作を再送する、または一括確定が失敗する", when_: "登録処理の結果を表示する", expected: "同じ登録は一度だけ追加し、一部成功を完了扱いしない。失敗時は再確認でき、成功時は追加件数と内容を表示する。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts","frontend/src/lib/persistence.ts"],
          tests: ["frontend/src/lib/domain.test.ts","frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-RECEIPT-DUPLICATE-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "過去のレシート登録と重複を照合する",
        subject: "レシート登録",
        actionName: "provide",
        objectName: "重複の可能性がある買い物の確認",
        rationale: "同じ画像の再登録と似た別の買い物を、利用者が区別できるようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-RECEIPT-DUPLICATE-001-1", given: "同じ画像ハッシュまたは購入内容の署名に一致候補がある", when_: "レシートを再度確定しようとする", expected: "登録済みの可能性と履歴入口を示し、登録日時・食品一覧・登録済み/取消済みを照合できる。" },
          { id: "AC-REQ-SVC-RECEIPT-DUPLICATE-001-2", given: "重複の可能性を表示している", when_: "利用者が同じ買い物、別の買い物、または判断できないと選ぶ", expected: "同じまたは不明なら登録をやめて在庫を確認でき、別なら明示確認で進める。取消済みの再登録でも現在の在庫確認を求め、全重複を検出する保証を表示しない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/receipt.ts","frontend/src/lib/domain.ts"],
          tests: ["frontend/src/lib/domain.test.ts","frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-RECEIPT-UNDO-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "今回登録の未消費残量だけを取り消す",
        subject: "レシート履歴",
        actionName: "enable",
        objectName: "指定した登録単位の未消費在庫の取消",
        rationale: "過去の在庫や使用履歴を壊さず、誤登録を後から戻せるようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-RECEIPT-UNDO-001-1", given: "以前から500gあり、今回300gを別の登録単位で追加し今回分を100g使用した", when_: "履歴から今回の登録を取り消し、残量を確認して確定する", expected: "今回の残り200gだけを除去し、以前の500gと使用100gの履歴を保持する。" },
          { id: "AC-REQ-SVC-RECEIPT-UNDO-001-2", given: "今回の追加分を編集済み、使い切り済み、削除済み、または数量不明である", when_: "取消前の内容を確認する", expected: "編集前後と現在残量を明示する。編集後250gなら250g、残量なしなら他在庫は変更せず、不明なら当該不明項目だけを外す。量を推測しない。" },
          { id: "AC-REQ-SVC-RECEIPT-UNDO-001-3", given: "取消を確定した登録がある", when_: "同じ履歴を開いて再度取り消そうとする", expected: "取消済みの履歴を残し、同じ取消を再実行できない。取消対象は登録単位で一度だけ反映する。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts"],
          tests: ["frontend/src/lib/domain.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-FOOD-EDIT-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "在庫の選択と編集を分ける",
        subject: "冷蔵庫",
        actionName: "maintain",
        objectName: "食材名と任意の数量・保存場所・優先状態",
        rationale: "検索に使う食材を選ぶ操作と在庫を書き換える操作を混同しないようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-FOOD-EDIT-001-1", given: "冷蔵庫に食材行がある", when_: "行本体または行内の編集を押す", expected: "行本体は検索用の選択を切り替え、独立した編集ボタンは選択を変えず編集画面を開く。" },
          { id: "AC-REQ-SVC-FOOD-EDIT-001-2", given: "食材を手入力または編集する", when_: "名前と任意の数量、冷蔵/冷凍/常温、優先状態を確定する", expected: "名前だけでも登録でき、数量不明へ戻せる。削除は対象確認と取消導線を持ち、優先状態を期限切れと同義にしない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts"],
          tests: ["frontend/src/lib/domain.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-MEAL-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "献立の料理ごとに人数を指定する",
        subject: "献立",
        actionName: "preserve",
        objectName: "選んだ各料理と独立した人数・分量",
        rationale: "主菜3人分と副菜2人分のように必要な量を料理ごとに決められるようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-MEAL-001-1", given: "分量調整した料理を献立に加える", when_: "献立に追加を押す", expected: "料理と確定分量を引き継いで表示し、料理の追加・変更・除去を行える。" },
          { id: "AC-REQ-SVC-MEAL-001-2", given: "主菜と副菜を献立に入れている", when_: "主菜の加減ボタンまたは直接入力で3人、副菜を2人へ変更する", expected: "各料理に人数が表示され、変更していない料理の人数と分量は変わらない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts"],
          tests: ["frontend/src/lib/domain.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-MEAL-QUANTITY-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "献立に必要な材料量を集計する",
        subject: "献立の材料集計",
        actionName: "derive",
        objectName: "各料理の確定した原材料必要量",
        rationale: "別料理の同じ食材をまとめつつ、異なる単位や加工状態を根拠なく合算しないようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-MEAL-QUANTITY-001-1", given: "料理別の人数・分量が確定している", when_: "買い物リストを開く、または献立を変更する", expected: "同一の食材・形態・換算可能な単位だけを合計し、必要量・手持ち・買う量を分けて更新する。付属材料を二重計上しない。" },
          { id: "AC-REQ-SVC-MEAL-QUANTITY-001-2", given: "なす必要240gで手持ち不明、卵必要3個で手持ち1個、豆腐必要150gで手持ちなしである", when_: "不足表示を見る", expected: "なすは量を確認、卵は買う2個、豆腐は買う150gと表示し、不明や換算不能を買い足し0と断定しない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts"],
          tests: ["frontend/src/lib/domain.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-SHOPPING-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "購入メモを在庫変更と分離する",
        subject: "買い物リスト",
        actionName: "maintain",
        objectName: "購入チェックと変更後の必要量",
        rationale: "買い物中のメモ操作で在庫が二重追加されることを防ぐ。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-SHOPPING-001-1", given: "買い物項目が表示されている", when_: "行を押して購入チェックを付け外しする", expected: "チェックだけを変更し、在庫は増減しない。在庫追加はレシートまたは実購入量を確認した手入力で行う。" },
          { id: "AC-REQ-SVC-SHOPPING-001-2", given: "購入チェック済みの項目がある", when_: "人数・献立変更で必要量が変わる、または項目がリストから外れる", expected: "必要量が変わった項目はチェックを解除し、外れた購入済み項目は以前の購入メモとして現行項目と分ける。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts"],
          tests: ["frontend/src/lib/domain.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-COOK-PLAN-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "作業可能な献立の段取りを示す",
        subject: "調理の段取り",
        actionName: "provide",
        objectName: "確定した料理工程の実行順",
        rationale: "複数料理を作るときに手順や器具の衝突を利用者へ押し付けないようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-COOK-PLAN-001-1", given: "複数料理と使う器具の条件がある", when_: "段取りを見るを押す", expected: "材料量と各工程の依存順を守った調理順を提示し、同時使用できない器具や一人で両立しない作業を同時実行として指示しない。" },
          { id: "AC-REQ-SVC-COOK-PLAN-001-2", given: "料理または人数・器具条件を変更した", when_: "段取りを確認する", expected: "変更後の条件で順番を再提示し、確定した段取りから調理を始められる。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts"],
          tests: ["frontend/src/lib/domain.test.ts","frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-COOK-RESUME-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "中断した工程から調理を再開する",
        subject: "調理画面",
        actionName: "preserve",
        objectName: "選んだ料理の工程位置と完了状態",
        rationale: "画面を離れても最初からやり直さず、誤って進めた工程へ戻れるようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-COOK-RESUME-001-1", given: "調理中に次へ、戻る、中断を操作した", when_: "ホーム上部または献立の調理を再開を押す", expected: "料理名と工程番号を示して保存した位置へ復帰し、完了済み状態を維持する。" },
          { id: "AC-REQ-SVC-COOK-RESUME-001-2", given: "次へを押しすぎた", when_: "戻るで前の工程を表示する", expected: "前の工程へ戻り、工程を移動しただけでは在庫を増減しない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts","frontend/src/lib/persistence.ts"],
          tests: ["frontend/src/lib/domain.test.ts","frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-COOK-TIMER-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "起動済みタイマーを重複させず保持する",
        subject: "調理タイマー",
        actionName: "preserve",
        objectName: "起動したタイマーとその経過状態",
        rationale: "工程移動や再開で同じタイマーが増え、誤った残時間を伝えることを防ぐ。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-COOK-TIMER-001-1", given: "工程に起動済みタイマーがある", when_: "工程を戻る、再訪する、または調理を再開する", expected: "既存タイマーの状態を引き継ぎ、同じタイマーを自動で重複起動しない。" },
          { id: "AC-REQ-SVC-COOK-TIMER-001-2", given: "タイマーを提供するDev版を使う", when_: "提供状態を確認し画面を閉じて再開する", expected: "画面外・再開時・音の動作条件が説明と一致し、終了していた場合に新しい全時間のタイマーとして再起動しない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts"],
          tests: ["frontend/src/lib/domain.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-STOCK-CONSENT-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "利用者が選んだ完了時だけ使用量を引く",
        subject: "調理完了",
        actionName: "constrain",
        objectName: "同単位で量が足りる在庫への確認済み使用量の反映",
        rationale: "完成操作だけで不明な在庫を推測して減らすことを防ぐ。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-STOCK-CONSENT-001-1", given: "調理完了画面を開いた", when_: "在庫から使用量を引くを選ばず完了する", expected: "減算チェックは初期OFFで、在庫を変更しない。" },
          { id: "AC-REQ-SVC-STOCK-CONSENT-001-2", given: "利用者が実使用量を編集し減算へ明示同意した", when_: "完了を確定する", expected: "同じ単位で十分な在庫がある材料だけを一度引く。不明・不足・換算不可は理由を表示し変更しない。反映した材料と見送った材料を表示する。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts"],
          tests: ["frontend/src/lib/domain.test.ts","frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-EXCLUSION-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "除外食材を検索と偶然の一品へ適用する",
        subject: "候補選定",
        actionName: "enforce",
        objectName: "利用者が指定した食べられない食材の条件",
        rationale: "入口によって除外条件が失われ、意図しない食品を提案することを防ぐ。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-EXCLUSION-001-1", given: "食べられない食材を設定している", when_: "検索・アレンジ・偶然の一品を開く", expected: "すべての候補入口で除外条件を守り、候補0件でも無断解除しない。" },
          { id: "AC-REQ-SVC-EXCLUSION-001-2", given: "加工食品の構成原料を確認できない", when_: "除外条件に対する候補の適合状態を見る", expected: "原材料未確認を示し、除外済み・安全確認済みと断定しない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts"],
          tests: ["frontend/src/lib/domain.test.ts","frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-BACKUP-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "検証したバックアップで端末データを復元する",
        subject: "データ管理",
        actionName: "enable",
        objectName: "利用者が指定したバックアップ内容による現在データの置換",
        rationale: "同期のない試用版でも持ち出しと復元を行い、不正ファイルによるデータ消失を防ぐ。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-BACKUP-001-1", given: "このブラウザの利用データがある", when_: "設定からデータを書き出す", expected: "対応するJSONバックアップを保存でき、持ち出す内容と復元の方法が分かる。" },
          { id: "AC-REQ-SVC-BACKUP-001-2", given: "バックアップを選択した", when_: "データを読み込む", expected: "形式・版・参照関係・数量を検証し、件数と置換対象を表示して確認後に全置換する。合算しない。不正ファイルや確認キャンセルでは現在データを変更しない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/persistence.ts"],
          tests: ["frontend/src/lib/domain.test.ts","frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-PRIVACY-001",
        revision: 2,
        status: "active",
        kind: "data",
        title: "読取画像と全文を永続保存しない",
        subject: "レシートデータ管理",
        actionName: "constrain",
        objectName: "確認のため一時的に保持した画像とOCR全文の保存期間",
        rationale: "レシートの個人情報を在庫登録に不要な形で残さないようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-PRIVACY-001-1", given: "レシートを読み取っている", when_: "登録・キャンセル・画面終了が完了する", expected: "画像とOCR全文をメモリから破棄し、店舗名・レシート上の購入日時を永続保存しない。選択前から端末にある写真は削除しない。" },
          { id: "AC-REQ-SVC-PRIVACY-001-2", given: "登録履歴と保存データを確認する", when_: "端末内の永続データを検査する", expected: "食材・数量・単位・登録日時・登録ID・画像ハッシュ・購入内容署名・必要な状態履歴だけを保存し、元画像や全文を復元できる形で保持しない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/ocr.ts","frontend/src/lib/receipt.ts","frontend/src/lib/persistence.ts","frontend/src/lib/types.ts"],
          tests: ["frontend/src/lib/domain.test.ts","frontend/src/App.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-SVC-BOOKMARK-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "料理のしおりと分量下書きを区別する",
        subject: "保存機能",
        actionName: "preserve",
        objectName: "料理IDに対するしおり",
        rationale: "保存した料理と今回調整した量の意味を混同しないようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-BOOKMARK-001-1", given: "料理詳細を開いている", when_: "保存する、または保存済みを解除する", expected: "料理IDのしおりを付け外しし、解除直後に取り消せる。しおり操作だけで在庫や献立は変更しない。" },
          { id: "AC-REQ-SVC-BOOKMARK-001-2", given: "個別分量の下書きがある", when_: "保存一覧から料理を開き直す", expected: "同じブラウザの下書きは別に保持され、しおり自体が分量セットでないことが説明される。公開終了した料理は理由を表示する。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","frontend/src/lib/domain.ts","frontend/src/lib/persistence.ts"],
          tests: [],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-GUIDE-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "切り方ガイドから同じ工程へ戻す",
        subject: "技法ガイド",
        actionName: "provide",
        objectName: "調理工程で参照した切り方",
        rationale: "用語が分からないため調理を中断したり、工程位置を見失うことを防ぐ。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-GUIDE-001-1", given: "調理中の工程に切り方の説明がある", when_: "切り方を見るを押して閉じる", expected: "図・文章または提供済み動画で説明を確認でき、閉じると同じ料理の同じ工程へ戻る。" },
          { id: "AC-REQ-SVC-GUIDE-001-2", given: "動画等の案内を取得できない", when_: "ガイドを開く", expected: "図や文章の説明へ切り替えられ、未提供動画を再生済みや提供済みと表示しない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte"],
          tests: [],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-SVC-CAPABILITY-001",
        revision: 2,
        status: "active",
        kind: "quality",
        title: "Devの提供範囲と将来のAWS同期を区別する",
        subject: "提供状態表示",
        actionName: "provide",
        objectName: "実際に利用できる機能と未提供機能",
        rationale: "仮想レビューや静的画像を実装成功と誤認せず、利用者が試せる範囲を判断できるようにする。",
        sourceRefs: ["user:2026-09-05:recipeweave-service", "docs/service/manual.md", "docs/service/faq.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-CAPABILITY-001-1", given: "初期Devを公開する", when_: "画面とマニュアルの提供表を確認する", expected: "8品のサンプル、端末内OCR、同じブラウザの保存範囲、タイマー等の実確認した動作を記載し、AWSによる認証・同期は未提供と明示する。" },
          { id: "AC-REQ-SVC-CAPABILITY-001-2", given: "設計図やエージェントの机上レビューだけがある", when_: "提供済み表示または受入記録を更新する", expected: "実装や実利用者テストの成功証拠へ読み替えない。設計対象・実装済み・検証済みを区別し、未提供ボタンで偽の完了を示さない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: ["frontend/src/App.svelte","tools/build-service-docs.mjs"],
          tests: [],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-SVC-PAGES-001",
        revision: 2,
        status: "active",
        kind: "operational",
        title: "検査したDev版をGitHub Pagesで閲覧可能にする",
        subject: "開発配布工程",
        actionName: "provide",
        objectName: "検査対象の変更版と対応したDevプレビュー",
        rationale: "ユーザーが依頼したGitHub Pages上で、変更結果を継続して確認できる状態にする。",
        sourceRefs: ["user:2026-09-05:recipeweave-dev-pages", "docs/service/manual.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-SVC-PAGES-001-1", given: "Dev版を配布する変更がある", when_: "GitHubのCIを実行する", expected: "変更と受入条件に関係する検査、ビルド、生成要件のdrift確認を行い、失敗した版を成功した配布として報告しない。" },
          { id: "AC-REQ-SVC-PAGES-001-2", given: "必要な検査とビルドが成功した", when_: "Dev版を公開しURLを確認する", expected: "その変更版をGitHub Pagesで閲覧でき、配布版識別・URL・検査結果を追跡できる。公開を確認していなければ確認済みとしない。" }
        ],
        verification: { method: "対応する受入条件の自動検査と画面操作確認", evidence: "docs/service/reviews の独立第2回机上レビューで仕様を確認済み。実装受入は未実施で、後続の実測証跡を追加する。" },
        traces: {
          design: ["docs/service/manual.md", "docs/service/screens-and-flows.md"],
          implementation: [".github/workflows/dev.yml","frontend/vite.config.ts","frontend/package.json"],
          tests: [],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-DEV-ARCH-001",
        revision: 2,
        status: "active",
        kind: "constraint",
        title: "採用ADRに従うWeb・API・AWS構成を提供する",
        subject: "RecipeWeaveの開発基盤",
        actionName: "provide",
        objectName: "ADR-0001で採用した構成に従う実装プロファイル",
        rationale: "CornellNoteWebの既知の開発方針へおおむね合わせるという依頼を、採用済みADRの構成として検証可能に固定する。未確認の別会話全体への完全準拠は主張しない。",
        sourceRefs: ["user:2026-09-05:cornellnoteweb-architecture", "docs/design/ADR-0001-service-dev.md", "docs/service/overview.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-DEV-ARCH-001-1", given: "採用ADRに従うWebとAPIの実装がある", when_: "ビルドと構成を確認する", expected: "フロントエンドはSvelte・TypeScriptによる静的Web、APIはFastAPIを基盤とし、CloudFront/S3からAPI Gateway HTTP API・Lambdaを経由してAurora DSQLへ接続する構成をコードとして提供する。" },
          { id: "AC-REQ-DEV-ARCH-001-2", given: "AWS向けの利用者状態APIを構成する", when_: "認証設定と利用者を変えて状態の読書きを検証する", expected: "Cognito access JWTで利用者を特定し、署名・issuer・期限・token_use・client_idを検証する。任意の利用者IDヘッダーを信用せず、別利用者の状態を取得更新できない。認証未設定時は状態APIを閉じ、版競合は無条件上書きしない。" },
          { id: "AC-REQ-DEV-ARCH-001-3", given: "PagesのDev版とAWS向けコードが存在する", when_: "利用者への提供状態と配備状態を確認する", expected: "Pagesはログイン不要・このブラウザの端末保存として提供する。AWS向けのコード・合成・検証の存在を実配備や同期提供の成功へ読み替えず、AWS未配備ならAWS実環境の受入は未完了と記録する。" }
        ],
        verification: { method: "構成コード・API契約の検査、認証と利用者分離の対象試験、実配備記録の照合", evidence: "採用済みADR-0001を要求源とする。構成の実装完成・対象試験・AWS実配備の受入証跡はこの要件追加時点では未登録。" },
        traces: {
          design: ["docs/design/ADR-0001-service-dev.md", "docs/service/overview.md"],
          implementation: ["frontend/package.json","frontend/src/App.svelte","backend/src/app/main.py","backend/src/app/core/dependencies.py","backend/src/app/integrations/auth/cognito_provider.py","backend/src/app/integrations/state/memory_provider.py","backend/src/app/integrations/state/dsql_provider.py","infra/lib/data-stack.ts","infra/lib/service-stack.ts"],
          tests: ["backend/tests/test_api.py","backend/tests/test_auth.py","backend/tests/test_state.py","backend/tests/test_dsql.py","infra/test/core.test.ts","infra/test/stack.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-DEV-QUALITY-001",
        revision: 2,
        status: "active",
        kind: "operational",
        title: "配備・移行・生成設計の検証契約を維持する",
        subject: "RecipeWeaveの開発工程",
        actionName: "maintain",
        objectName: "採用した配備とデータ移行に対応する再現可能な検証証跡",
        rationale: "インフラやDB移行をコードと検査で扱い、実装と設計文書の乖離、およびローカル検査と実環境受入の混同を防ぐ。",
        sourceRefs: ["user:2026-09-05:cornellnoteweb-development", "docs/design/ADR-0001-service-dev.md", "AGENTS.md"],
        acceptanceCriteria: [
          { id: "AC-REQ-DEV-QUALITY-001-1", given: "AWS構成を変更する", when_: "CDK合成・配備パッケージ・権限を検査する", expected: "CDKで構成を再現でき、必要な配布物を生成する。アプリ用とマイグレーション用のIAM/DB権限を分離し、用途に必要な権限に限定する。認証情報をコード・生成設計・ログへ埋め込まない。" },
          { id: "AC-REQ-DEV-QUALITY-001-2", given: "DSQLのスキーマまたは利用する索引を変更する", when_: "版管理したマイグレーションを実行・再実行する", expected: "適用済み状態を追跡し、DDLを一文ずつ別トランザクションで扱いDMLと混在させない。非同期の索引作成は完了を確認し、競合の再試行を有界にして同じ業務操作を二重適用しない。" },
          { id: "AC-REQ-DEV-QUALITY-001-3", given: "Web・API・DB・インフラの実装がある", when_: "設計文書の生成と差分検査を実行する", expected: "現存するコード・OpenAPI・SQL・CDK合成結果から現在状態の設計を決定的に生成し、同一入力の再生成で差分がなく、実装変更によるdriftを検出する。手編集の生成文書で差分を隠さない。" },
          { id: "AC-REQ-DEV-QUALITY-001-4", given: "型検査・ローカル試験・CDK合成・マイグレーション試験または配備を行う", when_: "受入記録を更新する", expected: "対象版、検査内容、結果、実行環境を対応させる。コード検査・ローカル代替・AWS実配備・実環境認証同期を区別し、未配備または未実施の実環境項目を合格にしない。" }
        ],
        verification: { method: "CDKと移行の対象検査、生成設計の再生成/drift確認、版に対応する受入証跡のレビュー", evidence: "採用済みADR-0001と既存AGENTSの三つの開発規約を要求源とする。実装・試験traceは実装完成後に存在と結果を確認して登録する。" },
        traces: {
          design: ["docs/design/ADR-0001-service-dev.md"],
          implementation: ["infra/lib/data-stack.ts","infra/lib/service-stack.ts","infra/lib/github-deploy-stack.ts","backend/tools/package_lambda.py","database/migrate.py","database/migrations/manifest.manual.json","database/migrations/001_user_state.sql","backend/src/app/integrations/state/dsql_provider.py","backend/src/app/tools/generate.py","tools/generate_service_design.py","tools/check_generated_service.py",".github/workflows/dev.yml"],
          tests: ["backend/tests/test_generation.py","backend/tests/test_dsql.py","infra/test/core.test.ts","infra/test/stack.test.ts"],
          standards: [],
        },
        lastChangedBy: "trace:2026-09-06:dev-v0.1",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      }
    ],
  }

  pure val lifecycleRequirement: Requirement = {
    id: "REQ-LIFECYCLE-MODEL-001",
    revision: 1,
    status: "active",
    kind: "functional",
    title: "lifecycle fixture",
    subject: "requirements lifecycle model",
    actionName: "maintain",
    objectName: "a typed catalog requirement",
    rationale: "A concrete item makes lifecycle refinement non-vacuous.",
    sourceRefs: ["model:requirements-lifecycle"],
    acceptanceCriteria: [
      { id: "AC-LIFECYCLE-MODEL-001-1", given: "a current catalog", when_: "a CAS transition is accepted", expected: "catalog and item revisions advance together" }
    ],
    verification: { method: "Quint model", evidence: "catalog lifecycle transition tests" },
    traces: {
      design: [],
      implementation: [],
      tests: [],
      standards: ["QUINT-0.32"],
    },
    lastChangedBy: "model:add",
    retirementReason: "",
    supersededBy: "",
    scopeName: "project",
    categoryName: "nonfunctional",
  }

  pure val successionR1: Requirement = lifecycleRequirement
    .with("id", "REQ-SUCCESSION-R1")
    .with("acceptanceCriteria", [
      { id: "AC-SUCCESSION-R1", given: "R1 exists", when_: "R1 is superseded", expected: "the chain advances" }
    ])
    .with("status", "retired")
    .with("retirementReason", "superseded by R2")
    .with("supersededBy", "REQ-SUCCESSION-R2")
  pure val successionR2: Requirement = lifecycleRequirement
    .with("id", "REQ-SUCCESSION-R2")
    .with("acceptanceCriteria", [
      { id: "AC-SUCCESSION-R2", given: "R2 exists", when_: "R2 is superseded", expected: "the chain advances" }
    ])
    .with("status", "retired")
    .with("retirementReason", "superseded by R3")
    .with("supersededBy", "REQ-SUCCESSION-R3")
  pure val successionR3: Requirement = lifecycleRequirement
    .with("id", "REQ-SUCCESSION-R3")
    .with("acceptanceCriteria", [
      { id: "AC-SUCCESSION-R3", given: "R3 exists", when_: "the chain terminates", expected: "R3 is active" }
    ])
  pure val successionCycleR2: Requirement = successionR2
    .with("supersededBy", "REQ-SUCCESSION-R1")
  pure val successionRetiredTerminalR2: Requirement = successionR2
    .with("supersededBy", "")
  pure val successionCatalog: Catalog = {
    schemaVersion: 1,
    catalogRevision: 1,
    product: "succession-contract",
    updatedAt: "succession:fixture",
    requirements: [successionR1, successionR2, successionR3],
  }

  pure val batchRequirement1: Requirement = lifecycleRequirement
    .with("id", "REQ-BATCH-1")
    .with("acceptanceCriteria", [
      { id: "AC-BATCH-1", given: "batch source", when_: "item one changes", expected: "revision advances once" }
    ])
  pure val batchRequirement2: Requirement = lifecycleRequirement
    .with("id", "REQ-BATCH-2")
    .with("acceptanceCriteria", [
      { id: "AC-BATCH-2", given: "batch source", when_: "item two changes", expected: "revision advances once" }
    ])
  pure val batchRequirement3: Requirement = lifecycleRequirement
    .with("id", "REQ-BATCH-3")
    .with("acceptanceCriteria", [
      { id: "AC-BATCH-3", given: "batch source", when_: "item three changes", expected: "revision advances once" }
    ])
  pure val batchBefore: Catalog = {
    schemaVersion: 1,
    catalogRevision: 5,
    product: "batch-contract",
    updatedAt: "batch:before",
    requirements: [batchRequirement1, batchRequirement2, batchRequirement3],
  }
  pure val batchAfterTwo: Catalog = batchBefore
    .with("catalogRevision", 6)
    .with("updatedAt", "batch:two")
    .with("requirements", [
      batchRequirement1
        .with("revision", 2)
        .with("title", "batch item one updated")
        .with("lastChangedBy", "batch:change"),
      batchRequirement2
        .with("revision", 2)
        .with("traces", batchRequirement2.traces.with("tests", ["tests/batch-two.py"]))
        .with("lastChangedBy", "batch:change"),
      batchRequirement3,
    ])
  pure val batchAfterThree: Catalog = batchBefore
    .with("catalogRevision", 6)
    .with("updatedAt", "batch:three")
    .with("requirements", [
      batchAfterTwo.requirements.nth(0),
      batchAfterTwo.requirements.nth(1),
      batchRequirement3
        .with("revision", 2)
        .with("status", "retired")
        .with("retirementReason", "batch retirement")
        .with("lastChangedBy", "batch:change"),
    ])
  pure val batchStaleAfter: Catalog = batchAfterTwo.with("requirements", [
    batchRequirement1,
    batchAfterTwo.requirements.nth(1),
    batchRequirement3,
  ])
  pure val batchPartialAfterStale: Catalog = batchBefore
    .with("catalogRevision", 6)
    .with("updatedAt", "batch:stale-after-valid")
    .with("requirements", [
      batchAfterTwo.requirements.nth(0),
      batchRequirement2,
      batchRequirement3,
    ])
  pure val batchInvalidAfter: Catalog = batchAfterTwo.with("requirements", [
    batchAfterTwo.requirements.nth(0).with("title", ""),
    batchAfterTwo.requirements.nth(1),
    batchRequirement3,
  ])
  pure val batchUpdateOperation: RequirementOperation = {
    kind: "update",
    id: "REQ-BATCH-1",
    expectedRevision: 1,
    replacement: batchAfterTwo.requirements.nth(0),
  }
  pure val batchTraceOperation: RequirementOperation = {
    kind: "trace",
    id: "REQ-BATCH-2",
    expectedRevision: 1,
    replacement: batchAfterTwo.requirements.nth(1),
  }
  pure val batchRetireOperation: RequirementOperation = {
    kind: "retire",
    id: "REQ-BATCH-3",
    expectedRevision: 1,
    replacement: batchAfterThree.requirements.nth(2),
  }
  pure val batchStaleOperation: RequirementOperation = batchUpdateOperation
    .with("expectedRevision", 0)
  pure val batchStaleTraceOperation: RequirementOperation = batchTraceOperation
    .with("expectedRevision", 0)
  pure val batchInvalidOperation: RequirementOperation = batchUpdateOperation
    .with("replacement", batchInvalidAfter.requirements.nth(0))
  pure val batchResurrectionOperation: RequirementOperation = {
    kind: "update",
    id: "REQ-BATCH-3",
    expectedRevision: 2,
    replacement: batchAfterThree.requirements.nth(2)
      .with("revision", 3)
      .with("status", "active")
      .with("retirementReason", "")
      .with("lastChangedBy", "batch:change"),
  }
  pure val batchResurrectedAfter: Catalog = batchAfterThree
    .with("catalogRevision", 7)
    .with("updatedAt", "batch:resurrection")
    .with("requirements", batchAfterThree.requirements.replaceAt(
      2,
      batchResurrectionOperation.replacement
    ))

  var catalog: Catalog
  var lifecycle: Lifecycle

  action init = all {
    catalog' = requirementsSource,
    lifecycle' = {
      catalogRevision: requirementsSource.catalogRevision,
      itemRevision: 0,
      itemPresent: false,
      itemStatus: "missing",
      traceRevision: 0,
      priorCatalogRevision: requirementsSource.catalogRevision,
      priorItemRevision: 0,
      priorItemPresent: false,
      priorItemStatus: "missing",
      priorTraceRevision: 0,
      lastOperation: "init",
    },
  }

  action addRequirementAt(expectedCatalogRevision: int): bool = all {
    expectedCatalogRevision == catalog.catalogRevision,
    lifecycle.catalogRevision == expectedCatalogRevision,
    not(lifecycle.itemPresent),
    catalog.requirements.indices().forall(i =>
      catalog.requirements.nth(i).id != lifecycleRequirement.id
    ),
    catalog' = catalog
      .with("catalogRevision", catalog.catalogRevision + 1)
      .with("requirements", catalog.requirements.append(lifecycleRequirement)),
    lifecycle' = {
      catalogRevision: lifecycle.catalogRevision + 1,
      itemRevision: 1,
      itemPresent: true,
      itemStatus: "active",
      traceRevision: 0,
      priorCatalogRevision: lifecycle.catalogRevision,
      priorItemRevision: lifecycle.itemRevision,
      priorItemPresent: lifecycle.itemPresent,
      priorItemStatus: lifecycle.itemStatus,
      priorTraceRevision: lifecycle.traceRevision,
      lastOperation: "add",
    },
  }

  action addRequirement = addRequirementAt(lifecycle.catalogRevision)

  def updateRequirementIsAllowed(expectedCatalogRevision: int, expectedItemRevision: int): bool =
    all {
      lifecycle.itemPresent,
      lifecycle.itemStatus == "active",
      expectedCatalogRevision == catalog.catalogRevision,
      expectedCatalogRevision == lifecycle.catalogRevision,
      expectedItemRevision == lifecycle.itemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).id == lifecycleRequirement.id,
      catalog.requirements.nth(catalog.requirements.length() - 1).revision == expectedItemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).status == "active",
      catalog.requirements.nth(catalog.requirements.length() - 1).title != "lifecycle fixture updated",
    }

  action updateRequirementAt(expectedCatalogRevision: int, expectedItemRevision: int): bool = all {
    updateRequirementIsAllowed(expectedCatalogRevision, expectedItemRevision),
    catalog' = catalog
      .with("catalogRevision", catalog.catalogRevision + 1)
      .with(
        "requirements",
        catalog.requirements.replaceAt(
          catalog.requirements.length() - 1,
          catalog.requirements.nth(catalog.requirements.length() - 1)
            .with("revision", expectedItemRevision + 1)
            .with("title", "lifecycle fixture updated")
            .with("lastChangedBy", "model:update")
        )
      ),
    lifecycle' = {
      catalogRevision: lifecycle.catalogRevision + 1,
      itemRevision: lifecycle.itemRevision + 1,
      itemPresent: true,
      itemStatus: "active",
      traceRevision: lifecycle.traceRevision,
      priorCatalogRevision: lifecycle.catalogRevision,
      priorItemRevision: lifecycle.itemRevision,
      priorItemPresent: lifecycle.itemPresent,
      priorItemStatus: lifecycle.itemStatus,
      priorTraceRevision: lifecycle.traceRevision,
      lastOperation: "update",
    },
  }

  action updateRequirement = updateRequirementAt(lifecycle.catalogRevision, lifecycle.itemRevision)

  def traceUpdateIsAllowed(expectedCatalogRevision: int, expectedItemRevision: int): bool =
    all {
      lifecycle.itemPresent,
      lifecycle.itemStatus == "active",
      lifecycle.traceRevision == 0,
      expectedCatalogRevision == catalog.catalogRevision,
      expectedCatalogRevision == lifecycle.catalogRevision,
      expectedItemRevision == lifecycle.itemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).id == lifecycleRequirement.id,
      catalog.requirements.nth(catalog.requirements.length() - 1).revision == expectedItemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).status == "active",
    }

  action updateRequirementTraceAt(expectedCatalogRevision: int, expectedItemRevision: int): bool = all {
    traceUpdateIsAllowed(expectedCatalogRevision, expectedItemRevision),
    catalog' = catalog
      .with("catalogRevision", catalog.catalogRevision + 1)
      .with(
        "requirements",
        catalog.requirements.replaceAt(
          catalog.requirements.length() - 1,
          catalog.requirements.nth(catalog.requirements.length() - 1)
            .with("revision", expectedItemRevision + 1)
            .with(
              "traces",
              catalog.requirements.nth(catalog.requirements.length() - 1).traces.with(
                "tests",
                catalog.requirements.nth(catalog.requirements.length() - 1).traces.tests
                  .append("tests/model-trace-update.py")
              )
            )
            .with("lastChangedBy", "model:trace-update")
        )
      ),
    lifecycle' = {
      catalogRevision: lifecycle.catalogRevision + 1,
      itemRevision: lifecycle.itemRevision + 1,
      itemPresent: true,
      itemStatus: "active",
      traceRevision: lifecycle.traceRevision + 1,
      priorCatalogRevision: lifecycle.catalogRevision,
      priorItemRevision: lifecycle.itemRevision,
      priorItemPresent: lifecycle.itemPresent,
      priorItemStatus: lifecycle.itemStatus,
      priorTraceRevision: lifecycle.traceRevision,
      lastOperation: "trace-update",
    },
  }

  action updateRequirementTrace =
    updateRequirementTraceAt(lifecycle.catalogRevision, lifecycle.itemRevision)

  def retirementIsAllowed(expectedCatalogRevision: int, expectedItemRevision: int): bool =
    all {
      lifecycle.itemPresent,
      lifecycle.itemStatus == "active",
      expectedCatalogRevision == catalog.catalogRevision,
      expectedCatalogRevision == lifecycle.catalogRevision,
      expectedItemRevision == lifecycle.itemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).id == lifecycleRequirement.id,
      catalog.requirements.nth(catalog.requirements.length() - 1).revision == expectedItemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).status == "active",
    }

  action retireRequirementAt(expectedCatalogRevision: int, expectedItemRevision: int): bool = all {
    retirementIsAllowed(expectedCatalogRevision, expectedItemRevision),
    catalog' = catalog
      .with("catalogRevision", catalog.catalogRevision + 1)
      .with(
        "requirements",
        catalog.requirements.replaceAt(
          catalog.requirements.length() - 1,
          catalog.requirements.nth(catalog.requirements.length() - 1)
            .with("revision", expectedItemRevision + 1)
            .with("status", "retired")
            .with("retirementReason", "model retirement")
            .with("lastChangedBy", "model:retire")
        )
      ),
    lifecycle' = {
      catalogRevision: lifecycle.catalogRevision + 1,
      itemRevision: lifecycle.itemRevision + 1,
      itemPresent: true,
      itemStatus: "retired",
      traceRevision: lifecycle.traceRevision,
      priorCatalogRevision: lifecycle.catalogRevision,
      priorItemRevision: lifecycle.itemRevision,
      priorItemPresent: lifecycle.itemPresent,
      priorItemStatus: lifecycle.itemStatus,
      priorTraceRevision: lifecycle.traceRevision,
      lastOperation: "retire",
    },
  }

  action retireRequirement = retireRequirementAt(lifecycle.catalogRevision, lifecycle.itemRevision)

  action lifecycleStutter = all {
    catalog' = catalog,
    lifecycle' = {
      catalogRevision: lifecycle.catalogRevision,
      itemRevision: lifecycle.itemRevision,
      itemPresent: lifecycle.itemPresent,
      itemStatus: lifecycle.itemStatus,
      traceRevision: lifecycle.traceRevision,
      priorCatalogRevision: lifecycle.catalogRevision,
      priorItemRevision: lifecycle.itemRevision,
      priorItemPresent: lifecycle.itemPresent,
      priorItemStatus: lifecycle.itemStatus,
      priorTraceRevision: lifecycle.traceRevision,
      lastOperation: "none",
    },
  }

  action counterOnlyMutation = all {
    catalog' = catalog,
    lifecycle' = lifecycle.with("catalogRevision", lifecycle.catalogRevision + 1),
  }

  action step = any {
    addRequirement,
    updateRequirement,
    updateRequirementTrace,
    retireRequirement,
    lifecycleStutter,
  }

  pure val allowedStatuses = Set("active", "retired")
  pure val allowedKinds = Set("functional", "quality", "constraint", "interface", "data", "operational")
  pure val allowedScopes = Set("product", "project")
  pure val allowedCategories = Set("functional", "nonfunctional")
  pure val allowedActions = Set(
    "constrain", "derive", "detect", "discover", "enable", "enforce", "estimate",
    "expand", "formalize", "generate", "maintain", "measure", "parse", "preserve",
    "provide", "route", "select", "separate", "stage", "stop", "structure", "validate", "verify"
  )

  pure def stringsAreUnique(values: List[str]): bool = values.indices().forall(i =>
    values.indices().forall(j => i == j or values.nth(i) != values.nth(j))
  )

  pure def stringsAreNonempty(values: List[str]): bool =
    values.indices().forall(i => values.nth(i) != "")

  pure def requirementIdsAreUniqueIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i =>
      requirements.indices().forall(j =>
        i == j or requirements.nth(i).id != requirements.nth(j).id
      )
    )

  val requirementIdsAreUnique = requirementIdsAreUniqueIn(catalog.requirements)

  // 構造的完全性は機械検査する。1 IDが意味的に1義務だけを表すかは、
  // 自然言語を解釈できる権限あるhuman semantic reviewの責務である。
  pure def requirementsAreStructurallyCompleteIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i => all {
      requirements.nth(i).id != "",
      requirements.nth(i).revision >= 1,
      requirements.nth(i).title != "",
      requirements.nth(i).subject != "",
      requirements.nth(i).actionName != "",
      requirements.nth(i).objectName != "",
      requirements.nth(i).rationale != "",
      requirements.nth(i).lastChangedBy != "",
      requirements.nth(i).sourceRefs.length() > 0,
      stringsAreNonempty(requirements.nth(i).sourceRefs),
      stringsAreUnique(requirements.nth(i).sourceRefs),
      requirements.nth(i).acceptanceCriteria.length() > 0,
      requirements.nth(i).verification.method != "",
      requirements.nth(i).verification.evidence != "",
    })

  val requirementsAreStructurallyComplete =
    requirementsAreStructurallyCompleteIn(catalog.requirements)

  pure def requirementsAreTypedIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i => all {
      allowedStatuses.contains(requirements.nth(i).status),
      allowedKinds.contains(requirements.nth(i).kind),
      allowedActions.contains(requirements.nth(i).actionName),
      (requirements.nth(i).scopeName == "").or(allowedScopes.contains(requirements.nth(i).scopeName)),
      (requirements.nth(i).categoryName == "").or(allowedCategories.contains(requirements.nth(i).categoryName)),
    })

  val requirementsAreTyped = requirementsAreTypedIn(catalog.requirements)

  pure def acceptanceCriteriaAreCompleteIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i =>
      requirements.nth(i).acceptanceCriteria.indices().forall(j => all {
        requirements.nth(i).acceptanceCriteria.nth(j).id != "",
        requirements.nth(i).acceptanceCriteria.nth(j).given != "",
        requirements.nth(i).acceptanceCriteria.nth(j).when_ != "",
        requirements.nth(i).acceptanceCriteria.nth(j).expected != "",
      })
    )

  val acceptanceCriteriaAreComplete =
    acceptanceCriteriaAreCompleteIn(catalog.requirements)

  pure def acceptanceCriterionIdsAreUniqueIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i =>
      requirements.indices().forall(j =>
        requirements.nth(i).acceptanceCriteria.indices().forall(x =>
          requirements.nth(j).acceptanceCriteria.indices().forall(y =>
          (i == j and x == y) or
            requirements.nth(i).acceptanceCriteria.nth(x).id !=
              requirements.nth(j).acceptanceCriteria.nth(y).id
          )
        )
      )
    )

  val acceptanceCriterionIdsAreUnique =
    acceptanceCriterionIdsAreUniqueIn(catalog.requirements)

  pure def traceLinksAreUniqueIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i => all {
      stringsAreNonempty(requirements.nth(i).traces.design),
      stringsAreNonempty(requirements.nth(i).traces.implementation),
      stringsAreNonempty(requirements.nth(i).traces.tests),
      stringsAreNonempty(requirements.nth(i).traces.standards),
      stringsAreUnique(requirements.nth(i).traces.design),
      stringsAreUnique(requirements.nth(i).traces.implementation),
      stringsAreUnique(requirements.nth(i).traces.tests),
      stringsAreUnique(requirements.nth(i).traces.standards),
    })

  val traceLinksAreUnique = traceLinksAreUniqueIn(catalog.requirements)

  pure def classificationIsPairedIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i =>
      (requirements.nth(i).scopeName == "") iff
      (requirements.nth(i).categoryName == "")
    )

  val classificationIsPaired = classificationIsPairedIn(catalog.requirements)

  pure def retirementFieldsAreConsistentIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i => all {
    (requirements.nth(i).status == "active").implies(all {
      requirements.nth(i).retirementReason == "",
      requirements.nth(i).supersededBy == "",
    }),
    (requirements.nth(i).status == "retired").implies(
      requirements.nth(i).retirementReason != ""
    ),
    (requirements.nth(i).supersededBy != "").implies(all {
      requirements.nth(i).status == "retired",
      requirements.nth(i).supersededBy != requirements.nth(i).id,
    }),
  })

  val retirementFieldsAreConsistent =
    retirementFieldsAreConsistentIn(catalog.requirements)

  pure def supersessionChainsAreValid(requirements: List[Requirement]): bool =
    requirements.indices().forall(i =>
      (requirements.nth(i).supersededBy != "").implies(
        requirements.indices().exists(j => all {
          j > i,
          requirements.nth(j).id == requirements.nth(i).supersededBy,
          requirements.nth(j).id != requirements.nth(i).id,
          (requirements.nth(j).status == "active").or(all {
            requirements.nth(j).status == "retired",
            requirements.nth(j).supersededBy != "",
          }),
        })
      )
    )

  pure def catalogHeaderIsValid(source: Catalog): bool = all {
    source.schemaVersion == 1,
    source.catalogRevision >= 1,
    source.product != "",
    source.updatedAt != "",
    source.requirements.length() > 0,
  }

  // Pure catalog component of catalogWellFormed. Lifecycle witness refinement
  // remains a state invariant below and is intentionally not fabricated for a
  // caller-supplied batch result.
  pure def catalogDataWellFormed(source: Catalog): bool = all {
    catalogHeaderIsValid(source),
    requirementIdsAreUniqueIn(source.requirements),
    requirementsAreStructurallyCompleteIn(source.requirements),
    requirementsAreTypedIn(source.requirements),
    acceptanceCriteriaAreCompleteIn(source.requirements),
    acceptanceCriterionIdsAreUniqueIn(source.requirements),
    traceLinksAreUniqueIn(source.requirements),
    classificationIsPairedIn(source.requirements),
    retirementFieldsAreConsistentIn(source.requirements),
    supersessionChainsAreValid(source.requirements),
  }

  pure def stringsContain(values: List[str], value: str): bool =
    values.indices().exists(i => values.nth(i) == value)

  pure def requirementExists(requirements: List[Requirement], id: str): bool =
    requirements.indices().exists(i => requirements.nth(i).id == id)

  pure def requirementById(requirements: List[Requirement], id: str): Requirement =
    requirements.select(requirement => requirement.id == id).head()

  pure def replaceRequirement(
    requirements: List[Requirement],
    id: str,
    replacement: Requirement,
  ): List[Requirement] =
    range(0, requirements.length()).foldl(requirements, (result, index) =>
      if (result.nth(index).id == id)
        result.replaceAt(index, replacement)
      else
        result
    )

  pure def updateReplacementIsValid(
    current: Requirement,
    replacement: Requirement,
    changeId: str,
  ): bool = all {
    current.status == "active",
    replacement == current
      .with("revision", current.revision + 1)
      .with("kind", replacement.kind)
      .with("title", replacement.title)
      .with("subject", replacement.subject)
      .with("actionName", replacement.actionName)
      .with("objectName", replacement.objectName)
      .with("rationale", replacement.rationale)
      .with("sourceRefs", replacement.sourceRefs)
      .with("acceptanceCriteria", replacement.acceptanceCriteria)
      .with("verification", replacement.verification)
      .with("scopeName", replacement.scopeName)
      .with("categoryName", replacement.categoryName)
      .with("lastChangedBy", changeId),
    replacement
      .with("revision", current.revision)
      .with("lastChangedBy", current.lastChangedBy) != current,
  }

  pure def traceReplacementIsValid(
    current: Requirement,
    replacement: Requirement,
    changeId: str,
  ): bool = all {
    current.status == "active",
    replacement.traces != current.traces,
    replacement == current
      .with("revision", current.revision + 1)
      .with("traces", replacement.traces)
      .with("lastChangedBy", changeId),
  }

  pure def retirementReplacementIsValid(
    current: Requirement,
    replacement: Requirement,
    changeId: str,
  ): bool = all {
    current.status == "active",
    replacement.retirementReason != "",
    replacement == current
      .with("revision", current.revision + 1)
      .with("status", "retired")
      .with("retirementReason", replacement.retirementReason)
      .with("supersededBy", replacement.supersededBy)
      .with("lastChangedBy", changeId),
  }

  pure def batchOperationIsAllowed(
    accumulator: BatchFold,
    operation: RequirementOperation,
    changeId: str,
  ): bool =
    if (not(accumulator.valid)) false
    else if (stringsContain(accumulator.touchedIds, operation.id)) false
    else if (operation.kind == "add") all {
      not(requirementExists(accumulator.requirements, operation.id)),
      operation.expectedRevision == 0,
      operation.id == operation.replacement.id,
      operation.replacement.revision == 1,
      operation.replacement.status == "active",
      operation.replacement.retirementReason == "",
      operation.replacement.supersededBy == "",
      operation.replacement.lastChangedBy == changeId,
    }
    else if (not(requirementExists(accumulator.requirements, operation.id))) false
    else if (
      operation.expectedRevision !=
        requirementById(accumulator.requirements, operation.id).revision
    ) false
    else if (operation.kind == "update") updateReplacementIsValid(
      requirementById(accumulator.requirements, operation.id),
      operation.replacement,
      changeId
    )
    else if (operation.kind == "trace") traceReplacementIsValid(
      requirementById(accumulator.requirements, operation.id),
      operation.replacement,
      changeId
    )
    else if (operation.kind == "retire") retirementReplacementIsValid(
      requirementById(accumulator.requirements, operation.id),
      operation.replacement,
      changeId
    )
    else false

  pure def applyBatchOperation(
    accumulator: BatchFold,
    operation: RequirementOperation,
    changeId: str,
  ): BatchFold =
    if (batchOperationIsAllowed(accumulator, operation, changeId)) {
      requirements:
        if (operation.kind == "add")
          accumulator.requirements.append(operation.replacement)
        else
          replaceRequirement(accumulator.requirements, operation.id, operation.replacement),
      touchedIds: accumulator.touchedIds.append(operation.id),
      valid: true,
    } else accumulator.with("valid", false)

  pure def initialBatchFold(before: Catalog): BatchFold = {
    requirements: before.requirements,
    touchedIds: [],
    valid: true,
  }

  pure def foldBatchOperations(
    before: Catalog,
    operations: List[RequirementOperation],
    changeId: str,
  ): BatchFold = operations.foldl(
    initialBatchFold(before),
    (accumulator, operation) => applyBatchOperation(accumulator, operation, changeId)
  )

  pure def batchCandidate(
    before: Catalog,
    operations: List[RequirementOperation],
    changedAt: str,
    changeId: str,
  ): Catalog = before
    .with("catalogRevision", before.catalogRevision + 1)
    .with("updatedAt", changedAt)
    .with("requirements", foldBatchOperations(before, operations, changeId).requirements)

  pure def batchWouldBeAccepted(
    before: Catalog,
    expectedCatalogRevision: int,
    operations: List[RequirementOperation],
    changedAt: str,
    changeId: str,
  ): bool = all {
    expectedCatalogRevision == before.catalogRevision,
    operations.length() > 0,
    changedAt != "",
    changeId != "",
    foldBatchOperations(before, operations, changeId).valid,
    catalogDataWellFormed(batchCandidate(before, operations, changedAt, changeId)),
  }

  // This relation models the same arbitrary-length operation fold and CAS
  // boundary as specflow.apply_change. No operation may resurrect a retired
  // item, and any stale or invalid member makes the entire batch stutter.
  pure def atomicBatchTransitionIsValid(
    before: Catalog,
    after: Catalog,
    expectedCatalogRevision: int,
    operations: List[RequirementOperation],
    changedAt: str,
    changeId: str,
    outcome: str,
  ): bool = all {
    Set("accepted", "rejected").contains(outcome),
    catalogDataWellFormed(before),
    (outcome == "accepted") iff batchWouldBeAccepted(
      before, expectedCatalogRevision, operations, changedAt, changeId
    ),
    (outcome == "accepted").implies(
      after == batchCandidate(before, operations, changedAt, changeId)
    ),
    (outcome == "rejected").implies(after == before),
  }

  val lifecycleRevisionTransitionIsSound = all {
    Set("init", "add", "update", "trace-update", "retire", "none").contains(lifecycle.lastOperation),
    (lifecycle.lastOperation == "init").implies(all {
      lifecycle.catalogRevision == requirementsSource.catalogRevision,
      lifecycle.itemRevision == 0,
      not(lifecycle.itemPresent),
    }),
    (lifecycle.lastOperation == "add").implies(all {
      not(lifecycle.priorItemPresent),
      lifecycle.itemPresent,
      lifecycle.itemStatus == "active",
      lifecycle.catalogRevision == lifecycle.priorCatalogRevision + 1,
      lifecycle.itemRevision == 1,
    }),
    (lifecycle.lastOperation == "update").implies(all {
      lifecycle.priorItemPresent,
      lifecycle.priorItemStatus == "active",
      lifecycle.itemStatus == "active",
      lifecycle.catalogRevision == lifecycle.priorCatalogRevision + 1,
      lifecycle.itemRevision == lifecycle.priorItemRevision + 1,
      lifecycle.traceRevision == lifecycle.priorTraceRevision,
    }),
    (lifecycle.lastOperation == "trace-update").implies(all {
      lifecycle.priorItemPresent,
      lifecycle.priorItemStatus == "active",
      lifecycle.itemStatus == "active",
      lifecycle.catalogRevision == lifecycle.priorCatalogRevision + 1,
      lifecycle.itemRevision == lifecycle.priorItemRevision + 1,
      lifecycle.traceRevision == lifecycle.priorTraceRevision + 1,
    }),
    (lifecycle.lastOperation == "retire").implies(all {
      lifecycle.priorItemPresent,
      lifecycle.priorItemStatus == "active",
      lifecycle.itemPresent,
      lifecycle.itemStatus == "retired",
      lifecycle.catalogRevision == lifecycle.priorCatalogRevision + 1,
      lifecycle.itemRevision == lifecycle.priorItemRevision + 1,
      lifecycle.traceRevision == lifecycle.priorTraceRevision,
    }),
    (lifecycle.lastOperation == "none").implies(all {
      lifecycle.catalogRevision == lifecycle.priorCatalogRevision,
      lifecycle.itemRevision == lifecycle.priorItemRevision,
      lifecycle.itemPresent == lifecycle.priorItemPresent,
      lifecycle.itemStatus == lifecycle.priorItemStatus,
      lifecycle.traceRevision == lifecycle.priorTraceRevision,
    }),
  }

  val lifecycleRefinesCatalog = all {
    lifecycle.catalogRevision == catalog.catalogRevision,
    lifecycle.itemPresent iff
      catalog.requirements.indices().exists(i =>
        catalog.requirements.nth(i).id == lifecycleRequirement.id
      ),
    lifecycle.itemPresent.implies(all {
      catalog.requirements.nth(catalog.requirements.length() - 1).id == lifecycleRequirement.id,
      catalog.requirements.nth(catalog.requirements.length() - 1).revision == lifecycle.itemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).status == lifecycle.itemStatus,
      (lifecycle.traceRevision == 0).implies(
        catalog.requirements.nth(catalog.requirements.length() - 1).traces.tests ==
          lifecycleRequirement.traces.tests
      ),
      (lifecycle.traceRevision == 1).implies(
        catalog.requirements.nth(catalog.requirements.length() - 1).traces.tests ==
          lifecycleRequirement.traces.tests.append("tests/model-trace-update.py")
      ),
    }),
  }

  val catalogWellFormed = all {
    catalogDataWellFormed(catalog),
    lifecycleRevisionTransitionIsSound,
    lifecycleRefinesCatalog,
  }

  run catalogContractTest = {
    init.then(all {
      assert(catalogWellFormed),
      catalog' = catalog,
      lifecycle' = lifecycle,
    })
  }

  run catalogAndSupersessionMutationRejectionTest = {
    init.then(all {
      assert(not(catalogHeaderIsValid(catalog.with("requirements", [])))),
      assert(catalogDataWellFormed(successionCatalog)),
      assert(supersessionChainsAreValid([successionR1, successionR2, successionR3])),
      assert(not(catalogDataWellFormed(successionCatalog.with("requirements", [successionR1])))),
      assert(not(catalogDataWellFormed(successionCatalog.with("requirements", [successionR1, successionRetiredTerminalR2])))),
      assert(not(catalogDataWellFormed(successionCatalog.with("requirements", [successionR1, successionCycleR2])))),
      assert(not(supersessionChainsAreValid([successionR1]))),
      assert(not(supersessionChainsAreValid([successionR1, successionRetiredTerminalR2]))),
      assert(not(supersessionChainsAreValid([successionR1, successionCycleR2]))),
      catalog' = catalog,
      lifecycle' = lifecycle,
    })
  }

  run atomicBatchTransitionContractTest = {
    init.then(all {
      assert(atomicBatchTransitionIsValid(batchBefore, batchAfterTwo, 5, [batchUpdateOperation, batchTraceOperation], "batch:two", "batch:change", "accepted")),
      assert(atomicBatchTransitionIsValid(batchBefore, batchAfterThree, 5, [batchUpdateOperation, batchTraceOperation, batchRetireOperation], "batch:three", "batch:change", "accepted")),
      assert(atomicBatchTransitionIsValid(batchBefore, batchBefore, 4, [batchUpdateOperation], "batch:stale-catalog", "batch:change", "rejected")),
      assert(atomicBatchTransitionIsValid(batchBefore, batchBefore, 5, [batchStaleOperation], "batch:stale-item", "batch:change", "rejected")),
      assert(atomicBatchTransitionIsValid(batchBefore, batchBefore, 5, [batchUpdateOperation, batchStaleTraceOperation], "batch:stale-after-valid", "batch:change", "rejected")),
      assert(not(atomicBatchTransitionIsValid(batchBefore, batchPartialAfterStale, 5, [batchUpdateOperation, batchStaleTraceOperation], "batch:stale-after-valid", "batch:change", "accepted"))),
      assert(atomicBatchTransitionIsValid(batchBefore, batchBefore, 5, [batchUpdateOperation, batchUpdateOperation], "batch:duplicate", "batch:change", "rejected")),
      assert(atomicBatchTransitionIsValid(batchBefore, batchBefore, 5, [batchInvalidOperation], "batch:invalid", "batch:change", "rejected")),
      assert(not(atomicBatchTransitionIsValid(batchBefore, batchInvalidAfter, 5, [batchInvalidOperation], "batch:invalid", "batch:change", "accepted"))),
      assert(catalogDataWellFormed(batchResurrectedAfter)),
      assert(atomicBatchTransitionIsValid(batchAfterThree, batchAfterThree, 6, [batchResurrectionOperation], "batch:resurrection", "batch:change", "rejected")),
      assert(not(atomicBatchTransitionIsValid(batchAfterThree, batchResurrectedAfter, 6, [batchResurrectionOperation], "batch:resurrection", "batch:change", "accepted"))),
      catalog' = catalog,
      lifecycle' = lifecycle,
    })
  }

  run lifecycleContractTest = {
    init
      .then(addRequirement)
      .then(updateRequirement)
      .then(updateRequirementTrace)
      .then(retireRequirement)
      .then(all {
        assert(catalogWellFormed),
        assert(lifecycleRefinesCatalog),
        assert(not(updateRequirementIsAllowed(catalog.catalogRevision, lifecycle.itemRevision))),
        assert(not(traceUpdateIsAllowed(catalog.catalogRevision, lifecycle.itemRevision))),
        catalog' = catalog,
        lifecycle' = lifecycle,
      })
  }

  run lifecycleCasRejectionTest = {
    init
      .then(addRequirement)
      .then(all {
        assert(not(updateRequirementIsAllowed(catalog.catalogRevision - 1, lifecycle.itemRevision))),
        assert(not(updateRequirementIsAllowed(catalog.catalogRevision, lifecycle.itemRevision - 1))),
        catalog' = catalog,
        lifecycle' = lifecycle,
      })
  }


  run refinementRejectsCounterOnlyMutationTest = {
    init
      .then(counterOnlyMutation)
      .then(all {
        assert(not(lifecycleRefinesCatalog)),
        catalog' = catalog,
        lifecycle' = lifecycle,
      })
  }
}
