import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
export default defineConfig({
  base: process.env.VITE_BASE_PATH || "./",
  plugins: [svelte()],
  build: { target: "es2022" },
  server: { host: "0.0.0.0" },
});
