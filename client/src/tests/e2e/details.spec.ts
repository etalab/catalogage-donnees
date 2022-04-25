import { expect } from "@playwright/test";
import { STATE_AUTHENTICATED } from "./constants";
import { test } from "./fixtures";

test.describe("Dataset details", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Displays dataset details", async ({ page, dataset }) => {
    await page.goto(`/fiches/${dataset.id}`);

    const title = page.locator("h1");
    expect(title).toHaveText(dataset.title);

    const description = page.locator("[data-testid=dataset-description]");
    expect(description).toHaveText(dataset.description);

    const editUrl = page.locator("text=Modifier");
    await page.pause();
    expect(await editUrl.getAttribute("href")).toBe(
      `/fiches/${dataset.id}/edit`
    );
  });
});
