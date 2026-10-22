# -*- coding: utf-8 -*-
"""Prototip HTML'lerindeki gömülü JavaScript'in sözdizimi kontrolü.

Tek dosyalık prototipler (saha demosu, Blok 8, yönetici paneli) binlerce satır
JS taşıyor; bir virgül hatası sayfayı sessizce boş bırakır. Bu betik <script>
bloklarını çıkarıp `node --check` ile doğrular ve hatanın HTML dosyasındaki
gerçek satır numarasını yazar.

    python js_kontrol.py            → tüm prototipleri kontrol eder
    python js_kontrol.py a.html b.html
Node yoksa kontrol atlanır (çıkış 0) — commit'i kilitlemez.
"""
import glob
import io
import os
import re
import subprocess
import sys
import tempfile

# Konsol cp1254 olabilir: bulgu satirlarindaki "→" gibi karakterler
# UnicodeEncodeError atmasin (hata yollari tam bu satirlardan gecer).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


KOK = os.path.dirname(os.path.abspath(__file__))
VARSAYILAN = ["docs/05-tasarim/05-prototip/*.html",      # prototipler: binlerce satir JS
              "docs/05-tasarim/07-brosur/talimatname-*.html",  # brosur/tanitim/foy (sayfa surumlerinde kucuk script)
              "index.html"]                               # urun dosyasi: arama ve filtre
BLOK = re.compile(r"<script(?P<oz>[^>]*)>(?P<kod>.*?)</script>", re.S | re.I)


def node_var():
    for ad in ("node", "node.exe"):
        try:
            subprocess.run([ad, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
            return ad
        except Exception:
            continue
    return None


def dosyalar(argv):
    desenler = argv or VARSAYILAN
    out = []
    for d in desenler:
        yol = d if os.path.isabs(d) else os.path.join(KOK, d.replace("/", os.sep))
        out += sorted(glob.glob(yol))
    return [y for y in out if y.lower().endswith((".html", ".htm"))]


def kontrol(yol, node):
    """Dosyadaki her gömülü script bloğunu doğrular → hata listesi."""
    metin = io.open(yol, encoding="utf-8").read()
    hatalar = []
    for i, m in enumerate(BLOK.finditer(metin)):
        oz = m.group("oz")
        if "src=" in oz:
            continue                                   # dış dosya; ayrı yüklenir
        tur = re.search(r'type\s*=\s*["\']([^"\']+)', oz)
        if tur and not re.search(r"javascript|module|ecmascript", tur.group(1), re.I):
            continue                                   # application/json, text/template… JS değil
        kod = m.group("kod")
        if not kod.strip():
            continue
        baslangic_satiri = metin[:m.start("kod")].count("\n") + 1
        gecici = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8")
        gecici.write(kod)
        gecici.close()
        try:
            p = subprocess.run([node, "--check", gecici.name], capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=90)   # node ciktisi UTF-8; cp1254 ile cozulemez
            if p.returncode != 0:
                ciktilar = (p.stderr or p.stdout or "").strip().split("\n")
                ozet = next((l for l in ciktilar if "Error" in l or "error" in l), ciktilar[0] if ciktilar else "sözdizimi hatası")
                ozet = ozet.strip()[:160]              # node bazen tüm satırı basar; rapor kısa kalsın
                satir = re.search(r":(\d+)\s*$", ciktilar[0]) if ciktilar else None
                yer = (" · HTML satırı ~%d" % (baslangic_satiri + int(satir.group(1)) - 1)) if satir else ""
                hatalar.append("%s · script #%d%s: %s" % (os.path.relpath(yol, KOK), i + 1, yer, ozet.strip()))
        finally:
            os.unlink(gecici.name)
    return hatalar


def main(argv):
    node = node_var()
    if not node:
        print("js kontrolü atlandı: node bulunamadı")
        return 0
    liste = dosyalar(argv)
    if not liste:
        print("js kontrolü: kontrol edilecek dosya yok")
        return 0
    tum = []
    for yol in liste:
        tum += kontrol(yol, node)
    if tum:
        for h in tum:
            print("  JS HATASI " + h)
        return 1
    print("js sözdizimi temiz (%d dosya)" % len(liste))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
