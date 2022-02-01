import adapter from "@sveltejs/adapter-node";
import preprocess from "svelte-preprocess";

const isDev = process.env.NODE_ENV === "development";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://github.com/sveltejs/svelte-preprocess
  // for more information about preprocessors
  preprocess: preprocess(),

  kit: {
    adapter: adapter(),

    // hydrate the <div id="svelte"> element in src/app.html
    target: "#svelte",

    // Override http methods in the Todo forms
    methodOverride: {
      allowed: ["PATCH", "DELETE"],
    },

    vite: {
      ...(isDev
        ? {
            server: {
              proxy: {
                // Make the location of the API server in production (<domain>/api) available during development.
                "/api": {
                  target: "http://localhost:3579",
                  rewrite: (path) => path.replace(/^\/api/, ""), // "/api/..." -> "/..."
                },
              },
            },
          }
        : {}),
    },
  },
};

export default config;
