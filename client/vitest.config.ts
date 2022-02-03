/// <reference types="vitest" />
import path from "path";
import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { config as baseConfig } from "./vite.config";

export default defineConfig({
  ...baseConfig,
  resolve: {
    alias: {
      ...baseConfig.resolve.alias,
      // Add any alias resolutions that should be mocked, because
      // they are not available unless SvelteKit runs.
      "$app/env": path.resolve("./src/__tests__/app.env.mock.ts"),
    },
  },
  plugins: [
    svelte({
      hot: !process.env.VITEST,
    }),
  ],
  test: {
    globals: true,
    environment: "jsdom",
  },
});
