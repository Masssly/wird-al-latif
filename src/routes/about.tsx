import { createFileRoute } from "@tanstack/react-router";
import { Legend } from "@/components/wird/Legend";
import { H2, PageShell } from "@/components/wird/PageShell";
import { COMPILER } from "@/lib/wird";

export const Route = createFileRoute("/about")({
  head: () => ({
    meta: [
      { title: "About al-Wird al-Laṭīf — Imām al-Ḥaddād" },
      {
        name: "description",
        content: "Who compiled al-Wird al-Laṭīf, how it is read, and how to read this edition's colours and counters.",
      },
      { property: "og:title", content: "About al-Wird al-Laṭīf" },
      { property: "og:description", content: "The litany of Imām al-Ḥaddād and how to read this open edition." },
      { property: "og:type", content: "article" },
      { name: "twitter:card", content: "summary" },
    ],
  }),
  component: About,
});

function About() {
  return (
    <PageShell title="About">
      <p>
        <i>Al-Wird al-Laṭīf</i> was compiled by Imām ʿAbd Allāh ibn ʿAlawī al-Ḥaddād (1044–1132 AH / 1634–1720 CE) of
        Tarim, in Ḥaḍramawt, Yemen. Smallpox took his sight before he was five, yet he became one of the best-known
        scholars and spiritual teachers of his age. He also compiled the <i>Rātib al-Ḥaddād</i>.
      </p>
      <p>
        The wird is made up of passages of the Qurʾān and of supplications that the Prophet ﷺ taught his community to
        say in the morning and the evening. It is read once each morning and once each evening.
      </p>
      <p>
        The Arabic of the Qurʾānic passages follows the Madinah muṣḥaf printed by the King Fahd Complex. Everything else
        is fully vowelled.
      </p>

      <H2>How to read this edition</H2>
      <p>
        The reader opens on the morning or evening wording depending on your clock; switch at the bottom of the screen.
        Lines with a number like <b>0 / 3</b> are repeated: tap once each time you say them. Your counts stay on your
        phone only and start fresh each day.
      </p>
      <Legend />

      <H2>This edition</H2>
      <p>
        Compiled by {COMPILER}. It is free, has no ads, accounts or tracking, and works without internet once opened.
        The duʿā Arabic and the Hausa and Dagbanli texts are still waiting to be proofread.
      </p>
    </PageShell>
  );
}
