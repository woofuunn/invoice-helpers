import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";


export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ["74d8-220-129-138-199.ngrok-free.app"],
    // Ngrok 代理地址 (Ngrok免費帳號是浮動地址，使用時須更新)
    proxy: {
      "/api": {
        target: "http://localhost:5000", // Flask 本地端
        changeOrigin: true,
        secure: false, // 忽略 SSL 憑證檢查
      },
    },
  },
  preview: {
    allowedHosts: ["2793-1-171-3-150.ngrok-free.app"],
    // Ngrok 代理地址 (Ngrok免費帳號是浮動地址，使用時須更新)
    proxy: {
      "/api": {
        target: "http://localhost:5000", // Flask 本地端
        changeOrigin: true,
        secure: false, // 忽略 SSL 憑證檢查
      },
    },
  },
});
