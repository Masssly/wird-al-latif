# Raw recording sessions

Unedited, full-length recordings of the owner reciting the wird, kept here so they can be
pulled down and re-edited later if the cut clips in `public/audio/` need fixing — not referenced
by the website or the build; nothing reads this folder automatically.

| File | Session | Marker convention |
|---|---|---|
| `morning-wird-raw.m4a` | Full morning wird, one take | said "end" after each completed item, "cancel" before redoing one |
| `evening-azkaar-raw.m4a` | Full evening azkār, one take | said the item's number (1–46) at the start of each |

Both are the owner's own recitation; same licence as the cut clips derived from them
(`data/wird.yaml`'s `audio.licence` per item, currently CC BY-SA 4.0).

To pull one down: `curl -LO https://raw.githubusercontent.com/Masssly/wird-al-latif/main/data/audio-sessions/<file>`
(or any branch name in place of `main`), or just download it from the file's page on github.com.
