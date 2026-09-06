import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
export default defineConfig({
  base: process.env.VITE_BASE_PATH || "./",
  plugins: [svelte()],
  build: { target: "es2022" },
  server: {
    host: "0.0.0.0",
    proxy: {
      "/api": {
        target: process.env.API_PROXY_TARGET || "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
