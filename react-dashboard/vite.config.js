import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: '/workspace/',
  plugins: [react()],
  server: {
    proxy: {
      '/stok': 'http://localhost:8000',
      '/api': 'http://localhost:8000',
      '/santiyeler': 'http://localhost:8000',
      '/beni-tan%C4%B1': 'http://localhost:8000',
      '/login': 'http://localhost:8000',
      '/bim-viewer': 'http://localhost:8000',
    },
  },
})
