/**
 * Builds src/data/wird.json for the website from the same YAML the PDF build
 * reads (data/, i18n/ at the repository root). Third-party Qurʾān text is
 * copied verbatim, for the verses the wird uses only, so the browser does not
 * load the 3.5 MB KFGQPC file.
 *
 * Run after changing anything in data/ or i18n/:  bun scripts/build-wird-data.ts
 * (src/test/wird-data.test.ts fails while src/data/wird.json is out of date.)
 */
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from "node:fs";
import { gunzipSync } from "node:zlib";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { parse } from "yaml";

const REPO = join(dirname(fileURLToPath(import.meta.url)), "..");
export const OUT_FILE = join(REPO, "src", "data", "wird.json");

export function buildWirdData() {
  const read = (rel: string) => readFileSync(join(REPO, rel), "utf-8");
  const yml = (rel: string) => parse(read(rel));

  const wird = yml("data/wird.yaml");
  const translit = yml("data/translit.yaml");

  const kfList: { sora: number; aya_no: number; aya_text: string }[] = JSON.parse(
    read("data/kfgqpc/data/hafsData_v18.json"),
  );
  const KF = new Map(kfList.map((x) => [`${x.sora}:${x.aya_no}`, x.aya_text]));
  const kf = (s: number, a: number, nonum = false) => {
    const t = KF.get(`${s}:${a}`)!;
    return nonum ? t.slice(0, t.lastIndexOf(" ")) : t;
  };

  function parseVerses(spec: string) {
    const m = /^(\d{1,3}):(\d{1,3})(?:-(\d{1,3}))?$/.exec(spec);
    if (!m) throw new Error(`bad verse range ${spec}`);
    const s = +m[1]!, a = +m[2]!, b = +(m[3] ?? m[2]!);
    return { s, a, b, keys: Array.from({ length: b - a + 1 }, (_, i) => `${s}:${a + i}`) };
  }

  const usedVerses: string[] = [];
  const sections = wird.sections.map((sec: any) => ({
    id: sec.id,
    items: sec.items.map((it: any) => {
      const base: any = { id: it.id, repeat: it.repeat ?? 1 };
      if (it.audio) base.audio = it.audio;
      const q = it.quran;
      if (!q) return { ...base, kind: "dua", arabic: it.arabic };
      const { s, a, keys } = parseVerses(q.verses);
      if (q.quote) {
        const full = kf(s, a);
        const i = full.indexOf(q.from_word);
        if (i < 0) throw new Error(`${it.id}: from_word not found`);
        return { ...base, kind: "quote", ref: q.verses, arabic: full.slice(i) };
      }
      usedVerses.push(...keys);
      const verses = keys.map((k) => {
        let ar = KF.get(k)!;
        if (q.opening && k === keys[0]) {
          if (!ar.startsWith(q.opening.replace)) throw new Error(`${it.id}: opening mismatch`);
          ar = q.opening.with + ar.slice(q.opening.replace.length);
        }
        return { key: k, aya: +k.split(":")[1]!, ar };
      });
      return { ...base, kind: "quran", ref: q.verses, sura: s, basmala: !!q.basmala, verses };
    }),
  }));

  const stripFn = (t: string) => t.replace(/\s*\[\d+\]/g, "").trim();
  const langs: Record<string, any> = {};
  for (const fn of readdirSync(join(REPO, "i18n")).sort()) {
    if (!fn.endsWith(".yaml")) continue;
    const d = yml(`i18n/${fn}`);
    const q = d.quran ?? {};
    const verses: Record<string, string> = {};
    let basmala = "";
    let quranSource: any = {};
    if (q.source === "quranenc") {
      const j = JSON.parse(gunzipSync(readFileSync(join(REPO, q.file))).toString("utf-8"));
      const get = (k: string) => {
        const [s, a] = k.split(":");
        return stripFn(j.verses[s!][a!].text);
      };
      for (const k of usedVerses) verses[k] = get(k);
      basmala = get("1:1");
      quranSource = {
        type: "quranenc",
        name: j.edition.name,
        version: j.edition.version ?? q.version,
        url: j.edition.sourceUrl,
      };
    } else if (q.source === "transcription") {
      const t = yml(q.file);
      for (const k of usedVerses) {
        if (!(k in t.verses)) throw new Error(`${fn}: transcription missing ${k}`);
        verses[k] = t.verses[k];
      }
      basmala = t.basmala;
      quranSource = { type: "transcription", translator: t.meta.translator, status: t.meta.status, online: t.meta.online };
    }
    langs[d.meta.lang] = {
      meta: d.meta,
      ui: d.ui ?? {},
      sections: d.sections ?? {},
      headings: d.headings ?? {},
      items: d.items ?? {},
      quran: { ...quranSource, basmala, verses },
    };
  }

  return {
    edition: wird.edition,
    title: wird.title,
    basmala: kf(1, 1, true),
    sections,
    translit: { meta: translit.meta, basmala: translit.basmala, quran: translit.quran, items: translit.items },
    langs,
  };
}

export const serialize = (data: unknown) => JSON.stringify(data);

// Run directly: write the file.
if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const out = buildWirdData();
  mkdirSync(dirname(OUT_FILE), { recursive: true });
  writeFileSync(OUT_FILE, serialize(out));
  console.log("items:", out.sections.reduce((n: number, s: any) => n + s.items.length, 0), "langs:", Object.keys(out.langs));
}
