/// <reference types="vitest/config" />
import path from 'path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

import { config } from "dotenv";

const { parsed } = config({ path: ".env" });

export default defineConfig({
  plugins: [react()],
  root: "./",
  optimizeDeps: {
    include: ["@vitest/coverage-istanbul"],
  },
  define: {
    "import.meta.env": parsed ?? {},
  },
  test: {
    pool: "vmThreads",
    poolOptions: {
      useAtomics: true,
    },
    include: [
      "**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}",
      "src/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}",
    ],
    name: "browser",
    css: true,
    browser: {
      enabled: true,
      name: "chromium",
      headless: true,
      provider: "playwright",
    },
    setupFiles: "./setupTests.ts",
    coverage: {
      enabled: false,
      provider: "istanbul",
      exclude: [
        "dist/**",
        "**/[.]**",
        "**/*.d.ts",
        "test?(s)/**",
        "test?(-*).?(c|m)[jt]s?(x)",
        "**/*{.,-}{test,spec}?(-d).?(c|m)[jt]s?(x)",
        "**/__tests__/**",
        // "**/pages/**",
        "**/{karma,rollup,webpack,vite,vitest,jest,ava,babel,nyc,cypress,tsup,build,astro,playwright}.config.*",
        "**/vitest.{workspace,projects}.[jt]s?(on)",
        "**/.{eslint,mocha,prettier}rc.{?(c|m)js,yml}",
      ],
    },
    environmentOptions: {
      jsdom: {
        resources: 'usable',
      }
    }
  },
  resolve: {
    alias: {
      '~': path.resolve(__dirname, './src')
    },
  },
});
