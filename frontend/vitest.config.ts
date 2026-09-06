import { defineConfig, mergeConfig } from "vitest/config";
import { svelteTesting } from "@testing-library/svelte/vite";
import viteConfig from "./vite.config.ts";
export default mergeConfig(
  viteConfig,
  defineConfig({
    plugins: [svelteTesting()],
    test: {
      include: ["src/**/*.test.ts"],
      testTimeout: 15000,
      coverage: {
        provider: "v8",
        reportsDirectory: "../reports/frontend-coverage",
        reporter: ["text", "json-summary", "html", "lcov"],
        include: ["src/**/*.{ts,svelte}"],
        exclude: ["src/**/*.test.ts", "src/test-fixtures.ts"],
      },
    },
  }),
);
