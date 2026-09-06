import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./report-tests",
  outputDir: "./test-results/quality-attachments",
  workers: 1,
  retries: 0,
  timeout: 90000,
  reporter: [["list"], ["json", { outputFile: "./test-results/quality.json" }]],
  use: {
    baseURL: `${(process.env.QUALITY_BASE_URL || "http://127.0.0.1:4174").replace(/\/$/, "")}/`,
    locale: "ja-JP",
    screenshot: "only-on-failure",
    ...(process.env.PW_CHROMIUM
      ? { launchOptions: { executablePath: process.env.PW_CHROMIUM } }
      : {}),
  },
  projects: [
    {
      name: "quality-desktop",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 1440, height: 1000 },
      },
    },
    { name: "quality-mobile", use: { ...devices["Pixel 7"] } },
  ],
});
