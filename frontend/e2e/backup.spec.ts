import { login as loginUser } from "./login";
import { test, expect, type Page, type TestInfo } from "@playwright/test";
import type { AppState } from "../src/lib/types";

async function step(
  page: Page,
  info: TestInfo,
  kind: string,
  description: string,
  action: () => Promise<void>,
) {
  await test.step(`${kind}: ${description}`, async () => {
    let failed = false;
    try {
      await action();
    } catch (cause) {
      failed = true;
      throw cause;
    } finally {
      try {
        const path = info.outputPath(`${kind}-${info.attachments.length}.png`);
        await page.screenshot({ path, fullPage: false, timeout: 5000 });
        await info.attach(`${kind}: ${description}`, {
          path,
          contentType: "image/png",
        });
      } catch (cause) {
        info.annotations.push({
          type: "証跡取得失敗",
          description: String(cause),
        });
        if (!failed) throw cause;
      }
    }
  });
}
async function workspace(page: Page): Promise<AppState> {
  return page.evaluate(async () => {
    const response = await fetch("/api/workspace", {
      headers: {
        Authorization: `Bearer ${sessionStorage.getItem("recipeweave.access-token")}`,
      },
    });
    if (!response.ok) throw new Error(`workspace ${response.status}`);
    return response.json();
  });
}
async function addStock(page: Page, amount: string) {
  await page.getByRole("button", { name: "冷蔵庫", exact: true }).click();
  await page.getByRole("button", { name: "手入力で追加", exact: true }).click();
  const dialog = page.getByRole("dialog");
  await dialog
    .getByLabel("食材", { exact: true })
    .selectOption({ label: "なす" });
  await dialog.getByLabel("数量（空欄は数量不明）").fill(amount);
  await dialog.getByLabel("単位", { exact: true }).selectOption("g");
  await dialog.getByRole("button", { name: "登録する", exact: true }).click();
  await expect(dialog).not.toBeVisible();
}
async function exportFile(page: Page, info: TestInfo): Promise<string> {
  await page.getByRole("button", { name: "設定", exact: true }).click();
  const downloadPromise = page.waitForEvent("download");
  await page
    .getByRole("button", { name: "データを書き出す", exact: true })
    .click();
  const download = await downloadPromise;
  const path = info.outputPath("issued-backup-v2.json");
  await download.saveAs(path);
  return path;
}
async function previewFile(page: Page, path: string) {
  await page.getByRole("button", { name: "設定", exact: true }).click();
  await page
    .getByLabel("復元するバックアップファイル", { exact: true })
    .setInputFiles(path);
  await expect(
    page.getByRole("heading", { name: "復元する内容を確認" }),
  ).toBeVisible();
  await expect(
    page.getByRole("table", { name: "復元するデータの件数" }),
  ).toBeVisible();
}

// バックアップ試験にはBobを使い、Aliceの調理・レシートの進行状態から独立させる。
test("最新DBから書き出したバックアップを確認して全置換し、別タブでも復元結果を読む", async ({
  page,
  context,
}, info) => {
  let backup = "";
  let expected: AppState;
  await step(
    page,
    info,
    "Given",
    "本人の在庫を保存し最新バックアップを書き出す",
    async () => {
      await loginUser(page, "bob");
      await addStock(page, "613");
      expected = await workspace(page);
      backup = await exportFile(page, info);
    },
  );
  await step(
    page,
    info,
    "When",
    "在庫を追加変更してから復元対象と件数を確認する",
    async () => {
      await addStock(page, "127");
      expect((await workspace(page)).lots.length).toBe(
        expected.lots.length + 1,
      );
      await previewFile(page, backup);
      await expect(page.getByText(/保持する対象：/)).toBeVisible();
      await page
        .getByRole("button", { name: "確認して次へ", exact: true })
        .click();
      await expect(
        page.getByRole("heading", { name: "現在のデータを置き換えますか？" }),
      ).toBeVisible();
    },
  );
  await step(
    page,
    info,
    "Then",
    "最終確認後は書き出した在庫だけに戻り、別タブにも同じ内容が出る",
    async () => {
      await page
        .getByRole("button", { name: "全置換して復元", exact: true })
        .click();
      await expect(page.getByRole("dialog")).not.toBeVisible({
        timeout: 30000,
      });
      const restored = await workspace(page);
      expect(
        restored.lots.map((lot) => [
          lot.id,
          lot.foodId,
          lot.quantity,
          lot.status,
        ]),
      ).toEqual(
        expected.lots.map((lot) => [
          lot.id,
          lot.foodId,
          lot.quantity,
          lot.status,
        ]),
      );
      const other = await context.newPage();
      try {
        await loginUser(other, "bob");
        expect((await workspace(other)).lots).toEqual(restored.lots);
      } finally {
        await other.close();
      }
    },
  );
});

test("復元確認のキャンセルと旧形式ファイルでは保存済みデータを変えない", async ({
  page,
}, info) => {
  let before: AppState;
  let backup = "";
  await step(
    page,
    info,
    "Given",
    "本人のバックアップと現在データを確認する",
    async () => {
      await loginUser(page, "bob");
      before = await workspace(page);
      backup = await exportFile(page, info);
      await previewFile(page, backup);
    },
  );
  await step(
    page,
    info,
    "When",
    "最終確認へ進んでからキャンセルする",
    async () => {
      await page
        .getByRole("button", { name: "確認して次へ", exact: true })
        .click();
      await page
        .getByRole("dialog")
        .getByRole("button", { name: "キャンセル", exact: true })
        .click();
      await expect(page.getByRole("dialog")).not.toBeVisible();
      expect(await workspace(page)).toEqual(before);
    },
  );
  await step(
    page,
    info,
    "Then",
    "旧ブラウザ形式も拒否され、復元前の内容を保持する",
    async () => {
      await page
        .getByLabel("復元するバックアップファイル", { exact: true })
        .setInputFiles({
          name: "legacy.json",
          mimeType: "application/json",
          buffer: Buffer.from('{"schemaVersion":1}'),
        });
      await expect(page.getByRole("alert")).toContainText("旧ブラウザ保存形式");
      expect(await workspace(page)).toEqual(before);
    },
  );
});

test("復元確認後に別の変更が入ったら全置換せず、内容を再確認する", async ({
  page,
}, info) => {
  let backup = "";
  let latest: AppState;
  await step(
    page,
    info,
    "Given",
    "最新バックアップの復元内容を確認する",
    async () => {
      await loginUser(page, "bob");
      backup = await exportFile(page, info);
      await previewFile(page, backup);
      await page
        .getByRole("button", { name: "確認して次へ", exact: true })
        .click();
    },
  );
  await step(
    page,
    info,
    "When",
    "別の操作でデータの版が進んだあと復元を確定する",
    async () => {
      const before = await workspace(page);
      const responseStatus = await page.evaluate(async (state) => {
        const response = await fetch("/api/settings", {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("recipeweave.access-token")}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            expectedVersion: state.version,
            settings: state.settings,
          }),
        });
        return response.status;
      }, before);
      expect(responseStatus).toBe(200);
      latest = await workspace(page);
      await page
        .getByRole("button", { name: "全置換して復元", exact: true })
        .click();
      await expect(page.getByRole("alert")).toContainText("更新されています");
    },
  );
  await step(
    page,
    info,
    "Then",
    "新しい版を上書きせず、確認を取り直してからキャンセルできる",
    async () => {
      expect(await workspace(page)).toEqual(latest);
      await page
        .getByRole("button", { name: "内容を再確認", exact: true })
        .click();
      await expect(
        page.getByRole("table", { name: "復元するデータの件数" }),
      ).toBeVisible();
      await page
        .getByRole("button", { name: "キャンセル", exact: true })
        .click();
      expect(await workspace(page)).toEqual(latest);
    },
  );
});
