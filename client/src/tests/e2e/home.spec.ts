import { expect } from "@playwright/test";
import { STATE_AUTHENTICATED } from "./constants";
import { test } from "./fixtures";

test.describe("Catalog list", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Visits the home page", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle("Catalogue");

    await page
      .locator("data-test-id=Catalogue des enquêtes réalisées par la DARES")
      .first()
      .click();

    await page.locator("text='Modifier'").waitFor();
  });

  test("Sees the pagination", async ({ page }) => {
    await page.goto("/");

    // Page size is 50 items, only 1 page during E2E tests.
    const currentPage = page.locator(
      "[data-testid='pagination-list'] [aria-current='page']"
    );
    await expect(page.locator("text=Première page")).toBeDisabled();
    await expect(page.locator("text=Page précédente")).toBeDisabled();
    await expect(currentPage).toHaveText("1");
    await expect(page.locator("text=Page suivante")).toBeDisabled();
    await expect(page.locator("text=Dernière page")).toBeDisabled();
  });
});
