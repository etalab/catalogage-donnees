import type { Handle } from "@sveltejs/kit";
import { API_BROWSER_URL, API_SSR_URL } from "./env";

const shouldApplyHydrateFix = API_SSR_URL != API_BROWSER_URL;

const getApiUrl = (clientHost: string) => {
  return `http://${clientHost}/api`;
};

// See: https://kit.svelte.dev/docs/hooks#handle
export const handle: Handle = async ({ event, resolve }) => {
  const clientHost = event.url.host;

  const response = await resolve(event);

  if (shouldApplyHydrateFix && response.body) {
    // Avoid re-fetching in the browser by patching Svelte's hydration (1) data-url
    // so that it matches what the browser would request.
    // (1) See: https://kit.svelte.dev/docs/appendix#hydration
    const body = await response.text();
    const apiDataUrl = `data-url="${API_SSR_URL}`;
    const browserDataUrl = `data-url="${getApiUrl(clientHost)}`;
    const patchedBody = body.replace(apiDataUrl, browserDataUrl);
    return new Response(patchedBody, response);
  }

  return response;
};
