import { test, expect } from "@playwright/test";
import { UPDATE_FREQUENCY } from "src/constants";
import { STATE_AUTHENTICATED } from "./constants";

test.describe("Basic form submission", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Visits the contribution page", async ({ page }) => {
    const titleText = "Un nom de jeu de données";
    const descriptionText = "Une longue\ndescription de jeu\nde données";
    const entrypointEmailText = "un.service@exemple.gouv.fr";
    const contactEmail1Text = "contact1@example.org";
    const contactEmail2Text = "contact2@example.org";
    const lastPublishedAtDate = "2000-05-05";
    const serviceText = "Ministère de l'écologie"

    await page.goto("/contribuer");

    // "Information Générales" section

    const title = page.locator("form [name=title]");
    await title.fill(titleText);
    expect(await title.inputValue()).toBe(titleText);

    const description = page.locator("form [name=description]");
    await description.fill(descriptionText);
    expect(await description.inputValue()).toBe(descriptionText);

    const apiFormat = page.locator("label[for=dataformats-api]");
    await apiFormat.check();
    expect(await page.isChecked("input[value=api]")).toBeTruthy();

    const service = page.locator("form [name=service]");
    await service.fill(serviceText);
    expect(await service.inputValue()).toBe(serviceText);

    const entrypointEmail = page.locator("label[for=entrypoint-email]");
    await entrypointEmail.fill(entrypointEmailText);
    expect(await entrypointEmail.inputValue()).toBe(entrypointEmailText);

    const contactEmail1 = page.locator("[id='contactEmails-0']");
    await contactEmail1.fill(contactEmail1Text);
    expect(await contactEmail1.inputValue()).toBe(contactEmail1Text);

    await page.locator("text='Ajouter un contact'").click();
    const contactEmail2 = page.locator("[id='contactEmails-1']");
    await contactEmail2.fill(contactEmail2Text);
    expect(await contactEmail2.inputValue()).toBe(contactEmail2Text);


    // "Mise à jour" section

    const lastPublishedAt = page.locator("form [name=lastPublishedAt]");
    await lastPublishedAt.fill("2000-05-05");
    expect(await lastPublishedAt.inputValue()).toBe(lastPublishedAtDate);

    const updateFrequency = page.locator("#updateFrequency");
    await updateFrequency.selectOption({ label: UPDATE_FREQUENCY.daily })

    const button = page.locator("button[type='submit']");
    const [request, response] = await Promise.all([
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
    expect(json.entrypoint_email).toBe(entrypointEmailText);
    expect(json.contact_emails).toEqual([contactEmail1Text, contactEmail2Text]);
    expect(json).toHaveProperty("id");
    expect(json.update_frequency).toBe("daily")
    expect(json.last_updated_at).toEqual("2000-05-05T00:00:00+00:00")

    await page.locator("text='Proposer une modification'").waitFor();
  });
});
