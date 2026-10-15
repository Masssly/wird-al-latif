"""The YAML holds exactly what the edition 1.0 Python modules held.

tests/baseline/legacy_content.json is a frozen dump of src/content.py,
src/dagbani.py and src/hausa.py as received in the handoff bundle.
"""
import json
import os

from conftest import ROOT
from wird_data import legacy

SNAP = json.load(open(os.path.join(ROOT, "tests", "baseline", "legacy_content.json"), encoding="utf-8"))


def _norm(it):
    it = dict(it)
    if isinstance(it["quran"], (list, tuple)):
        it["quran"] = [list(x) for x in it["quran"]]
    if it["ev"]:
        it["ev"] = list(it["ev"])
    return it


def test_sections():
    sections = legacy()[0]
    assert [list(s) for s in sections] == SNAP["SECTIONS"]


def test_items():
    items = legacy()[1]
    assert len(items) == len(SNAP["ITEMS"]) == 46
    for n, (new, old) in enumerate(zip(items, SNAP["ITEMS"]), 1):
        assert _norm(new) == old, f"item {n}"


def test_transcriptions():
    _, _, dag, dag_bism, hau, hau_bism = legacy()
    assert {f"{s}:{a}": t for (s, a), t in dag.items()} == SNAP["DAG"]
    assert {f"{s}:{a}": t for (s, a), t in hau.items()} == SNAP["HAU"]
    assert dag_bism == SNAP["DAG_BISM"]
    assert hau_bism == SNAP["HAU_BISM"]
