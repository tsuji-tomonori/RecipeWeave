import { DomainError, FOODS } from './domain';
import type { Food, Quantity, ReceiptCandidate, Unit } from './types';

const normalize = (value: string): string => value.normalize('NFKC').toLowerCase().replace(/\s+/g, '');
const excludedPattern = /合計|小計|お預り|お預かり|お釣り|釣銭|消費税|税率|内税|外税|値引|割引|クーポン|ポイント|会員|電話|領収|レシート|現金|クレジット|visa|mastercard|洗剤|漂白|柔軟剤|シャンプー|ティッシュ|トイレ|レジ袋|袋代|箸代|tel|登録番号|ご利用|営業時間|店$/i;
function explicitQuantity(raw: string, fallback: Unit): Quantity {
  // Digits without an explicit physical/purchase unit remain prices or unknown.
  // Package contents such as "10個入" are not a purchase quantity.
  const text = raw.normalize('NFKC').replace(/\d+(?:\.\d+)?\s*(?:個|枚|本)\s*入(?:り)?/g, '');
  const match = text.match(/(?:^|[^\d.\-])([0-9]+(?:\.[0-9]+)?)\s*(kg|ml|g|l|パック|袋|缶|個|本|枚|点)(?![a-z])/i);
  if (!match) return { value: null, unit: fallback };
  const value = Number(match[1]); const token = match[2].toLowerCase();
  if (token === 'kg') return { value: value * 1000, unit: 'g' };
  if (token === 'l') return { value: value * 1000, unit: 'ml' };
  return { value, unit: token as Unit };
}
export function parseReceipt(text: string, foods: Food[] = FOODS): ReceiptCandidate[] {
  const aliases = foods.flatMap((food) => [food.name, ...food.aliases].map((name) => ({ food, name: normalize(name) }))).sort((a, b) => b.name.length - a.name.length);
  return text.split(/\r?\n/).map((raw) => raw.trim()).filter(Boolean).map((rawText, index) => {
    const normalized = normalize(rawText);
    const match = aliases.find((entry) => normalized.includes(entry.name));
    const metadata = excludedPattern.test(normalized) || /^(?:[\d\s¥￥.,:：/\-年月日時分秒%*]+)$/.test(normalized);
    const status = metadata ? 'excluded' : match ? 'matched' : 'review';
    return { id: `line-${index + 1}`, rawText, foodId: metadata ? null : match?.food.id ?? null, quantity: explicitQuantity(rawText, match?.food.defaultUnit ?? 'g'), selected: status === 'matched', status,
      reason: status === 'excluded' ? '日用品・金額・店舗情報など。食品なら戻せます。' : status === 'matched' ? '食材候補を確認してください。' : '食材名を確認してください。' };
  });
}
async function sha256(value: ArrayBuffer): Promise<string> {
  const digest = await crypto.subtle.digest('SHA-256', value);
  return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
}
export async function receiptSignature(candidates: ReceiptCandidate[]): Promise<string> {
  // Order-independent but multiplicity-preserving. No raw OCR or store/date data persists.
  const rows = candidates.filter((x) => x.selected).map((x) => `${x.foodId ?? '?'}:${x.quantity.value ?? '?'}:${x.quantity.unit}`).sort();
  return sha256(new TextEncoder().encode(JSON.stringify(rows)).buffer as ArrayBuffer);
}
export function validateReceiptFile(file: Pick<File, 'type' | 'size'>): void {
  if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) throw new DomainError('UNSUPPORTED_IMAGE', 'JPEG・PNG・WebPの画像を選んでください。');
  if (!Number.isFinite(file.size) || file.size <= 0 || file.size > 10 * 1024 * 1024) throw new DomainError('IMAGE_SIZE', '画像は1枚10MBまでです。別の画像を選んでください。');
}
export async function hashImage(file: File): Promise<string> { validateReceiptFile(file); return sha256(await file.arrayBuffer()); }
