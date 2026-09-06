// @vitest-environment jsdom
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import { findRecipes, loadFoods, loadRecipe, randomRecipe } from "./api";
import { RECIPES, setCatalog } from "./domain";
import { fixtureFoods, fixtureRecipes } from "../test-fixtures";

interface Schema {
  $ref?: string;
  type?: string;
  properties?: Record<string, Schema>;
  items?: Schema;
  anyOf?: Schema[];
}
interface OpenApi {
  paths: Record<
    string,
    {
      get: {
        responses: Record<
          string,
          { content: Record<string, { schema: Schema }> }
        >;
      };
    }
  >;
  components: { schemas: Record<string, Schema> };
}
const specification: OpenApi = JSON.parse(
  readFileSync(resolve(process.cwd(), "../backend/openapi.gen.json"), "utf8"),
);

/** 包みの項目名を手書きせず、FastAPIから生成したOpenAPIの200応答構造を使う。 */
function responseFor(path: string, emptyRandom = false): unknown {
  function example(schema: Schema): unknown {
    if (schema.$ref) {
      const name = schema.$ref.split("/").at(-1)!;
      if (name === "Food") return fixtureFoods[0];
      if (name === "Recipe") return fixtureRecipes[0];
      const definition = specification.components.schemas[name];
      if (!definition) throw new Error(`未定義の応答モデル: ${name}`);
      return example(definition);
    }
    if (schema.anyOf) {
      const choice = schema.anyOf.find((item) =>
        emptyRandom ? item.type === "null" : item.type !== "null",
      );
      if (!choice) throw new Error("候補ゼロの応答がAPIで定義されていません");
      return example(choice);
    }
    if (schema.type === "null") return null;
    if (schema.type === "array" && schema.items) return [example(schema.items)];
    if (schema.type === "integer" || schema.type === "number") return 1;
    if (schema.properties)
      return Object.fromEntries(
        Object.entries(schema.properties).map(([key, value]) => [
          key,
          example(value),
        ]),
      );
    throw new Error(
      `カタログの応答構造を確認してください: ${JSON.stringify(schema)}`,
    );
  }
  return example(
    specification.paths[path].get.responses["200"].content["application/json"]
      .schema,
  );
}

afterEach(() => vi.unstubAllGlobals());

describe("生成OpenAPIとフロントのカタログ応答契約", () => {
  it("食材一覧・料理一覧・料理詳細・ランダム候補を、それぞれの200応答から取り出す", async () => {
    sessionStorage.clear();
    setCatalog([], []);
    const cases = [
      { path: "/api/foods", read: loadFoods, expected: [fixtureFoods[0]] },
      {
        path: "/api/recipes",
        read: async () => (await findRecipes()).items,
        expected: [fixtureRecipes[0]],
      },
      {
        path: "/api/recipes/{recipe_id}",
        read: () => loadRecipe(fixtureRecipes[0].id),
        expected: fixtureRecipes[0],
      },
      {
        path: "/api/recipes/random",
        read: () => randomRecipe([]),
        expected: fixtureRecipes[0],
      },
    ];
    for (const item of cases) {
      vi.stubGlobal(
        "fetch",
        vi.fn(async () => new Response(JSON.stringify(responseFor(item.path)))),
      );
      expect(await item.read(), item.path).toEqual(item.expected);
    }
    vi.stubGlobal(
      "fetch",
      vi.fn(
        async () =>
          new Response(
            JSON.stringify(responseFor("/api/recipes/random", true)),
          ),
      ),
    );
    expect(await randomRecipe([])).toBeNull();
    expect(RECIPES).toEqual([fixtureRecipes[0]]);
  });
});
