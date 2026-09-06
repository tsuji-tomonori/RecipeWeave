import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const base = process.env.DOCS_BASE || '/design';
export default defineConfig({
  site: 'https://tsuji-tomonori.github.io',
  base,
  outDir: '../reports/design',
  integrations: [starlight({
    title: 'RecipeWeave / 設計・品質',
    defaultLocale: 'root',
    locales: {root: {label: '日本語', lang: 'ja'}},
    customCss: ['./src/styles/theme.css'],
    components: {Footer: './src/components/Footer.astro'},
    // APIごとの6帳票は一覧と検索から開き、数千リンクを全ページへ複製しない。
    sidebar: [
      {label: '品質サマリーへ戻る', link: base.replace(/\/design\/?$/, '') + '/'},
      {label: '設計書の概要', slug: ''},
      {label: 'API仕様', items: [
        {label: 'API一覧・6帳票', slug: 'api'},
        {label: 'CRUD対応', slug: 'api/crud'},
        {label: 'モデルとenum', slug: 'api/models'},
        {label: '共通エラー', slug: 'api/errors'},
      ]},
      {label: 'データベース', items: [
        {label: '全テーブル一覧', slug: 'database'},
        {label: 'ER図', slug: 'database/er'},
      ]},
      {label: 'サービス・インフラ', slug: 'service'},
      {label: 'レシピ生成器', slug: 'generator'},
      {label: '要件と受入条件', slug: 'requirements'},
      {label: '生成方法', slug: 'automation'},
      {label: '生成元・ハッシュ', slug: 'manifest'},
    ],
    expressiveCode: {shiki: {langs: []}},
  })],
});
