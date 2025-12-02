import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const allowedHosts = [
  'localhost',
  '127.0.0.1',
  'frontend-production-3779.up.railway.app',
];

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    allowedHosts,
  },
});
