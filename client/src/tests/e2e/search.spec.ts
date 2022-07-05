import {
  expect,
  type Page,
  type Request,
  type Response,
} from "@playwright/test";
import { STATE_AUTHENTICATED } from "./constants";
import { test } from "./fixtures";

const performASearch = async (
  page: Page,
  searchValue: string
): Promise<[Request, Response]> => {
  const search = page.locator("form [name=q]");
  await search.fill(searchValue);

  expect(await search.inputValue()).toBe(searchValue);

  const button = page.locator("button[type='submit']");
  const [request, response] = await Promise.all([
    page.waitForRequest("**/datasets/?**"),
    page.waitForResponse("**/datasets/?**"),
    button.click(),
  ]);

  expect(request.method()).toBe("GET");
  const searchParams = new URLSearchParams(request.url());

  if (searchValue) {
    expect(searchParams.get("q")).toBe(searchValue);
  }

  expect(response.status()).toBe(200);

  return [request, response];
};

test.describe("Search", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Performs a search from the home page", async ({ page, dataset }) => {
    await page.goto("/");

    const [, response] = await performASearch(page, "title");

    const { items } = await response.json();
    expect(items.length).toBeGreaterThanOrEqual(1);
    expect(items[0].title).toBe(dataset.title);

    await expect(page).toHaveTitle("Rechercher un jeu de données");
    await expect(page).toHaveURL("/fiches/search?q=title");
    await page.locator(`text=/${items.length} résultat(s)?/i`).waitFor();
    await page.locator(`:has-text('${dataset.title}')`).first().waitFor();
  });

  test("Visits the search page and performs two searches", async ({
    page,
    dataset,
  }) => {
    await page.goto("/");

    const link = page.locator("a >> text='Rechercher'");
    await link.click();
    await page.waitForLoadState();

    await expect(page).toHaveTitle("Rechercher un jeu de données");
    await expect(page).toHaveURL("/fiches/search");

    // First search.

    const [, response] = await performASearch(page, "title");

    const { items } = await response.json();
    expect(items.length).toBeGreaterThanOrEqual(1);
    expect(items[0].title).toBe(dataset.title);

    await expect(page).toHaveURL("/fiches/search?q=title");
    await page.locator(`text=/${items.length} résultat(s)?/i`).waitFor();
    await page.locator(`:has-text('${dataset.title}')`).first().waitFor();

    // Second search. Aim at getting no results.

    const [secondRequest, secondResponse] = await performASearch(
      page,
      "noresultsexpected"
    );
    expect(new URLSearchParams(secondRequest.url()).get("q")).toBe(
      "noresultsexpected"
    );
    expect(secondRequest.method()).toBe("GET");
    expect(secondResponse.status()).toBe(200);
    const { items: secondCallItems } = await secondResponse.json();
    expect(secondCallItems.length).toBe(0);

    await expect(page).toHaveURL("/fiches/search?q=noresultsexpected");
  });

  test("should see 3 filter sections", async ({ page }) => {
    await page.goto("/");

    await performASearch(page, "crous");

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

    await performASearch(page, "crous");

    await page.locator("text=Affiner la recherche").click();
    await page
      .locator("[data-testid='couverture-geographique-button']")
      .click();
    const option = page.locator("li:has-text('Monde')").first();

    const [request, response] = await Promise.all([
      page.waitForRequest("**/datasets/?**"),
      page.waitForResponse("**/datasets/?**"),
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

    await performASearch(page, "crous");

    await page.locator("text=Affiner la recherche").click();
    const geographicalCoverageButton = await page.locator(
      "[data-testid='couverture-geographique-button']"
    );

    await geographicalCoverageButton.click();

    const option = page.locator("li:has-text('Monde')").first();

    const [request, response] = await Promise.all([
      page.waitForRequest("**/datasets/?**"),
      page.waitForResponse("**/datasets/?**"),
      option.click(),
    ]);
    expect(request.method()).toBe("GET");
    expect(response.status()).toBe(200);

    await geographicalCoverageButton.click();

    const resetOption = page
      .locator("li:has-text('Réinitialiser le filtre')")
      .first();

    await Promise.all([
      page.waitForRequest("**/datasets/?**"),
      page.waitForResponse("**/datasets/?**"),
      resetOption.click(),
    ]);

    const itemCount = await page
      .locator('[data-test-id="dataset-list-item"]')
      .count();
    expect(itemCount).toBe(2);
  });

  test("the search page should display several items by default", async ({
    page,
  }) => {
    await page.goto("/fiches/search");

    await Promise.all([
      page.waitForRequest("**/datasets/?**"),
      page.waitForResponse("**/datasets/?**"),
    ]);

    const itemCount = await page
      .locator('[data-test-id="dataset-list-item"]')
      .count();
    expect(itemCount).toBe(6);
  });

  test("permform an empty search query all items", async ({
    dataset,
    page,
  }) => {
    await page.goto("/");

    const link = page.locator("a >> text='Rechercher'");
    await link.click();
    await page.waitForLoadState();

    await expect(page).toHaveTitle("Rechercher un jeu de données");
    await expect(page).toHaveURL("/fiches/search");

    // First search.

    const [, response] = await performASearch(page, "title");

    const { items } = await response.json();
    expect(items.length).toBeGreaterThanOrEqual(1);
    expect(items[0].title).toBe(dataset.title);

    await expect(page).toHaveURL("/fiches/search?q=title");
    await page.locator(`text=/${items.length} résultat(s)?/i`).waitFor();
    await page.locator(`:has-text('${dataset.title}')`).first().waitFor();

    // Second search. Aim at getting no results.

    const [secondRequest, secondResponse] = await performASearch(page, "");

    expect(secondRequest.method()).toBe("GET");
    expect(secondResponse.status()).toBe(200);
    const { items: secondCallItems } = await secondResponse.json();
    expect(secondCallItems.length).toBe(7);

    await expect(page).toHaveURL("/fiches/search");
  });
});
