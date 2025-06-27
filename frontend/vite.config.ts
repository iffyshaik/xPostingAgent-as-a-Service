import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1", // ✅ Force IPv4
    proxy: {
      "/auth": "http://127.0.0.1:8000",
      "/users": "http://127.0.0.1:8000",
      "/content": "http://127.0.0.1:8000",
      "/pipeline": "http://127.0.0.1:8000"
    },
  },
});
