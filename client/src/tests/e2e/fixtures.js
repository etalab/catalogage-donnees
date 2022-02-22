/**
 * @typedef {import("@playwright/test").APIRequestContext} APIRequestContext
 * @typedef {import("src/definitions/datasets").Dataset} Dataset
 * @typedef {import("src/definitions/datasets").DatasetCreateData} DatasetCreateData
 */
import { test as base, expect } from "@playwright/test";

// See: https://playwright.dev/docs/test-fixtures

/**
 * @type {import("@playwright/test").Fixtures<{
 *  page: any,
 *  sampleDataset: Dataset
 * }>}
 */
const fixtures = {
  sampleDataset: async ({ page }, use) => {
    const [dataset, disposeDataset] = await getSampleDataset();
    await use(dataset);
    await disposeDataset();
  },
};

export const test = base.extend(fixtures);

// See: https://playwright.dev/docs/test-api-testing#sending-api-requests-from-ui-tests

/** @type {APIRequestContext} */
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
 * @returns {Promise<[Dataset, () => Promise<void>]>}
 */
const getSampleDataset = async () => {
  /** @type {DatasetCreateData} */
  const data = {
    title: "Sample title",
    description: "Sample description",
    formats: ["api"],
  };

  let response = await apiContext.post("/datasets/", { data });
  expect(response.ok()).toBeTruthy();

  /** @type {Dataset} */
  const dataset = await response.json();

  const disposeDataset = async () => {
    response = await apiContext.delete(`/datasets/${dataset.id}/`);
    expect(response.ok()).toBeTruthy();
  };

  return [dataset, disposeDataset];
};
