<script lang="ts">
 import type {Food} from './types';
 let {food,selected=false,onselect}:{food:Food;selected?:boolean;onselect:()=>void}=$props();
 const atlas=`${import.meta.env.BASE_URL}food/ingredients-atlas.png`;
</script>
<button class:selected class="food-tile" onclick={onselect} aria-pressed={selected} aria-label={`${food.name}を${selected?'外す':'選ぶ'}`}>
 {#if food.imageIndex!==null}<span class="food-photo" style={`background-image:url('${atlas}');background-position:${food.imageIndex%4*100/3}% ${Math.floor(food.imageIndex/4)*50}%`}></span>{:else}<span class="food-photo food-letter">{food.name.slice(0,1)}</span>{/if}
 <span class="selection-check" aria-hidden="true">{selected?'✓':''}</span><span class="food-name">{food.name}</span>
</button>
