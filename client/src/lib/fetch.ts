import { browser } from "$app/env";
import { API_PORT } from "src/env";

export const getApiUrl = () => {
  if (!browser) {
    // During SSR, request the local API server directly,
    // no need to travel through the Internet.
    return `http://localhost:${API_PORT}`;
  }
  // In the browser, request /api on the current domain.
  // * This works in production because this will use
  //   https://<domain>/api/..., which is the public URL to the
  //   API server.
  // * This works in development because Vite is configured
  //   to proxy localhost:3000/api/... to the local API server.
  // (We can't just switch on `NODE_ENV` because we don't have access
  // to `process.env` from here.)
  return "/api";
};
