"""Consistency of the YAML data and of the third-party sources it points to."""
import copy
import gzip
import json
import os

import pytest

from conftest import ROOT
from wird_data import DataError, items, load, parse_verses, render, validate

DATA = load()


def test_ids_and_numbering():
    ids = [it["id"] for _, it in items(DATA)]
    assert len(ids) == 46
    assert [s["id"] for s in DATA["wird"]["sections"]] == [
        "quran", "protection", "witness", "asking", "morning-evening", "glorification"]


def test_language_files():
    assert set(DATA["langs"]) == {"en", "de", "ha", "dag"}
    statuses = {"en": "reviewed", "de": "reviewed", "ha": "draft", "dag": "draft"}
    for code, d in DATA["langs"].items():
        assert d["meta"]["lang"] == code
        assert d["meta"]["status"] == statuses[code]


def test_english_covers_every_dua():
    en = DATA["langs"]["en"]["items"]
    for _, it in items(DATA):
        q = it.get("quran")
        assert (it["id"] in en) == (not q or bool(q.get("quote"))), it["id"]


def test_german_covers_every_dua():
    """German duʿā meanings are complete too (unlike Hausa/Dagbanli, which have none yet)."""
    de = DATA["langs"]["de"]["items"]
    for _, it in items(DATA):
        q = it.get("quran")
        assert (it["id"] in de) == (not q or bool(q.get("quote"))), it["id"]


def test_variants_line_up():
    """An item that changes in the evening changes in the Arabic, the
    transliteration and every complete meaning alike. German may split the
    variant differently from English (German grammar needs it; see
    i18n/de.yaml), so this only checks that a variant exists somewhere, not
    that the segments line up word for word."""
    en, de, tl = DATA["langs"]["en"]["items"], DATA["langs"]["de"]["items"], DATA["translit"]["items"]
    n = lambda v: sum(isinstance(s, dict) for s in v) if isinstance(v, list) else 0
    for _, it in items(DATA):
        if "arabic" not in it:
            continue
        has_variant = n(it["arabic"]) > 0
        assert has_variant == (n(tl[it["id"]]) > 0) == (n(en[it["id"]]) > 0), it["id"]
        if it["id"] in de:
            assert has_variant == (n(de[it["id"]]) > 0), it["id"]


def test_render():
    v = ["a ", {"morning": "M", "evening": "E"}, " b"]
    assert render(v, "morning") == "a M b"
    assert render(v, "evening", lambda s: f"[{s}]") == "a [E] b"
    assert render("plain", "evening") == "plain"


KF = {(x["sora"], x["aya_no"]): x["aya_text"]
      for x in json.load(open(os.path.join(ROOT, "data/kfgqpc/data/hafsData_v18.json"), encoding="utf-8"))}


def test_quran_references_exist_and_adjustments_apply():
    for _, it in items(DATA):
        q = it.get("quran")
        if not q:
            continue
        s, a, b = parse_verses(q["verses"])
        for v in range(a, b + 1):
            assert (s, v) in KF, (it["id"], s, v)
        if "opening" in q:
            assert KF[(s, a)].startswith(q["opening"]["replace"]), it["id"]
        if "from_word" in q:
            assert q["from_word"] in KF[(s, a)], it["id"]


@pytest.mark.parametrize("code", ["en", "de"])
def test_quranenc_pointer_matches_file(code):
    q = DATA["langs"][code]["quran"]
    d = json.load(gzip.open(os.path.join(ROOT, q["file"]), "rt", encoding="utf-8"))
    assert d["edition"]["sourceKey"] == q["key"]
    assert d["edition"]["version"] == q["version"]
    for _, it in items(DATA):
        if it.get("quran") and not it["quran"].get("quote"):
            s, a, b = parse_verses(it["quran"]["verses"])
            for v in range(a, b + 1):
                assert d["verses"][str(s)][str(v)]["text"]


def _broken(mutate):
    d = copy.deepcopy(DATA)
    mutate(d)
    with pytest.raises(DataError):
        validate(d)


def test_validator_rejects_bad_data():
    first = lambda d, sec=2: d["wird"]["sections"][sec]["items"][0]
    _broken(lambda d: first(d).__setitem__("repeat", 1))
    _broken(lambda d: first(d).__setitem__("colour", "red"))
    _broken(lambda d: first(d).__setitem__("arabic", ["x", {"morning": "a"}]))
    _broken(lambda d: first(d, 0)["quran"].__setitem__("verses", "112:4-1"))
    _broken(lambda d: d["langs"]["en"]["items"].__setitem__("no-such-item", "x"))
    _broken(lambda d: d["langs"]["de"]["meta"].__setitem__("status", "final"))
    _broken(lambda d: d["translit"]["quran"].pop("112:3"))
    _broken(lambda d: d["transcriptions"]["dag"]["verses"].pop("59:22"))
    _broken(lambda d: first(d).__setitem__("audio", {"file": "a.opus"}))


def test_validator_accepts_audio():
    d = copy.deepcopy(DATA)
    d["wird"]["sections"][0]["items"][0]["audio"] = {
        "file": "audio/ikhlas.opus", "reciter": "N.N.", "licence": "CC BY-SA 4.0", "start": 0.0, "end": 21.5}
    validate(d)
