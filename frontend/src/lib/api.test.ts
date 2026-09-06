// @vitest-environment jsdom
import { beforeEach, afterEach, describe, expect, it, vi } from "vitest";
import {
  addStock,
  createInitialState,
  setCatalog,
  startCooking,
  getDraft,
} from "./domain";
import {
  ApiError,
  completeCooking,
  request,
  saveState,
  findRecipes,
  commitReceipt,
  loadState,
} from "./api";
import { getToken, setToken } from "./auth";
import { fixtureFoods, fixtureRecipes } from "../test-fixtures";
import { validateAppState } from "./persistence";

beforeEach(() => {
  sessionStorage.clear();
  setCatalog(fixtureFoods, fixtureRecipes);
});
afterEach(() => {
  vi.unstubAllGlobals();
});

describe("実APIへの要求と失敗時の扱い", () => {
  it("サーバーの待ち時間を含む工程計画を維持し、工程の重複や不正な時間は拒否する", () => {
    const state = startCooking(createInitialState(), [
      { ...getDraft(createInitialState(), "eggplant-egg"), id: "meal-1" },
    ]);
    state.cooking!.plan = state.cooking!.plan.map((step) => ({
      ...step,
      startMinute: step.startMinute + 5,
      endMinute: step.endMinute + 5,
    }));
    expect(validateAppState(state).cooking!.plan[0].startMinute).toBe(5);
    const duplicate = structuredClone(state);
    duplicate.cooking!.plan[1] = structuredClone(duplicate.cooking!.plan[0]);
    expect(() => validateAppState(duplicate)).toThrow();
    const invalid = structuredClone(state);
    invalid.cooking!.plan[0].endMinute = -1;
    expect(() => validateAppState(invalid)).toThrow();
  });
  it("献立の履歴を復元するときは保存時の料理版を明示して取得する", async () => {
    const historical = structuredClone(fixtureRecipes[0]);
    historical.versionId = "historical-version";
    setCatalog(fixtureFoods, [historical]);
    const state = createInitialState();
    state.meal = [{ ...getDraft(state, historical.id), id: "saved-item" }];
    const current = structuredClone(historical);
    current.versionId = "current-version";
    current.ingredients[0].quantity.value = 999;
    setCatalog(fixtureFoods, [current]);
    const fetcher = vi.fn(
      async (input: string) =>
        new Response(
          JSON.stringify(input === "/api/workspace" ? state : historical),
        ),
    );
    vi.stubGlobal("fetch", fetcher);
    const restored = await loadState();
    expect(restored.meal[0].recipeVersionId).toBe("historical-version");
    const detailUrl = new URL(fetcher.mock.calls[1][0], "http://localhost");
    expect(detailUrl.searchParams.get("versionId")).toBe("historical-version");
  });
  it("在庫の追加では専用APIへ必要な入力とrevisionを送り、全状態をPUTしない", async () => {
    const initial = createInitialState();
    const next = addStock(
      initial,
      { foodId: "eggplant", quantity: { value: null, unit: "g" } },
      "lot-1",
    );
    const fetcher = vi.fn(
      async (_input: RequestInfo | URL, _init?: RequestInit) =>
        new Response(JSON.stringify({ ...next, version: 1 }), { status: 201 }),
    );
    vi.stubGlobal("fetch", fetcher);
    setToken("test-token");
    const saved = await saveState(initial, next);
    expect(saved.version).toBe(1);
    expect(fetcher).toHaveBeenCalledTimes(1);
    expect(fetcher.mock.calls[0]?.[0]).toBe("/api/pantry-lots");
    const options = fetcher.mock.calls[0]?.[1] as RequestInit;
    expect(options.method).toBe("POST");
    expect(JSON.parse(options.body as string)).toEqual({
      expectedVersion: 0,
      id: "lot-1",
      foodId: "eggplant",
      quantity: { value: null, unit: "g" },
      form: "標準",
      location: "冷蔵",
      priority: false,
      expiresOn: null,
    });
    expect(new Headers(options.headers).get("Authorization")).toBe(
      "Bearer test-token",
    );
  });

  it("検索と分量の一時編集ではDB更新要求を送らない", async () => {
    const state = createInitialState();
    const fetcher = vi.fn();
    vi.stubGlobal("fetch", fetcher);
    const result = await saveState(state, {
      ...state,
      search: { ...state.search, selectedFoodIds: ["eggplant"] },
    });
    expect(result.search.selectedFoodIds).toEqual(["eggplant"]);
    expect(fetcher).not.toHaveBeenCalled();
  });

  it("競合した登録は自動再送せず、変更前の入力を変更しない", async () => {
    const state = createInitialState();
    const next = addStock(state, {
      foodId: "eggplant",
      quantity: { value: 300, unit: "g" },
    });
    const fetcher = vi.fn(
      async (_input: RequestInfo | URL, _init?: RequestInit) =>
        new Response("{}", { status: 409 }),
    );
    vi.stubGlobal("fetch", fetcher);
    await expect(saveState(state, next)).rejects.toMatchObject({ status: 409 });
    expect(fetcher).toHaveBeenCalledTimes(1);
    expect(state.lots).toHaveLength(0);
    expect(next.lots[0].quantity.value).toBe(300);
  });

  it("要求中に利用者が変わったら古い結果を捨て、新しい認証を消さない", async () => {
    for (const duringBody of [false, true]) {
      setToken("alice-token");
      vi.stubGlobal(
        "fetch",
        vi.fn(async () => {
          const response = new Response(
            JSON.stringify({ privateValue: "alice" }),
          );
          if (duringBody)
            vi.spyOn(response, "json").mockImplementation(async () => {
              setToken("bob-token");
              return { privateValue: "alice" };
            });
          else setToken("bob-token");
          return response;
        }),
      );
      await expect(request("/api/workspace")).rejects.toMatchObject({
        status: 409,
      });
      expect(getToken()).toBe("bob-token");
    }
  });

  it("401では失効した認証を破棄し、通信失敗と区別する", async () => {
    setToken("expired");
    vi.stubGlobal(
      "fetch",
      vi.fn(
        async (_input: RequestInfo | URL, _init?: RequestInit) =>
          new Response("{}", { status: 401 }),
      ),
    );
    await expect(request("/api/me")).rejects.toMatchObject({ status: 401 });
    expect(getToken()).toBeNull();
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => {
        throw new TypeError("offline");
      }),
    );
    await expect(request("/api/workspace")).rejects.toBeInstanceOf(ApiError);
    await expect(request("/api/workspace")).rejects.toMatchObject({
      status: 0,
    });
  });

  it("食材検索のAPIパラメータに人数を入れず、ページ位置を送る", async () => {
    const fetcher = vi.fn(
      async (_input: RequestInfo | URL, _init?: RequestInit) =>
        new Response(
          JSON.stringify({ items: [], total: 300, offset: 50, limit: 50 }),
        ),
    );
    vi.stubGlobal("fetch", fetcher);
    await findRecipes(
      {
        ...createInitialState().search,
        selectedFoodIds: ["eggplant", "egg"],
        maxMinutes: 15,
      },
      ["milk"],
      50,
    );
    const url = new URL(
      fetcher.mock.calls[0]?.[0] as string,
      "http://localhost",
    );
    expect(url.searchParams.getAll("selectedFoodIds")).toEqual([
      "eggplant",
      "egg",
    ]);
    expect(url.searchParams.get("offset")).toBe("50");
    expect(url.searchParams.has("servings")).toBe(false);
  });

  it("レシート登録は候補・追加食品を単一の確定APIへ渡す", async () => {
    const state = createInitialState();
    const fetcher = vi.fn(
      async (_input: RequestInfo | URL, _init?: RequestInit) =>
        new Response(JSON.stringify(state)),
    );
    vi.stubGlobal("fetch", fetcher);
    await commitReceipt(
      state,
      {
        id: "receipt-1",
        imageHash: "a".repeat(64),
        purchaseSignature: "b".repeat(64),
        allowDuplicate: false,
        candidates: [
          {
            id: "selected",
            foodId: "tofu",
            quantity: { value: 300, unit: "g" },
            selected: true,
            status: "matched",
            rawText: "豆腐300g 店舗電話0123456789",
            reason: "OCR候補",
          },
          {
            id: "excluded",
            foodId: null,
            quantity: { value: null, unit: "g" },
            selected: false,
            status: "excluded",
            rawText: "カード番号123456",
            reason: "対象外",
          },
        ],
      },
      [],
    );
    expect(fetcher).toHaveBeenCalledTimes(1);
    expect(fetcher.mock.calls[0]?.[0]).toBe("/api/receipts/commit");
    const body = JSON.parse(fetcher.mock.calls[0]?.[1]?.body as string);
    expect(body.candidates).toHaveLength(1);
    expect(body.candidates[0].rawText).toBe("");
    expect(JSON.stringify(body)).not.toContain("123456");
  });

  it("調理完了で在庫を個別更新せず、明示的な使用量控除を一回だけ要求する", async () => {
    const state = startCooking(createInitialState(), [
      { ...getDraft(createInitialState(), "eggplant-egg"), id: "meal-1" },
    ]);
    const fetcher = vi.fn(
      async (url: string, _init?: RequestInit) =>
        new Response(
          JSON.stringify(
            url.includes("/api/recipes/")
              ? fixtureRecipes.find((recipe) => recipe.id === "eggplant-egg")
              : state,
          ),
        ),
    );
    vi.stubGlobal("fetch", fetcher);
    await completeCooking(state, true, [
      { foodId: "eggplant", form: "標準", quantity: { value: 170, unit: "g" } },
    ]);
    expect(
      fetcher.mock.calls
        .map(([url]) => url)
        .some((url) => url.includes("pantry-lots")),
    ).toBe(false);
    const options = fetcher.mock.calls[0]?.[1] as RequestInit;
    expect(JSON.parse(options.body as string).deduct).toBe(true);
    expect(
      JSON.parse(options.body as string).session.consumptionResults[0].quantity
        .value,
    ).toBe(170);
  });
});
