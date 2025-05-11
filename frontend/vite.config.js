import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',      // allows access via public IP or 0.0.0.0
    port: 3000,      // must match Docker exposed port
    strictPort: true // avoid fallback to other ports
  }
})
