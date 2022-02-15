import { browser } from "$app/env";
import { API_BROWSER_URL, API_SSR_URL } from "src/env";

export const getApiUrl = () => {
  if (browser) {
    // This is:
    // * http://localhost:3579 on local.
    // * /api when live (sends requests to Nginx, which serves the frontend app).
    return API_BROWSER_URL;
  }
  // This is always http://localhost:3579.
  // In live environments (prod/staging/etc), this ensures we don't travel the Internet
  // when making requests during SSR (Server-Side Rendering).
  return API_SSR_URL;
};
