import { expect } from "@playwright/test";
import { test } from "./fixtures.js";

test.describe("Search", () => {
  test("Performs a search from the home page", async ({ page, dataset }) => {
    await page.goto("/");

    const search = page.locator("form [name=q]");
    await search.fill("title");
    expect(await search.inputValue()).toBe("title");

    const button = page.locator("button[type='submit']");
    const [request, response, _] = await Promise.all([
      page.waitForRequest("**/datasets/?q=title"),
      page.waitForResponse("**/datasets/?q=title"),
      button.click(),
    ]);
    expect(request.method()).toBe("GET");
    expect(response.status()).toBe(200);
    const json = await response.json();
    expect(json.length).toBeGreaterThanOrEqual(1);
    expect(json[0].title).toBe(dataset.title);

    await expect(page).toHaveTitle("Rechercher un jeu de données");
    await expect(page).toHaveURL("/fiches/search?q=title");
    await page.locator(`text=/${json.length} résultat(s)?/i`).waitFor();
    await page.locator(`text='${dataset.title}'`).first().waitFor();
  });

  test("Vists the search page and performs two searches", async ({
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

    let search = page.locator("form [name=q]");
    await search.fill("title");
    expect(await search.inputValue()).toBe("title");

    const button = page.locator("button[type='submit']");
    let [request, response, _] = await Promise.all([
      page.waitForRequest("**/datasets/?q=title"),
      page.waitForResponse("**/datasets/?q=title"),
      button.click(),
    ]);
    expect(request.method()).toBe("GET");
    expect(response.status()).toBe(200);
    let json = await response.json();
    expect(json.length).toBeGreaterThanOrEqual(1);
    expect(json[0].title).toBe(dataset.title);

    await expect(page).toHaveURL("/fiches/search?q=title");
    await page.locator(`text=/${json.length} résultat(s)?/i`).waitFor();
    await page.locator(`text='${dataset.title}'`).first().waitFor();

    // Second search. Aim at getting no results.

    search = page.locator("form [name=q]");
    await search.fill("noresultsexpected");
    expect(await search.inputValue()).toBe("noresultsexpected");

    [request, response, _] = await Promise.all([
      page.waitForRequest("**/datasets/?q=noresultsexpected"),
      page.waitForResponse("**/datasets/?q=noresultsexpected"),
      button.click(),
    ]);
    expect(request.method()).toBe("GET");
    expect(response.status()).toBe(200);
    json = await response.json();
    expect(json.length).toBe(0);

    await expect(page).toHaveURL("/fiches/search?q=noresultsexpected");
    await page.locator("text='0 résultats'").waitFor();
  });
});
