/** 単体テストだけで使う固定値。本番の依存グラフには含めない。 */
import foods from "../../data/samples/foods.json";
import recipes from "../../data/samples/recipes.json";
import type { Food, Recipe } from "./lib/types";
export const fixtureFoods = foods as Food[];
export const fixtureRecipes = recipes as Recipe[];
