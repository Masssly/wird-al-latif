# CLAUDE.md
Read SPEC.md first (it supersedes the Website section of HANDOFF.md), then HANDOFF.md for history and decisions.

Build: `python3 src/build.py` → `dist/al-Wird-al-Latif.pdf` (WeasyPrint 70.0, Inter installed system-wide). Test: `python3 -m pytest -q`.
Text lives in YAML (`data/wird.yaml`, `data/translit.yaml`, `data/transcriptions/`, `i18n/`); the format is in docs/DATA.md. `src/wird_data.py` loads and validates it.

Rules:
- Never modify KFGQPC or QuranEnc files (checksums in `data/third_party.sha256` are tested). Credit source and version.
- The duʿā Arabic and the Dagbanli/Hausa transcriptions are unproofread. Don't "fix" them from memory; add a note to REVIEW.md.
- Copy Arabic code point for code point; never retype it (marks can be ordered differently and look the same).
- `tests/test_pdf_regression.py` requires the PDF to match `tests/baseline/` glyph for glyph. If an intended change alters the PDF, regenerate the baseline in the same commit and say why.
- Nothing from rqawasme/Wirdi until its licence is clear (THIRD_PARTY.md).
- No LICENSE file until the owner confirms the licences.
- Owner: Mohammed Sadat Abdulai (compiler). Keep kids' material simple and scholar-reviewable.
