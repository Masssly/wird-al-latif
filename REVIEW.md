# Review log

Things that need a qualified human decision. **Do not "fix" the Arabic,
Hausa or Dagbanli from memory.** Add a note here (or open an issue) and leave
the text as it is until a reviewer signs it off. When a point is settled,
record who decided, when and what changed, and keep the entry.

Each entry has an id (used in code comments), a status and the files it
concerns.

## Text that needs proofreading

### R-A1 · Duʿā Arabic is unproofread · open · highest priority
`data/wird.yaml`: every item with an `arabic` field (37 items: numbers 7, 10–16 and 18–46).
The Arabic was typed from knowledge and a garbled source PDF (HANDOFF.md §3).
It needs a check, word by word, by a qualified reader before wide release,
covering both the morning and the evening wording.
Its provenance is also unresolved (THIRD_PARTY.md).

### R-A2 · Evening wording · open
`data/wird.yaml`, `data/translit.yaml`, `i18n/en.yaml`, section `morning-evening` and items `nima-afiya-sitr`, `ushhiduka`.
The evening forms follow the Ashnataar 2012 edition and salawat.com (HANDOFF.md §2).
Check them against a scholarly source at the same time as R-A1, especially:
the swapped order in `bika-asbahna`;
*al-nushūr* → *al-maṣīr*;
*hādhā al-yawm* → *hādhihi al-laylah*, with the feminine suffixes;
*aṣbaḥa* → *amsā*.

### R-T0 · Transliteration · open
`data/translit.yaml`, status draft.
Based on a circulating edition, so its provenance is unresolved.
Decide whether to keep it or rewrite it with our own consistent scheme (open question for the owner).
It is a separate layer, so replacing it touches nothing else.

### R-T1 · Hausa Qurʾān transcription (Gumi) · open
`data/transcriptions/hausa_gumi.yaml`.
Typed by eye from the King Fahd Complex print. Check every verse against the printed page (the page numbers are in the file), ideally with a native speaker.

QuranEnc publishes the same translation online (`hausa_gummi` v1.2.2).
On 2026-10-14 its text was compared with the transcription, ignoring punctuation, quotation marks and capitalisation.
Some differences look like revisions in the online edition, for example 113:4 and 59:23.
Others may be typing slips: 112:2 *bukata*, 114:1 *neman*/*mutane*, 59:23 *tĩlastãwa* (the online text has *tastãwa*).
**Each one must be checked against the print, not against QuranEnc.**

| Verse | Transcription | QuranEnc `hausa_gummi` |
|---|---|---|
| 112:1 | Makaɗaici | Makaɗaĩci |
| 112:2 | bukata | buƙata |
| 112:4 | tamka | kini |
| 113:4 | ƙulle-ƙulle | kuduri |
| 113:5 | hãsada | hasada |
| 114:1 | neman | nẽman |
| 114:1 | mutane | mutãne |
| 114:3 | mutane | mutãne |
| 59:21 | Alƙur’ãni | Alƙur’ani |
| 59:22 | Alƙur’ãni | Alƙur’ani |
| 59:23 | tĩlastãwa | tastãwa |
| 59:23 | kãmun kai Tsarki | nuna isa tsarki |
| 37:81 | bãyinMu | bãyin Mu |

### R-T2 · Dagbanli Qurʾān transcription (Gbetobu) · open
`data/transcriptions/dagbani_gbetobu.yaml`.
Typed by eye from the archive.org scan of the King Fahd Complex print.
Check every verse against the scan (page numbers are in the file), ideally with a native speaker.

QuranEnc publishes it online as `dagbani_ghatubo`. Its text sometimes uses Greek ε (U+03B5) for ɛ; that was ignored in the comparison.
Large differences, for example 30:17–18, 113:5 and 59:23–24, suggest the online text is a revised translation.
Small ones may be typing slips, for example 59:22 *Nambɔnaa*, where the basmala has *Nambɔzobonaa*.
**Check against the print.**

| Verse | Transcription | QuranEnc `dagbani_ghatubo` |
|---|---|---|
| 112:4 | — | (binnamda puuni) |
| 113:5 | putɔɣulana | nyubiɛɣu lana zaɣibetali |
| 113:5 | niŋ putɔɣu | zabi nyuli |
| 114:4 | yɛltɔɣabɛri | yɛltɔɣabiɛri |
| 114:5 | yɛltɔɣabɛri m-bahiri | yɛltɔɣabiɛri m-birti |
| 23:98 | taɣibu A | taɣibuA |
| 23:116 | duuma | duma |
| 23:116 | n-kani | nkani |
| 23:118 | — | gari ban |
| 23:118 | n-gari ŋun kam zɔri nambɔɣu | — |
| 30:17 | wuntaŋ | yi |
| 30:17 | luri ya | luhiri wuliŋga |
| 30:17 | yi | biɛɣu |
| 30:17 | bɛɣu | ya |
| 30:18 | Paɣibu | Ŋuna n-su paɣibu |
| 30:18 | nyɛla O dini | — |
| 30:18 | n-ti pahi Azafar jiŋli saha | ni dabsili yi ti pirgi sunsuuni |
| 30:19 | nyɛvulilana bimkpiŋ | nyɛvuli lana binkpiŋ |
| 30:19 | bimkpiŋ | binkpiŋ |
| 59:21 | ka nyɛla | kanyɛla |
| 59:22 | so duuma | So duma |
| 59:22 | n-kani | ni kani |
| 59:22 | n-nyɛ Ŋun mi din | n-nyɛŊun midin |
| 59:22 | Nambɔnaa | Nambɔzobonaa |
| 59:23 | so duuma | So duma |
| 59:23 | niŋ kasi Yɛmbahiga lana | nam simsi Yɛmbahigalana |
| 59:23 | Tibginsim lana | Tibginsimlana |
| 59:23 | niŋ kasi | simsiya |
| 59:24 | niŋdi | simsiri |
| 59:24 | la kasi Yaha | mi |
| 59:24 | n-nyɛ | lahi nyɛ |

## Decisions for the owner

### R-Q1 · 23:97 is not used quite verbatim · open
`data/wird.yaml` item `muminun-97` (`opening`), applied in `pdf/build.py` and `scripts/build-wird-data.ts`.
The wird begins at *Rabbī*, so the build drops وَقُل and writes رَبِّ instead of KFGQPC's رَّبِّ, without the shadda.
That is a change to KFGQPC text, while the 1.0 Sources page says "Used verbatim; in 23:97 the wird begins at Rabbī".
Options:
1. Keep the change and say so on the Sources page.
2. Show the KFGQPC wording unchanged from رَّبِّ.
3. Show the whole verse with وَقُل greyed.

### R-L1 · Redistribution of the Hausa and Dagbanli translations · open
Ask KFGQPC or QuranEnc whether the transcribed text may be redistributed on a public website and in PDFs (THIRD_PARTY.md).

## Bugs in the edition 1.0 build (kept for now so the PDF reproduces exactly)

### R-B1 · Grey "silent letters" are never shown · open
`pdf/build.py`.
The How-to page says grey letters are written but not pronounced, but no letter in the PDF is grey, not even its own example ٱلشَّمۡسِ.
Cause: `SUN` is defined twice. First it is the set of sun letters used for lām al-shamsiyya. Later it is overwritten with the sun icon's data URI, so the lām check always fails.
The other rule, the Madinah round zero (U+0652) in Qurʾān text, matches only one letter in the verses used (تَوَلَّوۡاْ in 9:129), and that word comes before the quoted part.
Fixing this changes the PDF on purpose, so do it in the template rewrite (milestone 2) and regenerate the baseline in the same commit.
**The website already differs:** its port of these rules (`src/lib/wird.ts`) has no such clash, so the site does grey the silent lām.
That colouring has not been reviewed, and the web and PDF disagree until this is settled.

### R-W1 · Website shows 9:129 in Amiri, the PDF in the KFGQPC font · open
`src/components/wird/ItemCard.tsx`.
The quoted end of 9:129 (item 17, `hasbiya`) is KFGQPC text, but the website sets it in Amiri (`font-dua`) like the duʿās, while the PDF uses the Madinah muṣḥaf font.

### R-B2 · German duʿā meanings are new, AI-assisted and unproofread · open
`i18n/de.yaml` now has German meanings for all 38 duʿā items (2026-10-31), at the owner's request ("German is a high-resource language and AI is pretty good at it").
They are a fresh translation from the English meanings, written by Claude and not corrected from any existing published source — no native-speaker or qualified reviewer has checked them.
`meta.status` is `reviewed` (so the website shows no draft badge for German, matching the owner's decision in #6), but that reflects the *Qurʾān* translation's standing (Bubenheim & Elyas, an established scholarly translation); the new duʿā text itself carries no such standing yet.
Flagging here per the project's own rule on AI-written religious text, so a German speaker can check it before it's treated as settled. Points worth a second look in particular: "Meister" for *sayyidunā* (chosen over "Herr", which in German usually means God the Lord — a reviewer may prefer another word), and the three-item split in `khayra-hadha-al-yawm`/`khayra-ma-fih`/`ma-asbaha-bi`, where German grammar forces the morning/evening change to span a whole clause instead of one word, unlike the other languages.

Hausa and Dagbanli still have no duʿā meanings at all (not even a draft): their items remain English-only in the reader, per R-L1 below.
