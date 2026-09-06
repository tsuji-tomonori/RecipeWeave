import { defineConfig, mergeConfig } from "vitest/config";
import { svelteTesting } from "@testing-library/svelte/vite";
import viteConfig from "./vite.config.ts";
export default mergeConfig(
  viteConfig,
  defineConfig({
    plugins: [svelteTesting()],
    test: { include: ["src/**/*.test.ts"], testTimeout: 15000 },
  }),
);
