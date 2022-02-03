// Vite reads this from .env files.
// See: https://vitejs.dev/guide/env-and-mode.html#env-files
const { VITE_API_PORT } = import.meta.env;

export const API_PORT = VITE_API_PORT || "3579";
