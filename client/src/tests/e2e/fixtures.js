import { test as base, expect } from "@playwright/test";

/**
 * @type {import("@playwright/test").Fixtures<
 *  {
 *    apiContext: import("@playwright/test").APIRequestContext,
 *    dataset: import("src/definitions/datasets").Dataset
 *  },
 *  {},
 *  import("@playwright/test").PlaywrightTestArgs,
 *  import("@playwright/test").PlaywrightWorkerArgs
 * >}
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
