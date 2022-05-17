import { test, expect } from "@playwright/test";
import {
  UPDATE_FREQUENCY_LABELS,
  GEOGRAPHICAL_COVERAGE_LABELS,
} from "src/constants";
import { STATE_AUTHENTICATED } from "./constants";

test.describe("Basic form submission", () => {
  test.use({ storageState: STATE_AUTHENTICATED });

  test("Visits the contribution page", async ({ page }) => {
    const titleText = "Un nom de jeu de données";
    const descriptionText = "Une longue\ndescription de jeu\nde données";
    const producerEmailText = "un.service@exemple.gouv.fr";
    const contactEmail1Text = "contact1@mydomain.org";
    const contactEmail2Text = "contact2@mydomain.org";
    const lastUpdatedAtDate = "2000-05-05";
    const serviceText = "Ministère de l'écologie";
    const technicalSourceText = "foo/bar";
    const publishedUrlText = "https://data.gouv.fr/datasets/example";
    const tagName = "services";

    await page.goto("/contribuer");

    // "Information Générales" section

    expect(
      page
        .locator("a.fr-sidemenu__link", { hasText: "Informations générales" })
        .first()
    ).toHaveAttribute("aria-current", "page");
    const title = page.locator("form [name=title]");
    await title.fill(titleText);
    expect(await title.inputValue()).toBe(titleText);

    const description = page.locator("form [name=description]");
    await description.fill(descriptionText);
    expect(await description.inputValue()).toBe(descriptionText);

    const geographicalCoverage = page.locator(
      "form [name=geographicalCoverage]"
    );
    await geographicalCoverage.selectOption({
      label: GEOGRAPHICAL_COVERAGE_LABELS.europe,
    });

    // "Sources et formats" section

    const apiFormat = page.locator("label[for=dataformats-api]");
    await apiFormat.check();
    expect(await page.isChecked("input[value=api]")).toBeTruthy();

    const technicalSource = page.locator("form [name=technicalSource]");
    await technicalSource.fill(technicalSourceText);
    expect(await technicalSource.inputValue()).toBe(technicalSourceText);

    // "Contacts" section

    const service = page.locator("form [name=service]");
    await service.fill(serviceText);
    expect(await service.inputValue()).toBe(serviceText);

    const producerEmail = page.locator("label[for=producerEmail]");
    await producerEmail.fill(producerEmailText);
    expect(await producerEmail.inputValue()).toBe(producerEmailText);

    const contactEmail1 = page.locator("[id='contactEmails-0']");
    await contactEmail1.fill(contactEmail1Text);
    expect(await contactEmail1.inputValue()).toBe(contactEmail1Text);

    await page.locator("text='Ajouter un contact'").click();
    const contactEmail2 = page.locator("[id='contactEmails-1']");
    await contactEmail2.fill(contactEmail2Text);
    expect(await contactEmail2.inputValue()).toBe(contactEmail2Text);
    expect(
      page.locator("a.fr-sidemenu__link", { hasText: "Contacts" }).first()
    ).toHaveAttribute("aria-current", "page");

    // "Mise à jour" section

    const lastUpdatedAt = page.locator("form [name=lastUpdatedAt]");
    await lastUpdatedAt.fill("2000-05-05");
    expect(await lastUpdatedAt.inputValue()).toBe(lastUpdatedAtDate);

    const updateFrequency = page.locator("form [name=updateFrequency]");
    await updateFrequency.selectOption({
      label: UPDATE_FREQUENCY_LABELS.daily,
    });

    // "Ouverture" section

    const publishedUrl = page.locator("form [name=publishedUrl]");
    await publishedUrl.fill(publishedUrlText);
    expect(await publishedUrl.inputValue()).toBe(publishedUrlText);

    // "Mots clés" section

    const tags = page.locator("form [name=tags]");

    await tags.fill(tagName);

    await tags.press("Enter");

    const selectedTag = page.locator("text=services");
    await selectedTag.waitFor();

    const button = page.locator("button[type='submit']");
    const [request, response] = await Promise.all([
      page.waitForRequest("**/datasets/"),
      page.waitForResponse("**/datasets/"),
      button.click(),
    ]);
    expect(
      page.locator("a.fr-sidemenu__link", { hasText: "Ouverture" }).first()
    ).toHaveAttribute("aria-current", "page");
    expect(request.method()).toBe("POST");
    expect(response.status()).toBe(201);
    const json = await response.json();
    expect(json.title).toBe(titleText);
    expect(json.description).toBe(descriptionText);
    expect(json.geographical_coverage).toBe("europe");
    expect(json.formats).toStrictEqual(["api"]);
    expect(json.producer_email).toBe(producerEmailText);
    expect(json.contact_emails).toEqual([contactEmail1Text, contactEmail2Text]);
    expect(json).toHaveProperty("id");
    expect(json.technical_source).toBe(technicalSourceText);
    expect(json.update_frequency).toBe("daily");
    expect(json.last_updated_at).toEqual("2000-05-05T00:00:00+00:00");
    expect(json.service).toBe(serviceText);
    expect(json.published_url).toBe(publishedUrlText);

    const hasTag = json.tags.findIndex((item) => item.name === tagName) !== -1;
    expect(hasTag).toBeTruthy();

    await page.locator("text='Modifier'").waitFor();
  });
});
