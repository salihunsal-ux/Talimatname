# -*- coding: utf-8 -*-
"""Belgelerdeki sayıların tek kaynağı.

Gereksinim, test, ekran, iş kuralı ve hikâye sayıları belgelerden sayılır;
broşür/tanıtım/föy sayfa sayıları üretilmiş HTML'den okunur. Üreticiler
(build_ilan, build_brosur, build_tanitim, build_index) bu modülü içe aktarır;
markdown dosyalarındaki elle yazılmış sayılar `python sayilar.py --guncelle`
ile yenilenir.

    python sayilar.py              → sayıları yazdırır
    python sayilar.py --kontrol    → markdown'daki bayat sayıları listeler (çıkış kodu 1)
    python sayilar.py --guncelle   → bayat sayıları düzeltir
"""
import io
import os
import re
import sys

# Konsol cp1254 olabilir: bulgu satirlarindaki "→" gibi karakterler
# UnicodeEncodeError atmasin (hata yollari tam bu satirlardan gecer).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


KOK = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(KOK, "docs")


def oku(*parca):
    yol = os.path.join(KOK, *parca)
    return io.open(yol, encoding="utf-8").read() if os.path.exists(yol) else ""


def surum_say(metin, onek):
    """'Sürüm' sütunlu tabloda id'li satırları sayar → (toplam, v1, v1.1)."""
    toplam = v1 = 0
    sutun = None
    satirlar = metin.split("\n")
    for i, l in enumerate(satirlar):
        if not l.startswith("|"):
            continue
        hucre = [c.strip() for c in l.strip().strip("|").split("|")]
        if i + 1 < len(satirlar) and re.match(r"^\|\s*-", satirlar[i + 1]):
            sutun = next((j for j, c in enumerate(hucre) if c.startswith("Sürüm")), None)
            continue
        if re.match(r"^%s-[A-Za-z0-9-]*\d" % onek, hucre[0]) and sutun is not None and sutun < len(hucre):
            toplam += 1
            v = hucre[sutun]
            if v.startswith("v1") and not v.startswith("v1.1"):
                v1 += 1
    return toplam, v1, toplam - v1


def sayfa_say(*parca):
    """Üretilmiş yazdırma HTML'indeki sayfa (sheet) sayısı."""
    return oku(*parca).count('class="sheet"')


def hepsi():
    fr_t, fr_v1, fr_v11 = surum_say(oku("docs", "04-gereksinimler", "01-fonksiyonel-gereksinimler.md"), "FR")
    tc_t, tc_v1, tc_v11 = surum_say(oku("docs", "06-test", "02-kabul-test-senaryolari.md"), "TC")
    scr_t, scr_v1, _ = surum_say(oku("docs", "05-tasarim", "01-ekran-envanteri-ve-navigasyon.md"), "SCR")
    br = len(re.findall(r"^- \*\*BR-\d+", oku("docs", "04-gereksinimler", "03-is-kurallari.md"), flags=re.M))
    st = len(set(re.findall(r"^\| (ST-\d{3})", oku("docs", "07-gelistirme", "03-backlog-ve-sprint-plani.md"), flags=re.M)))
    adr = len([x for x in os.listdir(os.path.join(KOK, "docs", "adr")) if re.match(r"^\d{4}-.*\.md$", x)])
    sk = oku("docs", "02-urun", "07-sablon-kutuphanesi.md")
    sablon = len(re.findall(r"^## (\d+)\. ", sk, flags=re.M))
    sablon_madde = len(re.findall(r"^\| \d+ \| .*? \| .*? \|", sk, flags=re.M))
    return {
        "fr": fr_t, "fr_v1": fr_v1, "fr_v11": fr_v11,
        "tc": tc_t, "tc_v1": tc_v1, "tc_v11": tc_v11,
        "scr": scr_t, "scr_v1": scr_v1, "br": br, "st": st, "adr": adr,
        "sablon": sablon, "sablon_madde": sablon_madde,
        "brosur_sayfa": sayfa_say("docs", "05-tasarim", "07-brosur", "talimatname-brosur.html") or 2,
        "tanitim_sayfa": sayfa_say("docs", "05-tasarim", "07-brosur", "talimatname-tanitim.html") or 8,
        "foy_sayfa": sayfa_say("docs", "05-tasarim", "07-brosur", "talimatname-ozellikler.html") or 10,
    }


# ---------------------------------------------------------------- markdown'daki elle yazılmış sayılar
def _kurallar(s):
    """(dosya, desen, yeni metin) üçlüleri — desen tek grup yakalar, grup değiştirilir."""
    foy_taslak = s["foy_sayfa"] - 4          # ilk dört sayfa bugünkü sürüm
    return [
        ("docs/07-gelistirme/00-kodlama-hazirlik-indeksi.md",
         r"- \[x\] (\d+ fonksiyonel gereksinim \(\d+ v1, \d+ v1\.1\))",
         "%d fonksiyonel gereksinim (%d v1, %d v1.1)" % (s["fr"], s["fr_v1"], s["fr_v11"])),
        ("docs/07-gelistirme/00-kodlama-hazirlik-indeksi.md",
         r"- \[x\] (\d+ kabul testi \(\d+ v1, \d+ v1\.1\))",
         "%d kabul testi (%d v1, %d v1.1)" % (s["tc"], s["tc_v1"], s["tc_v11"])),
        ("docs/06-test/02-kabul-test-senaryolari.md",
         r"^(\d+) kabul testi; her biri", str(s["tc"])),
        ("docs/07-gelistirme/07-serbest-gelistirici-secimi.md",
         r"gereksinimler \((\d+) FR\)", str(s["fr"])),
        ("docs/07-gelistirme/07-serbest-gelistirici-secimi.md",
         r"ekranlar, (\d+) kabul testi", str(s["tc"])),
        ("docs/07-gelistirme/07-serbest-gelistirici-secimi.md",
         r"anlatan (\d+) sayfalık özellik föyü", str(s["foy_sayfa"])),
        ("docs/05-tasarim/07-brosur/README.md",
         r"(\d+) sayfalık broşür", str(s["brosur_sayfa"])),
        ("docs/05-tasarim/07-brosur/README.md",
         r"(\d+) sayfalık tanıtım dosyası", str(s["tanitim_sayfa"])),
        ("docs/05-tasarim/07-brosur/README.md",
         r"(\d+) sayfalık özellik föyü", str(s["foy_sayfa"])),
        ("docs/06-test/01-test-stratejisi.md",
         r"v1 etiketli (\d+) kabul testi", str(s["tc_v1"])),
        ("docs/07-gelistirme/03-backlog-ve-sprint-plani.md",
         r"tamamı; (\d+) v1 kabul testi", str(s["tc_v1"])),
        ("docs/07-gelistirme/03-backlog-ve-sprint-plani.md",
         r"v1 kabul testleri \((\d+)\)", str(s["tc_v1"])),
        ("docs/07-gelistirme/05-sprint0-ve-teknik-spike.md",
         r"\| (\d+) v1 kabul testi", str(s["tc_v1"])),
        # --- sablon kutuphanesi sayisi (02-urun/07) ---
        ("docs/02-urun/07-sablon-kutuphanesi.md", r"v1'in (\d+) şablonu", str(s["sablon"])),
        ("docs/02-urun/07-sablon-kutuphanesi.md", r"v1'de \*\*(\d+) hazır şablon\*\*", str(s["sablon"])),
        ("docs/02-urun/06-v1-cekirdek-kapsam.md", r"\| Kütüphane \| (\d+) şablon:", str(s["sablon"])),
        ("docs/02-urun/06-v1-cekirdek-kapsam.md", r"Kütüphane \| (\d+) şablon, kopyala", str(s["sablon"])),
        ("docs/02-urun/04-yetenek-haritasi.md", r"puan; (\d+) şablon", str(s["sablon"])),
        ("docs/02-urun/04-yetenek-haritasi.md", r"\(boş\); (\d+) şablon içeriği", str(s["sablon"])),
        ("docs/02-urun/08-madde-kutuphanesi.md", r"\(bugünkü (\d+) şablon\)", str(s["sablon"])),
        ("docs/02-urun/08-madde-kutuphanesi.md", r"kafe paketi: (\d+) şablon", str(s["sablon"])),
        ("docs/02-urun/08-madde-kutuphanesi.md", r"şablon, (\d+) madde, planlar", str(s["sablon_madde"])),
        ("docs/02-urun/08-madde-kutuphanesi.md", r"\(boş\); (\d+) şablon içeriği", str(s["sablon"])),
        ("docs/03-analiz/03-usecase-detaylari.md", r"kütüphanedeki (\d+) şablondan", str(s["sablon"])),
        ("docs/04-gereksinimler/01-fonksiyonel-gereksinimler.md", r"Kütüphane \(v1\): (\d+) Türkçe", str(s["sablon"])),
        ("docs/06-test/06-demo-kapsam-denetimi.md", r"Kütüphane \(v1\): (\d+) Türkçe", str(s["sablon"])),
        ("docs/07-gelistirme/03-backlog-ve-sprint-plani.md", r"Basit şablon editörü, (\d+) şablon", str(s["sablon"])),
        ("docs/07-gelistirme/03-backlog-ve-sprint-plani.md", r"Hash zinciri, (\d+) şablon", str(s["sablon"])),
        ("docs/07-gelistirme/03-backlog-ve-sprint-plani.md", r"İçerik: (\d+) Türkçe", str(s["sablon"])),
        ("docs/07-gelistirme/00-kodlama-hazirlik-indeksi.md", r"\[x\] (\d+) şablon içeriği", str(s["sablon"])),
        ("docs/00-urun-merkezi.md", r"kütüphane \((\d+) şablon, kopyala", str(s["sablon"])),
        ("docs/01-strateji/dogrulama-sprinti/00-sprint-plani.md", r"şablon uyarlaması \((\d+) şablon\)", str(s["sablon"])),
        ("docs/adr/0010-madde-kutuphanesi-v1-1.md", r"(\d+) şablon belgesi", str(s["sablon"])),
    ]


def tara(yaz=False):
    s = hepsi()
    bulgular = []
    for dosya, desen, yeni in _kurallar(s):
        yol = os.path.join(KOK, dosya.replace("/", os.sep))
        if not os.path.exists(yol):
            bulgular.append((dosya, "dosya yok", ""))
            continue
        metin = io.open(yol, encoding="utf-8").read()
        m = re.search(desen, metin, flags=re.M)
        if not m:
            bulgular.append((dosya, "desen bulunamadı: " + desen, ""))
            continue
        if m.group(1) != yeni:
            bulgular.append((dosya, m.group(1), yeni))
            if yaz:
                bas, son = m.span(1)
                io.open(yol, "w", encoding="utf-8", newline="").write(metin[:bas] + yeni + metin[son:])
    return s, bulgular


if __name__ == "__main__":
    guncelle = "--guncelle" in sys.argv
    s, bulgular = tara(yaz=guncelle)
    print("FR %d (v1 %d / v1.1 %d) · TC %d (v1 %d / v1.1 %d) · SCR %d · BR %d · ST %d · ADR %d" %
          (s["fr"], s["fr_v1"], s["fr_v11"], s["tc"], s["tc_v1"], s["tc_v11"], s["scr"], s["br"], s["st"], s["adr"]))
    print("Şablon: %d şablon · %d cevaplı madde" % (s["sablon"], s["sablon_madde"]))
    print("Sayfa: broşür %d · tanıtım %d · föy %d" % (s["brosur_sayfa"], s["tanitim_sayfa"], s["foy_sayfa"]))
    if bulgular:
        for dosya, eski, yeni in bulgular:
            print(("  düzeltildi " if guncelle else "  BAYAT ") + dosya + ": " + str(eski) + (" → " + yeni if yeni else ""))
        if not guncelle and "--kontrol" in sys.argv:
            sys.exit(1)
    else:
        print("markdown sayıları güncel.")
