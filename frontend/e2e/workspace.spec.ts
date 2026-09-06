import { test, expect, type Page, type TestInfo } from "@playwright/test";
import type { AppState } from "../src/lib/types";

/** 条件・操作・期待結果を、同じ実行のスクリーンショットと対応させる。 */
async function step(
  page: Page,
  info: TestInfo,
  kind: "Given" | "When" | "Then",
  description: string,
  action: () => Promise<void>,
) {
  await test.step(`${kind}: ${description}`, async () => {
    try {
      await action();
    } finally {
      if (!page.isClosed()) {
        const path = info.outputPath(`${kind}-${info.attachments.length}.png`);
        await page.screenshot({ path, fullPage: true });
        await info.attach(`${kind}: ${description}`, {
          path,
          contentType: "image/png",
        });
      }
    }
  });
}

async function login(page: Page, username = "alice") {
  await page.goto("/#/login");
  await page.getByLabel("ユーザー名", { exact: true }).fill(username);
  await page
    .getByLabel("パスワード", { exact: true })
    .fill("recipeweave-local");
  await page
    .locator("form")
    .getByRole("button", { name: "ログイン", exact: true })
    .click();
  await expect(page.getByRole("button", { name: "ログアウト" })).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "今日の一品、ここから。" }),
  ).toBeVisible();
}

async function workspace(page: Page): Promise<AppState> {
  return page.evaluate(async () => {
    const token = sessionStorage.getItem("recipeweave.access-token");
    const response = await fetch("/api/workspace", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) throw new Error(`workspace: ${response.status}`);
    return response.json();
  });
}

async function selectFood(page: Page, name: string) {
  await page.getByRole("button", { name: "食材をもっと見る" }).click();
  await page.getByLabel("食材名", { exact: true }).fill(name);
  await page
    .getByRole("button", { name: `${name}を選ぶ`, exact: true })
    .click();
}

async function addPantry(page: Page, amount: string) {
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

/** 個人情報を含まない検査用のレシート画像を作り、実際のOCRへ渡す。 */
async function recognizeTestReceipt(page: Page, marker: string) {
  await page.getByRole("button", { name: "冷蔵庫", exact: true }).click();
  await page
    .getByRole("button", { name: "レシートから追加", exact: true })
    .first()
    .click();
  const image = await page.evaluate((text) => {
    const canvas = document.createElement("canvas");
    canvas.width = 1000;
    canvas.height = 620;
    const context = canvas.getContext("2d")!;
    context.fillStyle = "white";
    context.fillRect(0, 0, 1000, 620);
    context.fillStyle = "black";
    context.font = '52px "Noto Sans CJK JP", sans-serif';
    [
      "食品レシート",
      "なす 200g 198円",
      "トマト 300g 298円",
      "合計 496円",
      text,
    ].forEach((line, index) => context.fillText(line, 60, 95 + index * 105));
    return canvas.toDataURL("image/png").split(",")[1];
  }, marker);
  await page.getByLabel("レシート画像を選ぶ", { exact: true }).setInputFiles({
    name: "receipt-test.png",
    mimeType: "image/png",
    buffer: Buffer.from(image, "base64"),
  });
  await page.getByRole("button", { name: "読み取る", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "この内容で登録", exact: true }),
  ).toBeVisible({ timeout: 65000 });
}

test("ログインして実DBの食材を選び、料理の分量を変えて献立・買物・調理へ進む", async ({
  page,
}, info) => {
  await step(
    page,
    info,
    "Given",
    "ログインして食材の選択画面を開く",
    async () => {
      await login(page);
      await selectFood(page, "なす");
      await expect(
        page.getByRole("button", { name: "なすを外す" }),
      ).toHaveAttribute("aria-pressed", "true");
    },
  );
  await step(
    page,
    info,
    "When",
    "食材から料理を検索し、選択後に人数を3人へ変える",
    async () => {
      await page.getByRole("button", { name: "この1つで探す" }).click();
      await expect(
        page.getByRole("heading", { name: "こんな一品、どう？" }),
      ).toBeVisible();
      await expect(
        page.getByRole("spinbutton", { name: "人数", exact: true }),
      ).toHaveCount(0);
      await page
        .getByRole("button", { name: "なすと卵の醤油炒めを見る" })
        .click();
      await page.getByLabel("人数", { exact: true }).fill("3");
      await page.getByLabel("人数", { exact: true }).press("Tab");
      await expect(page.getByLabel("人数", { exact: true })).toHaveValue("3");
      await page
        .getByRole("button", { name: "献立に追加", exact: true })
        .click();
      await expect
        .poll(async () =>
          (await workspace(page)).meal.some((item) => item.servings === 3),
        )
        .toBe(true);
    },
  );
  await step(
    page,
    info,
    "Then",
    "再読み込み後も献立の人数を保持し、買物量と調理手順を表示する",
    async () => {
      await page.reload();
      await expect(
        page
          .getByRole("spinbutton", { name: "なすと卵の醤油炒めの人数" })
          .last(),
      ).toHaveValue("3");
      await page
        .getByRole("button", { name: /買い物/ })
        .first()
        .click();
      await expect(
        page.getByRole("heading", { name: "買うもの、これだけ。" }),
      ).toBeVisible();
      await page.getByRole("button", { name: "献立に戻る" }).click();
      // 初期レシピの工程時間は基準2人だけが登録済み。人数を推測で外挿しない。
      const servings = page.getByRole("spinbutton", {
        name: "なすと卵の醤油炒めの人数",
      });
      for (const input of await servings.all()) {
        await input.fill("2");
        await input.press("Tab");
      }
      await expect
        .poll(async () =>
          (await workspace(page)).meal.every((item) => item.servings === 2),
        )
        .toBe(true);
      await page.getByRole("button", { name: "段取りを見る" }).click();
      await expect(
        page.getByRole("heading", { name: "無理なく、ひとつずつ。" }),
      ).toBeVisible();
      expect(await page.evaluate(() => localStorage.length)).toBe(0);
    },
  );
  await step(
    page,
    info,
    "When",
    "調理を始め、工程を進めて実使用量の確認を開く",
    async () => {
      await page
        .getByRole("button", { name: "調理を始める", exact: true })
        .click();
      await expect(page.locator(".focus-screen")).toBeVisible();
      const count = (await workspace(page)).cooking!.plan.length;
      for (let index = 0; index < count - 1; index++) {
        await page.getByRole("button", { name: "次へ", exact: true }).click();
        await expect
          .poll(async () => (await workspace(page)).cooking!.index)
          .toBe(index + 1);
      }
      await page
        .getByRole("button", { name: "使用量を確認する", exact: true })
        .click();
      await expect(
        page.getByRole("checkbox", { name: /在庫から使用量を引く/ }),
      ).not.toBeChecked();
    },
  );
  await step(
    page,
    info,
    "Then",
    "利用者が控除を選ばなければ在庫を変更せず完了する",
    async () => {
      const before = (await workspace(page)).lots;
      await page.getByRole("button", { name: "完了", exact: true }).click();
      await expect
        .poll(async () => (await workspace(page)).cooking?.status)
        .toBe("completed");
      expect((await workspace(page)).lots).toEqual(before);
      await page.reload();
      expect((await workspace(page)).cooking?.status).toBe("completed");
    },
  );
});

test("在庫を登録すると再読み込み・別のタブでも同じ在庫を表示する", async ({
  page,
  context,
}, info) => {
  let lotId = "";
  await step(page, info, "Given", "自分の冷蔵庫を開く", async () => {
    await login(page);
  });
  await step(page, info, "When", "なすの量を271gとして登録する", async () => {
    const before = await workspace(page);
    await addPantry(page, "271");
    const after = await workspace(page);
    lotId = after.lots.find(
      (lot) => !before.lots.some((old) => old.id === lot.id),
    )!.id;
    expect(after.lots.find((lot) => lot.id === lotId)?.quantity.value).toBe(
      271,
    );
  });
  const other = await context.newPage();
  await step(
    other,
    info,
    "Then",
    "同じ利用者で別のタブにログインしても登録した在庫が見える",
    async () => {
      await login(other);
      await other.getByRole("button", { name: "冷蔵庫", exact: true }).click();
      expect(
        (await workspace(other)).lots.find((lot) => lot.id === lotId)?.quantity
          .value,
      ).toBe(271);
      await expect(
        other.getByText("271g", { exact: true }).last(),
      ).toBeVisible();
      await page.reload();
      expect(
        (await workspace(page)).lots.find((lot) => lot.id === lotId)?.quantity
          .value,
      ).toBe(271);
    },
  );
  await other.close();
});

test("別の利用者の冷蔵庫は表示せず、他人の在庫の削除も拒否する", async ({
  page,
  browser,
}, info) => {
  let lotId = "";
  await step(page, info, "Given", "Aliceが自分の在庫を登録する", async () => {
    await login(page);
    const before = await workspace(page);
    await addPantry(page, "389");
    lotId = (await workspace(page)).lots.find(
      (lot) => !before.lots.some((old) => old.id === lot.id),
    )!.id;
  });
  const context = await browser.newContext({
    viewport: info.project.use.viewport,
    locale: "ja-JP",
  });
  const bob = await context.newPage();
  await step(
    bob,
    info,
    "When",
    "Bobが別のアカウントでログインする",
    async () => {
      await login(bob, "bob");
      await bob.getByRole("button", { name: "冷蔵庫", exact: true }).click();
    },
  );
  await step(
    bob,
    info,
    "Then",
    "Aliceの在庫は一覧に含まれず、IDを指定した削除も拒否される",
    async () => {
      const state = await workspace(bob);
      expect(state.lots.some((lot) => lot.id === lotId)).toBe(false);
      const status = await bob.evaluate(
        async ({ lotId, version }) =>
          (
            await fetch(`/api/pantry-lots/${lotId}`, {
              method: "DELETE",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${sessionStorage.getItem("recipeweave.access-token")}`,
              },
              body: JSON.stringify({ expectedVersion: version }),
            })
          ).status,
        { lotId, version: state.version },
      );
      expect([403, 404]).toContain(status);
      expect(
        (await workspace(page)).lots.find((lot) => lot.id === lotId)?.status,
      ).toBe("active");
    },
  );
  await context.close();
});

test("誤ったパスワードではログインしない", async ({ page }, info) => {
  await step(page, info, "Given", "ログイン画面を開く", async () => {
    await page.goto("/#/login");
  });
  await step(page, info, "When", "誤ったパスワードを入力する", async () => {
    await page.getByLabel("ユーザー名", { exact: true }).fill("alice");
    await page.getByLabel("パスワード", { exact: true }).fill("wrong-password");
    await page
      .locator("form")
      .getByRole("button", { name: "ログイン", exact: true })
      .click();
  });
  await step(
    page,
    info,
    "Then",
    "エラーを表示し、認証トークンを保存しない",
    async () => {
      await expect(page.getByRole("alert")).toBeVisible();
      await expect(
        page.getByRole("button", { name: "ログアウト" }),
      ).toHaveCount(0);
      expect(
        await page.evaluate(() =>
          sessionStorage.getItem("recipeweave.access-token"),
        ),
      ).toBeNull();
    },
  );
});

test("通信に失敗した在庫登録は成功と表示せず入力を保持する", async ({
  page,
}, info) => {
  await step(
    page,
    info,
    "Given",
    "在庫の追加画面で数量を入力する",
    async () => {
      await login(page);
      await page.getByRole("button", { name: "冷蔵庫", exact: true }).click();
      await page
        .getByRole("button", { name: "手入力で追加", exact: true })
        .click();
      await page.getByLabel("数量（空欄は数量不明）").fill("417");
    },
  );
  await step(page, info, "When", "登録時に通信が切れる", async () => {
    await page.route("**/api/pantry-lots", (route) =>
      route.abort("internetdisconnected"),
    );
    await page.getByRole("button", { name: "登録する", exact: true }).click();
  });
  await step(
    page,
    info,
    "Then",
    "登録画面と入力値を保ち、成功したと扱わない",
    async () => {
      await expect(page.getByRole("dialog")).toBeVisible();
      await expect(page.getByLabel("数量（空欄は数量不明）")).toHaveValue(
        "417",
      );
      await expect(page.getByRole("alert")).toContainText("接続できません");
    },
  );
});

test("レシート画像を実際に読み取り、確認した食材を登録して履歴から取り消す", async ({
  page,
}, info) => {
  let before: AppState;
  let importId = "";
  await step(
    page,
    info,
    "Given",
    "ログインしてレシート画像を読み取る",
    async () => {
      await login(page);
      before = await workspace(page);
      await recognizeTestReceipt(page, `${info.project.name} ${Date.now()}`);
      expect((await workspace(page)).imports.length).toBe(
        before.imports.length,
      );
    },
  );
  await step(
    page,
    info,
    "When",
    "候補を確認してから冷蔵庫へ登録する",
    async () => {
      await expect(
        page.getByRole("button", { name: "この内容で登録", exact: true }),
      ).toBeEnabled();
      await page
        .getByRole("button", { name: "この内容で登録", exact: true })
        .click();
      await expect
        .poll(async () => (await workspace(page)).imports.length)
        .toBe(before.imports.length + 1);
      importId = (await workspace(page)).imports.find(
        (entry) => !before.imports.some((old) => old.id === entry.id),
      )!.id;
      expect(
        (await workspace(page)).lots.filter(
          (lot) => lot.sourceImportId === importId,
        ).length,
      ).toBeGreaterThan(0);
    },
  );
  await step(
    page,
    info,
    "Then",
    "登録結果を読み込み直し、履歴からこのレシートの追加だけを取り消す",
    async () => {
      await page.goto("/#/history");
      await expect(
        page.getByRole("heading", { name: "レシート履歴" }),
      ).toBeVisible();
      await page
        .getByRole("button", { name: /取り消す/ })
        .first()
        .click();
      await page
        .getByRole("dialog")
        .getByRole("button", { name: "この内容で取り消す", exact: true })
        .click();
      await expect
        .poll(
          async () =>
            (await workspace(page)).imports.find(
              (entry) => entry.id === importId,
            )?.state,
        )
        .toBe("undone");
      const after = await workspace(page);
      expect(
        after.lots
          .filter((lot) => lot.sourceImportId === importId)
          .every((lot) => lot.status === "undone"),
      ).toBe(true);
      expect(
        after.lots.filter((lot) => before.lots.some((old) => old.id === lot.id))
          .length,
      ).toBe(before.lots.length);
    },
  );
});

test("読取候補をキャンセルしても冷蔵庫や登録履歴を変更しない", async ({
  page,
}, info) => {
  let before: AppState;
  await step(
    page,
    info,
    "Given",
    "読み取ったレシートの確認画面を表示する",
    async () => {
      await login(page);
      before = await workspace(page);
      await recognizeTestReceipt(page, `cancel ${Date.now()}`);
    },
  );
  await step(
    page,
    info,
    "When",
    "キャンセルして読み取り候補を破棄する",
    async () => {
      await page
        .getByRole("button", { name: "キャンセル", exact: true })
        .click();
      await page
        .getByRole("button", { name: "破棄してやめる", exact: true })
        .click();
    },
  );
  await step(page, info, "Then", "登録前と同じ在庫と履歴が残る", async () => {
    await expect(
      page.getByRole("heading", { name: "冷蔵庫に、何がある？" }),
    ).toBeVisible();
    const after = await workspace(page);
    expect(after.lots).toEqual(before.lots);
    expect(after.imports).toEqual(before.imports);
  });
});

test("同時更新を検知すると上書きせず、最新内容を読んでから再操作できる", async ({
  page,
}, info) => {
  let before: AppState;
  await step(
    page,
    info,
    "Given",
    "在庫の入力中に別の操作が同じアカウントを更新する",
    async () => {
      await login(page);
      await page.getByRole("button", { name: "冷蔵庫", exact: true }).click();
      await page
        .getByRole("button", { name: "手入力で追加", exact: true })
        .click();
      await page.getByLabel("数量（空欄は数量不明）").fill("523");
      before = await workspace(page);
      const status = await page.evaluate(
        async (state) =>
          (
            await fetch("/api/settings", {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${sessionStorage.getItem("recipeweave.access-token")}`,
              },
              body: JSON.stringify({
                expectedVersion: state.version,
                settings: state.settings,
              }),
            })
          ).status,
        before,
      );
      expect(status).toBe(200);
    },
  );
  await step(
    page,
    info,
    "When",
    "古い状態の画面から登録を実行する",
    async () => {
      await page.getByRole("button", { name: "登録する", exact: true }).click();
      await expect(page.getByRole("alert")).toContainText("ほかの画面で更新");
      expect((await workspace(page)).lots).toEqual(before.lots);
    },
  );
  await step(
    page,
    info,
    "Then",
    "入力を保ったまま最新内容を読み、再操作で一件だけ登録する",
    async () => {
      await expect(page.getByLabel("数量（空欄は数量不明）")).toHaveValue(
        "523",
      );
      await page
        .getByRole("dialog")
        .getByRole("button", { name: "最新の内容を読み込む" })
        .click();
      await expect(page.getByRole("alert")).toHaveCount(0);
      await page.getByRole("button", { name: "登録する", exact: true }).click();
      await expect(page.getByRole("dialog")).not.toBeVisible();
      expect((await workspace(page)).lots.length).toBe(before.lots.length + 1);
    },
  );
});
