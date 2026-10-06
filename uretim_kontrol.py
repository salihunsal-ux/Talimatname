# -*- coding: utf-8 -*-
"""Üretilmiş belgeler, üreticileriyle aynı sürümden mi?

Broşür, tanıtım dosyası, özellik föyü, ilan ve ürün dosyası elle yazılmaz;
bir build_*.py üretir. Script değişip çıktı yeniden üretilmezse depoya bayat
HTML (ve PDF) girer — bu, sayfa taşması kadar sessiz bir hatadır.

Çözüm: her üretici, çıktısının içine kendi kaynak özetini damgalar
(`<!-- uretici: build_x.py@ab12cd34 -->`). Bu betik damgayı script'in güncel
özetiyle karşılaştırır.

    python uretim_kontrol.py          → durumu yazdırır
    python uretim_kontrol.py --kontrol → bayat çıktı varsa çıkış kodu 1
"""
import hashlib
import io
import os
import re
import sys

KOK = os.path.dirname(os.path.abspath(__file__))

# üretici → ürettiği HTML dosyaları
HARITA = {
    "docs/05-tasarim/07-brosur/build_brosur.py": [
        "docs/05-tasarim/07-brosur/talimatname-brosur.html"],
    "docs/05-tasarim/07-brosur/build_tanitim.py": [
        "docs/05-tasarim/07-brosur/talimatname-tanitim.html",
        "docs/05-tasarim/07-brosur/talimatname-tanitim-sayfa.html"],
    "docs/05-tasarim/07-brosur/build_ozellikler.py": [
        "docs/05-tasarim/07-brosur/talimatname-ozellikler.html",
        "docs/05-tasarim/07-brosur/talimatname-ozellikler-sayfa.html"],
    "docs/07-gelistirme/ilan/build_ilan.py": [
        "docs/07-gelistirme/ilan/serbest-gelistirici-ilani.html"],
}
DAMGA = re.compile(r"<!-- uretici: (?P<ad>[\w.\-]+)@(?P<ozet>[0-9a-f]{8}) -->")


def yol(p):
    return os.path.join(KOK, p.replace("/", os.sep))


def ozet(dosya):
    """Üretici script'in (ve bağımlı olduğu ortak modüllerin) kaynak özeti."""
    h = hashlib.sha1()
    for p in [dosya] + BAGIMLILIK.get(dosya, []):
        tam = yol(p)
        if os.path.exists(tam):
            h.update(io.open(tam, "rb").read())
    return h.hexdigest()[:8]


# özellik föyü broşür ve tanıtımın bileşenlerini kullanır: onlar değişince föy de bayatlar
BAGIMLILIK = {
    "docs/05-tasarim/07-brosur/build_ozellikler.py": [
        "docs/05-tasarim/07-brosur/build_brosur.py",
        "docs/05-tasarim/07-brosur/build_tanitim.py"],
}


def damgala(metin, ad, oz):
    """Çıktının başına damga koyar ya da varsa günceller."""
    yeni = "<!-- uretici: %s@%s -->" % (ad, oz)
    if DAMGA.search(metin):
        return DAMGA.sub(yeni, metin, count=1)
    return yeni + "\n" + metin


def tara():
    bulgular = []
    for uretici, ciktilar in HARITA.items():
        if not os.path.exists(yol(uretici)):
            bulgular.append((uretici, "üretici yok"))
            continue
        oz = ozet(uretici)
        ad = os.path.basename(uretici)
        for c in ciktilar:
            tam = yol(c)
            if not os.path.exists(tam):
                bulgular.append((c, "çıktı yok — %s çalıştırın" % ad))
                continue
            m = DAMGA.search(io.open(tam, encoding="utf-8").read())
            if not m:
                bulgular.append((c, "damga yok — %s çalıştırın" % ad))
            elif m.group("ozet") != oz:
                bulgular.append((c, "bayat (%s ≠ %s) — %s çalıştırın" % (m.group("ozet"), oz, ad)))
    return bulgular


if __name__ == "__main__":
    bulgular = tara()
    if bulgular:
        for dosya, neden in bulgular:
            print("  BAYAT ÇIKTI %s: %s" % (dosya, neden))
        sys.exit(1 if "--kontrol" in sys.argv else 0)
    print("üretilmiş belgeler güncel (%d çıktı)" % sum(len(v) for v in HARITA.values()))
