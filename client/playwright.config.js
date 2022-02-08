const config = {
  testDir: "./src/tests/e2e/",
  use: {
    screenshot: "only-on-failure",
    video: "on-first-retry",
  },
};
export default config;
