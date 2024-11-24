import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import tsconfigPaths from 'vite-tsconfig-paths'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tsconfigPaths()
  ],
  resolve: {
    alias: {
      '~': path.resolve(__dirname, './src'),
    },
  },
  test: {
    environment: 'jsdom',
    setupFiles: ['./setupTests.ts'],
    alias: {
      '~': path.resolve(__dirname, './src')
    },
    coverage: {
      reporter: ['text', 'json', 'html'],
    },
    globals: true,
    viewport: {
      width: 1920,
      height: 1080,
    },
    snapshotFormat: {
      printBasicPrototype: false,
    }
  }
});