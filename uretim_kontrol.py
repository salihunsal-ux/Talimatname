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

# Konsol cp1254 olabilir: bulgu satirlarindaki "→" gibi karakterler
# UnicodeEncodeError atmasin (hata yollari tam bu satirlardan gecer).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


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

# üretici → ürettiği PDF'ler. PDF'e yorum gömülemediği için damga yan dosyada durur:
#   <pdf>.damga → "build_x.py@<ozet> · pdf <sha1-8> · <tarih>"
PDF_HARITA = {
    "docs/05-tasarim/07-brosur/build_brosur.py": ["docs/05-tasarim/07-brosur/talimatname-brosur.pdf"],
    "docs/05-tasarim/07-brosur/build_tanitim.py": ["docs/05-tasarim/07-brosur/talimatname-tanitim.pdf"],
    "docs/05-tasarim/07-brosur/build_ozellikler.py": ["docs/05-tasarim/07-brosur/talimatname-ozellikler.pdf"],
    "docs/07-gelistirme/ilan/build_ilan.py": ["docs/07-gelistirme/ilan/serbest-gelistirici-ilani.pdf"],
}
# Damgaya giren sayilar: yalnizca uretilen belgelerin METNINDE gecenler. Buraya yeni bir
# alan eklemek, o sayi degisince ilgili ciktilarin yeniden uretilmesini zorunlu kilar.
DAMGA_ALANLARI = ["fr", "tc", "brosur_sayfa", "tanitim_sayfa", "foy_sayfa"]
PDF_DAMGA = re.compile(r"^(?P<ad>[\w.\-]+)@(?P<ozet>[0-9a-f]{8}) · pdf (?P<pdf>[0-9a-f]{8})")


def dosya_ozeti(tam):
    return hashlib.sha1(io.open(tam, "rb").read()).hexdigest()[:8]


def pdf_damgala(pdf_yolu, uretici_adi, uretici_ozeti):
    """PDF üretildikten sonra yan damga dosyasını yazar; üretici bunu çağırır."""
    import datetime
    satir = "%s@%s · pdf %s · %s\n" % (uretici_adi, uretici_ozeti, dosya_ozeti(pdf_yolu),
                                        datetime.date.today().isoformat())
    io.open(pdf_yolu + ".damga", "w", encoding="utf-8", newline="").write(satir)
    return satir.strip()


def yol(p):
    return os.path.join(KOK, p.replace("/", os.sep))


def ozet(dosya):
    """Üretici script'in (ve bağımlı olduğu ortak modüllerin) kaynak özeti."""
    h = hashlib.sha1()
    for p in [dosya] + BAGIMLILIK.get(dosya, []):
        tam = yol(p)
        if os.path.exists(tam):
            h.update(io.open(tam, "rb").read())
    try:                                           # yalnızca ÜRETİLEN METİNDE geçen sayılar girdi olur
        sys.path.insert(0, KOK)
        import sayilar as SAY
        s = SAY.hepsi()
        h.update(repr([(k, s[k]) for k in DAMGA_ALANLARI if k in s]).encode("utf-8"))
    except Exception:
        pass
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

    for uretici, pdfler in PDF_HARITA.items():
        if not os.path.exists(yol(uretici)):
            continue
        oz = ozet(uretici)
        ad = os.path.basename(uretici)
        for pdf in pdfler:
            tam = yol(pdf)
            if not os.path.exists(tam):
                bulgular.append((pdf, "PDF yok — %s --pdf çalıştırın" % ad))
                continue
            dmg = tam + ".damga"
            if not os.path.exists(dmg):
                bulgular.append((pdf, "damga yok — %s --pdf çalıştırın" % ad))
                continue
            m = PDF_DAMGA.match(io.open(dmg, encoding="utf-8").read().strip())
            if not m:
                bulgular.append((pdf, "damga okunamadı — %s --pdf çalıştırın" % ad))
            elif m.group("ozet") != oz:
                bulgular.append((pdf, "bayat (%s ≠ %s) — %s --pdf çalıştırın" % (m.group("ozet"), oz, ad)))
            elif m.group("pdf") != dosya_ozeti(tam):
                bulgular.append((pdf, "PDF dosyası damgasıyla uyuşmuyor — %s --pdf çalıştırın" % ad))
    return bulgular


if __name__ == "__main__":
    bulgular = tara()
    if bulgular:
        for dosya, neden in bulgular:
            print("  BAYAT ÇIKTI %s: %s" % (dosya, neden))
        sys.exit(1 if "--kontrol" in sys.argv else 0)
    print("üretilmiş belgeler güncel (%d HTML + %d PDF)" % (sum(len(v) for v in HARITA.values()),
                                                          sum(len(v) for v in PDF_HARITA.values())))
