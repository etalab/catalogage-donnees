import { test as base, expect, type APIRequestContext } from "@playwright/test";
import type { Dataset, SearchFilter } from "src/definitions/datasets";
import { toPayload } from "src/lib/transformers/dataset";
import { getFakeSearchFilter } from "../factories/dataset";
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
  datasetFilters: SearchFilter;
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
    const headers = { Authorization: `Bearer ${adminApiToken}` };

    const data = {
      id: "xxx-xxx-xxx",
      title: "Sample title",
      description: "Sample description",
      formats: ["api"],
      entrypoint_email: "jane.doe@beta.gouv.fr",
      contact_emails: ["contact@beta.gouv.fr"],
      service: "La Drac",
      technical_source: "foo/baz",
      update_frequency: "never",
      last_updated_at: new Date(),
      geographical_coverage: "world",
      tagIds: ["ceb19363-1681-4052-813c-f771d4459295"],
    };
    let response = await apiContext.post("/datasets/", {
      data: toPayload(data),
      headers,
    });

    expect(response.ok()).toBeTruthy();
    const dataset = await response.json();

    await use(dataset);

    response = await apiContext.delete(`/datasets/${dataset.id}/`, {
      headers,
    });
    expect(response.ok()).toBeTruthy();
  },
});
