import { resolve } from 'path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 8080,
  },
  build: {
    rollupOptions: {
      input: {
        app: resolve(__dirname, 'index.html'),
        appKgChat: resolve(__dirname, 'use-cases/chat-with-kg/index.html'),
      },
    },
  },
})
