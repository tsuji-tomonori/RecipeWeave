import { expect, test, type Page } from "@playwright/test";

/** CI専用の合成利用者でログインし、失敗時はトークンを除いた画面・API診断を残す。 */
export async function login(page: Page, username = "alice") {
  await page.goto("/#/login");
  await page.getByLabel("ユーザー名", { exact: true }).fill(username);
  await page
    .getByLabel("パスワード", { exact: true })
    .fill("recipeweave-local");
  await page
    .locator("form")
    .getByRole("button", { name: "ログイン", exact: true })
    .click();
  try {
    const logout = page.getByRole("button", { name: "ログアウト" });
    await expect(logout).toBeVisible();
    // 認証だけでなく、本人の在庫・料理カタログの読取が終わるまで待つ。
    await expect(logout).toBeEnabled({ timeout: 30000 });
    await expect(
      page.getByRole("heading", { name: "今日の一品、ここから。" }),
    ).toBeVisible();
  } catch (cause) {
    try {
      const alerts = await page.getByRole("alert").allTextContents();
      const state = await page.evaluate(async () => {
        try {
          const response = await fetch("/api/workspace", {
            headers: {
              Authorization: `Bearer ${sessionStorage.getItem("recipeweave.access-token")}`,
            },
            signal: AbortSignal.timeout(10000),
          });
          return { status: response.status, body: await response.text() };
        } catch (error) {
          return { error: String(error) };
        }
      });
      const diagnostic = JSON.stringify(
        { username, route: new URL(page.url()).hash, alerts, workspace: state },
        null,
        2,
      );
      console.error("ログイン後の画面診断（合成データ）", diagnostic);
      await test
        .info()
        .attach("ログイン後の画面・API診断", {
          body: diagnostic,
          contentType: "application/json",
        });
    } catch (diagnosticError) {
      console.error("ログイン診断の取得失敗", String(diagnosticError));
    }
    throw cause;
  }
}
