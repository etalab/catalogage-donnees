import { test, expect } from "@playwright/test";

test.describe("Catalog list", () => {
  test("Visits the home page", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle("Catalogue");

    const link = page.locator("text='Voir'").first();
    await link.click();
    await page.locator("text='Fiche de données'").waitFor();
  });
});
