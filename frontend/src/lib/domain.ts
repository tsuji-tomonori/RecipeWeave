import { UNITS } from "./types";
import type {
  AppState,
  ConsumptionRequest,
  ConsumptionResult,
  Food,
  MealItem,
  PlannedStep,
  Quantity,
  ReceiptCommit,
  Recipe,
  RecipeDraft,
  RecipeIngredient,
  SearchFilters,
  ShoppingList,
  ShoppingRow,
  StockInput,
  StockLot,
  UndoPreview,
  CookingTimer,
} from "./types";

/** APIから読み込んだ閲覧用キャッシュ。永続データの正本はデータベース。 */
export const FOODS: Food[] = [];
export const RECIPES: Recipe[] = [];
export function setCatalog(foods: Food[], recipes: Recipe[]): void {
  FOODS.splice(0, FOODS.length, ...structuredClone(foods));
  RECIPES.splice(0, RECIPES.length, ...structuredClone(recipes));
}
export function cacheRecipes(recipes: Recipe[], makeCurrent = true): void {
  for (const recipe of recipes) {
    const index = RECIPES.findIndex(
      (existing) =>
        existing.id === recipe.id && existing.versionId === recipe.versionId,
    );
    if (index >= 0 && !makeCurrent) {
      RECIPES.splice(index, 1, structuredClone(recipe));
      continue;
    }
    if (index >= 0) RECIPES.splice(index, 1);
    if (makeCurrent) RECIPES.unshift(structuredClone(recipe));
    else RECIPES.push(structuredClone(recipe));
  }
}
export class DomainError extends Error {
  constructor(
    public readonly code: string,
    message: string,
  ) {
    super(message);
    this.name = "DomainError";
  }
}
export function newId(): string {
  return crypto.randomUUID();
}
const timestamp = (): string => new Date().toISOString();
const copy = <T>(value: T): T => structuredClone(value);
const round = (value: number): number => Math.round(value * 1e6) / 1e6;
export function validateQuantity(q: Quantity): void {
  if (
    !UNITS.includes(q.unit) ||
    (q.value !== null && (!Number.isFinite(q.value) || q.value < 0))
  )
    throw new DomainError(
      "INVALID_QUANTITY",
      "数量は0以上の数、または数量不明にしてください。",
    );
}
export function createInitialState(): AppState {
  return {
    schemaVersion: 1,
    version: 0,
    lots: [],
    imports: [],
    drafts: {},
    meal: [],
    saved: [],
    shoppingChecks: [],
    cooking: null,
    settings: {
      excludedFoodIds: [],
      pantryFoodIds: [],
      equipment: ["フライパン", "鍋", "電子レンジ", "ケトル", "包丁"],
    },
    customFoods: [],
    search: {
      selectedFoodIds: [],
      match: "all",
      maxMinutes: null,
      noShopping: false,
      equipment: [],
    },
  };
}
export const allFoods = (state: AppState): Food[] => [
  ...new Map(
    [...FOODS, ...state.customFoods].map((food) => [food.id, food]),
  ).values(),
];
export function getFood(state: AppState, id: string): Food {
  const food = allFoods(state).find((x) => x.id === id);
  if (!food) throw new DomainError("FOOD_NOT_FOUND", "食材が見つかりません。");
  return food;
}
export function getRecipe(id: string, versionId?: string): Recipe {
  const recipe = RECIPES.find(
    (x) => x.id === id && (!versionId || x.versionId === versionId),
  );
  if (!recipe)
    throw new DomainError("RECIPE_NOT_FOUND", "この料理は公開されていません。");
  return recipe;
}
export function quantityText(q: Quantity): string {
  return q.value === null
    ? "数量不明"
    : `${q.value}${q.unit}${["パック", "袋", "缶", "点"].includes(q.unit) ? "（内容量は確認）" : ""}`;
}
/** 材料行を識別する。同じ食品の下味・仕上げを別々に調整できる。 */
export const ingredientKey = (ingredient: RecipeIngredient): string =>
  ingredient.ingredientId ?? ingredient.foodId;
export function getDraft(
  state: AppState,
  recipeId: string,
  versionId?: string,
): RecipeDraft {
  if (
    state.drafts[recipeId] &&
    (!versionId || state.drafts[recipeId].recipeVersionId === versionId)
  )
    return copy(state.drafts[recipeId]);
  const recipe = getRecipe(recipeId, versionId);
  return {
    recipeId,
    ...(recipe.versionId ? { recipeVersionId: recipe.versionId } : {}),
    servings: recipe.servings,
    amounts: Object.fromEntries(
      recipe.ingredients.map((x) => [ingredientKey(x), copy(x.quantity)]),
    ),
    adjusted: false,
  };
}
function validateDraft(draft: RecipeDraft): void {
  if (!Number.isFinite(draft.servings) || draft.servings <= 0)
    throw new DomainError(
      "INVALID_SERVINGS",
      "人数は0より大きい数にしてください。",
    );
  const recipe = getRecipe(draft.recipeId, draft.recipeVersionId);
  const expected = recipe.ingredients.map(ingredientKey).sort();
  if (
    JSON.stringify(Object.keys(draft.amounts).sort()) !==
    JSON.stringify(expected)
  )
    throw new DomainError("INVALID_DRAFT", "材料の構成が一致しません。");
  for (const ingredient of recipe.ingredients) {
    const q = draft.amounts[ingredientKey(ingredient)];
    validateQuantity(q);
    if (q.value === null || q.unit !== ingredient.quantity.unit)
      throw new DomainError(
        "INVALID_DRAFT",
        "料理の量と単位を確認してください。",
      );
  }
}
export function scaleDraft(
  draft: RecipeDraft,
  newServings: number,
): RecipeDraft {
  validateDraft(draft);
  if (!Number.isFinite(newServings) || newServings <= 0)
    throw new DomainError(
      "INVALID_SERVINGS",
      "人数は0より大きい数にしてください。",
    );
  const next = copy(draft);
  for (const q of Object.values(next.amounts))
    if (q.value !== null) {
      q.value = round((q.value * newServings) / draft.servings);
      validateQuantity(q);
    }
  next.servings = newServings;
  return next;
}
export function setDraftAmount(
  draft: RecipeDraft,
  foodId: string,
  quantity: Quantity,
): RecipeDraft {
  const next = copy(draft);
  next.amounts[foodId] = copy(quantity);
  next.adjusted = true;
  validateDraft(next);
  return next;
}
export function saveDraft(state: AppState, draft: RecipeDraft): AppState {
  validateDraft(draft);
  return {
    ...state,
    drafts: { ...state.drafts, [draft.recipeId]: copy(draft) },
  };
}
export function resetDraft(state: AppState, recipeId: string): AppState {
  getRecipe(recipeId);
  const next = copy(state);
  delete next.drafts[recipeId];
  return next;
}
export function addToMeal(
  state: AppState,
  draft: RecipeDraft,
  id = newId(),
): AppState {
  validateDraft(draft);
  if (state.meal.some((x) => x.id === id)) return state;
  return reconcileShopping(state, {
    ...state,
    meal: [...state.meal, { ...copy(draft), id }],
  });
}
export function updateMeal(
  state: AppState,
  itemId: string,
  draft: RecipeDraft,
): AppState {
  validateDraft(draft);
  if (!state.meal.some((x) => x.id === itemId))
    throw new DomainError("MEAL_NOT_FOUND", "献立の料理が見つかりません。");
  return reconcileShopping(state, {
    ...state,
    meal: state.meal.map((x) =>
      x.id === itemId ? { ...copy(draft), id: itemId } : x,
    ),
  });
}
export const removeFromMeal = (state: AppState, itemId: string): AppState =>
  reconcileShopping(state, {
    ...state,
    meal: state.meal.filter((x) => x.id !== itemId),
  });
export function toggleSaved(state: AppState, id: string): AppState {
  getRecipe(id);
  return {
    ...state,
    saved: state.saved.includes(id)
      ? state.saved.filter((x) => x !== id)
      : [...state.saved, id],
  };
}
export function addCustomFood(
  state: AppState,
  name: string,
  id = newId(),
): AppState {
  const normalized = name.normalize("NFKC").trim();
  if (!normalized || normalized.length > 80)
    throw new DomainError(
      "INVALID_FOOD",
      "食材名は1〜80文字で入力してください。",
    );
  if (allFoods(state).some((f) => f.id === id || f.name === normalized))
    throw new DomainError("DUPLICATE_FOOD", "同じ食材が登録済みです。");
  const food: Food = {
    id,
    name: normalized,
    aliases: [],
    category: "追加した食材",
    defaultUnit: "g",
    location: "冷蔵",
    pantry: false,
    imageIndex: null,
    componentsKnown: false,
    componentFoodIds: [],
  };
  return { ...state, customFoods: [...state.customFoods, food] };
}
export function addStock(
  state: AppState,
  input: StockInput,
  id = newId(),
): AppState {
  const food = getFood(state, input.foodId);
  validateQuantity(input.quantity);
  if (state.lots.some((x) => x.id === id))
    throw new DomainError("DUPLICATE_LOT", "この登録は追加済みです。");
  const now = timestamp();
  const lot: StockLot = {
    id,
    foodId: food.id,
    originalFoodId: food.id,
    quantity: copy(input.quantity),
    originalQuantity: copy(input.quantity),
    form: input.form ?? "標準",
    location: input.location ?? food.location,
    priority: input.priority ?? false,
    expiresOn: input.expiresOn ?? null,
    createdAt: now,
    updatedAt: now,
    sourceImportId: null,
    status: "active",
    consumed: [],
    edited: false,
  };
  return { ...state, lots: [...state.lots, lot] };
}
export function updateStock(
  state: AppState,
  lotId: string,
  input: StockInput,
): AppState {
  getFood(state, input.foodId);
  validateQuantity(input.quantity);
  if (!state.lots.some((x) => x.id === lotId && x.status === "active"))
    throw new DomainError("LOT_NOT_FOUND", "この在庫は編集できません。");
  return {
    ...state,
    lots: state.lots.map((x) =>
      x.id === lotId
        ? {
            ...x,
            foodId: input.foodId,
            quantity: copy(input.quantity),
            form: input.form ?? x.form,
            location: input.location ?? x.location,
            priority: input.priority ?? x.priority,
            expiresOn:
              input.expiresOn === undefined ? x.expiresOn : input.expiresOn,
            updatedAt: timestamp(),
            edited: true,
          }
        : x,
    ),
  };
}
export function deleteStock(state: AppState, lotId: string): AppState {
  if (!state.lots.some((x) => x.id === lotId && x.status === "active"))
    throw new DomainError("LOT_NOT_FOUND", "この在庫は削除済みです。");
  return {
    ...state,
    lots: state.lots.map((x) =>
      x.id === lotId ? { ...x, status: "deleted", updatedAt: timestamp() } : x,
    ),
  };
}
export function restoreStock(state: AppState, lotId: string): AppState {
  const lot = state.lots.find((x) => x.id === lotId);
  if (
    !lot ||
    lot.status !== "deleted" ||
    state.imports.some(
      (x) => x.id === lot.sourceImportId && x.state === "undone",
    )
  )
    throw new DomainError("RESTORE_NOT_ALLOWED", "この削除は取り消せません。");
  return {
    ...state,
    lots: state.lots.map((x) =>
      x.id === lotId ? { ...x, status: "active", updatedAt: timestamp() } : x,
    ),
  };
}
export function duplicateImports(
  state: AppState,
  hash: string,
  signature: string,
) {
  return state.imports.filter(
    (x) =>
      (hash !== "" && x.imageHash === hash) ||
      (signature !== "" && x.purchaseSignature === signature),
  );
}
export function commitReceipt(state: AppState, input: ReceiptCommit): AppState {
  if (state.imports.some((x) => x.id === input.id)) return state;
  const selected = input.candidates.filter((x) => x.selected);
  if (!selected.length)
    throw new DomainError("EMPTY_RECEIPT", "登録する食品を選んでください。");
  for (const candidate of selected) {
    if (!candidate.foodId)
      throw new DomainError(
        "UNRESOLVED_FOOD",
        "選択した行の食材名を確認してください。",
      );
    getFood(state, candidate.foodId);
    validateQuantity(candidate.quantity);
  }
  if (
    !input.allowDuplicate &&
    duplicateImports(state, input.imageHash, input.purchaseSignature).length
  )
    throw new DomainError(
      "DUPLICATE_RECEIPT",
      "登録済みの可能性があります。履歴を確認してください。",
    );
  const next = copy(state);
  const now = timestamp();
  const createdLotIds: string[] = [];
  for (const candidate of selected) {
    const food = getFood(state, candidate.foodId!);
    const id = newId();
    createdLotIds.push(id);
    next.lots.push({
      id,
      foodId: food.id,
      originalFoodId: food.id,
      quantity: copy(candidate.quantity),
      originalQuantity: copy(candidate.quantity),
      form: "標準",
      location: food.location,
      priority: false,
      expiresOn: null,
      createdAt: now,
      updatedAt: now,
      sourceImportId: input.id,
      status: "active",
      consumed: [],
      edited: false,
    });
  }
  next.imports.push({
    id: input.id,
    imageHash: input.imageHash,
    purchaseSignature: input.purchaseSignature,
    createdAt: now,
    state: "registered",
    createdLotIds,
    undoneAt: null,
  });
  return next;
}
export function previewUndoImport(state: AppState, id: string): UndoPreview {
  const entry = state.imports.find((x) => x.id === id);
  if (!entry)
    throw new DomainError("IMPORT_NOT_FOUND", "登録履歴が見つかりません。");
  const lots = state.lots.filter((x) => entry.createdLotIds.includes(x.id));
  return {
    importId: id,
    lots: copy(lots),
    needsConfirmation: lots.some(
      (x) => x.edited || x.consumed.length > 0 || x.status !== "active",
    ),
    alreadyUndone: entry.state === "undone",
  };
}
export function undoImport(state: AppState, id: string): AppState {
  const preview = previewUndoImport(state, id);
  if (preview.alreadyUndone)
    throw new DomainError("ALREADY_UNDONE", "この登録は取消済みです。");
  const ids = new Set(
    preview.lots
      .filter(
        (lot) =>
          lot.status === "active" && !lot.edited && lot.consumed.length === 0,
      )
      .map((lot) => lot.id),
  );
  const now = timestamp();
  return {
    ...state,
    lots: state.lots.map((x) =>
      ids.has(x.id) ? { ...x, status: "undone", updatedAt: now } : x,
    ),
    imports: state.imports.map((x) =>
      x.id === id ? { ...x, state: "undone", undoneAt: now } : x,
    ),
  };
}
const quantityKey = (foodId: string, form: string, unit: string): string =>
  `${foodId}|${form}|${unit}`;
export function requiredQuantities(items: RecipeDraft[]): ConsumptionRequest[] {
  const totals = new Map<string, ConsumptionRequest>();
  for (const item of items) {
    validateDraft(item);
    for (const ingredient of getRecipe(item.recipeId, item.recipeVersionId)
      .ingredients) {
      const quantity = item.amounts[ingredientKey(ingredient)];
      if (quantity.value === 0) continue;
      const key = quantityKey(
        ingredient.foodId,
        ingredient.form,
        quantity.unit,
      );
      const previous = totals.get(key);
      if (previous)
        previous.quantity.value = round(
          (previous.quantity.value ?? 0) + (quantity.value ?? 0),
        );
      else
        totals.set(key, {
          foodId: ingredient.foodId,
          form: ingredient.form,
          quantity: copy(quantity),
        });
    }
  }
  return [...totals.values()];
}
function stockStatus(
  state: AppState,
  request: ConsumptionRequest,
): ShoppingRow {
  validateQuantity(request.quantity);
  const lots = state.lots.filter(
    (x) =>
      x.status === "active" &&
      x.foodId === request.foodId &&
      x.form === request.form &&
      x.quantity.value !== 0,
  );
  const matching = lots.filter(
    (x) => x.quantity.unit === request.quantity.unit,
  );
  const known = matching.reduce((sum, x) => sum + (x.quantity.value ?? 0), 0);
  const unknown =
    lots.some((x) => x.quantity.value === null) ||
    (lots.length === 0 &&
      state.settings.pantryFoodIds.includes(request.foodId));
  const incompatible = lots.some(
    (x) => x.quantity.unit !== request.quantity.unit,
  );
  let status: ShoppingRow["status"] = "buy";
  let reason = "買い足し";
  let toBuy: number | null = Math.max(
    0,
    round((request.quantity.value ?? 0) - known),
  );
  if (request.quantity.value === null || unknown) {
    status = "unknown";
    reason = "量を確認（数量不明）";
    toBuy = null;
  } else if (incompatible && known < request.quantity.value) {
    status = "incompatible";
    reason = "量を確認（単位が異なります）";
    toBuy = null;
  } else if (known >= request.quantity.value) {
    status = "enough";
    reason = "手持ちで足ります";
    toBuy = 0;
  }
  const key = quantityKey(request.foodId, request.form, request.quantity.unit);
  const signature = `${key}:${request.quantity.value}`;
  return {
    key,
    foodId: request.foodId,
    form: request.form,
    required: copy(request.quantity),
    available: {
      value: unknown || status === "incompatible" ? null : known,
      unit: request.quantity.unit,
    },
    toBuy: { value: toBuy, unit: request.quantity.unit },
    status,
    reason,
    checked: state.shoppingChecks.some(
      (x) => !x.archived && x.key === key && x.signature === signature,
    ),
  };
}
function reconcileShopping(previous: AppState, next: AppState): AppState {
  const signatures = new Set(
    requiredQuantities(next.meal).map(
      (x) =>
        `${quantityKey(x.foodId, x.form, x.quantity.unit)}:${x.quantity.value}`,
    ),
  );
  return {
    ...next,
    shoppingChecks: previous.shoppingChecks.map((x) =>
      signatures.has(x.signature) ? x : { ...x, archived: true },
    ),
  };
}
export function shoppingList(state: AppState): ShoppingList {
  const rows = requiredQuantities(state.meal).map((x) => stockStatus(state, x));
  return {
    rows,
    previous: state.shoppingChecks.filter(
      (check) =>
        check.archived ||
        !rows.some(
          (row) =>
            row.key === check.key &&
            check.signature === `${row.key}:${row.required.value}`,
        ),
    ),
  };
}
export function toggleShoppingCheck(state: AppState, rowKey: string): AppState {
  const row = shoppingList(state).rows.find((x) => x.key === rowKey);
  if (!row)
    return {
      ...state,
      shoppingChecks: state.shoppingChecks.filter((x) => x.key !== rowKey),
    };
  const signature = `${row.key}:${row.required.value}`;
  const checks = state.shoppingChecks.filter((x) => x.signature !== signature);
  if (!row.checked)
    checks.push({
      key: row.key,
      signature,
      foodId: row.foodId,
      quantity: copy(row.required),
      checkedAt: timestamp(),
      archived: false,
    });
  return { ...state, shoppingChecks: checks };
}
function allowedRecipe(state: AppState, recipe: Recipe): boolean {
  const excluded = new Set(state.settings.excludedFoodIds);
  return !recipe.ingredients.some(
    (x) =>
      excluded.has(x.foodId) ||
      getFood(state, x.foodId).componentFoodIds.some((id) => excluded.has(id)),
  );
}
export function searchRecipes(
  state: AppState,
  filters: SearchFilters = state.search,
): Recipe[] {
  return RECIPES.filter((recipe) => {
    if (!allowedRecipe(state, recipe)) return false;
    const ids = recipe.ingredients.map((x) => x.foodId);
    if (
      filters.selectedFoodIds.length &&
      !(filters.match === "all"
        ? filters.selectedFoodIds.every((x) => ids.includes(x))
        : filters.selectedFoodIds.some((x) => ids.includes(x)))
    )
      return false;
    if (filters.maxMinutes !== null && recipe.minutes > filters.maxMinutes)
      return false;
    if (
      filters.equipment.length &&
      !recipe.equipment.every((x) => filters.equipment.includes(x))
    )
      return false;
    if (
      filters.noShopping &&
      recipe.ingredients.some(
        (x) =>
          stockStatus(state, {
            foodId: x.foodId,
            form: x.form,
            quantity: x.quantity,
          }).status === "buy",
      )
    )
      return false;
    return true;
  });
}
export function randomRecipe(
  state: AppState,
  previousId?: string,
): Recipe | null {
  let candidates = RECIPES.filter((x) => allowedRecipe(state, x));
  if (candidates.length > 1)
    candidates = candidates.filter((x) => x.id !== previousId);
  return candidates.length
    ? candidates[Math.floor(Math.random() * candidates.length)]
    : null;
}
export function arrangements(state: AppState, recipeId: string): Recipe[] {
  return getRecipe(recipeId)
    .arrangementIds.map((id) => getRecipe(id))
    .filter((x) => allowedRecipe(state, x));
}
/** リストスケジューリング。同時に行う手作業は1つとし、待ち時間の工程も器具を占有する。 */
export function buildCookingPlan(
  items: MealItem[],
  equipment?: string[],
): PlannedStep[] {
  const recipes = items.map((item) => {
    validateDraft(item);
    return getRecipe(item.recipeId, item.recipeVersionId);
  });
  if (
    equipment &&
    recipes.some((r) => r.equipment.some((e) => !equipment.includes(e)))
  )
    throw new DomainError(
      "MISSING_EQUIPMENT",
      "使う器具の設定を確認してください。",
    );
  const nextIndexes = items.map(() => 0);
  const readyAt = items.map(() => 0);
  const heldUntil = new Map<string, number>();
  let handsFree = 0;
  const result: PlannedStep[] = [];
  while (recipes.some((r, i) => nextIndexes[i] < r.steps.length)) {
    const candidates = recipes
      .flatMap((recipe, i) => {
        const step = recipe.steps[nextIndexes[i]];
        if (!step) return [];
        const start = Math.max(
          readyAt[i],
          handsFree,
          ...step.equipment.map((e) => heldUntil.get(e) ?? 0),
        );
        return [{ i, recipe, step, start }];
      })
      .sort((a, b) => a.start - b.start || a.i - b.i);
    const selected = candidates[0];
    const end = selected.start + selected.step.minutes;
    result.push({
      ...copy(selected.step),
      key: `${items[selected.i].id}:${selected.step.id}`,
      mealItemId: items[selected.i].id,
      recipeId: selected.recipe.id,
      recipeName: selected.recipe.name,
      startMinute: selected.start,
      endMinute: end,
    });
    for (const e of selected.step.equipment) heldUntil.set(e, end);
    if (selected.step.mode !== "passive") handsFree = end;
    else handsFree = selected.start;
    readyAt[selected.i] = end;
    nextIndexes[selected.i]++;
  }
  return result;
}
export function startCooking(
  state: AppState,
  items: MealItem[],
  id = newId(),
): AppState {
  if (!items.length)
    throw new DomainError("EMPTY_MEAL", "料理を選んでください。");
  if (state.cooking && state.cooking.status !== "completed")
    throw new DomainError(
      "COOKING_IN_PROGRESS",
      "調理中の料理を再開するか、完了してから始めてください。",
    );
  return {
    ...state,
    cooking: {
      id,
      mealSnapshot: copy(items),
      plan: buildCookingPlan(items, state.settings.equipment),
      index: 0,
      completedStepIds: [],
      timers: [],
      status: "active",
      consumptionResults: [],
    },
  };
}
export function moveCooking(state: AppState, direction: 1 | -1): AppState {
  if (!state.cooking || state.cooking.status === "completed")
    throw new DomainError("NOT_COOKING", "調理中の工程がありません。");
  const cooking = copy(state.cooking);
  const current = cooking.plan[cooking.index];
  if (
    direction === 1 &&
    current &&
    !cooking.completedStepIds.includes(current.key)
  )
    cooking.completedStepIds.push(current.key);
  cooking.index = Math.max(
    0,
    Math.min(cooking.plan.length, cooking.index + direction),
  );
  return { ...state, cooking };
}
export function pauseCooking(state: AppState): AppState {
  return state.cooking && state.cooking.status !== "completed"
    ? { ...state, cooking: { ...state.cooking, status: "paused" } }
    : state;
}
export function resumeCooking(state: AppState): AppState {
  return state.cooking && state.cooking.status !== "completed"
    ? { ...state, cooking: { ...state.cooking, status: "active" } }
    : state;
}
export function startTimer(
  state: AppState,
  stepKey: string,
  now = Date.now(),
): AppState {
  const cooking = state.cooking;
  const step = cooking?.plan.find((x) => x.key === stepKey);
  if (!cooking || !step || cooking.status === "completed")
    throw new DomainError(
      "TIMER_UNAVAILABLE",
      "タイマーを使う工程を確認してください。",
    );
  if (cooking.timers.some((x) => x.stepKey === stepKey)) return state;
  return {
    ...state,
    cooking: {
      ...cooking,
      timers: [
        ...cooking.timers,
        { stepKey, startedAt: now, durationSeconds: step.minutes * 60 },
      ],
    },
  };
}
export const timerRemaining = (timer: CookingTimer, now = Date.now()): number =>
  Math.max(
    0,
    Math.ceil(timer.durationSeconds - (now - timer.startedAt) / 1000),
  );
export function previewConsumption(
  state: AppState,
  requests: ConsumptionRequest[],
): ConsumptionResult[] {
  const totals = new Map<string, ConsumptionRequest>();
  for (const request of requests) {
    getFood(state, request.foodId);
    validateQuantity(request.quantity);
    const key = quantityKey(
      request.foodId,
      request.form,
      request.quantity.unit,
    );
    const prev = totals.get(key);
    if (prev)
      prev.quantity.value =
        prev.quantity.value === null || request.quantity.value === null
          ? null
          : round(prev.quantity.value + request.quantity.value);
    else totals.set(key, copy(request));
  }
  return [...totals.values()].map((request) => {
    const row = stockStatus(state, request);
    const applied = row.status === "enough" && request.quantity.value !== null;
    const lotIds = applied
      ? state.lots
          .filter(
            (x) =>
              x.status === "active" &&
              x.foodId === request.foodId &&
              x.form === request.form &&
              x.quantity.unit === request.quantity.unit &&
              x.quantity.value !== null &&
              x.quantity.value > 0,
          )
          .sort((a, b) => a.createdAt.localeCompare(b.createdAt))
          .map((x) => x.id)
      : [];
    return {
      ...request,
      applied,
      reason: applied ? "反映できます" : row.reason,
      lotIds,
    };
  });
}
export function completeCooking(
  state: AppState,
  deduct: boolean,
  requests?: ConsumptionRequest[],
): AppState {
  if (!state.cooking)
    throw new DomainError("NOT_COOKING", "調理中の料理がありません。");
  if (state.cooking.status === "completed") return state;
  const next = copy(state);
  const actual = requests ?? requiredQuantities(state.cooking.mealSnapshot);
  for (const request of actual) {
    getFood(state, request.foodId);
    validateQuantity(request.quantity);
  }
  const results = deduct
    ? previewConsumption(state, actual)
    : actual.map((x) => ({
        ...copy(x),
        applied: false,
        reason: "在庫変更なしで完了",
        lotIds: [],
      }));
  if (deduct)
    for (const result of results) {
      if (!result.applied) continue;
      let remaining = result.quantity.value ?? 0;
      const usedIds: string[] = [];
      for (const id of result.lotIds) {
        const lot = next.lots.find((x) => x.id === id)!;
        const used = Math.min(remaining, lot.quantity.value ?? 0);
        if (used > 0) {
          lot.quantity.value = round((lot.quantity.value ?? 0) - used);
          lot.consumed.push({ value: used, unit: result.quantity.unit });
          lot.updatedAt = timestamp();
          remaining = round(remaining - used);
          usedIds.push(id);
        }
        if (remaining === 0) break;
      }
      result.lotIds = usedIds;
      result.reason = "使用量を反映しました";
    }
  next.cooking = {
    ...next.cooking!,
    status: "completed",
    consumptionResults: results,
  };
  return next;
}
