import adapter from "@sveltejs/adapter-node";
import preprocess from "svelte-preprocess";
import path from "path";
import dotenv from "dotenv";

// Vite loads .env contents into process.env for source files.
// But this is the config file from where it all begins.
// So, we need to load .env contents explicitly.
dotenv.config({
  path: path.resolve("..", ".env")
});

const API_PORT = process.env.VITE_API_PORT || "3579";

const shouldProxy = process.env.NODE_ENV === "development" && Boolean(API_PORT);

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://github.com/sveltejs/svelte-preprocess
  // for more information about preprocessors
  preprocess: preprocess(),

  kit: {
    adapter: adapter(),

    // Override http methods in the Todo forms
    methodOverride: {
      allowed: ["PATCH", "DELETE"],
    },

    vite: {
      envDir: path.resolve(".."),
      resolve: {
        alias: {
          src: path.resolve("./src"),
        },
      },
      ...(shouldProxy ? {
        server: {
          proxy: {
            // Proxy requests to /api to the local API server.
            "/api": {
              target: `http://localhost:${API_PORT}`,
              rewrite: (path) => path.replace(/^\/api/, ""), // "/api/..." -> "/..."
            },
          },
        },
      } : {}),
    }
  },
};

export default config;
