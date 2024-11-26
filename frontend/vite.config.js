/* eslint-disable no-undef */
import { defineConfig,loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

import { ViteImageOptimizer } from "vite-plugin-image-optimizer";
import viteCompression from "vite-plugin-compression";


// https://vite.dev/config/
export default defineConfig(({mode})=>{
  process.env = { ...process.env, ...loadEnv(mode, process.cwd(), "") }
  const config = {
    plugins: [react(), viteCompression(), ViteImageOptimizer()],
    root: "./src",
    define:{
      "process.env": process.env
    },
    build: {
      outDir: resolve(__dirname, "../static/reactUI"),
      emptyOutDir: true,
      assetsDir: ".",
      manifest: true,
      cssMinify: "lightningcss",
      cssCodeSplit: false,
      sourcemap: false,
      minify: "terser",
      terserOptions: {
        parse: { html5_comments: false },
        compress: {
          arrows: false,
          drop_console: true,
          passes: 2,
        },
        format: {
          comments: false,
          indent_level: 1,
        },
      },
      rollupOptions: {
        output: {
          entryFileNames: "[name].js",
          chunkFileNames: "[name]-[hash].js",
          assetFileNames: "[name].[ext]",
        },
      },
    },
  }
  if (mode === "production") {
    config['base'] = "/static/reactUI/"
  }
  return config
});
