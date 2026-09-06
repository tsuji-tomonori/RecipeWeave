import { test, expect, type Page, type TestInfo } from "@playwright/test";

async function step(
  page: Page,
  info: TestInfo,
  kind: string,
  description: string,
  action: () => Promise<void>,
) {
  await test.step(`${kind}: ${description}`, async () => {
    let actionFailed = false;
    try {
      await action();
    } catch (cause) {
      actionFailed = true;
      throw cause;
    } finally {
      try {
        if (page.isClosed())
          throw new Error("証跡撮影前にページが閉じられました。");
        const path = info.outputPath(`${kind}-${info.attachments.length}.png`);
        await page.screenshot({ path, fullPage: false, timeout: 5000 });
        await info.attach(`${kind}: ${description}`, {
          path,
          contentType: "image/png",
        });
      } catch (captureError) {
        info.annotations.push({
          type: "証跡取得失敗",
          description:
            captureError instanceof Error
              ? captureError.message
              : String(captureError),
        });
        // 操作が先に失敗した場合、その原因を撮影エラーで置き換えない。
        if (!actionFailed) throw captureError;
      }
    }
  });
}

test("品質レポートの分類とケース一覧から証跡画像を拡大できる", async ({
  page,
}, info) => {
  await step(page, info, "Given", "生成済みの品質サマリーを開く", async () => {
    const response = await page.goto("./");
    expect(response?.status()).toBe(200);
    await expect(
      page.getByRole("navigation", { name: "レポートの分類" }),
    ).toBeVisible();
  });
  await step(page, info, "When", "E2E分類で操作の証跡画像を開く", async () => {
    await page.goto("./e2e.html");
    await expect(
      page.getByRole("navigation", { name: "テストケース一覧" }),
    ).toBeVisible();
    const image = page.locator("[data-screenshot]").first();
    await expect(image.locator("img")).toBeVisible();
    await image.click();
  });
  await step(
    page,
    info,
    "Then",
    "実行時の原寸画像がダイアログ内に表示される",
    async () => {
      const dialog = page.getByRole("dialog");
      await expect(dialog).toBeVisible();
      await expect
        .poll(async () =>
          dialog
            .locator("img")
            .evaluate(
              (image: HTMLImageElement) =>
                image.complete && image.naturalWidth > 0,
            ),
        )
        .toBe(true);
      await expect(
        dialog.getByRole("link", { name: "原寸画像を開く" }),
      ).toHaveAttribute("href", /\.png$/);
      await dialog.getByRole("button", { name: "閉じる", exact: true }).click();
      await expect(dialog).not.toBeVisible();
    },
  );
});

test("生成設計を全文検索し、関連するAPI仕様へ移動できる", async ({
  page,
}, info) => {
  await step(page, info, "Given", "設計書サイトを開く", async () => {
    const response = await page.goto("./design/");
    expect(response?.status()).toBe(200);
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  });
  await step(
    page,
    info,
    "When",
    "全文検索でレシピに関する設計を探す",
    async () => {
      const search = page.locator("site-search");
      const open = search.getByRole("button", { name: "検索", exact: true });
      await expect(open).toBeEnabled();
      await open.click();
      const dialog = search.getByRole("dialog", { name: "検索", exact: true });
      await expect(dialog).toBeVisible();
      // Pagefind UI は type=text の入力を生成する。実際の検索コンポーネントへ限定する。
      const input = dialog.locator("input.pagefind-ui__search-input");
      await expect(input).toBeVisible({ timeout: 15000 });
      await input.fill("recipe");
      await expect(
        dialog.locator(".pagefind-ui__result-link").first(),
      ).toBeVisible({ timeout: 15000 });
    },
  );
  await step(
    page,
    info,
    "Then",
    "検索結果から設計本文を開いて読める",
    async () => {
      await page.locator(".pagefind-ui__result-link").first().click();
      await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
      await expect(page.locator(".sl-markdown-content")).not.toBeEmpty();
      expect(new URL(page.url()).pathname).toContain("/design/");
    },
  );
});

test("ER図とAPIシーケンスがコード文字列ではなくSVGとして描画される", async ({
  page,
}, info) => {
  await step(
    page,
    info,
    "Given",
    "生成されたテーブルのER図を開く",
    async () => {
      const response = await page.goto("./design/database/er/");
      expect(response?.status()).toBe(200);
      await expect(page.locator(".mermaid").first()).toBeVisible();
    },
  );
  await step(
    page,
    info,
    "Then",
    "ER図の全ブロックが描画され、エラー表示がない",
    async () => {
      await expect
        .poll(async () => page.locator(".mermaid svg").count())
        .toBe(await page.locator(".mermaid").count());
      await expect(page.locator('[data-render-error="true"]')).toHaveCount(0);
    },
  );
  await step(
    page,
    info,
    "When",
    "実装から生成したAPIのシーケンスを開く",
    async () => {
      const response = await page.goto(
        "./design/api/operations/get_health/sequence/",
      );
      expect(response?.status()).toBe(200);
      await expect(page.locator(".mermaid").first()).toBeVisible();
    },
  );
  await step(page, info, "Then", "処理順序をSVGで読める", async () => {
    await expect
      .poll(async () => page.locator(".mermaid svg").count())
      .toBe(await page.locator(".mermaid").count());
    await expect(page.locator('[data-render-error="true"]')).toHaveCount(0);
  });
});
