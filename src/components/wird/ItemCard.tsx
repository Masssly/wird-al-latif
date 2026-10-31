import { Check, RotateCcw } from "lucide-react";
import { getLang, WIRD, type Item, type Lang, type When } from "@/lib/wird";
import { Rich } from "./Rich";

type Props = {
  item: Item;
  n: number;
  lang: Lang;
  en: Lang;
  when: When;
  count: number;
  onTap: () => void;
  showTranslit: boolean;
  /** Languages to show the meaning in, in order. A language missing the meaning is simply skipped. */
  meaningLangs: string[];
};

export function ItemCard({
  item,
  n,
  lang,
  en,
  when,
  count,
  onTap,
  showTranslit,
  meaningLangs,
}: Props) {
  const done = count >= item.repeat;
  const heading = lang.headings[item.id] ?? en.headings[item.id];
  const tl = WIRD.translit;
  const itemTl = tl.items[item.id];

  return (
    <article id={item.id} className="scroll-mt-20 border-b border-border py-6">
      <div className="mb-3 flex items-center gap-2">
        <span
          className="flex size-7 shrink-0 items-center justify-center rounded-full border border-border text-xs text-muted-foreground"
          aria-label={`Line ${n}`}
        >
          {n}
        </span>
        {heading && <h3 className="min-w-0 truncate text-sm font-semibold text-gold">{heading}</h3>}
        {item.kind === "quote" && item.ref && (
          <span className="text-xs text-muted-foreground">
            {(lang.ui.from_quran ?? en.ui.from_quran ?? "From Qurʾān {ref}").replace(
              "{ref}",
              item.ref,
            )}
          </span>
        )}
      </div>

      {item.kind === "quran" ? (
        <QuranBody item={item} showTranslit={showTranslit} meaningLangs={meaningLangs} />
      ) : (
        <>
          <p lang="ar" dir="rtl" className="text-ar font-dua text-ink">
            <Rich
              text={item.arabic!}
              when={when}
              mode={item.kind === "quote" ? "uthmani" : "arabic"}
            />
          </p>
          {showTranslit && itemTl && (
            <p lang="ar-Latn" className="text-lat mt-2 italic text-foreground/85">
              <Rich text={itemTl} when={when} mode="translit" />
            </p>
          )}
          <Meaning item={item} langs={meaningLangs} when={when} />
        </>
      )}

      <button
        type="button"
        onClick={onTap}
        aria-label={
          item.repeat > 1
            ? `Count, ${count} of ${item.repeat}${done ? ", done" : ""}`
            : done
              ? "Done, tap to undo"
              : "Mark as said"
        }
        className={`mt-4 flex min-h-11 w-full items-center justify-center gap-2 rounded-full border text-sm font-semibold transition-colors active:scale-[0.98] print:hidden ${
          done
            ? "border-transparent bg-primary text-primary-foreground"
            : "border-border bg-card text-secondary-foreground"
        }`}
      >
        {done ? (
          <>
            <Check className="size-4" /> {item.repeat > 1 ? `${item.repeat} × done` : "Done"}
            <RotateCcw className="ml-1 size-3.5 opacity-60" />
          </>
        ) : item.repeat > 1 ? (
          <>
            <span key={count} className="animate-pop tabular-nums">
              {count} / {item.repeat}
            </span>
            <span className="font-normal text-muted-foreground">
              · tap each time · repeat {item.repeat}×
            </span>
          </>
        ) : (
          "Said once · tap when done"
        )}
      </button>
      {/* The tap counter is a reading aid, not printable content — print the repeat count as
          plain text instead, since there's nothing to tap on paper. */}
      {item.repeat > 1 && (
        <p className="mt-4 hidden text-sm font-semibold text-muted-foreground print:block">
          Repeat {item.repeat}×
        </p>
      )}
    </article>
  );
}

/** One paragraph per selected language that actually has this meaning; a language without it is just skipped. */
function Meaning({ item, langs, when }: { item: Item; langs: string[]; when: When }) {
  const entries = langs
    .map((code) => ({ code, text: getLang(code).items[item.id] }))
    .filter((e): e is { code: string; text: NonNullable<(typeof e)["text"]> } => !!e.text);
  if (!entries.length) return null;
  return (
    <>
      {entries.map(({ code, text }) => (
        <p key={code} lang={code} className="text-lat mt-2 text-muted-foreground">
          {entries.length > 1 && <LangPill>{code.toUpperCase()}</LangPill>}
          <Rich text={text} when={when} mode="meaning" />
        </p>
      ))}
    </>
  );
}

function LangPill({ children }: { children: string }) {
  return (
    <span className="mr-1.5 inline-block rounded bg-muted px-1 align-[0.1em] text-[0.65rem] font-bold not-italic tracking-wide text-muted-foreground">
      {children}
    </span>
  );
}

function QuranBody({
  item,
  showTranslit,
  meaningLangs,
}: {
  item: Item;
  showTranslit: boolean;
  meaningLangs: string[];
}) {
  const tl = WIRD.translit;
  return (
    <div>
      {item.basmala && (
        <p lang="ar" dir="rtl" className="text-ar text-center font-quran text-ink">
          <Rich text={WIRD.basmala} when="morning" mode="uthmani" />
        </p>
      )}
      <p lang="ar" dir="rtl" className="text-ar font-quran text-ink">
        {item.verses!.map((v) => (
          <span key={v.key}>
            <Rich text={v.ar} when="morning" mode="uthmani" />{" "}
          </span>
        ))}
      </p>
      {showTranslit && (
        <p lang="ar-Latn" className="text-lat mt-2 italic text-foreground/85">
          {item.basmala && (
            <>
              <Rich text={tl.basmala} when="morning" mode="translit" />
              <br />
            </>
          )}
          {item.verses!.map((v) => (
            <span key={v.key}>
              <sup className="mr-0.5 text-[0.65em] not-italic text-gold">{v.aya}</sup>
              <Rich text={tl.quran[v.key] ?? ""} when="morning" mode="translit" />{" "}
            </span>
          ))}
        </p>
      )}
      {meaningLangs.length > 0 && (
        <div className="mt-2 space-y-2">
          {meaningLangs.map((code) => {
            const l = getLang(code);
            return (
              <p key={code} lang={code} className="text-lat text-muted-foreground">
                {meaningLangs.length > 1 && <LangPill>{code.toUpperCase()}</LangPill>}
                {item.basmala && (
                  <>
                    <Rich text={l.quran.basmala} when="morning" mode="meaning" />
                    <br />
                  </>
                )}
                {item.verses!.map((v) => (
                  <span key={v.key}>
                    <sup className="mr-0.5 text-[0.65em] text-gold">{v.aya}</sup>
                    <Rich text={l.quran.verses[v.key] ?? ""} when="morning" mode="meaning" />{" "}
                  </span>
                ))}
              </p>
            );
          })}
        </div>
      )}
    </div>
  );
}
