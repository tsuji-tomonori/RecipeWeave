---
name: recipeweave-design-contract
description: RecipeWeaveのAPI・DB・SQL・設計生成器を変更するとき、実装由来のMarkdown設計、API別SQL、静的解析、日本語の説明を同じ変更へ対応させる。汎用dev-standardの導入や他リポジトリの設定には使用しない。
---

# RecipeWeaveの実装と生成設計

このスキルはRecipeWeave固有の生成契約を補足する。導入済みdev-standardの要件・設計・検査の3本柱を維持し、ブランチ、マージ、承認の追加規則を設けない。

## 変更の入口

- 永続義務を変更する場合は`spec/requirements/requirements.qnt`を更新し、`python tools/quintflow.py generate`でJSONと人向けMarkdownを生成する。生成された要件を手編集しない。
- APIやDDLの変更時は[生成対象と入力契約](references/service-design.md)を読み、ソースと同じ変更で設計生成器・出力・対象検査を更新する。手書きの一覧で生成漏れを埋めない。
- 人向けの生成設計は`docs/design/generated/`配下のMarkdownとする。機械用のOpenAPI JSONや要件JSONは、人向け仕様の代わりとして数えない。
- 元DB正本は`spec/database/source-sheet.json`。全表・列・外部キーをDDLと照合し、実装済みの一部の表だけを数えて完了としない。必要な補完と元定義の進化は追加移行へ明記する。
- 食品・料理の初期ファイルはseed入力専用とする。API・Webの実行時参照とJSON全状態保存を追加しない。料理版IDと材料行IDを保持する。

## SQLの扱い

- 永続化するAPI操作の`sql/`にSQL文ごとの`.sql`を置き、`uv run app-docs`で型付き呼出しを生成する。`functions.py`から永続化のポートを呼び、その実装が生成されたクエリを使う。ORMや別の手書きクエリをSQL正本へ混在させない。
- 束縛値をSQL文字列へ連結せず、採用したパラメータ契約を使う。DB操作のないAPIへ形だけのSQLを追加しない。
- SQL変更時は`uv run app-sql-lint`と`uv run app-docs --check`を実行する。SQLFluffの構文解析失敗や対象漏れを無視せず、SQLGlotによる型付き生成・設計導出も確認する。
- 適用済み移行のchecksumは保持する。日本語化だけのために過去の移行を変更せず、新しい移行と説明を追加する。

## 生成と検証

`uv run python tools/generate_service_design.py`をプロジェクトの生成入口、同じコマンドの`--check`を差分検査の入口とする。API用の`app-docs`生成と、インフラ用の既存CDK合成を先に完了させる。対象の構成や配布物がなければ準備不足として報告し、架空の合成結果を作らない。

CDK資材を変更するときは`backend/tools/package_lambda.py --verify-reproducible`で別出力先との全バイト一致を確認し、画面もCIと同じ公開設定で構築する。import検証のbytecodeや起動スクリプトの絶対パスを配備資材へ持ち込まない。設計の実合成入力hashとDevのclean-tree検査を残し、環境差による生成差分を無視する例外は設けない。

変更に応じて、次のうち失敗を検出できる検査を選ぶ。

- 同一入力で2回生成したときの全出力のbyte一致。
- スキーマ・SQL・ルートの変更が各仕様へ反映されること。
- 解析対象内の未対応構文、API対応の欠落や重複を拒否すること。
- `--check`が変更・欠落・余剰を検出し、repositoryを書き換えないこと。
- 既存のSQL静的解析、型検査、生成されたクエリの回帰試験。

コメント・docstring・生成文書の説明は原則日本語とし、ソースを修正してから再生成する。識別子や機械用指示等の例外は`AGENTS.md`に従う。現在の実装を説明する生成設計と、実際のAWS配備・認証同期の受入結果を区別する。

実DBの制約・所有権・再送・競合の変更はPostgreSQLと非管理者アプリロールで検証する。
実DBテストが接続不足でskipされた結果を、DB検証の成功へ読み替えない。
E2Eは日本語Given/When/Thenごとに実画面を保存し、実行版と結果を対応させる。
`tools/report.py`と`tools/docs_site.py`で品質と検索可能な設計サイトを生成する。
出力先とCornellNoteWebv2の参照版は`docs/design/ADR-0002-relational-service.md`で確認する。

## 配布済みdev-standardとの境界

既存の4スキルと`spec/skills/skills.qnt`は導入元の固定契約である。このローカル補足はその契約を書き換えずに併用する。配布物のhash・receipt・commitmentを変更して検査を通すことはしない。ローカルスキルの変更は、このリポジトリのコードとともにGitへ保存する。
