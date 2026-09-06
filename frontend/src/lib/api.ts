import type {
  AppState,
  DurationEstimate,
  MealItem,
  PlannedStep,
  Food,
  Recipe,
  SearchFilters,
  ReceiptCommit,
  StockLot,
  ConsumptionRequest,
} from "./types";
import { cacheRecipes } from "./domain";
import { validateAppState } from "./persistence";
import { clearToken, getToken, setToken, localMode } from "./auth";
import type { BackupPreview } from "./backup";

export interface User {
  id: string;
  display_name: string;
  role: string;
}
export interface StateEnvelope {
  version: number;
  snapshot: AppState | null;
}
export interface RecipePage {
  items: Recipe[];
  total: number;
  offset: number;
  limit: number;
}
export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}
const API_ROOT =
  (import.meta.env.VITE_API_BASE_URL as string | undefined)?.replace(
    /\/$/,
    "",
  ) ?? "";

/** 失敗した更新を自動再送しない。重複登録や古い状態の上書きを防ぐ。 */
export async function request<T>(
  path: string,
  options: RequestInit = {},
  responseFormat: "json" | "text" = "json",
): Promise<T> {
  const headers = new Headers(options.headers);
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (options.body) headers.set("Content-Type", "application/json");
  let response: Response;
  try {
    response = await fetch(`${API_ROOT}${path}`, {
      ...options,
      headers,
      cache: "no-store",
      signal: options.signal ?? AbortSignal.timeout(20000),
    });
  } catch {
    throw new ApiError(
      0,
      "サーバーに接続できません。通信状態を確認して、再読み込みしてください。入力中の内容は保持しています。",
    );
  }
  if (getToken() !== token)
    throw new ApiError(
      409,
      "ログイン状態が変わったため、前の要求の結果は表示しません。",
    );
  if (!response.ok) {
    if (response.status === 401) {
      clearToken();
      throw new ApiError(
        401,
        path === "/api/auth/local-login"
          ? "ユーザー名またはパスワードが違います。"
          : "ログインの有効期限が切れました。もう一度ログインしてください。",
      );
    }
    if (response.status === 409 || response.status === 412)
      throw new ApiError(
        response.status,
        "ほかの画面で更新されています。最新の内容を読み込んでから、もう一度操作してください。",
      );
    const body = (await response.json().catch(() => ({}))) as {
      detail?: unknown;
      message?: unknown;
    };
    const detail =
      typeof body.detail === "string"
        ? body.detail
        : typeof body.message === "string"
          ? body.message
          : "";
    throw new ApiError(
      response.status,
      detail ||
        (response.status === 403
          ? "この操作を行う権限がありません。"
          : "処理を完了できませんでした。入力内容を確認してください。"),
    );
  }
  const result =
    response.status === 204
      ? undefined
      : responseFormat === "text"
        ? await response.text()
        : await response.json();
  if (getToken() !== token)
    throw new ApiError(
      409,
      "ログイン状態が変わったため、前の要求の結果は表示しません。",
    );
  return result as T;
}
export async function localLogin(
  username: string,
  password: string,
): Promise<User> {
  const result = await request<{ access_token: string; user: User }>(
    "/api/auth/local-login",
    {
      method: "POST",
      body: JSON.stringify({ username, password }),
    },
  );
  setToken(result.access_token);
  return result.user;
}
export async function currentUser(): Promise<User | null> {
  if (!getToken()) return null;
  return request<User>("/api/me");
}
export async function loadFoods(): Promise<Food[]> {
  const result = await request<{ items: Food[]; total: number }>("/api/foods");
  return result.items;
}
/** 試用データの要求は明示した配信環境と認証がそろう場合だけ。公開可否はAPIが判定する。 */
const requestCatalogPreview = (): boolean =>
  Boolean(getToken()) &&
  (localMode || import.meta.env.VITE_CATALOG_PREVIEW === "true");

export async function findRecipes(
  filters?: SearchFilters,
  excludedFoodIds: string[] = [],
  offset = 0,
): Promise<RecipePage> {
  const params = new URLSearchParams({ limit: "50", offset: String(offset) });
  if (requestCatalogPreview()) params.set("preview", "true");
  if (filters) {
    for (const id of filters.selectedFoodIds)
      params.append("selectedFoodIds", id);
    params.set("match", filters.match);
    if (filters.maxMinutes !== null)
      params.set("maxMinutes", String(filters.maxMinutes));
    for (const equipment of filters.equipment)
      params.append("equipment", equipment);
  }
  for (const id of excludedFoodIds) params.append("excludedFoodIds", id);
  const result = await request<RecipePage>(`/api/recipes?${params}`);
  cacheRecipes(result.items);
  return result;
}
export async function randomRecipe(
  excludedFoodIds: string[],
  previousId = "",
): Promise<Recipe | null> {
  const params = new URLSearchParams();
  if (requestCatalogPreview()) params.set("preview", "true");
  if (previousId) params.set("excludeId", previousId);
  for (const id of excludedFoodIds) params.append("excludedFoodIds", id);
  const response = await request<{ item: Recipe | null; total: number }>(
    `/api/recipes/random?${params}`,
  );
  // 候補ゼロも正常な応答。包みのオブジェクトを料理としてキャッシュしない。
  if (response.item) cacheRecipes([response.item]);
  return response.item;
}
export async function loadRecipe(
  id: string,
  versionId?: string,
): Promise<Recipe> {
  const params = new URLSearchParams();
  if (requestCatalogPreview()) params.set("preview", "true");
  if (versionId) params.set("versionId", versionId);
  const recipe = await request<Recipe>(
    `/api/recipes/${encodeURIComponent(id)}?${params}`,
  );
  cacheRecipes([recipe], !versionId);
  return recipe;
}
/** 献立・調理履歴は保存時の料理版で読み、現在版の分量や工程と混同しない。 */
async function hydrateWorkspace(snapshot: AppState): Promise<AppState> {
  const references = [
    ...snapshot.meal,
    ...Object.values(snapshot.drafts),
    ...(snapshot.cooking?.mealSnapshot ?? []),
  ];
  const keys = new Map(
    references.map((item) => [
      `${item.recipeId}:${item.recipeVersionId ?? ""}`,
      item,
    ]),
  );
  for (const recipeId of snapshot.saved)
    keys.set(recipeId, { recipeId, servings: 1, amounts: {}, adjusted: false });
  await Promise.all(
    [...keys.values()].map((item) =>
      loadRecipe(item.recipeId, item.recipeVersionId),
    ),
  );
  return validateAppState(snapshot);
}
export async function loadState(): Promise<AppState> {
  return hydrateWorkspace(await request<AppState>("/api/workspace"));
}
const same = (a: unknown, b: unknown): boolean =>
  JSON.stringify(a) === JSON.stringify(b);
const stockInput = (lot: StockLot) => ({
  foodId: lot.foodId,
  quantity: lot.quantity,
  form: lot.form,
  location: lot.location,
  priority: lot.priority,
  expiresOn: lot.expiresOn,
});

/** 一回のUI操作を業務APIへ変換する。成功したrevisionを次の操作へ渡す。 */
export async function saveState(
  current: AppState,
  next: AppState,
  durationEstimates: DurationEstimate[] = [],
): Promise<AppState> {
  let result = current;
  const mutate = async (path: string, method: string, body: object = {}) => {
    result = await request<AppState>(path, {
      method,
      body: JSON.stringify({ ...body, expectedVersion: result.version }),
    });
  };
  const newImports = next.imports.filter(
    (entry) => !current.imports.some((old) => old.id === entry.id),
  );
  if (newImports.length)
    throw new ApiError(422, "レシートは確認画面から登録してください。");
  for (const food of next.customFoods.filter(
    (item) => !current.customFoods.some((old) => old.id === item.id),
  ))
    await mutate("/api/foods/custom", "POST", { food });
  for (const entry of next.imports) {
    const old = current.imports.find((item) => item.id === entry.id);
    if (old?.state === "registered" && entry.state === "undone")
      await mutate(
        `/api/receipts/${encodeURIComponent(entry.id)}/undo`,
        "POST",
      );
  }
  for (const lot of next.lots) {
    if (lot.status === "undone") continue;
    const old = current.lots.find((item) => item.id === lot.id);
    if (!old)
      await mutate("/api/pantry-lots", "POST", {
        id: lot.id,
        ...stockInput(lot),
      });
    else if (!same(old, lot)) {
      if (lot.status === "deleted")
        await mutate(
          `/api/pantry-lots/${encodeURIComponent(lot.id)}`,
          "DELETE",
        );
      else
        await mutate(
          `/api/pantry-lots/${encodeURIComponent(lot.id)}`,
          "PATCH",
          { ...stockInput(lot), restore: old.status === "deleted" },
        );
    }
  }
  for (const item of current.meal.filter(
    (item) => !next.meal.some((value) => value.id === item.id),
  ))
    await mutate(
      `/api/menus/current/items/${encodeURIComponent(item.id)}`,
      "DELETE",
    );
  for (const item of next.meal) {
    const old = current.meal.find((value) => value.id === item.id);
    if (!old) await mutate("/api/menus/current/items", "POST", { item });
    else if (!same(old, item))
      await mutate(
        `/api/menus/current/items/${encodeURIComponent(item.id)}`,
        "PATCH",
        { item },
      );
  }
  for (const id of next.saved.filter((id) => !current.saved.includes(id)))
    await mutate(`/api/saved-recipes/${encodeURIComponent(id)}`, "PUT");
  for (const id of current.saved.filter((id) => !next.saved.includes(id)))
    await mutate(`/api/saved-recipes/${encodeURIComponent(id)}`, "DELETE");
  if (!same(current.settings, next.settings))
    await mutate("/api/settings", "PUT", { settings: next.settings });
  if (!same(current.shoppingChecks, next.shoppingChecks))
    await mutate("/api/shopping-checks", "PUT", {
      checks: next.shoppingChecks,
    });
  if (!same(current.cooking, next.cooking) && next.cooking)
    await mutate(
      current.cooking?.id === next.cooking.id
        ? `/api/cooking-sessions/${encodeURIComponent(next.cooking.id)}`
        : "/api/cooking-sessions",
      current.cooking?.id === next.cooking.id ? "PATCH" : "POST",
      {
        session: next.cooking,
        ...(current.cooking?.id !== next.cooking.id && durationEstimates.length
          ? { durationEstimates }
          : {}),
      },
    );
  // 検索条件と料理選択前の分量調整は、この画面だけの一時状態。
  return {
    ...(await hydrateWorkspace(result)),
    search: next.search,
    drafts: next.drafts,
  };
}
export async function completeCooking(
  current: AppState,
  deduct: boolean,
  consumption: ConsumptionRequest[],
): Promise<AppState> {
  if (!current.cooking) throw new ApiError(422, "進行中の調理がありません。");
  const result = await request<AppState>(
    `/api/cooking-sessions/${encodeURIComponent(current.cooking.id)}`,
    {
      method: "PATCH",
      body: JSON.stringify({
        expectedVersion: current.version,
        deduct,
        session: {
          ...current.cooking,
          status: "completed",
          completedStepIds: [
            ...new Set([
              ...current.cooking.completedStepIds,
              current.cooking.plan[current.cooking.index].key,
            ]),
          ],
          consumptionResults: consumption.map((item) => ({
            ...item,
            applied: false,
            reason: "利用者が入力した実使用量",
            lotIds: [],
          })),
        },
      }),
    },
  );
  return {
    ...(await hydrateWorkspace(result)),
    search: current.search,
    drafts: current.drafts,
  };
}
export async function commitReceipt(
  current: AppState,
  input: ReceiptCommit,
  customFoods: Food[],
): Promise<AppState> {
  const result = await request<AppState>("/api/receipts/commit", {
    method: "POST",
    body: JSON.stringify({
      ...input,
      // OCRの元の行や除外行はサーバーへ送らず、確認済みの食品と数量だけを渡す。
      candidates: input.candidates
        .filter((candidate) => candidate.selected)
        .map((candidate) => ({
          ...candidate,
          rawText: "",
          reason: "利用者確認済み",
        })),
      customFoods,
      expectedVersion: current.version,
    }),
  });
  return {
    ...(await hydrateWorkspace(result)),
    search: current.search,
    drafts: current.drafts,
  };
}

/** 調理開始と同じ規則で、書き込みを行わず段取りだけを確認する。 */
export async function previewCookingPlan(
  items: MealItem[],
  durationEstimates: DurationEstimate[] = [],
): Promise<{ plan: PlannedStep[] }> {
  return request("/api/cooking-plan", {
    method: "POST",
    body: JSON.stringify({ items, durationEstimates }),
  });
}

/** DBの数値精度を維持するため、バックアップだけは応答本文をそのまま保存する。 */
export async function exportDatabaseBackup(): Promise<string> {
  return request<string>("/api/backups/export", { method: "POST" }, "text");
}
export async function previewDatabaseBackup(
  backupText: string,
): Promise<BackupPreview> {
  return request("/api/backups/preview", {
    method: "POST",
    body: `{"backup":${backupText}}`,
  });
}
export async function restoreDatabaseBackup(
  backupText: string,
  preview: BackupPreview,
): Promise<AppState> {
  const confirmation = JSON.stringify({
    intentId: preview.intentId,
    expectedVersion: preview.expectedVersion,
    confirmed: true,
  });
  const result = await request<AppState>("/api/backups/restore", {
    method: "POST",
    body: `{"backup":${backupText},${confirmation.slice(1)}`,
  });
  return hydrateWorkspace(result);
}
