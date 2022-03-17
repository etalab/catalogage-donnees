import { expect } from "@playwright/test";
import { STATE_AUTHENTICATED } from "./constants";
import { test } from "./fixtures";

test.describe("Dataset details", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Displays dataset details", async ({ page, dataset }) => {
    await page.goto(`/fiches/${dataset.id}`);

    const title = await page.locator("h1");
    expect(title).toHaveText(dataset.title);

    const description = await page.locator("[aria-labelledby=tabpanel-resume]");
    expect(description).toHaveText(dataset.description);

    const editUrl = await page.locator("text=Proposer une modification");
    await page.pause();
    expect(await editUrl.getAttribute("href")).toBe(
      `/fiches/${dataset.id}/edit`
    );
  });
});
