# Third-party material

Everything in this repository that was not written for this edition, with its
source, version and terms. Third-party files are kept byte-identical to what
was published; `data/third_party.sha256` records their checksums and
`tests/test_third_party.py` fails if one changes. To update a source on
purpose, replace the file and update the checksum and this page in the same
commit.

Licensing of the material written for this edition (code, duʿā translations,
layout) is **not yet decided**. The proposal is CC BY-SA 4.0 for text and MIT
for code, and no LICENSE file will be added until the owner confirms.

## Qurʾānic Arabic: KFGQPC Uthmanic Ḥafṣ, version 18

| | |
|---|---|
| Files | `data/kfgqpc/data/hafsData_v18.json`, `data/kfgqpc/font/hafs.18.ttf`, `data/kfgqpc/README-upstream.md` |
| Publisher | King Fahd Glorious Qurʾān Printing Complex, <https://qurancomplex.gov.sa/en/techquran/dev/> |
| Obtained from | mirror <https://github.com/thetruetruth/quran-data-kfgqpc> (commit `281dbbe`, 2022-02-15); identical to the copy in the edition 1.0 handoff bundle |
| Version | data 0.18 (2021-10-25); font "KFGQPC HAFS Uthmanic Script" version 0.18 |
| Terms | © KFGQPC. Free to use, copy and distribute; **may not be sold or modified**. Not eligible for Wikimedia Commons. |
| Use | Verses are taken verbatim at build time. Two adjustments are made when they are displayed. In 23:97 the build starts at رَبِّ, dropping وَقُل and the shadda on the rāʾ (see REVIEW.md R-Q1). From 9:129 only the words from حَسۡبِيَ onwards are shown. The data file itself is never changed. |

Other formats of the same data (csv, html, sql, xlsx, xml) are not
included because nothing reads them; they are on the mirror.

## Qurʾān translations: QuranEnc

| Language | Translation | Version | File |
|---|---|---|---|
| English | Rowwad Translation Center (`english_rwwad`) | 1.0.19 (2026-03-12) | `data/quranenc/english_rwwad/1.0.19-288aad99be073280.json.gz` |
| German | Frank Bubenheim and Nadeem Elyas (`german_bubenheim`) | 1.1.4 | `data/quranenc/german_bubenheim/1.1.4-b4308b0db371b2ff.json.gz` |

- Source: <https://quranenc.com> (API terms: <https://quranenc.com/en/home/api/>). Each file's own `edition` block records the source and permission URLs.
- Terms: credit the source and the version, do **not** change the text, and keep it up to date. Both versions were still the current ones on 2026-10-14.
- Use: verses are shown verbatim. Footnote markers (`[1]`) are removed at build time and the footnotes are not reproduced; the Sources page says so.
- Not CC-compatible, so these stay separately credited. A Commons-eligible edition would need a public-domain translation (e.g. Pickthall) and a free Qurʾān font.

## Qurʾān translations transcribed from print (Hausa, Dagbanli)

| Language | Translation | Printed by | Transcription |
|---|---|---|---|
| Hausa | Abubakar Mahmoud Gumi | King Fahd Complex | `data/transcriptions/hausa_gumi.yaml` |
| Dagbanli | Muḥammad Bābā Gbetobu | King Fahd Complex (King Abdullah edition; [archive.org scan](https://archive.org/details/dagbani-quran-translation-the-holy-quran-king-abdullah-bin-abdal-aziz-al-saud)) | `data/transcriptions/dagbani_gbetobu.yaml` |

- Typed by eye by Mohammed Sadat Abdulai from the printed pages (page numbers are in each file). These are **unproofread** (REVIEW.md R-T1, R-T2).
- The text belongs to the King Fahd Complex. **Redistribution terms have not been confirmed**; ask KFGQPC/QuranEnc before publishing widely.
- Both are also published online by QuranEnc: `hausa_gummi` (v1.2.2) and `dagbani_ghatubo`. The Dagbanli one is served by the API but is missing from the QuranEnc translations index as of 2026-10-14. The online texts are a different revision from the print (see REVIEW.md), so they were not substituted.

## Duʿā Arabic, transliteration and evening wording: provenance unresolved

- The Arabic of the duʿās and the transliteration are derived from a **circulating edition of the wird**. The evening wording follows *The Graceful and Benevolent Litany* (Ashnataar Publications, © 2012, ed. Ghoesain Mohamed) and <https://salawat.com/wird-al-latif/> (© Salawat.com). The 1.0 PDF says the text was "fully vowelled and corrected for this edition"; HANDOFF.md says it was typed from knowledge plus a garbled source PDF.
- Status: **unresolved**. The Arabic of a 17th-century litany is not itself in copyright, but a particular edition's vowelling and transliteration may be. Before the licence question is settled, either confirm independence from the Ashnataar text or re-derive the Arabic from public-domain manuscripts or printings.
- For that reason the transliteration lives in its own replaceable file, `data/translit.yaml`. Replacing it touches nothing else.
- The English meanings of the duʿās (`i18n/en.yaml`) are new translations written for this edition by the compiler.

## Fonts

| Font | Version | Licence | Location |
|---|---|---|---|
| Amiri (Regular, Bold) | 1.000 | SIL Open Font License 1.1 (`fonts/Amiri-1.000/OFL.txt`) | `fonts/Amiri-1.000/` |
| Inter | 4.0 (system package `fonts-inter`) | SIL Open Font License 1.1 | not bundled; installed system-wide |
| KFGQPC Uthmanic Script HAFS | 0.18 | KFGQPC terms (above) | `data/kfgqpc/font/` |

## Other references

- Dates of Imām al-Ḥaddād: Wikipedia. Description of the wird: SeekersGuidance (Ustadh Amjad Tarsin). Neither is reproduced.

## Prior art: rqawasme/Wirdi

<https://github.com/rqawasme/Wirdi> is a Flutter habit/dhikr app. Wird al-Laṭīf was added in PR #7 (September 2026) as `wird-al-latif.json`, with 46 entries in Arabic, transliteration and English, and the Qurʾān by sura/āya reference. No licence is stated for that data.

- **Nothing from Wirdi has been copied into this repository.** Do not copy anything until the licence is clarified.
- Mohammed Sadat Abdulai has opened an issue on the Wirdi repository asking about the licence of its data and offering to compare texts.
- Reply log:

| Date | From | Summary |
|---|---|---|
| (awaiting reply) | | |
