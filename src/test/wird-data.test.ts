import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { buildWirdData, OUT_FILE, serialize } from "../../scripts/build-wird-data";

describe("src/data/wird.json", () => {
  it("is up to date with data/ and i18n/ (run: bun scripts/build-wird-data.ts)", () => {
    expect(readFileSync(OUT_FILE, "utf-8")).toBe(serialize(buildWirdData()));
  });
});
