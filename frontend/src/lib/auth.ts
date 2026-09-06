/** 認証トークンのみをタブ内に保持し、食材・在庫・献立は保存しない。 */
const TOKEN_KEY = "recipeweave.access-token";
const PKCE_KEY = "recipeweave.pkce";
const STATE_KEY = "recipeweave.oauth-state";
const domain = import.meta.env.VITE_COGNITO_DOMAIN as string | undefined;
const clientId = import.meta.env.VITE_COGNITO_CLIENT_ID as string | undefined;
export const localMode = import.meta.env.VITE_AUTH_MODE === "local";
const base64url = (bytes: Uint8Array): string =>
  btoa(String.fromCharCode(...bytes))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
export const getToken = (): string | null => sessionStorage.getItem(TOKEN_KEY);
export const setToken = (token: string): void =>
  sessionStorage.setItem(TOKEN_KEY, token);
export const clearToken = (): void => sessionStorage.removeItem(TOKEN_KEY);
const redirectUri = (): string =>
  new URL(import.meta.env.BASE_URL, location.origin + location.pathname).href;

export async function loginCognito(): Promise<void> {
  if (!domain || !clientId)
    throw new Error(
      "ログインの接続設定がありません。管理者に連絡してください。",
    );
  const verifier = base64url(crypto.getRandomValues(new Uint8Array(32)));
  const state = base64url(crypto.getRandomValues(new Uint8Array(24)));
  sessionStorage.setItem(PKCE_KEY, verifier);
  sessionStorage.setItem(STATE_KEY, state);
  const challenge = base64url(
    new Uint8Array(
      await crypto.subtle.digest("SHA-256", new TextEncoder().encode(verifier)),
    ),
  );
  location.assign(
    `https://${domain}/oauth2/authorize?${new URLSearchParams({
      client_id: clientId,
      response_type: "code",
      scope: "openid email profile",
      redirect_uri: redirectUri(),
      state,
      code_challenge: challenge,
      code_challenge_method: "S256",
    })}`,
  );
}

export async function completeLogin(): Promise<void> {
  const params = new URLSearchParams(location.search);
  if (!params.has("code") && !params.has("error")) return;
  const verifier = sessionStorage.getItem(PKCE_KEY);
  const state = sessionStorage.getItem(STATE_KEY);
  sessionStorage.removeItem(PKCE_KEY);
  sessionStorage.removeItem(STATE_KEY);
  const callback = redirectUri();
  history.replaceState(null, "", `${location.pathname}${location.hash}`);
  if (params.has("error"))
    throw new Error("ログインを完了できませんでした。もう一度お試しください。");
  if (
    !domain ||
    !clientId ||
    !verifier ||
    !state ||
    params.get("state") !== state
  )
    throw new Error(
      "ログイン状態を確認できません。もう一度ログインしてください。",
    );
  const response = await fetch(`https://${domain}/oauth2/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      client_id: clientId,
      code: params.get("code")!,
      redirect_uri: callback,
      code_verifier: verifier,
    }),
  });
  if (!response.ok)
    throw new Error("ログインに失敗しました。もう一度お試しください。");
  const result = (await response.json()) as { access_token?: string };
  if (!result.access_token)
    throw new Error("認証サーバーからトークンを受け取れませんでした。");
  setToken(result.access_token);
}

export function logout(): void {
  clearToken();
  if (!localMode && domain && clientId)
    location.assign(
      `https://${domain}/logout?${new URLSearchParams({ client_id: clientId, logout_uri: redirectUri() })}`,
    );
}
