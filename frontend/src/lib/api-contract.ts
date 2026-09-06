import type {
  AppState,
  CookingSession,
  Food,
  MealItem,
  ReceiptCommit,
  Settings,
  ShoppingCheck,
  StockInput,
} from "./types";

/** GET /api/workspace は正規化テーブルを画面用に集約する。JSON全体の更新APIは設けない。 */
export type WorkspaceResponse = AppState;
/** 変更前のworkspace.versionを送り、他タブ・他端末の更新競合を検出する。 */
export interface RevisionRequest {
  expectedVersion: number;
}
/** 各変更APIはトランザクション成功後のworkspace全体を返す。 */
export type WorkspaceMutationResponse = WorkspaceResponse;
export interface CreatePantryLotRequest extends RevisionRequest, StockInput {
  id: string;
}
export interface UpdatePantryLotRequest extends RevisionRequest, StockInput {
  restore?: boolean;
}
export interface CommitReceiptRequest extends RevisionRequest, ReceiptCommit {
  customFoods: Food[];
}
export interface AddMenuItemRequest extends RevisionRequest {
  item: MealItem;
}
export interface PutSettingsRequest extends RevisionRequest {
  settings: Settings;
}
export interface PutShoppingChecksRequest extends RevisionRequest {
  checks: ShoppingCheck[];
}
export interface CreateCookingSessionRequest extends RevisionRequest {
  session: CookingSession;
}
export interface UpdateCookingSessionRequest extends RevisionRequest {
  session: CookingSession;
  deduct?: boolean;
}
/** POST /api/foods/custom は、その利用者が登録した食品を作成する。 */
export interface CreateCustomFoodRequest extends RevisionRequest {
  food: Food;
}
