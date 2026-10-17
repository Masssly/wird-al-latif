# -*- coding: utf-8 -*-
"""Load and check the wird's YAML data.

Files (schema in docs/DATA.md):
  data/wird.yaml                  structure, repeat counts, duʿā Arabic, Qurʾān references
  data/translit.yaml              transliteration layer (replaceable)
  data/transcriptions/*.yaml      third-party Qurʾān translations transcribed from print
  i18n/<lang>.yaml                per-language metadata, section titles, duʿā meanings

Text fields are either a plain string or a list of segments, where a segment is
a string (said morning and evening) or {morning: ..., evening: ...}.

`legacy()` returns the structures the edition 1.0 build script expects
(SECTIONS, ITEMS, DAG, HAU, ...), so the PDF can be rebuilt unchanged while
the templates are rewritten.
"""
import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATUSES = ("draft", "reviewed", "verified")
VERSES = re.compile(r"^(\d{1,3}):(\d{1,3})(?:-(\d{1,3}))?$")
REQUIRED_META = ("lang", "status", "translator", "reviewers", "source", "licence", "version")


class DataError(ValueError):
    pass


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return yaml.safe_load(f)


def _check_text(where, val):
    if isinstance(val, str):
        return
    if not isinstance(val, list) or not val:
        raise DataError(f"{where}: expected a string or a list of segments")
    for seg in val:
        if isinstance(seg, str):
            continue
        if not (isinstance(seg, dict) and set(seg) == {"morning", "evening"}
                and all(isinstance(v, str) for v in seg.values())):
            raise DataError(f"{where}: bad segment {seg!r}")


def has_variants(val):
    return isinstance(val, list) and any(isinstance(s, dict) for s in val)


def render(val, when, mark=None):
    """Flatten a text field for `when` ('morning' or 'evening').
    `mark(s)` wraps the words that differ between morning and evening."""
    if isinstance(val, str):
        return val
    out = []
    for seg in val:
        if isinstance(seg, str):
            out.append(seg)
        else:
            out.append(mark(seg[when]) if mark else seg[when])
    return "".join(out)


def parse_verses(spec):
    m = VERSES.match(spec)
    if not m:
        raise DataError(f"bad verse range {spec!r}")
    s, a, b = int(m[1]), int(m[2]), int(m[3] or m[2])
    if b < a:
        raise DataError(f"bad verse range {spec!r}")
    return s, a, b


def load():
    wird = _read("data/wird.yaml")
    translit = _read("data/translit.yaml")
    langs = {}
    for fn in sorted(os.listdir(os.path.join(ROOT, "i18n"))):
        if fn.endswith(".yaml"):
            d = _read(f"i18n/{fn}")
            langs[d["meta"]["lang"]] = d
    data = {"wird": wird, "translit": translit, "langs": langs, "transcriptions": {}}
    for code, d in langs.items():
        q = d.get("quran") or {}
        if q.get("source") == "transcription":
            data["transcriptions"][code] = _read(q["file"])
    validate(data)
    return data


def items(data):
    for sec in data["wird"]["sections"]:
        for it in sec["items"]:
            yield sec["id"], it


def validate(data):
    wird, translit = data["wird"], data["translit"]
    ids, sec_ids = [], []
    for sec in wird["sections"]:
        sec_ids.append(sec["id"])
        for it in sec["items"]:
            iid = it.get("id")
            where = f"data/wird.yaml item {iid}"
            ids.append(iid)
            unknown = set(it) - {"id", "repeat", "quran", "arabic", "audio"}
            if unknown:
                raise DataError(f"{where}: unknown keys {sorted(unknown)}")
            if "repeat" in it and not (isinstance(it["repeat"], int) and it["repeat"] > 1):
                raise DataError(f"{where}: repeat must be an integer > 1 (omit it for once)")
            q = it.get("quran")
            if q:
                parse_verses(q["verses"])
                unknown = set(q) - {"verses", "basmala", "opening", "from_word", "quote"}
                if unknown:
                    raise DataError(f"{where}: unknown quran keys {sorted(unknown)}")
            if bool(q) == ("arabic" in it):
                raise DataError(f"{where}: needs exactly one of arabic or quran")
            if "arabic" in it:
                _check_text(where, it["arabic"])
            if "audio" in it:
                a = it["audio"]
                if not (isinstance(a, dict) and {"file", "reciter", "licence"} <= set(a)
                        and set(a) <= {"file", "reciter", "licence", "start", "end"}):
                    raise DataError(f"{where}: audio needs file, reciter, licence (+ optional start, end)")
    if len(ids) != len(set(ids)) or len(sec_ids) != len(set(sec_ids)):
        raise DataError("duplicate item or section ids")
    known = set(ids)

    # transliteration: every duʿā (and quoted verse) has one, every verse read has one
    for sid, it in items(data):
        q = it.get("quran")
        if q and not q.get("quote"):
            s, a, b = parse_verses(q["verses"])
            for v in range(a, b + 1):
                if f"{s}:{v}" not in translit["quran"]:
                    raise DataError(f"data/translit.yaml: missing {s}:{v}")
        elif it["id"] not in translit["items"]:
            raise DataError(f"data/translit.yaml: missing item {it['id']}")
    for iid, val in translit["items"].items():
        if iid not in known:
            raise DataError(f"data/translit.yaml: unknown item {iid}")
        _check_text(f"data/translit.yaml {iid}", val)

    for code, d in data["langs"].items():
        meta = d.get("meta", {})
        missing = [k for k in REQUIRED_META if k not in meta]
        if missing:
            raise DataError(f"i18n/{code}.yaml: meta lacks {missing}")
        if meta["status"] not in STATUSES:
            raise DataError(f"i18n/{code}.yaml: status must be one of {STATUSES}")
        for iid, val in (d.get("items") or {}).items():
            if iid not in known:
                raise DataError(f"i18n/{code}.yaml: unknown item {iid}")
            _check_text(f"i18n/{code}.yaml {iid}", val)
        for iid in d.get("headings") or {}:
            if iid not in known:
                raise DataError(f"i18n/{code}.yaml: heading for unknown item {iid}")
        for sid in d.get("sections") or {}:
            if sid not in sec_ids:
                raise DataError(f"i18n/{code}.yaml: unknown section {sid}")
        q = d.get("quran") or {}
        if q.get("file") and not os.path.exists(os.path.join(ROOT, q["file"])):
            raise DataError(f"i18n/{code}.yaml: {q['file']} not found")

    for code, t in data["transcriptions"].items():
        for sid, it in items(data):
            q = it.get("quran")
            if q and not q.get("quote"):
                s, a, b = parse_verses(q["verses"])
                for v in range(a, b + 1):
                    if f"{s}:{v}" not in t["verses"]:
                        raise DataError(f"{code} transcription: missing {s}:{v}")


# ---------------------------------------------------------------- edition 1.0 adapter

def legacy(data=None):
    """Return (SECTIONS, ITEMS, DAG, DAG_BISM, HAU, HAU_BISM) in the shape of
    the edition 1.0 modules src/content.py, src/dagbani.py and src/hausa.py.
    Variant words are wrapped in ⟦…⟧, which build.py turns into highlights."""
    data = data or load()
    en, tl = data["langs"]["en"], data["translit"]
    mark = lambda s: f"⟦{s}⟧"
    sup = lambda n: f"<sup>{n}</sup>"

    # build.py knows sections as s1..s6 (it special-cases s1 and s5)
    sec_key = {s["id"]: f"s{k}" for k, s in enumerate(data["wird"]["sections"], 1)}
    sections = [(sec_key[s["id"]], en["sections"][s["id"]]["title"], en["sections"][s["id"]]["description"])
                for s in data["wird"]["sections"]]
    out = []
    for sid, it in items(data):
        sid = sec_key[sid]
        iid = it["id"]
        q = it.get("quran") or {}
        d = dict(sec=sid, ar=None, tr=None, en=None, heading=en.get("headings", {}).get(iid),
                 count=f"{it['repeat']}×" if "repeat" in it else None,
                 quran=None, bism=bool(q.get("basmala")), ev=None, ref=None)
        if q.get("quote"):
            # edition 1.0 only quotes the end of 9:129 (from حَسۡبِيَ)
            assert q["verses"] == "9:129" and q["from_word"] == "\u062D\u064E\u0633\u06E1\u0628\u0650\u064A\u064E"  # حَسۡبِيَ
            d["quran"] = "9:129-part"
            d["ref"] = en["ui"]["from_quran"].format(ref=q["verses"])
        elif q:
            s, a, b = parse_verses(q["verses"])
            d["quran"] = [(s, a, b)]
            if "opening" in q:
                # edition 1.0 hard-codes this adjustment in build.py
                assert (s, a) == (23, 97) and q["opening"] == {"replace": "\u0648\u064E\u0642\u064F\u0644\u0020\u0631\u0651\u064E\u0628\u0651\u0650", "with": "\u0631\u064E\u0628\u0651\u0650"}
            verses = " ".join(f"{sup(v)}{tl['quran'][f'{s}:{v}']}" for v in range(a, b + 1))
            d["tr"] = f"{tl['basmala']}<br>{verses}" if d["bism"] else verses
        if "arabic" in it:
            d["ar"] = render(it["arabic"], "morning", mark if has_variants(it["arabic"]) else None)
        if not q or q.get("quote"):
            tr, mean = tl["items"][iid], en["items"][iid]
            d["tr"] = render(tr, "morning", mark)
            d["en"] = render(mean, "morning", mark)
            fields = [it.get("arabic"), tr, mean]
            if any(has_variants(f) for f in fields):
                d["ev"] = tuple(render(f, "evening", mark) for f in fields)
        out.append(d)

    def table(code):
        t = data["transcriptions"][code]
        return {tuple(int(x) for x in k.split(":")): v for k, v in t["verses"].items()}, t["basmala"]

    dag, dag_bism = table("dag")
    hau, hau_bism = table("ha")
    return sections, out, dag, dag_bism, hau, hau_bism
