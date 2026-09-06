import { createWorker, OEM, type Worker } from "tesseract.js";
export interface OcrTask {
  cancel(): Promise<void>;
  result: Promise<string>;
}
export async function validateReceiptImage(file: File): Promise<void> {
  const bytes = new Uint8Array(await file.slice(0, 16).arrayBuffer());
  const png =
    bytes[0] === 0x89 &&
    bytes[1] === 0x50 &&
    bytes[2] === 0x4e &&
    bytes[3] === 0x47 &&
    bytes[4] === 0x0d &&
    bytes[5] === 0x0a &&
    bytes[6] === 0x1a &&
    bytes[7] === 0x0a;
  const jpeg = bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff;
  const webp =
    String.fromCharCode(...bytes.slice(0, 4)) === "RIFF" &&
    String.fromCharCode(...bytes.slice(8, 12)) === "WEBP";
  if (!(
    (file.type === "image/png" && png) ||
    (file.type === "image/jpeg" && jpeg) ||
    (file.type === "image/webp" && webp)
  ))
    throw new Error(
      "画像の形式と内容が一致しません。JPEG・PNG・WebPの画像を選んでください。",
    );
  try {
    const bitmap = await createImageBitmap(file);
    if (
      !bitmap.width ||
      !bitmap.height ||
      bitmap.width * bitmap.height > 40_000_000
    ) {
      bitmap.close();
      throw new Error("画像サイズが大きすぎます。");
    }
    bitmap.close();
  } catch {
    throw new Error(
      "この画像を開けません。破損していない画像、または4,000万画素以下の画像を選んでください。",
    );
  }
}
/** All OCR assets are hosted with the app. Receipt pixels never leave the browser. */
export function recognizeReceipt(
  file: File,
  onProgress: (progress: number, status: string) => void,
): OcrTask {
  let worker: Worker | null = null;
  let cancelled = false;
  let rejectCancel: (reason: Error) => void = () => {};
  const cancelledResult = new Promise<never>((_, reject) => {
    rejectCancel = reject;
  });
  const base = new URL(`${import.meta.env.BASE_URL}ocr/`, document.baseURI)
    .href;
  const recognition = (async () => {
    worker = await createWorker("jpn", OEM.LSTM_ONLY, {
      workerPath: `${base}worker.min.js`,
      langPath: base,
      corePath: base,
      cacheMethod: "none",
      logger: (m) => {
        if (!cancelled) onProgress(m.progress, m.status);
      },
    });
    if (cancelled) {
      await worker.terminate();
      worker = null;
      throw new Error("読み取りをキャンセルしました。");
    }
    try {
      const result = await worker.recognize(file);
      if (cancelled) throw new Error("読み取りをキャンセルしました。");
      return result.data.text;
    } finally {
      if (worker) {
        await worker.terminate();
        worker = null;
      }
    }
  })();
  return {
    result: Promise.race([recognition, cancelledResult]),
    cancel: async () => {
      cancelled = true;
      rejectCancel(new Error("読み取りをキャンセルしました。"));
      if (worker) {
        await worker.terminate();
        worker = null;
      }
    },
  };
}
