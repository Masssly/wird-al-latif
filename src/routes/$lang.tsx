import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { ChevronLeft, Moon, RotateCcw, Settings2, Sun } from "lucide-react";
import { useMemo, useState } from "react";
import { ItemCard } from "@/components/wird/ItemCard";
import { ReaderSettings } from "@/components/wird/ReaderSettings";
import { StatusBadge } from "@/components/wird/StatusBadge";
import { useProgress, useSettings, useWhen } from "@/lib/reader-state";
import { getLang, isLang, WIRD } from "@/lib/wird";

export const Route = createFileRoute("/$lang")({
  beforeLoad: ({ params }) => {
    if (!isLang(params.lang)) throw notFound();
  },
  head: ({ params }) => {
    const name = WIRD.langs[params.lang]?.meta.name ?? "Reader";
    return {
      meta: [
        { title: `al-Wird al-Laṭīf — ${name} reader` },
        {
          name: "description",
          content: `Read al-Wird al-Laṭīf of Imām al-Ḥaddād morning and evening: vowelled Arabic, transliteration and ${name} meanings.`,
        },
        { property: "og:title", content: `al-Wird al-Laṭīf — ${name}` },
        {
          property: "og:description",
          content: `Morning and evening litany of Imām al-Ḥaddād with ${name} meanings.`,
        },
        { property: "og:type", content: "article" },
        { name: "twitter:card", content: "summary" },
      ],
      htmlAttrs: { lang: params.lang },
    };
  },
  component: Reader,
});

function Reader() {
  const { lang: code } = Route.useParams();
  const lang = getLang(code);
  const en = getLang("en");
  const [when, setWhen] = useWhen();
  const [settings, update] = useSettings();
  const { counts, tap, reset } = useProgress(when);
  const [open, setOpen] = useState(false);

  // The language being read, plus any others the reader chose to mix in. Never filled in
  // automatically: a language with no meaning for an item just shows nothing for it.
  const meaningLangs = useMemo(
    () =>
      settings.meaning
        ? [code, ...settings.meaningLangs.filter((c) => c !== code && isLang(c))]
        : [],
    [settings.meaning, settings.meaningLangs, code],
  );

  const numbered = useMemo(() => {
    let n = 0;
    return WIRD.sections.map((s) => ({ ...s, items: s.items.map((it) => ({ it, n: ++n })) }));
  }, []);
  const total = numbered.reduce((a, s) => a + s.items.length, 0);
  const done = numbered.reduce(
    (a, s) => a + s.items.filter(({ it }) => (counts[it.id] ?? 0) >= it.repeat).length,
    0,
  );

  return (
    <div className="reader min-h-dvh bg-background" data-size={settings.size}>
      <header className="sticky top-0 z-20 border-b border-border bg-background/90 pt-safe backdrop-blur">
        <div className="mx-auto flex h-14 max-w-2xl items-center gap-2 px-3">
          <Link
            to="/"
            className="-ml-1 flex size-11 items-center justify-center rounded-full"
            aria-label="Home"
          >
            <ChevronLeft className="size-5" />
          </Link>
          <div className="min-w-0 flex-1">
            <p
              lang="ar"
              dir="rtl"
              className="truncate text-left font-dua text-lg leading-tight text-ink"
            >
              {WIRD.title}
            </p>
            <p className="flex items-center gap-1.5 text-xs text-muted-foreground">
              {lang.meta.native_name} <StatusBadge status={lang.meta.status} />
            </p>
          </div>
          <button
            type="button"
            onClick={() => setOpen(true)}
            className="flex size-11 items-center justify-center rounded-full"
            aria-label="Reading settings"
          >
            <Settings2 className="size-5" />
          </button>
        </div>
        <div
          className="h-1 bg-muted"
          role="progressbar"
          aria-valuemin={0}
          aria-valuemax={total}
          aria-valuenow={done}
        >
          <div
            className="h-full bg-primary transition-all"
            style={{ width: `${(done / total) * 100}%` }}
          />
        </div>
      </header>

      <main className="mx-auto max-w-2xl px-4 pb-32">
        {lang.meta.lang !== "en" && Object.keys(lang.items).length === 0 && (
          <p className="mt-4 rounded-xl bg-secondary p-3 text-sm text-secondary-foreground">
            The Qurʾān passages are shown in {lang.meta.name}; the duʿā meanings are not yet
            translated, so they are left out here. Add English, or another language, in Reading
            settings to see them alongside {lang.meta.name}.
          </p>
        )}
        {numbered.map((sec, k) => {
          const t = lang.sections[sec.id] ?? en.sections[sec.id];
          return (
            <section key={sec.id} aria-labelledby={`sec-${sec.id}`} className="pt-6">
              <div className="rounded-2xl bg-secondary px-4 py-3">
                <p className="text-[0.7rem] font-bold uppercase tracking-widest text-gold">
                  Part {k + 1}
                </p>
                <h2
                  id={`sec-${sec.id}`}
                  className="font-serif text-xl font-bold text-secondary-foreground"
                >
                  {t?.title}
                </h2>
                {t?.description && <p className="text-sm text-muted-foreground">{t.description}</p>}
              </div>
              {sec.items.map(({ it, n }) => (
                <ItemCard
                  key={it.id}
                  item={it}
                  n={n}
                  lang={lang}
                  en={en}
                  when={when}
                  count={counts[it.id] ?? 0}
                  onTap={() => tap(it.id, it.repeat)}
                  showTranslit={settings.translit}
                  meaningLangs={meaningLangs}
                />
              ))}
            </section>
          );
        })}
        <div className="py-10 text-center">
          <p className="font-serif text-lg text-gold">
            {done === total ? "The wird is complete." : `${done} of ${total} lines said`}
          </p>
          <button
            type="button"
            onClick={reset}
            className="mt-3 inline-flex min-h-11 items-center gap-2 rounded-full px-4 text-sm text-muted-foreground"
          >
            <RotateCcw className="size-4" /> Clear this {when}'s counts
          </button>
        </div>
      </main>

      {/* Morning / evening switch within thumb reach */}
      <nav className="fixed inset-x-0 bottom-0 z-20 border-t border-border bg-background/95 px-4 pt-2 pb-safe backdrop-blur">
        <div
          role="radiogroup"
          aria-label="Time of day"
          className="mx-auto grid max-w-md grid-cols-2 gap-1 rounded-full bg-muted p-1"
        >
          {(["morning", "evening"] as const).map((w) => (
            <button
              key={w}
              type="button"
              role="radio"
              aria-checked={when === w}
              onClick={() => setWhen(w)}
              className={`flex min-h-11 items-center justify-center gap-2 rounded-full text-sm font-semibold transition-colors ${
                when === w
                  ? w === "morning"
                    ? "bg-sun text-sun-foreground"
                    : "bg-moon text-moon-foreground"
                  : "text-muted-foreground"
              }`}
            >
              {w === "morning" ? <Sun className="size-4" /> : <Moon className="size-4" />}
              {w === "morning" ? "Morning" : "Evening"}
              {when === w && (
                <span className="font-normal opacity-75">
                  · {done}/{total}
                </span>
              )}
            </button>
          ))}
        </div>
      </nav>

      <ReaderSettings
        open={open}
        onOpenChange={setOpen}
        settings={settings}
        update={update}
        current={code}
      />
    </div>
  );
}
