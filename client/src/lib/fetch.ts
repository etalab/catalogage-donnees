import { API_PORT } from "src/env";

export const getApiUrl = () => {
  return `http://localhost:${API_PORT}/api`;
};
