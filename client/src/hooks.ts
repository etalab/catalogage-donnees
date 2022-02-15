import type { Handle } from "@sveltejs/kit";

const getApiUrl = (clientHost: string): string => {
  return `http://${clientHost}/api/`;
};

// See: https://kit.svelte.dev/docs/hooks#handle
export const handle: Handle = async ({ event, resolve }) => {
  const clientHost = event.url.host;

  const response = await resolve(event);

  if (response.body) {
    // Avoid re-fetching in the browser by patching Svelte's hydration (1) data-url
    // so that it matches what the browser would request.
    // (1) See: https://kit.svelte.dev/docs/appendix#hydration
    const body = await response.text();
    const apiDataUrl = /data-url="http(s?):\/\/[^/]+\//g
    const clientDataUrl = `data-url="${getApiUrl(clientHost)}`;
    const patchedBody = body.replace(apiDataUrl, clientDataUrl);
    return new Response(patchedBody, response);
  }

  return response;
};
