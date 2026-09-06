<script lang="ts">
  import type { Food } from "./types";

  let {
    foods,
    selected,
    label,
    onselect,
  }: {
    foods: Food[];
    selected: string[];
    label: string;
    onselect: (id: string) => void;
  } = $props();
  let query = $state("");
  let limit = $state(24);
  const matching = $derived(
    foods.filter(
      (food) =>
        !selected.includes(food.id) &&
        (!query.trim() ||
          [food.name, ...food.aliases].some((name) =>
            name.includes(query.trim()),
          )),
    ),
  );
  const visible = $derived([
    ...foods.filter((food) => selected.includes(food.id)),
    ...matching.slice(0, limit),
  ]);
</script>

<label class="field gap-bottom">
  {label}を探す
  <input
    type="search"
    bind:value={query}
    oninput={() => (limit = 24)}
    placeholder="食材名を入力"
  />
</label>
<p class="check-note">
  選択中 {selected.length}件 · 選んだ食材は検索中も表示します。
</p>
<div class="settings-options">
  {#each visible as food (food.id)}
    <button
      class="chip"
      class:on={selected.includes(food.id)}
      aria-pressed={selected.includes(food.id)}
      onclick={() => onselect(food.id)}
      >{selected.includes(food.id) ? "✓ " : ""}{food.name}</button
    >
  {/each}
</div>
{#if !matching.length}
  <p class="check-note">検索に一致する未選択の食材はありません。</p>
{:else if matching.length > limit}
  <button class="text-button" onclick={() => (limit += 24)}
    >もっと表示（あと{matching.length - limit}件）</button
  >
{/if}
