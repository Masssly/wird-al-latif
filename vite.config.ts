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
      prerender: {
        enabled: true,
        crawlLinks: true,
        failOnError: true,
        // The crawler fetches every same-origin link it finds and writes the response
        // back to disk as a "page" — fine for routes, but for a real static file (the
        // PDF link on the home page) it reads the binary response as text and
        // overwrites the file with a corrupted copy. Every route here is extension-less,
        // so skip any crawled link that has one; it's an existing static asset already
        // in public/, not a route to prerender.
        filter: (page: { path: string }) => !/\.\w+$/.test(page.path),
      },
    }),
  },
  ...(STATIC && {
    nitro: false,
    vite: { base: BASE },
  }),
});
