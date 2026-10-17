# SPEC: al-Wird al-Laṭīf Open Edition (website + multilingual PDFs)

Read HANDOFF.md and CLAUDE.md in this folder first. This spec supersedes the "Website" section of HANDOFF.md.

## Purpose
A free, open, phone-first edition of al-Wird al-Laṭīf of Imām ʿAbd Allāh b. ʿAlawī al-Ḥaddād. It is a plain text edition, not a habit tracker. Owner and compiler: Mohammed Sadat Abdulai. The project is personal and devotional, non-commercial, and meant for the commons. A secondary goal is teaching it to children.

## Positioning (decided)
- Closest prior art is rqawasme/Wirdi (Flutter iOS/Android habit tracker; Wird al-Laṭīf merged in PR #7, Sept 2026; Arabic + transliteration + English; no licence stated). Do NOT build tracker features: no reminders, streaks or accounts.
- Our differentiators: web + downloadable PDF per language, Hausa and Dagbanli (plus German) Qurʾān translations, vowelled Arabic with Madinah muṣḥaf script for verses, colour-coded names, open licence, structured data anyone can translate, kids mode.
- I (Mohammed) have posted an issue on the Wirdi repo asking about the licence of its data and offering to compare texts. Until they reply, DO NOT copy anything from Wirdi's data. Record any reply in THIRD_PARTY.md.

## Constraints and rules
- Never modify KFGQPC text/font or QuranEnc translations. Credit the source and version. Keep them separate from our CC-licensed material.
- The duʿā Arabic and the Dagbanli/Hausa transcriptions are unproofread. Do not "correct" them from memory. Flag doubts in `REVIEW.md` instead.
- Provenance of the duʿā Arabic/transliteration (derived from the circulating Ashnataar © 2012 edition) is unresolved. Mark it in THIRD_PARTY.md and keep the transliteration as a replaceable layer.
- Proposed licences: CC BY-SA 4.0 for our text and English duʿā translations, MIT for code. Confirm with me before adding LICENSE files.
- No tracking, no analytics, no third-party scripts or CDNs. Per-reader progress stays in localStorage.
- Hosting: GitHub Pages via GitHub Actions, static output only, so it stays portable to GitLab Pages.

## Architecture
1. Data (single source of truth)
   - `data/wird.yaml`: sections, items, ids, repeat counts, morning/evening variants as explicit structure (replace the `⟦…⟧` text markers), Qurʾān items as sura:āya references.
   - `i18n/<lang>.yaml`: per-item translation, and Qurʾān translations keyed by `sura:āya`. Each file has metadata: `lang`, `status` (draft | reviewed | verified), `translator`, `reviewers`, `source`, `licence`, `version`.
   - Third-party Qurʾān data stays in `data/` unchanged.
2. Build (Python + Jinja, reuse existing WeasyPrint pipeline)
   - Step 0: migrate `src/content.py`, `dagbani.py`, `hausa.py` into YAML. Add a test that the regenerated English PDF text matches the current `dist/al-Wird-al-Latif.pdf`. Do this before anything else.
   - Outputs: `site/<lang>/index.html` (reader), `site/<lang>/wird-<lang>.pdf`, a landing page with language picker, `site/about`, `site/sources`.
3. CI: GitHub Actions builds everything on push and deploys to Pages. The PDFs are build artifacts, not committed.

## Reader page (v1)
- Mobile-first, single column, works offline (service worker).
- Morning/evening toggle, defaulting by local time.
- Per-item tap counter for the repeat badges, with a checklist stored locally.
- Text-size control, light/dark, RTL-correct Arabic.
- Same colour code as the PDF (Allah red, Muḥammad ﷺ green, silent letters grey), with a legend.
- Language switcher that shows each language's status badge.
- Accessibility: semantic HTML, proper `lang`/`dir` attributes, keyboard-navigable, sufficient contrast.

## Kids mode (v2, needs scholar/teacher review before release)
One item per screen, large text, tap to reveal the meaning, simple vocabulary cards, progress stars. No ads, no accounts.

## Audio (v3, deferred, I will handle recordings)
Design the data model now so it can be added later: an optional `audio` field per item (file, reciter, licence) and per-item timestamps. Do not add any third-party audio without written permission.

## Languages
- v1: English (own duʿā translations; Qurʾān via QuranEnc Rowwad), German (Bubenheim), Hausa (Gumi), Dagbanli (Gbetobu). Arabic and transliteration for all.
- Later: French, Indonesian, Urdu, Turkish, Swahili, via PRs or Weblate. Contribution guide in CONTRIBUTING.md. New languages start as `draft`.

## Milestones
1. Repo init, THIRD_PARTY.md, REVIEW.md, YAML migration + regression test.
2. Jinja templates, per-language PDF builds, CI + Pages deploy.
3. Reader page features above.
4. CONTRIBUTING.md, status badges, call for proofreaders (Arabic first, then Hausa/Dagbanli native speakers).
5. Kids mode, then audio.

## Open questions (ask me, don't assume)
- Licence confirmation, and the repo/org name and domain.
- Whether to keep the duʿā transliteration or rewrite it.
- Whether to build a Commons-eligible edition (needs Pickthall + a free font, no KFGQPC/QuranEnc).

## Decisions log
- 2026-10-15 · Hosting: **GitHub** (repo Masssly/wird-al-latif, GitHub Pages via GitHub Actions). Output stays static so a move to GitLab Pages remains possible.
- 2026-10-17 · Single home: **Masssly/wird-al-latif-guide**, the repository Lovable created for its project, because Lovable can only sync with a repository it creates. The history of Masssly/wird-al-latif was merged in, and that repository is to be archived.
