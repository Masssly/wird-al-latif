import raw from "@/data/wird.json";

export type Seg = string | { morning: string; evening: string };
export type Text = string | Seg[];
export type When = "morning" | "evening";

export type Verse = { key: string; aya: number; ar: string };
export type Item = {
  id: string;
  repeat: number;
  kind: "dua" | "quran" | "quote";
  arabic?: Text;
  ref?: string;
  sura?: number;
  basmala?: boolean;
  verses?: Verse[];
};
export type Section = { id: string; items: Item[] };
export type LangMeta = {
  lang: string;
  name: string;
  native_name: string;
  status: "draft" | "reviewed" | "verified";
  translator: string | null;
  reviewers: string[];
  source: string;
  licence: string;
  version: string;
};
export type Lang = {
  meta: LangMeta;
  ui: { label?: string; from_quran?: string };
  sections: Record<string, { title: string; description: string }>;
  headings: Record<string, string>;
  items: Record<string, Text>;
  quran: {
    type: "quranenc" | "transcription";
    name?: string;
    version?: string;
    url?: string;
    translator?: string;
    status?: string;
    online?: string;
    basmala: string;
    verses: Record<string, string>;
  };
};
export type WirdData = {
  edition: string;
  title: string;
  basmala: string;
  sections: Section[];
  translit: {
    meta: Record<string, string>;
    basmala: string;
    quran: Record<string, string>;
    items: Record<string, Text>;
  };
  langs: Record<string, Lang>;
};

export const WIRD = raw as unknown as WirdData;
export const COMPILER = "Mohammed Sadat Abdulai";
/** Display order of languages on the site: alphabetical by native name, Arabic first (the source language). */
export const LANG_ORDER = ["dag", "de", "en", "ha"].filter((c) => c in WIRD.langs);
export const isLang = (c: string) => c in WIRD.langs;
export const getLang = (c: string): Lang => (WIRD.langs[c] ?? WIRD.langs["en"])!;

export const allItems = () => WIRD.sections.flatMap((s) => s.items);

/** Flatten a text field for one time of day; `changed` marks the morning/evening words. */
export function segments(text: Text, when: When): { t: string; changed: boolean }[] {
  if (typeof text === "string") return [{ t: text, changed: false }];
  return text.map((s) => (typeof s === "string" ? { t: s, changed: false } : { t: s[when], changed: true }));
}

export const hasVariants = (text?: Text) =>
  Array.isArray(text) && text.some((s) => typeof s !== "string");

export function itemHasVariants(item: Item) {
  return hasVariants(item.arabic) || hasVariants(WIRD.translit.items[item.id]);
}

/** Default time of day from the local clock: morning from 03:00 until 15:00. */
export function defaultWhen(d = new Date()): When {
  const h = d.getHours();
  return h >= 3 && h < 15 ? "morning" : "evening";
}

// ------------------------------------------------------------ colour coding
// Port of the edition 1.0 PDF rules in pdf/build.py (see REVIEW.md R-B1 for one difference).
export type Tok = { t: string; c?: "allah" | "nabi" | "silent" };

const ZWJ = "‍";
const SUN = new Set("تثدذرزسشصضطظلن");
const RIGHT_ONLY = new Set("اأإآٱدذرزوؤةء");
const AR_WORD = /[ء-ٰٟ-ۜ۟-ۭ]+/g;
const MN = /\p{Mn}/u;

const baseForm = (w: string) =>
  [...w].filter((c) => !MN.test(c)).map((c) => (c === "ٱ" ? "ا" : c)).join("");

function clusters(w: string) {
  const cl: string[] = [];
  for (const c of w) {
    if (cl.length && MN.test(c)) cl[cl.length - 1] += c;
    else cl.push(c);
  }
  return cl;
}

function colourWord(w: string, uthmani: boolean): Tok[] {
  const b = baseForm(w);
  if (b.includes("لله")) return [{ t: w, c: "allah" }];
  if (b.includes("محمد")) return [{ t: w, c: "nabi" }];
  const cl = clusters(w);
  const silent = cl.map((c, i) => {
    let s = false;
    if (c === "ل" && i + 1 < cl.length && SUN.has(cl[i + 1]![0]!) && cl[i + 1]!.includes("ّ")) s = true;
    if (uthmani && c.includes("ْ")) s = true;
    return s;
  });
  if (!silent.some(Boolean)) return [{ t: w }];
  const out: Tok[] = [];
  let i = 0;
  while (i < cl.length) {
    let j = i;
    while (j < cl.length && silent[j] === silent[i]) j++;
    const lead = i > 0 && !RIGHT_ONLY.has(cl[i - 1]![0]!) ? ZWJ : "";
    const trail = j < cl.length && !RIGHT_ONLY.has(cl[j - 1]![0]!) ? ZWJ : "";
    const seg = lead + cl.slice(i, j).join("") + trail;
    out.push(silent[i] ? { t: seg, c: "silent" } : { t: seg });
    i = j;
  }
  return out;
}

function splitBy(s: string, rx: RegExp, fn: (m: string) => Tok[]): Tok[] {
  const out: Tok[] = [];
  let last = 0;
  for (const m of s.matchAll(rx)) {
    if (m.index! > last) out.push({ t: s.slice(last, m.index) });
    out.push(...fn(m[0]));
    last = m.index! + m[0].length;
  }
  if (last < s.length) out.push({ t: s.slice(last) });
  return out;
}

export const colourArabic = (s: string, uthmani: boolean) => splitBy(s, AR_WORD, (w) => colourWord(w, uthmani));

const TR_ALLAH = /[\p{L}\p{N}_ʾʿ-]*llāh[\p{L}\p{N}_ʾʿ]*/gu;
const TR_NABI = /Muḥammad[\p{L}]*/gu;
const EN_ALLAH = /\b(?:Allahs?|Naawuni)\b/g;
const EN_NABI = /\bMuhammads?\b/g;

function colourLatinWith(s: string, a: RegExp, n: RegExp): Tok[] {
  return splitBy(s, a, (m) => [{ t: m, c: "allah" }]).flatMap((tok) =>
    tok.c ? [tok] : splitBy(tok.t, n, (m) => [{ t: m, c: "nabi" }]),
  );
}
export const colourTranslit = (s: string) => colourLatinWith(s, TR_ALLAH, TR_NABI);
export const colourMeaning = (s: string) => colourLatinWith(s, EN_ALLAH, EN_NABI);
