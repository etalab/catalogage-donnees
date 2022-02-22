import { test as base, expect } from "@playwright/test";

/**
 * These fixtures allow simplifying setup/teardown logic in tests,
 * especially for preparing server-side state.
 * See: https://playwright.dev/docs/test-fixtures
 * See: https://playwright.dev/docs/test-api-testing#sending-api-requests-from-ui-tests
 */

/**
 * This is JSDoc annotations. We use them while waiting for Playwright TS setup to land.
 * See: https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html
 * See: https://github.com/etalab/catalogage-donnees/issues/87
 *
 * @typedef {{
 *  apiContext: import("@playwright/test").APIRequestContext,
 *  dataset: import("src/definitions/datasets").Dataset,
 * }} AppTestArgs
 *
 * @typedef {{}} AppWorkerArgs
 *
 * @typedef {import("@playwright/test").PlaywrightTestArgs} PlaywrightTestArgs
 * @typedef {import("@playwright/test").PlaywrightWorkerArgs} PlaywrightWorkerArgs
 *
 * @typedef {import("@playwright/test").Fixtures<
 *  AppTestArgs, AppWorkerArgs, PlaywrightTestArgs, PlaywrightWorkerArgs
 * >} AppFixtures
 */

/**
 * @type AppFixtures
 */
const fixtures = {
  apiContext: async ({ playwright }, use) => {
    const baseURL = "http://localhost:3579";
    const apiContext = await playwright.request.newContext({ baseURL });
    await use(apiContext);
    await apiContext.dispose();
  },

  dataset: async ({ apiContext }, use) => {
    /** @type {import("src/definitions/datasets").DatasetCreateData} */
    const data = {
      title: "Sample title",
      description: "Sample description",
      formats: ["api"],
    };
    let response = await apiContext.post("/datasets/", { data });
    expect(response.ok()).toBeTruthy();
    const dataset = await response.json();

    await use(dataset);

    response = await apiContext.delete(`/datasets/${dataset.id}/`);
    expect(response.ok()).toBeTruthy();
  },
};

export const test = base.extend(fixtures);
