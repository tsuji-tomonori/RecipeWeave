<!-- dev-standard:begin -->
# dev-standard lightweight guardrails

portableなblocking guardrailは次の3本だけです。

1. durableな要件を`spec/requirements/requirements.qnt`へ原子的に保つ。
2. 現在状態の設計を実装artifactから決定的に生成する。
3. 変更と受入条件に関係する検査だけを実行する。

通常の入口は`$chat-first-development`です。Quint正本からJSONを生成し、そのJSONから人向けMarkdownを生成します。生成viewは直接編集しません。

dev-standardは、このrepositoryのbranch、merge方式、CI/CD workflow、required check、PR template、commit形式を追加も変更もしません。既存のrepository指示と権限境界を優先してください。
<!-- dev-standard:end -->

## RecipeWeaveの開発規約

Python依存はuv、monorepoのタスクはmoonを使用します。
コミットは `feat: 食品同一性に基づく列挙を追加` のように、Conventional Commitsのtypeと日本語の説明で記録します。
組み合わせ元・アルゴリズム・全量出力の定義digestを対応させ、評価結果を見て同じholdoutを再利用した最適化は行いません。

API・DB・設計生成器・SQLを変更するときは、`$recipeweave-design-contract`のプロジェクト固有契約を参照します。既存のdev-standardの3本柱に従い、要件正本、実装、生成設計と必要な検査を同じ変更に対応させます。

手書きコードのコメント・docstring・SQLの説明と、人向けに生成する設計説明は原則日本語で書きます。識別子、外部APIの互換フィールド、機械用ディレクティブ、外部仕様名は必要な原表記を保ちます。既存の適用済み移行`database/migrations/001_user_state.sql`はchecksum保持のため説明の翻訳だけでは変更しません。導入元がdigestで管理するdev-standardの配布物も維持し、このプロジェクト固有の補足は上記ローカルスキルへ記載します。

正規化DBとCornellNoteWebv2の適用範囲はADR-0002を参照します。元の全テーブルと実DDLの対応、型付きAPI、実DB試験、PC・モバイルの操作画像を同じ変更に対応させます。Pagesの設計図やCI成功をAWS実配備の成功とは扱いません。APIが未接続のときに試用JSONを返して正常に見せる実装は追加しません。
