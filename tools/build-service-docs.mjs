import { cp, mkdir, readFile, readdir, writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const requireFrontend = createRequire(join(root, 'frontend/package.json'));
const { marked } = await import(pathToFileURL(requireFrontend.resolve('marked')).href);
const source = join(root, 'docs/service');
const out = resolve(root, process.argv[2] ?? 'frontend/public/help');
const names = {
  overview: 'サービス概要',
  manual: '使い方',
  faq: 'Q&A',
  'screens-and-flows': '画面と動線',
  'review-scenarios': '確認シナリオ',
  'revision-log': '改訂記録',
};
const css = `body{font-family:system-ui,"Noto Sans JP",sans-serif;color:#30241f;background:#fffcf8;margin:0;line-height:1.85}main{max-width:960px;margin:auto;padding:32px 24px 80px}h1{font-size:30px;line-height:1.5}h2{margin-top:56px;padding-bottom:12px;border-bottom:2px solid #ee4d05}h3{margin-top:32px}a{color:#a93200}nav{padding:14px 24px;background:white;border-bottom:1px solid #e6ded7;display:flex;gap:20px;flex-wrap:wrap}nav a{padding:8px 0}table{border-collapse:collapse;width:100%;display:block;overflow-x:auto;font-size:14px}th,td{border:1px solid #e3d9d1;padding:12px;min-width:100px;vertical-align:top}th{background:#ffede1}img{display:block;max-width:100%;max-height:880px;object-fit:contain;margin:24px auto;border:1px solid #eee;border-radius:16px}blockquote{border-left:4px solid #ee4d05;padding:8px 20px;background:#fff0e5;margin:20px 0}.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:24px}.gallery img{height:280px;width:100%;margin:8px 0;background:white}.badge{color:#a83905;font-size:13px}li{margin:8px 0}code{overflow-wrap:anywhere}a:focus-visible{outline:3px solid #a93200;outline-offset:4px}@media print{nav{display:none}main{padding:0}h2{break-after:avoid}img{max-height:650px}table{font-size:10px}}`;
const nav = `<nav aria-label="サービス資料"><strong>RecipeWeave</strong>${Object.entries(names).map(([key, name]) => `<a href="${key}.html">${name}</a>`).join('')}<a href="index.html">画像一覧</a></nav>`;
const page = (title, body) => `<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>${title} | RecipeWeave</title><style>${css}</style></head><body>${nav}<main>${body}</main></body></html>`;
await mkdir(out, { recursive: true });
for (const [key, title] of Object.entries(names)) {
  const text = await readFile(join(source, `${key}.md`), 'utf8');
  const html = marked.parse(text).replace(/href="([^"#]+)\.md(?=["#])/g, 'href="$1.html');
  await writeFile(join(out, `${key}.html`), page(title, html));
  await writeFile(join(out, `${key}.md`), text);
}
await cp(join(source, 'images'), join(out, 'images'), { recursive: true });
await cp(join(source, 'reviews'), join(out, 'reviews'), { recursive: true });
const pictures = (await readdir(join(source, 'images'))).filter(name => name.endsWith('.png')).sort();
const gallery = pictures.map(name => `<a href="images/${name}"><img loading="lazy" src="images/${name}" alt="操作イメージ ${name.replace('.png', '')}">${name.replace('.png', '')}</a>`).join('');
await writeFile(join(out, 'index.html'), page('サービス資料', `<p class="badge">操作重視型 B · サービス設計</p><h1>食材を選ぶところから、<br>今日の料理ができるまで。</h1><p>利用者向けの説明と、押す場所が分かる操作図です。01〜20は基本画面案、21〜28はレシートと主な操作のガイドです。実提供の範囲はマニュアル冒頭で確認してください。</p><div class="gallery">${gallery}</div>`));
console.log(`Service documents: ${Object.keys(names).length + 1} HTML pages, ${pictures.length} images → ${out}`);
