# RecipeWeaveの設計生成対象

この表は生成器の対象と出典を定める。生成された一覧や仕様の内容を手書きで重複保守しない。

| 出力 | 主な入力 | 保持する内容 |
|---|---|---|
| `database/README.md` | 版管理DDL・移行台帳DDL・説明の補足 | 実装されたテーブル一覧と各表へのリンク |
| `database/tables/<schema>.<table>.md` | SQLGlotのDDL AST | 列、型、NULL、既定値、主キー、一意制約、外部キー、CHECK、索引、出典 |
| `database/ER.md` | DDLの表・外部キー | Mermaidの物理ER図。外部キーがなければ明記 |
| `api/README.md` | 実アプリのOpenAPI・router AST | API操作一覧、メソッド、パス、認証、各仕様へのリンク |
| `api/CRUD.md` | 操作ごとのSQL AST | APIとテーブルのC/R/U/D対応 |
| `api/MODELS.md` | 実アプリのOpenAPI | 要求・応答等で参照する共通スキーマ |
| `api/operations/<id>/interface.md` | OpenAPI・schemaの説明 | path/query/header、要求・応答、型、必須、制約、ステータス |
| 同`sequence.md` | router/functions AST | 実呼出順、分岐、繰返しを保持したMermaid図 |
| 同`queries.md` | APIのSQL・生成クエリの対応 | SQLファイル、パラメータ、処理対象、CRUD |
| 同`detail.md` | router/functionsと操作契約 | 処理の責務、呼出先、エラー、解析境界 |
| 同`tests.md` | 実在するテスト・明示的対応 | 対象試験の対応。試験実行の成功を静的解析から推測しない |
| `REGISTRY.md` / `MANIFEST.md` | 生成器と実入力ファイル | 生成入口・担当範囲・入力の相対パスとSHA-256 |

出力はすべて`docs/design/generated/`からの相対パスである。テーブルの日本語説明は`database/design.manual.json`から補足できるが、列集合・型・制約は実DDLから導出する。補足と実DDLの対応が欠ける場合は、不一致を生成成功で隠さない。

## APIとSQLの一致

`create_app()`から得るOpenAPIをAPI契約の入力とし、`router.py`の実ルートと対応を照合する。操作ごとの`contract.py`はSQLやテストとの明示的な関連付けに使い、対応するファイル・操作の存在を確認する。ルート名やSQL名が似ているという理由だけで対応を推測しない。

SQLのCRUDはSQLGlot ASTから導出する。書込み先と副問い合わせの読取り先を区別し、文字列の正規表現だけで実行SQLを解析しない。SQLFluffは構文と選択した規約の検査、SQLGlotは型付きクエリ・設計導出の検査として役割を分ける。

## シーケンス図の範囲

生成図は各操作のrouterと到達可能なfunctionsからポート呼出しまでを対象にする。分岐や繰返しを保持し、未対応構文はファイル・関数・行・構文種別を示して失敗する。依存性注入、Cognito認証、ポート先のDSQL処理等を解析していなければ、その内部を完全に展開した図とは記載しない。

## 変更時の保守

ソースの追加・変更・削除に応じて、生成器の入力一覧と出力集合も更新する。生成器が所有する範囲だけを置き換え、管理外ファイル、symlink、範囲外パスへ書き込まない。`--check`では候補と既存出力を比較するだけとし、修復や生成ファイル削除を同時に行わない。

生成対象を拡張するときは、正常例に加え、実装変更への追従と未対応構文の検出を対象試験へ追加する。仕様に記載しただけの将来テーブル、API、外部処理を実装済みとして図へ追加しない。
