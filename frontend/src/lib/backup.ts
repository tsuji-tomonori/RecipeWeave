/** サーバー発行のバックアップ本文を保持し、DBの整数・小数をブラウザで丸めない。 */
export const MAX_BACKUP_BYTES = 5_000_000;
export interface BackupInput {
  text: string;
  name: string;
  exportedAt: string;
  ownerId: string;
}
export interface BackupPreview {
  intentId: string;
  expiresAt: string;
  expectedVersion: number;
  backupSha256: string;
  sourceVersion: number;
  counts: {
    table: string;
    label: string;
    currentCount: number;
    restoreCount: number;
  }[];
  replaceTargets: string[];
  preservedTargets: string[];
}
export async function readBackupFile(file: File): Promise<BackupInput> {
  if (!file.size || file.size > MAX_BACKUP_BYTES)
    throw new Error(
      "バックアップは5,000,000バイト以内のJSONファイルを選んでください。",
    );
  const text = await file.text();
  let value: unknown;
  try {
    value = JSON.parse(text);
  } catch {
    throw new Error(
      "JSONファイルを読み取れません。書き出したバックアップを選び直してください。",
    );
  }
  if (!value || typeof value !== "object" || Array.isArray(value))
    throw new Error("対応するバックアップの形式ではありません。");
  const metadata = value as Record<string, unknown>;
  if (
    metadata.format !== "recipeweave-relational" ||
    metadata.formatVersion !== 2
  )
    throw new Error(
      "このファイルは復元できません。現在のアプリから書き出した形式2のバックアップを選んでください。旧ブラウザ保存形式には対応していません。",
    );
  if (
    typeof metadata.ownerId !== "string" ||
    typeof metadata.exportedAt !== "string" ||
    typeof metadata.artifactId !== "string"
  )
    throw new Error("バックアップの発行情報が不足しています。");
  return {
    text,
    name: file.name,
    ownerId: metadata.ownerId,
    exportedAt: metadata.exportedAt,
  };
}
