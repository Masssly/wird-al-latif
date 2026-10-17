# al-Wird al-Laṭīf — project handoff

Owner/compiler: **Mohammed Sadat Abdulai** (day job: Wikidata lexemes / Dagbanli at WMDE; this project is personal and devotional — he was introduced to the wird by Hamza Yusuf). Goal: share the wird of Imām ʿAbd Allāh b. ʿAlawī al-Ḥaddād with the world as a free, phone-friendly, vowelled, multilingual edition, teach his kids with it, and eventually host it on GitHub Pages or GitLab Pages (undecided) with downloads in many languages and maybe audio.

## 1. Current state

`python3 src/build.py` → `dist/al-Wird-al-Latif.pdf` (77 pages, 72×128 mm, single column, WeasyPrint). Verified to rebuild from this bundle.

Dependencies: Python 3, `weasyprint` (built with v70), `pypdf` only for checking. Fonts bundled: Amiri (SIL OFL), KFGQPC Uthmanic Hafs v18 (`data/kfgqpc/font/hafs.18.ttf`). Body font Inter must be installed system-wide (falls back to DejaVu Sans).

Layout of the bundle:
- `src/content.py` — the text. `SECTIONS` (6) and `ITEMS` (46) via `add(sec, ar, tr, en, heading=, count=, quran=, bism=, ev=, ref=)`. Qur'an items have `ar=None` and `quran=[(sura, first, last)]`; Hasbiya Allah uses `quran="9:129-part"`. `ev=(ar, tr, en)` holds the evening form. `⟦…⟧` marks changed morning/evening words (yellow = morning, blue = evening).
- `src/dagbani.py`, `src/hausa.py` — hand-transcribed Qur'an translations for the 11 passages the wird uses (112–114, 23:97–98, 23:115–118, 30:17–19, 59:21–24, 37:79–81). Printed page numbers noted in comments for proofreading.
- `src/build.py` — HTML generation + two-pass PDF build (pass 1 collects anchor page numbers, pass 2 fills contents).
- `data/kfgqpc/` — KFGQPC Ḥafṣ v18 JSON (+ font). `data/quranenc/` — English (Rowwad v1.0.19) and German (Bubenheim v1.1.4) from QuranEnc.

Features done: Madinah-muṣḥaf script for verses; vowelled duʿās in Amiri; "n / total" page numbers; colour code (Allah red, Muḥammad ﷺ green, silent letters grey); morning + evening in one PDF (evening in a blue box under morning); repeat badges ("×3") distinct from item numbers; sun/moon labels; contents, About, How-to-read, Sources/licence pages; compiler credit; PDF bookmarks. Verses shown in Arabic + English + German + Hausa + Dagbanli.

## 2. Decisions made (don't relitigate)
- No separate night PDF; one combined file.
- Full tajwīd colouring rejected as overkill for now (possible later "tajwīd edition").
- Plain "repeat ×3" badges; sun and moon icons for morning/evening.
- English duʿā meanings are **new translations written for this edition** (so they can be freely licensed).
- Audio: the user will handle it later.
- Evening rules: aṣbaḥtu→amsaytu, aṣbaḥnā→amsaynā, aṣbaḥa→amsā; yawm→laylah with feminine suffixes (hu→hā); al-nushūr→al-maṣīr; order swap in "Allāhumma bika aṣbaḥnā".

## 3. Open items
1. **Proofread the duʿā Arabic** (typed from knowledge + a garbled source PDF) by a qualified person. Highest priority before wide release.
2. **Proofread Dagbanli and Hausa** transcriptions against the scans (typed by eye, not OCR). Ideally a native speaker.
3. **Provenance of the duʿā Arabic/transliteration**: derived from a circulating edition (Ashnataar, © 2012) — review and, if needed, re-derive Arabic from public-domain manuscripts/printings and write own transliteration.
4. Decide the licence for the web edition (see §5).
5. Hosting: GitHub Pages vs GitLab Pages (see §6).

## 4. What already exists (surveyed Oct 2026 — none is multilingual, open, or kid-oriented)
| Resource | What it is | Gap |
|---|---|---|
| Google Play "Wird Al-Latif – Global Version" (avblogdev, Indonesia; 1K+ installs, ads, v1.1.4 Aug 2026) | Android app | Closed, ads, no stated licence, languages unclear |
| Google Play "al-Wird al-Latif" (Ahlesunnats Soft, India; 1K+) | Android page-viewer; English + Urdu title | Scanned-book style, zoom + go-to-page only |
| GitHub **rqawasme/Wirdi** (Flutter, iOS/Android; PR #7 merged 6 Sep 2026) | Habit/dhikr app with Wird al-Laṭīf morning & evening; `wird-al-latif.json`, 46 entries, Arabic + English + transliteration, Qur'an by sura/āya reference (QUL, Saheeh International) | Apps only, no web/PDF, English only, no stated licence on the litany data. **Closest prior art — consider contacting the author; their 46-entry JSON mirrors our 46 items.** |
| salawat.com/wird-al-latif | Web page: Arabic (Uthmani/IndoPak), transliteration, English, morning/evening | English only, no audio, © Salawat.com |
| SeekersGuidance article (Ustadh Amjad Tarsin) | Page images with transliteration | Images, no translation, all rights reserved |
| Safina Society /wird | PDF + SoundCloud + YouTube of morning adhkar | No translations, © Safina Society |
| SimplyIslam Academy article | Partial text, YouTube video | Incomplete, English |
| Internet Archive "WirdAlLatif" text PDF | Scanned/typeset text | Not vowelled-mobile-friendly, not multilingual |
| Hamza Yusuf commentary (blog) | Commentary | Not a reusable edition |

**Not found:** an open-licensed, multilingual (esp. Hausa/Dagbanli/German/French/Urdu/Indonesian/Turkish/Swahili), phone-first, structured-data edition; any kids' edition; any properly licensed audio. That is the niche.

## 5. Licensing notes (important)
- New material (layout, code, English duʿā translations, transliteration if rewritten): propose **CC BY-SA 4.0** for text, **MIT/Apache-2.0** (or AGPL if preferred) for code.
- KFGQPC font/data: free to use/copy/distribute, **not to be sold or modified**. Cannot be uploaded to Wikimedia Commons.
- QuranEnc translations (English Rowwad, German Bubenheim): **no modification**, credit source + version, keep up to date. Not CC-compatible → keep them as separately-credited third-party content; a Commons-eligible edition would need Pickthall (PD) + a free font.
- King Fahd Complex prints of Gumi (Hausa) and Gbetobu (Dagbanli): transcribed by hand; confirm redistribution terms with KFGQPC/QuranEnc before publishing broadly.
- Mushaf-Learning/quran-translations repo is non-commercial only; Talal Itani is CC BY-ND-NC — avoid both.

## 6. Website — recommended shape
See the chat reply for the full reasoning. Summary:
- **Host:** GitHub Pages (simplest, biggest contributor base, Actions builds PDFs). GitLab only if you want built-in i18n tooling/self-hosting preference. Repo = source of truth either way; keep it portable (static output, no vendor lock).
- **Single source of truth:** move `content.py` into structured data — `data/wird.yaml` (items, counts, sections, morning/evening forms with explicit variant markers instead of `⟦⟧` text hacks) and `i18n/<lang>.yaml` (translation per item id). Qur'an passages stored by sura:āya reference only; translations per language keyed by the same reference.
- **Static generator:** Eleventy or Astro (or plain Python + Jinja since the pipeline is already Python). Output: one HTML reader page per language + per-language PDF built in CI with WeasyPrint.
- **Reader UX:** mobile-first, morning/evening toggle that defaults by local time, per-item checklist/counter (localStorage only, no tracking), colour-code legend, text-size, RTL-aware, works offline (PWA/service worker).
- **Kids mode:** big text, one item per screen, tap-to-reveal meaning, colour-coded Allah/Muḥammad ﷺ words, progress stars; later a short "story of the wird" and simple vocabulary cards. Needs a scholar/teacher review.
- **Translations:** one YAML file per language; contributors open PRs or use Weblate/Codeberg Translate (free for libre projects). Mark each language `draft | reviewed | verified` and show that status on the site. Start with languages you can verify: English, German, Hausa, Dagbanli; then French, Indonesian, Urdu, Turkish, Swahili.
- **Audio (later):** record own or obtain written permission from a reciter; host MP3/Opus on GitHub Releases/Internet Archive (Pages size cap ~1 GB, 100 GB/month bandwidth soft limit); timestamp per item to enable highlight-as-you-listen.
- **Governance:** `CONTRIBUTING.md`, `LICENSE`, `CITATION.cff`, `THIRD_PARTY.md` listing each source and its terms; named reviewers for Arabic text; changelog and edition numbers.

## 7. Suggested first steps in Claude Code
1. `git init`, add LICENSE / THIRD_PARTY.md, commit this bundle.
2. Convert `content.py` → `data/wird.yaml` + `i18n/en.yaml`, keeping a test that regenerates the same PDF text.
3. Add a Jinja HTML reader template and GitHub Actions workflow (build PDFs, deploy Pages).
4. Add language switcher + status badges; then recruit proofreaders.
5. Contact Wirdi author (rqawasme) about sharing data / avoiding duplicate effort.

## Sources
- https://play.google.com/store/apps/details?id=com.wirdallatif.global.avblogdev
- https://play.google.com/store/apps/details?id=com.ahlesunnts.Alwird_AlLatif
- https://github.com/rqawasme/Wirdi (PR #7)
- https://www.salawat.com/wird-al-latif
- https://seekersguidance.org/articles/prophetic-guidance/the-complete-wird-latif-of-imam-al-haddad-with-transliteration/
- https://www.safinasociety.org/wird
- https://simplyislam.academy/blog/the-complete-wird-al-latif
- https://ia801402.us.archive.org/14/items/WirdAlLatif/wird_al-latif_text.pdf
- https://qurancomplex.gov.sa/en/techquran/dev/ · https://github.com/thetruetruth/quran-data-kfgqpc · https://github.com/m-alhamry/Quran-text-assets
