// @vitest-environment jsdom
import {afterEach,beforeEach,describe,expect,it,vi} from 'vitest';
import {cleanup,fireEvent,render,screen,waitFor,within} from '@testing-library/svelte';
import {webcrypto} from 'node:crypto';
import App from './App.svelte';
import {createInitialState,getDraft,startCooking} from './lib/domain';
import {loadState,STORAGE_KEY} from './lib/persistence';

beforeEach(()=>{
 localStorage.clear();window.history.replaceState(null,'','#/home');
 Object.defineProperty(globalThis,'crypto',{value:webcrypto,configurable:true});
 Object.defineProperty(navigator,'locks',{value:{request:async(_name:string,fn:()=>unknown)=>new Promise((resolve,reject)=>setTimeout(()=>{try{resolve(fn());}catch(e){reject(e);}},5))},configurable:true});
 window.scrollTo=vi.fn();window.confirm=vi.fn(()=>true);URL.createObjectURL=vi.fn(()=> 'blob:receipt-preview');URL.revokeObjectURL=vi.fn();
});
afterEach(()=>{cleanup();vi.restoreAllMocks();});
const click=async(name:string|RegExp)=>fireEvent.click(await screen.findByRole('button',{name}));
const page=(route:string)=>{window.history.replaceState(null,'',`#/${route}`);return render(App);};
const saved=()=>loadState();

describe('service flows through mounted Svelte UI (simulated DOM)',()=>{
 it('selects full ingredient cards, keeps selected ingredients on return, and omits servings from search',async()=>{
  page('home');await click('なすを選ぶ');await click('卵を選ぶ');
  await waitFor(()=>expect(screen.getByRole('button',{name:'この2つで探す'})).toBeTruthy());
  await click('この2つで探す');await waitFor(()=>expect(screen.getByRole('heading',{name:'こんな一品、どう？'})).toBeTruthy());
  expect(screen.queryByRole('spinbutton',{name:'人数'})).toBeNull();
  expect(screen.getByRole('button',{name:'なすと卵の醤油炒めを見る'})).toBeTruthy();
  await click('戻る');await waitFor(()=>expect(screen.getByRole('button',{name:'なすを外す'}).getAttribute('aria-pressed')).toBe('true'));
 });
 it('registers only selected sample receipt foods, then reviews a duplicate without losing candidates',async()=>{
  page('receipt');await click('サンプルで試す');
  await waitFor(()=>expect(screen.getByRole('button',{name:'この内容で登録'})).toBeTruthy());
  expect(saved().lots).toHaveLength(0);
  await click('この内容で登録');await waitFor(()=>expect(saved().imports).toHaveLength(1));
  expect(saved().lots).toHaveLength(2);expect(saved().lots.every(l=>l.quantity.value===null)).toBe(true);
  await click('冷蔵庫');await waitFor(()=>expect(screen.getAllByRole('button',{name:'レシートから追加'})[0]).toBeTruthy());
  await fireEvent.click(screen.getAllByRole('button',{name:'レシートから追加'})[0]);await click('サンプルで試す');await click('この内容で登録');
  await waitFor(()=>expect(screen.getByRole('dialog')).toBeTruthy());await click('履歴を見る');
  expect(screen.getByText('読み取り中の候補は保持しています。登録日時と食材を比べてください。')).toBeTruthy();
  await click('読取内容の確認に戻る');expect(screen.getByRole('button',{name:'別の買い物として登録'})).toBeTruthy();
  expect(saved().imports).toHaveLength(1);
 });
 it('keeps corrected receipt names temporary until committing the receipt',async()=>{
  page('receipt');await click('サンプルで試す');await click('食材を選ぶ');
  const dialog=screen.getByRole('dialog');const select=within(dialog).getByLabelText('食材');
  await fireEvent.change(select,{target:{value:''}});
  await fireEvent.input(within(dialog).getByLabelText('新しい食材名'),{target:{value:'試用の野菜'}});
  await click('確認して戻る');expect(saved().customFoods).toHaveLength(0);expect(saved().lots).toHaveLength(0);
  await click('キャンセル');await click('破棄してやめる');
  await waitFor(()=>expect(screen.getByRole('heading',{name:'冷蔵庫に、何がある？'})).toBeTruthy());
  expect(saved().customFoods).toHaveLength(0);expect(saved().lots).toHaveLength(0);
 });
 it('starts cooking with the latest amount even while the quantity write is pending',async()=>{
  page('detail/eggplant-egg');
  const amount=screen.getByRole('spinbutton',{name:'なすの量'});
  await fireEvent.change(amount,{target:{value:'375'}});
  await click('この料理を作る');
  await waitFor(()=>expect(saved().cooking?.mealSnapshot[0].amounts.eggplant.value).toBe(375));
  expect(saved().lots).toHaveLength(0);
 });
 it('reconstructs completion quantities on reload and leaves deduction unchecked',async()=>{
  const initial=createInitialState();const started=startCooking(initial,[{...getDraft(initial,'eggplant-egg'),id:'meal-test'}]);
  localStorage.setItem(STORAGE_KEY,JSON.stringify(started));page('complete');
  await waitFor(()=>expect(screen.getByRole('spinbutton',{name:'なすの実使用量'})).toBeTruthy());
  expect((screen.getByRole('checkbox',{name:/在庫から使用量を引く/}) as HTMLInputElement).checked).toBe(false);
  await click('完了');await waitFor(()=>expect(saved().cooking?.status).toBe('completed'));
  expect(saved().cooking?.consumptionResults.every(r=>!r.applied)).toBe(true);expect(saved().lots).toHaveLength(0);
 });
 it('persists settings safely and respects exclusions on the random dish',async()=>{
  page('settings');await click('卵');await click('変更を保存');
  await waitFor(()=>expect(saved().settings.excludedFoodIds).toContain('egg'));
  await click('ホーム');await waitFor(()=>expect(screen.getByRole('heading',{name:'今日の一品、ここから。'})).toBeTruthy());
  expect(screen.queryByRole('button',{name:'なすと卵の醤油炒めを見る'})).toBeNull();
  expect(screen.queryByRole('button',{name:'トマトと卵の炒めものを見る'})).toBeNull();
 });
 it('shows an equipment correction instead of throwing when the plan cannot use the selected tools',async()=>{
  const initial=createInitialState();initial.meal=[{...getDraft(initial,'eggplant-egg'),id:'meal-1'}];initial.settings.equipment=[];
  localStorage.setItem(STORAGE_KEY,JSON.stringify(initial));page('plan');
  await waitFor(()=>expect(screen.getByRole('button',{name:'使う器具の設定を確認'})).toBeTruthy());
  expect(screen.queryByRole('button',{name:'調理を始める'})).toBeNull();
 });
 it('keeps damaged-storage errors visible after route initialization',async()=>{
  localStorage.setItem(STORAGE_KEY,'{broken');page('home');
  await waitFor(()=>expect(screen.getByText(/保存データを開けません/)).toBeTruthy());
  expect(localStorage.getItem(STORAGE_KEY)).toBe('{broken');
 });
});
