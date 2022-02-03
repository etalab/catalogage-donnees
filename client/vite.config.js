import { defineConfig } from "vite";
import path from "path";
import dotenv from "dotenv";

// Vite loads .env contents into process.env for source files.
// But this is the config file from where it all begins.
// So, we need to load .env contents explicitly.
dotenv.config({
  path: path.resolve("..", ".env"),
});

const API_PORT = process.env.VITE_API_PORT || "3579";

const shouldProxy = process.env.NODE_ENV === "development" && Boolean(API_PORT);

export const config = {
  envDir: path.resolve(".."),
  resolve: {
    alias: {
      src: path.resolve("./src"),
      $lib: path.resolve("./src/lib"),
    },
  },
  server: {
    proxy: shouldProxy
      ? {
          // Proxy requests to /api to the local API server.
          "/api": {
            target: `http://localhost:${API_PORT}`,
            rewrite: (path) => path.replace(/^\/api/, ""), // "/api/..." -> "/..."
          },
        }
      : null,
  },
};

export default defineConfig(config);
