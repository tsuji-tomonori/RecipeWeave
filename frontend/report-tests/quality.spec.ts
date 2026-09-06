import { test, expect, type Page, type TestInfo } from "@playwright/test";

async function step(page: Page, info: TestInfo, kind: string, description: string, action: () => Promise<void>) {
  await test.step(`${kind}: ${description}`, async () => {
    try { await action(); }
    finally {
      const path = info.outputPath(`${kind}-${info.attachments.length}.png`);
      await page.screenshot({ path, fullPage: false });
      await info.attach(`${kind}: ${description}`, { path, contentType: "image/png" });
    }
  });
}

test("品質レポートの分類とケース一覧から証跡画像を拡大できる", async ({ page }, info) => {
  await step(page, info, "Given", "生成済みの品質サマリーを開く", async () => {
    const response = await page.goto("./");
    expect(response?.status()).toBe(200);
    await expect(page.getByRole("navigation", { name: "レポートの分類" })).toBeVisible();
  });
  await step(page, info, "When", "E2E分類で操作の証跡画像を開く", async () => {
    await page.goto("./e2e.html");
    await expect(page.getByRole("navigation", { name: "テストケース一覧" })).toBeVisible();
    const image = page.locator("[data-screenshot]").first();
    await expect(image.locator("img")).toBeVisible();
    await image.click();
  });
  await step(page, info, "Then", "実行時の原寸画像がダイアログ内に表示される", async () => {
    const dialog = page.getByRole("dialog");
    await expect(dialog).toBeVisible();
    await expect.poll(async () => dialog.locator("img").evaluate((image: HTMLImageElement) => image.complete && image.naturalWidth > 0)).toBe(true);
    await expect(dialog.getByRole("link", { name: "原寸画像を開く" })).toHaveAttribute("href", /\.png$/);
    await dialog.getByRole("button", { name: "閉じる", exact: true }).click();
    await expect(dialog).not.toBeVisible();
  });
});

test("生成設計を全文検索し、関連するAPI仕様へ移動できる", async ({ page }, info) => {
  await step(page, info, "Given", "設計書サイトを開く", async () => {
    const response = await page.goto("./design/"); expect(response?.status()).toBe(200);
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  });
  await step(page, info, "When", "全文検索でレシピに関する設計を探す", async () => {
    await page.getByRole("button", { name: /検索/ }).first().click();
    await page.locator('input[type="search"]').fill("recipe");
    await expect(page.locator(".pagefind-ui__result-link").first()).toBeVisible();
  });
  await step(page, info, "Then", "検索結果から設計本文を開いて読める", async () => {
    await page.locator(".pagefind-ui__result-link").first().click();
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    await expect(page.locator(".sl-markdown-content")).not.toBeEmpty();
    expect(new URL(page.url()).pathname).toContain("/design/");
  });
});

test("ER図とAPIシーケンスがコード文字列ではなくSVGとして描画される", async ({ page }, info) => {
  await step(page, info, "Given", "生成されたテーブルのER図を開く", async () => {
    const response = await page.goto("./design/database/er/"); expect(response?.status()).toBe(200);
    await expect(page.locator(".mermaid").first()).toBeVisible();
  });
  await step(page, info, "Then", "ER図の全ブロックが描画され、エラー表示がない", async () => {
    await expect.poll(async () => page.locator(".mermaid svg").count()).toBe(await page.locator(".mermaid").count());
    await expect(page.locator('[data-render-error="true"]')).toHaveCount(0);
  });
  await step(page, info, "When", "実装から生成したAPIのシーケンスを開く", async () => {
    const response = await page.goto("./design/api/operations/get_health/sequence/"); expect(response?.status()).toBe(200);
    await expect(page.locator(".mermaid").first()).toBeVisible();
  });
  await step(page, info, "Then", "処理順序をSVGで読める", async () => {
    await expect.poll(async () => page.locator(".mermaid svg").count()).toBe(await page.locator(".mermaid").count());
    await expect(page.locator('[data-render-error="true"]')).toHaveCount(0);
  });
});
