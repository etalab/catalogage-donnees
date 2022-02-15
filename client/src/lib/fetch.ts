import { browser } from "$app/env";
import { API_PORT } from "src/env";

export const getApiUrl = () => {
  if (!browser) {
    return `http://localhost:${API_PORT}/api`;
  }
  return "/api";
};
