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
        {item.audio && !audio.playing && <AudioChip onToggle={audio.toggle} />}
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
 * shared by every ItemCard). Collapsed to a small chip until played; the real browser
 * controls — play/pause, scrubbing, volume, speed — only take up space while playing. */
function useAudioToggle(
  id: string,
  playingAudioId: string | null,
  setPlayingAudioId: (id: string | null) => void,
) {
  const ref = useRef<HTMLAudioElement>(null);
  const playing = playingAudioId === id;

  // Some other item started: stop this one, even if it's mid-playback.
  useEffect(() => {
    if (!playing) ref.current?.pause();
  }, [playing]);

  const toggle = () => {
    setPlayingAudioId(id);
    // A quick pause right after can abort this promise (e.g. tapping again before it starts) —
    // expected, not an error; HTMLMediaElement just doesn't let play() itself opt out of the
    // console warning, so catch it here instead.
    ref.current?.play().catch(() => {});
  };
  // Fires both for a real pause (the reciter's own controls) and for the one we trigger above
  // when another item starts — only the former should still be "us" by the time it fires.
  const onPauseOrEnded = () => {
    if (playing) setPlayingAudioId(null);
  };

  return { ref, playing, toggle, onPauseOrEnded };
}

type AudioToggle = ReturnType<typeof useAudioToggle>;

/** Collapsed state: a small play button, out of the way of the text. Once playing, the real
 * controls (below, in AudioBar) take over — pause lives there, not here, so there's one
 * control for it, not two. */
function AudioChip({ onToggle }: { onToggle: () => void }) {
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-label="Play the recitation"
      className="ml-auto flex size-7 shrink-0 items-center justify-center rounded-full border border-border text-gold print:hidden"
    >
      <Play className="size-3.5 translate-x-0.5" />
    </button>
  );
}

/** The full browser audio player — play/pause, scrubbing, volume, speed where the browser
 * offers it. Mounted (and visible) only while playing, so it folds away the moment playback
 * stops, rather than sitting there taking up space between listens. */
function AudioBar({ audio, ...t }: { audio: NonNullable<Item["audio"]> } & AudioToggle) {
  const BASE = import.meta.env.BASE_URL;
  return (
    <audio
      ref={t.ref}
      preload="none"
      controls={t.playing}
      src={`${BASE}${audio.file}`}
      onEnded={t.onPauseOrEnded}
      onPause={t.onPauseOrEnded}
      className={t.playing ? "mt-2 h-9 w-full print:hidden" : "hidden"}
    />
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
