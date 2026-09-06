import { fixtureFoods, fixtureRecipes } from "../test-fixtures";
import { setCatalog } from "./domain";
beforeEach(() => setCatalog(fixtureFoods, fixtureRecipes));
import { beforeEach, describe, expect, it } from "vitest";
import {
  addStock,
  addToMeal,
  arrangements,
  buildCookingPlan,
  commitReceipt,
  completeCooking,
  createInitialState,
  getDraft,
  getRecipe,
  moveCooking,
  previewConsumption,
  previewUndoImport,
  randomRecipe,
  removeFromMeal,
  scaleDraft,
  searchRecipes,
  setDraftAmount,
  shoppingList,
  startCooking,
  startTimer,
  timerRemaining,
  toggleShoppingCheck,
  undoImport,
  updateMeal,
  updateStock,
} from "./domain";
import { parseReceipt, receiptSignature, validateReceiptFile } from "./receipt";
import {
  exportBackup,
  inspectRecovery,
  loadState,
  parseBackup,
  recoverBackup,
  restoreBackup,
  STORAGE_KEY,
  transact,
} from "./persistence";
import type { LockManagerLike, StorageLike } from "./persistence";
import type { AppState, ReceiptCommit } from "./types";

const receipt = (id = "receipt-1"): ReceiptCommit => ({
  id,
  imageHash: "a".repeat(64),
  purchaseSignature: "b".repeat(64),
  allowDuplicate: false,
  candidates: [
    {
      id: "1",
      rawText: "豆腐 300g 198円",
      foodId: "tofu",
      quantity: { value: 300, unit: "g" },
      selected: true,
      status: "matched",
      reason: "",
    },
  ],
});
class MemoryStorage implements StorageLike {
  value: string | null = null;
  fail = false;
  getItem(): string | null {
    return this.value;
  }
  setItem(_key: string, value: string): void {
    if (this.fail) throw new Error("quota");
    this.value = value;
  }
}
class SerialLocks implements LockManagerLike {
  private tail: Promise<unknown> = Promise.resolve();
  request<T>(_name: string, callback: () => T): Promise<T> {
    const next = this.tail.then(callback);
    this.tail = next.catch(() => undefined);
    return next;
  }
}
function cookingTofu(state: AppState): AppState {
  return startCooking(
    state,
    [{ ...getDraft(state, "tofu-soup"), id: "meal-1" }],
    "cook-1",
  );
}

describe("quantities and search", () => {
  it("scales latest edits by serving ratio without changing time", () => {
    const draft = getDraft(createInitialState(), "eggplant-egg");
    const three = scaleDraft(draft, 3);
    expect(three.amounts.eggplant.value).toBe(240);
    expect(three.amounts.egg.value).toBe(3);
    expect(three.amounts.oil.value).toBe(12);
    const custom = setDraftAmount(three, "eggplant", { value: 180, unit: "g" });
    expect(scaleDraft(custom, 2).amounts.eggplant.value).toBe(120);
    expect(getRecipe("eggplant-egg").minutes).toBe(15);
    expect(() => scaleDraft(draft, 0)).toThrow();
    expect(() =>
      setDraftAmount(draft, "egg", { value: -1, unit: "個" }),
    ).toThrow();
  });
  it("applies exclusions to search, arrangements and random without relaxing zero results", () => {
    const state = createInitialState();
    state.settings.excludedFoodIds = ["egg"];
    state.search.selectedFoodIds = ["eggplant"];
    expect(searchRecipes(state)).toEqual([]);
    expect(arrangements(state, "eggplant-egg")).toEqual([]);
    for (let n = 0; n < 20; n++)
      expect(
        randomRecipe(state)?.ingredients.some((x) => x.foodId === "egg"),
      ).toBe(false);
    state.settings.excludedFoodIds = [
      "egg",
      "tofu",
      "tuna",
      "yakisoba",
      "mushroom",
    ];
    expect(randomRecipe(state)).toBeNull();
  });
  it("keeps quantities unknown, zero and incompatible distinct", () => {
    let state = addToMeal(
      createInitialState(),
      getDraft(createInitialState(), "eggplant-egg"),
      "meal-1",
    );
    state = addStock(state, {
      foodId: "eggplant",
      quantity: { value: null, unit: "g" },
    });
    state = addStock(state, {
      foodId: "egg",
      quantity: { value: 1, unit: "パック" },
    });
    state = addStock(state, {
      foodId: "oil",
      quantity: { value: 0, unit: "g" },
    });
    const rows = shoppingList(state).rows;
    expect(rows.find((x) => x.foodId === "eggplant")?.status).toBe("unknown");
    expect(rows.find((x) => x.foodId === "egg")?.status).toBe("incompatible");
    expect(rows.find((x) => x.foodId === "egg")?.available.value).toBeNull();
    expect(rows.find((x) => x.foodId === "oil")?.toBuy.value).toBe(8);
  });
});

describe("receipt review and import integrity", () => {
  it("does not turn a price into weight, preserves duplicate rows and offers excluded rows", () => {
    const rows = parseReceipt(
      "鶏肉 198円\n鶏肉 198円\nキャベツ 1点 200円\n卵10個入 248円\n洗剤 398円\n合計 1242円\nナス ２００ｇ 100円",
    );
    expect(rows).toHaveLength(7);
    expect(rows[0].quantity.value).toBeNull();
    expect(rows[1].foodId).toBe("chicken");
    expect(rows[2].quantity).toEqual({ value: 1, unit: "点" });
    expect(rows[3].quantity.value).toBeNull();
    expect(rows[4].status).toBe("excluded");
    expect(rows[5].selected).toBe(false);
    expect(rows[6].quantity).toEqual({ value: 200, unit: "g" });
  });
  it("preserves multiplicity in purchase signature and ignores source OCR metadata", async () => {
    const rows = parseReceipt("トマト 198円\n卵 1パック 248円");
    expect(await receiptSignature(rows)).toBe(
      await receiptSignature([...rows].reverse()),
    );
    expect(await receiptSignature(rows)).not.toBe(
      await receiptSignature([...rows, rows[0]]),
    );
    expect(await receiptSignature(rows)).toMatch(/^[0-9a-f]{64}$/);
  });
  it("commits selected valid rows atomically and is idempotent before duplicate warning", () => {
    const state = createInitialState();
    const input = receipt();
    input.candidates.push({
      id: "unresolved",
      rawText: "キヌ",
      foodId: null,
      quantity: { value: null, unit: "g" },
      selected: false,
      status: "review",
      reason: "",
    });
    const next = commitReceipt(state, input);
    expect(next.lots).toHaveLength(1);
    expect(state.lots).toHaveLength(0);
    expect(commitReceipt(next, input)).toBe(next);
    expect(() => commitReceipt(next, { ...input, id: "other" })).toThrow(
      "登録済み",
    );
    expect(
      commitReceipt(next, { ...input, id: "other", allowDuplicate: true }).lots,
    ).toHaveLength(2);
    input.candidates[1].selected = true;
    expect(() => commitReceipt(state, input)).toThrow("食材名");
    expect(state.lots).toHaveLength(0);
    expect(exportBackup(next)).not.toContain("rawText");
    expect(exportBackup(next)).not.toContain("198円");
  });
  it("取消は使用済み在庫を保護し、同じ登録に二度適用しない", () => {
    let state = commitReceipt(createInitialState(), receipt());
    state.lots[0].createdAt = "2026-01-01T00:00:00.000Z";
    state = addStock(
      state,
      { foodId: "tofu", quantity: { value: 100, unit: "g" } },
      "previous",
    );
    const imported = state.lots[0].id;
    state = cookingTofu(state);
    state = completeCooking(state, true, [
      { foodId: "tofu", form: "標準", quantity: { value: 100, unit: "g" } },
    ]);
    expect(state.lots.find((x) => x.id === imported)?.quantity.value).toBe(200);
    expect(previewUndoImport(state, "receipt-1").needsConfirmation).toBe(true);
    const undone = undoImport(state, "receipt-1");
    expect(undone.lots.find((x) => x.id === imported)?.status).toBe("active");
    expect(undone.lots.find((x) => x.id === imported)?.quantity.value).toBe(200);
    expect(undone.lots.find((x) => x.id === imported)?.consumed[0].value).toBe(
      100,
    );
    expect(undone.lots.find((x) => x.id === "previous")?.quantity.value).toBe(
      100,
    );
    expect(() => undoImport(undone, "receipt-1")).toThrow("取消済み");
  });
  it("uses current edited remaining amount for undo preview", () => {
    let state = commitReceipt(createInitialState(), receipt());
    const id = state.lots[0].id;
    state = updateStock(state, id, {
      foodId: "tofu",
      quantity: { value: 250, unit: "g" },
    });
    const preview = previewUndoImport(state, "receipt-1");
    expect(preview.lots[0].quantity.value).toBe(250);
    expect(preview.lots[0].originalQuantity.value).toBe(300);
    expect(preview.needsConfirmation).toBe(true);
  });
  it("refuses unsupported or oversized image inputs", () => {
    expect(() =>
      validateReceiptFile({ type: "image/heic", size: 100 }),
    ).toThrow();
    expect(() =>
      validateReceiptFile({ type: "image/png", size: 10 * 1024 * 1024 + 1 }),
    ).toThrow();
    expect(() =>
      validateReceiptFile({ type: "image/png", size: 10 * 1024 * 1024 }),
    ).not.toThrow();
  });
});

describe("meals, cooking and consumption", () => {
  it("clears changed purchase checks and retains memos without resurrecting checks", () => {
    let state = addToMeal(
      createInitialState(),
      getDraft(createInitialState(), "eggplant-egg"),
      "main",
    );
    const key = shoppingList(state).rows[0].key;
    state = toggleShoppingCheck(state, key);
    const initialLots = structuredClone(state.lots);
    state = updateMeal(state, "main", scaleDraft(state.meal[0], 3));
    expect(shoppingList(state).rows[0].checked).toBe(false);
    expect(shoppingList(state).previous).toHaveLength(1);
    state = updateMeal(state, "main", scaleDraft(state.meal[0], 2));
    expect(shoppingList(state).rows[0].checked).toBe(false);
    state = removeFromMeal(state, "main");
    expect(shoppingList(state).rows).toHaveLength(0);
    expect(shoppingList(state).previous).toHaveLength(1);
    expect(state.lots).toEqual(initialLots);
  });
  it("schedules one active task and each appliance at a time while using passive waits", () => {
    const state = createInitialState();
    const items = ["tofu-soup", "cabbage-tuna"].map((id, index) => ({
      ...getDraft(state, id),
      id: `m${index}`,
    }));
    const plan = buildCookingPlan(items);
    let overlap = false;
    for (let a = 0; a < plan.length; a++)
      for (let b = a + 1; b < plan.length; b++) {
        const left = plan[a];
        const right = plan[b];
        const intersects =
          left.startMinute < right.endMinute &&
          right.startMinute < left.endMinute;
        if (intersects) {
          overlap = true;
          expect(left.mode === "active" && right.mode === "active").toBe(false);
          expect(left.equipment.some((x) => right.equipment.includes(x))).toBe(
            false,
          );
        }
      }
    expect(overlap).toBe(true);
    for (const item of items) {
      const steps = plan.filter((x) => x.mealItemId === item.id);
      for (let i = 1; i < steps.length; i++)
        expect(steps[i].startMinute).toBeGreaterThanOrEqual(
          steps[i - 1].endMinute,
        );
    }
  });
  it("keeps timers after back/reopen, and completion requires consent and only applies once", () => {
    let state = addStock(createInitialState(), {
      foodId: "tofu",
      quantity: { value: 200, unit: "g" },
    });
    state = cookingTofu(state);
    const key = state.cooking!.plan[0].key;
    state = startTimer(state, key, 1000);
    state = moveCooking(state, 1);
    state = moveCooking(state, -1);
    expect(startTimer(state, key, 2000).cooking!.timers).toHaveLength(1);
    expect(timerRemaining(state.cooking!.timers[0], 1000000)).toBe(0);
    const noDeduct = completeCooking(state, false);
    expect(noDeduct.lots[0].quantity.value).toBe(200);
    const deducted = completeCooking(state, true);
    expect(deducted.lots[0].quantity.value).toBe(50);
    expect(completeCooking(deducted, true).lots[0].quantity.value).toBe(50);
  });
  it("does not partially consume insufficient or uncertain inventory", () => {
    let state = addStock(createInitialState(), {
      foodId: "tofu",
      quantity: { value: 50, unit: "g" },
    });
    const request = {
      foodId: "tofu",
      form: "標準",
      quantity: { value: 100, unit: "g" as const },
    };
    expect(previewConsumption(state, [request])[0].applied).toBe(false);
    state = addStock(state, {
      foodId: "tofu",
      quantity: { value: null, unit: "g" },
    });
    expect(previewConsumption(state, [request])[0].reason).toContain(
      "数量不明",
    );
    expect(
      completeCooking(cookingTofu(state), true, [request]).lots[0].quantity
        .value,
    ).toBe(50);
  });
});

describe("validated atomic persistence", () => {
  it("restores only a fully valid snapshot and rejects corrupt references, quantities, fields and versions", () => {
    const state = commitReceipt(createInitialState(), receipt());
    expect(parseBackup(exportBackup(state))).toEqual(state);
    const invalids: unknown[] = [
      null,
      { ...state, schemaVersion: 2 },
      { ...state, image: "private" },
      { ...state, lots: [{ ...state.lots[0], foodId: "missing" }] },
      {
        ...state,
        lots: [{ ...state.lots[0], quantity: { value: -3, unit: "g" } }],
      },
      { ...state, imports: [] },
      {
        ...state,
        lots: [{ ...state.lots[0], consumed: [{ value: null, unit: "g" }] }],
      },
    ];
    for (const invalid of invalids)
      expect(() => parseBackup(JSON.stringify(invalid))).toThrow();
    expect(() => parseBackup("{")).toThrow();
  });
  it("preserves stored and UI state when saving fails or stale tab attempts a write", async () => {
    const storage = new MemoryStorage();
    const locks = new SerialLocks();
    const before = createInitialState();
    const saved = await transact(
      before,
      (s) => addStock(s, { foodId: "egg", quantity: { value: 2, unit: "個" } }),
      storage,
      locks,
    );
    const raw = storage.value;
    storage.fail = true;
    await expect(
      transact(
        saved,
        (s) =>
          addStock(s, { foodId: "tofu", quantity: { value: null, unit: "g" } }),
        storage,
        locks,
      ),
    ).rejects.toThrow("保存できません");
    expect(storage.value).toBe(raw);
    expect(saved.lots).toHaveLength(1);
    await expect(transact(before, (s) => s, storage, locks)).rejects.toThrow(
      "別のタブ",
    );
    expect(before.version).toBe(0);
  });
  it("serializes simultaneous tabs and accepts exactly one update", async () => {
    const storage = new MemoryStorage();
    const locks = new SerialLocks();
    const state = createInitialState();
    const result = await Promise.allSettled([
      transact(
        state,
        (s) =>
          addStock(s, { foodId: "egg", quantity: { value: 2, unit: "個" } }),
        storage,
        locks,
      ),
      transact(
        state,
        (s) =>
          addStock(s, { foodId: "tofu", quantity: { value: 100, unit: "g" } }),
        storage,
        locks,
      ),
    ]);
    expect(result.filter((x) => x.status === "fulfilled")).toHaveLength(1);
    expect(loadState(storage).lots).toHaveLength(1);
  });
  it("replaces without merging, increments current version, and never resets corrupt storage", async () => {
    const storage = new MemoryStorage();
    const locks = new SerialLocks();
    let state = createInitialState();
    state = await transact(
      state,
      (s) => addStock(s, { foodId: "egg", quantity: { value: 2, unit: "個" } }),
      storage,
      locks,
    );
    const restored = await restoreBackup(
      state,
      createInitialState(),
      storage,
      locks,
    );
    expect(restored.lots).toHaveLength(0);
    expect(restored.version).toBe(2);
    storage.setItem(STORAGE_KEY, "{");
    expect(() => loadState(storage)).toThrow();
    expect(storage.value).toBe("{");
  });
  it("recovers syntactically damaged data only after inspection, using a validated backup", async () => {
    const storage = new MemoryStorage();
    const locks = new SerialLocks();
    storage.value = "{";
    const token = inspectRecovery(storage);
    expect(token.reason).toBe("malformed-json");
    expect(storage.value).toBe("{");
    const backup = addStock(createInitialState(), {
      foodId: "egg",
      quantity: { value: 3, unit: "個" },
    });
    const recovered = await recoverBackup(token, backup, storage, locks);
    expect(recovered.lots[0].quantity.value).toBe(3);
    expect(recovered.version).toBe(1);
    expect(loadState(storage)).toEqual(recovered);
  });
  it("recovers a broken known schema and retains its revision progression", async () => {
    const storage = new MemoryStorage();
    const locks = new SerialLocks();
    storage.value = JSON.stringify({
      schemaVersion: 1,
      version: 11,
      lots: "broken",
    });
    const token = inspectRecovery(storage);
    expect(token.reason).toBe("invalid-data");
    const recovered = await recoverBackup(
      token,
      createInitialState(),
      storage,
      locks,
    );
    expect(recovered.version).toBe(12);
  });
  it("never treats healthy state or an unknown schema version as recovery candidates", async () => {
    const storage = new MemoryStorage();
    const locks = new SerialLocks();
    for (const value of [
      createInitialState(),
      { ...createInitialState(), schemaVersion: 2 },
    ]) {
      storage.value = JSON.stringify(value);
      const raw = storage.value;
      expect(() => inspectRecovery(storage)).toThrow();
      await expect(
        recoverBackup(
          { raw, reason: "invalid-data" },
          createInitialState(),
          storage,
          locks,
        ),
      ).rejects.toThrow();
      expect(storage.value).toBe(raw);
    }
    storage.value = null;
    expect(() => inspectRecovery(storage)).toThrow();
  });
  it("rejects changed damaged raw data and concurrent recovery even when no valid version exists", async () => {
    const storage = new MemoryStorage();
    const locks = new SerialLocks();
    storage.value = "{";
    const token = inspectRecovery(storage);
    storage.value = "{other";
    await expect(
      recoverBackup(token, createInitialState(), storage, locks),
    ).rejects.toThrow("別のタブ");
    expect(storage.value).toBe("{other");
    const fresh = inspectRecovery(storage);
    const results = await Promise.allSettled([
      recoverBackup(fresh, createInitialState(), storage, locks),
      recoverBackup(fresh, createInitialState(), storage, locks),
    ]);
    expect(results.filter((x) => x.status === "fulfilled")).toHaveLength(1);
  });
  it("retains damaged raw content when the backup is invalid or recovery cannot save", async () => {
    const storage = new MemoryStorage();
    const locks = new SerialLocks();
    storage.value = "{";
    const token = inspectRecovery(storage);
    await expect(
      recoverBackup(
        token,
        { ...createInitialState(), saved: ["missing"] },
        storage,
        locks,
      ),
    ).rejects.toThrow();
    expect(storage.value).toBe("{");
    storage.fail = true;
    await expect(
      recoverBackup(token, createInitialState(), storage, locks),
    ).rejects.toThrow("保存できません");
    expect(storage.value).toBe("{");
  });
  it("rejects a stale pre-recovery tab even if the recovered revision has the same number", async () => {
    const storage = new MemoryStorage();
    const locks = new SerialLocks();
    const stale = { ...createInitialState(), version: 1 };
    storage.value = "{";
    const recovered = await recoverBackup(
      inspectRecovery(storage),
      addStock(createInitialState(), {
        foodId: "egg",
        quantity: { value: 3, unit: "個" },
      }),
      storage,
      locks,
    );
    expect(recovered.version).toBe(stale.version);
    await expect(transact(stale, (s) => s, storage, locks)).rejects.toThrow(
      "別のタブ",
    );
    expect(loadState(storage).lots).toHaveLength(1);
  });
});
