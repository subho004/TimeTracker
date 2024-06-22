import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/

import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],

  build: {
    commonjsOptions: {
      transformMixedEsModules: true,
    },
  },
  optimizeDeps: {
    include: ["timeseries_pb.js", "timeseries_grpc_web_pb.js"],
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
