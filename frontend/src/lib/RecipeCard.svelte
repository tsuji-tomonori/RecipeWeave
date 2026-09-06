<script lang="ts">
  import type { Recipe } from "./types";
  let {
    recipe,
    onclick,
    large = false,
  }: { recipe: Recipe; onclick: () => void; large?: boolean } = $props();
</script>

<button
  class:large
  class="recipe-card"
  {onclick}
  aria-label={`${recipe.name}を見る`}
>
  <img
    src={recipe.imageUrl ||
      `${import.meta.env.BASE_URL}food/recipe-placeholder.svg`}
    alt={recipe.name}
    loading="lazy"
  />
  <span class="recipe-copy"
    ><span class="eyebrow">{recipe.tags[0] || "今日の一品"}</span><strong
      >{recipe.name}</strong
    ><span class="muted"
      >{recipe.minutes}分 <span class="dot">·</span>
      {recipe.equipment.join("・")}</span
    ></span
  >
  <span class="card-arrow" aria-hidden="true">↗</span>
</button>
