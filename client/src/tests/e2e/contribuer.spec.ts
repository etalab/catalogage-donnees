import { test, expect } from "@playwright/test";
import { STATE_AUTHENTICATED } from "./constants";

test.describe("Basic form submission", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Visits the contribution page", async ({ page }) => {
    const titleText = "Un nom de jeu de données";
    const descriptionText = "Une longue\ndescription de jeu\nde données";
    const entrypointEmailText = "un.service@exemple.gouv.fr";

    await page.goto("/contribuer");

    const title = page.locator("form [name=title]");
    await title.fill(titleText);
    expect(await title.inputValue()).toBe(titleText);

    const description = page.locator("form [name=description]");
    await description.fill(descriptionText);
    expect(await description.inputValue()).toBe(descriptionText);

    const apiFormat = page.locator("label[for=dataformats-api]");
    await apiFormat.check();
    expect(await page.isChecked("input[value=api]")).toBeTruthy();

    const entrypointEmail = page.locator("label[for=entrypoint-email]");
    await entrypointEmail.fill(entrypointEmailText);
    expect(await entrypointEmail.inputValue()).toBe(entrypointEmailText);

    const button = page.locator("button[type='submit']");
    const [request, response, _] = await Promise.all([
      page.waitForRequest("**/datasets/"),
      page.waitForResponse("**/datasets/"),
      button.click(),
    ]);
    expect(request.method()).toBe("POST");
    expect(response.status()).toBe(201);
    const json = await response.json();
    expect(json.title).toBe(titleText);
    expect(json.description).toBe(descriptionText);
    expect(json.formats).toStrictEqual(["api"]);
    expect(json).toHaveProperty("id");

    await page.locator("text='Proposer une modification'").waitFor();
  });
});
