# -*- coding: utf-8 -*-
"""Talimatname tanıtım dosyası — 6 sayfalık ayrıntılı broşür (A4) + 3 yeni ekran tasarımı.
2 sayfalık özet broşür (build_brosur.py) bırakılacak belge; bu dosya anlatım içindir.
Üretir: T1…T6.dc.html (sayfalar), YapilamadI/Detay/Sihirbaz .dc.html (ekranlar), canvas-tanitim.json,
talimatname-tanitim.html (+ --pdf).
Ortak bileşenler build_brosur.py'den; tasarım token'ları 05-tasarim/04."""
import os, sys, subprocess, tempfile, time, json
import build_brosur as B

T, SANS, SERIF = B.T, B.SANS, B.SERIF
HERE = os.path.dirname(os.path.abspath(__file__))
w, card, chip, box, row, phone, scaled = B.wordmark, B.card, B.chip, B.box, B.row, B.phone, B.scaled

# ---------------------------------------------------------------- küçük yardımcılar
def h1(t, size=34): return f'<h1 style="font-family:{SERIF};font-size:{size}px;line-height:1.1;font-weight:700;margin:0;letter-spacing:-0.01em">{t}</h1>'
def h2(t): return f'<h2 style="font-family:{SERIF};font-size:21px;font-weight:700;margin:0 0 2px;line-height:1.2">{t}</h2>'
def p(t, size=14, color=None, mw="78ch"): return f'<p style="margin:0;font-size:{size}px;line-height:1.5;color:{color or T["ink2"]};max-width:{mw}">{t}</p>'
def label(t): return f'<div style="font-size:11px;font-weight:600;letter-spacing:0.07em;text-transform:uppercase;color:{T["sessiz"]}">{t}</div>'
def rule(): return f'<div style="height:1px;background:{T["cizgi"]}"></div>'

def page(inner, gap=18):
    return (f'<div style="box-sizing:border-box;width:794px;height:1123px;background:{T["zemin"]};font-family:{SANS};color:{T["ink"]};'
            f'padding:40px 46px 30px;display:flex;flex-direction:column;gap:{gap}px;overflow:hidden">{inner}</div>')

def head(no, title):
    return (f'<div style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid {T["cizgi"]};padding-bottom:10px">'
            f'{w(18)}<div style="font-size:12px;color:{T["sessiz"]}">{no} · {title}</div></div>')

def foot(no, note=""):
    return (f'<div style="margin-top:auto;display:flex;align-items:center;justify-content:space-between;border-top:1px solid {T["cizgi"]};padding-top:10px;font-size:11px;color:{T["sessiz"]}">'
            f'<span>{note or "Ekranlar ürün tasarımındandır; veriler örnektir."}</span><span>Talimatname · tanıtım dosyası · {no}/6</span></div>')

def bullet(t, d=""):
    return (f'<div style="display:flex;gap:10px;align-items:flex-start">{box("ok")}'
            f'<div style="font-size:14px;line-height:1.45"><b>{t}</b>{" " + d if d else ""}</div></div>')

def tile(n, l, c=None, s=""):
    return (f'<div style="background:{T["yuzey"]};border:1px solid {T["cizgi"]};border-radius:12px;padding:12px 14px;flex:1;min-width:0">'
            f'<div style="font-family:{SERIF};font-size:24px;font-weight:700;line-height:1.1;color:{c or T["ink"]}">{n}</div>'
            f'<div style="font-size:12.5px;color:{T["ink2"]};margin-top:3px;line-height:1.35">{l}</div>'
            + (f'<div style="font-size:11.5px;color:{T["sessiz"]};margin-top:3px">{s}</div>' if s else "") + '</div>')

def table(cols, rows, widths=None, size=13):
    wcols = "".join(f'<col style="width:{x}">' for x in widths) if widths else ""
    th = "".join(f'<th style="text-align:left;padding:7px 9px;font-size:10.5px;letter-spacing:.05em;text-transform:uppercase;color:{T["sessiz"]};background:{T["yuzey2"]};border-bottom:1px solid {T["cizgi"]};font-weight:600">{c}</th>' for c in cols)
    tr = ""
    for i, r in enumerate(rows):
        last = i == len(rows) - 1
        tds = "".join(f'<td style="padding:7px 9px;border-bottom:{"0" if last else "1px solid " + T["cizgi"]};vertical-align:top;line-height:1.4">{c}</td>' for c in r)
        tr += f"<tr>{tds}</tr>"
    return (f'<div style="border:1px solid {T["cizgi"]};border-radius:10px;overflow:hidden;background:{T["yuzey"]}">'
            f'<table style="border-collapse:collapse;width:100%;font-size:{size}px">{wcols}<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>')

# ---------------------------------------------------------------- yeni ekranlar
def scr_unable():
    """Yapılamadı alt sayfası (mobil)."""
    opt = lambda t, sel=False: (f'<div style="padding:13px 12px;border:1.5px solid {T["marka"] if sel else T["cizgi"]};border-radius:12px;font-size:15px;'
                                f'background:{T["markaA"] if sel else T["yuzey"]}">{t}</div>')
    sheet = (f'<div style="position:absolute;left:0;right:0;bottom:0;background:{T["yuzey"]};border-radius:22px 22px 0 0;padding:18px 18px 24px;'
             f'box-shadow:0 -12px 30px rgba(0,0,0,.18);display:flex;flex-direction:column;gap:9px">'
             f'<div style="font-size:18px;font-weight:700">Yapılamadı — Zemin süpürüldü ve paspaslandı</div>'
             f'<div style="padding:12px;border:1.5px dashed {T["cizgi"]};border-radius:12px;font-size:14.5px;color:{T["ink2"]}">İşareti kaldır (yeniden yapacağım)</div>'
             f'<div style="font-size:13px;color:{T["sessiz"]}">Yapılamadıysa sebep seçin</div>'
             + opt("Malzeme yok", True) + opt("Ekipman arızalı") + opt("Zaman yetmedi") + opt("Yetkim yok") + opt("Diğer (not zorunlu)")
             + f'<div style="border:1.5px solid {T["cizgi"]};border-radius:10px;padding:10px 12px;font-size:14px;color:{T["ink2"]}">Paspas deterjanı bitti</div>'
             + f'<div style="display:flex;gap:10px"><div style="flex:1;min-height:48px;border-radius:12px;border:1.5px solid {T["cizgi"]};display:flex;align-items:center;justify-content:center;font-weight:600;color:{T["sessiz"]}">Vazgeç</div>'
             f'<div style="flex:2;min-height:48px;border-radius:12px;border:1.5px solid {T["kritik"]};color:{T["kritik"]};display:flex;align-items:center;justify-content:center;font-weight:600">Kaydet — şube müdürüne bildir</div></div></div>')
    return phone(B.phone_header("Emre T.", "Kadıköy · Cts 13 Eyl") + B.kiosk_list_body(dim=True) + sheet)

def scr_detail(W=1200, H=760):
    """Web: çalıştırma detayı — maddeler, kanıt, aksiyon, olay izi."""
    def mrow(no, title, ans, t, kind="ok", note=""):
        ic = box("crit") if kind == "crit" else (f'<div style="width:26px;height:26px;border-radius:7px;flex:none;background:{T["uyariA"]};border:2px solid {T["uyari"]};display:flex;align-items:center;justify-content:center;color:{T["uyari"]};font-weight:700;font-size:13px">–</div>' if kind == "un" else box("ok"))
        col = T["kritik"] if kind == "crit" else (T["uyari"] if kind == "un" else T["ink"])
        return (f'<div style="display:flex;gap:10px;align-items:center;padding:7px 0;border-bottom:1px solid {T["cizgi"]}">{ic}'
                f'<div style="width:22px;font-size:12px;color:{T["sessiz"]};flex:none">{no}</div>'
                f'<div style="flex:1;min-width:0;font-size:13.5px">{title}{(f"<div style=\'font-size:12px;color:{T[chr(34)+chr(34)] if False else T["sessiz"]}\'>" + note + "</div>") if note else ""}</div>'
                f'<div style="font-size:13px;font-weight:600;color:{col};white-space:nowrap">{ans}</div>'
                f'<div style="width:46px;text-align:right;font-size:12px;color:{T["sessiz"]}">{t}</div></div>')
    maddeler = (mrow(2, "Kahve makinesi ve öğütücü temizlendi", "Yapıldı · fotoğraf", "23:06")
                + mrow(3, "Süt dolabı sıcaklığı", "3,1 °C", "23:09")
                + mrow(4, "Mutfak buzdolabı sıcaklığı", "6,0 °C · aralık dışı", "23:20", "crit", "not: kapı contası gevşek · 1 fotoğraf")
                + mrow(5, "Dondurucu sıcaklığı", "−19,5 °C", "23:21")
                + mrow(10, "Zemin süpürüldü ve paspaslandı", "Yapılamadı · malzeme yok", "23:30", "un", "not: paspas deterjanı bitti")
                + mrow(13, "Gaz vanası kapatıldı", "Evet", "23:37"))
    ph = lambda cap: (f'<div><div style="aspect-ratio:4/3;border-radius:8px;background:repeating-linear-gradient(135deg,#dfe3e8 0 9px,#eef1f4 9px 18px);position:relative;overflow:hidden;border:1px solid {T["cizgi"]}">'
                      f'<div style="position:absolute;left:0;right:0;bottom:0;background:rgba(28,33,40,.82);color:#fff;font:9px/1.3 ui-monospace,Menlo,Consolas,monospace;padding:3px 5px">Kadıköy · 13.09 23:20 · Emre T.</div></div>'
                      f'<div style="font-size:11px;color:{T["sessiz"]};margin-top:3px">{cap}</div></div>')
    tl = lambda t, s, crit=False: (f'<li style="display:grid;grid-template-columns:52px 1fr;gap:8px;padding:3px 0;border-bottom:1px dotted {T["cizgi"]}">'
                                   f'<span style="font:11.5px ui-monospace,Menlo,Consolas,monospace;color:{T["ink2"]}">{t}</span>'
                                   f'<span style="font-size:12.5px;{"color:"+T["kritik"]+";font-weight:600" if crit else ""}">{s}</span></li>')
    izi = ("".join([tl("22:00", "Pencere açıldı (sistem)"), tl("22:58", "Emre T. PIN ile giriş · şube tableti KDK-T1 · konum şube içinde"),
                    tl("23:20", "Madde 4: 6,0 °C aralık dışı → kritik → aksiyon #418 · push Ayşe K. ✓ · push Murat D. ✓", True),
                    tl("23:30", "Madde 10 yapılamadı (malzeme yok) → aksiyon #419"),
                    tl("23:41", "<b>Gönderildi</b> · başarısız (kritik madde) · kayıt kilitlendi"),
                    tl("07:00", "Sabah özeti: Murat D., Selin Y."), tl("08:05", "Aksiyon #418 kapatıldı — Ayşe K. · not + 1 fotoğraf")]))
    return (f'<div style="box-sizing:border-box;width:{W}px;height:{H}px;background:{T["zemin"]};font-family:{SANS};color:{T["ink"]};padding:18px 22px;'
            f'display:flex;flex-direction:column;gap:12px;overflow:hidden;border:1px solid {T["cizgi"]};border-radius:12px;box-shadow:0 18px 40px rgba(28,33,40,.14)">'
            f'<div style="display:flex;align-items:center;gap:12px">{w(18)}<div style="padding-left:14px;border-left:1px solid {T["cizgi"]}">'
            f'<div style="font-family:{SERIF};font-size:19px;font-weight:700">Kadıköy · Kapanış · 13 Eylül</div>'
            f'<div style="font-size:12.5px;color:{T["ink2"]}">Pencere 22:00–01:30 · gönderim 23:41 · Emre T. · şube tableti · puan %87 (bilgi)</div></div>'
            f'<div style="margin-left:auto">{chip("başarısız (kritik madde)", "crit")}</div></div>'
            f'<div style="display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:16px;min-height:0">'
            f'<div style="display:flex;flex-direction:column;gap:10px;min-width:0">{card("<div style=\'font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:" + T["sessiz"] + ";margin-bottom:4px\'>Maddeler (15 / seçili 6)</div>" + maddeler, "padding:12px 14px")}'
            f'{card("<div style=\'font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:" + T["sessiz"] + ";margin-bottom:6px\'>Kanıt fotoğrafları (4)</div><div style=\'display:grid;grid-template-columns:repeat(4,1fr);gap:8px\'>" + ph("2 · Kahve makinesi") + ph("4 · Buzdolabı") + ph("12 · Çöp alanı") + ph("15 · Kepenk") + "</div>", "padding:12px 14px")}</div>'
            f'<div style="display:flex;flex-direction:column;gap:10px;min-width:0">'
            f'{card("<b style=\'font-size:13.5px\'>Aksiyon #418 · kritik</b><div style=\'font-size:12.5px;color:" + T["ink2"] + ";margin-top:3px\'>Mutfak buzdolabı aralık dışı · Ayşe K. · vade 03:20</div><div style=\'font-size:12.5px;margin-top:6px;color:" + T["marka"] + ";font-weight:600\'>Kapalı 08:05 — “Servis geldi, conta değişti; ölçüm 3,4 °C.”</div>", "padding:12px 14px;border-color:" + T["kritik"])}'
            f'{card("<div style=\'font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:" + T["sessiz"] + ";margin-bottom:4px\'>Olay izi — ekle-yalnız, hash zincirli</div><ul style=\'list-style:none;margin:0;padding:0\'>" + izi + "</ul>", "padding:12px 14px")}'
            f'<div style="display:flex;gap:8px;align-items:center;font-size:12px;color:{T["sessiz"]}">'
            f'<div style="padding:8px 12px;border-radius:9px;border:1.5px solid {T["ink"]};color:{T["ink"]};font-weight:600;font-size:13px">PDF indir</div>Doğrulama kodu TN-K7F3A-9C2D</div></div></div></div>')

def scr_wizard(W=1200, H=760):
    """Web: kurulum sihirbazı adım 3 — plan ve pencere."""
    st = lambda n, t, s, state: (f'<div style="border:1.5px solid {T["marka"] if state!="todo" else T["cizgi"]};background:{T["markaA"] if state=="on" else T["yuzey"]};'
                                 f'border-radius:10px;padding:10px 12px"><b style="font-size:13.5px">{"✓ " if state=="done" else ""}{n} · {t}</b>'
                                 f'<div style="font-size:12px;color:{T["sessiz"]}">{s}</div></div>')
    fld = lambda l, v: (f'<label style="display:flex;flex-direction:column;gap:4px;font-size:12px;color:{T["ink2"]}">{l}'
                        f'<div style="border:1.5px solid {T["cizgi"]};border-radius:8px;padding:8px 10px;background:{T["yuzey"]};font-size:14px;color:{T["ink"]}">{v} <span style="color:{T["sessiz"]};float:right">▾</span></div></label>')
    rows = [["Kadıköy", "23:00", "22:00 – 00:30 <span style='color:" + T["sessiz"] + "'>(+1 gün, aynı iş günü)</span>", "02:30"],
            ["Üsküdar", "23:00", "22:00 – 00:30", "02:30"], ["Ataşehir", "24:00", "23:00 – 01:30", "03:30"],
            ["Kartal", "22:00", "21:00 – 23:30", "01:30"], ["Bornova", "23:00", "22:00 – 00:30", "02:30"]]
    return (f'<div style="box-sizing:border-box;width:{W}px;height:{H}px;background:{T["zemin"]};font-family:{SANS};color:{T["ink"]};padding:18px 22px;'
            f'display:flex;flex-direction:column;gap:12px;overflow:hidden;border:1px solid {T["cizgi"]};border-radius:12px;box-shadow:0 18px 40px rgba(28,33,40,.14)">'
            f'<div style="display:flex;align-items:center;gap:12px">{w(18)}<div style="padding-left:14px;border-left:1px solid {T["cizgi"]};font-family:{SERIF};font-size:19px;font-weight:700">Kurulum sihirbazı</div>'
            f'<div style="margin-left:auto;font-size:12.5px;color:{T["ink2"]}">Hesap: <b>Kahve Durağı</b> · 12 şube</div></div>'
            f'<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px">'
            + st(1, "Marka ve şubeler", "12 şube · Excel", "done") + st(2, "Kapanış şablonu", "15 madde · 4 kritik", "done")
            + st(3, "Plan (saatler)", "pencere ve tolerans", "on") + st(4, "Personel ve cihazlar", "davet + kiosk", "todo") + '</div>'
            f'<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:16px;min-height:0">'
            f'<div style="display:flex;flex-direction:column;gap:10px">'
            f'{card("<div style=\'font-family:" + SERIF + ";font-size:15px;font-weight:700;margin-bottom:8px\'>Tekrar ve pencere</div><div style=\'display:grid;grid-template-columns:1fr 1fr;gap:10px\'>" + fld("Tekrar", "Her gün") + fld("Tolerans", "120 dk (sabit)") + fld("Pencere başlangıcı", "Kapanıştan 60 dk önce") + fld("Pencere bitişi", "Kapanıştan 90 dk sonra") + "</div>", "padding:12px 14px")}'
            f'{card("<div style=\'font-family:" + SERIF + ";font-size:15px;font-weight:700;margin-bottom:6px\'>Atama</div><div style=\'font-size:13.5px;line-height:1.5\'><b style=\'color:" + T["marka"] + "\'>●</b> Şubedeki herkes görür, biri tamamlasın (ilk açan alır)<br><span style=\'color:" + T["sessiz"] + "\'>○ Rol: kapanışçı &nbsp; ○ Kişi</span></div>", "padding:12px 14px")}'
            f'{card("<div style=\'font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:" + T["sessiz"] + ";margin-bottom:5px\'>Hatırlatma ve eskalasyon · v1’de sabit</div><div style=\'font-size:12.5px;line-height:1.5;color:" + T["ink2"] + "\'>Pencere açılışında ve bitişe 30 dk kala push · kaçırılan liste → şube müdürüne anında, bölge müdürüne 07:00 özeti · kritik madde → anında push, teslim olmazsa SMS · sessiz saat 23:00–07:00</div>", "padding:12px 14px;background:" + T["yuzey2"])}</div>'
            f'<div style="display:flex;flex-direction:column;gap:10px;min-width:0">'
            f'<div style="font-size:12.5px;color:{T["ink2"]}">Şube başına hesaplanan pencere — çalışma saatinden türetildi; gece yarısını aşan pencere aynı iş gününe yazılır.</div>'
            + table(["Şube", "Kapanış", "Pencere", "Tolerans sonu"], rows, size=12.5)
            + f'<div style="margin-top:auto;display:flex;gap:10px;justify-content:flex-end"><div style="padding:9px 14px;border-radius:9px;border:1.5px solid {T["cizgi"]};color:{T["ink2"]};font-size:13.5px">← Geri</div>'
            f'<div style="padding:9px 16px;border-radius:9px;background:{T["marka"]};color:#fff;font-weight:600;font-size:13.5px">Devam: personel →</div></div></div></div></div>')

# ---------------------------------------------------------------- sayfalar
def t1():
    kapak = (f'<div style="display:flex;flex-direction:column;gap:14px">'
             f'{label("Ürün tanıtım dosyası · Ekim 2026")}{h1("Şube talimatları,<br>kanıtıyla.", 46)}'
             f'{p("Çok şubeli yeme-içme zincirleri için açılış, kapanış, hijyen ve soğuk zincir listeleri: merkez bir kez kurar, listeler her gece şubelerde kendiliğinden açılır, personel fotoğraf ve ölçümle kanıtlayarak kapatır, yapamadığını sebebiyle bildirir. Merkez her sabah yalnızca aksayanı görür; denetim kaydı doğrulama kodlu PDF olarak çıkar.", 17, T["ink"], "62ch")}</div>')
    problem = (f'<div style="display:flex;flex-direction:column;gap:10px">{h2("Bugün ne oluyor")}'
               f'<div style="display:flex;gap:10px">'
               + tile("WhatsApp", "talimat, fotoğraf ve itiraz aynı akışta", T["kritik"], "mesaj kayboluyor, arşiv aranamıyor")
               + tile("“Yapıldı”", "söz, kanıt değil", T["kritik"], "kontrol = bölge müdürünün ziyareti")
               + tile("Saatler", "denetimde kayıt aramak", T["kritik"], "sıcaklık defteri sonradan doldurulabiliyor") + '</div></div>')
    kim = (f'<div style="display:flex;flex-direction:column;gap:10px">{h2("Kimin için")}'
           + table(["Rol", "Ne yapar", "Nerede"],
                   [["<b>Operasyon müdürü</b> (satın alan)", "Şablonu ve planı kurar, panoyu okur, denetim kaydını çıkarır", "Web"],
                    ["<b>Bölge müdürü</b>", "Her sabah özetle dün geceyi görür, aksiyon takip eder", "Telefon + web"],
                    ["<b>Şube müdürü</b>", "Günlük atama, aksiyon kapatma, “yapılmayacak”, personele PIN", "Telefon"],
                    ["<b>Personel</b>", "Listeyi tablet veya telefondan tamamlar, kanıtlar", "Şube tableti (kiosk)"]],
                   widths=["30%", "48%", "22%"]) + '</div>')
    icerik = (f'<div style="background:{T["yuzey"]};border:1px solid {T["cizgi"]};border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:6px">'
              f'{label("Bu dosyada")}'
              + "".join(f'<div style="display:flex;gap:10px;font-size:13.5px;line-height:1.5"><span style="color:{T["marka"]};font-weight:700;width:16px">{i}</span><span>{t}</span></div>'
                        for i, t in [(2, "Bir gecenin akışı: 22:00’den ertesi sabah 07:00’ye"), (3, "Personel tarafı — üç ekran, altı madde türü, tek kural"),
                                     (4, "Yönetici tarafı — sabah özeti, istisna panosu, sabit eskalasyon"), (5, "Kanıt ve uyum — damga, hash zinciri, denetim PDF’i, KVKK"),
                                     (6, "Kurulum, şablonlar, pilot ve yol haritası")]) + '</div>')
    return page(f'{w(26)}{kapak}{problem}{kim}{icerik}{foot(1)}', gap=20)

def t2():
    tl = [("22:00", "Pencere açıldı", "Kapanış listesi şube tabletinde belirir; pencere şubenin kapanış saatinden türetilir (−60 dk / +90 dk).", "ok"),
          ("22:58", "Emre PIN ile girdi", "Ortak tablette adına dokunur, 4 haneli PIN girer. Listeyi ilk açan alır; diğerleri “Emre yapıyor” görür.", "ok"),
          ("23:20", "Mutfak buzdolabı 6,0 °C", "Aralık dışı: fotoğraf ve not zorunlu. Kritik madde olduğu için şube ve bölge müdürüne anında bildirim; 10 dakikada okunmazsa SMS. Aksiyon #418 açıldı (4 saat vade).", "crit"),
          ("23:30", "Zemin yapılamadı", "Sebep seçildi: malzeme yok. Aksiyon #419 şube müdürüne düştü (72 saat).", "un"),
          ("23:41", "Gönderildi", "15 maddenin 13’ü geçti. Kritik madde yüzünden çalıştırma “başarısız”. Kayıt kilitlendi; sonradan değiştirilemez.", "crit"),
          ("03:30", "Tolerans doldu", "Bakırköy’de kapanış hiç başlamadı → “kaçırıldı”; şube müdürüne push. Gece kimse aranmaz.", "crit"),
          ("07:00", "Sabah özeti", "Bölge müdürü ve yöneticiye push + e-posta: kaçıran, başarısız, yapılamayan, gecikmiş aksiyon.", "ok"),
          ("08:05", "Aksiyon kapandı", "Servis geldi, conta değişti, ölçüm 3,4 °C. Not zorunlu; notlar silinmez, olay izine yazılır.", "ok")]
    def item(t, b, d, kind, last=False):
        col = T["kritik"] if kind == "crit" else (T["uyari"] if kind == "un" else T["marka"])
        line = "" if last else f'<div style="position:absolute;left:7px;top:18px;bottom:-14px;width:2px;background:{T["cizgi"]}"></div>'
        return (f'<div style="position:relative;padding-left:28px;padding-bottom:{0 if last else 14}px">{line}'
                f'<div style="position:absolute;left:0;top:4px;width:16px;height:16px;border-radius:50%;background:{col};border:3px solid {T["zemin"]}"></div>'
                f'<div style="display:flex;gap:10px;align-items:baseline"><b style="font:600 13px ui-monospace,Menlo,Consolas,monospace;color:{T["ink2"]};width:44px;flex:none">{t}</b>'
                f'<div><b style="font-size:14.5px">{b}</b><div style="font-size:13px;color:{T["ink2"]};line-height:1.45;margin-top:2px;max-width:60ch">{d}</div></div></div></div>')
    gece = "".join(item(*x, last=(i == len(tl) - 1)) for i, x in enumerate(tl))
    not_ = (f'<div style="background:{T["markaA"]};border-radius:12px;padding:12px 14px;font-size:13px;line-height:1.5;color:{T["ink2"]}">'
            f'<b style="color:{T["marka"]};font-family:{SERIF};font-size:15px;display:block;margin-bottom:3px">Gece kimse aranmaz</b>'
            f'Kaçırılan liste için şube müdürüne anında push, bölge müdürüne 07:00 özeti. Yalnızca kritik madde (sıcaklık, gaz, kasa farkı) anında bildirilir; teslim olmazsa SMS. Sessiz saat 23:00–07:00.</div>')
    return page(f'{head(2, "Bir gecenin akışı")}{h1("22:00’den ertesi sabah 07:00’ye", 30)}'
                f'{p("Kadıköy şubesinde 13 Eylül gecesi — üründeki örnek senaryo. Prototipler, basılı raporlar ve bu dosyadaki ekranlar aynı geceyi anlatır.")}'
                f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 210px;gap:18px;align-items:start">'
                f'<div style="display:flex;flex-direction:column">{gece}</div>'
                f'<div style="display:flex;flex-direction:column;gap:12px">{scaled(scr_unable(), 390, 844, 0.5)}{not_}</div></div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start">'
                f'{card("<div style=\'font-family:" + SERIF + ";font-size:15px;font-weight:700;margin-bottom:6px\'>Bugün bu gece nasıl geçerdi</div>" + "".join(f"<div style=\'font-size:13px;line-height:1.5;color:" + T["ink2"] + "\'>• " + x + "</div>" for x in ["Kapanış WhatsApp’a birkaç fotoğrafla bildirilir; 6,0 °C kimsenin dikkatini çekmez", "Deterjan bitti bilgisi sabahçıya ulaşmaz", "Bakırköy’ün hiç kapanış yapmadığı ancak ertesi gün fark edilir", "Denetimde 13 Eylül kaydı aranır, bulunamaz"]), "padding:12px 14px")}'
                f'{card("<div style=\'font-family:" + SERIF + ";font-size:15px;font-weight:700;margin-bottom:6px;color:" + T["marka"] + "\'>Talimatname’de ne oldu</div>" + "".join(f"<div style=\'font-size:13px;line-height:1.5;color:" + T["ink2"] + "\'>• " + x + "</div>" for x in ["Aralık dışı ölçüm fotoğraf ve notla kayda girdi, aksiyon açıldı, iki yönetici anında haberdar oldu", "Sabahçı açılış listesinde “dün gece” bloğunu gördü", "Kaçırılan kapanış 03:30’da şube müdürüne düştü, 07:00 özetinde merkeze", "Kayıt doğrulama kodlu PDF olarak 3 dakikada çıkıyor"]), "padding:12px 14px;border-color:" + T["marka"])}</div>{foot(2)}')

def t3():
    turler = table(["Madde türü", "Ne için", "Örnek"],
                   [["Onay", "Tek dokunuşla yapıldı", "Tezgâh dezenfekte edildi"],
                    ["Çoktan seçmeli", "Evet / Hayır / Uygun değil", "Gaz vanası kapatıldı mı?"],
                    ["Sayı + birim", "Sayılan değer", "Kasa sayımı (₺), polar madde (%)"],
                    ["Sıcaklık", "Kabul aralığı ile", "Buzdolabı 0–4 °C, dondurucu −30…−18 °C"],
                    ["Fotoğraf (1–3)", "Sonradan tartışılan işler", "Çöp alanı, kepenk, irsaliye"],
                    ["Metin · talimat", "Kısa açıklama; talimat satırı cevap istemez", "Devralan kişi · “Kasa kapanışını Kasa devri listesinde tamamlayın”"]],
                   widths=["22%", "30%", "48%"], size=12)
    kural = (f'<div style="background:{T["yuzey"]};border:2px solid {T["marka"]};border-radius:12px;padding:14px 16px">'
             f'<div style="font-family:{SERIF};font-size:17px;font-weight:700;color:{T["marka"]};margin-bottom:4px">Tek kural</div>'
             f'<div style="font-size:14px;line-height:1.5">“Hayır”, “Uygun değil” veya <b>aralık dışı</b> cevapta <b>fotoğraf ve not zorunlu</b>. Madde kritikse ayrıca aksiyon açılır (şube müdürü, 4 saat) ve çalıştırma “başarısız” sayılır.</div>'
             f'<div style="font-size:12.5px;color:{T["sessiz"]};margin-top:6px">Kural editörü yok: herkes aynı kuralı bilir. Puan bilgi amaçlıdır; başarısızlığı kritik madde belirler.</div></div>')
    ozellik = "".join([bullet("Kiosk modu.", "Ortak tablet; adına dokun, PIN gir; 2 dakika dokunulmazsa kilitlenir ve kaldığı yerden devam eder. Telefonu olmayan personele şube müdürü PIN atar."),
                       bullet("Çevrimdışı çalışır.", "Wi-Fi gidince liste cihazda devam eder; cevaplar ve fotoğraflar kuyruğa alınır (72 saat), bağlantı gelince senklenir ve zaman damgaları sunucu saatiyle düzeltilir."),
                       bullet("Kamera uygulama içinde.", "Galeriden seçim yok; fotoğrafa şube, tarih-saat ve kişi sunucuda damgalanır. Kapanış 6–8 dakika, iki dokunuşta bir madde."),
                       bullet("Açılışta “dün gece”.", "Sabahçı listeyi açtığında ilk gördüğü blok: dün gece yapılamayan ve başarısız maddeler.")])
    cap = lambda t: f'<div style="font-size:11.5px;color:{T["sessiz"]};margin-top:4px;text-align:center">{t}</div>'
    ekranlar = (f'<div style="display:flex;gap:12px;align-items:flex-start">'
                f'<div>{scaled(B.scr_kiosk(), 390, 844, 0.335)}{cap("Kapanış listesi")}</div>'
                f'<div>{scaled(B.scr_temp(), 390, 844, 0.335)}{cap("Sıcaklık · aralık dışı")}</div>'
                f'<div>{scaled(scr_unable(), 390, 844, 0.335)}{cap("Yapılamadı")}</div>'
                f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:10px">{kural}{turler}</div></div>')
    return page(f'{head(3, "Personel tarafı")}{h1("Gece vardiyasının altı dakikası", 30)}'
                f'{p("Personel için tek akış: listeyi aç, maddeleri işaretle, kanıtla, gönder. Ekranlar düşük segment Android tablette ve telefonda aynı; dokunma alanları eldivenle kullanılacak büyüklükte.")}'
                f'{ekranlar}'
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px 20px">{ozellik}</div>{foot(3)}', gap=12)

def t4():
    esk = (f'<div style="background:{T["yuzey"]};border:1px solid {T["cizgi"]};border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:8px">'
           f'{label("Sabit eskalasyon — v1’de ayar yok")}'
           + "".join(f'<div style="display:flex;gap:9px;align-items:flex-start;font-size:13px;line-height:1.45">'
                     f'<div style="width:9px;height:9px;border-radius:50%;background:{c};margin-top:5px;flex:none"></div><div><b>{t}</b> {d}</div></div>'
                     for t, d, c in [("Kritik madde başarısız →", "şube ve bölge müdürüne anında push; 10 dakikada teslim/okunma yoksa SMS. Sessiz saatten muaf.", T["kritik"]),
                                     ("Kaçırılan liste →", "şube müdürüne anında push; bölge müdürü ve yönetici 07:00 sabah özetinde görür.", T["kritik"]),
                                     ("Yapılamadı →", "şube müdürüne bildirim ve aksiyon (orta, 72 saat).", T["uyari"]),
                                     ("Gecikmiş aksiyon →", "sabah özetinde listelenir.", T["uyari"]),
                                     ("Sessiz saat 23:00–07:00:", "yöneticiye yalnızca kritik bildirim gider.", T["marka"])]) + '</div>')
    kpi = (f'<div style="display:flex;gap:8px">' + tile("%81", "zamanında tamamlanma", T["marka"], "aylık özet")
           + tile("%97", "fotoğraf zorunlu maddede kanıt", T["marka"]) + tile("3 dk", "denetim kaydı → PDF", T["ink"]) + '</div>')
    return page(f'{head(4, "Yönetici tarafı")}{h1("Her sabah iki dakika", 30)}'
                f'{p("Yönetici ürünü taramaz; ürün ona aksayanı getirir. Sabah özeti push ve e-posta olarak gelir; panonun varsayılanı istisna görünümüdür — sorun yoksa sayfa bunu tek cümleyle söyler.")}'
                f'<div style="display:flex;gap:14px;align-items:flex-start">{scaled(B.scr_morning(), 390, 844, 0.49)}'
                f'<div style="display:flex;flex-direction:column;gap:10px;flex:1;min-width:0">{scaled(B.scr_pano(1200, 760), 1200, 760, 0.42)}{esk}</div></div>'
                f'{kpi}{foot(4)}', gap=15)

def t5():
    zincir = ["Fotoğraf uygulama içinden çekilir — galeri kapalı",
              "Sunucu damgalar: şube · tarih-saat · kullanıcı · cihaz (ham dosya ayrıca saklanır)",
              "Dosyanın SHA-256 özeti cevaba bağlanır",
              "Her olay ekle-yalnız günlüğe yazılır; kayıtlar önceki olayın özetiyle zincirlenir",
              "Gönderilen kayıt değişmez; düzeltme ayrı “ek” kaydıdır",
              "PDF doğrulama kodu ve üretim zamanı taşır"]
    akis = "".join(f'<div style="display:flex;gap:10px;align-items:flex-start;font-size:13.5px;line-height:1.45">'
                   f'<div style="width:20px;height:20px;border-radius:50%;background:{T["markaA"]};color:{T["marka"]};font-weight:700;font-size:11px;display:flex;align-items:center;justify-content:center;flex:none;margin-top:2px">{i+1}</div>{t}</div>'
                   for i, t in enumerate(zincir))
    kvkk = table(["KVKK", "Talimatname’de"],
                 [["Kişi bazlı performans puanı", "<b>Yok.</b> Skor şube ve bölge düzeyinde; kişi düzeyinde yalnızca gecikme ve eksik görünür"],
                  ["Biyometrik veri", "<b>İşlenmez.</b> Kimlik telefon + OTP veya kioskta PIN (Kurul 2026/921)"],
                  ["Konum", "Yalnızca madde tamamlanma anında tek nokta; izin verilmezse kayıt “konum yok” notuyla sürer"],
                  ["Barındırma", "Türkiye’deki yerel bulut; alt işleyen listesi sözleşme ekinde"],
                  ["Saklama", "Kanıt dosyaları 24 ay, sonra otomatik silinir; iş kaydı kişi maskelenerek kalır"],
                  ["Belgeler", "Personel aydınlatma metni ve veri işleme sözleşmesi taslakları hazır (avukat onayından geçer)"]],
                 widths=["28%", "72%"], size=12.5)
    return page(f'{head(5, "Kanıt ve uyum")}{h1("Kayıt sonradan değiştirilemez", 30)}'
                f'{p("Ürünün değeri kanıtın sonradan değiştirilememesine dayanır: “fotoğrafı dün çekmiş” itirazı teknik olarak cevaplanır. Cihaz saati değil sunucu zamanı esastır.")}'
                f'<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:16px;align-items:start">'
                f'{card("<div style=\'font-family:" + SERIF + ";font-size:16px;font-weight:700;margin-bottom:8px\'>Kanıt zinciri</div>" + akis, "padding:14px 16px")}'
                f'<div style="display:flex;flex-direction:column;gap:8px">{label("Çalıştırma raporu — denetimde verilen belge")}{scaled(scr_detail(1200, 760), 1200, 760, 0.40)}</div></div>'
                f'{kvkk}{foot(5)}', gap=15)

def t6():
    sablon = table(["Hazır şablon", "Tekrar", "Madde"],
                   [["Kapanış (kafe / hızlı servis)", "Her gün, kapanış −60 dk", "15"], ["Açılış", "Her gün, açılış −45 dk", "13"],
                    ["Saatlik tuvalet ve hijyen", "10:00–22:00, her 2 saat", "7"], ["Soğuk zincir sıcaklık kaydı", "08:00 · 14:00 · 20:00", "5"],
                    ["Haftalık derin temizlik", "Pazartesi", "10"], ["Fritöz yağı kontrolü", "Her gün 15:00–17:00", "7"],
                    ["Kasa devri", "Vardiya ve kapanış", "7"], ["Teslimat kabul", "Tedarik günleri", "9"]],
                   widths=["52%", "33%", "15%"], size=12.5)
    pilot = (f'<div style="background:{T["yuzey"]};border:2px solid {T["marka"]};border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:7px">'
             f'<div style="font-family:{SERIF};font-size:18px;font-weight:700;color:{T["marka"]}">8 haftalık pilot</div>'
             f'{p("Seçilen 5–15 şubede kapanış ve soğuk zincir listeleriyle başlanır. Yerinde kurulum bir gün: kiosk, PIN’ler, şablon uyarlaması, şube müdürüne 30 dakika ve personele 10 dakika eğitim. Haftalık 30 dakikalık geri bildirim görüşmesi.", 13)}'
             f'<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:2px">'
             + "".join(f'<div style="background:{T["markaA"]};border-radius:10px;padding:9px 11px"><div style="font-family:{SERIF};font-size:19px;font-weight:700;color:{T["marka"]}">{n}</div><div style="font-size:11.5px;color:{T["ink2"]};line-height:1.3">{l}</div></div>'
                       for n, l in [("≥ %80", "liste pencere içinde tamamlanır"), ("≥ %95", "fotoğraf zorunlu maddede kanıt"), ("≥ %80", "kritik aksiyon vadesinde kapanır")])
             + f'</div><div style="font-size:12px;color:{T["sessiz"]}">4. hafta sonunda birlikte ölçülür; ölçütler tutarsa yıllık sözleşme konuşulur, tutmazsa kalan aylar iade edilir. Şube başına aylık ücret görüşmede belirlenir.</div></div>')
    yol = table(["Sürüm", "İçerik"],
                [["<b>v1</b> — ilk sürüm", "4 rol · 6 madde türü + talimat · tek kural · 8 şablon · kiosk ve çevrimdışı · sabit eskalasyon ve 07:00 özeti · istisna panosu · aylık tek sayfa · sıcaklık günlüğü · doğrulama kodlu PDF"],
                 ["<b>v1.1</b> — pilot sonrası", "Madde kütüphanesi ve işletme türü paketleri · duyuru ve okundu onayı · koşul editörü · ayrıntılı raporlar · denetim izi ekranı · ayarlar paneli · 2FA"],
                 ["<b>v2</b>", "Franchise marka kütüphanesi · başka sektör paketleri · entegrasyonlar (POS, İK) · salt okunur API"]],
                widths=["20%", "80%"], size=12.5)
    iletisim = (f'<div style="display:flex;align-items:center;justify-content:space-between;gap:16px;border-top:1px solid {T["cizgi"]};padding-top:12px">'
                f'{w(22)}<div style="font-size:13px;color:{T["ink2"]};text-align:right;line-height:1.5">[Ad Soyad] · [telefon]<br>[e-posta] · [alan adı]</div></div>')
    return page(f'{head(6, "Kurulum, şablonlar, pilot")}{h1("Bir saatte kurulur, bu gece başlar", 30)}'
                f'<div style="display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:16px;align-items:start">'
                f'<div style="display:flex;flex-direction:column;gap:8px">{label("Kurulum sihirbazı — dört adım")}{scaled(scr_wizard(1200, 760), 1200, 760, 0.33)}</div>'
                f'<div style="display:flex;flex-direction:column;gap:8px">{label("Hazır şablonlar — kopyalanır, düzenlenir")}{sablon}</div></div>'
                f'{pilot}{yol}{iletisim}{foot(6, "Talimatname çalışma adıdır; veriler örnektir.")}', gap=14)

# ---------------------------------------------------------------- üretim
PAGES = {"Main.dc.html": t1, "T2.dc.html": t2, "T3.dc.html": t3, "T4.dc.html": t4, "T5.dc.html": t5, "T6.dc.html": t6}
SCREENS = {"Yapilamadi.dc.html": scr_unable, "Detay.dc.html": scr_detail, "Sihirbaz.dc.html": scr_wizard}
OUTDIR = os.path.join(HERE, "tanitim")

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    for name, fn in list(PAGES.items()) + list(SCREENS.items()):
        open(os.path.join(OUTDIR, name), "w", encoding="utf-8").write(B.dc(fn()))
    ab = []
    for i, name in enumerate(PAGES):
        ab.append({"file": name, "title": f"Tanıtım · sayfa {i+1}", "x": i * 880, "y": 0, "w": 794, "h": 1123, "print": "fixed"})
    for i, (name, t) in enumerate([("Yapilamadi.dc.html", "Ekran · yapılamadı"), ("Detay.dc.html", "Ekran · çalıştırma detayı (web)"), ("Sihirbaz.dc.html", "Ekran · kurulum sihirbazı (web)")]):
        ab.append({"file": name, "title": t, "x": i * 1320, "y": 1280, "w": 390 if i == 0 else 1200, "h": 844 if i == 0 else 760})
    json.dump({"artboards": ab, "launch": {"view": "canvas"}}, open(os.path.join(OUTDIR, "canvas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    css = ("body{margin:0;background:#e9e6de;font-family:" + SANS + "} .sheet{margin:18px auto;box-shadow:0 10px 30px rgba(28,33,40,.14);width:794px} "
           "@media print{body{background:#fff}.sheet{margin:0;box-shadow:none}.sheet+.sheet{break-before:page}@page{size:A4;margin:0}}")
    sheets = "".join(f'<div class="sheet">{fn()}</div>' for fn in PAGES.values())
    html = (f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>Talimatname tanıtım dosyası</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bitter:wght@700&display=swap">'
            f'<style>{css}</style></head><body>{sheets}</body></html>')
    out = os.path.join(HERE, "talimatname-tanitim.html"); open(out, "w", encoding="utf-8").write(html)

    # yayın sürümü: dar ekranda sayfa ölçeklenir (A4 yeniden akmaz)
    css2 = ("body{margin:0;background:#e9e6de;font-family:" + SANS + "}"
            ".page{width:100%;display:flex;justify-content:center;padding:14px 8px}"
            ".box{width:794px;transform-origin:top center;box-shadow:0 10px 30px rgba(28,33,40,.14)}"
            "@media print{body{background:#fff}.page{padding:0}.box{transform:none!important;box-shadow:none}"
            ".page+.page{break-before:page}@page{size:A4;margin:0}}")
    js = ("<script>(function(){function f(){var w=Math.min(document.documentElement.clientWidth-16,794);var s=w/794;"
          "document.querySelectorAll('.page').forEach(function(pg){var b=pg.querySelector('.box');b.style.transform='scale('+s+')';"
          "pg.style.height=(1123*s+28)+'px';});}f();addEventListener('resize',f);})();</script>")
    sheets2 = "".join(f'<div class="page"><div class="box">{fn()}</div></div>' for fn in PAGES.values())
    html2 = (f'<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
             f'<title>Talimatname Tanıtım Dosyası</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bitter:wght@700&display=swap">'
             f'<style>{css2}</style>{sheets2}{js}')
    out2 = os.path.join(HERE, "talimatname-tanitim-sayfa.html"); open(out2, "w", encoding="utf-8").write(html2)
    print("ok:", len(PAGES), "sayfa,", len(SCREENS), "ekran →", OUTDIR, "+", os.path.basename(out))
    if "--pdf" in sys.argv:
        edge = next((x for x in [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"] if os.path.exists(x)), None)
        if not edge: print("Edge yok"); return
        pdf = out.replace(".html", ".pdf")
        if os.path.exists(pdf): os.remove(pdf)
        prof = tempfile.mkdtemp(prefix="talimatname-pdf-")
        subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={prof}", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", "--virtual-time-budget=8000", "file:///" + out.replace(os.sep, "/")],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
        for _ in range(160):
            if os.path.exists(pdf) and os.path.getsize(pdf) > 10_000: break
            time.sleep(0.5)
        print(pdf, "ok" if os.path.exists(pdf) else "HATA")

if __name__ == "__main__":
    main()
