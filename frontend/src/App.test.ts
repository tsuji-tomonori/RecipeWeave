// @vitest-environment jsdom
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/svelte";
import { webcrypto } from "node:crypto";
import App from "./App.svelte";
import { createInitialState, getDraft, startCooking } from "./lib/domain";
import * as D from "./lib/domain";
import type { AppState, SearchFilters, ReceiptCommit, Food } from "./lib/types";
import { fixtureFoods, fixtureRecipes } from "./test-fixtures";
const backend = vi.hoisted(() => ({
  state: null as AppState | null,
  failLoad: false,
}));
vi.mock("./lib/auth", () => ({
  completeLogin: async () => {},
  localMode: true,
  logout: () => {},
  loginCognito: async () => {},
}));
vi.mock("./lib/api", async () => ({
  ApiError: class extends Error {
    status = 0;
  },
  currentUser: async () => ({
    id: "alice",
    display_name: "Alice",
    role: "user",
  }),
  previewCookingPlan: async (items: AppState["meal"]) => ({
    plan: D.buildCookingPlan(items, backend.state!.settings.equipment),
  }),
  loadFoods: async () => {
    if (backend.failLoad) throw new Error("サーバーに接続できません");
    return fixtureFoods;
  },
  findRecipes: async (filters?: SearchFilters) => {
    const items = filters
      ? D.searchRecipes(backend.state!, filters)
      : fixtureRecipes;
    D.cacheRecipes(items);
    return { items, total: items.length, offset: 0, limit: 50 };
  },
  randomRecipe: async (_excluded: string[], previous: string) => {
    const recipe = D.randomRecipe(backend.state!, previous);
    if (!recipe) throw new Error("対象なし");
    return recipe;
  },
  loadRecipe: async (id: string) => D.getRecipe(id),
  loadState: async () => structuredClone(backend.state!),
  saveState: async (_old: AppState, next: AppState) => {
    await new Promise((resolve) => setTimeout(resolve, 5));
    backend.state = { ...structuredClone(next), version: next.version + 1 };
    return structuredClone(backend.state);
  },
  completeCooking: async (
    current: AppState,
    deduct: boolean,
    consumption: import("./lib/types").ConsumptionRequest[],
  ) => {
    backend.state = D.completeCooking(current, deduct, consumption);
    return structuredClone(backend.state);
  },
  commitReceipt: async (
    current: AppState,
    input: ReceiptCommit,
    customFoods: Food[],
  ) => {
    backend.state = D.commitReceipt({ ...current, customFoods }, input);
    return structuredClone(backend.state);
  },
}));
vi.mock("./lib/ocr", () => ({
  validateReceiptImage: async () => {},
  recognizeReceipt: () => ({
    cancel: async () => {},
    result: Promise.resolve(
      "トマト 198円\nたまご 248円\nキヌ 98円\nレジ袋 5円\n合計 549円",
    ),
  }),
}));

beforeEach(() => {
  localStorage.clear();
  sessionStorage.clear();
  D.setCatalog(fixtureFoods, fixtureRecipes);
  backend.state = createInitialState();
  backend.failLoad = false;
  window.history.replaceState(null, "", "#/home");
  Object.defineProperty(globalThis, "crypto", {
    value: webcrypto,
    configurable: true,
  });
  Object.defineProperty(navigator, "locks", {
    value: {
      request: async (_name: string, fn: () => unknown) =>
        new Promise((resolve, reject) =>
          setTimeout(() => {
            try {
              resolve(fn());
            } catch (e) {
              reject(e);
            }
          }, 5),
        ),
    },
    configurable: true,
  });
  Object.defineProperty(window, "scrollY", {
    value: 0,
    writable: true,
    configurable: true,
  });
  window.scrollTo = vi.fn((options?: ScrollToOptions | number, y?: number) => {
    const top = typeof options === "number" ? (y ?? 0) : (options?.top ?? 0);
    Object.defineProperty(window, "scrollY", {
      value: top,
      writable: true,
      configurable: true,
    });
  });
  window.confirm = vi.fn(() => true);
  URL.createObjectURL = vi.fn(() => "blob:receipt-preview");
  URL.revokeObjectURL = vi.fn();
});
afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});
const click = async (name: string | RegExp) =>
  fireEvent.click(await screen.findByRole("button", { name }));
const page = (route: string) => {
  window.history.replaceState(null, "", `#/${route}`);
  return render(App);
};
const saved = () => backend.state!;
async function readReceipt() {
  const input = await screen.findByLabelText("レシート画像を選ぶ");
  const file = new File(["receipt"], "receipt.png", { type: "image/png" });
  Object.defineProperty(file, "arrayBuffer", {
    value: async () => new TextEncoder().encode("receipt").buffer,
  });
  await fireEvent.change(input, { target: { files: [file] } });
  await click("読み取る");
}

describe("service flows through mounted Svelte UI (simulated DOM)", () => {
  it("selects full ingredient cards, keeps selected ingredients on return, and omits servings from search", async () => {
    page("home");
    await click("なすを選ぶ");
    await click("卵を選ぶ");
    await waitFor(() =>
      expect(
        screen.getByRole("button", { name: "この2つで探す" }),
      ).toBeTruthy(),
    );
    await click("この2つで探す");
    await waitFor(() =>
      expect(
        screen.getByRole("heading", { name: "こんな一品、どう？" }),
      ).toBeTruthy(),
    );
    expect(screen.queryByRole("spinbutton", { name: "人数" })).toBeNull();
    expect(
      screen.getByRole("button", { name: "なすと卵の醤油炒めを見る" }),
    ).toBeTruthy();
    await click("戻る");
    await waitFor(() =>
      expect(
        screen
          .getByRole("button", { name: "なすを外す" })
          .getAttribute("aria-pressed"),
      ).toBe("true"),
    );
  });
  it("restores list and home positions on screen back, while a new search starts at the top", async () => {
    page("home");
    await click("なすを選ぶ");
    await click("卵を選ぶ");
    await waitFor(() =>
      expect(saved().search.selectedFoodIds).toEqual(["eggplant", "egg"]),
    );
    Object.defineProperty(window, "scrollY", { value: 320, writable: true });
    await fireEvent.scroll(window);
    await click("この2つで探す");
    await screen.findByRole("heading", { name: "こんな一品、どう？" });
    await waitFor(() =>
      expect(window.scrollTo).toHaveBeenLastCalledWith({
        top: 0,
        behavior: "instant",
      }),
    );
    Object.defineProperty(window, "scrollY", { value: 680, writable: true });
    await fireEvent.scroll(window);
    await click("なすと卵の醤油炒めを見る");
    await screen.findByRole("heading", { name: "なすと卵の醤油炒め" });
    await click("戻る");
    await screen.findByRole("heading", { name: "こんな一品、どう？" });
    await waitFor(() =>
      expect(window.scrollTo).toHaveBeenLastCalledWith({
        top: 680,
        behavior: "instant",
      }),
    );
    expect(saved().search.selectedFoodIds).toEqual(["eggplant", "egg"]);
    await click("戻る");
    await screen.findByRole("heading", { name: "今日の一品、ここから。" });
    await waitFor(() =>
      expect(window.scrollTo).toHaveBeenLastCalledWith({
        top: 320,
        behavior: "instant",
      }),
    );
    await click("この2つで探す");
    await screen.findByRole("heading", { name: "こんな一品、どう？" });
    await waitFor(() =>
      expect(window.scrollTo).toHaveBeenLastCalledWith({
        top: 0,
        behavior: "instant",
      }),
    );
    Object.defineProperty(window, "scrollY", { value: 440, writable: true });
    await fireEvent.scroll(window);
    await click("条件");
    await click("この条件で探す");
    await waitFor(() => expect(screen.queryByRole("dialog")).toBeNull());
    await waitFor(() =>
      expect(window.scrollTo).toHaveBeenLastCalledWith({
        top: 0,
        behavior: "instant",
      }),
    );
  });
  it("restores the home origin of a random recipe and handles browser back without clearing selections", async () => {
    page("home");
    await click("なすを選ぶ");
    await waitFor(() =>
      expect(saved().search.selectedFoodIds).toEqual(["eggplant"]),
    );
    Object.defineProperty(window, "scrollY", { value: 520, writable: true });
    await fireEvent.scroll(window);
    await waitFor(() =>
      expect(document.querySelector(".discover .recipe-card")).not.toBeNull(),
    );
    const dish = document.querySelector<HTMLButtonElement>(
      ".discover .recipe-card",
    )!;
    await fireEvent.click(dish);
    await screen.findByRole("button", { name: "この料理を作る" });
    await click("戻る");
    await screen.findByRole("heading", { name: "今日の一品、ここから。" });
    await waitFor(() =>
      expect(window.scrollTo).toHaveBeenLastCalledWith({
        top: 520,
        behavior: "instant",
      }),
    );
    await click("この1つで探す");
    await screen.findByRole("heading", { name: "こんな一品、どう？" });
    Object.defineProperty(window, "scrollY", { value: 750, writable: true });
    await fireEvent.scroll(window);
    await click("なすと卵の醤油炒めを見る");
    await screen.findByRole("button", { name: "この料理を作る" });
    window.history.back();
    await screen.findByRole("heading", { name: "こんな一品、どう？" });
    await waitFor(() =>
      expect(window.scrollTo).toHaveBeenLastCalledWith({
        top: 750,
        behavior: "instant",
      }),
    );
    expect(saved().search.selectedFoodIds).toEqual(["eggplant"]);
  });
  it("starts a reloaded page at the top while retaining persisted search selections", async () => {
    const initial = createInitialState();
    initial.search.selectedFoodIds = ["eggplant", "egg"];
    backend.state = initial;
    Object.defineProperty(window, "scrollY", { value: 900, writable: true });
    page("results");
    await screen.findByRole("heading", { name: "こんな一品、どう？" });
    await waitFor(() =>
      expect(window.scrollTo).toHaveBeenLastCalledWith({
        top: 0,
        behavior: "instant",
      }),
    );
    expect(saved().search.selectedFoodIds).toEqual(["eggplant", "egg"]);
  });
  it("registers only selected recognized receipt foods, then reviews a duplicate without losing candidates", async () => {
    page("receipt");
    await readReceipt();
    await waitFor(() =>
      expect(
        screen.getByRole("button", { name: "この内容で登録" }),
      ).toBeTruthy(),
    );
    expect(saved().lots).toHaveLength(0);
    await click("この内容で登録");
    await waitFor(() => expect(saved().imports).toHaveLength(1));
    expect(saved().lots).toHaveLength(2);
    expect(saved().lots.every((l) => l.quantity.value === null)).toBe(true);
    await click("冷蔵庫");
    await waitFor(() =>
      expect(
        screen.getAllByRole("button", { name: "レシートから追加" })[0],
      ).toBeTruthy(),
    );
    await fireEvent.click(
      screen.getAllByRole("button", { name: "レシートから追加" })[0],
    );
    await readReceipt();
    await click("この内容で登録");
    await waitFor(() => expect(screen.getByRole("dialog")).toBeTruthy());
    await click("履歴を見る");
    expect(
      screen.getByText(
        "読み取り中の候補は保持しています。登録日時と食材を比べてください。",
      ),
    ).toBeTruthy();
    await click("読取内容の確認に戻る");
    expect(
      screen.getByRole("button", { name: "別の買い物として登録" }),
    ).toBeTruthy();
    expect(saved().imports).toHaveLength(1);
  });
  it("keeps corrected receipt names temporary until committing the receipt", async () => {
    page("receipt");
    await readReceipt();
    await click("食材を選ぶ");
    const dialog = screen.getByRole("dialog");
    const select = within(dialog).getByLabelText("食材");
    await fireEvent.change(select, { target: { value: "" } });
    await fireEvent.input(within(dialog).getByLabelText("新しい食材名"), {
      target: { value: "試用の野菜" },
    });
    await click("確認して戻る");
    expect(saved().customFoods).toHaveLength(0);
    expect(saved().lots).toHaveLength(0);
    await click("キャンセル");
    await click("破棄してやめる");
    await waitFor(() =>
      expect(
        screen.getByRole("heading", { name: "冷蔵庫に、何がある？" }),
      ).toBeTruthy(),
    );
    expect(saved().customFoods).toHaveLength(0);
    expect(saved().lots).toHaveLength(0);
  });
  it("starts cooking with the latest amount even while the quantity write is pending", async () => {
    page("detail/eggplant-egg");
    const amount = await screen.findByRole("spinbutton", { name: "なすの量" });
    await fireEvent.change(amount, { target: { value: "375" } });
    await click("この料理を作る");
    await waitFor(() =>
      expect(saved().cooking?.mealSnapshot[0].amounts.eggplant.value).toBe(375),
    );
    expect(saved().lots).toHaveLength(0);
  });
  it("reconstructs completion quantities on reload and leaves deduction unchecked", async () => {
    const initial = createInitialState();
    const started = startCooking(initial, [
      { ...getDraft(initial, "eggplant-egg"), id: "meal-test" },
    ]);
    backend.state = started;
    page("complete");
    await waitFor(() =>
      expect(
        screen.getByRole("spinbutton", { name: "なすの実使用量" }),
      ).toBeTruthy(),
    );
    expect(
      (
        screen.getByRole("checkbox", {
          name: /在庫から使用量を引く/,
        }) as HTMLInputElement
      ).checked,
    ).toBe(false);
    await click("完了");
    await waitFor(() => expect(saved().cooking?.status).toBe("completed"));
    expect(saved().cooking?.consumptionResults.every((r) => !r.applied)).toBe(
      true,
    );
    expect(saved().lots).toHaveLength(0);
  });
  it("persists settings safely and respects exclusions on the random dish", async () => {
    page("settings");
    await click("卵");
    await click("変更を保存");
    await waitFor(() =>
      expect(saved().settings.excludedFoodIds).toContain("egg"),
    );
    await click("ホーム");
    await waitFor(() =>
      expect(
        screen.getByRole("heading", { name: "今日の一品、ここから。" }),
      ).toBeTruthy(),
    );
    expect(
      screen.queryByRole("button", { name: "なすと卵の醤油炒めを見る" }),
    ).toBeNull();
    expect(
      screen.queryByRole("button", { name: "トマトと卵の炒めものを見る" }),
    ).toBeNull();
  });
  it("shows an equipment correction instead of throwing when the plan cannot use the selected tools", async () => {
    const initial = createInitialState();
    initial.meal = [{ ...getDraft(initial, "eggplant-egg"), id: "meal-1" }];
    initial.settings.equipment = [];
    backend.state = initial;
    page("plan");
    await waitFor(() =>
      expect(
        screen.getByRole("button", { name: "使う器具の設定を確認" }),
      ).toBeTruthy(),
    );
    expect(screen.queryByRole("button", { name: "調理を始める" })).toBeNull();
  });
  it("keeps server connectivity errors visible after route initialization", async () => {
    backend.failLoad = true;
    page("home");
    await waitFor(() =>
      expect(screen.getByText(/保存データを開けません/)).toBeTruthy(),
    );
    expect(localStorage.length).toBe(0);
  });
});
