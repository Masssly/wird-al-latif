// The shared config already sets up TanStack Start, React, Tailwind, the @ path
// alias and the build target. Adding those plugins here again breaks the build;
// pass extra settings through defineConfig({ vite: { ... } }) instead.
import { defineConfig } from "@lovable.dev/vite-tanstack-config";

// GitHub Pages build (set by .github/workflows/pages.yml): every page is
// prerendered to static HTML and served under BASE_PATH (e.g. /wird-al-latif/).
// Without STATIC_SITE=1 (local development, other hosts) the defaults apply.
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
