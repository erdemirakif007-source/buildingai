import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/stok': 'http://localhost:8000',
      '/api': 'http://localhost:8000',
      '/santiyeler': 'http://localhost:8000',
      '/bim-viewer': 'http://localhost:8000',
    },
  },
})
