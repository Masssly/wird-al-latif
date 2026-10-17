import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

// A package left over in node_modules hides a missing entry in package.json
// until a clean install (CI, Lovable) breaks the build.
const pkg = JSON.parse(readFileSync("package.json", "utf8"));
const declared = new Set([...Object.keys(pkg.dependencies), ...Object.keys(pkg.devDependencies)]);

function files(dir: string): string[] {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory()
      ? files(join(dir, e.name))
      : /\.(tsx?|css)$/.test(e.name)
        ? [join(dir, e.name)]
        : [],
  );
}

function packageName(spec: string) {
  const parts = spec.split("/");
  return spec.startsWith("@") ? parts.slice(0, 2).join("/") : parts[0]!;
}

describe("dependencies", () => {
  it("declares every package the site imports", () => {
    const missing: string[] = [];
    for (const f of [...files("src"), "scripts/build-wird-data.ts"]) {
      const src = readFileSync(f, "utf8");
      for (const [, spec] of src.matchAll(/(?:from|import)\s*\(?\s*["']([^"'./][^"']*)["']/g)) {
        if (/^(@\/|node:|virtual:)/.test(spec!)) continue;
        const name = packageName(spec!);
        if (!declared.has(name)) missing.push(`${name} (${f})`);
      }
    }
    expect(missing).toEqual([]);
  });
});
