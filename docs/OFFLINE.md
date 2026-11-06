# Making a web app work offline

What this site does: once you've opened it with a connection, it keeps working without one —
reload, navigate between pages, and the previously-loaded ones still render, data included, since
the whole thing is baked into the build. This is standard PWA (Progressive Web App) technique for
§§1–3, nothing exotic, but it only shows up in guides scattered across MDN/web.dev; §4 is the part
that actually makes an app's *content* usable offline, not just its shell. Here's exactly what's
wired up, concretely, so it can be copied into another project rather than re-derived from scratch.

Four independent pieces, each worth doing on its own:

1. **A service worker** (`public/sw.js`) — caches the app shell (HTML/JS/CSS/fonts).
2. **A web app manifest** (`public/site.webmanifest`) + icons — proper home-screen install,
   not strictly "offline" but the two always travel together in practice.
3. **Registering the worker** from the app shell, carefully (dev mode and editor previews need
   to skip it, or you'll be debugging stale caches instead of your code).
4. **Syncing the actual data**, for an app whose data is too big to just bake into the build —
   the piece that matters most, and the one §§1–3 don't cover at all.

## 1. The service worker

```js
// public/sw.js — see this file for the exact, current version.
const CACHE = "yourapp-v1"; // bump this string on any change that should force a refresh
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});
self.addEventListener("fetch", (e) => {
  const req = e.request;
  const url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== self.location.origin) return; // never touch POSTs or third-party requests

  if (req.mode === "navigate") {
    // Pages: try the network first (so a new deploy shows up on reload), fall back to the
    // cached copy, and if even that's missing, fall back to the cached app shell — this is
    // what makes a client-rendered route like /en work offline even if the browser never
    // specifically cached /en itself.
    e.respondWith(
      fetch(req)
        .then((res) => { caches.open(CACHE).then((c) => c.put(req, res.clone())); return res; })
        .catch(() => caches.match(req).then((r) => r || caches.match(self.registration.scope))),
    );
    return;
  }

  // Everything else (JS, CSS, fonts, images, json): cache-first, so a repeat visit is instant
  // and works offline; still fetches once to populate the cache.
  e.respondWith(
    caches.match(req).then((hit) => hit || fetch(req).then((res) => {
      if (res.ok) caches.open(CACHE).then((c) => c.put(req, res.clone()));
      return res;
    })),
  );
});
```

Two different strategies on purpose, by request type:

- **Navigations** (`mode: "navigate"` — a page load, not a sub-resource) are **network-first**:
  always try for the live version, so a deploy is visible on next reload; only fall back to
  the cache when there's no connection at all.
- **Everything else** (scripts, styles, fonts, images, data files) is **cache-first**: once
  fetched, never fetched again unless the cache is cleared. This is safe because those assets
  are fingerprinted by the bundler (a new build gets a new filename), so "cached forever" never
  means "stuck on stale code" — the HTML that references them is what's network-first, and it
  points at the new filenames after a deploy.

`url.origin !== self.location.origin` is a hard line at same-origin only — nothing from a CDN
or an API on another domain gets cached or touched. That's also why this is easiest on a site
with **no backend**: every request the service worker sees is to a file the build already
produced, so there's nothing to go stale in a way that matters.

### If the app has a backend/API (read-only offline, the realistic version)

A fully static site (this one) has no API calls to worry about — the whole app, data included,
is baked into the build. Most real apps aren't that simple. The above still works for the app
shell (HTML/JS/CSS/fonts) unchanged; for API data, add a **separate, smaller, stale-while-revalidate**
path instead of trying to go fully offline-first everywhere:

```js
// Add this as another branch in the fetch handler, before the generic cache-first one,
// matched to your actual API path:
if (url.pathname.startsWith("/api/") && req.method === "GET") {
  e.respondWith(
    caches.open(CACHE).then(async (c) => {
      const hit = await c.match(req);
      const fresh = fetch(req).then((res) => { if (res.ok) c.put(req, res.clone()); return res; });
      return hit || fresh.catch(() => undefined); // show the stale copy immediately if there is one
    }),
  );
  return;
}
```

This gets you "basic read-only still works" — the last-seen data renders instead of a blank
error screen — without touching writes, auth, or sync at all. A write made while offline should
just fail with a clear "you're offline" message; building a write-queue that replays later is a
real feature in its own right, not a drop-in.

## 2. The manifest and icons

`public/site.webmanifest`:

```json
{
  "name": "Full App Name",
  "short_name": "Short Name",
  "start_url": ".",
  "scope": ".",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#ffffff",
  "icons": [
    { "src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any" },
    { "src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any" },
    { "src": "icons/icon-maskable-192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable" },
    { "src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
```

`start_url` and icon `src` are **relative**, not `/absolute`: that's what lets the exact same
file work whether the app is served from the domain root or from a subpath like GitHub Pages'
`/reponame/` — relative paths resolve against the manifest's own URL, so there's no
environment-specific templating needed.

A `maskable` icon needs its artwork kept inside the centre ~80%-diameter circle, or Android's
circular/squircle crop clips it; a plain square `any` icon has no such constraint. Two sizes
of each (192, 512) covers every platform's actual request.

`apple-touch-icon.png` (180×180, flat PNG, no transparency) is separate — iOS reads that and
a few `<meta name="apple-mobile-web-app-*">` tags directly, not the manifest, for its home
screen icon and app name.

In the page `<head>`:

```html
<link rel="icon" href="/favicon.ico" type="image/x-icon" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="manifest" href="/site.webmanifest" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="default" />
<meta name="apple-mobile-web-app-title" content="Short Name" />
```

## 3. Registering the service worker

```js
useEffect(() => {
  if (!("serviceWorker" in navigator)) return;
  // Skip registering in dev (you want live code, not a cached copy) and inside an iframe
  // (an editor/preview pane showing the app — same reasoning).
  if (import.meta.env.DEV || window.self !== window.top) {
    navigator.serviceWorker.getRegistrations().then((rs) => rs.forEach((r) => r.unregister()));
    return;
  }
  navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(() => {});
}, []);
```

The dev/iframe skip is the single most common reason "offline support" quietly breaks local
development: a service worker cached in a dev tab serves itself stale JS forever until you
remember to unregister it by hand in devtools. Skipping registration in dev avoids ever hitting
that, and actively unregistering any leftover one (from before this check existed, or a stray
preview tab) cleans up the one case it could already have happened.

## 4. For real offline *use*, not just offline *loading*: sync the dataset

Everything above makes the app shell load without a connection. For an app that's really a
browsable or searchable body of data — a dictionary, a reference list, a catalogue — that's
the easy, less valuable half. The part that actually matters is getting the *data* onto the
device, once, so the real feature (search, browse, look things up) keeps working with no
connection at all. This project's own `src/data/wird.json` already works exactly this way: it's
baked into the JS bundle at build time, so there's no sync step needed — but most apps' data is
too large or changes too often for that, and need an explicit sync step instead.

The pattern (seen working, at the sibling Dagbanli dictionary project in this account — a
different technique from its service worker, which only covers its own shell):

1. **Publish the dataset as one fetchable file.** A JSON array, built and uploaded wherever the
   app's static assets already live (object storage, a CDN, a build artifact) — not a page-by-page
   API. One request gets the whole thing.
2. **Publish a small manifest alongside it**: `{ version, updatedAt, count }` or similar. Fetching
   this is cheap; fetching the full dataset is not, so check the manifest before deciding whether
   a re-sync is even worth it.
3. **On first load (or when the manifest's version has changed), download the dataset and bulk-write
   it into IndexedDB** (via a thin wrapper like Dexie, or raw `IndexedDB` — either works, Dexie is
   just less code). Chunk the insert (e.g. 500 rows at a time) so the UI thread doesn't stall on a
   large dataset, and report progress if the download is big enough that a user would otherwise
   wonder if it's frozen.
4. **Record the synced version** (`localStorage` is fine for one string) so step 2's check actually
   skips the re-download next time nothing's changed — the whole point, on a slow or metered
   connection, is paying that download cost once.
5. **Read from IndexedDB, not the network, for the actual feature.** Search, lookup, filtering —
   all of it runs against the local copy once synced. The network is only ever involved in getting
   a fresher copy, never in answering a query.

This is a genuinely different, bigger decision than the service worker: it means committing to
"the whole dataset lives on the device," which only makes sense when the data is read-heavy,
changes slowly, and is reasonably sized (megabytes, not gigabytes) — a live, frequently-written,
per-user, or genuinely huge dataset doesn't fit this pattern and shouldn't be forced into it.
Where it does fit, it's what turns "the page loads offline" into "the actual feature works
offline," which is usually the part worth having.

## Checklist for another app

1. Is it (or can its frontend be) a fully static build, or does it call a live API/backend?
   Static → the plain service worker above is enough, no changes needed. Has a backend → add
   the stale-while-revalidate branch for GET requests under §1, and accept that writes just
   fail offline for now.
2. No third-party CDNs for fonts/scripts the app depends on to render at all — a `<link>` to a
   Google Fonts URL (or any other cross-origin resource the shell needs) is a single point of
   failure for offline load, since the service worker only touches same-origin requests. Self-host
   anything load-bearing.
3. Icons: one 1024px master is enough to derive favicon.ico, apple-touch-icon.png, and the four
   manifest sizes (192/512 × any/maskable) from — same approach as this project's own icon.
4. Test it for real: load the deployed app once, then DevTools → Network → Offline, reload.
   That's the actual bar, not "the code looks right."
5. Does the app have a body of data worth browsing offline, not just a shell worth loading
   offline? If the data's small enough to bake into the build (this project's own approach),
   do that — simplest option, no sync code at all. If it's bigger or changes on its own
   schedule, that's §4 above: sync it into IndexedDB once, version it, and read from there.
