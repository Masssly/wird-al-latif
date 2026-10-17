# Project ground rules (for every agent: Claude Code, Lovable, others)

al-Wird al-Laṭīf open edition: a free, phone-first text edition of the
litany of Imām al-Ḥaddād, with a PDF and a website per language. Owner and
compiler: Mohammed Sadat Abdulai. Read SPEC.md for the plan. HANDOFF.md has
the history and the decisions already made; don't reopen those decisions.

## Text integrity: non-negotiable
- **Never modify third-party text or fonts.** That means `data/kfgqpc/` (Qurʾān text and font), `data/quranenc/` (English and German translations) and `fonts/`. Their checksums are tested (`data/third_party.sha256`). Credit the source and version wherever they are shown.
- **Never "correct" the duʿā Arabic, the transliteration, or the Hausa and Dagbanli transcriptions** (`data/wird.yaml`, `data/translit.yaml`, `data/transcriptions/`). They are unproofread, and the owner's reviewers decide changes. Put doubts in REVIEW.md instead.
- **Don't retype Arabic: copy it.** Arabic marks can be stored in different orders that look identical but are different text.
- **Treat AI "corrections" of Arabic, Hausa, Dagbanli and Ghanaian names with suspicion,** in code, comments and generated content alike. Use "Dagbanli" in our own text.
- **Nothing from rqawasme/Wirdi** until its licence is clear (THIRD_PARTY.md).

## Where things live
- **Text** is in YAML: `data/wird.yaml` holds the structure and the Arabic, `data/translit.yaml` the transliteration, and `i18n/<lang>.yaml` the per-language text. The format is in `docs/DATA.md`, and `src/wird_data.py` validates it.
- **The website and PDFs are generated** from the YAML by the Python build (`src/`). Don't hard-code wird text in pages or components. Read it from the data.
- **Third-party Qurʾān translations** stay in `data/` and are referenced, not copied into `i18n/`.

## Stack constraints (SPEC.md)
- **Static output only,** served by GitHub Pages and kept portable to GitLab Pages. No backend, database, auth or accounts.
- **No tracking, analytics, third-party scripts, CDNs or remote fonts.** Serve everything from the repo.
- **Reading progress stays in the reader's own browser** (`localStorage`).
- **Not a habit tracker:** no reminders, streaks or notifications.
- **Accessibility:** semantic HTML, correct `lang`/`dir`, RTL Arabic, keyboard use and sufficient contrast.

## Working together on this repository
- The repository is edited mainly by Claude Code; Lovable edits it too. Pull the latest default branch before starting, and keep each change small and focused.
- **Never rewrite published history:** no force-push, and no rebasing, amending or squashing of pushed commits.
- Keep the default branch working: `python3 -m pytest -q` must pass.
- `tests/test_pdf_regression.py` compares the PDF glyph for glyph with `tests/baseline/`. If a change alters the PDF on purpose, regenerate the baseline in the same commit and say why.
- **No LICENSE file** until the owner confirms the licences. Don't add a licence or a licence badge.

## Build and test
```sh
pip install -r requirements.txt   # WeasyPrint 70.0; Inter font installed system-wide
python3 src/build.py              # → dist/al-Wird-al-Latif.pdf
python3 -m pytest -q
```
