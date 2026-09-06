# 設計書の自動生成と検証

Dev Standardの「要件正本・実装からの設計生成・品質ゲート」に従う。
参照元は `tsuji-tomonori/dev-standard` の `1b92caa53ecf42a431774e73c53838494d58c516`。
要件は `spec/requirements/requirements.qnt`、実際のAPIはFastAPI、物理DBは移行DDLを正とする。

## 生成対象

| 入力 | 自動生成する仕様 |
|---|---|
| 移行SQLと移行台帳のCREATE TABLE | テーブル一覧・各表の列型、NULL、既定値、制約・ER図 |
| `database/design.manual.json` | 表・列の日本語の意味。型や制約はここから生成しない |
| 実FastAPI OpenAPIと各操作の`contract.py` | API一覧・入出力・認証・応答・共有モデル・enum・制約 |
| 各APIの`sql/*.sql` | SQL本文・バインド変数・対象表と列・CRUDマトリクス |
| 各操作の`router.py`と`functions.py` | 関数ごとのシーケンス・責務・対応する実装 |
| 依存解決・例外handler・middleware | 詳細設計・共通エラー仕様 |
| 対象メソッドとURLを明示するテスト | API別の検証仕様と表明一覧 |
| サンプルJSON・フロント・CDK合成結果 | サービス一覧・CDK資源一覧 |
| 入力ファイル・出力内容 | 生成物一覧・SHA-256マニフェスト |

出力は [生成設計書の入口](generated/README.md)。`api/`・`database/`は生成専用。
`generator.md`はレシピ生成器側の独立した生成コマンドが管理する。

## 更新手順

リポジトリのルートで実行する。依存は`uv.lock`と各`package-lock.json`に固定する。

```sh
uv sync --locked --all-packages
uv run --locked --package recipeweave-api app-sql-lint
uv run --locked --package recipeweave-api app-docs
uv run --locked --package recipeweave-api python backend/tools/package_lambda.py --architecture x86_64
npm run synth --prefix infra
uv run --locked python -m recipeweave_generator.design
uv run --locked python tools/generate_service_design.py
uv run --locked python tools/generate_service_design.py --check
uv run --locked pytest tests/test_service_design.py -q
```

`--check`は書き込まない。生成コマンドは入力を全件検査してから管理対象を更新する。
APIの削除で不要となった設計書は削除し、生成先のシンボリックリンクや管理対象外のファイルは拒否する。
CIでは再生成後に`tools/check_generated_service.py`でGit差分も確認する。
生成物の変更はソース変更と一緒にレビュー・コミットする。図だけを手で修正してはならない。

## SQLと解析範囲

APIのDBアクセスは`sql/*.sql`、型付き生成wrapper、psycopgプロバイダーを経由する。
現実装はORMを使用していない。JSONカタログ参照・稼働確認APIに実行しないSQLを置かない。
SQLFluffはPostgreSQL方言、psycopgの名前付きプレースホルダーを検査用の値で解析する。
SQLGlotは構造・対象表・明示列を検査する。利用者の実データや接続情報は静的解析に渡さない。

物理表は現在2表。`user_state.payload`内部の配列や、将来のレシピDBの計画を物理表として扱わない。
外部キーがなければER図に線を追加しない。DDL解析は明示列を持つCREATE TABLEを対象とし、
ALTER・DROP・独立インデックス等が追加された時点で生成を停止する。対応投影と回帰試験を追加してから進める。
既定値・列制約・表制約はSQL ASTから投影する。

シーケンスは関数単位。if・for・while・return・raise・continue・breakを保持し、
短絡評価・内包表記は条件付き式として残す。依存解決やプロバイダー内部を推測で展開しない。
try/with/matchや動的な呼出先等は未対応として失敗する。対応する実装も併記する。
テストの静的抽出は成功実績や全要件の受入完了を意味しない。CIの実行結果と併せて判断する。

## 日本語とスキル

手書きのコメント・docstring・設計上の説明は日本語にする。識別子、プロトコル値、外部仕様の引用は保持する。
適用済み移行001と検証SQLはチェックサム保護のためバイト列を保持する。説明は`database/README.md`へ補記する。
固定配布スキルとreceiptは変更せず、追加契約はリポジトリ内の`recipeweave-design-contract`スキルへ記載する。

## devブランチと公開

変更はfeatureからdevへのPRでレビューする。devのCIでも同じ生成・検証を実行する。
GitHub Pagesへの公開は既存の`github-pages`環境の保護ルールに従う。
ブランチが許可されていない場合は設定所有者の対応が必要で、別環境への付け替えや検査の無効化は行わない。
