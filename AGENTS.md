<!-- LOVABLE:BEGIN -->
> [!IMPORTANT]
> This project is connected to [Lovable](https://lovable.dev). Avoid rewriting
> published git history — force pushing, or rebasing/amending/squashing commits
> that are already pushed — as it rewrites history on Lovable's side and the
> user will likely lose their project history.
>
> Commits you push to the connected branch sync back to Lovable and show up in
> the editor, so keep the branch in a working state.
<!-- LOVABLE:END -->

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
One repository, one copy of the text, two outputs.

| Path | What |
|---|---|
| `data/`, `i18n/` | **All text.** `data/wird.yaml` holds the structure and the Arabic, `data/translit.yaml` the transliteration, and `i18n/<lang>.yaml` the per-language text. The format is in `docs/DATA.md`. Third-party Qurʾān text is in `data/kfgqpc/` and `data/quranenc/`, referenced and never copied into `i18n/`. |
| `src/`, `public/` | The website (TanStack Start + React, made with Lovable). It reads the text from `src/data/wird.json`. |
| `scripts/build-wird-data.ts` | Builds `src/data/wird.json` from `data/` and `i18n/`. **Never edit `src/data/wird.json` by hand.** After any change in `data/` or `i18n/`, run `bun scripts/build-wird-data.ts` and commit the result. A test fails while it is out of date. |
| `pdf/` | The PDF build (Python, WeasyPrint): `pdf/build.py`, and `pdf/wird_data.py`, which loads and validates the YAML. |
| `tests/` | Python tests: data checks, third-party checksums, and the PDF compared glyph for glyph with `tests/baseline/`. |
| `src/test/` | Website tests (Vitest). |
| `public/fonts/` | Copies of the bundled fonts for the website. They must stay byte-identical to `fonts/` and `data/kfgqpc/font/`; their checksums are tested. |

Don't hard-code wird text in pages or components; read it from the data. Don't add a second copy of the data anywhere (no `content/` folder).

## Stack constraints (SPEC.md)
- **Static output only,** served by GitHub Pages and kept portable to GitLab Pages. No backend, database, auth or accounts.
- **No tracking, analytics, third-party scripts, CDNs or remote fonts.** Serve everything from the repo.
- **Reading progress stays in the reader's own browser** (`localStorage`).
- **Not a habit tracker:** no reminders, streaks or notifications.
- **Accessibility:** semantic HTML, correct `lang`/`dir`, RTL Arabic, keyboard use and sufficient contrast.

## Working together on this repository
- The repository is edited mainly by Claude Code; Lovable edits it too, syncing its `main` branch both ways. Pull the latest `main` before starting, and keep each change small and focused.
- **Never rewrite published history:** no force-push, and no rebasing, amending or squashing of pushed commits.
- Keep the default branch working: `python3 -m pytest -q` and `bunx vitest run` must pass.
- `tests/test_pdf_regression.py` compares the PDF glyph for glyph with `tests/baseline/`. If a change alters the PDF on purpose, regenerate the baseline in the same commit and say why.
- **No LICENSE file** until the owner confirms the licences. Don't add a licence or a licence badge.

## Build and test
```sh
# website
bun install
bun scripts/build-wird-data.ts    # after changing data/ or i18n/
bun run dev                       # or: bun run build
bunx vitest run

# PDF and data checks
pip install -r requirements.txt   # WeasyPrint 70.0; Inter font installed system-wide
python3 pdf/build.py              # → build/al-Wird-al-Latif.pdf
python3 -m pytest -q
```
