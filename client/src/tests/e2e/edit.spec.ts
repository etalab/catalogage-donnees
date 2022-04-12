import { expect } from "@playwright/test";
import { STATE_AUTHENTICATED, STATE_AUTHENTICATED_ADMIN } from "./constants";
import { test } from "./fixtures";

const DELETE_DATASET_BUTTON_LOCATOR = "text=Supprimer ce jeu de données";

test.describe("Edit dataset", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Visits the edit page", async ({ page, dataset }) => {
    await page.goto(`/fiches/${dataset.id}/edit`);

    // Check initial data

    const title = page.locator("form [name=title]");
    expect(await title.inputValue()).toBe(dataset.title);

    const description = page.locator("form [name=description]");
    expect(await description.inputValue()).toBe(dataset.description);

    expect(await page.isChecked("input[value='api']")).toBeTruthy();

    // Make and submit changes

    const newTitleText = "Other title";
    expect(newTitleText).not.toBe(dataset.title);
    await title.fill(newTitleText);
    expect(await title.inputValue()).toBe(newTitleText);

    const newDescriptionText = "Other description";
    expect(newDescriptionText).not.toBe(dataset.description);
    await description.fill(newDescriptionText);
    expect(await description.inputValue()).toBe(newDescriptionText);

    const apiFormat = page.locator("label[for=dataformats-api]");
    await apiFormat.uncheck();
    expect(await page.isChecked("input[value=api]")).toBeFalsy();
    const websiteFormat = page.locator("label[for=dataformats-website]");
    await websiteFormat.check();
    expect(await page.isChecked("input[value=website]")).toBeTruthy();
    const databaseFormat = page.locator("label[for=dataformats-database]");
    await databaseFormat.check();
    expect(await page.isChecked("input[value=database]")).toBeTruthy();

    const button = page.locator("button[type='submit']");
    const [request, response] = await Promise.all([
      page.waitForRequest(`**/datasets/${dataset.id}/`),
      page.waitForResponse(`**/datasets/${dataset.id}/`),
      button.click(),
    ]);
    expect(request.method()).toBe("PUT");
    expect(response.status()).toBe(200);
    const json = await response.json();
    expect(json).toHaveProperty("id");
    expect(json.title).toBe(newTitleText);
    expect(json.description).toBe(newDescriptionText);
    expect(json.formats).toStrictEqual(["database", "website"]);
  });

  test("Does not see delete button", async ({ page, dataset }) => {
    await page.goto(`/fiches/${dataset.id}/edit`);
    const deleteButton = page.locator(DELETE_DATASET_BUTTON_LOCATOR);
    await expect(deleteButton).not.toBeVisible();
  });
});

test.describe("Edit dataset as admin", () => {
  test.use({ storageState: STATE_AUTHENTICATED_ADMIN });

  test("Deletes dataset via edit page", async ({ page, dataset }) => {
    await page.goto(`/fiches/${dataset.id}/edit`);

    let confirmShown = false;
    page.on("dialog", async (dialog) => {
      expect(dialog.type()).toBe("confirm");
      confirmShown = true;
      await dialog.accept();
    });

    const deleteButton = page.locator(DELETE_DATASET_BUTTON_LOCATOR);

    await Promise.all([
      page.waitForRequest((request) => request.method() === "DELETE"),
      page.waitForResponse((response) => response.status() === 204),
      deleteButton.click(),
    ]);
    await page.waitForURL("/");
    expect(confirmShown).toBe(true);

    await page.goto(`/fiches/${dataset.id}`);
    const response = await page.waitForResponse(`**/datasets/${dataset.id}/`);
    expect(response.status()).toBe(404);
  });
});
