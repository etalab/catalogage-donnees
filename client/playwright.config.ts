import path from "path";
import dotenv from "dotenv";
import { Config } from "@playwright/test";

dotenv.config({
  path: path.resolve("..", ".env"),
});

const config: Config = {
  testDir: "./src/tests/e2e/",
  globalSetup: "./src/tests/e2e/global-setup.ts",
  retries: 3,
  use: {
    baseURL: "http://localhost:3000",
    browserName: "firefox",
    headless: true,
    screenshot: "only-on-failure",
    video: "on-first-retry",
  },
  projects: [
    {
      name: "default",
      use: {
        adminTestPassword: process.env.TOOLS_ADMIN_PASSWORD,
      },
    },
  ],
};

export default config;
