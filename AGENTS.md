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
