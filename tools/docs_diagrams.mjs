/** 生成したMermaidを実パーサーへ通し、描画時まで構文不備を隠さない。 */
import { createHash } from 'node:crypto';
import { readdir, readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import mermaid from '../documentation/node_modules/mermaid/dist/mermaid.esm.mjs';

const directory = resolve('docs/design/generated');
const seen = new Set();
let count = 0;
async function walk(path) {
  for (const entry of await readdir(path, { withFileTypes: true })) {
    const name = resolve(path, entry.name);
    if (entry.isSymbolicLink()) throw new Error(`図の入力にリンクは使えません: ${name}`);
    if (entry.isDirectory()) await walk(name);
    else if (entry.name.endsWith('.md')) {
      const text = await readFile(name, 'utf8');
      for (const [index, match] of [...text.matchAll(/```mermaid\n([\s\S]*?)```/g)].entries()) {
        count += 1;
        const hash = createHash('sha256').update(match[1]).digest('hex');
        if (seen.has(hash)) continue;
        try {
          await mermaid.parse(match[1]);
        } catch (error) {
          throw new Error(`図の構文エラー: ${name} / 図${index + 1}: ${error.message}`);
        }
        seen.add(hash);
      }
    }
  }
}
await walk(directory);
if (!count) throw new Error('生成図がありません');
process.stdout.write(`Mermaid構文: ${count} 図 / 固有の構造 ${seen.size} 件を検証\n`);
