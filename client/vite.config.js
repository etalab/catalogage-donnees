import { defineConfig } from "vite";
import path from "path";
import dotenv from "dotenv";

// Vite loads .env contents into process.env for source files.
// But this is the config file from where it all begins.
// So, we need to load .env contents explicitly.
dotenv.config({
  path: path.resolve("..", ".env"),
});

function getProxy() {
  // Return the proxy to use for the Vite dev server (not used in production).
  // See: https://vitejs.dev/config/#server-proxy
  const API_PORT = process.env.VITE_API_PORT || "3579";

  return {
    // Proxy requests to /api to the local API server.
    // We need this in development to match the live configuration
    // which exposes the API on /api on the web server.
    "/api": {
      target: `http://localhost:${API_PORT}`,
      rewrite: (path) => path.replace(/^\/api/, ""), // "/api/..." -> "/..."
    },
  };
}

/**
 * @type {import('vite').UserConfig}
 */
export const config = {
  envDir: path.resolve(".."),
  resolve: {
    alias: {
      src: path.resolve("./src"),
      $lib: path.resolve("./src/lib"),
    },
  },
  server: {
    proxy: getProxy(),
  },
};

export default defineConfig(config);
