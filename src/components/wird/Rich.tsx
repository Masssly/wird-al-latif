import { Fragment } from "react";
import {
  colourArabic,
  colourMeaning,
  colourTranslit,
  segments,
  type Text,
  type Tok,
  type When,
} from "@/lib/wird";

const CLS: Record<NonNullable<Tok["c"]>, string> = {
  allah: "text-allah",
  nabi: "text-nabi",
  silent: "text-silent",
};

function Toks({ toks }: { toks: Tok[] }) {
  return (
    <>
      {toks.map((k, i) =>
        k.c ? (
          <span key={i} className={CLS[k.c]}>
            {k.t}
          </span>
        ) : (
          <Fragment key={i}>{k.t}</Fragment>
        ),
      )}
    </>
  );
}

type Mode = "arabic" | "uthmani" | "translit" | "meaning";

/** Renders a text field for one time of day, with colour coding and changed-word highlights. */
export function Rich({ text, when, mode }: { text: Text; when: When; mode: Mode }) {
  const colour = (s: string) =>
    mode === "arabic" || mode === "uthmani"
      ? colourArabic(s, mode === "uthmani")
      : mode === "translit"
        ? colourTranslit(s)
        : colourMeaning(s);
  return (
    <>
      {segments(text, when).map((s, i) =>
        s.changed ? (
          <mark key={i} className={when === "morning" ? "chg-morning" : "chg-evening"}>
            <Toks toks={colour(s.t)} />
          </mark>
        ) : (
          <Toks key={i} toks={colour(s.t)} />
        ),
      )}
    </>
  );
}
