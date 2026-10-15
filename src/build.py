# -*- coding: utf-8 -*-
"""Builds the phone edition of al-Wird al-Latif (single-column, 72x128 mm pages)."""
import sys, re, json, gzip, glob, unicodedata, html as _html
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from weasyprint import HTML
from wird_data import legacy
SECTIONS, ITEMS, DAG, DAG_BISM, HAU, HAU_BISM = legacy()

EDITION = "Edition 1.0 · October 2026"
COMPILER = "Mohammed Sadat Abdulai"

# ---------------------------------------------------------------- sources
KF = os.path.join(ROOT, "data", "kfgqpc")
KFD = {(x["sora"], x["aya_no"]): x["aya_text"] for x in json.load(open(f"{KF}/data/hafsData_v18.json", encoding="utf-8"))}
QE = {}
for key in ("english_rwwad", "german_bubenheim"):
    d = json.load(gzip.open(glob.glob(os.path.join(ROOT, "data", "quranenc", key, "*.json.gz"))[0], "rt", encoding="utf-8"))
    QE[key] = d
QE_META = {k: (v["edition"]["name"], v["edition"]["version"], v["edition"]["sourceUrl"]) for k, v in QE.items()}

def kf(s, a, nonum=False):
    t = KFD[(s, a)]
    return t.rsplit(" ", 1)[0] if nonum else t

def qe(key, s, a):
    t = QE[key]["verses"][str(s)][str(a)]["text"]
    return re.sub(r"\s*\[\d+\]", "", t).strip()   # footnote markers omitted (footnotes not reproduced)

KF_BISM = kf(1, 1, nonum=True)

def quran_ar(spec, bism):
    parts = []
    for s, a, b in spec:
        txt = " ".join(kf(s, i) for i in range(a, b + 1))
        if (s, a) == (23, 97):
            # the wird begins at "Rabbi a'udhu"; started there, ra' carries no shadda
            pre = "وَقُل رَّبِّ"
            assert txt.startswith(pre)
            txt = "رَبِّ" + txt[len(pre):]
        parts.append(txt)
    body = " ".join(parts)
    return f"{KF_BISM}<br>{body}" if bism else body

def quran_tl(key, spec, bism):
    out = []
    if bism:
        out.append(qe(key, 1, 1) + "<br>")
    for s, a, b in spec:
        out.append(" ".join(f"<sup>{i}</sup>{qe(key, s, i)}" for i in range(a, b + 1)))
    return " ".join(out)

def table_tl(table, bism_line, spec, bism):
    out = [bism_line + "<br>"] if bism else []
    for s_, a, b in spec:
        out.append(" ".join(f"<sup>{i}</sup>{table[(s_, i)]}" for i in range(a, b + 1)))
    return " ".join(out)

def dag_tl(spec, bism):
    return table_tl(DAG, DAG_BISM, spec, bism)

for it in ITEMS:
    it["kind"] = "d"
    if it["quran"] == "9:129-part":
        h = kf(9, 129)
        it["ar"] = h[h.index("حَسۡبِيَ"):]
        it["kind"] = "k"
        it["quran"] = None
    elif it["quran"]:
        it["ar"] = quran_ar(it["quran"], it["bism"])
        it["kind"] = "k"
        it["en"] = quran_tl("english_rwwad", it["quran"], it["bism"])
        it["de"] = quran_tl("german_bubenheim", it["quran"], it["bism"])
        it["dag"] = dag_tl(it["quran"], it["bism"])
        it["hau"] = table_tl(HAU, HAU_BISM, it["quran"], it["bism"])

# ---------------------------------------------------------------- colour coding
ZWJ = "‍"
SUN = set("تثدذرزسشصضطظلن")
RIGHT_ONLY = set("اأإآٱدذرزوؤةء")
AR_WORD = re.compile(r"[ء-ٰٟ-ۜ۟-ۭ]+")

def _base(w):
    return "".join("ا" if c == "ٱ" else c for c in w if unicodedata.category(c) != "Mn")

def _clusters(w):
    cl = []
    for c in w:
        if cl and unicodedata.category(c) == "Mn":
            cl[-1] += c
        else:
            cl.append(c)
    return cl

def _color_word(m, uthmani):
    w = m.group(0)
    b = _base(w)
    if "لله" in b:
        return f'<span class="c-allah">{w}</span>'
    if "محمد" in b:
        return f'<span class="c-nabi">{w}</span>'
    cl = _clusters(w)
    silent = [False] * len(cl)
    for i, c in enumerate(cl):
        if c == "ل" and i + 1 < len(cl) and cl[i + 1][0] in SUN and "ّ" in cl[i + 1]:
            silent[i] = True            # lam al-shamsiyya
        if uthmani and "ْ" in c:
            silent[i] = True            # Madinah mushaf: round zero = never pronounced
    if not any(silent):
        return w
    out, i = [], 0
    while i < len(cl):
        j = i
        while j < len(cl) and silent[j] == silent[i]:
            j += 1
        seg = "".join(cl[i:j])
        lead = ZWJ if i > 0 and cl[i - 1][0] not in RIGHT_ONLY else ""
        trail = ZWJ if j < len(cl) and cl[j - 1][0] not in RIGHT_ONLY else ""
        seg = f"{lead}{seg}{trail}"
        out.append(f'<span class="c-silent">{seg}</span>' if silent[i] else seg)
        i = j
    return "".join(out)

def color_ar(s, uthmani):
    return AR_WORD.sub(lambda m: _color_word(m, uthmani), s)

def _outside_tags(s, rx, cls):
    parts = re.split(r"(<[^>]+>)", s)
    return "".join(p if p.startswith("<") else rx.sub(lambda m: f'<span class="{cls}">{m.group(0)}</span>', p) for p in parts)

TR_ALLAH = re.compile(r"[\wʾʿ\-]*llāh[\wʾʿ]*")
TR_NABI = re.compile(r"Muḥammad\w*")
EN_ALLAH = re.compile(r"\b(?:Allahs?|Naawuni)\b")
EN_NABI = re.compile(r"\bMuhammads?\b")

def marks(s, cls):
    return s.replace("⟦", f'<span class="{cls}">').replace("⟧", "</span>")

def fmt_ar(s, uthmani, cls="chg"):
    return marks(color_ar(s, uthmani), cls)

def fmt_tr(s, cls="chg"):
    return marks(_outside_tags(_outside_tags(s, TR_ALLAH, "c-allah"), TR_NABI, "c-nabi"), cls)

def fmt_en(s, cls="chg"):
    return marks(_outside_tags(_outside_tags(s, EN_ALLAH, "c-allah"), EN_NABI, "c-nabi"), cls)


import base64 as _b64
def _svg(svg):
    return "data:image/svg+xml;base64," + _b64.b64encode(svg.encode()).decode()
SUN = _svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g stroke="#d9920f" stroke-width="2.2" stroke-linecap="round"><line x1="12" y1="1.6" x2="12" y2="4.4"/><line x1="12" y1="19.6" x2="12" y2="22.4"/><line x1="1.6" y1="12" x2="4.4" y2="12"/><line x1="19.6" y1="12" x2="22.4" y2="12"/><line x1="4.6" y1="4.6" x2="6.6" y2="6.6"/><line x1="17.4" y1="17.4" x2="19.4" y2="19.4"/><line x1="4.6" y1="19.4" x2="6.6" y2="17.4"/><line x1="17.4" y1="6.6" x2="19.4" y2="4.6"/></g><circle cx="12" cy="12" r="5.2" fill="#f2b51d" stroke="#d9920f" stroke-width="1.2"/></svg>')
MOON = _svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M15.5 3.2A9 9 0 1 0 20.8 16 7.2 7.2 0 0 1 15.5 3.2z" fill="#2b3a7a"/><path d="M19 4.2l.7 1.6 1.6.7-1.6.7-.7 1.6-.7-1.6-1.6-.7 1.6-.7z" fill="#2b3a7a"/></svg>')
REPEAT = _svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#fbf8f1" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12a8 8 0 1 1-2.6-5.9"/><path d="M20 3.5v4.8h-4.8"/></svg>')

def repeat_badge(count):
    n = count.rstrip("×").strip()
    return f'<span class="count"><img class="ic" src="{REPEAT}">Repeat {n} times</span>'
MORNING_TAG = f'<div class="tag tag-m"><img class="ic" src="{SUN}">Morning</div>'
EVENING_TAG = f'<div class="eve-h"><span class="tag-e"><img class="ic" src="{MOON}">Evening</span> say this instead</div>'

# ---------------------------------------------------------------- styles
FONTS = os.path.join(ROOT, "fonts", "Amiri-1.000")
CSS = f"""
@font-face {{ font-family: 'KFHafs'; src: url('file://{KF}/font/hafs.18.ttf'); }}
@font-face {{ font-family: 'AmiriR'; src: url('file://{FONTS}/Amiri-Regular.ttf'); }}
@font-face {{ font-family: 'AmiriR'; font-weight: bold; src: url('file://{FONTS}/Amiri-Bold.ttf'); }}
@page {{
  size: 72mm 128mm;
  margin: 6mm 5mm 9mm 5mm;
  background: #fbf8f1;
  @bottom-center {{ content: counter(page) " / " counter(pages); font: 7pt 'Inter', sans-serif; color: #8a8372; }}
}}
@page :first {{ @bottom-center {{ content: none; }} }}
:root {{ --allah: #b3262d; --nabi: #17784a; --silent: #ada38b; --gold: #7a5c14; --sun: #f7e1a1; --moon: #e3e7f6; --moonink: #2b3a7a; }}
html {{ background: #fbf8f1; }}
body {{ margin: 0; color: #1f1d19; font-family: 'Inter', 'DejaVu Sans', sans-serif; font-size: 8.6pt; line-height: 1.5; }}
a {{ color: inherit; text-decoration: none; }}
.c-allah {{ color: var(--allah); }}
.c-nabi {{ color: var(--nabi); }}
.c-silent {{ color: var(--silent); }}
.chg {{ background: var(--sun); border-radius: 1mm; }}
.chg.ev {{ background: #c9d1f0; }}

/* title page */
.titlepage {{ text-align: center; padding-top: 22mm; }}
.titlepage .ar {{ font-family: 'AmiriR', serif; font-size: 30pt; line-height: 1.6; direction: rtl; color: #3b2f12; text-align: center; }}
.titlepage h1 {{ font-size: 14pt; margin: 2mm 0 0; bookmark-level: none; }}
.titlepage .sub {{ margin: 2mm 0 0; font-size: 8pt; color: #6b6452; }}
.titlepage .rule {{ width: 18mm; border-top: 0.5mm solid #b9ad8a; margin: 6mm auto; }}
.titlepage .ed {{ font-size: 7.4pt; color: #8a8372; margin-top: 14mm; }}
.titlepage .cby {{ font-size: 6.8pt; letter-spacing: .06em; text-transform: uppercase; }}
.titlepage .cname {{ font-size: 9pt; color: #3b2f12; }}

/* page-level blocks */
.page {{ break-before: page; }}
h2.pg {{ font-size: 11pt; color: var(--gold); margin: 0 0 3mm; bookmark-level: 1; }}
.toc a {{ display: flex; align-items: baseline; padding: 1.4mm 0; border-bottom: 0.2mm solid #e7dfca; }}
.toc a .t {{ flex: 1; }}
.toc a .t small {{ display: block; color: #8a8372; font-size: 6.8pt; }}
.toc a .pg {{ color: var(--gold); font-weight: 700; padding-left: 2mm; }}
.toc a.sub {{ padding: 0.6mm 0 0.6mm 4mm; border: none; font-size: 7.6pt; color: #4a4638; }}
.toc .n {{ color: var(--gold); font-weight: 700; width: 5mm; flex: none; }}
p {{ margin: 0 0 2.2mm; }}
.about p {{ font-size: 8.2pt; }}
.howto {{ margin: 0; padding: 0; list-style: none; }}
.howto li {{ display: flex; gap: 2mm; margin: 0 0 1.3mm; font-size: 7.4pt; line-height: 1.38; }}
.howto .sw {{ flex: none; width: 3mm; height: 3mm; border-radius: 50%; margin-top: 0.7mm; }}
.howto .pill {{ flex: none; background: var(--gold); color: #fbf8f1; font-size: 6.4pt; font-weight: 700; padding: 0 1.4mm; border-radius: 2mm; height: 3.6mm; line-height: 3.6mm; margin-top: 0.2mm; }}
.howto .blk {{ flex: none; width: 3mm; height: 3mm; border-radius: 0.6mm; margin-top: 0.7mm; }}
.saw {{ font-family: 'AmiriR', serif; font-size: 1.25em; line-height: 1; }}
.lg-ar {{ display: inline-block; unicode-bidi: isolate; direction: rtl; font-family: 'KFHafs', serif; font-size: 14pt; line-height: 1; }}
h3.box {{ font-size: 8.4pt; color: var(--gold); margin: 0 0 2mm; }}

/* sections and items */
.sec {{ break-before: page; }}
.sec-h {{ background: #f1ead6; border-radius: 2mm; padding: 2.5mm 3mm; margin: 0 0 4mm; }}
.sec-h h2 {{ font-size: 10.5pt; margin: 0; color: #3b2f12; bookmark-level: 1; }}
.sec-h .sn {{ color: var(--gold); font-weight: 700; font-size: 7.2pt; letter-spacing: .06em; text-transform: uppercase; }}
.sec-h .sd {{ font-size: 7.4pt; color: #6b6452; margin-top: 0.6mm; }}
h3.qh {{ font-size: 8.4pt; font-weight: 700; color: var(--gold); margin: 0 0 1.4mm; bookmark-level: 2; break-after: avoid; }}
.item {{ margin: 0 0 4.5mm; padding: 0 0 4mm; border-bottom: 0.25mm solid #e1d9c3; }}
.meta {{ display: flex; gap: 1.6mm; align-items: center; margin: 0 0 1.2mm; break-after: avoid; }}
.num {{ flex: none; width: 4.6mm; height: 4.6mm; border-radius: 50%; border: 0.25mm solid #c9c0aa; color: #8f8770; font-size: 6.2pt; font-weight: 500; text-align: center; line-height: 4.6mm; }}
.count {{ background: var(--gold); color: #fbf8f1; font-size: 7.2pt; font-weight: 700; padding: 0.5mm 2.4mm 0.5mm 1.6mm; border-radius: 3mm; }}
.ic {{ width: 3.2mm; height: 3.2mm; vertical-align: -0.7mm; margin-right: 1mm; }}
.ref {{ font-size: 7.2pt; color: #8a7a4a; }}
.tag {{ break-after: avoid; margin: 1.2mm 0 0.4mm; }}
.tag-m {{ display: table; background: var(--sun); color: #6b4d05; font-size: 7.6pt; font-weight: 700; padding: 0.6mm 2.6mm 0.6mm 1.6mm; border-radius: 3mm; }}
.tag-m .ic, .tag-e .ic {{ width: 4mm; height: 4mm; vertical-align: -1mm; }}
.tag-e {{ display: inline-block; background: #c9d1f0; color: var(--moonink); font-size: 7.6pt; font-weight: 700; padding: 0.6mm 2.6mm 0.6mm 1.6mm; border-radius: 3mm; margin-right: 1.2mm; }}
.ar {{ direction: rtl; text-align: right; font-size: 14.5pt; line-height: 2.1; color: #14110a; }}
.ar.k {{ font-family: 'KFHafs', serif; font-size: 16pt; line-height: 2.2; }}
.ar.d {{ font-family: 'AmiriR', serif; }}
.tr {{ font-style: italic; color: #3a352a; margin: 1.5mm 0 1.5mm; }}
.en {{ color: #4a4638; font-size: 8.2pt; }}
.tl {{ color: #4a4638; font-size: 8pt; margin: 0 0 1.4mm; }}
.lang {{ display: inline-block; font-size: 5.8pt; font-weight: 700; letter-spacing: .05em; color: #fbf8f1; background: #a39573; border-radius: 1mm; padding: 0 1mm; margin-right: 1.2mm; vertical-align: 0.3mm; font-style: normal; }}
sup {{ font-size: 6pt; color: #8a7a4a; font-style: normal; vertical-align: super; line-height: 0; }}
.eve {{ break-inside: avoid; background: var(--moon); border-radius: 2mm; padding: 1.5mm 3mm 2.5mm; margin-top: 3mm; }}
.eve-h {{ break-after: avoid; font-size: 7.2pt; font-weight: 600; color: var(--moonink); margin: 0.8mm 0 0.6mm; }}
.eve .tr, .eve .en {{ color: #2a2f45; }}
.end {{ text-align: center; font-size: 7.4pt; color: #7a7360; margin: 6mm 0 0; }}

/* sources */
.src p {{ font-size: 7.2pt; line-height: 1.45; margin: 0 0 1.8mm; }}
.src h3 {{ font-size: 7.8pt; color: var(--gold); margin: 3mm 0 1mm; }}
.src a {{ color: #5b4a1c; text-decoration: underline; }}
.lic {{ background: #f1ead6; border-radius: 2mm; padding: 2.2mm 3mm; }}
"""

# ---------------------------------------------------------------- pages
def title_page():
    return f'''<div class="titlepage">
  <div class="ar">الْوِرْدُ اللَّطِيفُ</div>
  <h1>Al-Wird al-Laṭīf</h1>
  <div class="sub">of Imām ʿAbd Allāh ibn ʿAlawī al-Ḥaddād</div>
  <div class="rule"></div>
  <div class="sub">Morning and evening litany<br>Arabic · transliteration · meaning</div>
  <div class="ed"><span class="cby">Compiled by</span><br><b class="cname">{COMPILER}</b><br><br>{EDITION}</div>
</div>'''

def contents_page(item_ranges, qheads):
    rows = ['<a href="#about"><span class="n"></span><span class="t">About this wird</span><span class="pg">@@PG@@</span></a>',
            '<a href="#howto"><span class="n"></span><span class="t">How to read this edition</span><span class="pg">@@PG@@</span></a>']
    for k, (sid, name, desc) in enumerate(SECTIONS, 1):
        a, b = item_ranges[sid]
        mark = f' <img class="ic" style="margin:0 0 0 1mm" src="{SUN}"><img class="ic" style="margin:0" src="{MOON}">' if sid == "s5" else ""
        rows.append(f'<a href="#{sid}"><span class="n">{k}</span><span class="t">{name}{mark}<small>Items {a}–{b} · {desc}</small></span><span class="pg">@@PG@@</span></a>')
        if sid == "s1":
            for qid, qname in qheads:
                rows.append(f'<a class="sub" href="#{qid}"><span class="t">{qname}</span><span class="pg">@@PG@@</span></a>')
    rows.append('<a href="#sources"><span class="n"></span><span class="t">Sources and licence</span><span class="pg">@@PG@@</span></a>')
    return f'<div class="page toc"><h2 class="pg">Contents</h2>{"".join(rows)}</div>'

def about_page():
    return '''<div class="page about" id="about">
<h2 class="pg">About this wird</h2>
<p><i>Al-Wird al-Laṭīf</i> was compiled by Imām ʿAbd Allāh ibn ʿAlawī al-Ḥaddād (1044–1132 AH / 1634–1720 CE) of Tarim, in Ḥaḍramawt, Yemen. Smallpox took his sight before he was five, yet he became one of the best-known scholars and spiritual teachers of his age. He also compiled the <i>Rātib al-Ḥaddād</i>.</p>
<p>The wird is made up of passages of the Qurʾān and of supplications that the Prophet ﷺ taught his community to say in the morning and the evening. It is read once each morning and once each evening.</p>
<p>The Arabic of the Qurʾānic passages follows the Madinah muṣḥaf printed by the King Fahd Complex. Everything else is fully vowelled.</p>
</div>'''

def howto_page():
    return '''<div class="page" id="howto">
<h3 class="box" style="bookmark-level:1;bookmark-label:'How to read this edition'">How to read this edition</h3>
<ul class="howto">
<li><span class="num">12</span><span>The small grey number is the line number, to help you find your place.</span></li>
<li><span>@@REPEAT@@</span></li>
<li style="display:block;margin-left:0">This gold badge says how many times to say the line. Lines without it are said once.</li>
<li><span class="sw" style="background:var(--allah)"></span><span><b class="c-allah">Allah</b> is red in the Arabic, the transliteration and the translations, so the word can be matched across all three.</span></li>
<li><span class="sw" style="background:var(--nabi)"></span><span>The Prophet’s name, <b class="c-nabi">Muhammad</b> ﷺ, is green.</span></li>
<li><span class="sw" style="background:var(--silent)"></span><span>Grey letters are written but <b>not pronounced</b>, e.g. <bdi class="lg-ar" dir="rtl">{EX}</bdi> is read <i>ash-shams</i>.</span></li>
<li style="display:block">@@MTAG@@<div style="margin-top:1mm">Words on a <span class="chg">yellow</span> background are said in the <b>morning</b>.</div></li>
<li style="display:block"><div class="eve-h" style="margin:0">@@ETAG@@</div><div style="margin-top:1mm">In the <b>evening</b>, read the blue box underneath instead. The changed words are marked in <span class="chg ev">blue</span>.</div></li>
<li><span class="pill">EN</span><span>Qurʾānic passages show translations in English, German (<span class="lang" style="margin:0">DE</span>), Hausa (<span class="lang" style="margin:0">HA</span>) and Dagbanli (<span class="lang" style="margin:0">DAG</span>). The duʿās show a simple English meaning.</span></li>
<li><span class="sw" style="background:var(--allah)"></span><span>In Dagbanli, <b class="c-allah">Naawuni</b> (Allah) is red too.</span></li>
</ul>
<p style="font-size:7pt;color:#6b6452;margin-top:2mm">Tap any line in the Contents to jump to it. Your PDF app’s bookmarks list the sections too.</p>
</div>'''.replace('{EX}', color_ar('ٱلشَّمۡسِ', True)).replace('@@REPEAT@@', repeat_badge('3×')).replace('@@MTAG@@', MORNING_TAG.replace('class="tag tag-m"', 'class="tag-m"')).replace('@@ETAG@@', f'<span class="tag-e"><img class="ic" src="{MOON}">Evening</span>')

def sources_page():
    en_name, en_v, en_url = QE_META["english_rwwad"]
    de_name, de_v, de_url = QE_META["german_bubenheim"]
    en_name = en_name.replace("English Translation - ", "")
    de_name = de_name.replace("German Translation - ", "")
    return f'''<div class="page src" id="sources">
<h2 class="pg">Sources and licence</h2>
<h3>Qurʾānic Arabic</h3>
<p>Text: King Fahd Glorious Qurʾān Printing Complex (KFGQPC), Uthmanic Ḥafṣ data v18 (<a href="https://qurancomplex.gov.sa/en/techquran/dev/">qurancomplex.gov.sa</a>), as mirrored at <a href="https://github.com/thetruetruth/quran-data-kfgqpc">github.com/thetruetruth/quran-data-kfgqpc</a>. Used verbatim; in 23:97 the wird begins at <i>Rabbī</i>.</p>
<p>Font: KFGQPC Uthmanic Script HAFS. © 2010 KFGQPC; free to use, copy and distribute; may not be sold or modified.</p>
<h3>Qurʾān translations</h3>
<p>English: {en_name}, v{en_v} — <a href="{en_url}">QuranEnc.com</a>.<br>German: {de_name} (with Nadeem Elyas), v{de_v} — <a href="{de_url}">QuranEnc.com</a>.<br>Reproduced verbatim under QuranEnc’s terms (credit the source, do not change the text). Footnotes are not reproduced; see the source for them and for updates.</p>
<p>Hausa: translation by Abubakar Mahmoud Gumi, as printed by the King Fahd Complex (also on <a href="https://quranenc.com/ha/browse/hausa_gummi">QuranEnc.com</a>). Transcribed from the printed edition (pp. 525, 527, 615, 679, 843–844, 959–960), keeping its spelling; footnote markers omitted, words split across lines rejoined.</p>
<p>Dagbanli: translation by Muḥammad Bābā Gbetobu, as printed by the King Fahd Complex (also on <a href="https://quranenc.com/en/browse/dagbani_ghatubo">QuranEnc.com</a>). Transcribed from the printed edition (<a href="https://archive.org/details/dagbani-quran-translation-the-holy-quran-king-abdullah-bin-abdal-aziz-al-saud">archive.org scan</a>, pp. 564–567, 665–666, 741, 929–930, 1060–1062); words split across lines in print are rejoined.</p>
<h3>Duʿās and evening wording</h3>
<p>Arabic and transliteration based on a circulating edition of the wird, fully vowelled and corrected for this edition. English meanings of the duʿās are new translations made for this edition.</p>
<p>Evening wording as given in <i>The Graceful and Benevolent Litany</i> (Ashnataar Publications, 2012, ed. Ghoesain Mohamed) and on <a href="https://salawat.com/wird-al-latif/">salawat.com</a>.</p>
<h3>Other</h3>
<p>Dates of Imām al-Ḥaddād: <a href="https://en.wikipedia.org/wiki/%27Abdullah_ibn_%27Alawi_al-Haddad">Wikipedia</a>. Description of the wird: <a href="https://seekersguidance.org/articles/prophetic-guidance/the-complete-wird-latif-of-imam-al-haddad-with-transliteration/">SeekersGuidance</a>.</p>
<p>Other fonts: Amiri and Inter, both under the SIL Open Font License 1.1.</p>
<h3>Compiler</h3>
<p>This phone edition was compiled by {COMPILER}.</p>
<div class="lic"><p style="margin:0"><b>Licence.</b> The new material in this edition — the duʿā translations, revised transliteration, notes and layout — is released by {COMPILER} under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. The Qurʾān translations remain under QuranEnc’s terms and the Qurʾān font under the KFGQPC licence. {EDITION}.</p></div>
</div>'''

def render():
    out = [f'<html lang="en"><head><meta charset="utf-8"><title>Al-Wird al-Laṭīf</title><meta name="author" content="{COMPILER} (compiler)"><meta name="description" content="Phone edition of al-Wird al-Laṭīf of Imām al-Ḥaddād — {EDITION}"><style>{CSS}</style></head><body>']
    out.append(title_page())
    # numbering + section ranges
    item_ranges, qheads = {}, []
    for n, it in enumerate(ITEMS, 1):
        it["n"] = n
        a, b = item_ranges.get(it["sec"], (n, n))
        item_ranges[it["sec"]] = (min(a, n), max(b, n))
        if it["sec"] == "s1" and it["heading"] and it["quran"]:
            qheads.append((f"i{n}", it["heading"]))
    out.append(contents_page(item_ranges, qheads))
    out.append(about_page())
    out.append(howto_page())
    for k, (sid, name, desc) in enumerate(SECTIONS, 1):
        out.append(f'<div class="sec" id="{sid}"><div class="sec-h"><div class="sn">Section {k}</div><h2>{name}</h2><div class="sd">{desc}</div></div>')
        for it in [x for x in ITEMS if x["sec"] == sid]:
            uth = it["kind"] == "k"
            out.append(f'<div class="item" id="i{it["n"]}">')
            if it["heading"]:
                tag = "h3 class=\"qh\"" if it["quran"] else "h3 class=\"qh\" style=\"bookmark-level:none\""
                out.append(f'<{tag}>{it["heading"]}</h3>')
            meta = f'<span class="num">{it["n"]}</span>'
            if it["count"]:
                meta += repeat_badge(it["count"])
            if it["ref"]:
                meta += f'<span class="ref">{it["ref"]}</span>'
            out.append(f'<div class="meta">{meta}</div>')
            if it["ev"]:
                out.append(MORNING_TAG)
            out.append(f'<div class="ar {it["kind"]}" lang="ar" dir="rtl">{fmt_ar(it["ar"], uth)}</div>')
            out.append(f'<div class="tr">{fmt_tr(it["tr"])}</div>')
            if it["quran"]:
                out.append(f'<div class="tl"><span class="lang">EN</span>{fmt_en(it["en"])}</div>')
                out.append(f'<div class="tl" lang="de"><span class="lang">DE</span>{fmt_en(it["de"])}</div>')
                out.append(f'<div class="tl" lang="ha"><span class="lang">HA</span>{fmt_en(it["hau"])}</div>')
                out.append(f'<div class="tl" lang="dag"><span class="lang">DAG</span>{fmt_en(it["dag"])}</div>')
            else:
                out.append(f'<div class="en">{fmt_en(it["en"])}</div>')
            if it["ev"]:
                ear, etr, een = it["ev"]
                out.append(f'<div class="eve">{EVENING_TAG}'
                           f'<div class="ar d" lang="ar" dir="rtl">{fmt_ar(ear, False, "chg ev")}</div>'
                           f'<div class="tr">{fmt_tr(etr, "chg ev")}</div>'
                           f'<div class="en">{fmt_en(een, "chg ev")}</div></div>')
            out.append('</div>')
        out.append('</div>')
    out.append('<div class="end">End of the wird</div>')
    out.append(sources_page())
    out.append('</body></html>')
    return "\n".join(out)

if __name__ == "__main__":
    for d in ("build", "dist"):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    h = render()
    body_start = h.index("<body>")
    h = h[:body_start] + h[body_start:].replace("ﷺ", '<span class="saw">ﷺ</span>')
    open(os.path.join(ROOT, "build", "wird.html"), "w", encoding="utf-8").write(h)
    def pages_for(html_str):
        doc = HTML(string=html_str, base_url=os.path.join(ROOT, "build") + "/").render()
        where = {}
        for i, pg in enumerate(doc.pages, 1):
            for a in pg.anchors:
                where.setdefault(a, i)
        return doc, where
    def fill(html_str, where):
        def rep(m):
            href = m.group(1)
            return m.group(0).replace("@@PG@@", str(where.get(href, "")))
        return re.sub(r'<a [^>]*href="#([^"]+)".*?</a>', rep, html_str, flags=re.S)
    _, where = pages_for(h.replace("@@PG@@", "00"))
    final = fill(h, where)
    doc, where2 = pages_for(final)
    assert where == where2, "page numbers shifted"
    open(os.path.join(ROOT, "build", "wird.html"), "w", encoding="utf-8").write(final)
    doc.write_pdf(os.path.join(ROOT, "dist", "al-Wird-al-Latif.pdf"))
    print("ok", len(ITEMS), "items")
