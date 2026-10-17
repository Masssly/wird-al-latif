import { createFileRoute } from "@tanstack/react-router";
import { A, H2, PageShell } from "@/components/wird/PageShell";
import { COMPILER, getLang } from "@/lib/wird";

export const Route = createFileRoute("/sources")({
  head: () => ({
    meta: [
      { title: "Sources and licences — al-Wird al-Laṭīf" },
      {
        name: "description",
        content: "Where the Qurʾān text, fonts and translations in this edition of al-Wird al-Laṭīf come from.",
      },
      { property: "og:title", content: "Sources — al-Wird al-Laṭīf" },
      { property: "og:description", content: "Credits for the Qurʾān text, translations and fonts used." },
      { property: "og:type", content: "article" },
      { name: "twitter:card", content: "summary" },
    ],
  }),
  component: Sources,
});

function Sources() {
  const en = getLang("en").quran;
  const de = getLang("de").quran;
  return (
    <PageShell title="Sources">
      <H2>Qurʾānic Arabic</H2>
      <p>
        Text: King Fahd Glorious Qurʾān Printing Complex (KFGQPC), Uthmanic Ḥafṣ data v18 (
        <A href="https://qurancomplex.gov.sa/en/techquran/dev/">qurancomplex.gov.sa</A>), as mirrored at{" "}
        <A href="https://github.com/thetruetruth/quran-data-kfgqpc">github.com/thetruetruth/quran-data-kfgqpc</A>. Used
        verbatim; in 23:97 the wird begins at <i>Rabbī</i>.
      </p>
      <p>Font: KFGQPC Uthmanic Script HAFS. © 2010 KFGQPC; free to use, copy and distribute; may not be sold or modified.</p>

      <H2>Qurʾān translations</H2>
      <p>
        English: {en.name?.replace("English Translation - ", "")}, v{en.version} —{" "}
        <A href={en.url ?? "https://quranenc.com"}>QuranEnc.com</A>.
        <br />
        German: {de.name?.replace("German Translation - ", "")} (with Nadeem Elyas), v{de.version} —{" "}
        <A href={de.url ?? "https://quranenc.com"}>QuranEnc.com</A>.
        <br />
        Reproduced verbatim under QuranEnc’s terms (credit the source, do not change the text). Footnotes are not
        reproduced.
      </p>
      <p>
        Hausa: translation by Abubakar Mahmoud Gumi, as printed by the King Fahd Complex (also on{" "}
        <A href="https://quranenc.com/ha/browse/hausa_gummi">QuranEnc.com</A>). Transcribed from the printed edition,
        keeping its spelling. Not yet proofread.
      </p>
      <p>
        Dagbanli: translation by Muḥammad Bābā Gbetobu, as printed by the King Fahd Complex (also on{" "}
        <A href="https://quranenc.com/en/browse/dagbani_ghatubo">QuranEnc.com</A>). Transcribed from the printed edition.
        Not yet proofread.
      </p>

      <H2>Duʿās and evening wording</H2>
      <p>
        Arabic and transliteration based on a circulating edition of the wird, fully vowelled and corrected for this
        edition; their provenance is still being reviewed. English meanings of the duʿās are new translations made for
        this edition.
      </p>
      <p>
        Evening wording as given in <i>The Graceful and Benevolent Litany</i> (Ashnataar Publications, 2012, ed.
        Ghoesain Mohamed) and on <A href="https://salawat.com/wird-al-latif/">salawat.com</A>.
      </p>

      <H2>Other</H2>
      <p>
        Dates of Imām al-Ḥaddād:{" "}
        <A href="https://en.wikipedia.org/wiki/%27Abdullah_ibn_%27Alawi_al-Haddad">Wikipedia</A>. Fonts: Amiri and Inter,
        both under the SIL Open Font License 1.1.
      </p>

      <H2>Licence</H2>
      <p className="rounded-xl bg-secondary p-3 text-secondary-foreground">
        The licence for the new material by {COMPILER} (duʿā translations, transliteration, notes and layout) is not yet
        decided; CC BY-SA 4.0 is proposed. The Qurʾān translations stay under their publishers’ terms and the Qurʾān
        font under the KFGQPC licence.
      </p>
    </PageShell>
  );
}
