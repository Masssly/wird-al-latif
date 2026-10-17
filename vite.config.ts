// @lovable.dev/vite-tanstack-config already includes the following — do NOT add them manually
// or the app will break with duplicate plugins:
//   - TanStack devtools (dev-only, first), tanstackStart, viteReact, tailwindcss, tsConfigPaths,
//     nitro (build-only using cloudflare as a default target), VITE_* env injection, @ path alias,
//     React/TanStack dedupe, error logger plugins, and sandbox detection (port/host/strictPort).
// You can pass additional config via defineConfig({ vite: { ... }, etc... }) if needed.
import { defineConfig } from "@lovable.dev/vite-tanstack-config";

// GitHub Pages build (set by .github/workflows/pages.yml): every page is
// prerendered to static HTML and served under BASE_PATH (e.g. /wird-al-latif/).
// Lovable's own preview and publish builds ignore this and keep their defaults.
const STATIC = process.env["STATIC_SITE"] === "1";
const BASE = process.env["BASE_PATH"] || "/";

export default defineConfig({
  tanstackStart: {
    // Redirect TanStack Start's bundled server entry to src/server.ts (our SSR error wrapper).
    // nitro/vite builds from this
    server: { entry: "server" },
    ...(STATIC && {
      prerender: { enabled: true, crawlLinks: true, failOnError: true },
    }),
  },
  ...(STATIC && {
    nitro: false,
    vite: { base: BASE },
  }),
});
