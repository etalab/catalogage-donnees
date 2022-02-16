import { defineConfig } from "vite";
import path from "path";
import dotenv from "dotenv";

// Vite loads .env contents into process.env for source files.
// But this is the config file from where it all begins.
// So, we need to load .env contents explicitly.
dotenv.config({
  path: path.resolve("..", ".env"),
});

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
};

export default defineConfig(config);
