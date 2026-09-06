import { describe, expect, it } from "vitest";
import { readBackupFile, MAX_BACKUP_BYTES } from "./backup";

const raw =
  '{"format":"recipeweave-relational","formatVersion":2,"artifactId":"artifact","ownerId":"owner","exportedAt":"2026-09-06T00:00:00Z","tables":{"ledger":[{"amount":9007199254740993,"small":0.000000000000000001}]}}';

describe("バックアップファイルの入口", () => {
  it("DB型の数値をJSONの再出力で丸めず、元の本文を保持する", async () => {
    const result = await readBackupFile(new File([raw], "backup.json"));
    expect(result.text).toBe(raw);
    expect(result.ownerId).toBe("owner");
  });
  it("旧形式・壊れたJSON・上限を超えるファイルは復元要求へ渡さない", async () => {
    await expect(
      readBackupFile(new File(['{"schemaVersion":1}'], "legacy.json")),
    ).rejects.toThrow("旧ブラウザ保存形式");
    await expect(
      readBackupFile(new File(["{"], "broken.json")),
    ).rejects.toThrow("JSONファイル");
    await expect(
      readBackupFile(
        new File([new Uint8Array(MAX_BACKUP_BYTES + 1)], "large.json"),
      ),
    ).rejects.toThrow("5,000,000");
  });
});
