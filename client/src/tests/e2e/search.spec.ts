import { expect } from "@playwright/test";
import { STATE_AUTHENTICATED } from "./constants";
import { test } from "./fixtures";

test.describe("Search", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Performs a search from the home page", async ({ page, dataset }) => {
    await page.goto("/");

    const search = page.locator("form [name=q]");
    await search.fill("title");
    expect(await search.inputValue()).toBe("title");

    const button = page.locator("button[type='submit']");
    const [request, response] = await Promise.all([
      page.waitForRequest((req) => req.url().includes("/datasets/")),
      page.waitForResponse((resp) => resp.url().includes("/datasets/")),
      button.click(),
    ]);
    expect(request.method()).toBe("GET");
    const searchParams = new URLSearchParams(request.url());
    expect(searchParams.get("q")).toBe("title");
    expect(response.status()).toBe(200);
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

    let search = page.locator("form [name=q]");
    await search.fill("title");
    expect(await search.inputValue()).toBe("title");

    const button = page.locator("button[type='submit']");
    let [request, response] = await Promise.all([
      page.waitForRequest((req) => req.url().includes("/datasets/")),
      page.waitForResponse((resp) => resp.url().includes("/datasets/")),
      button.click(),
    ]);
    expect(request.method()).toBe("GET");
    const searchParams = new URLSearchParams(request.url());
    expect(searchParams.get("q")).toBe("title");
    expect(response.status()).toBe(200);
    let { items } = await response.json();
    expect(items.length).toBeGreaterThanOrEqual(1);
    expect(items[0].title).toBe(dataset.title);

    await expect(page).toHaveURL("/fiches/search?q=title");
    await page.locator(`text=/${items.length} résultat(s)?/i`).waitFor();
    await page.locator(`:has-text('${dataset.title}')`).first().waitFor();

    // Second search. Aim at getting no results.

    search = page.locator("form [name=q]");
    await search.fill("noresultsexpected");
    expect(await search.inputValue()).toBe("noresultsexpected");

    [request, response] = await Promise.all([
      page.waitForRequest((req) => req.url().includes("/datasets/")),
      page.waitForResponse((resp) => resp.url().includes("/datasets/")),
      button.click(),
    ]);
    expect(new URLSearchParams(request.url()).get("q")).toBe(
      "noresultsexpected"
    );
    expect(request.method()).toBe("GET");
    expect(response.status()).toBe(200);
    ({ items } = await response.json());
    expect(items.length).toBe(0);

    await expect(page).toHaveURL("/fiches/search?q=noresultsexpected");
  });
});
