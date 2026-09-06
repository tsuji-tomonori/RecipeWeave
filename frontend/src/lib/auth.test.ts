// @vitest-environment jsdom
import { afterEach, beforeEach, expect, it, vi } from "vitest";

beforeEach(() => {
  sessionStorage.clear();
  vi.resetModules();
  vi.stubEnv("VITE_COGNITO_DOMAIN", "login.example.invalid");
  vi.stubEnv("VITE_COGNITO_CLIENT_ID", "test-client");
  vi.stubEnv("BASE_URL", "/RecipeWeave/");
});
afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
});

it("OAuthのstateが一致しない応答を拒否し、認証コードをURLに残さない", async () => {
  history.replaceState(null, "", "/RecipeWeave/?code=untrusted&state=other");
  sessionStorage.setItem("recipeweave.pkce", "test-verifier");
  sessionStorage.setItem("recipeweave.oauth-state", "expected");
  const fetcher = vi.fn();
  vi.stubGlobal("fetch", fetcher);
  const { completeLogin, getToken } = await import("./auth");
  await expect(completeLogin()).rejects.toThrow("ログイン状態を確認できません");
  expect(fetcher).not.toHaveBeenCalled();
  expect(location.search).toBe("");
  expect(sessionStorage.getItem("recipeweave.pkce")).toBeNull();
  expect(getToken()).toBeNull();
});

it("PKCEで認証コードを交換し、Pagesのプロジェクトパスを維持する", async () => {
  history.replaceState(null, "", "/RecipeWeave/?code=test-code&state=expected");
  sessionStorage.setItem("recipeweave.pkce", "test-verifier");
  sessionStorage.setItem("recipeweave.oauth-state", "expected");
  const fetcher = vi.fn(
    async (_input: RequestInfo | URL, _init?: RequestInit) =>
      new Response(JSON.stringify({ access_token: "test-access" })),
  );
  vi.stubGlobal("fetch", fetcher);
  const { completeLogin, getToken } = await import("./auth");
  await completeLogin();
  const body = fetcher.mock.calls[0][1]!.body as URLSearchParams;
  expect(body.get("code_verifier")).toBe("test-verifier");
  expect(body.get("redirect_uri")).toBe(`${location.origin}/RecipeWeave/`);
  expect(getToken()).toBe("test-access");
  expect(location.pathname).toBe("/RecipeWeave/");
});
