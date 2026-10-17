"""Read what a WeasyPrint PDF actually draws, for regression tests.

Walks each page's content stream and returns every text run with its font,
size, fill colour, position, glyph ids and Unicode text, every filled
rectangle (the morning/evening highlights and boxes) and every link.

Comparing glyph ids rather than extracted text matters for the Arabic: the
PDF's ToUnicode maps lose mark order and ligature structure, so two different
vowellings can extract to the same string, while their glyphs differ.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import pikepdf


@dataclass
class Glyph:
    gid: int
    text: str
    x: float  # left edge in page space (points, origin bottom-left)
    width: float


@dataclass
class Run:
    page: int  # 1-based
    font: str  # base font without subset prefix, e.g. "AmiriR", "Inter-Italic"
    size: float
    color: tuple  # RGB 0..1, rounded
    x: float
    y: float  # baseline, page space
    glyphs: list[Glyph] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "".join(g.text for g in self.glyphs)

    @property
    def x1(self) -> float:
        return max((g.x + g.width for g in self.glyphs), default=self.x)

    @property
    def x0(self) -> float:
        return min((g.x for g in self.glyphs), default=self.x)

    @property
    def gids(self) -> list[int]:
        return [g.gid for g in self.glyphs]


@dataclass
class Rect:
    page: int
    x: float
    y: float
    w: float
    h: float
    color: tuple


@dataclass
class Link:
    page: int
    rect: tuple
    dest: str | None


def _mul(a, b):
    a0, a1, a2, a3, a4, a5 = a
    b0, b1, b2, b3, b4, b5 = b
    return (
        a0 * b0 + a1 * b2,
        a0 * b1 + a1 * b3,
        a2 * b0 + a3 * b2,
        a2 * b1 + a3 * b3,
        a4 * b0 + a5 * b2 + b4,
        a4 * b1 + a5 * b3 + b5,
    )


def _apply(m, x, y):
    return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])


_BF = re.compile(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*(\[[^\]]*\]|<[0-9A-Fa-f]*>)")


def _hex_to_text(h: bytes) -> str:
    raw = bytes.fromhex(h.decode())
    return raw.decode("utf-16-be", errors="replace")


def _parse_tounicode(stream: bytes) -> dict[int, str]:
    out: dict[int, str] = {}
    for block in re.findall(rb"beginbfchar(.*?)endbfchar", stream, re.S):
        for src, dst in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]*)>", block):
            out[int(src, 16)] = _hex_to_text(dst)
    for block in re.findall(rb"beginbfrange(.*?)endbfrange", stream, re.S):
        for lo, hi, dst in _BF.findall(block):
            lo, hi = int(lo, 16), int(hi, 16)
            if dst.startswith(b"["):
                items = re.findall(rb"<([0-9A-Fa-f]*)>", dst)
                for i, h in enumerate(items):
                    out[lo + i] = _hex_to_text(h)
            else:
                base = bytes.fromhex(dst[1:-1].decode())
                for i in range(hi - lo + 1):
                    b = bytearray(base)
                    b[-1] += i
                    out[lo + i] = bytes(b).decode("utf-16-be", errors="replace")
    return out


class _Font:
    def __init__(self, obj):
        self.base = str(obj.BaseFont).lstrip("/")
        self.base = self.base.split("+", 1)[-1]
        desc = obj.DescendantFonts[0]
        self.dw = float(desc.get("/DW", 1000))
        self.widths: dict[int, float] = {}
        w = desc.get("/W")
        if w is not None:
            w = list(w)
            i = 0
            while i < len(w):
                first = int(w[i])
                nxt = w[i + 1]
                if isinstance(nxt, pikepdf.Array):
                    for j, val in enumerate(nxt):
                        self.widths[first + j] = float(val)
                    i += 2
                else:
                    last = int(nxt)
                    val = float(w[i + 2])
                    for c in range(first, last + 1):
                        self.widths[c] = val
                    i += 3
        tu = obj.get("/ToUnicode")
        self.cmap = _parse_tounicode(tu.read_bytes()) if tu is not None else {}

    def width(self, cid: int) -> float:
        return self.widths.get(cid, self.dw)


def _rgb(op, operands):
    vals = [float(v) for v in operands if not isinstance(v, pikepdf.Name)]
    if op in ("g",):
        v = vals[0]
        return (v, v, v)
    if op in ("k",):
        c, m, y, k = vals
        return ((1 - c) * (1 - k), (1 - m) * (1 - k), (1 - y) * (1 - k))
    if len(vals) == 3:
        return tuple(vals)
    if len(vals) == 1:
        return (vals[0],) * 3
    return (0.0, 0.0, 0.0)


def _round(c):
    return tuple(round(v, 3) for v in c)


def read_pdf(path: str | Path):
    """Return (runs, rects, links, page_count, page_height)."""
    pdf = pikepdf.open(str(path))
    runs: list[Run] = []
    rects: list[Rect] = []
    links: list[Link] = []
    font_cache: dict = {}

    # Named destinations, for the Contents links.
    dests = {}
    try:
        names = pdf.Root.Names.Dests.Names
        for i in range(0, len(names), 2):
            dests[str(names[i])] = names[i + 1]
    except AttributeError:
        pass

    page_height = 0.0
    for pno, page in enumerate(pdf.pages, 1):
        mb = [float(v) for v in page.MediaBox]
        page_height = mb[3] - mb[1]
        fonts = {}
        res = page.Resources
        if "/Font" in res:
            for name, fobj in res.Font.items():
                key = fobj.objgen
                if key not in font_cache:
                    font_cache[key] = _Font(fobj)
                fonts[name] = font_cache[key]

        for annot in page.get("/Annots", []):
            if annot.get("/Subtype") == "/Link":
                d = annot.get("/Dest")
                links.append(
                    Link(pno, tuple(float(v) for v in annot.Rect), str(d) if d is not None else None)
                )

        ctm = (1, 0, 0, 1, 0, 0)
        stack = []
        fill = (0.0, 0.0, 0.0)
        path_rects = []
        tm = tlm = (1, 0, 0, 1, 0, 0)
        font = None
        size = 0.0
        tc = tw = 0.0
        th = 1.0
        tl = 0.0
        rise = 0.0

        def show(items):
            nonlocal tm
            run = None
            for it in items:
                if not isinstance(it, (bytes, pikepdf.String)):
                    adj = float(it)
                    tx = -adj / 1000.0 * size * th
                    tm = _mul((1, 0, 0, 1, tx, 0), tm)
                    continue
                data = bytes(it)
                for i in range(0, len(data) - 1, 2):
                    cid = (data[i] << 8) | data[i + 1]
                    trm = _mul(_mul((size * th, 0, 0, size, 0, rise), tm), ctm)
                    w0 = font.width(cid) / 1000.0
                    adv = (w0 * size + tc) * th
                    if run is None:
                        run = Run(pno, font.base, round(abs(trm[3]), 2), _round(fill), trm[4], trm[5])
                    tm = _mul((1, 0, 0, 1, adv, 0), tm)
                    nx = _mul(_mul((size * th, 0, 0, size, 0, rise), tm), ctm)[4]
                    run.glyphs.append(Glyph(cid, font.cmap.get(cid, ""), min(trm[4], nx), abs(nx - trm[4])))
            if run is not None and run.glyphs:
                runs.append(run)

        for operands, op in pikepdf.parse_content_stream(page):
            op = str(op)
            if op == "q":
                stack.append((ctm, fill))
            elif op == "Q":
                ctm, fill = stack.pop()
            elif op == "cm":
                ctm = _mul(tuple(float(v) for v in operands), ctm)
            elif op in ("rg", "g", "k", "sc", "scn"):
                fill = _rgb(op, operands)
            elif op == "re":
                x, y, w, h = (float(v) for v in operands)
                path_rects.append((x, y, w, h))
            elif op in ("f", "F", "f*", "B", "B*", "b", "b*"):
                for x, y, w, h in path_rects:
                    x0, y0 = _apply(ctm, x, y)
                    x1, y1 = _apply(ctm, x + w, y + h)
                    rects.append(
                        Rect(pno, min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0), _round(fill))
                    )
                path_rects = []
            elif op in ("n", "S", "s", "W", "W*"):
                if op != "W" and op != "W*":
                    path_rects = []
            elif op == "BT":
                tm = tlm = (1, 0, 0, 1, 0, 0)
            elif op == "Tf":
                font = fonts[operands[0]]
                size = float(operands[1])
            elif op == "Tc":
                tc = float(operands[0])
            elif op == "Tw":
                tw = float(operands[0])
            elif op == "Tz":
                th = float(operands[0]) / 100.0
            elif op == "TL":
                tl = float(operands[0])
            elif op == "Ts":
                rise = float(operands[0])
            elif op == "Td":
                tlm = _mul((1, 0, 0, 1, float(operands[0]), float(operands[1])), tlm)
                tm = tlm
            elif op == "TD":
                tl = -float(operands[1])
                tlm = _mul((1, 0, 0, 1, float(operands[0]), float(operands[1])), tlm)
                tm = tlm
            elif op == "Tm":
                tlm = tm = tuple(float(v) for v in operands)
            elif op == "T*":
                tlm = _mul((1, 0, 0, 1, 0, -tl), tlm)
                tm = tlm
            elif op == "Tj":
                show([operands[0]])
            elif op == "TJ":
                show(list(operands[0]))
    return runs, rects, links, len(pdf.pages), page_height


def signature(path):
    """Everything visible on the pages, in a form that can be compared with ==."""
    runs, rects, links, pages, _ = read_pdf(path)
    return {
        "pages": pages,
        "runs": [
            (r.page, r.font, r.size, r.color, round(r.x, 2), round(r.y, 2), tuple(r.gids))
            for r in runs
        ],
        "rects": [
            (b.page, b.color, round(b.x, 2), round(b.y, 2), round(b.w, 2), round(b.h, 2))
            for b in rects
        ],
        "links": [(l.page, tuple(round(v, 2) for v in l.rect)) for l in links],
    }


def page_text(path, page):
    """Unicode text of one page's runs, for readable failure messages."""
    runs = read_pdf(path)[0]
    return " ".join(r.text for r in runs if r.page == page)
