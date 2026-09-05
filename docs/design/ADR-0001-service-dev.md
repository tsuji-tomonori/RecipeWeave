# ADR-0001: RecipeWeave のサービス試用版

状態: 採用。対象: サービス要件 `REQ-SVC-*`。根拠は利用者マニュアル・Q&Aの2回の独立レビューと、QNTから生成した要件定義書。

## サービスと実装の境界

食材を選ぶ、料理を決める、分量を変える、献立・買い物をまとめる、調理する、という利用者の順序に合わせる。レシートは「画像を選ぶ → 読み取る → 確認 → 登録」。確認中に在庫を変えない。

最初の Dev は8品のサンプルを扱う静的Webアプリにする。既存の約1,200万件の出力は構造候補であり、完成レシピとして表示しない。既存の生成器・候補データは保持する。サンプルの人数違いを別レシピとして数えない。

| 境界 | 今回の実装 | 公開前に確認すること |
|---|---|---|
| UI | Svelte 5 / TypeScript、Viteによる静的SPA、hashによる遷移 | モバイル幅、ボタンの名称、戻る・再開 |
| レシート | Tesseract.jsの日本語OCRを端末で実行。worker・WASM・言語データも同じ配信元へ配置 | 実画像からの文字認識、失敗・中止、画像や全文を保存しないこと |
| 数量と在庫 | TypeScriptの独立した関数。明示単位と数量不明を維持 | 人数比、集計、連打、消費後の取消、旧在庫保持 |
| 端末保存 | 版付きのローカル状態。書込成功後に画面へ反映 | 保存拒否・容量超過・別タブ競合・不正バックアップ |
| API | FastAPI、operation単位のsrc構成、OpenAPI | 型、入力、認証、CAS、利用者の分離 |
| AWS | CloudFront / S3 → API Gateway → Lambda → Aurora DSQL、CDK | 合成・パッケージ・権限。実環境への反映は別途結果を記録 |
| Dev配信 | GitHub Actionsで検査・ビルドし、GitHub Pagesへ配置 | Pagesの有効化、deployジョブ、実URL |

Svelte/Viteは今回の静的・操作中心の画面に対する実装判断。CornellNoteWebv2のリポジトリは確認時に空であり、別会話の完全なプロンプトに準拠したとは主張しない。既知のCloudFront/S3、API Gateway、Lambda FastAPI、Aurora DSQL、CDK、マイグレーションの方針に合わせる。

## 保存されるデータ

画面と計算の型の正本は `frontend/src/lib/types.ts`。数量は `{value: number | null, unit}` とし、`null` と0を区別する。レシピの標準分量、利用者が調整した分量、献立に入れた時点の分量を別に持つ。

冷蔵庫は購入・登録ごとの在庫を保持する。同じ食材でも、以前からの在庫と今回のレシートの追加分を併合して由来を失わない。取消はその登録に由来する現在の未消費分だけを対象にする。消費履歴と他の登録分はそのまま残す。取消状態は二重取消を防ぐ業務上の履歴であり、アカウント削除を汎用の削除フラグで代用する仕組みではない。

レシート画像、OCR全文、店舗名、購入日時は端末の永続状態に入れない。保存するのは、確認した食材、量・単位、登録日時、登録の識別子、重複照合に使うハッシュ・署名、取消状態など。バックアップはこの許可された状態だけを検証し、確認後に全置換する。

## 数量と調理

- 人数の変更は直前の確定量に新旧の人数比を掛ける。加熱時間は人数に比例させない。
- 食材・形態・換算可能な単位の組が同じものだけを集計する。パック・点数を根拠なくgにしない。
- 手持ち量が不明、単位が合わない、必要量に足りない場合を分ける。
- 買い物のチェックは購入メモ。チェックだけで在庫を増やさない。
- 調理完了時の在庫更新は初期OFF。確認した使用量に対し、換算可能で足りる在庫だけを減らす。
- 段取りでは料理内の前後関係、人が作業する時間、器具の占有を扱う。待ち時間に別料理を進めることと、1人が同時に二つの手作業をすることを区別する。

## API と認証

| API | 目的 | 認証 |
|---|---|---|
| GET /api/health | 稼働状態 | 公開 |
| GET /api/foods | サンプルの食材カタログ | 公開 |
| GET /api/recipes | サンプル検索 | 公開 |
| GET /api/recipes/{id} | 料理詳細 | 公開 |
| GET /api/state | 自分の版付き状態 | Cognito access JWT |
| PUT /api/state | 期待する版と一致した状態を更新 | Cognito access JWT |

状態の読書きは署名・issuer・有効期限・token_use・client_idを検証し、JWTのsubjectで利用者を決める。任意ヘッダーの利用者IDを信用しない。認証設定がなければ状態APIは閉じる。競合は409を返し、無条件で上書きしない。

DSQLの状態スナップショットは最初の同期境界であり、既存の詳細なレシピ・材料・工程モデルを置き換える最終DB設計ではない。Devの端末保存をクラウド同期済みと表示しない。AWSでの認証・同期を利用者に提供する際は、実環境試験と移行説明を別途完了する。

## DSQLとマイグレーション

DSQLはIAMを用いて接続し、アプリ用のDBロールとマイグレーション用の権限を分離する。SQLは値をバインドし、認証トークンをログに残さない。[AWS認証・認可の説明](https://docs.aws.amazon.com/aurora-dsql/latest/userguide/authentication-authorization.html)

DDLは1文ずつ別トランザクションで扱い、DMLと混在させない。非同期のインデックス作成はジョブの終了を確認する。OCC競合の再試行は上限を設け、同じ業務操作を二重適用しない。[移行ガイド](https://docs.aws.amazon.com/aurora-dsql/latest/userguide/working-with-postgresql-compatibility-migration-guide.html)、[非同期インデックス](https://docs.aws.amazon.com/aurora-dsql/latest/userguide/working-with-create-index-async.html)

2026年8月27日に外部キー対応が追加されているため、古い「DSQLは外部キー非対応」という前提を要件へ固定しない。必要な参照に適用し、競合と追加読込の影響を確認する。[外部キーの説明](https://docs.aws.amazon.com/aurora-dsql/latest/userguide/working-with-foreign-key-constraints.html)

## 検証と配信

実装由来の文書をコード・OpenAPI・SQL・CDK合成結果から生成し、差分を検査する。検査結果と公開状態は `docs/verification/` に記録する。机上レビューは実ユーザーテスト、実機での操作性、OCRの一般精度の証明とは区別する。

Pagesの有効化には、通常のGITHUB_TOKENとは別の管理権限が必要。確認時点でリポジトリは未有効、現GitHub連携にPages設定の操作はない。無効な状態で公開成功を表示しない。[configure-pagesの入力仕様](https://github.com/actions/configure-pages/blob/main/action.yml)

AWS連携も確認時に再認証が必要だった。CDK合成・テストの成功とAWSデプロイの成功は別々に記録する。
