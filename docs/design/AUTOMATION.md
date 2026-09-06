# 設計書の自動生成と品質証跡

Dev Standardの要件正本・実装由来の設計・必要な品質ゲートを維持する。
今回の公開形式は `CornellNoteWebv2` の dev `aa680430d7b309a3ed478dc86d17e23198fd1089` を参照し、
検索可能なStarlight設計サイト、実行結果一覧、日本語のGiven / When / Then画像を導入した。
レシピサービスのアプリはPagesのトップ、品質証跡は `/quality/`、設計は `/quality/design/` に置く。

## 実装と設計の正本

要件は `spec/requirements/requirements.qnt`、原DB計画はDriveから取得した
`spec/database/source-sheet.json`、物理構造は `database/migrations/*.sql`、
提供APIはFastAPIが実際に登録するルートとOpenAPIを正とする。
初期の2表だけの実装は原DB計画の完了ではなかったため、元の71表を実装して照合対象に含める。
追加表・補完列・移行台帳も実DDLから数え、期待件数を固定文字列で書き込まない。

| 入力 | 自動生成する設計 |
|---|---|
| PostgreSQL文法で解析した全移行、DDLから抽出したカタログ | 全テーブル一覧、列型・NULL・既定値・CHECK・一意性・外部キー・索引、ER |
| DDLのCOMMENT、原設計との対応、保持方針 | テーブル・列の日本語の意味と保持区分 |
| 実OpenAPIと操作メタデータ | API一覧、型・制約・enum、認証、要求・応答、単独のSwagger互換JSON |
| 操作ごとのSQL、共有監査・アウトボックスSQL | SQL全文、バインド、実テーブルと列、縦方向のCRUD対応 |
| router・functions・共有EntityServiceのAST | 入力→DBと値の出所→返却値の詳細設計、分岐とトランザクションのシーケンス |
| 実logger呼出 | ログレベル、イベント本文、構造化項目、発生関数・位置 |
| テスト関数・明示した要因対応 | 要因別のGiven / When / Thenと実在test node、表明 |
| CDK合成結果、フロント実装、初期投入データ | 実装要素、配備定義、再現用データの記録 |
| 全入力と出力 | 出力一覧、SHA-256マニフェスト |

APIごとに **詳細・インターフェース・メッセージ・クエリ・シーケンス・要因別テストの6帳票** を生成する。
詳細設計をソースコード全文の貼付で代替しない。ログはHTTPエラー本文を転記せず、実装された出力を載せる。
SQLを持たない操作やログを持たない操作では、その事実を明示する。

## 更新コマンド

リポジトリのルートで実行する。Pythonはuv、Nodeは各package-lockに固定する。
CDK合成と実OpenAPI・SQL呼出しの生成を先に完了する。

```sh
uv run python database/schema_catalog.py --check
uv run python tools/generate_entity_apis.py --check
uv run python tools/generate_backup_api.py --check
uv run app-sql-lint
uv run app-docs
npm --prefix infra run synth
uv run python -m recipeweave_generator.design
uv run python tools/generate_service_design.py
uv run python tools/generate_service_design.py --check
uv run pytest tests/test_service_design.py tests/test_quality_reports.py
python tools/report.py
DOCS_BASE=/RecipeWeave/quality/design python tools/docs_site.py
```

出力入口は [生成設計書](generated/README.md)。API・DBの生成専用ディレクトリと管理対象の一覧ファイルだけを更新する。
`--check`は一切書き込まず、差分・欠落・余剰を検出する。削除されたAPIの古い仕様は生成時に削除する。
シンボリックリンク、管理範囲から外れるパス、未定義のOpenAPI参照を拒否する。

## PostgreSQLの解析範囲

SQLFluff、SQLGlot、pglastを役割ごとに使う。
SQLFluffはSQLの構文と記法、SQLGlotはAPIクエリの名前解決・対象表・列・CRUD、
pglastは全移行のPostgreSQL構文を検査する。
DDLカタログの表・列・外部キー・索引集合はpglastの文法木と照合し、抽出の漏れを成功扱いしない。
CREATE TABLE以外の拡張、外部キー追加、索引、CHECK、関数、トリガー、RLSも移行契約として生成する。
PL/pgSQL関数本体の意味は静的な一覧だけで証明せず、実PostgreSQLの移行・制約試験を別に実施する。

CTE・副問い合わせ・集約・表関数の派生列はSQLGlotのscopeで解決し、派生表を物理表として数えない。
PostgreSQLの `xmin` は競合判定用のシステム列として認識する。
`ON CONFLICT DO UPDATE` は新規作成と更新の両方へ投影し、競合キーと更新式を残す。
`FOR SHARE OF` 等のロック別名は同じ問い合わせの表と照合してから列解析し、SQL仕様には元の句を残す。
復元候補の制約検証に使う `SET CONSTRAINTS ALL IMMEDIATE/DEFERRED` はpglastで単文・対象ALLを検証し、
CRUDを追加せず検証タイミングの変更として詳細設計へ記載する。他のSET文や複数文は許可しない。
バックアップの挿入値は型付き本文の各表・各列から実装上の行展開と型変換まで追跡し、保存済みの行IDを新規発行IDと混同しない。
要因別試験は `backend/tests/*_test_contracts.json` を全件読み、実在する試験関数と対応づける。
更新と同じトランザクションで行う監査・アウトボックスへのINSERTも各操作のCRUDへ含める。
実装とSQLの列集合が不一致、未定義表、不正な列参照、未対応の複合DMLは生成を停止する。

## 品質証跡の入力と公開

| 実測ファイル | 公開内容 |
|---|---|
| `reports/quality.json` | 検査名・終了コード・実出力、失敗の理由 |
| `reports/*-junit.xml`、`reports/pytest.xml`、`reports/vitest.json` | パラメーター展開後の単体・結合テスト一覧、失敗・スキップ |
| `reports/playwright.json` | E2Eケース、各段階の日本語説明、取得したPNG |
| `reports/python-coverage.json`、`reports/frontend-coverage/coverage-summary.json` | C0・C1とコード行のHTMLレポートへのリンク |
| `reports/sqlfluff.json` | SQLの実指摘と対応するソース |

Playwrightでは `Given: 日本語の前提`、`When: 日本語の操作`、`Then: 日本語の結果` の名前でPNGをattachする。
各画像はその操作で取得したものを使う。未実行は未実行、未計測は未計測と表示し、0件を成功へ変換しない。
成功したE2Eで3段階の画像が欠けている場合、品質レポート生成も「証跡不足」で失敗する。
実装からの設計はコードとの一致を示す資料で、AWS実配備や実ログインの成功実績とは区別する。

Starlightは検索・章一覧・ページ内見出し・Mermaidを備える。
Markdown内部リンクは公開URLへ変換し、変換対象の欠落とビルド後の内部リンク切れを検出する。
品質画面は全ケースを常時表示し、PC・スマートフォン別に選べる階層一覧と画像の原寸表示を用意する。
GitHub Pagesではアプリ成果物へ `reports/` を `quality/` として組み込み、同じ検証対象コミットを表示する。

## 日本語とスキル

手書きのコメント・docstring・人向け説明は日本語にする。識別子・外部仕様値は原表記を保持する。
適用済み移行001のチェックサムは保持する。固定配布スキル・receiptのhashは書き換えず、
プロジェクト固有の生成契約は `recipeweave-design-contract` へ追記する。
公開は既存のGitHub環境保護に従い、検査の無効化や別環境への付け替えで回避しない。
