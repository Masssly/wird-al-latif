import { describe, expect, it } from "vitest";
import { allItems, colourArabic, colourMeaning, defaultWhen, segments, WIRD } from "@/lib/wird";

// Arabic is written as escapes so no editor can silently reorder its marks.
const ALLAHU = "\u0627\u0644\u0644\u064e\u0651\u0647\u064f"; // اللَّهُ
const SHAMS = "\u0671\u0644\u0634\u064e\u0651\u0645\u06e1\u0633\u0650"; // ٱلشَّمۡسِ

describe("wird data", () => {
  it("has the 46 items of edition 1.0", () => {
    expect(allItems()).toHaveLength(46);
  });
  it("starts 23:97 at Rabbi, without wa-qul", () => {
    const it97 = allItems().find((i) => i.id === "muminun-97")!;
    expect(it97.verses![0]!.ar.startsWith("ر")).toBe(true);
  });
  it("shows the whole basmala (all four words, no verse number)", () => {
    expect(WIRD.basmala.split(" ")).toHaveLength(4);
    expect(WIRD.basmala).not.toContain("\u00a0");
  });
  it("every language has a translation for every verse read", () => {
    const keys = allItems().flatMap((i) => i.verses?.map((v) => v.key) ?? []);
    for (const l of Object.values(WIRD.langs)) for (const k of keys) expect(l.quran.verses[k]).toBeTruthy();
  });
});

describe("morning / evening", () => {
  it("defaults to morning at 06:00 and evening at 18:00", () => {
    expect(defaultWhen(new Date(2026, 0, 1, 6))).toBe("morning");
    expect(defaultWhen(new Date(2026, 0, 1, 18))).toBe("evening");
  });
  it("picks the evening wording", () => {
    const s = segments(["a ", { morning: "M", evening: "E" }], "evening");
    expect(s.map((x) => x.t).join("")).toBe("a E");
  });
});

describe("colour code", () => {
  it("marks Allah red and Muhammad green", () => {
    expect(colourMeaning("O Allah, bless Muhammad").filter((t) => t.c).map((t) => t.c)).toEqual(["allah", "nabi"]);
    expect(colourArabic(ALLAHU, false)[0]!.c).toBe("allah");
  });
  it("greys the silent lām of ٱلشَّمۡسِ", () => {
    expect(colourArabic(SHAMS, true).some((t) => t.c === "silent")).toBe(true);
  });
});
