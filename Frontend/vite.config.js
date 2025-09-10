import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'https://learn-x-grow-2-r7lg.onrender.com',
        changeOrigin: true,
      },
    },
  },
})
