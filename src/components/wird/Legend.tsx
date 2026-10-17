import { colourArabic } from "@/lib/wird";

/** ٱلشَّمۡسِ, code point for code point as in pdf/build.py's legend example. */
const SHAMS = "ٱلشَّمۡسِ";

export function Legend() {
  const ex = colourArabic(SHAMS, true);
  return (
    <ul className="space-y-2.5 text-sm">
      <li className="flex gap-3">
        <span className="mt-1 size-3 shrink-0 rounded-full bg-allah" />
        <span>
          <b className="text-allah">Allah</b> is red in the Arabic, the transliteration and the meanings (also{" "}
          <b className="text-allah">Naawuni</b> in Dagbanli).
        </span>
      </li>
      <li className="flex gap-3">
        <span className="mt-1 size-3 shrink-0 rounded-full bg-nabi" />
        <span>
          The Prophet’s name, <b className="text-nabi">Muhammad</b> ﷺ, is green.
        </span>
      </li>
      <li className="flex gap-3">
        <span className="mt-1 size-3 shrink-0 rounded-full bg-silent" />
        <span>
          Grey letters are written but not pronounced:{" "}
          <bdi lang="ar" dir="rtl" className="font-quran text-xl">
            {ex.map((t, i) => (
              <span key={i} className={t.c === "silent" ? "text-silent" : undefined}>
                {t.t}
              </span>
            ))}
          </bdi>{" "}
          is read <i>ash-shams</i>.
        </span>
      </li>
      <li className="flex gap-3">
        <span className="mt-1 size-3 shrink-0 rounded-full bg-sun" />
        <span>
          Words that change between morning and evening are highlighted: <mark className="chg-morning">yellow</mark> in
          the morning, <mark className="chg-evening">blue</mark> in the evening.
        </span>
      </li>
    </ul>
  );
}
