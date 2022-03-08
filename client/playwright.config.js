/** @type {import('@playwright/test').Config} */
const config = {
  testDir: "./src/tests/e2e/",
  globalSetup: "./src/tests/e2e/global-setup.js",
  retries: 3,
  use: {
    baseURL: "http://localhost:3000",
    browserName: "firefox",
    headless: true,
    screenshot: "only-on-failure",
    video: "on-first-retry",
  },
};
export default config;
