import { test, expect } from "@playwright/test";

test.describe("Basic form submission", () => {
  test("Visits the contribution page", async ({ page }) => {
    const titleText = "Un nom de jeu de données";
    const descriptionText = "Une longue\ndescription de jeu\nde données";

    await page.goto("/contribuer");

    const title = page.locator("form [name=title]");
    await title.fill(titleText);
    expect(await title.inputValue()).toBe(titleText);

    const description = page.locator("form [name=description]");
    await description.fill(descriptionText);
    expect(await description.inputValue()).toBe(descriptionText);

    const button = page.locator("button[type='submit']");
    const [request, response, _] = await Promise.all([
      page.waitForRequest("**/datasets/"),
      page.waitForResponse("**/datasets/"),
      button.click(),
    ]);
    expect(await button.textContent()).toContain("Contribution");
    expect(request.method()).toBe("POST");
    expect(response.status()).toBe(201);
    const json = await response.json();
    expect(json.title).toBe(titleText);
    expect(json.description).toBe(descriptionText);
    expect(json).toHaveProperty("id");
  });
});
