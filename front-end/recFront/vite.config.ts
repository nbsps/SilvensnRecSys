import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import * as path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  plugins: [vue()],
  // build: {  // build 与 flask 结合有点问题
  //   outDir: path.resolve("./dist"),
  //   assetsDir: "",
  //   manifest: true,
  //   emptyOutDir: true,
  //   target: "es2015",
  //   rollupOptions: {
  //     input: {
  //       main: path.resolve("./src/main.ts"),
  //     },
  //     output: {
  //       chunkFileNames: undefined,
  //     },
  //   },
  // },
});
