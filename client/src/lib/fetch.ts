import { browser } from "$app/env";

export const getApiUrl = () => {
  if (!browser) {
    // During SSR, request the local API server directly.
    // This assumes the same port is used in production
    // and during development.
    return "http://localhost:3579";
  }
  // In the browser, request /api on the current domain.
  // This works in production because this will use
  // https://<domain>/api/..., which is the public URL to the
  // API server.
  // This works in development because Vite is configured
  // to proxy localhost:3000/api/... to the local API server.
  return "/api";
};
