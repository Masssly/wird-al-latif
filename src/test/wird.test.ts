import { describe, expect, it } from "vitest";
import { allItems, colourArabic, colourMeaning, defaultWhen, segments, WIRD } from "@/lib/wird";

describe("wird data", () => {
  it("has the 46 items of edition 1.0", () => {
    expect(allItems()).toHaveLength(46);
  });
  it("starts 23:97 at رَبِّ", () => {
    const it97 = allItems().find((i) => i.id === "muminun-97")!;
    expect(it97.verses![0].ar.startsWith("رَبِّ")).toBe(true);
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
    expect(colourArabic("اللَّهُ", false)[0].c).toBe("allah");
  });
  it("greys the silent lām of ٱلشَّمۡسِ", () => {
    expect(colourArabic("ٱلشَّمۡسِ", true).some((t) => t.c === "silent")).toBe(true);
  });
});
