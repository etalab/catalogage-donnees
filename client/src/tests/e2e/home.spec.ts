import { expect } from "@playwright/test";
import { STATE_AUTHENTICATED } from "./constants";
import { test } from "./fixtures";

test.describe("Catalog list", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Visits the home page", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle("Catalogue");

    await page.locator("data-test-id=dataset-list-item").first().click();

    await page.locator("text='Modifier'").waitFor();
  });

  test("Sees the pagination", async ({ page }) => {
    await page.goto("/");
    const currentPage = page.locator(
      "[data-testid='pagination-list'] [aria-current='page']"
    );
    await expect(page.locator("text=Première page")).toBeDisabled();
    await expect(page.locator("text=Page précédente")).toBeDisabled();
    await expect(currentPage).toHaveText("1");
    await expect(page.locator("text=Page suivante")).toBeDisabled();
    await expect(page.locator("text=Dernière page")).toBeDisabled();
  });

  test("could open and close the filter section", async ({ page }) => {
    await page.goto("/");

    const button = await page.locator("text=Affiner la recherche");
    const filterSection = await page.locator("[data-testid='dataset-filters']");
    expect(filterSection).not.toBeVisible();

    await button.click();

    expect(filterSection).toBeVisible();
  });

  test("should see 3 filter sections", async ({ page }) => {
    await page.goto("/");

    await page.locator("text=Affiner la recherche").click();
    const sectionTitles = await page.locator("h6");

    expect(await sectionTitles.count()).toBe(3);

    const titles = await sectionTitles.allTextContents();
    expect(titles).toEqual([
      "Informations Générales",
      "Sources et Formats",
      "Mots-clés Thématiques",
    ]);
  });

  test("should filter results by geographical_coverage", async ({ page }) => {
    await page.goto("/");

    await page.locator("text=Affiner la recherche").click();
    await page
      .locator("[data-testid='couverture-geographique-button']")
      .click();
    const option = page.locator("li:has-text('EPCI')").first();

    const [request, response] = await Promise.all([
      page.waitForRequest("**/datasets/**"),
      page.waitForResponse("**/datasets/**"),
      option.click(),
    ]);
    expect(request.method()).toBe("GET");
    expect(response.status()).toBe(200);

    const itemCount = await page
      .locator('[data-test-id="dataset-list-item"]')
      .count();
    expect(itemCount).toBe(1);
  });

  test("should remove a filter", async ({ page }) => {
    await page.goto("/");

    await page.locator("text=Affiner la recherche").click();
    const geographicalCoverageButton = await page.locator(
      "[data-testid='couverture-geographique-button']"
    );

    await geographicalCoverageButton.click();

    const option = page.locator("li:has-text('EPCI')").first();

    const [request, response] = await Promise.all([
      page.waitForRequest("**/datasets/**"),
      page.waitForResponse("**/datasets/**"),
      option.click(),
    ]);
    expect(request.method()).toBe("GET");
    expect(response.status()).toBe(200);

    await geographicalCoverageButton.click();

    const resetOption = page
      .locator("li:has-text('Réinitialiser le filtre')")
      .first();

    await Promise.all([
      page.waitForRequest("**/datasets/**"),
      page.waitForResponse("**/datasets/**"),
      resetOption.click(),
    ]);

    const itemCount = await page
      .locator('[data-test-id="dataset-list-item"]')
      .count();
    expect(itemCount).toBe(11);
  });
});
