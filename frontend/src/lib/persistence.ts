import {
  DomainError,
  FOODS,
  RECIPES,
  createInitialState,
  ingredientKey,
} from "./domain";
import { UNITS } from "./types";
import type { AppState } from "./types";

export const STORAGE_KEY = "recipeweave.dev.v1";
export interface StorageLike {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
}
export interface LockManagerLike {
  request<T>(name: string, callback: () => T): Promise<T>;
}
/** 一時的な比較用トークン。破損した生データは保存もログ出力もしない。 */
export interface RecoverySnapshot {
  raw: string;
  reason: "malformed-json" | "invalid-data";
}
const fail = (): never => {
  throw new DomainError(
    "INVALID_BACKUP",
    "保存データの形式・版・参照・数量が不正です。現在のデータは変更していません。",
  );
};
const obj = (value: unknown, keys: string[]): Record<string, unknown> => {
  if (!value || typeof value !== "object" || Array.isArray(value))
    return fail();
  const result = value as Record<string, unknown>;
  if (Object.keys(result).sort().join("\0") !== [...keys].sort().join("\0"))
    return fail();
  return result;
};
const str = (value: unknown, max = 500): string => {
  if (typeof value !== "string" || value.length > max || !value.length)
    return fail();
  return value;
};
const bool = (value: unknown): boolean => {
  if (typeof value !== "boolean") return fail();
  return value;
};
const num = (value: unknown, minimum = 0): number => {
  if (typeof value !== "number" || !Number.isFinite(value) || value < minimum)
    return fail();
  return value;
};
const integer = (value: unknown): number => {
  const result = num(value);
  if (!Number.isSafeInteger(result)) return fail();
  return result;
};
const date = (value: unknown): string => {
  const text = str(value);
  if (!/^\d{4}-\d{2}-\d{2}T/.test(text) || !Number.isFinite(Date.parse(text)))
    return fail();
  return text;
};
const strings = (value: unknown, unique = true): string[] => {
  if (!Array.isArray(value)) return fail();
  const result = value.map((x: unknown) => str(x));
  if (unique && new Set(result).size !== result.length) return fail();
  return result;
};
const array = (value: unknown): unknown[] => {
  if (!Array.isArray(value) || value.length > 100000) return fail();
  return value;
};
const oneOf = (value: unknown, options: readonly string[]): string => {
  const result = str(value);
  if (!options.includes(result)) return fail();
  return result;
};
const record = (value: unknown): Record<string, unknown> => {
  if (!value || typeof value !== "object" || Array.isArray(value))
    return fail();
  return value as Record<string, unknown>;
};
const nullable = (value: unknown, validate: (x: unknown) => unknown): void => {
  if (value !== null) validate(value);
};
function canonical(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value && typeof value === "object")
    return `{${Object.entries(value)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([key, item]) => `${JSON.stringify(key)}:${canonical(item)}`)
      .join(",")}}`;
  return JSON.stringify(value);
}
function quantity(value: unknown): void {
  const q = obj(value, ["value", "unit"]);
  nullable(q.value, num);
  oneOf(q.unit, UNITS);
}
function uniqueIds(value: unknown[]): Set<string> {
  const ids = value.map((x) => str(record(x).id));
  if (new Set(ids).size !== ids.length) return fail();
  return new Set(ids);
}

/** 不正な入れ子データと余分な項目を拒否し、レシートの生データがバックアップへ混入するのを防ぐ。 */
export function validateAppState(value: unknown): AppState {
  const root = obj(value, [
    "schemaVersion",
    "version",
    "lots",
    "imports",
    "drafts",
    "meal",
    "saved",
    "shoppingChecks",
    "cooking",
    "settings",
    "customFoods",
    "search",
  ]);
  if (root.schemaVersion !== 1) fail();
  integer(root.version);
  const customFoods = array(root.customFoods);
  const foodIds = uniqueIds(customFoods);
  // 非公開の追加食品がcatalogにも含まれる場合は、同じIDとして扱う。
  for (const food of FOODS) foodIds.add(food.id);
  const foodRef = (x: unknown): string => {
    const id = str(x);
    if (!foodIds.has(id)) return fail();
    return id;
  };
  const recipeIds = new Set(RECIPES.map((x) => x.id));
  const recipeRef = (x: unknown): string => {
    const id = str(x);
    if (!recipeIds.has(id)) return fail();
    return id;
  };
  for (const value of customFoods) {
    const food = obj(value, [
      "id",
      "name",
      "aliases",
      "category",
      "defaultUnit",
      "location",
      "pantry",
      "imageIndex",
      "componentsKnown",
      "componentFoodIds",
    ]);
    str(food.id);
    str(food.name, 80);
    strings(food.aliases);
    str(food.category);
    oneOf(food.defaultUnit, UNITS);
    oneOf(food.location, ["冷蔵", "冷凍", "常温"]);
    bool(food.pantry);
    bool(food.componentsKnown);
    if (food.imageIndex !== null && integer(food.imageIndex) > 11) fail();
    strings(food.componentFoodIds).forEach(foodRef);
  }
  const lots = array(root.lots);
  const lotIds = uniqueIds(lots);
  const imports = array(root.imports);
  const importIds = uniqueIds(imports);
  for (const value of lots) {
    const lot = obj(value, [
      "id",
      "foodId",
      "originalFoodId",
      "quantity",
      "originalQuantity",
      "form",
      "location",
      "priority",
      "expiresOn",
      "createdAt",
      "updatedAt",
      "sourceImportId",
      "status",
      "consumed",
      "edited",
    ]);
    str(lot.id);
    foodRef(lot.foodId);
    foodRef(lot.originalFoodId);
    quantity(lot.quantity);
    quantity(lot.originalQuantity);
    str(lot.form);
    oneOf(lot.location, ["冷蔵", "冷凍", "常温"]);
    bool(lot.priority);
    bool(lot.edited);
    date(lot.createdAt);
    date(lot.updatedAt);
    oneOf(lot.status, ["active", "deleted", "undone"]);
    nullable(lot.expiresOn, (x) => {
      const text = str(x);
      if (
        !/^\d{4}-\d{2}-\d{2}$/.test(text) ||
        !Number.isFinite(Date.parse(text)) ||
        new Date(text).toISOString().slice(0, 10) !== text
      )
        fail();
    });
    nullable(lot.sourceImportId, (x) => {
      if (!importIds.has(str(x))) fail();
    });
    array(lot.consumed).forEach((x) => {
      quantity(x);
      if (record(x).value === null) fail();
    });
  }
  const claimedLotIds = new Set<string>();
  for (const value of imports) {
    const entry = obj(value, [
      "id",
      "imageHash",
      "purchaseSignature",
      "createdAt",
      "state",
      "createdLotIds",
      "undoneAt",
    ]);
    str(entry.id);
    if (
      !/^[0-9a-f]{64}$/.test(str(entry.imageHash)) ||
      !/^[0-9a-f]{64}$/.test(str(entry.purchaseSignature))
    )
      fail();
    date(entry.createdAt);
    oneOf(entry.state, ["registered", "undone"]);
    nullable(entry.undoneAt, date);
    if ((entry.state === "undone") !== (entry.undoneAt !== null)) fail();
    const ids = strings(entry.createdLotIds);
    if (!ids.length) fail();
    for (const id of ids) {
      if (!lotIds.has(id) || claimedLotIds.has(id)) fail();
      claimedLotIds.add(id);
      const lot = record(lots.find((x) => record(x).id === id));
      if (
        lot.sourceImportId !== entry.id ||
        (entry.state === "undone" &&
          lot.status === "active" &&
          !lot.edited &&
          array(lot.consumed).length === 0) ||
        (entry.state === "registered" && lot.status === "undone")
      )
        fail();
    }
  }
  for (const lot of lots.map(record))
    if ((lot.sourceImportId !== null) !== claimedLotIds.has(str(lot.id)))
      fail();
  function draft(value: unknown, meal = false): void {
    const d = obj(value, [
      "recipeId",
      ...(record(value).recipeVersionId !== undefined
        ? ["recipeVersionId"]
        : []),
      "servings",
      "amounts",
      "adjusted",
      ...(meal ? ["id"] : []),
    ]);
    if (meal) str(d.id);
    const recipeId = recipeRef(d.recipeId);
    if (num(d.servings) <= 0) fail();
    bool(d.adjusted);
    const versionId =
      d.recipeVersionId === undefined ? undefined : str(d.recipeVersionId);
    const recipe = RECIPES.find(
      (x) => x.id === recipeId && (!versionId || x.versionId === versionId),
    );
    if (!recipe) return fail();
    const amounts = obj(d.amounts, recipe.ingredients.map(ingredientKey));
    for (const ingredient of recipe.ingredients) {
      quantity(amounts[ingredientKey(ingredient)]);
      const q = record(amounts[ingredientKey(ingredient)]);
      if (q.value === null || q.unit !== ingredient.quantity.unit) fail();
    }
  }
  for (const [id, d] of Object.entries(record(root.drafts))) {
    recipeRef(id);
    draft(d);
    if (record(d).recipeId !== id) fail();
  }
  const meal = array(root.meal);
  uniqueIds(meal);
  meal.forEach((x) => draft(x, true));
  strings(root.saved).forEach(recipeRef);
  const shopping = array(root.shoppingChecks);
  const signatures: string[] = [];
  for (const value of shopping) {
    const check = obj(value, [
      "key",
      "signature",
      "foodId",
      "quantity",
      "checkedAt",
      "archived",
    ]);
    bool(check.archived);
    const foodId = foodRef(check.foodId);
    quantity(check.quantity);
    date(check.checkedAt);
    const key = str(check.key);
    const q = record(check.quantity);
    if (
      !key.startsWith(`${foodId}|`) ||
      !key.endsWith(`|${str(q.unit)}`) ||
      check.signature !== `${key}:${String(q.value)}`
    )
      fail();
    signatures.push(str(check.signature));
  }
  if (new Set(signatures).size !== signatures.length) fail();
  const settings = obj(root.settings, [
    "excludedFoodIds",
    "pantryFoodIds",
    "equipment",
  ]);
  strings(settings.excludedFoodIds).forEach(foodRef);
  strings(settings.pantryFoodIds).forEach(foodRef);
  strings(settings.equipment);
  const search = obj(root.search, [
    "selectedFoodIds",
    "match",
    "maxMinutes",
    "noShopping",
    "equipment",
  ]);
  strings(search.selectedFoodIds).forEach(foodRef);
  oneOf(search.match, ["all", "any"]);
  nullable(search.maxMinutes, num);
  bool(search.noShopping);
  strings(search.equipment);
  if (root.cooking !== null) {
    const cooking = obj(root.cooking, [
      "id",
      "mealSnapshot",
      "plan",
      "index",
      "completedStepIds",
      "timers",
      "status",
      "consumptionResults",
    ]);
    str(cooking.id);
    const snapshot = array(cooking.mealSnapshot);
    uniqueIds(snapshot);
    if (!snapshot.length) fail();
    snapshot.forEach((x) => draft(x, true));
    // サーバーの工程依存関係と器具容量に基づく計画を正本とする。
    // ブラウザの簡易計画で上書きせず、参照・重複・時間の整合性だけを検証する。
    const expectedKeys = new Set(
      (snapshot as AppState["meal"]).flatMap((item) =>
        RECIPES.find(
          (recipe) =>
            recipe.id === item.recipeId &&
            (!item.recipeVersionId ||
              recipe.versionId === item.recipeVersionId),
        )!.steps.map((step) => `${item.id}:${step.id}`),
      ),
    );
    const plan = array(cooking.plan);
    const stepKeys = new Set<string>();
    let previousStart = 0;
    for (const value of plan) {
      const step = obj(value, [
        "id",
        "title",
        "instruction",
        "minutes",
        "mode",
        "equipment",
        "guide",
        "key",
        "mealItemId",
        "recipeId",
        "recipeName",
        "startMinute",
        "endMinute",
        ...(record(value).timeScalingMode !== undefined
          ? ["timeScalingMode"]
          : []),
        ...(record(value).durationSource !== undefined
          ? ["durationSource"]
          : []),
        ...(record(value).confirmedDurationSeconds !== undefined
          ? ["confirmedDurationSeconds"]
          : []),
      ]);
      const key = str(step.key);
      const itemId = str(step.mealItemId);
      const recipeId = recipeRef(step.recipeId);
      const id = str(step.id);
      if (
        !expectedKeys.has(key) ||
        stepKeys.has(key) ||
        key !== `${itemId}:${id}` ||
        !snapshot.some(
          (item) =>
            record(item).id === itemId && record(item).recipeId === recipeId,
        )
      )
        fail();
      stepKeys.add(key);
      str(step.title);
      str(step.instruction, 10000);
      str(step.recipeName);
      strings(step.equipment);
      nullable(step.guide, str);
      oneOf(step.mode, ["active", "passive", "monitored"]);
      if (step.timeScalingMode !== undefined)
        oneOf(step.timeScalingMode, [
          "linear",
          "fixed_batch",
          "capacity_batch",
          "validated_curve",
          "manual",
        ]);
      if (step.durationSource !== undefined)
        oneOf(step.durationSource, ["recipe_rule", "user_estimate"]);
      if (step.confirmedDurationSeconds !== undefined)
        nullable(step.confirmedDurationSeconds, num);
      if (
        step.durationSource === "user_estimate" &&
        (step.confirmedDurationSeconds === null ||
          step.confirmedDurationSeconds === undefined ||
          num(step.confirmedDurationSeconds) <= 0)
      )
        fail();
      const minutes = num(step.minutes);
      const start = num(step.startMinute);
      const end = num(step.endMinute);
      if (
        start < previousStart ||
        end < start ||
        Math.abs(end - start - minutes) > 0.000001
      )
        fail();
      previousStart = start;
    }
    if (
      stepKeys.size !== expectedKeys.size ||
      integer(cooking.index) > plan.length ||
      (cooking.status !== "completed" && integer(cooking.index) === plan.length)
    )
      fail();
    oneOf(cooking.status, ["active", "paused", "completed"]);
    strings(cooking.completedStepIds).forEach((x) => {
      if (!stepKeys.has(x)) fail();
    });
    const timerKeys: string[] = [];
    for (const value of array(cooking.timers)) {
      const timer = obj(value, ["stepKey", "startedAt", "durationSeconds"]);
      const key = str(timer.stepKey);
      if (!stepKeys.has(key)) fail();
      timerKeys.push(key);
      num(timer.startedAt);
      num(timer.durationSeconds);
      if (
        timer.durationSeconds !==
        Number(record(plan.find((x) => record(x).key === key)).minutes) * 60
      )
        fail();
    }
    if (new Set(timerKeys).size !== timerKeys.length) fail();
    for (const value of array(cooking.consumptionResults)) {
      const result = obj(value, [
        "foodId",
        "quantity",
        "form",
        "applied",
        "reason",
        "lotIds",
      ]);
      foodRef(result.foodId);
      quantity(result.quantity);
      str(result.form);
      bool(result.applied);
      str(result.reason);
      strings(result.lotIds).forEach((x) => {
        if (!lotIds.has(x)) fail();
      });
    }
  }
  return structuredClone(value) as AppState;
}
export function parseBackup(text: string): AppState {
  try {
    return validateAppState(JSON.parse(text) as unknown);
  } catch (error) {
    if (error instanceof DomainError) throw error;
    return fail();
  }
}
function defaultStorage(): StorageLike {
  try {
    return localStorage;
  } catch {
    throw new DomainError(
      "STORAGE_UNAVAILABLE",
      "このブラウザでは保存領域を使えません。設定を確認してください。",
    );
  }
}
function readRaw(storage: StorageLike): string | null {
  try {
    return storage.getItem(STORAGE_KEY);
  } catch {
    throw new DomainError(
      "STORAGE_UNAVAILABLE",
      "保存データを読み込めません。現在のデータを保ったまま再試行してください。",
    );
  }
}
export function loadState(storage: StorageLike = defaultStorage()): AppState {
  const raw = readRaw(storage);
  return raw === null ? createInitialState() : parseBackup(raw);
}
function recoveryCandidate(raw: string | null): RecoverySnapshot {
  if (raw === null)
    throw new DomainError(
      "RECOVERY_NOT_REQUIRED",
      "保存データは破損していません。通常のデータ読込みを使ってください。",
    );
  let value: unknown;
  try {
    value = JSON.parse(raw) as unknown;
  } catch {
    return { raw, reason: "malformed-json" };
  }
  // 異なるバージョンの宣言は将来の正当な形式の可能性があるため、破損とみなさない。
  if (value && typeof value === "object" && !Array.isArray(value)) {
    const declared = (value as Record<string, unknown>).schemaVersion;
    if (typeof declared === "number" && declared !== 1)
      throw new DomainError(
        "UNSUPPORTED_SCHEMA",
        "この保存データは異なる版です。新しい対応版で開いてください。破損データとして上書きできません。",
      );
  }
  try {
    validateAppState(value);
  } catch (error) {
    if (error instanceof DomainError && error.code === "INVALID_BACKUP")
      return { raw, reason: "invalid-data" };
    throw error;
  }
  throw new DomainError(
    "RECOVERY_NOT_REQUIRED",
    "保存データは正常です。再読込みして通常のデータ読込みを使ってください。",
  );
}
export function inspectRecovery(
  storage: StorageLike = defaultStorage(),
): RecoverySnapshot {
  return recoveryCandidate(readRaw(storage));
}
function defaultLocks(): LockManagerLike {
  if (typeof navigator === "undefined" || !navigator.locks)
    throw new DomainError(
      "LOCKS_UNAVAILABLE",
      "このブラウザでは安全に保存できません。最新版のChrome・Safari・Firefox等で開いてください。閲覧とデータの書き出しはできます。",
    );
  return {
    request: (name, callback) => navigator.locks.request(name, callback),
  };
}
export async function transact(
  state: AppState,
  mutator: (current: AppState) => AppState,
  storage: StorageLike = defaultStorage(),
  locks: LockManagerLike = defaultLocks(),
): Promise<AppState> {
  return locks.request(STORAGE_KEY, () => {
    const current = loadState(storage);
    if (
      current.version !== state.version ||
      canonical(current) !== canonical(state)
    )
      throw new DomainError(
        "VERSION_CONFLICT",
        "別のタブでデータが更新されました。再読込みしてからもう一度お試しください。",
      );
    const changed = mutator(structuredClone(state));
    const next = validateAppState({
      ...changed,
      schemaVersion: 1,
      version: state.version + 1,
    });
    try {
      storage.setItem(STORAGE_KEY, JSON.stringify(next));
    } catch {
      throw new DomainError(
        "STORAGE_FULL",
        "保存できませんでした。容量やブラウザ設定を確認してください。データは変更していません。",
      );
    }
    return next;
  });
}
export function exportBackup(state: AppState): string {
  return JSON.stringify(validateAppState(state), null, 2);
}
export async function restoreBackup(
  current: AppState,
  backup: AppState,
  storage?: StorageLike,
  locks?: LockManagerLike,
): Promise<AppState> {
  const validated = validateAppState(backup);
  return transact(current, () => validated, storage, locks);
}

/** 検証済みバックアップで破損データを置き換えることを、利用者が確認してから呼び出す。 */
export async function recoverBackup(
  recovery: RecoverySnapshot,
  backup: AppState,
  storage: StorageLike = defaultStorage(),
  locks: LockManagerLike = defaultLocks(),
): Promise<AppState> {
  const validated = validateAppState(backup);
  return locks.request(STORAGE_KEY, () => {
    const raw = readRaw(storage);
    if (raw !== recovery.raw)
      throw new DomainError(
        "VERSION_CONFLICT",
        "確認後に別のタブで保存データが変わりました。復旧を中止しました。再読込みして確認してください。",
      );
    recoveryCandidate(raw); // ロック内で再検査し、偽造トークンによる正常データや将来形式の上書きを防ぐ。
    let previousVersion = 0;
    try {
      const previous = JSON.parse(recovery.raw) as unknown;
      if (
        previous &&
        typeof previous === "object" &&
        !Array.isArray(previous)
      ) {
        const version = (previous as Record<string, unknown>).version;
        if (
          typeof version === "number" &&
          Number.isSafeInteger(version) &&
          version >= 0 &&
          version < Number.MAX_SAFE_INTEGER
        )
          previousVersion = version;
      }
    } catch {
      /* JSONの構文が破損している場合、リビジョンは信頼できない。 */
    }
    // 破損したリビジョンを1から再開した場合も、通常の更新で内容を比較することで、
    // 復旧前の古いタブからの更新を拒否する。
    const next = validateAppState({
      ...validated,
      version: previousVersion + 1,
    });
    try {
      storage.setItem(STORAGE_KEY, JSON.stringify(next));
    } catch {
      throw new DomainError(
        "STORAGE_FULL",
        "復旧データを保存できませんでした。元の保存内容は変更していません。容量や設定を確認してください。",
      );
    }
    return next;
  });
}
