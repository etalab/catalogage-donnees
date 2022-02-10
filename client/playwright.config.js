const config = {
  testDir: "./src/tests/e2e/",
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
