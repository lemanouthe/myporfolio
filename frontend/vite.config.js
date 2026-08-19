import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// In prod the app is served by Django/WhiteNoise under /static/, so built asset
// URLs must be prefixed accordingly. In dev the Vite server serves at root and
// proxies /api + /media to the backend (reproduces the prod same-origin setup).
export default defineConfig(({ mode }) => ({
  plugins: [vue()],
  base: mode === "production" ? "/static/" : "/",
  server: {
    // Port fixe + échoue si occupé (au lieu de basculer en 5174 silencieusement).
    port: 5173,
    strictPort: true,
    proxy: {
      "/api": "http://localhost:8000",
      "/media": "http://localhost:8000",
    },
    // HMR fiable : polling du système de fichiers (utile si le watcher natif
    // rate des modifications). Recharge le navigateur à chaque sauvegarde.
    watch: {
      usePolling: true,
      interval: 300,
    },
  },
}));
