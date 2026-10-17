"""Third-party files are used exactly as published.

KFGQPC (text and font) and QuranEnc translations must not be modified; the
fonts are pinned too because the PDF regression depends on them.  To update
a source deliberately, replace the file, update data/third_party.sha256 and
THIRD_PARTY.md in the same commit.
"""
import hashlib
import os

import pytest

from conftest import ROOT

MANIFEST = os.path.join(ROOT, "data", "third_party.sha256")
ENTRIES = [line.split(None, 1) for line in open(MANIFEST, encoding="utf-8") if line.strip()]


@pytest.mark.parametrize("digest,path", ENTRIES, ids=[p.strip() for _, p in ENTRIES])
def test_unchanged(digest, path):
    with open(os.path.join(ROOT, path.strip()), "rb") as f:
        assert hashlib.sha256(f.read()).hexdigest() == digest
