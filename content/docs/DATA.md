# Data format

All text lives in YAML files. The build scripts read them, and
`src/wird_data.py` checks them on every load. If a file breaks a rule below,
the build stops with an error that names the file and the item.

```
data/wird.yaml                 order of the wird, repeat counts, duʿā Arabic, Qurʾān references
data/translit.yaml             transliteration (one replaceable layer)
data/transcriptions/*.yaml     Qurʾān translations typed from print (third-party)
data/kfgqpc/, data/quranenc/   published third-party data, byte-identical (see THIRD_PARTY.md)
i18n/<lang>.yaml               one file per language: metadata, titles, duʿā meanings
```

## Text fields and morning/evening variants

A text field is either a plain string, or a list of **segments** when some
words change in the evening:

```yaml
arabic:
  - "اللَّهُمَّ إِنِّي "
  - {morning: "أَصْبَحْتُ", evening: "أَمْسَيْتُ"}
  - " مِنْكَ فِي نِعْمَةٍ …"
```

A string segment is said both morning and evening. A `{morning, evening}`
segment holds the two wordings; the reader and the PDF highlight it (yellow
in the morning, blue in the evening). Spaces belong to the string segments
around a variant, so keep them where they are.

If an item's Arabic has variants, its transliteration and every translation
must have them too (`tests/test_data.py` checks this).

## data/wird.yaml

```yaml
sections:
  - id: witness              # stable id; never reuse or renumber
    items:
      - id: ushhiduka        # stable id used by every other file
        repeat: 4            # omit when the line is said once
        arabic: …            # text field (duʿās)
        audio:               # optional, for later (see below)
          file: audio/…
          reciter: …
          licence: …
          start: 12.5        # seconds, optional
          end: 31.0
```

Item numbers (1–46) are not stored; they follow from the order.

Qurʾānic items have `quran` instead of `arabic`. The Arabic comes from
KFGQPC at build time:

```yaml
      - id: ikhlas
        repeat: 3
        quran:
          verses: "112:1-4"   # sura:first-last, or sura:aya
          basmala: true       # show the basmala first
      - id: muminun-97
        quran:
          verses: "23:97-98"
          opening: {replace: "وَقُل رَّبِّ", with: "رَبِّ"}   # display adjustment; see REVIEW.md R-Q1
      - id: hasbiya
        quran:
          verses: "9:129"
          from_word: "حَسۡبِيَ"   # show only from this word on
          quote: true            # read like a duʿā: has its own transliteration
                                 # and meanings, no verse translations
```

The Arabic in `opening` and `from_word` must match KFGQPC code point for code
point. Arabic marks can be typed in different orders that look the same, so
copy them from the data file; don't retype them.

## data/translit.yaml

`meta` (scheme, status, provenance, licence, version), `basmala`, `quran`
(keyed `"sura:aya"`, text of the part the wird reads) and `items` (keyed by
item id, text fields). It is a separate layer so it can be replaced wholesale
(see THIRD_PARTY.md).

## i18n/<lang>.yaml

```yaml
meta:
  lang: en                 # BCP 47 / ISO 639 code; the file name matches
  name: English
  native_name: English
  status: draft            # draft | reviewed | verified
  translator: "…"          # or null
  reviewers: []
  source: "…"
  licence: "…"
  version: "1.0"
quran:                     # where the verse translations come from
  source: quranenc         # quranenc | transcription
  key: english_rwwad
  version: "1.0.19"
  file: data/quranenc/english_rwwad/1.0.19-….json.gz
ui:
  label: EN
sections:                  # titles of the sections, by section id
  witness: {title: "…", description: "…"}
headings:                  # optional headings above items, by item id
  ikhlas: "Sūrat al-Ikhlāṣ (112)"
items:                     # meanings of the duʿās, by item id (text fields)
  ushhiduka: [ … ]
```

Third-party verse translations are never copied into `i18n/`. The file points
to them, so our files contain only material that can carry our licence. A new
language starts as `status: draft`, with an empty `items: {}` if needed. See
CONTRIBUTING.md (milestone 4).

## Transcriptions (data/transcriptions/*.yaml)

`meta` (translator, publisher, edition, scan, printed pages per sura, status,
licence), `basmala`, and `verses` keyed `"sura:aya"`. Spelling is kept as
printed.
