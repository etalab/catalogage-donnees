import path from "path";
import dotenv from "dotenv";
import type { PlaywrightTestConfig } from "@playwright/test";
import type { AppTestArgs } from "src/tests/e2e/fixtures";
import { ADMIN_EMAIL } from "./tests/e2e/constants";

dotenv.config({
  path: path.resolve("..", ".env"),
});

const getAdminTestPassword = (): string => {
  const passwords = Object.fromEntries(
    process.env.TOOLS_PASSWORDS.split(",")
      .map((value) => value.trim())
      .map((value) => value.split("="))
  );
  const adminPassword = passwords[ADMIN_EMAIL];
  if (!adminPassword) {
    throw new Error(
      `Password for ${ADMIN_EMAIL} not defined in TOOLS_PASSWORDS`
    );
  }
  return adminPassword;
};

const config: PlaywrightTestConfig<AppTestArgs> = {
  testDir: "./tests/e2e/",
  globalSetup: "./tests/e2e/global-setup.ts",
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
        adminTestPassword: getAdminTestPassword(),
      },
    },
  ],
};

export default config;
