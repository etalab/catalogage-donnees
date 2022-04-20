import { test as base, expect, APIRequestContext } from "@playwright/test";
import type { Dataset } from "src/definitions/datasets";
import { getFakeDataset } from "src/tests/factories/dataset";
import { toPayload } from "src/lib/transformers/dataset";
import { ADMIN_EMAIL } from "./constants";

/**
 * These fixtures allow simplifying setup/teardown logic in tests,
 * especially for preparing server-side state.
 * See: https://playwright.dev/docs/test-fixtures
 * See: https://playwright.dev/docs/test-api-testing#sending-api-requests-from-ui-tests
 */

type AppOptions = {
  adminTestPassword: string;
};

type AppFixtures = {
  apiContext: APIRequestContext;
  adminApiToken: string;
  dataset: Dataset;
};

export type AppTestArgs = AppOptions & AppFixtures;

export const test = base.extend<AppTestArgs>({
  adminTestPassword: ["admin", { option: true }],

  apiContext: async ({ playwright }, use) => {
    const baseURL = "http://localhost:3579";
    const apiContext = await playwright.request.newContext({ baseURL });
    await use(apiContext);
    await apiContext.dispose();
  },

  adminApiToken: async ({ apiContext, adminTestPassword }, use) => {
    const data = {
      email: ADMIN_EMAIL,
      password: adminTestPassword,
    };
    const response = await apiContext.post("/auth/login/", { data });
    expect(response.ok()).toBeTruthy();
    const { api_token: apiToken } = await response.json();
    await use(apiToken);
  },

  dataset: async ({ apiContext, adminApiToken }, use) => {
    const data = getFakeDataset({
      title: "Sample title",
      description: "Sample description",
      updateFrequency: "never",
      formats: ["api"],
      technicalSource: "foo/baz",
      geographicalCoverage: "world",
    });
    let response = await apiContext.post("/datasets/", {
      data: toPayload(data),
    });
    expect(response.ok()).toBeTruthy();
    const dataset = await response.json();

    await use(dataset);

    response = await apiContext.delete(`/datasets/${dataset.id}/`, {
      headers: { Authorization: `Bearer ${adminApiToken}` },
    });
    expect(response.ok()).toBeTruthy();
  },
});
