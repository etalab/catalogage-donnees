// Vite reads this from .env files.
// See: https://vitejs.dev/guide/env-and-mode.html#env-files
const { VITE_API_BROWSER_URL, VITE_API_SSR_URL } = import.meta.env;

export const API_BROWSER_URL = VITE_API_BROWSER_URL || "http://localhost:3579";
export const API_SSR_URL = VITE_API_SSR_URL || "http://localhost:3579";
