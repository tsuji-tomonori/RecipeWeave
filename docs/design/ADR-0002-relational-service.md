# ADR-0002 全量の正規化モデルと実APIへの移行

状態: 採用。ADR-0001の2表スナップショット保存とDSQL選択を、この変更で置き換える。

## 要求と根拠

2026-09-06の利用者指示に従い、Google Sheetsで定義した71テーブル・554カラムをすべて実装する。
取得した正本は `spec/database/source-sheet.json`、食品・組合せ候補は `spec/database/catalog-source-sheet.json` に保持する。
元の表と実DDLの対応は設計生成器が照合する。現在の実装数を目標設計の数として代用しない。

開発・証跡・公開サイトの参照は `tsuji-tomonori/CornellNoteWebv2` のdev、
commit `aa680430d7b309a3ed478dc86d17e23198fd1089`。
PostgreSQLの結合試験、日本語のGiven/When/Thenの画像証跡、APIごとの6帳票、
検索できる設計サイトと品質レポートの公開をRecipeWeaveの構成へ適用する。

## 採用する保存とAPI

- 料理・食品・工程・材料・献立・在庫・履歴はPostgreSQLの正規化行を正本とする。
  初期投入ファイルはseedの入力であり、APIや本番Webから読み込まない。
- 全表へ用途に応じた型付き操作を生成する。個人データは行と親参照の所有権を検査する。
  追記専用台帳、公開済み版、生成リースには、その意味を壊す汎用更新を提供しない。
- 食品IDと材料行ID、料理IDと料理版ID、商品と商品版を区別する。
  献立は選択した料理版を固定し、材料ごとの上書きは材料行IDで保持する。
- 画面用のGET集約はJSONで返すが、AppState全体を保存するAPIは設けない。
  更新は業務操作ごとのSQLで行い、集約版・監査・在庫消費を同じトランザクションで確定する。
- 遅延制約の失敗を成功応答にしないため、DB依存の終了をFastAPIのfunction scopeに置く。
  これは応答送信前にトランザクションを確定するための選択である。
  [FastAPIの依存終了タイミング](https://fastapi.tiangolo.com/advanced/advanced-dependencies/)

## DBエンジンと補完

ローカル・CIはPostgreSQL 16とpgvector、本番向け構成はAurora PostgreSQLを採用する。
本モデルのPL/pgSQL関数、トリガー、行レベルセキュリティ等をDB側で検証するためである。
DSQLの外部キー対応状況を移行理由にしない。DSQLのPL/pgSQL・トリガーとの相違が根拠である。
[AWSのPostgreSQL互換性資料](https://docs.aws.amazon.com/aurora-dsql/latest/userguide/working-with-postgresql-compatibility-migration-guide.html)

元71表の構造を002で実装し、003には実サービスに必要なレシート、本人の更新版、
独自食材所有、常備指定、買い物確認、在庫消費の台帳を追加する。
不明な在庫量は明示した品質状態とNULLで表現する。元のNULL不可からの変更は移行に明記する。
私有カタログは共通の公開版と分離し、利用者消去時に共通食品へ変えて公開しない。
テーブル数・追加列・外部キー数は手書きで重複保守せず、DDL由来の設計書で確認する。

## 認証、検証、配備の区別

本番はCognitoの署名・発行者・用途・アプリクライアントを検証する。
固定ログインは明示したlocal/test環境だけで、Lambdaでは無効にする。
CIは管理者の移行接続とNOSUPERUSER/NOBYPASSRLSのアプリ接続を分けて実行する。

Pagesの先頭はWebアプリ、`quality/`は検査結果、`quality/design/`は設計サイトとする。
PagesはAPIやDBを実行しない。実際に配備したAPIのURLがない場合は接続未設定を示し、
見本データの応答へ切り替えない。AWSの合成・構造試験と実配備の成功を区別する。
