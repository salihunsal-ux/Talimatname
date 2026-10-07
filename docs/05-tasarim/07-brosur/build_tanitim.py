# -*- coding: utf-8 -*-
"""Talimatname tanıtım dosyası — 8 sayfalık satış/anlatım broşürü (A4) + açıklamalı ekran tasarımları.
Tek başına ürün tanıtımı yapabilecek belge: konumlanma, maliyet, akış, ekranlar, kanıt, karşılaştırma,
itirazlar, pilot ve sonraki adım. 2 sayfalık özet broşür ayrı (build_brosur.py).
Üretir: tanitim/*.dc.html (sayfalar + ekranlar), canvas.json, talimatname-tanitim.html (+ --pdf),
talimatname-tanitim-sayfa.html (yayın sürümü)."""
import os, sys, subprocess, tempfile, time, json
import build_brosur as B

T, SANS, SERIF = B.T, B.SANS, B.SERIF
HERE = os.path.dirname(os.path.abspath(__file__))

def _kok():                                        # sayilarin tek kaynagi: depo kokundeki sayilar.py
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(d, "sayilar.py")) and os.path.dirname(d) != d:
        d = os.path.dirname(d)
    return d
sys.path.insert(0, _kok())
import sayilar as SAY
S = SAY.hepsi()

def _damga(metin):
    """Ciktiya uretici kaynak ozeti; bayat HTML'i uretim_kontrol.py yakalar."""
    import uretim_kontrol as UK
    ad = os.path.basename(os.path.abspath(__file__))
    for yol in UK.HARITA:
        if os.path.basename(yol) == ad:
            return UK.damgala(metin, ad, UK.ozet(yol))
    return metin
OUTDIR = os.path.join(HERE, "tanitim")
w, card, chip, box, phone, scaled = B.wordmark, B.card, B.chip, B.box, B.phone, B.scaled
INK_BAND = "#171c21"

def _pdf_damga(pdf_yolu):
    """PDF üretilince yan damga dosyası: bayat PDF'i uretim_kontrol.py yakalar."""
    import uretim_kontrol as UK
    ad = os.path.basename(os.path.abspath(__file__))
    kaynak = next((y for y in UK.PDF_HARITA if os.path.basename(y) == ad), None)
    if kaynak and os.path.exists(pdf_yolu):
        UK.pdf_damgala(pdf_yolu, ad, UK.ozet(kaynak))


# ---------------------------------------------------------------- tipografi (ortak bileşenler build_brosur'dan)
from build_brosur import h1, h2, h3, mp as p, label, pin, shot, legend, stat, table, quote, check, qa, INK_BAND

def page(inner, gap=18, bg=None):
    return ('<div style="box-sizing:border-box;width:794px;height:1123px;background:' + (bg or T["zemin"]) + ';font-family:' + SANS + ';color:' + T["ink"] +
            ';padding:38px 44px 26px;display:flex;flex-direction:column;gap:' + str(gap) + 'px;overflow:hidden">' + inner + '</div>')

def head(no, title):
    return ('<div style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid ' + T["cizgi"] + ';padding-bottom:9px">'
            + w(17) + '<div style="font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:' + T["sessiz"] + '">' + title + '</div></div>')

def foot(no, note=""):
    return ('<div style="margin-top:auto;display:flex;align-items:center;justify-content:space-between;border-top:1px solid ' + T["cizgi"] +
            ';padding-top:9px;font-size:10.5px;color:' + T["sessiz"] + '"><span>' + (note or "Ekranlar ürün tasarımındandır; veriler örnektir.") +
            '</span><span>Talimatname · ' + str(no) + ' / 8</span></div>')

# ---------------------------------------------------------------- ekranlar
def scr_unable():
    opt = lambda t, sel=False: ('<div style="padding:12px;border:1.5px solid ' + (T["marka"] if sel else T["cizgi"]) + ';border-radius:12px;font-size:15px;background:'
                                + (T["markaA"] if sel else T["yuzey"]) + '">' + t + '</div>')
    sheet = ('<div style="position:absolute;left:0;right:0;bottom:0;background:' + T["yuzey"] + ';border-radius:22px 22px 0 0;padding:18px 18px 22px;'
             'box-shadow:0 -14px 34px rgba(0,0,0,.2);display:flex;flex-direction:column;gap:9px">'
             '<div style="font-size:18px;font-weight:700;line-height:1.25">Yapılamadı — Zemin süpürüldü ve paspaslandı</div>'
             '<div style="padding:11px;border:1.5px dashed ' + T["cizgi"] + ';border-radius:12px;font-size:14.5px;color:' + T["ink2"] + '">İşareti kaldır (yeniden yapacağım)</div>'
             '<div style="font-size:13px;color:' + T["sessiz"] + '">Yapılamadıysa sebep seçin</div>'
             + opt("Malzeme yok", True) + opt("Ekipman arızalı") + opt("Zaman yetmedi") + opt("Yetkim yok") + opt("Diğer (not zorunlu)")
             + '<div style="border:1.5px solid ' + T["cizgi"] + ';border-radius:10px;padding:10px 12px;font-size:14px;color:' + T["ink2"] + '">Paspas deterjanı bitti</div>'
             + '<div style="display:flex;gap:10px"><div style="flex:1;min-height:48px;border-radius:12px;border:1.5px solid ' + T["cizgi"] +
             ';display:flex;align-items:center;justify-content:center;font-weight:600;color:' + T["sessiz"] + '">Vazgeç</div>'
             '<div style="flex:2;min-height:48px;border-radius:12px;background:' + T["kritik"] + ';color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600">Kaydet ve bildir</div></div></div>')
    return phone(B.phone_header("Emre T.", "Kadıköy · Cts 13 Eyl") + B.kiosk_list_body(dim=True) + sheet)

def scr_detail(W=1200, H=760):
    def mrow(no, title, ans, t, kind="ok", note=""):
        if kind == "crit":
            ic, col = box("crit"), T["kritik"]
        elif kind == "un":
            ic = ('<div style="width:26px;height:26px;border-radius:7px;flex:none;background:' + T["uyariA"] + ';border:2px solid ' + T["uyari"] +
                  ';display:flex;align-items:center;justify-content:center;color:' + T["uyari"] + ';font-weight:700;font-size:13px">–</div>')
            col = T["uyari"]
        else:
            ic, col = box("ok"), T["ink"]
        sub = ('<div style="font-size:11.5px;color:' + T["sessiz"] + ';margin-top:1px">' + note + '</div>') if note else ""
        return ('<div style="display:flex;gap:10px;align-items:center;padding:7px 0;border-bottom:1px solid ' + T["cizgi"] + '">' + ic +
                '<div style="width:20px;font-size:11.5px;color:' + T["sessiz"] + ';flex:none">' + str(no) + '</div>'
                '<div style="flex:1;min-width:0;font-size:13.5px;line-height:1.3">' + title + sub + '</div>'
                '<div style="font-size:13px;font-weight:600;color:' + col + ';white-space:nowrap">' + ans + '</div>'
                '<div style="width:44px;text-align:right;font-size:11.5px;color:' + T["sessiz"] + '">' + t + '</div></div>')
    maddeler = (mrow(2, "Kahve makinesi ve öğütücü temizlendi", "Yapıldı · fotoğraf", "23:06")
                + mrow(3, "Süt dolabı sıcaklığı", "3,1 °C", "23:09")
                + mrow(4, "Mutfak buzdolabı sıcaklığı", "6,0 °C · aralık dışı", "23:20", "crit", "not: kapı contası gevşek · 1 fotoğraf")
                + mrow(5, "Dondurucu sıcaklığı", "−19,5 °C", "23:21")
                + mrow(10, "Zemin süpürüldü ve paspaslandı", "Yapılamadı · malzeme yok", "23:30", "un", "not: paspas deterjanı bitti")
                + mrow(13, "Gaz vanası kapatıldı", "Evet", "23:37"))
    ph = lambda cap: ('<div><div style="aspect-ratio:4/3;border-radius:8px;background:repeating-linear-gradient(135deg,#dfe3e8 0 9px,#eef1f4 9px 18px);position:relative;overflow:hidden;border:1px solid ' + T["cizgi"] + '">'
                      '<div style="position:absolute;left:0;right:0;bottom:0;background:rgba(28,33,40,.84);color:#fff;font:9px/1.3 ui-monospace,Menlo,Consolas,monospace;padding:3px 5px">Kadıköy · 13.09 23:20 · Emre T.</div></div>'
                      '<div style="font-size:11px;color:' + T["sessiz"] + ';margin-top:3px">' + cap + '</div></div>')
    tl = lambda t, s, crit=False: ('<li style="display:grid;grid-template-columns:50px 1fr;gap:8px;padding:3px 0;border-bottom:1px dotted ' + T["cizgi"] + '">'
                                   '<span style="font:11.5px ui-monospace,Menlo,Consolas,monospace;color:' + T["ink2"] + '">' + t + '</span>'
                                   '<span style="font-size:12.5px;line-height:1.4' + (';color:' + T["kritik"] + ';font-weight:600' if crit else '') + '">' + s + '</span></li>')
    izi = (tl("22:00", "Pencere açıldı (sistem)") + tl("22:58", "Emre T. PIN ile giriş · şube tableti KDK-T1 · konum şube içinde")
           + tl("23:20", "Madde 4: 6,0 °C aralık dışı → kritik → aksiyon #418 · push Ayşe K. ✓ · push Murat D. ✓", True)
           + tl("23:30", "Madde 10 yapılamadı (malzeme yok) → aksiyon #419")
           + tl("23:41", "<b>Gönderildi</b> · başarısız (kritik madde) · kayıt kilitlendi")
           + tl("07:00", "Sabah özeti: Murat D., Selin Y.") + tl("08:05", "Aksiyon #418 kapatıldı — Ayşe K. · not + 1 fotoğraf"))
    lbl = lambda t: '<div style="font-size:10px;letter-spacing:.07em;text-transform:uppercase;color:' + T["sessiz"] + ';margin-bottom:5px;font-weight:700">' + t + '</div>'
    sol = ('<div style="display:flex;flex-direction:column;gap:10px;min-width:0">'
           + card(lbl("Maddeler · 15 maddeden 6’sı") + maddeler, "padding:12px 14px")
           + card(lbl("Kanıt fotoğrafları (4)") + '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px">'
                  + ph("2 · Kahve makinesi") + ph("4 · Buzdolabı") + ph("12 · Çöp alanı") + ph("15 · Kepenk") + '</div>', "padding:12px 14px") + '</div>')
    sag = ('<div style="display:flex;flex-direction:column;gap:10px;min-width:0">'
           + card('<b style="font-size:13.5px">Aksiyon #418 · kritik</b>'
                  '<div style="font-size:12.5px;color:' + T["ink2"] + ';margin-top:3px">Mutfak buzdolabı aralık dışı · Ayşe K. · vade 03:20</div>'
                  '<div style="font-size:12.5px;margin-top:6px;color:' + T["marka"] + ';font-weight:600">Kapalı 08:05 — “Servis geldi, conta değişti; ölçüm 3,4 °C.”</div>',
                  "padding:12px 14px;border-color:" + T["kritik"])
           + card(lbl("Olay izi — ekle-yalnız, hash zincirli") + '<ul style="list-style:none;margin:0;padding:0">' + izi + '</ul>', "padding:12px 14px")
           + '<div style="display:flex;gap:9px;align-items:center;font-size:11.5px;color:' + T["sessiz"] + '">'
           '<div style="padding:8px 13px;border-radius:9px;background:' + T["ink"] + ';color:#fff;font-weight:600;font-size:13px">PDF indir</div>'
           'Doğrulama kodu TN-K7F3A-9C2D</div></div>')
    return ('<div style="box-sizing:border-box;width:' + str(W) + 'px;height:' + str(H) + 'px;background:' + T["zemin"] + ';font-family:' + SANS + ';color:' + T["ink"] +
            ';padding:18px 22px;display:flex;flex-direction:column;gap:12px;overflow:hidden;border:1px solid ' + T["cizgi"] + ';border-radius:12px">'
            '<div style="display:flex;align-items:center;gap:12px">' + w(18) +
            '<div style="padding-left:14px;border-left:1px solid ' + T["cizgi"] + '">'
            '<div style="font-family:' + SERIF + ';font-size:19px;font-weight:700">Kadıköy · Kapanış · 13 Eylül</div>'
            '<div style="font-size:12.5px;color:' + T["ink2"] + '">Pencere 22:00–01:30 · gönderim 23:41 · Emre T. · şube tableti · puan %87 (bilgi)</div></div>'
            '<div style="margin-left:auto">' + chip("başarısız (kritik madde)", "crit") + '</div></div>'
            '<div style="display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:16px;min-height:0">' + sol + sag + '</div></div>')

def scr_wizard(W=1200, H=760):
    st = lambda n, t, s, state: ('<div style="border:1.5px solid ' + (T["marka"] if state != "todo" else T["cizgi"]) + ';background:' + (T["markaA"] if state == "on" else T["yuzey"]) +
                                 ';border-radius:10px;padding:10px 12px"><b style="font-size:13.5px">' + ("✓ " if state == "done" else "") + str(n) + ' · ' + t + '</b>'
                                 '<div style="font-size:11.5px;color:' + T["sessiz"] + '">' + s + '</div></div>')
    fld = lambda l, v: ('<label style="display:flex;flex-direction:column;gap:4px;font-size:11.5px;color:' + T["ink2"] + '">' + l +
                        '<div style="border:1.5px solid ' + T["cizgi"] + ';border-radius:8px;padding:8px 10px;background:' + T["yuzey"] + ';font-size:14px;color:' + T["ink"] + '">' + v +
                        ' <span style="color:' + T["sessiz"] + ';float:right">▾</span></div></label>')
    rows = [["Kadıköy", "23:00", "22:00 – 00:30 <span style='color:" + T["sessiz"] + "'>(+1 gün, aynı iş günü)</span>", "02:30"],
            ["Üsküdar", "23:00", "22:00 – 00:30", "02:30"], ["Ataşehir", "24:00", "23:00 – 01:30", "03:30"],
            ["Kartal", "22:00", "21:00 – 23:30", "01:30"], ["Bornova", "23:00", "22:00 – 00:30", "02:30"]]
    return ('<div style="box-sizing:border-box;width:' + str(W) + 'px;height:' + str(H) + 'px;background:' + T["zemin"] + ';font-family:' + SANS + ';color:' + T["ink"] +
            ';padding:18px 22px;display:flex;flex-direction:column;gap:12px;overflow:hidden;border:1px solid ' + T["cizgi"] + ';border-radius:12px">'
            '<div style="display:flex;align-items:center;gap:12px">' + w(18) +
            '<div style="padding-left:14px;border-left:1px solid ' + T["cizgi"] + ';font-family:' + SERIF + ';font-size:19px;font-weight:700">Kurulum sihirbazı</div>'
            '<div style="margin-left:auto;font-size:12.5px;color:' + T["ink2"] + '">Hesap: <b>Kahve Durağı</b> · 12 şube</div></div>'
            '<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px">'
            + st(1, "Marka ve şubeler", "12 şube · Excel", "done") + st(2, "Kapanış şablonu", "15 madde · 4 kritik", "done")
            + st(3, "Plan (saatler)", "pencere ve tolerans", "on") + st(4, "Personel ve cihazlar", "davet + kiosk", "todo") + '</div>'
            '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:16px;min-height:0">'
            '<div style="display:flex;flex-direction:column;gap:10px">'
            + card('<div style="font-family:' + SERIF + ';font-size:15px;font-weight:700;margin-bottom:8px">Tekrar ve pencere</div>'
                   '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">' + fld("Tekrar", "Her gün") + fld("Tolerans", "120 dk (sabit)")
                   + fld("Pencere başlangıcı", "Kapanıştan 60 dk önce") + fld("Pencere bitişi", "Kapanıştan 90 dk sonra") + '</div>', "padding:12px 14px")
            + card('<div style="font-family:' + SERIF + ';font-size:15px;font-weight:700;margin-bottom:6px">Atama</div>'
                   '<div style="font-size:13.5px;line-height:1.5"><b style="color:' + T["marka"] + '">●</b> Şubedeki herkes görür, biri tamamlasın (ilk açan alır)'
                   '<br><span style="color:' + T["sessiz"] + '">○ Rol: kapanışçı &nbsp; ○ Kişi</span></div>', "padding:12px 14px")
            + card('<div style="font-size:10px;letter-spacing:.07em;text-transform:uppercase;color:' + T["sessiz"] + ';margin-bottom:5px;font-weight:700">Hatırlatma ve eskalasyon · sabit</div>'
                   '<div style="font-size:12.5px;line-height:1.5;color:' + T["ink2"] + '">Pencere açılışında ve bitişe 30 dk kala push · kaçırılan liste → şube müdürüne anında, '
                   'bölge müdürüne 07:00 özeti · kritik madde → anında push, teslim olmazsa SMS · sessiz saat 23:00–07:00</div>',
                   "padding:12px 14px;background:" + T["yuzey2"]) + '</div>'
            '<div style="display:flex;flex-direction:column;gap:10px;min-width:0">'
            '<div style="font-size:12.5px;color:' + T["ink2"] + '">Şube başına hesaplanan pencere — çalışma saatinden türetildi; gece yarısını aşan pencere aynı iş gününe yazılır.</div>'
            + table(["Şube", "Kapanış", "Pencere", "Tolerans sonu"], rows, size=12)
            + '<div style="margin-top:auto;display:flex;gap:10px;justify-content:flex-end">'
            '<div style="padding:9px 14px;border-radius:9px;border:1.5px solid ' + T["cizgi"] + ';color:' + T["ink2"] + ';font-size:13.5px">← Geri</div>'
            '<div style="padding:9px 16px;border-radius:9px;background:' + T["marka"] + ';color:#fff;font-weight:600;font-size:13.5px">Devam: personel →</div></div></div></div></div>')

# ---------------------------------------------------------------- sayfalar
def t1():
    hero = ('<div style="background:' + INK_BAND + ';border-radius:16px;padding:28px 30px;display:flex;gap:24px;align-items:center;overflow:hidden">'
            '<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:13px">'
            + label("Çok şubeli yeme-içme zincirleri için", "rgba(255,255,255,.55)")
            + h1("Şube talimatları,<br>kanıtıyla.", 40, "#fff", "16ch")
            + p("Açılış, kapanış, hijyen ve soğuk zincir listeleri merkez tarafından bir kez kurulur; her gece şubede kendiliğinden açılır; "
                "personel fotoğraf ve ölçümle kapatır. Merkez sabah yalnızca aksayanı görür, denetim kaydını tek tuşla alır.", 14, "rgba(255,255,255,.78)", "46ch")
            + '<div style="display:flex;gap:7px;flex-wrap:wrap">'
            + "".join('<span style="font-size:11px;font-weight:600;color:#fff;background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.18);'
                      'border-radius:999px;padding:4px 10px">' + x + '</span>' for x in ["5–100 şube", "Türkçe", "Veriler Türkiye’de", "Kişi puanı yok"])
            + '</div></div>'
            '<div style="flex:none;position:relative;width:236px;height:286px">'
            '<div style="position:absolute;left:-4px;top:-14px">' + scaled(B.scr_kiosk(), 390, 844, 0.38) + '</div>'
            '<div style="position:absolute;left:86px;top:112px;border-radius:10px;box-shadow:0 18px 38px rgba(0,0,0,.4)">' + scaled(B.scr_morning(), 390, 844, 0.25) + '</div>'
            '</div></div>')
    stats = ('<div style="display:flex;gap:10px">'
             + stat("6–8 dk", "kapanış listesinin personele maliyeti")
             + stat("3 dk", "denetim kaydının PDF olarak çıkması")
             + stat("1 saat", "ilk şubenin kurulumu; aynı gece başlar")
             + stat("0", "kişi puanı, biyometri, sohbet", T["marka"]) + '</div>')
    kim = table(["Kim", "Ne kazanır", "Nerede"],
                [["<b>Operasyon müdürü</b><div style='color:" + T["sessiz"] + ";font-size:11px'>satın alan</div>",
                  "Elli şubede kapanışın gerçekten yapıldığını kanıtla görür; denetimde kaydı dakikalar içinde verir", "Web"],
                 ["<b>Bölge müdürü</b>", "Ziyaretini kontrolle değil işle geçirir; dün geceyi sabah 07:00’de özetle alır", "Telefon + web"],
                 ["<b>Şube müdürü</b>", "Üç gruptan gelen aynı soruyu cevaplamayı bırakır; yapılamayanı sebebiyle görür", "Telefon"],
                 ["<b>Personel</b>", "Ne yapacağını tek ekranda görür; yaptığını kanıtlar, sonradan suçlanmaz", "Şube tableti"]],
                widths=["24%", "56%", "20%"])
    idx = ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:12px;padding:12px 15px;display:grid;'
           'grid-template-columns:1fr 1fr;gap:5px 18px">'
           + "".join('<div style="display:flex;gap:9px;font-size:12.5px;line-height:1.45"><span style="color:' + T["marka"] + ';font-weight:700;width:14px">' + str(i) + '</span><span>' + t + '</span></div>'
                     for i, t in [(2, "Sorun ve bedeli"), (3, "Nasıl çalışır — bir gece"), (4, "Personel deneyimi"), (5, "Yönetici deneyimi"),
                                  (6, "Kanıt ve uyum"), (7, "Alternatiflerle karşılaştırma"), (8, "Pilot ve sonraki adım")])
           + '</div>')
    return page(w(25) + hero + stats + h2("Kim için, ne kazanır") + kim + label("Bu dosyada") + idx + foot(1), gap=15)

def t2():
    tanidik = ['Kapanışın yapıldığını sabah açan söylüyor; yapılmadıysa kimse söylemiyor',
               'Geçen ayın bir gününe ait fotoğrafı bulmak imkânsız; WhatsApp’ta kayboldu',
               'Sıcaklık defteri aynı kalemle, aynı anda doldurulmuş görünüyor',
               'Bölge müdürü ziyaretinin yarısı “yapıldı mı” kontrolüyle geçiyor',
               'Denetimde istenen kaydı aramak saatler alıyor, eksik çıkabiliyor',
               'Aynı soru üç ayrı WhatsApp grubunda tekrar ediyor']
    liste = "".join('<div style="display:flex;gap:9px;align-items:flex-start">'
                    '<div style="width:15px;height:15px;border:1.5px solid ' + T["sessiz"] + ';border-radius:4px;margin-top:3px;flex:none"></div>'
                    '<div style="font-size:13.5px;line-height:1.45">' + t + '</div></div>' for t in tanidik)
    hesap = table(["25 şubelik bir zincirde", "Ayda"],
                  [["Şube müdürü başına WhatsApp takibi ≈ 6 saat <span style='color:" + T["sessiz"] + "'>(25 × ₺250/saat)</span>", "<b>₺37.500</b>"],
                   ["Bölge müdürü ziyaretlerinin kontrol payı", "<span style='color:" + T["sessiz"] + "'>ölçülecek</span>"],
                   ["Kaçırılan işin ürün kaybı ve şikâyet maliyeti", "<span style='color:" + T["sessiz"] + "'>ölçülecek</span>"],
                   ["Bir denetim cezası riski", "<span style='color:" + T["sessiz"] + "'>tek olayda yıllık bedeli aşabilir</span>"]],
                  widths=["74%", "26%"])
    uyari = ('<div style="background:' + T["uyariA"] + ';border-radius:11px;padding:11px 13px;font-size:12px;line-height:1.5;color:' + T["ink2"] + '">'
             '<b>Bu rakamlar varsayımdır.</b> Pilotun ilk haftasında sizin şubelerinizin verisiyle yeniden hesaplanır; '
             'tek hedef, aylık bedelin karşılığının ölçülebilir olması.</div>')
    kayit = ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["kritik"] + ';border-radius:12px;padding:12px 14px">'
             + h3("Bir de görünmeyen kayıp", T["kritik"])
             + p("Bazı işletmelerde sipariş geçilmeden ürün üretiliyor, para elden alınıyor ve kasaya hiç girmiyor. Bunun imzası tek bir eşitsizlik: "
                 "<b>üretilen > satılan</b>. Yol haritasında bu fark, kimseyi suçlamadan “açıklanamayan fark” olarak raporlanır.", 12.5) + '</div>')
    return page(head(2, "Sorun") + h1("Sorun işin yapılmaması değil;<br>yapıldığının bilinmemesi.", 31, mw="30ch")
                + p("Talimat WhatsApp’tan gidiyor, cevap “yapıldı abi” olarak geliyor. İş genellikle yapılıyor — ama yapılmadığında bunu kimse zamanında görmüyor, "
                    "yapıldığında da kanıtı bulunamıyor. Maliyet iki yerde birikiyor: yöneticinin zamanı ve kanıtsızlığın riski.")
                + '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:18px;align-items:start">'
                + '<div style="display:flex;flex-direction:column;gap:9px">' + label("Tanıdık geliyorsa") + liste
                + quote("Elli şubede kapanış gerçekten yapılıyor mu, bilmiyorum.", "Hedef müşteri tanımındaki operasyon müdürü — 02-urun/02 personalar") + '</div>'
                + '<div style="display:flex;flex-direction:column;gap:10px">' + label("Bugünün görünmeyen faturası") + hesap + uyari + kayit + '</div></div>'
                + label("Yapılmayan iş ne zaman fark edilir?")
                + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">'
                + '<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:12px;padding:12px 14px">'
                + h3("Bugün", T["kritik"])
                + "".join('<div style="display:flex;gap:8px;font-size:12.5px;line-height:1.5;color:' + T["ink2"] + '"><span style="color:' + T["kritik"] + '">→</span>' + x + '</div>'
                          for x in ["Müşteri şikâyeti geldiğinde", "Bölge müdürü ziyarete gittiğinde", "Denetçi kapıda beklerken", "Çoğu zaman: hiç"])
                + '</div><div style="background:' + T["yuzey"] + ';border:1px solid ' + T["marka"] + ';border-radius:12px;padding:12px 14px">'
                + h3("Talimatname ile", T["marka"])
                + "".join('<div style="display:flex;gap:8px;font-size:12.5px;line-height:1.5;color:' + T["ink2"] + '"><span style="color:' + T["marka"] + '">→</span>' + x + '</div>'
                          for x in ["Kritik maddede aynı dakika (push, gerekirse SMS)", "Kaçırılan listede tolerans dolduğunda",
                                    "Ertesi sabah 07:00 özetinde, kanıtıyla", "Denetimde: doğrulama kodlu PDF"])
                + '</div></div>' + foot(2), gap=14)

def t3():
    adim = lambda n, t, d: ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:12px;padding:12px 14px;flex:1;min-width:0">'
                            '<div style="font-family:' + SERIF + ';font-size:25px;font-weight:700;color:' + T["marka"] + ';line-height:1">' + str(n) + '</div>'
                            '<div style="font-size:14px;font-weight:700;margin-top:3px">' + t + '</div>'
                            '<div style="font-size:12.5px;line-height:1.45;color:' + T["ink2"] + ';margin-top:4px">' + d + '</div></div>')
    tl = [("22:00", "Pencere açıldı", "Liste şube tabletinde belirir; saat şubenin kapanışından türetilir.", T["marka"]),
          ("22:58", "Emre PIN ile girdi", "Ortak tablette adına dokunur. Listeyi ilk açan alır; diğerleri “Emre yapıyor” görür.", T["marka"]),
          ("23:20", "Buzdolabı 6,0 °C", "Aralık dışı: fotoğraf ve not zorunlu. Kritik madde → şube ve bölge müdürüne anında bildirim, 10 dakikada okunmazsa SMS; aksiyon açıldı.", T["kritik"]),
          ("23:30", "Zemin yapılamadı", "Sebep: malzeme yok. Şube müdürüne aksiyon düştü (72 saat).", T["uyari"]),
          ("23:41", "Gönderildi", "13 madde geçti; kritik madde yüzünden sonuç “başarısız”. Kayıt kilitlendi.", T["kritik"]),
          ("03:30", "Bakırköy kaçırdı", "Tolerans doldu; şube müdürüne bildirim. Gece kimse aranmaz.", T["kritik"]),
          ("07:00", "Sabah özeti", "Bölge müdürü ve yöneticiye push + e-posta: kaçıran, başarısız, yapılamayan, gecikmiş aksiyon.", T["marka"]),
          ("08:05", "Aksiyon kapandı", "Servis geldi, conta değişti, ölçüm 3,4 °C. Not zorunlu; olay izine yazıldı.", T["marka"])]
    def item(t, b, d, c, last=False):
        line = "" if last else '<div style="position:absolute;left:6px;top:17px;bottom:-11px;width:2px;background:' + T["cizgi"] + '"></div>'
        return ('<div style="position:relative;padding-left:26px;padding-bottom:' + ("0" if last else "11") + 'px">' + line +
                '<div style="position:absolute;left:0;top:4px;width:14px;height:14px;border-radius:50%;background:' + c + ';border:3px solid ' + T["zemin"] + '"></div>'
                '<div style="display:flex;gap:10px;align-items:baseline">'
                '<b style="font:600 12.5px ui-monospace,Menlo,Consolas,monospace;color:' + T["ink2"] + ';width:42px;flex:none">' + t + '</b>'
                '<div><b style="font-size:14px">' + b + '</b>'
                '<div style="font-size:12.5px;color:' + T["ink2"] + ';line-height:1.45;margin-top:1px;max-width:50ch">' + d + '</div></div></div></div>')
    gece = "".join(item(*x, last=(i == len(tl) - 1)) for i, x in enumerate(tl))
    kutu = ('<div style="background:' + T["markaA"] + ';border-radius:12px;padding:12px 14px">' + h3("Gece kimse aranmaz", T["marka"])
            + p("Kaçırılan liste için şube müdürüne anında bildirim, bölge müdürüne 07:00 özeti. Yalnızca gıda güvenliği, iş güvenliği ve para ile ilgili "
                "kritik maddeler anında bildirilir; teslim olmazsa SMS. Sessiz saat 23:00–07:00. Kuralların tamamı sabittir — ayar labirenti yok.", 12.5) + '</div>')
    return page(head(3, "Nasıl çalışır") + h1("Bir gece, baştan sona", 31)
                + '<div style="display:flex;gap:10px">'
                + adim(1, "Merkez kurar", "Şubeler Excel’den; kapanış listesi 8 hazır şablondan; pencere şube saatinden hesaplanır. Bu gece başlar.")
                + adim(2, "Personel tamamlar", "Kioskta PIN, maddeler, kamera doğrudan açılır, sıcaklık girilir. Wi-Fi yoksa kayıt cihazda bekler.")
                + adim(3, "Merkez görür", "07:00 özeti ve istisna panosu; her çalıştırma için doğrulama kodlu PDF.") + '</div>'
                + '<div style="display:grid;grid-template-columns:minmax(0,1fr) 225px;gap:18px;align-items:start">'
                + '<div style="display:flex;flex-direction:column">' + gece + '</div>'
                + '<div style="display:flex;flex-direction:column;gap:11px">' + shot(scr_unable(), 390, 844, 0.44, "“Yapılamadı” — sebep seti sabit") + kutu + '</div></div>' + foot(3), gap=14)

def t4():
    ekranlar = ('<div style="display:flex;gap:12px;align-items:flex-start">'
                + shot(B.scr_kiosk(), 390, 844, 0.33, "Kapanış listesi · şube tableti", [(1, 50, 8), (2, 80, 43), (3, 50, 93)])
                + shot(B.scr_temp(), 390, 844, 0.33, "Sıcaklık · aralık dışı", [(4, 50, 68), (5, 50, 86)])
                + '<div style="flex:1;min-width:0">'
                + legend([(1, "<b>Kim yapıyor belli.</b> Ortak tablette adına dokun, PIN gir; listeyi ilk açan alır."),
                          (2, "<b>Kanıt iki dokunuşta.</b> Kamera doğrudan açılır, galeri kapalı; fotoğrafa şube, saat ve kişi damgalanır."),
                          (3, "<b>Eksikse gönderilemez.</b> Zorunlu maddeler bitmeden “Gönder” pasif; gönderilen kayıt kilitlenir."),
                          (4, "<b>Aralık ekranda.</b> Kabul aralığı maddeyle birlikte gelir; her dolap için ayrı tanımlanır."),
                          (5, "<b>Tek kural.</b> Aralık dışı veya “Hayır” cevapta fotoğraf ve not zorunlu; kritikse aksiyon açılır.")])
                + '</div></div>')
    turler = table(["Madde türü", "Örnek"],
                   [["Onay", "Tezgâh dezenfekte edildi"],
                    ["Çoktan seçmeli <span style='color:" + T["sessiz"] + "'>Evet / Hayır / Uygun değil</span>", "Gaz vanası kapatıldı mı?"],
                    ["Sayı + birim", "Kasa sayımı (₺) · polar madde (%)"],
                    ["Sıcaklık <span style='color:" + T["sessiz"] + "'>kabul aralığıyla</span>", "Buzdolabı 0–4 °C · dondurucu −30…−18 °C"],
                    ["Fotoğraf (1–3)", "Çöp alanı · kepenk · irsaliye"],
                    ["Metin · talimat", "Devralan kişi · “Kasa devri listesinde tamamlayın”"]],
                   widths=["44%", "56%"])
    benimseme = ('<div style="display:flex;flex-direction:column;gap:8px">'
                 + check("Telefonu olmayan personel.", "Şube müdürü kioskta PIN atar; kimse dışarıda kalmaz.")
                 + check("Wi-Fi gidince.", "Liste cihazda devam eder, kayıtlar 72 saat kuyrukta bekler, bağlantıda senklenir; damga sunucu saatiyle düzeltilir.")
                 + check("Vardiya devri.", "Sabahçı açılış listesinin başında “dün gece” bloğunu görür.")
                 + check("Gözetim değil, kanıt.", "Kişi bazlı puan yok; kayıt personeli de korur — “ben yapmıştım” tartışması biter.") + '</div>')
    return page(head(4, "Personel deneyimi") + h1("Altı dakikada biter,<br>bir günde öğrenilir.", 31, mw="26ch")
                + p("Personel tarafı üç ekrandan ibarettir: bugün, liste, kanıt. Dokunma alanları eldivenle kullanılacak büyüklükte; "
                    "ekranlar düşük segment Android tablette de akar. Yeni gelen personel ilk gece listeyi tek başına tamamlayabilir.")
                + ekranlar
                + '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:16px;align-items:start">'
                + '<div style="display:flex;flex-direction:column;gap:7px">' + label("Altı madde türü, hepsi bu") + turler + '</div>'
                + '<div style="display:flex;flex-direction:column;gap:7px">' + label("Sahadaki gerçekler") + benimseme + '</div></div>' + foot(4), gap=13)

def t5():
    esk = ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:7px">'
           + label("Sabit eskalasyon")
           + "".join('<div style="display:flex;gap:9px;align-items:flex-start;font-size:12.5px;line-height:1.45">'
                     '<div style="width:8px;height:8px;border-radius:50%;background:' + c + ';margin-top:5px;flex:none"></div><div><b>' + t + '</b> ' + d + '</div></div>'
                     for t, d, c in [("Kritik madde başarısız →", "şube ve bölge müdürüne anında push; 10 dakikada okunmazsa SMS.", T["kritik"]),
                                      ("Kaçırılan liste →", "şube müdürüne anında; bölge müdürü ve yönetici 07:00 özetinde.", T["kritik"]),
                                      ("Yapılamadı →", "şube müdürüne aksiyon (72 saat), sebebiyle birlikte.", T["uyari"]),
                                      ("Gecikmiş aksiyon →", "sabah özetinde başa yazılır.", T["uyari"]),
                                      ("Sessiz saat 23:00–07:00:", "yöneticiye yalnızca kritik bildirim gider.", T["marka"])]) + '</div>')
    return page(head(5, "Yönetici deneyimi") + h1("Her sabah iki dakika", 31)
                + p("Yönetici ürünü taramaz; ürün ona aksayanı getirir. Panonun varsayılanı istisna görünümüdür: sorun yoksa sayfa bunu tek cümleyle söyler — "
                    "“Dün gece 12 şubenin 12’si yolunda.”")
                + '<div style="display:flex;gap:14px;align-items:flex-start">'
                + shot(B.scr_morning(), 390, 844, 0.38, "Sabah özeti · bölge müdürü", [(1, 50, 7), (2, 50, 37)])
                + '<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:10px">'
                + shot(B.scr_pano(1200, 760), 1200, 760, 0.345, "İstisna panosu · merkez", [(3, 22, 34), (4, 50, 60), (5, 84, 85)])
                + legend([(1, "Push ve e-posta aynı metinle gider; telefon açılmadan durum bilinir."),
                          (2, "Dikkat isteyen şube ve nedeni; tıklayınca çalıştırma detayı ve fotoğraflar."),
                          (3, "Altı sayıda gece özeti: zamanında, geç, başarısız, kaçırıldı, yapılamadı, açık aksiyon."),
                          (4, "Yalnızca sorunlu satırlar listelenir — “her şey yolunda” da bir cevaptır."),
                          (5, "Şube × liste ızgarası: tüm gün tek bakışta, hücreden detaya.")]) + '</div></div>'
                + '<div style="display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:16px;align-items:start">' + esk
                + '<div style="display:flex;gap:9px">' + stat("%81", "zamanında tamamlanma <span style='color:" + T["sessiz"] + "'>örnek ay</span>", T["marka"])
                + stat("%97", "fotoğraf zorunlu maddede kanıt", T["marka"]) + '</div></div>' + foot(5), gap=13)

def t6():
    zincir = ["Fotoğraf yalnızca uygulama içinden çekilir — galeri kapalı",
              "Sunucu damgalar: şube · tarih-saat · kullanıcı · cihaz; ham dosya ayrıca saklanır",
              "Dosyanın SHA-256 özeti cevaba bağlanır; aynı fotoğraf ikinci kez gönderilemez",
              "Her olay ekle-yalnız günlüğe yazılır, önceki olayın özetiyle zincirlenir",
              "Gönderilen kayıt değişmez; düzeltme ayrı “ek” kaydıdır",
              "Galeri · şube dışında konum · cihaz saati farkı · toplu geç senk kayıtta bayrakla görünür",
              "PDF doğrulama kodu ve üretim zamanı taşır"]
    akis = "".join('<div style="display:flex;gap:9px;align-items:flex-start;font-size:13px;line-height:1.45">' + pin(i + 1) +
                   '<div style="color:' + T["ink2"] + '">' + t + '</div></div>' for i, t in enumerate(zincir))
    kvkk = table(["Soru", "Talimatname’de cevap"],
                 [["Personel puanlanıyor mu?", "<b>Hayır.</b> Skor şube ve bölge düzeyinde; kişi düzeyinde yalnızca gecikme ve eksik görünür"],
                  ["Biyometri?", "<b>İşlenmez.</b> Giriş telefon + OTP ya da kioskta PIN"],
                  ["Konum?", "Yalnızca madde tamamlanma anında tek nokta; izin verilmezse kayıt “konum yok” notuyla sürer"],
                  ["Veri nerede?", "Türkiye’deki yerel bulutta; alt işleyen listesi sözleşme ekinde"],
                  ["Ne kadar saklanıyor?", "Kanıt dosyaları 24 ay, sonra otomatik silinir; iş kaydı kişi maskelenerek kalır"],
                  ["Belgeler hazır mı?", "Personel aydınlatma metni ve veri işleme sözleşmesi taslakları hazır; avukat onayından geçirilir"]],
                 widths=["26%", "74%"])
    return page(head(6, "Kanıt ve uyum") + h1("“Fotoğrafı dün çekmiş”<br>tartışması biter.", 31, mw="26ch")
                + p("Ürünün değeri kanıtın sonradan değiştirilememesine dayanır. Cihaz saati değil sunucu zamanı esastır; kayıt silinmez, düzeltme ek kayıt olarak görünür.")
                + '<div style="display:grid;grid-template-columns:minmax(0,0.85fr) minmax(0,1.15fr);gap:16px;align-items:start">'
                + '<div style="display:flex;flex-direction:column;gap:9px">' + label("Kanıt zinciri") + akis
                + '<div style="background:' + T["yuzey2"] + ';border-radius:11px;padding:9px 12px;font-size:12.3px;line-height:1.5;color:' + T["ink2"] + '">'
                '<b>Denetim günü:</b> şube ve tarih seçilir; sıcaklık günlüğü ve çalıştırma raporu doğrulama kodlu PDF olarak iner. '
                'Denetçi hangi ölçümün ne zaman, kim tarafından girildiğini sayfada görür.</div>'
                + '<div style="background:' + T["yuzey2"] + ';border-radius:11px;padding:9px 12px;font-size:12.3px;line-height:1.5;color:' + T["ink2"] + '">'
                '<b>Belge takvimi:</b> yangın tüpü dolumu, baca ve su deposu temizliği, periyodik elektrik kontrolü, hijyen eğitimi ve portör belgeleri geçerlilik bitişiyle kayıtlıdır; 30 ve 7 gün önce uyarır, süresi geçende aksiyon açılır.</div></div>'
                + '<div style="display:flex;flex-direction:column;gap:7px">' + label("Çalıştırma raporu — denetimde verilen belge")
                + shot(scr_detail(1200, 760), 1200, 760, 0.335, "Kadıköy · 13 Eylül · doğrulama kodlu") + '</div></div>'
                + kvkk + foot(6), gap=11)

def t7():
    ok = '<span style="color:' + T["marka"] + ';font-weight:700">var</span>'
    no = '<span style="color:' + T["sessiz"] + '">yok</span>'
    kismi = '<span style="color:' + T["uyari"] + '">kısmen</span>'
    karsilastirma = table(["", "WhatsApp grupları", "Kâğıt form / Excel", "<b>Talimatname</b>"],
                          [["Liste kendiliğinden açılır", no, no, ok],
                           ["Yapılmayan iş yöneticiye düşer", no, no, ok],
                           ["Fotoğraf ve ölçüm kanıtı aranabilir", no, kismi, ok],
                           ["Kayıt sonradan değiştirilemez", no, no, ok],
                           ["Denetim kaydı dakikalar içinde", no, kismi, ok],
                           ["Çevrimdışı çalışır", ok, ok, ok],
                           ["Personel eğitimi", "<span style='color:" + T["marka"] + "'>gerekmez</span>", "<span style='color:" + T["marka"] + "'>gerekmez</span>", "10 dakika"]],
                          widths=["34%", "20%", "22%", "24%"])
    itiraz = ('<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">'
              + qa("“Personel kullanmaz.”", "Akış üç ekran ve iki dokunuş; kioskta PIN’le giriş. Personele mesaj “seni izliyoruz” değil, “yaptığını kanıtlıyorsun”.")
              + qa("“Şubede tablet yok.”", "Personel kendi telefonundan da tamamlayabilir; pilotta ödünç tablet verilebilir. Kiosk zorunlu değil.")
              + qa("“Mutfakta internet zayıf.”", "Çevrimdışı öncelikli: liste cihazda tamamlanır, bağlantı gelince senklenir; damga sunucu saatiyle düzeltilir.")
              + qa("“KVKK sorun çıkarır mı?”", "Kişi puanı ve biyometri yok, konum tek nokta, veriler Türkiye’de; aydınlatma metni ve veri işleme sözleşmesi hazır.")
              + qa("“Zaten kameramız var.”", "Kamera ne yapıldığını kanıtlamaz, kaydı aramak saatler alır. Talimatname maddeyi, saati ve kişiyi kayıtla verir.")
              + qa("“Yazılımımızda görev modülü var.”", "Varsa kullanın. Fark, kanıtın değiştirilemezliği ve denetimde kullanılabilir PDF; iki hafta yan yana deneyin.") + '</div>')
    degil = ('<div style="background:' + T["yuzey2"] + ';border-radius:11px;padding:11px 14px">' + h3("Ne değil")
             + p("Sohbet uygulaması değil, mesai/PDKS değil, vardiya planlama değil, eğitim platformu değil, personel performans sistemi değil. "
                 "İlk sürüm bilerek dar: dört rol, altı madde türü, tek kural. Duyuru, koşul editörü ve ayrıntılı raporlar pilot sonrasına bırakıldı.", 12.5) + '</div>')
    return page(head(7, "Karşılaştırma") + h1("Alternatifle yan yana", 31)
                + p("Bu işi bugün WhatsApp, kâğıt form ve Excel yapıyor. Soru “daha iyi bir uygulama” değil, “yapıldığını nasıl biliyoruz” sorusudur.")
                + karsilastirma + label("Sık gelen itirazlar") + itiraz + degil + foot(7), gap=12)

def t8():
    kutu = lambda n, l: ('<div style="background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:11px;padding:11px 13px;flex:1;min-width:0">'
                         '<div style="font-family:' + SERIF + ';font-size:21px;font-weight:700;color:#fff">' + n + '</div>'
                         '<div style="font-size:11.5px;line-height:1.35;color:rgba(255,255,255,.72);margin-top:3px">' + l + '</div></div>')
    pilot = ('<div style="background:' + INK_BAND + ';border-radius:16px;padding:24px 26px;display:flex;flex-direction:column;gap:13px">'
             + label("Sonraki adım", "rgba(255,255,255,.55)") + h1("8 haftalık ücretli pilot", 30, "#fff", "20ch")
             + p("Seçtiğiniz 5–15 şubede kapanış ve soğuk zincir listeleriyle başlarız. Yerinde kurulum bir gün: kiosk, PIN’ler, şablon uyarlaması, "
                 "şube müdürüne 30 dakika ve personele 10 dakika eğitim. Haftada bir 30 dakikalık geri bildirim görüşmesi.", 13.5, "rgba(255,255,255,.78)", "60ch")
             + '<div style="display:flex;gap:9px">' + kutu("≥ %80", "liste pencere içinde tamamlanır") + kutu("≥ %95", "fotoğraf zorunlu maddede kanıt")
             + kutu("≥ %80", "kritik aksiyon vadesinde kapanır") + '</div>'
             + p("Dördüncü hafta sonunda birlikte ölçeriz. Ölçütler tutarsa yıllık sözleşmeyi konuşuruz; tutmazsa kalan aylar iade edilir. "
                 "Şube başına aylık ücret, pilot kapsamına göre görüşmede belirlenir.", 12, "rgba(255,255,255,.62)", "70ch") + '</div>')
    takvim = table(["Pilot takvimi", "Ne olur"],
                   [["<b>Gün 0</b>", "Şube ve personel listesi (Excel), aydınlatma metninin personele iletilmesi"],
                    ["<b>Gün 1</b>", "Yerinde kurulum: kiosk, PIN’ler, şablon uyarlaması, eğitim — akşam ilk kapanış listesi açılır"],
                    ["<b>Hafta 1–2</b>", "Günlük takip; madde ve saat ayarları sahadan gelen geri bildirimle düzeltilir"],
                    ["<b>Hafta 4</b>", "Ölçüm: tamamlanma, kanıt ve aksiyon oranları; ara karar"],
                    ["<b>Hafta 8</b>", "Pilot raporu; yıllık sözleşme görüşmesi veya ayrılma"]],
                   widths=["22%", "78%"])
    yol = table(["Sürüm", "İçerik"],
                [["<b>v1</b>", "4 rol · 6 madde türü · tek kural · 8 hazır şablon · kiosk ve çevrimdışı · sabit eskalasyon ve 07:00 özeti · istisna panosu · aylık özet · sıcaklık günlüğü · belge ve periyodik bakım takvimi · kanıt bütünlüğü bayrakları · doğrulama kodlu PDF"],
                 ["<b>v1.1</b>", "<b>Denetçiye tek dosya ve süreli bağlantı</b> · madde kütüphanesi ve işletme türü paketleri · yakın kopya fotoğraf tespiti · üretim–satış mutabakatı · duyuru ve okundu onayı · koşul editörü · ayrıntılı raporlar · denetim izi ekranı"],
                 ["<b>v2</b>", "Franchise marka kütüphanesi · başka sektör paketleri · POS ve İK entegrasyonları · kamera ile üretim sayımı"]],
                widths=["12%", "88%"])
    iletisim = ('<div style="display:flex;align-items:center;justify-content:space-between;gap:16px;border-top:1px solid ' + T["cizgi"] + ';padding-top:12px">'
                '<div style="display:flex;flex-direction:column;gap:3px">' + w(23) +
                '<div style="font-size:12px;color:' + T["sessiz"] + '">Şube operasyonları, kanıtıyla.</div></div>'
                '<div style="font-size:13.5px;color:' + T["ink"] + ';text-align:right;line-height:1.55">'
                '<b>[Ad Soyad]</b> · [telefon]<br><span style="color:' + T["ink2"] + '">[e-posta] · [alan adı]</span></div></div>')
    yol_not = ('<div style="font-size:11.5px;color:' + T["ink2"] + ';background:' + T["uyariA"] + ';border-radius:9px;padding:7px 11px;margin-top:-2px">'
               '<b>v1.1 ve v2 satırları yol haritasıdır:</b> henüz geliştirilmediler, pilot ölçütleri ve sözleşme yalnızca <b>v1</b> satırını kapsar. '
               'Sıraları pilotta sizin şubelerinizden çıkan ihtiyaca göre belirlenir.</div>')
    foy = ('<div style="font-size:11.5px;color:' + T["sessiz"] + ';margin-top:-4px">'
           'Her satırın kısa açıklaması ve ekranı ayrı bir belgede: <b style="color:' + T["ink2"] + '">özellik föyü</b> (A4, ' + str(S["foy_sayfa"]) + ' sayfa; yol haritası satırlarının tasarım taslakları da orada — denetçi dosyası 8. sayfada).</div>')
    return page(head(8, "Pilot ve sonraki adım") + pilot + takvim + label("Yol haritası · v1 dışındaki satırlar sözleşme kapsamına girmez") + yol + yol_not + foy + iletisim
                + foot(8, "Talimatname çalışma adıdır; ekranlardaki veriler örnektir."), gap=13)

# ---------------------------------------------------------------- üretim
PAGES = {"Main.dc.html": t1, "T2.dc.html": t2, "T3.dc.html": t3, "T4.dc.html": t4,
         "T5.dc.html": t5, "T6.dc.html": t6, "T7.dc.html": t7, "T8.dc.html": t8}
SCREENS = {"Yapilamadi.dc.html": scr_unable, "Detay.dc.html": scr_detail, "Sihirbaz.dc.html": scr_wizard}

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    for name, fn in list(PAGES.items()) + list(SCREENS.items()):
        open(os.path.join(OUTDIR, name), "w", encoding="utf-8").write(B.dc(fn()))
    ab = [{"file": n, "title": "Tanıtım · sayfa " + str(i + 1), "x": i * 880, "y": 0, "w": 794, "h": 1123, "print": "fixed"}
          for i, n in enumerate(PAGES)]
    for i, (n, t) in enumerate([("Yapilamadi.dc.html", "Ekran · yapılamadı"), ("Detay.dc.html", "Ekran · çalıştırma detayı (web)"), ("Sihirbaz.dc.html", "Ekran · kurulum sihirbazı (web)")]):
        ab.append({"file": n, "title": t, "x": i * 1320, "y": 1280, "w": 390 if i == 0 else 1200, "h": 844 if i == 0 else 760})
    json.dump({"artboards": ab, "launch": {"view": "canvas"}}, open(os.path.join(OUTDIR, "canvas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    css = ("body{margin:0;background:#e9e6de;font-family:" + SANS + "} .sheet{margin:18px auto;box-shadow:0 10px 30px rgba(28,33,40,.14);width:794px} "
           "@media print{body{background:#fff}.sheet{margin:0;box-shadow:none}.sheet+.sheet{break-before:page}@page{size:A4;margin:0}}")
    html = ('<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Talimatname tanıtım dosyası</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bitter:wght@700&display=swap">'
            '<style>' + css + '</style></head><body>'
            + "".join('<div class="sheet">' + fn() + '</div>' for fn in PAGES.values()) + '</body></html>')
    out = os.path.join(HERE, "talimatname-tanitim.html")
    open(out, "w", encoding="utf-8").write(_damga(html))

    css2 = ("body{margin:0;background:#e9e6de;font-family:" + SANS + "}"
            ".page{width:100%;display:flex;justify-content:center;padding:14px 8px}"
            ".box{width:794px;transform-origin:top center;box-shadow:0 10px 30px rgba(28,33,40,.14)}"
            "@media print{body{background:#fff}.page{padding:0}.box{transform:none!important;box-shadow:none}"
            ".page+.page{break-before:page}@page{size:A4;margin:0}}")
    js = ("<script>(function(){function f(){var w=Math.min(document.documentElement.clientWidth-16,794);var s=w/794;"
          "document.querySelectorAll('.page').forEach(function(pg){var b=pg.querySelector('.box');b.style.transform='scale('+s+')';"
          "pg.style.height=(1123*s+28)+'px';});}f();addEventListener('resize',f);})();</script>")
    html2 = ('<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
             '<title>Talimatname Tanıtım Dosyası</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bitter:wght@700&display=swap">'
             '<style>' + css2 + '</style>'
             + "".join('<div class="page"><div class="box">' + fn() + '</div></div>' for fn in PAGES.values()) + js)
    open(os.path.join(HERE, "talimatname-tanitim-sayfa.html"), "w", encoding="utf-8").write(_damga(html2))
    print("ok:", len(PAGES), "sayfa,", len(SCREENS), "ekran")

    if "--pdf" in sys.argv:
        edge = next((x for x in [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"] if os.path.exists(x)), None)
        if not edge:
            print("Edge yok"); return
        pdf = out.replace(".html", ".pdf")
        if os.path.exists(pdf):
            os.remove(pdf)
        prof = tempfile.mkdtemp(prefix="talimatname-pdf-")
        subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-first-run", "--user-data-dir=" + prof, "--no-pdf-header-footer",
                        "--print-to-pdf=" + pdf, "--virtual-time-budget=9000", "file:///" + out.replace(os.sep, "/")],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=200)
        for _ in range(180):
            if os.path.exists(pdf) and os.path.getsize(pdf) > 10_000:
                break
            time.sleep(0.5)
        _pdf_damga(pdf)
        print(pdf, "ok" if os.path.exists(pdf) else "HATA")

if __name__ == "__main__":
    main()
