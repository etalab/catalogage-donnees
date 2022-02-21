import { test as base, expect } from "@playwright/test";

// See: https://playwright.dev/docs/test-fixtures

/**
 * @type {import("@playwright/test").Fixtures<{
 *  page: any,
 *  sampleDataset: import('src/definitions/datasets').Dataset
 * }>}
 */
const fixtures = {
  sampleDataset: async ({ page }, use) => {
    const [dataset, dispose] = await getSampleDataset();
    await use(dataset);
    await dispose();
  },
};

export const test = base.extend(fixtures);

// See: https://playwright.dev/docs/test-api-testing#sending-api-requests-from-ui-tests

/**
 * @type {import("@playwright/test").APIRequestContext}
 */
let apiContext;

test.beforeAll(async ({ playwright }) => {
  apiContext = await playwright.request.newContext({
    baseURL: "http://localhost:3579",
  });
});

test.afterAll(async () => {
  await apiContext.dispose();
});

/**
 *
 * @returns {Promise<[import("src/definitions/datasets").Dataset, () => Promise<void>]>}
 */
const getSampleDataset = async () => {
  /**
   * @type {import("src/definitions/datasets").DatasetCreateData}
   */
  const data = {
    title: "Sample title",
    description: "Sample description",
    formats: ["api"],
  };

  let response = await apiContext.post("/datasets/", {
    data,
  });
  expect(response.ok()).toBeTruthy();

  /**
   * @type {import("src/definitions/datasets").Dataset}
   */
  const dataset = await response.json();

  const dispose = async () => {
    response = await apiContext.delete(`/datasets/${dataset.id}/`);
    expect(response.ok()).toBeTruthy();
  };

  return [dataset, dispose];
};
