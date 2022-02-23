import { expect } from "@playwright/test";
import { STATE_AUTHENTICATED } from "./constants.js";
import { test } from "./fixtures.js";

test.describe("Catalog list", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Visits the home page", async ({ page, dataset }) => {
    await page.goto("/");

    await expect(page).toHaveTitle("Catalogue");

    const link = page.locator("text='Voir'").first();
    await link.click();
    await page.locator("text='Proposer une modification'").waitFor();
  });
});
