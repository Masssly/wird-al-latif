"""Building from the YAML reproduces the edition 1.0 PDF glyph for glyph.

The baseline is the PDF shipped in the handoff bundle.  The comparison covers
every glyph id, font, size, colour and position, every filled rectangle
(highlights, boxes, badges) and every link.  Glyph-level output depends on the
renderer, so the test only runs with WeasyPrint 70.0 and the Inter font.
"""
import os
import shutil
import subprocess
import sys

import pytest

from conftest import ROOT
from pdfglyphs import page_text, signature

BASELINE = os.path.join(ROOT, "tests", "baseline", "al-Wird-al-Latif-1.0.pdf")
OUT = os.path.join(ROOT, "dist", "al-Wird-al-Latif.pdf")


def _renderer_ok():
    try:
        import weasyprint
    except ImportError:
        return "weasyprint not installed"
    if weasyprint.__version__ != "70.0":
        return f"needs WeasyPrint 70.0, found {weasyprint.__version__}"
    if shutil.which("fc-list") is None or "Inter" not in subprocess.run(
            ["fc-list", ":family=Inter"], capture_output=True, text=True).stdout:
        return "the Inter font is not installed"
    return None


@pytest.fixture(scope="module")
def built():
    why = _renderer_ok()
    if why:
        pytest.skip(why)
    subprocess.run([sys.executable, os.path.join(ROOT, "src", "build.py")], check=True, cwd=ROOT)
    return signature(OUT)


@pytest.fixture(scope="module")
def baseline():
    return signature(BASELINE)


def test_page_count(built, baseline):
    assert built["pages"] == baseline["pages"] == 77


def test_glyphs(built, baseline):
    for a, b in zip(built["runs"], baseline["runs"]):
        if a != b:
            page = b[0]
            pytest.fail(f"first difference on page {page}:\n built:    {page_text(OUT, page)[:400]}\n"
                        f" baseline: {page_text(BASELINE, page)[:400]}")
    assert len(built["runs"]) == len(baseline["runs"])


def test_boxes_and_highlights(built, baseline):
    assert built["rects"] == baseline["rects"]


def test_links(built, baseline):
    assert built["links"] == baseline["links"]
