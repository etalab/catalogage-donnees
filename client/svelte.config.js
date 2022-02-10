import adapter from "@sveltejs/adapter-node";
import preprocess from "svelte-preprocess";

import vite from "./vite.config.js";

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

    vite,
  },
  onwarn: (warning, handler) => {
    const { code } = warning;
    if (code === "a11y-no-redundant-roles") return;

    handler(warning);
  },
};

export default config;
