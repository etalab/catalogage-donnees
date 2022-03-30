import { test as base, expect, APIRequestContext } from "@playwright/test";
import type { Dataset } from "src/definitions/datasets";

/**
 * These fixtures allow simplifying setup/teardown logic in tests,
 * especially for preparing server-side state.
 * See: https://playwright.dev/docs/test-fixtures
 * See: https://playwright.dev/docs/test-api-testing#sending-api-requests-from-ui-tests
 */

type AppFixtures = {
  apiContext: APIRequestContext;
  dataset: Dataset;
};

export const test = base.extend<AppFixtures>({
  apiContext: async ({ playwright }, use) => {
    const baseURL = "http://localhost:3579";
    const apiContext = await playwright.request.newContext({ baseURL });
    await use(apiContext);
    await apiContext.dispose();
  },

  dataset: async ({ apiContext }, use) => {
    const data = {
      title: "Sample title",
      description: "Sample description",
      formats: ["api"],
      entrypoint_email: "service@example.org",
    };
    let response = await apiContext.post("/datasets/", { data });
    expect(response.ok()).toBeTruthy();
    const dataset = await response.json();

    await use(dataset);

    response = await apiContext.delete(`/datasets/${dataset.id}/`);
    expect(response.ok()).toBeTruthy();
  },
});
