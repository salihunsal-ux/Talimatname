# -*- coding: utf-8 -*-
"""Yazdırma belgelerinde sayfa taşması kontrolü.

Broşür, tanıtım dosyası ve özellik föyünde her yaprak sabit 1123 px (A4) ve
`overflow:hidden`; içerik taşarsa alttan **sessizce kırpılır** — PDF sayfa
sayısı değişmediği için fark edilmez. Bu betik ölçüm için bir kopya üretir:
yaprakların sabit yüksekliğini kaldırır, taşmayı görünür kılar ve Edge ile
PDF'e basar. İçerik A4'ü aşan yaprak iki PDF sayfası doğurur; sayfa sayısı
yaprak sayısını geçiyorsa taşma vardır.

    python tasma_kontrol.py              → üç belgeyi ölçer
    python tasma_kontrol.py --kontrol    → taşma varsa çıkış kodu 1
    python tasma_kontrol.py <dosya.html> → tek belge

Edge bulunamazsa kontrol atlanır (çıkış 0). Ölçüm ~8 sn/belge sürer; bu yüzden
pre-commit kancası bunu yalnızca ilgili belgeler commit'e girdiğinde çalıştırır.
"""
import io
import os
import re
import subprocess
import sys
import tempfile
import time

KOK = os.path.dirname(os.path.abspath(__file__))
BELGELER = [
    "docs/05-tasarim/07-brosur/talimatname-brosur.html",
    "docs/05-tasarim/07-brosur/talimatname-tanitim.html",
    "docs/05-tasarim/07-brosur/talimatname-ozellikler.html",
]
EDGE = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]

# ölçüm CSS'i: yaprağın sabit yüksekliği ve kırpması kalkar, taşma sayfaya düşer
OLCUM_CSS = """
<style id="tasma-olcum">
  .sheet { height: auto !important; min-height: 0 !important; overflow: visible !important; }
  .sheet > * { height: auto !important; min-height: 0 !important; overflow: visible !important; }
  @media print { .sheet + .sheet { break-before: page; } @page { size: A4; margin: 0; } }
</style>
"""


def edge_yolu():
    return next((x for x in EDGE if os.path.exists(x)), None)


def pdf_sayfa(yol):
    d = io.open(yol, "rb").read()
    return len(re.findall(rb"/Type\s*/Page[^s]", d))


def olc(html_yolu, edge):
    """(yaprak sayısı, ölçüm PDF'inin sayfa sayısı) döner."""
    metin = io.open(html_yolu, encoding="utf-8").read()
    yaprak = metin.count('class="sheet"')
    if not yaprak:
        return 0, 0
    olcum = metin.replace("</body>", OLCUM_CSS + "</body>") if "</body>" in metin else metin + OLCUM_CSS
    gecici_html = os.path.join(os.path.dirname(html_yolu), "_tasma_olcum.html")   # yanında: yazı tipleri aynı
    io.open(gecici_html, "w", encoding="utf-8").write(olcum)
    pdf = os.path.join(tempfile.gettempdir(), "tasma_%d.pdf" % os.getpid())
    if os.path.exists(pdf):
        os.remove(pdf)
    prof = tempfile.mkdtemp(prefix="tasma-")
    try:
        subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-first-run", "--user-data-dir=" + prof,
                        "--no-pdf-header-footer", "--print-to-pdf=" + pdf, "--virtual-time-budget=9000",
                        "file:///" + gecici_html.replace(os.sep, "/")],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=240)
        for _ in range(120):
            if os.path.exists(pdf) and os.path.getsize(pdf) > 5000:
                break
            time.sleep(0.5)
        return yaprak, (pdf_sayfa(pdf) if os.path.exists(pdf) else -1)
    finally:
        for p in (gecici_html, pdf):
            if os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass


def main(argv):
    edge = edge_yolu()
    if not edge:
        print("taşma kontrolü atlandı: Edge bulunamadı")
        return 0
    hedefler = [a for a in argv if not a.startswith("--")] or BELGELER
    tasan = []
    for h in hedefler:
        yol = h if os.path.isabs(h) else os.path.join(KOK, h.replace("/", os.sep))
        if not os.path.exists(yol):
            print("  dosya yok:", h)
            continue
        yaprak, sayfa = olc(yol, edge)
        ad = os.path.relpath(yol, KOK)
        if sayfa < 0:
            print("  ÖLÇÜLEMEDİ %s (Edge PDF üretmedi)" % ad)
            continue
        if sayfa > yaprak:
            tasan.append(ad)
            print("  TAŞMA %s: %d yaprak → ölçümde %d sayfa (%d yaprak A4'ü aşıyor)" % (ad, yaprak, sayfa, sayfa - yaprak))
        else:
            print("  tamam %s: %d yaprak, taşma yok" % (ad, yaprak))
    if tasan:
        print("\nTaşan yaprakta içerik alttan kırpılır; ilgili build_*.py içinde kısaltın ya da ölçek düşürün.")
        return 1 if "--kontrol" in argv else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
