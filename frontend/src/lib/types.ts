/** Persistent model. Receipt images, raw OCR and purchase dates are intentionally absent. */
export const UNITS = ['g', 'ml', '個', 'パック', '袋', '缶', '本', '枚', '点'] as const;
export type Unit = (typeof UNITS)[number];
export type StorageLocation = '冷蔵' | '冷凍' | '常温';
export interface Quantity { value: number | null; unit: Unit }
export interface Food {
  id: string; name: string; aliases: string[]; category: string;
  defaultUnit: Unit; location: StorageLocation; pantry: boolean;
  imageIndex: number | null; componentsKnown: boolean; componentFoodIds: string[];
}
export interface RecipeIngredient { foodId: string; quantity: Quantity; form: string; note: string }
export interface RecipeStep {
  id: string; title: string; instruction: string; minutes: number;
  mode: 'active' | 'passive'; equipment: string[]; guide: string | null;
}
export interface Recipe {
  id: string; name: string; description: string; servings: number; minutes: number;
  equipment: string[]; ingredients: RecipeIngredient[]; steps: RecipeStep[];
  arrangementIds: string[]; tags: string[]; sample: true;
}
export interface RecipeDraft { recipeId: string; servings: number; amounts: Record<string, Quantity>; adjusted: boolean }
export interface MealItem extends RecipeDraft { id: string }
export interface StockLot {
  id: string; foodId: string; originalFoodId: string; quantity: Quantity; originalQuantity: Quantity;
  form: string; location: StorageLocation; priority: boolean; expiresOn: string | null;
  createdAt: string; updatedAt: string; sourceImportId: string | null;
  status: 'active' | 'deleted' | 'undone'; consumed: Quantity[]; edited: boolean;
}
export interface ReceiptImport {
  id: string; imageHash: string; purchaseSignature: string; createdAt: string;
  state: 'registered' | 'undone'; createdLotIds: string[]; undoneAt: string | null;
}
/** Temporary only: never serialize candidates into AppState. */
export interface ReceiptCandidate {
  id: string; rawText: string; foodId: string | null; quantity: Quantity;
  selected: boolean; status: 'matched' | 'review' | 'excluded'; reason: string;
}
export interface ReceiptCommit {
  id: string; imageHash: string; purchaseSignature: string;
  candidates: ReceiptCandidate[]; allowDuplicate: boolean;
}
export interface ShoppingCheck { key: string; signature: string; foodId: string; quantity: Quantity; checkedAt: string; archived: boolean }
export interface ShoppingRow {
  key: string; foodId: string; form: string; required: Quantity; available: Quantity;
  toBuy: Quantity; status: 'enough' | 'buy' | 'unknown' | 'incompatible';
  reason: string; checked: boolean;
}
export interface ShoppingList { rows: ShoppingRow[]; previous: ShoppingCheck[] }
export interface PlannedStep extends RecipeStep {
  key: string; mealItemId: string; recipeId: string; recipeName: string;
  startMinute: number; endMinute: number;
}
export interface CookingTimer { stepKey: string; startedAt: number; durationSeconds: number }
export interface ConsumptionRequest { foodId: string; quantity: Quantity; form: string }
export interface ConsumptionResult extends ConsumptionRequest {
  applied: boolean; reason: string; lotIds: string[];
}
export interface CookingSession {
  id: string; mealSnapshot: MealItem[]; plan: PlannedStep[]; index: number;
  completedStepIds: string[]; timers: CookingTimer[];
  status: 'active' | 'paused' | 'completed'; consumptionResults: ConsumptionResult[];
}
export interface Settings { excludedFoodIds: string[]; pantryFoodIds: string[]; equipment: string[] }
export interface SearchFilters {
  selectedFoodIds: string[]; match: 'all' | 'any'; maxMinutes: number | null;
  noShopping: boolean; equipment: string[];
}
export interface AppState {
  schemaVersion: 1; version: number; lots: StockLot[]; imports: ReceiptImport[];
  drafts: Record<string, RecipeDraft>; meal: MealItem[]; saved: string[];
  shoppingChecks: ShoppingCheck[]; cooking: CookingSession | null;
  settings: Settings; customFoods: Food[]; search: SearchFilters;
}
export interface StockInput {
  foodId: string; quantity: Quantity; form?: string; location?: StorageLocation;
  priority?: boolean; expiresOn?: string | null;
}
export interface UndoPreview { importId: string; lots: StockLot[]; needsConfirmation: boolean; alreadyUndone: boolean }
