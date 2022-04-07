import { Browser, expect, firefox, FullConfig } from "@playwright/test";
import { STATE_AUTHENTICATED, TEST_EMAIL, TEST_PASSWORD } from "./constants";

export default async function globalSetup(config: FullConfig): Promise<void> {
  const browser = await firefox.launch();
  await saveAuthenticatedState(browser, config);
  await browser.close();
}

async function saveAuthenticatedState(browser: Browser, config: FullConfig) {
  const page = await browser.newPage({
    baseURL: config.projects[0].use.baseURL,
  });
  await page.goto("/login");
  await page.fill("input[name='email']", TEST_EMAIL);
  await page.fill("input[name='password']", TEST_PASSWORD);
  await page.locator("button[type='submit']").click();
  const response = await page.waitForResponse("**/auth/login/");
  expect(response.status()).toBe(200); // If this fails, ensure you ran `make initdata`.
  await page.waitForURL("/");
  await page.context().storageState({ path: STATE_AUTHENTICATED });
}
