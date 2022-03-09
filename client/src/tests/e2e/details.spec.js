import { expect } from "@playwright/test";
import { test } from "./fixtures.js";

test.describe("Dataset details", () => {
  test("displays dataset details", async ({ page, dataset }) => {
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