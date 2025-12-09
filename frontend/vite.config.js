import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/chat': {
        target: 'https://ai-chatbot-using-llms.onrender.com',
        changeOrigin: true,
      },
      '/upload': {
        target: 'https://ai-chatbot-using-llms.onrender.com',
        changeOrigin: true,
      },
    },
  },
})
