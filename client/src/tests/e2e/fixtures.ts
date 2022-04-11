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
  adminApiToken: string;
  dataset: Dataset;
};

export const test = base.extend<AppFixtures>({
  apiContext: async ({ playwright }, use) => {
    const baseURL = "http://localhost:3579";
    const apiContext = await playwright.request.newContext({ baseURL });
    await use(apiContext);
    await apiContext.dispose();
  },

  adminApiToken: async ({ apiContext }, use) => {
    const data = { email: "admin@catalogue.data.gouv.fr", password: "admin" };
    const response = await apiContext.post("/auth/login/", { data });
    expect(response.ok()).toBeTruthy();
    const { api_token: apiToken } = await response.json();
    await use(apiToken);
  },

  dataset: async ({ apiContext, adminApiToken }, use) => {
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

    response = await apiContext.delete(`/datasets/${dataset.id}/`, {
      headers: { Authorization: `Bearer ${adminApiToken}` },
    });
    expect(response.ok()).toBeTruthy();
  },
});
