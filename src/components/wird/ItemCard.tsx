import { Check, Pause, Play, RotateCcw } from "lucide-react";
import { useEffect, useRef, useState } from "react";
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
  /** Id of the one item whose recitation may be playing right now, page-wide. */
  playingAudioId: string | null;
  setPlayingAudioId: (id: string | null) => void;
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
  playingAudioId,
  setPlayingAudioId,
}: Props) {
  const done = count >= item.repeat;
  const heading = lang.headings[item.id] ?? en.headings[item.id];
  const tl = WIRD.translit;
  const itemTl = tl.items[item.id];
  const audio = useAudioToggle(item.id, playingAudioId, setPlayingAudioId);

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
        {item.audio && <AudioChip playing={audio.playing} onToggle={audio.toggle} />}
      </div>

      {item.kind === "quran" ? (
        <QuranBody
          item={item}
          showTranslit={showTranslit}
          meaningLangs={meaningLangs}
          audio={audio}
        />
      ) : (
        <>
          <p lang="ar" dir="rtl" className="text-ar font-dua text-ink">
            <Rich
              text={item.arabic!}
              when={when}
              mode={item.kind === "quote" ? "uthmani" : "arabic"}
            />
          </p>
          {item.audio && <AudioBar audio={item.audio} {...audio} />}
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

/** Drives one item's recitation: at most one plays at a time, page-wide (playingAudioId is
 * shared by every ItemCard). Collapsed to a small chip until played; the full bar — what's
 * actually playing, and where — only takes up space while it's playing. */
function useAudioToggle(
  id: string,
  playingAudioId: string | null,
  setPlayingAudioId: (id: string | null) => void,
) {
  const ref = useRef<HTMLAudioElement>(null);
  const [current, setCurrent] = useState(0);
  const [duration, setDuration] = useState(0);
  const playing = playingAudioId === id;

  // Some other item started: stop this one, even if it's mid-playback.
  useEffect(() => {
    if (!playing) ref.current?.pause();
  }, [playing]);

  const toggle = () => {
    if (playing) {
      setPlayingAudioId(null);
    } else {
      setCurrent(0);
      setPlayingAudioId(id);
      // A quick pause right after can abort this promise (e.g. tapping again before it starts) —
      // expected, not an error; HTMLMediaElement just doesn't let play() itself opt out of the
      // console warning, so catch it here instead.
      ref.current?.play().catch(() => {});
    }
  };
  const onEnded = () => setPlayingAudioId(null);

  return {
    ref,
    playing,
    toggle,
    current,
    duration,
    onEnded,
    onTimeUpdate: () => setCurrent(ref.current?.currentTime ?? 0),
    onLoadedMetadata: () => setDuration(ref.current?.duration ?? 0),
  };
}

type AudioToggle = ReturnType<typeof useAudioToggle>;

/** The play/pause button, always present once an item has audio — in the header, out of the
 * way of the text. The rest of the player only shows up while actually playing. */
function AudioChip({ playing, onToggle }: { playing: boolean; onToggle: () => void }) {
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-label={playing ? "Pause the recitation" : "Play the recitation"}
      aria-pressed={playing}
      className="ml-auto flex size-7 shrink-0 items-center justify-center rounded-full border border-border text-gold print:hidden"
    >
      {playing ? <Pause className="size-3.5" /> : <Play className="size-3.5 translate-x-0.5" />}
    </button>
  );
}

const fmt = (s: number) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

/** The expanded row: scrub track and time. Mounted only while playing, so it folds away — not
 * just visually hidden — the moment playback stops. */
function AudioBar({ audio, ...t }: { audio: NonNullable<Item["audio"]> } & AudioToggle) {
  const BASE = import.meta.env.BASE_URL;
  const pct = t.duration ? (t.current / t.duration) * 100 : 0;
  return (
    <>
      <audio
        ref={t.ref}
        preload="none"
        src={`${BASE}${audio.file}`}
        onEnded={t.onEnded}
        onTimeUpdate={t.onTimeUpdate}
        onLoadedMetadata={t.onLoadedMetadata}
        className="hidden"
      />
      {t.playing && (
        <div className="mt-2 flex h-7 items-center gap-2 print:hidden">
          <div className="h-[3px] flex-1 rounded-full bg-border">
            <div className="h-full rounded-full bg-primary" style={{ width: `${pct}%` }} />
          </div>
          <span className="text-[11px] tabular-nums text-muted-foreground">
            {fmt(t.current)} / {fmt(t.duration)}
          </span>
        </div>
      )}
    </>
  );
}

function QuranBody({
  item,
  showTranslit,
  meaningLangs,
  audio,
}: {
  item: Item;
  showTranslit: boolean;
  meaningLangs: string[];
  audio: AudioToggle;
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
      {item.audio && <AudioBar audio={item.audio} {...audio} />}
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
