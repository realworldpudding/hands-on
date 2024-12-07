/// <reference types="vitest/config" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  root: "./",
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./setupTests.js'],
    pool: "vmThreads",
    poolOptions: {
      useAtomics: true,
    },
    environmentOptions: {
      jsdom: {
        resources: 'usable',
      }
    },
    include: [
      "**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}",
      "src/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}",
    ],
  },
})
