# サービス実装由来の設計

生成元: OpenAPI・TypeScript/Python実装・SQL・サンプルJSON・CDK合成結果。手編集禁止。
`uv run python tools/generate_service_design.py` で生成、`--check` で差分検査。
コードと配備定義の存在を示す。実配備・実機評価・OCR精度の実測を証明するものではない。

## サンプルデータ

食材 35 件、料理 8 件。完成レシピの本番カタログとは別のDev用標本。

| ファイル | SHA-256 |
|---|---|
| `data/samples/foods.json` | `69f10ea50bc80682b9bbfd5613fc749584bc78c3dd50a58bc2ddfe6f429f940c` |
| `data/samples/recipes.json` | `cd12f4aa81a30967fd9485b1d0218727ec87f89a2a6151b0bda06ed1a34412c7` |

## API

| Method | Path | operationId | 認証定義 | 応答 |
|---|---|---|---|---|
| GET | `/api/foods` | `list_foods` | 公開 | 200, 422 |
| GET | `/api/health` | `get_health` | 公開 | 200 |
| GET | `/api/recipes` | `list_recipes` | 公開 | 200, 422 |
| GET | `/api/recipes/{recipe_id}` | `get_recipe` | 公開 | 200, 404, 422 |
| GET | `/api/state` | `get_state` | HTTPBearer | 200, 401, 503 |
| PUT | `/api/state` | `put_state` | HTTPBearer | 200, 401, 409, 413, 422, 503 |

## 実装の公開要素

| ファイル | 公開要素 | SHA-256 |
|---|---|---|
| `frontend/src/App.test.ts` | 検証コード | `6d302cca375e46480d158b07da040287d5d780eaee4c3cb2f6ecf7aa48f0efb1` |
| `frontend/src/lib/domain.test.ts` | 検証コード | `f9ec084aa0c4307ae29cf631a553f6b907dbc006fa9f968d23233d2a83c35856` |
| `frontend/src/lib/domain.ts` | `FOODS`, `RECIPES`, `DomainError`, `newId`, `validateQuantity`, `createInitialState`, `allFoods`, `getFood`, `getRecipe`, `quantityText`, `getDraft`, `scaleDraft`, `setDraftAmount`, `saveDraft`, `resetDraft`, `addToMeal`, `updateMeal`, `removeFromMeal`, `toggleSaved`, `addCustomFood`, `addStock`, `updateStock`, `deleteStock`, `restoreStock`, `duplicateImports`, `commitReceipt`, `previewUndoImport`, `undoImport`, `requiredQuantities`, `shoppingList`, `toggleShoppingCheck`, `searchRecipes`, `randomRecipe`, `arrangements`, `buildCookingPlan`, `startCooking`, `moveCooking`, `pauseCooking`, `resumeCooking`, `startTimer`, `timerRemaining`, `previewConsumption`, `completeCooking` | `8de6512faecba50b224b6c71cc811da00cd4821bc9920ce526bae2a1be1dac82` |
| `frontend/src/lib/ocr.ts` | `OcrTask`, `validateReceiptImage`, `recognizeReceipt` | `61590b3c31d6fe513092640a1e3d6f37a3cc8f229bc80003a11098f36964d4ec` |
| `frontend/src/lib/persistence.ts` | `STORAGE_KEY`, `StorageLike`, `LockManagerLike`, `RecoverySnapshot`, `validateAppState`, `parseBackup`, `loadState`, `inspectRecovery`, `transact`, `exportBackup`, `restoreBackup`, `recoverBackup` | `7bfb0243d4103d66a890f80a5cfd651c2f4035549142912a8dac1ff8403449de` |
| `frontend/src/lib/receipt.ts` | `parseReceipt`, `receiptSignature`, `validateReceiptFile`, `hashImage` | `4575e6a5096fceb8770bf9824e576265bd9bb5cfd4441ee48cde5088a5c23619` |
| `frontend/src/lib/types.ts` | `UNITS`, `Unit`, `StorageLocation`, `Quantity`, `Food`, `RecipeIngredient`, `RecipeStep`, `Recipe`, `RecipeDraft`, `MealItem`, `StockLot`, `ReceiptImport`, `ReceiptCandidate`, `ReceiptCommit`, `ShoppingCheck`, `ShoppingRow`, `ShoppingList`, `PlannedStep`, `CookingTimer`, `ConsumptionRequest`, `ConsumptionResult`, `CookingSession`, `Settings`, `SearchFilters`, `AppState`, `StockInput`, `UndoPreview` | `4d2c48088aa014be86b9c12bde285dc9b7b25b6e561b088f18c5358c2d6da3f7` |
| `frontend/src/main.ts` | 画面コンポーネント／起動処理 | `ec315a1d373f5470b11a7dcaa0d972ab81e3f513113325bd18aea471c1ce2d62` |
| `frontend/src/App.svelte` | 画面コンポーネント／起動処理 | `d66ba8ea29346964253a1b060d67636a5185b748ee13f1b739c840ce3a91889a` |
| `frontend/src/lib/FoodTile.svelte` | 画面コンポーネント／起動処理 | `8be1fc4f7ab1b54c026a7ff77fa74f67e479f8b09a7cf25c944807da71024333` |
| `frontend/src/lib/RecipeCard.svelte` | 画面コンポーネント／起動処理 | `0921fc76b0d516fdf56d67ac4299d01a2a6245a60bf8f7289aafd25da11cb6e6` |

## SQL境界

| SQL | SHA-256 |
|---|---|
| `backend/src/app/apis/state/get_state/sql/001_select_state.sql` | `6140d5bf18b78dac277dbe8c58325ed4a06c84535ca387612ba1923928dee8ee` |
| `backend/src/app/apis/state/put_state/sql/001_insert_state.sql` | `d64b097cd651c2c0cba2a8fc15e72a3cb1034899243b9534b40ace8bd924258e` |
| `backend/src/app/apis/state/put_state/sql/002_update_state.sql` | `39f304389ac61b149bcbf5b89616dd330f1866ee7a390e53e1c634667569d253` |
| `database/migrations/001_user_state.sql` | `4f085833e9d63238900f9b3a7be1356fe5bb05e56bc93b276ffa32a139cc20f4` |

## CDK合成資源

以下は合成テンプレートの資源定義。アカウントへの作成結果ではない。

### Data

| 資源種別 | 数 |
|---|---|
| `AWS::CDK::Metadata` | 1 |
| `AWS::Cognito::UserPool` | 1 |
| `AWS::Cognito::UserPoolClient` | 1 |
| `AWS::DSQL::Cluster` | 1 |

| Logical ID | 資源種別 |
|---|---|
| `CDKMetadata` | `AWS::CDK::Metadata` |
| `InventoryCluster` | `AWS::DSQL::Cluster` |
| `Users0A0EEA89` | `AWS::Cognito::UserPool` |
| `UsersWebClient8EE36D42` | `AWS::Cognito::UserPoolClient` |

### Service

| 資源種別 | 数 |
|---|---|
| `AWS::ApiGatewayV2::Api` | 1 |
| `AWS::ApiGatewayV2::Authorizer` | 1 |
| `AWS::ApiGatewayV2::Integration` | 1 |
| `AWS::ApiGatewayV2::Route` | 6 |
| `AWS::ApiGatewayV2::Stage` | 1 |
| `AWS::CDK::Metadata` | 1 |
| `AWS::CloudFront::CachePolicy` | 2 |
| `AWS::CloudFront::Distribution` | 1 |
| `AWS::CloudFront::OriginAccessControl` | 1 |
| `AWS::IAM::Policy` | 3 |
| `AWS::IAM::Role` | 3 |
| `AWS::Lambda::Function` | 2 |
| `AWS::Lambda::LayerVersion` | 1 |
| `AWS::Lambda::Permission` | 6 |
| `AWS::Logs::LogGroup` | 3 |
| `AWS::S3::Bucket` | 1 |
| `AWS::S3::BucketPolicy` | 1 |
| `Custom::CDKBucketDeployment` | 1 |

| Logical ID | 資源種別 |
|---|---|
| `ApiF70053CD` | `AWS::Lambda::Function` |
| `ApiLogs3D05D88B` | `AWS::Logs::LogGroup` |
| `ApiServiceRole1BD550DA` | `AWS::IAM::Role` |
| `ApiServiceRoleDefaultPolicyB24862FE` | `AWS::IAM::Policy` |
| `ApiStage` | `AWS::ApiGatewayV2::Stage` |
| `CDKMetadata` | `AWS::CDK::Metadata` |
| `CatalogCache9E6D21C9` | `AWS::CloudFront::CachePolicy` |
| `CustomCDKBucketDeployment8693BB64968944B69AAFB0CC9EB8756C81C01536` | `AWS::Lambda::Function` |
| `CustomCDKBucketDeployment8693BB64968944B69AAFB0CC9EB8756CServiceRole89A01265` | `AWS::IAM::Role` |
| `CustomCDKBucketDeployment8693BB64968944B69AAFB0CC9EB8756CServiceRoleDefaultPolicy88902FDF` | `AWS::IAM::Policy` |
| `DeployWebAwsCliLayer4A26D5E7` | `AWS::Lambda::LayerVersion` |
| `DeployWebCustomResource253E03A7` | `Custom::CDKBucketDeployment` |
| `DsqlMigrationRole65704575` | `AWS::IAM::Role` |
| `DsqlMigrationRoleDefaultPolicy52E39712` | `AWS::IAM::Policy` |
| `HttpAccessLogs7ADEF396` | `AWS::Logs::LogGroup` |
| `HttpApiCognitoAccessTokenBE9C5DCE` | `AWS::ApiGatewayV2::Authorizer` |
| `HttpApiF5A9A8A7` | `AWS::ApiGatewayV2::Api` |
| `HttpApiGETapifoods0C6499D1` | `AWS::ApiGatewayV2::Route` |
| `HttpApiGETapifoodsFastApiPermission567B5FD7` | `AWS::Lambda::Permission` |
| `HttpApiGETapihealth7FA5887F` | `AWS::ApiGatewayV2::Route` |
| `HttpApiGETapihealthFastApi9BC91470` | `AWS::ApiGatewayV2::Integration` |
| `HttpApiGETapihealthFastApiPermission8540C7D2` | `AWS::Lambda::Permission` |
| `HttpApiGETapirecipesE2E6BAF0` | `AWS::ApiGatewayV2::Route` |
| `HttpApiGETapirecipesFastApiPermission7B41916C` | `AWS::Lambda::Permission` |
| `HttpApiGETapirecipesid684DE094` | `AWS::ApiGatewayV2::Route` |
| `HttpApiGETapirecipesidFastApiPermissionAD10D674` | `AWS::Lambda::Permission` |
| `HttpApiGETapistate742B9D5D` | `AWS::ApiGatewayV2::Route` |
| `HttpApiGETapistateFastApiPermission344DAADB` | `AWS::Lambda::Permission` |
| `HttpApiPUTapistateAF5B9132` | `AWS::ApiGatewayV2::Route` |
| `HttpApiPUTapistateFastApiPermission4E66FB85` | `AWS::Lambda::Permission` |
| `StaticCache185A1D0E` | `AWS::CloudFront::CachePolicy` |
| `Web3C8945DB` | `AWS::CloudFront::Distribution` |
| `WebAssets27872646` | `AWS::S3::Bucket` |
| `WebAssetsPolicy59254521` | `AWS::S3::BucketPolicy` |
| `WebDeploymentLogs48919846` | `AWS::Logs::LogGroup` |
| `WebOrigin1S3OriginAccessControl98EE5C09` | `AWS::CloudFront::OriginAccessControl` |

## 再現と受入の境界

- 画面の型検査・状態計算テストと、APIの型検査・認証/競合テストを別々に実行する。
- OpenAPIとSQL wrapperは `app-docs --check`、本書は `--check` で追従を確認する。
- CDK構造検査と合成は配備前の検証。DSQL実接続・Cognito実ログインは別の受入を要する。
- 設計判断は [ADR-0001](../ADR-0001-service-dev.md) を参照する。
