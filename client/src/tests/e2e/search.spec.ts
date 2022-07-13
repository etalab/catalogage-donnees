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

  test("Visits the search page and sees default results", async ({ page }) => {
    await page.goto("/fiches/search");
    const response = await page.waitForResponse("**/datasets/?**");
    const { items } = await response.json();
    expect(items.length).toBeGreaterThanOrEqual(4);
    const itemCount = await page
      .locator('[data-test-id="dataset-list-item"]')
      .count();
    expect(itemCount).toBe(items.length);
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

    await expect(page).toHaveURL("/fiches/search?q=title&page=1");
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

    await expect(page).toHaveURL("/fiches/search?q=noresultsexpected&page=1");
  });

  test("Visits the search page directly and sees results", async ({
    page,
    dataset,
  }) => {
    await page.goto(`/fiches/search?q=${dataset.title}`);
    const search = page.locator("form [name=q]");
    expect(await search.inputValue()).toBe(dataset.title);
    await page.locator(`text=/résultat(s)?/i`).waitFor();
    await page.locator(`:has-text('${dataset.title}')`).first().waitFor();
  });

  test("Sees the pagination", async ({ page }) => {
    await page.goto("/fiches/search");
    await page.locator("[data-testid='pagination-list']").waitFor();
  });
});

test.describe("Search filters", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Sees filter sections and buttons", async ({ page }) => {
    await page.goto("/fiches/search");

    await page.locator("text=Affiner la recherche").click();

    const filterPanel = page.locator("[data-test-id='filter-panel']");

    expect(await filterPanel.locator("h6").count()).toBe(3);
    await filterPanel.locator("text=Informations générales").waitFor();
    await filterPanel.locator("text=Sources et formats").waitFor();
    await filterPanel.locator("text=Mots-clés thématiques").waitFor();

    expect(await filterPanel.locator("button").count()).toBe(6);
    await filterPanel.locator("text=Couverture géographique").waitFor();
    await filterPanel.locator("text=Service producteur de la donnée").waitFor();
    await filterPanel.locator("text=Licence de réutilisation").waitFor();
    await filterPanel.locator("text=Format de mise à disposition").waitFor();
    await filterPanel.locator("text=Système d'information source").waitFor();
    await filterPanel.locator("text=Mot-clé").waitFor();
  });

  test("Filters results by geographical_coverage", async ({ page }) => {
    await page.goto("/fiches/search");

    await page.locator("text=Affiner la recherche").click();

    const filterPanel = page.locator("[data-test-id='filter-panel']");
    const geographicalCoverageButton = filterPanel.locator(
      "data-testid=couverture-geographique-button"
    );
    expect(geographicalCoverageButton).toHaveText("Rechercher...");
    await geographicalCoverageButton.click();
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

  test("Visits the search page directly and removes the geographical_coverage filter", async ({
    page,
  }) => {
    await page.goto("/fiches/search?geographical_coverage=Monde");

    await page.locator("text=Affiner la recherche").click();

    const filterPanel = page.locator("[data-test-id='filter-panel']");
    const geographicalCoverageButton = filterPanel.locator(
      "data-testid=couverture-geographique-button"
    );
    expect(geographicalCoverageButton).toHaveText("Monde");
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
    expect(itemCount).toBeGreaterThanOrEqual(4);
  });
});
