// Vite reads this from .env files.
// See: https://vitejs.dev/guide/env-and-mode.html#env-files
const { VITE_API_BROWSER_URL, VITE_API_SSR_URL } = import.meta.env;

const stringOnly = (value: any) =>
  typeof value === "string" ? value : undefined;

export const API_BROWSER_URL =
  stringOnly(VITE_API_BROWSER_URL) || "http://localhost:3579";
export const API_SSR_URL =
  stringOnly(VITE_API_SSR_URL) || "http://localhost:3579";
