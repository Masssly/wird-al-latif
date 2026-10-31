import { createFileRoute, Link } from "@tanstack/react-router";
import { ChevronRight, Download } from "lucide-react";
import { StatusBadge } from "@/components/wird/StatusBadge";
import { COMPILER, getLang, LANG_ORDER, WIRD } from "@/lib/wird";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "al-Wird al-Laṭīf — open multilingual edition" },
      {
        name: "description",
        content:
          "A free, phone-first edition of the morning and evening litany of Imām al-Ḥaddād: vowelled Arabic, transliteration, and meanings in English, German, Hausa and Dagbanli.",
      },
      { property: "og:title", content: "al-Wird al-Laṭīf — open edition" },
      {
        property: "og:description",
        content:
          "The morning and evening litany of Imām al-Ḥaddād, free and readable on any phone.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary" },
    ],
  }),
  component: Home,
});

function Home() {
  return (
    <div className="min-h-dvh">
      <main className="mx-auto flex min-h-dvh max-w-md flex-col px-5 pt-safe pb-safe">
        <div className="flex flex-1 flex-col justify-center py-12 text-center">
          <p lang="ar" dir="rtl" className="font-dua text-6xl leading-[1.6] text-ink">
            {WIRD.title}
          </p>
          <h1 className="mt-1 font-serif text-3xl font-bold">al-Wird al-Laṭīf</h1>
          <p className="mt-2 text-muted-foreground">of Imām ʿAbd Allāh ibn ʿAlawī al-Ḥaddād</p>
          <div className="mx-auto my-6 h-px w-16 bg-gold/50" />
          <p className="text-sm text-muted-foreground">
            Morning and evening litany
            <br />
            Arabic · transliteration · meaning
          </p>
        </div>

        <section aria-labelledby="pick" className="pb-6">
          <h2 id="pick" className="mb-3 text-xs font-bold uppercase tracking-widest text-gold">
            Choose a language
          </h2>
          <ul className="space-y-2">
            {LANG_ORDER.map((c) => {
              const m = getLang(c).meta;
              return (
                <li key={c}>
                  <Link
                    to="/$lang"
                    params={{ lang: c }}
                    className="flex min-h-14 items-center gap-3 rounded-2xl border border-border bg-card px-4 transition-colors active:bg-secondary"
                  >
                    <span className="flex-1">
                      <span className="block font-semibold">{m.native_name}</span>
                      <span className="block text-xs text-muted-foreground">
                        {c === "en"
                          ? "Qurʾān and duʿā meanings"
                          : "Qurʾān meanings · duʿās not yet translated"}
                      </span>
                    </span>
                    <StatusBadge status={m.status} />
                    <ChevronRight className="size-4 text-muted-foreground" />
                  </Link>
                </li>
              );
            })}
          </ul>
          <p className="mt-4 rounded-xl bg-secondary p-3 text-xs text-secondary-foreground">
            This edition is still being proofread. The duʿā Arabic and the Hausa and Dagbanli texts
            have not yet been checked by a qualified reader.
          </p>
        </section>

        <nav className="flex flex-wrap items-center justify-center gap-x-5 gap-y-1 border-t border-border py-4 text-sm">
          <Link to="/about" className="min-h-11 content-center">
            About
          </Link>
          <Link to="/sources" className="min-h-11 content-center">
            Sources
          </Link>
          <a
            href={`${import.meta.env.BASE_URL}al-Wird-al-Latif.pdf`}
            className="inline-flex min-h-11 items-center gap-1"
          >
            <Download className="size-4" /> Printed edition (PDF)
          </a>
        </nav>
        <p className="pb-2 text-center text-xs text-muted-foreground">
          Compiled by {COMPILER} · Edition {WIRD.edition}
        </p>
      </main>
    </div>
  );
}
