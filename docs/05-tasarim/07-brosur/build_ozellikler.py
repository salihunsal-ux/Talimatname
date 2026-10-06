# -*- coding: utf-8 -*-
"""Talimatname özellik föyü (A4, 5 sayfa): yol haritasındaki her satırın kısa açıklaması ve ekranı.
v1 özellikleri ekran görseliyle; v1.1 ve v2 yalnızca açıklamayla (ekranları henüz çizilmedi).
Üretir: ozellikler/*.dc.html (sayfalar + yeni ekranlar), canvas.json, talimatname-ozellikler.html (+ --pdf),
talimatname-ozellikler-sayfa.html (yayın sürümü). Ortak bileşenler build_brosur.py'den."""
import os, sys, subprocess, tempfile, time, json
import build_brosur as B
import build_tanitim as TT

T, SANS, SERIF = B.T, B.SANS, B.SERIF
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "ozellikler")
w, card, chip, box, phone, scaled = B.wordmark, B.card, B.chip, B.box, B.phone, B.scaled
from build_brosur import h1, h2, h3, mp as p, label, table, INK_BAND

SAYFA = 10

def page(inner, gap=14, bg=None):
    return ('<div style="box-sizing:border-box;width:794px;height:1123px;background:' + (bg or T["zemin"]) + ';font-family:' + SANS + ';color:' + T["ink"] +
            ';padding:36px 44px 24px;display:flex;flex-direction:column;gap:' + str(gap) + 'px;overflow:hidden">' + inner + '</div>')

def head(title):
    return ('<div style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid ' + T["cizgi"] + ';padding-bottom:9px">'
            + w(17) + '<div style="font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:' + T["sessiz"] + '">' + title + '</div></div>')

def foot(no, note=""):
    return ('<div style="margin-top:auto;display:flex;align-items:center;justify-content:space-between;border-top:1px solid ' + T["cizgi"] +
            ';padding-top:9px;font-size:10.5px;color:' + T["sessiz"] + '"><span>' + (note or "Ekranlar ürün tasarımındandır; veriler örnektir.") +
            '</span><span>Talimatname · özellik föyü · ' + str(no) + ' / ' + str(SAYFA) + '</span></div>')

# ---------------------------------------------------------------- kart bileşeni
def rozet(t, kind="n"):
    bg, fg = T["yuzey2"], T["ink2"]
    if kind == "mobil": bg, fg = T["markaA"], T["marka"]
    if kind == "web": bg, fg = "#e2e8ef", "#3c566e"
    if kind == "pdf": bg, fg = T["uyariA"], T["uyari"]
    if kind == "taslak": bg, fg = "#ece9f3", "#5b4b86"
    return ('<span style="display:inline-block;padding:2px 9px;border-radius:999px;font-size:10.5px;font-weight:700;'
            'letter-spacing:.04em;text-transform:uppercase;background:' + bg + ';color:' + fg + ';white-space:nowrap">' + t + '</span>')

def bullets(items):
    out = ""
    for t in items:
        out += ('<div style="display:flex;gap:8px;align-items:flex-start">'
                '<span style="width:5px;height:5px;border-radius:50%;background:' + T["marka"] + ';margin-top:6px;flex:none"></span>'
                '<span style="font-size:12px;line-height:1.45;color:' + T["ink2"] + '">' + t + '</span></div>')
    return '<div style="display:flex;flex-direction:column;gap:4px;margin-top:7px">' + out + '</div>'

def kart(no, baslik, nerede, kind, ozet, liste, gorsel, cap, sol_w=None):
    gw = ('width:' + str(sol_w) + 'px;') if sol_w else ""
    sol = ('<div style="flex:none;' + gw + 'display:flex;flex-direction:column;gap:6px;align-items:flex-start">' + gorsel +
           '<div style="font-size:10.5px;color:' + T["sessiz"] + ';line-height:1.3">' + cap + '</div></div>')
    sag = ('<div style="flex:1;min-width:0">'
           '<div style="display:flex;align-items:center;gap:9px;flex-wrap:wrap">'
           '<span style="font-family:' + SERIF + ';font-size:19px;font-weight:700;color:' + T["marka"] + ';line-height:1">' + str(no) + '</span>'
           '<span style="font-family:' + SERIF + ';font-size:16.5px;font-weight:700;line-height:1.2">' + baslik + '</span>' + rozet(nerede, kind) + '</div>'
           '<div style="font-size:13px;line-height:1.5;color:' + T["ink2"] + ';margin-top:5px;max-width:62ch">' + ozet + '</div>'
           + bullets(liste) + '</div>')
    return ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:13px;padding:13px 15px;display:flex;gap:16px;align-items:flex-start">'
            + sol + sag + '</div>')

# ---------------------------------------------------------------- yeni ekranlar
def scr_sablon(W=1200, H=760):
    def tpl(ad, meta, surum, durum="yayında", aktif=False):
        d = chip(durum, "ok" if durum == "yayında" else "")
        return ('<div style="background:' + T["yuzey"] + ';border:1.5px solid ' + (T["marka"] if aktif else T["cizgi"]) + ';border-radius:11px;padding:11px 13px">'
                '<div style="display:flex;align-items:center;justify-content:space-between;gap:8px"><b style="font-size:14px">' + ad + '</b>' + d + '</div>'
                '<div style="font-size:12px;color:' + T["ink2"] + ';margin-top:3px">' + meta + '</div>'
                '<div style="font-size:11.5px;color:' + T["sessiz"] + ';margin-top:2px">' + surum + '</div></div>')
    kartlar = "".join([
        tpl("Kapanış (kafe / hızlı servis)", "15 madde + 1 talimat · 4 kritik · 6–8 dk", "sürüm 3 · 12 planda", aktif=True),
        tpl("Açılış", "13 madde · 2 kritik · 5 dk", "sürüm 2 · 12 planda"),
        tpl("Saatlik tuvalet ve hijyen kontrolü", "7 madde · kritik yok · 1–2 dk", "sürüm 1 · 9 planda"),
        tpl("Soğuk zincir sıcaklık kaydı", "5 ölçüm + 1 talimat · tamamı kritik · 2 dk", "sürüm 2 · 12 planda"),
        tpl("Haftalık derin temizlik", "10 madde · 1 kritik · 4 dk kayıt", "sürüm 1 · 12 planda"),
        tpl("Fritöz yağı kontrolü ve değişimi", "fritöz başına 3 madde · 1 kritik · 3 dk", "sürüm 1 · 5 planda"),
        tpl("Kasa devri", "7 madde · 1 kritik · 4 dk", "sürüm 1 · 12 planda"),
        tpl("Teslimat kabul", "9 madde · 3 kritik · 4 dk", "taslak", "taslak"),
    ])
    tur = lambda ad, ornek: ('<div style="display:flex;gap:10px;align-items:flex-start;padding:7px 0;border-bottom:1px solid ' + T["cizgi"] + '">'
                             '<div style="width:92px;flex:none;font-size:12.5px;font-weight:600">' + ad + '</div>'
                             '<div style="flex:1;font-size:12px;color:' + T["ink2"] + ';line-height:1.4">' + ornek + '</div></div>')
    turler = (tur("Onay", "Evet / Hayır — “Gaz vanası kapatıldı”")
              + tur("Çoktan seçmeli", "Yapıldı · Uygun değil · Yapılamadı")
              + tur("Sayı", "“Kasa farkı (₺)” · birim ve aralık")
              + tur("Sıcaklık", "“Mutfak buzdolabı” · kabul aralığı 0–4 °C")
              + tur("Metin", "“Devralan kişi”, kısa not")
              + tur("Fotoğraf", "1–3 kare · yalnızca uygulama kamerası"))
    isaret = ('<div style="background:' + T["yuzey2"] + ';border-radius:10px;padding:10px 12px;font-size:12px;line-height:1.5;color:' + T["ink2"] + '">'
              '<b>Madde işaretleri:</b> <b style="color:' + T["ink"] + '">Z</b> zorunlu · <b style="color:' + T["ink"] + '">F</b> fotoğraf zorunlu · '
              '<b style="color:' + T["kritik"] + '">K</b> kritik (gıda güvenliği, iş güvenliği, para). Kritik madde başarısızsa liste “başarısız” sayılır ve aksiyon açılır.</div>')
    return ('<div style="box-sizing:border-box;width:' + str(W) + 'px;height:' + str(H) + 'px;background:' + T["zemin"] + ';font-family:' + SANS + ';color:' + T["ink"] +
            ';padding:18px 22px;display:flex;flex-direction:column;gap:12px;overflow:hidden;border:1px solid ' + T["cizgi"] + ';border-radius:12px">'
            '<div style="display:flex;align-items:center;gap:12px">' + w(18) +
            '<div style="padding-left:14px;border-left:1px solid ' + T["cizgi"] + ';font-family:' + SERIF + ';font-size:19px;font-weight:700">Şablonlar</div>'
            '<div style="margin-left:auto;display:flex;gap:8px;align-items:center">'
            '<div style="padding:6px 10px;border:1.5px solid ' + T["cizgi"] + ';border-radius:8px;font-size:13px;background:' + T["yuzey"] + '">Kütüphane ▾</div>'
            '<div style="padding:7px 13px;border-radius:9px;background:' + T["marka"] + ';color:#fff;font-weight:600;font-size:13px">Yeni şablon</div></div></div>'
            '<div style="display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:16px;min-height:0">'
            '<div style="display:flex;flex-direction:column;gap:9px"><div style="font-size:12.5px;color:' + T["ink2"] + '">'
            '8 hazır şablon kurulumda gelir; kopyalayıp şubenize göre düzenlersiniz. Yayındaki sürüm değişmeden kalır, düzenleme yeni sürüm açar.</div>'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">' + kartlar + '</div></div>'
            '<div style="display:flex;flex-direction:column;gap:10px">'
            + card('<div style="font-family:' + SERIF + ';font-size:15px;font-weight:700;margin-bottom:4px">Altı madde türü + talimat satırı</div>' + turler, "padding:12px 14px")
            + isaret + '</div></div></div>')

def scr_offline():
    banner = ('<div style="display:flex;gap:9px;align-items:center;background:' + T["uyariA"] + ';border-bottom:1px solid ' + T["uyari"] + ';padding:10px 16px">'
              '<div style="width:22px;height:22px;border-radius:50%;background:' + T["uyari"] + ';color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;flex:none">!</div>'
              '<div style="font-size:12.5px;line-height:1.35;color:' + T["ink"] + '"><b>Çevrimdışı.</b> Liste cihazda devam ediyor; 3 kayıt kuyrukta bekliyor.</div></div>')
    bottom = ('<div style="padding:12px 16px 20px;border-top:1px solid ' + T["cizgi"] + ';background:' + T["zemin"] + '">'
              '<div style="display:flex;align-items:center;justify-content:center;gap:8px;min-height:52px;border-radius:12px;background:' + T["ink"] + ';color:#fff;font-weight:600;font-size:16px">Gönder — bağlantı gelince iletilecek</div>'
              '<div style="font-size:12px;color:' + T["sessiz"] + ';margin-top:6px;text-align:center">Kuyruk 72 saat saklanır · damga sunucu saatiyle düzeltilir</div></div>')
    return phone(B.phone_header("Emre T.", "Kadıköy · Cts 13 Eyl") + banner + B.kiosk_list_body() + bottom)

def scr_bayrak(W=900, H=520):
    def ph(cap, flag=None, fc=None):
        f = ''
        if flag:
            f = ('<div style="position:absolute;left:5px;top:5px;background:' + (fc or T["uyari"]) + ';color:#fff;border-radius:999px;'
                 'padding:2px 8px;font-size:10px;font-weight:700">' + flag + '</div>')
        return ('<div><div style="aspect-ratio:4/3;border-radius:8px;background:repeating-linear-gradient(135deg,#dfe3e8 0 9px,#eef1f4 9px 18px);position:relative;overflow:hidden;border:1px solid ' + T["cizgi"] + '">' + f +
                '<div style="position:absolute;left:0;right:0;bottom:0;background:rgba(28,33,40,.84);color:#fff;font:9px/1.3 ui-monospace,Menlo,Consolas,monospace;padding:3px 5px">Kadıköy · 13.09 · Emre T.</div></div>'
                '<div style="font-size:10.5px;color:' + T["sessiz"] + ';margin-top:3px">' + cap + '</div></div>')
    uyari_sat = lambda t, d, c: ('<div style="display:flex;gap:9px;align-items:flex-start;padding:6px 0;border-bottom:1px solid ' + T["cizgi"] + '">'
                                 '<span style="width:9px;height:9px;border-radius:2px;background:' + c + ';margin-top:4px;flex:none"></span>'
                                 '<div style="font-size:12px;line-height:1.4"><b>' + t + '</b> <span style="color:' + T["ink2"] + '">' + d + '</span></div></div>')
    red = ('<div style="background:' + T["kritikA"] + ';border:1px solid ' + T["kritik"] + ';border-radius:11px;padding:11px 13px;display:flex;gap:10px;align-items:flex-start">'
           + box("crit") + '<div style="font-size:12.5px;line-height:1.45"><b style="color:' + T["kritik"] + '">Yükleme reddedildi.</b> '
           'Bu fotoğraf daha önce gönderildi (13.09 · 23:06 · madde 2). Yeniden çekin.<div style="color:' + T["sessiz"] + ';font-size:11px;margin-top:3px">'
           'Dosya özeti (SHA-256) eşleşti · deneme olay izine yazıldı</div></div></div>')
    return ('<div style="box-sizing:border-box;width:' + str(W) + 'px;height:' + str(H) + 'px;background:' + T["zemin"] + ';font-family:' + SANS + ';color:' + T["ink"] +
            ';padding:16px 20px;display:flex;flex-direction:column;gap:11px;overflow:hidden;border:1px solid ' + T["cizgi"] + ';border-radius:12px">'
            '<div style="display:flex;align-items:center;gap:12px">' + w(17) +
            '<div style="padding-left:12px;border-left:1px solid ' + T["cizgi"] + ';font-family:' + SERIF + ';font-size:17px;font-weight:700">Kanıtlar · Kadıköy · Kapanış · 13 Eylül</div>'
            '<div style="margin-left:auto">' + chip("şüpheli kanıt filtresi açık", "warn") + '</div></div>'
            '<div style="display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:14px;min-height:0">'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px;align-content:start">'
            + ph("2 · Kahve makinesi · 23:06") + ph("4 · Buzdolabı · 23:20", "konum", T["uyari"])
            + ph("12 · Çöp alanı · 23:33", "cihaz saati", T["uyari"]) + ph("15 · Kepenk · 23:39") + '</div>'
            '<div style="display:flex;flex-direction:column;gap:9px;min-width:0">' + red
            + card('<div style="font-size:10px;letter-spacing:.07em;text-transform:uppercase;color:' + T["sessiz"] + ';font-weight:700;margin-bottom:4px">Bu çalıştırmadaki bayraklar</div>'
                   + uyari_sat("Konum şube dışında", "— 420 m · madde 4", T["uyari"])
                   + uyari_sat("Cihaz saati farkı", "— 25 dk ileri; damga sunucu saatiyle düzeltildi · madde 12", T["uyari"])
                   + uyari_sat("Galeriden yükleme denemesi", "— reddedildi, kamera açıldı", T["kritik"]), "padding:11px 13px")
            + '<div style="background:' + T["yuzey2"] + ';border-radius:10px;padding:10px 12px;font-size:11.5px;line-height:1.45;color:' + T["ink2"] + '">'
            'Bayrak bir suçlama değil, <b>incelemeye çağrıdır</b>: panoda filtrelenir, çalıştırma PDF’inde görünür, kişi puanına dönüşmez.</div></div></div></div>')

def scr_belge(W=1200, H=760):
    kpi = lambda n, l, c: ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:12px;padding:12px 14px">'
                           '<div style="font-family:' + SERIF + ';font-size:26px;font-weight:700;color:' + c + ';line-height:1.1">' + n + '</div>'
                           '<div style="font-size:12px;color:' + T["sessiz"] + ';margin-top:3px">' + l + '</div></div>')
    def tr(sube, belge, bitis, kalan, kim, durum, last=False):
        bb = "0" if last else "1px solid " + T["cizgi"]
        c = chip("süresi geçti", "crit") if durum == "gecti" else chip("7 gün", "warn") if durum == "yakin" else chip("güncel", "ok")
        kc = T["kritik"] if durum == "gecti" else T["uyari"] if durum == "yakin" else T["ink2"]
        return ('<tr><td style="padding:8px 10px;border-bottom:' + bb + ';font-weight:600">' + sube + '</td>'
                '<td style="padding:8px 10px;border-bottom:' + bb + '">' + belge + '</td>'
                '<td style="padding:8px 10px;border-bottom:' + bb + ';white-space:nowrap">' + bitis + '</td>'
                '<td style="padding:8px 10px;border-bottom:' + bb + ';color:' + kc + ';font-weight:600;white-space:nowrap">' + kalan + '</td>'
                '<td style="padding:8px 10px;border-bottom:' + bb + ';color:' + T["ink2"] + '">' + kim + '</td>'
                '<td style="padding:8px 10px;border-bottom:' + bb + '">' + c + '</td></tr>')
    rows = (tr("Kadıköy", "Yangın tüpü dolumu", "30 Eyl 2026", "4 gün geçti", "Ayşe K.", "gecti")
            + tr("Bornova", "Su deposu temizliği", "2 Eki 2026", "2 gün geçti", "Deniz A.", "gecti")
            + tr("Bakırköy", "Baca temizliği", "11 Eki 2026", "7 gün", "Mehmet T.", "yakin")
            + tr("Şişli", "Portör muayenesi · 3 kişi", "24 Eki 2026", "20 gün", "Ayşe K.", "ok")
            + tr("Ataşehir", "Periyodik elektrik kontrolü", "15 Ara 2026", "72 gün", "Bölge · Murat D.", "ok")
            + tr("Kartal", "Hijyen eğitimi belgesi", "3 Oca 2027", "91 gün", "Ayşe K.", "ok", last=True))
    th = "".join('<th style="text-align:left;padding:8px 10px;font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:' + T["sessiz"] +
                 ';background:' + T["yuzey2"] + ';border-bottom:1px solid ' + T["cizgi"] + '">' + h + '</th>'
                 for h in ["Şube", "Belge", "Geçerlilik bitişi", "Kalan", "Sorumlu", "Durum"])
    tablo = ('<div style="border:1px solid ' + T["cizgi"] + ';border-radius:10px;overflow:hidden;background:' + T["yuzey"] + '">'
             '<table style="border-collapse:collapse;width:100%;font-size:13px"><thead><tr>' + th + '</tr></thead><tbody>' + rows + '</tbody></table></div>')
    dosya = ('<div style="display:flex;gap:10px;align-items:flex-start">'
             '<div style="width:62px;height:82px;background:' + T["yuzey2"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:6px;flex:none;padding:6px;display:flex;flex-direction:column;gap:3px">'
             + "".join('<div style="height:4px;background:' + T["cizgi"] + ';border-radius:2px;width:' + x + '%"></div>' for x in ["90", "70", "85", "60", "80"])
             + '<div style="margin-top:auto;font-size:6px;color:' + T["sessiz"] + '">PDF · 1,2 MB</div></div>'
             '<div style="font-size:12px;line-height:1.5;color:' + T["ink2"] + '"><b style="color:' + T["ink"] + '">yangin-tupu-dolum-2025.pdf</b><br>'
             'Yüklendi 12 Eki 2025 · Ayşe K.<br>Sunucu damgası ve SHA-256 özeti bağlı</div></div>')
    panel = ('<div style="display:flex;flex-direction:column;gap:10px;min-width:0">'
             + card('<div style="display:flex;align-items:center;justify-content:space-between;gap:8px">'
                    '<b style="font-family:' + SERIF + ';font-size:15px">Kadıköy · Yangın tüpü dolumu</b>' + chip("süresi geçti", "crit") + '</div>'
                    '<div style="font-size:12.5px;color:' + T["ink2"] + ';margin-top:5px;line-height:1.5">Tür: yangın tüpü dolum · Ekipman: 4 tüp (mutfak 2, salon 1, depo 1)<br>'
                    'Geçerlilik bitişi <b style="color:' + T["kritik"] + '">30 Eyl 2026</b> · Sorumlu: Ayşe K.</div>'
                    '<div style="margin-top:8px">' + dosya + '</div>'
                    '<div style="margin-top:9px;background:' + T["kritikA"] + ';border-radius:9px;padding:9px 11px;font-size:12px;line-height:1.45;color:' + T["ink2"] + '">'
                    '<b style="color:' + T["kritik"] + '">Aksiyon #431 açık</b> — tarih geçtiğinde otomatik açıldı, vade 7 gün. Şube “belge eksik” işaretli.</div>'
                    '<div style="display:flex;gap:8px;margin-top:10px">'
                    '<div style="padding:8px 13px;border-radius:9px;background:' + T["marka"] + ';color:#fff;font-weight:600;font-size:13px">Yeni belge yükle</div>'
                    '<div style="padding:8px 13px;border-radius:9px;border:1.5px solid ' + T["cizgi"] + ';font-size:13px;color:' + T["ink2"] + '">Sorumluyu değiştir</div></div>', "padding:12px 14px")
             + '<div style="background:' + T["yuzey2"] + ';border-radius:11px;padding:11px 13px;font-size:12px;line-height:1.5;color:' + T["ink2"] + '">'
             '<b>Uyarı takvimi:</b> bitişe 30 ve 7 gün kala sorumluya ve şube müdürüne bildirim; tarih geçince aksiyon açılır. '
             'Dönem PDF’i zincir genelindeki tüm belgeleri doğrulama koduyla listeler.</div></div>')
    return ('<div style="box-sizing:border-box;width:' + str(W) + 'px;height:' + str(H) + 'px;background:' + T["zemin"] + ';font-family:' + SANS + ';color:' + T["ink"] +
            ';padding:18px 22px;display:flex;flex-direction:column;gap:12px;overflow:hidden;border:1px solid ' + T["cizgi"] + ';border-radius:12px">'
            '<div style="display:flex;align-items:center;gap:12px">' + w(18) +
            '<div style="padding-left:14px;border-left:1px solid ' + T["cizgi"] + ';font-family:' + SERIF + ';font-size:19px;font-weight:700">Belge takvimi</div>'
            '<div style="margin-left:auto;display:flex;gap:8px;align-items:center">'
            '<div style="padding:6px 10px;border:1.5px solid ' + T["cizgi"] + ';border-radius:8px;font-size:13px;background:' + T["yuzey"] + '">Tüm şubeler ▾</div>'
            '<div style="padding:6px 10px;border:1.5px solid ' + T["marka"] + ';border-radius:8px;font-size:13px;background:' + T["markaA"] + ';color:' + T["marka"] + ';font-weight:600">30 gün içinde ve geçmişler</div>'
            '<div style="padding:7px 13px;border-radius:9px;background:' + T["ink"] + ';color:#fff;font-weight:600;font-size:13px">Dönem PDF’i</div></div></div>'
            '<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px">'
            + kpi("2", "süresi geçmiş belge", T["kritik"]) + kpi("3", "30 gün içinde bitiyor", T["uyari"])
            + kpi("41", "güncel belge", T["marka"]) + kpi("2", "“belge eksik” şube", T["kritik"]) + '</div>'
            '<div style="display:grid;grid-template-columns:minmax(0,1.45fr) minmax(0,1fr);gap:16px;min-height:0">'
            '<div style="display:flex;flex-direction:column;gap:9px">'
            '<div style="font-family:' + SERIF + ';font-size:16px;font-weight:700">Yaklaşanlar ve süresi geçenler (6)</div>' + tablo + '</div>' + panel + '</div></div>')

def paper(baslik, rozet_t, rozet_c, satirlar, kare=False, kod="TN-K7F3A-9C2D"):
    line = lambda x, c=None: '<div style="height:5px;width:' + str(x) + '%;background:' + (c or T["cizgi"]) + ';border-radius:2px"></div>'
    kareler = ('<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin:2px 0">'
               + "".join('<div style="height:20px;background:repeating-linear-gradient(135deg,#e6e3da 0 4px,#cbc8be 4px 8px);border-radius:2px"></div>' for _ in range(3)) + '</div>') if kare else ""
    return ('<div style="box-sizing:border-box;width:150px;height:200px;background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';box-shadow:0 8px 20px rgba(28,33,40,.14);'
            'padding:12px;display:flex;flex-direction:column;gap:6px;flex:none">'
            '<div style="display:flex;justify-content:space-between;align-items:center">'
            '<div style="font-family:' + SERIF + ';font-size:9px;font-weight:700">' + baslik + '</div>'
            '<div style="width:16px;height:16px;background:' + T["ink"] + ';border-radius:2px"></div></div>'
            '<div style="font-size:7px;color:' + rozet_c + ';font-weight:700">' + rozet_t + '</div>'
            + "".join(line(x, c) for x, c in satirlar) + kareler
            + '<div style="margin-top:auto;font-size:6.5px;color:' + T["sessiz"] + ';font-family:ui-monospace,Menlo,monospace">Doğrulama ' + kod + '</div></div>')

# ---------------------------------------------------------------- sayfalar
def icindekiler():
    grup = lambda t: ('<div style="font-size:10px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:' + T["marka"] +
                      ';margin:6px 0 2px">' + t + '</div>')
    oge = lambda n, t, sf: ('<div style="display:flex;gap:7px;align-items:baseline;font-size:11.5px;line-height:1.45">'
                            '<span style="color:' + T["marka"] + ';font-weight:700;width:14px;flex:none">' + str(n) + '</span>'
                            '<span style="flex:1;min-width:0">' + t + '</span>'
                            '<span style="color:' + T["sessiz"] + ';flex:none">s.' + str(sf) + '</span></div>')
    sol = (grup("Merkez ne görür") + oge(1, "Her sabah iki dakika", 1) + oge(2, "Sorunsuz gün tek cümledir", 1)
           + grup("Kanıt ve denetim") + oge(3, "Denetim geldiğinde üç dakika", 2) + oge(4, "“Fotoğrafı dün çekmiş” tartışması biter", 2)
           + oge(5, "Belge süresi kaçmaz", 2))
    sag = (grup("Şubede nasıl yürür") + oge(6, "Personel altı dakikada bitirir", 3) + oge(7, "Soğuk zincir kendini savunur", 3)
           + oge(8, "Yapılamayan iş kaybolmaz", 3)
           + grup("Başlamak") + oge(9, "Wi-Fi gidince iş durmaz", 4) + oge(10, "Liste yazmakla uğraşmazsınız", 4)
           + oge(11, "Bir günde kurulur, aynı gece başlar", 4))
    return ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:12px;padding:11px 15px">'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0 26px">'
            '<div>' + sol + '</div><div>' + sag + '</div></div>'
            '<div style="font-size:11px;color:' + T["sessiz"] + ';margin-top:8px;border-top:1px solid ' + T["cizgi"] + ';padding-top:7px">'
            'Sayfa 5–10: bugünkü sürümün dışında kalanlar — on iki <b>tasarım taslağı</b> ekranla, neden sıraya alındıklarıyla.</div></div>')

def s1():
    giris = ('<div style="background:' + INK_BAND + ';border-radius:14px;padding:18px 24px;display:flex;flex-direction:column;gap:8px">'
             + label("Özellik föyü", "rgba(255,255,255,.55)")
             + h1("Her özelliğin karşılığı:<br>ekranda ne görürsünüz", 26, "#fff", "30ch")
             + p("Broşürdeki yol haritasında her satır tek cümleydi. Burada on bir özelliğin her biri bir ekranla: merkezin ne gördüğü, "
                 "şubenin ne yaptığı, denetimde ne verdiğiniz.", 13, "rgba(255,255,255,.78)", "76ch") + '</div>')
    k1 = kart(1, "Her sabah iki dakika", "telefon + e-posta", "mobil",
              "Dün gece şubelerin kaçı yolunda? Cevap 07:00'de telefonunuzda ve e-postanızda; yalnızca aksayanlar, sebebiyle. "
              "Gece kimse aranmaz — sadece gıda güvenliği, iş güvenliği ve parayla ilgili kritik maddeler anında bildirilir.",
              ["Kaçırılan liste şube müdürüne anında düşer; size sabah özetinde gelir",
               "Kritik madde başarısızsa anında bildirim, 10 dakikada okunmazsa SMS",
               "Sessiz saat 23:00–07:00: gece telefonunuz çalmaz"],
              scaled(B.scr_morning(), 390, 844, 0.30), "Sabah özeti · bölge müdürü")
    k2 = kart(2, "Sorunsuz gün tek cümledir", "web", "web",
              "Elli şubeyi tek tek gezmezsiniz: panonun varsayılanı “her şey yolunda”dır ve yalnızca dikkat isteyen hücreler listelenir. "
              "Tüm günün şube × liste ızgarası tek bakışta durur.",
              ["Altı sayı: zamanında, geç, başarısız, kaçırıldı, yapılamadı, açık aksiyon",
               "Hücreden o gecenin tamamına ve fotoğraflara tek tıkla inersiniz",
               "Gün, bölge ve “şüpheli kanıt” filtreleri"],
              scaled(B.scr_pano(1200, 760), 1200, 760, 0.28), "Operasyon panosu · merkez")
    return page(head("Merkez ne görür") + giris + icindekiler() + k1 + k2 + foot(1, "Ekranlar ürün tasarımındandır; veriler örnektir. · Sürüm 1.1 · 4 Ekim 2026"), gap=12)

def s2():
    pdf_grup = ('<div style="display:flex;gap:9px">'
                + paper("Çalıştırma raporu", "BAŞARISIZ · kritik madde", T["kritik"],
                        [("90", None), ("70", None), ("85", None), ("60", T["kritikA"]), ("80", None)], kare=True)
                + paper("Aylık özet", "EYLÜL · 12 ŞUBE", T["marka"],
                        [("85", None), ("65", T["markaA"]), ("75", None), ("55", None), ("80", None), ("70", T["markaA"]), ("60", None)], kod="TN-9B2E1-44AC")
                + paper("Sıcaklık günlüğü", "1–30 EYLÜL · 3 ÖLÇÜM/GÜN", T["marka"],
                        [("90", None), ("88", None), ("86", None), ("84", T["kritikA"]), ("88", None), ("85", None), ("80", None)], kod="TN-3C7D0-18BF") + '</div>')
    pdfler = scaled(pdf_grup, 468, 200, 0.72)
    k3 = kart(3, "Denetim geldiğinde üç dakika", "PDF", "pdf",
              "Denetçi kaydı istediğinde klasör karıştırmazsınız. Üç çıktı doğrulama kodlu PDF olarak iner: bir gecenin tamamını "
              "fotoğraflarıyla gösteren çalıştırma raporu, aylık tek sayfa özet ve sıcaklık günlüğü.",
              ["Hangi ölçümün ne zaman, kim tarafından girildiği satır satır görünür",
               "Her PDF üretim zamanı ve doğrulama kodu taşır",
               "Kanıt dosyaları 24 ay saklanır, sonra otomatik silinir"],
              pdfler, "Çalıştırma raporu · aylık özet · sıcaklık günlüğü", sol_w=340)
    k4 = kart(4, "“Fotoğrafı dün çekmiş” tartışması biter", "web", "web",
              "Fotoğraf yalnızca uygulama içinden çekilir, sunucu damgalar ve kayıt gönderildikten sonra değişmez. "
              "Aynı fotoğraf ikinci kez gönderilemez; sistem dosyayı tanır ve reddeder.",
              ["Galeriden yükleme denemesi, şube dışı konum ve cihaz saati farkı kayıtta işaretlenir",
               "Panoda tek filtreyle incelenmesi gereken kayıtlar listelenir",
               "İşaret bir suçlama değil: kimse puanlanmaz, kayıt personeli de korur"],
              scaled(scr_bayrak(900, 520), 900, 520, 0.40), "Kanıtlar ve bütünlük işaretleri")
    k5 = kart(5, "Belge süresi kaçmaz", "web", "web",
              "Yangın tüpü dolumu, baca ve su deposu temizliği, periyodik elektrik kontrolü, hijyen eğitimi ve portör belgeleri "
              "tarihleriyle durur. Süre dolmadan uyarır; geçerse işi kendisi açar.",
              ["Bitişe 30 ve 7 gün kala sorumluya ve şube müdürüne bildirim",
               "Tarih geçerse iş açılır ve şube “belge eksik” olarak görünür",
               "Zincirin tamamı tek listede; denetim için dönem PDF’i"],
              scaled(scr_belge(1200, 760), 1200, 760, 0.28), "Belge takvimi · zincir görünümü")
    return page(head("Kanıt ve denetim") + k3 + k4 + k5 + foot(2), gap=12)

def s3():
    k6 = kart(6, "Personel altı dakikada bitirir", "şube tableti", "mobil",
              "Şube tableti açık durur; personel adına dokunup dört haneli PIN'ini girer, maddeleri işaretler, fotoğrafı uygulamadan çeker. "
              "Telefonu olmayan personel de kayıt dışı kalmaz.",
              ["Eğitim 10 dakika: üç ekran, iki dokunuş; eldivenle kullanılacak büyüklükte",
               "Listeyi ilk açan alır, diğer cihazlarda “Emre yapıyor” görünür",
               "İki dakika hareketsizlikte kilitlenir, kaldığı yerden devam eder"],
              scaled(B.scr_kiosk(), 390, 844, 0.30), "Kapanış listesi · şube tableti")
    k7 = kart(7, "Soğuk zincir kendini savunur", "mobil", "mobil",
              "Kabul aralığı maddenin içinde yazar. Aralık dışı ölçüm ya da “Hayır” cevabı tek bir sabit kuralı işletir: "
              "fotoğraf ve not zorunlu, madde kritikse iş açılır ve anında bildirilir.",
              ["Kural her şubede aynı çalışır — ayarlanacak bir şey yok",
               "Girilen her ölçüm sıcaklık günlüğüne düşer, denetimde oradan çıkar",
               "İş kapanırken not zorunlu: ne yapıldığı kayda geçer"],
              scaled(B.scr_temp(), 390, 844, 0.30), "Aralık dışı ölçüm · kural devrede")
    k8 = kart(8, "Yapılamayan iş kaybolmaz", "mobil", "mobil",
              "Personel yapamadığını sebebiyle bildirir. İş sessizce düşmez: şube müdürüne 72 saatlik iş olarak açılır ve "
              "ertesi sabah açılış listesinin başında görünür.",
              ["Sabit sebepler: malzeme yok · ekipman arızalı · zaman yetmedi · yetkim yok · diğer",
               "Sebepler merkezde birikir; tekrar eden eksik görünür hâle gelir",
               "“Dün gece” bloğu: sabahçı, önceki vardiyanın açık bıraktığını görür"],
              scaled(TT.scr_unable(), 390, 844, 0.30), "Yapılamadı · sebep seçimi")
    return page(head("Şubede nasıl yürür") + k6 + k7 + k8 + foot(3), gap=12)

def s4():
    k9 = kart(9, "Wi-Fi gidince iş durmaz", "mobil", "mobil",
              "Mutfakta bağlantı kesilse de liste cihazda devam eder; kayıtlar 72 saate kadar bekler ve bağlantı gelince sırayla gönderilir. "
              "Hiçbir cevap “internet yoktu” diye kaybolmaz.",
              ["Fotoğraf cihazda küçültülüp kuyrukta saklanır",
               "Saat cihazdan değil sunucudan alınır; damga sonradan düzeltilir",
               "Geç ulaşan kayıt işaretlenir, silinmez"],
              scaled(scr_offline(), 390, 844, 0.30), "Çevrimdışı · kuyrukta bekleyen kayıtlar")
    k10 = kart(10, "Liste yazmakla uğraşmazsınız", "web", "web",
               "Kapanış, açılış, saatlik hijyen, soğuk zincir, haftalık derin temizlik, fritöz yağı, kasa devri ve teslimat kabul listeleri "
               "73 maddeyle hazır gelir; kopyalayıp kendi işletmenize göre düzenlersiniz.",
               ["Altı madde türü: onay, seçim, sayı, sıcaklık, metin, fotoğraf",
                "Her madde zorunlu, fotoğraf zorunlu veya kritik olarak işaretlenebilir",
                "Düzenleme yeni sürüm açar; o sırada çalışan planlar bozulmaz"],
               scaled(scr_sablon(1200, 760), 1200, 760, 0.28), "Şablonlar ve madde türleri")
    k11 = kart(11, "Bir günde kurulur, aynı gece başlar", "web", "web",
               "Şubeler Excel'den yüklenir, liste hazır şablondan seçilir, saatler şubenin kendi çalışma saatinden hesaplanır. "
               "Dört adım; ilk liste kurulumun olduğu gece açılır.",
               ["25 satırlık şube dosyası tek seferde; hatalı satırlar rapor olarak döner",
                "Dört rol — yönetici, bölge müdürü, şube müdürü, personel — herkes yalnızca kendi kapsamını görür",
                "Gece yarısını aşan pencere aynı iş gününe yazılır"],
               scaled(TT.scr_wizard(1200, 760), 1200, 760, 0.28), "Kurulum sihirbazı · adım 3")
    return page(head("Başlamak") + k9 + k10 + k11 + foot(4), gap=12)

# ---------------------------------------------------------------- yol haritası ekranları (tasarım taslağı)
def ekran(W, H, baslik, sag_ust, inner, gap=11):
    return ('<div style="box-sizing:border-box;width:' + str(W) + 'px;height:' + str(H) + 'px;background:' + T["zemin"] + ';font-family:' + SANS +
            ';color:' + T["ink"] + ';padding:16px 20px;display:flex;flex-direction:column;gap:' + str(gap) + 'px;overflow:hidden;border:1px solid ' + T["cizgi"] + ';border-radius:12px">'
            '<div style="display:flex;align-items:center;gap:12px">' + w(17) +
            '<div style="padding-left:12px;border-left:1px solid ' + T["cizgi"] + ';font-family:' + SERIF + ';font-size:17px;font-weight:700">' + baslik + '</div>'
            '<div style="margin-left:auto;font-size:12.5px;color:' + T["ink2"] + '">' + sag_ust + '</div></div>' + inner + '</div>')

def lbl(t):
    return '<div style="font-size:10px;letter-spacing:.07em;text-transform:uppercase;color:' + T["sessiz"] + ';font-weight:700;margin-bottom:5px">' + t + '</div>'

def satir(hucreler, basliklar=None, genislikler=None, size=12.5):
    wc = "".join('<col style="width:' + x + '">' for x in genislikler) if genislikler else ""
    th = "".join('<th style="text-align:left;padding:7px 9px;font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:' + T["sessiz"] +
                 ';background:' + T["yuzey2"] + ';border-bottom:1px solid ' + T["cizgi"] + '">' + c + '</th>' for c in (basliklar or []))
    tr = ""
    for i, r in enumerate(hucreler):
        bb = "0" if i == len(hucreler) - 1 else "1px solid " + T["cizgi"]
        tr += "<tr>" + "".join('<td style="padding:7px 9px;border-bottom:' + bb + ';vertical-align:top;line-height:1.4">' + c + '</td>' for c in r) + "</tr>"
    return ('<div style="border:1px solid ' + T["cizgi"] + ';border-radius:10px;overflow:hidden;background:' + T["yuzey"] + '">'
            '<table style="border-collapse:collapse;width:100%;font-size:' + str(size) + 'px">' + wc +
            ('<thead><tr>' + th + '</tr></thead>' if basliklar else '') + '<tbody>' + tr + '</tbody></table></div>')

def foto(cap, flag=None, fc=None, en="100%"):
    f = ('<div style="position:absolute;left:5px;top:5px;background:' + (fc or T["uyari"]) + ';color:#fff;border-radius:999px;padding:2px 8px;font-size:10px;font-weight:700">' + flag + '</div>') if flag else ''
    return ('<div style="width:' + en + '"><div style="aspect-ratio:4/3;border-radius:8px;background:repeating-linear-gradient(135deg,#dfe3e8 0 9px,#eef1f4 9px 18px);position:relative;overflow:hidden;border:1px solid ' + T["cizgi"] + '">' + f +
            '<div style="position:absolute;left:0;right:0;bottom:0;background:rgba(28,33,40,.84);color:#fff;font:9px/1.3 ui-monospace,Menlo,Consolas,monospace;padding:3px 5px">' + cap + '</div></div></div>')

# --- S1 madde kütüphanesi ve işletme türü paketleri
def scr_kutuphane(W=1100, H=620):
    paket = lambda ad, n, sec=False: ('<div style="border:1.5px solid ' + (T["marka"] if sec else T["cizgi"]) + ';background:' + (T["markaA"] if sec else T["yuzey"]) +
                                      ';border-radius:10px;padding:9px 11px"><b style="font-size:13px">' + ad + '</b>'
                                      '<div style="font-size:11.5px;color:' + T["sessiz"] + '">' + n + '</div></div>')
    md = lambda ad, tur, rozet_="", uyari=False: ('<div style="display:flex;gap:9px;align-items:center;padding:7px 0;border-bottom:1px solid ' + T["cizgi"] + '">'
                                                  '<div style="width:16px;height:16px;border-radius:4px;border:1.5px solid ' + (T["marka"] if not uyari else T["uyari"]) + ';flex:none"></div>'
                                                  '<div style="flex:1;min-width:0;font-size:12.5px;line-height:1.35">' + ad +
                                                  ('<div style="font-size:11px;color:' + T["uyari"] + ';font-weight:600;margin-top:1px">kütüphanede güncellendi — farkı gör</div>' if uyari else '') + '</div>'
                                                  '<div style="font-size:11px;color:' + T["sessiz"] + ';white-space:nowrap">' + tur + '</div>' + (chip(rozet_) if rozet_ else '') + '</div>')
    sol = ('<div style="display:flex;flex-direction:column;gap:9px">' + lbl("İşletme türü paketleri")
           + paket("Kafe · bar", "6 liste · 78 madde", True) + paket("Fırın ve pastane", "5 liste · 64 madde")
           + paket("Hızlı servis", "6 liste · 71 madde") + paket("Lokanta · ocakbaşı", "5 liste · 59 madde")
           + '<div style="background:' + T["yuzey2"] + ';border-radius:10px;padding:9px 11px;font-size:11.5px;line-height:1.45;color:' + T["ink2"] + '">'
           'Paketi şubenize kopyalarsınız; kütüphane maddesi güncellenince kopyanız bozulmaz, yalnızca uyarı alır.</div></div>')
    sag = ('<div style="display:flex;flex-direction:column;gap:9px;min-width:0">'
           + card(lbl("Kafe · bar paketi — kapanış maddeleri") + md("Espresso makinesi geri yıkandı", "onay", "kütüphane")
                  + md("Süt dolabı sıcaklığı", "sıcaklık 0–4 °C", "kritik") + md("Kahve öğütücü hazneleri temizlendi", "fotoğraf", "kütüphane", uyari=True)
                  + md("Buzmatik temizlendi ve kurulandı", "onay") + md("Bar tezgâhı dezenfekte edildi", "onay", "kütüphane"), "padding:11px 13px")
           + '<div style="display:flex;gap:9px"><div style="padding:8px 13px;border-radius:9px;background:' + T["marka"] + ';color:#fff;font-weight:600;font-size:13px">Seçili 4 maddeyi şubeye ekle</div>'
           '<div style="padding:8px 13px;border-radius:9px;border:1.5px solid ' + T["cizgi"] + ';font-size:13px;color:' + T["ink2"] + '">Farkları incele (1)</div></div></div>')
    return ekran(W, H, "Madde kütüphanesi", "Kahve Durağı · 12 şube",
                 '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.6fr);gap:14px;min-height:0">' + sol + sag + '</div>')

# --- S2 üretim–satış mutabakatı
def scr_mutabakat(W=1100, H=620):
    kpi = lambda n, l, c: ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:11px;padding:10px 13px">'
                           '<div style="font-family:' + SERIF + ';font-size:23px;font-weight:700;color:' + c + ';line-height:1.1">' + n + '</div>'
                           '<div style="font-size:11.5px;color:' + T["sessiz"] + ';margin-top:2px">' + l + '</div></div>')
    r = lambda u, ur, sa, fi, fa, kr=False: [u, ur, sa, fi,
                                             '<b style="color:' + (T["kritik"] if kr else T["ink2"]) + '">' + fa + '</b>']
    tablo = satir([r("Pide · kıymalı", "128", "119", "4 (fire)", "5"),
                   r("Pide · kaşarlı", "96", "71", "2 (personel yemeği)", "23", True),
                   r("Lahmacun", "210", "204", "6 (ikram)", "0"),
                   r("Ayran (şişe)", "180", "176", "0", "4"),
                   r("Künefe", "44", "43", "1 (hatalı üretim)", "0")],
                  ["Ürün", "Üretilen", "Satılan", "Açıklanan", "Fark"], ["34%", "15%", "15%", "22%", "14%"])
    sebep = lambda t, sec=False: ('<div style="padding:7px 10px;border:1.5px solid ' + (T["marka"] if sec else T["cizgi"]) + ';border-radius:9px;font-size:12px;background:' +
                                  (T["markaA"] if sec else T["yuzey"]) + '">' + t + '</div>')
    sag = ('<div style="display:flex;flex-direction:column;gap:9px;min-width:0">'
           + card(lbl("Açıklama gerekiyor · kaşarlı pide") +
                  '<div style="font-size:12.5px;line-height:1.5;color:' + T["ink2"] + ';margin-bottom:7px">23 adet fark · yaklaşık <b style="color:' + T["ink"] + '">₺2.760</b> · Cmt 13 Eylül akşam vardiyası</div>'
                  + '<div style="display:flex;flex-direction:column;gap:6px">' + sebep("Fire / hatalı üretim") + sebep("Personel yemeği") + sebep("İkram")
                  + sebep("Kasaya geç girildi", True) + sebep("Sayım hatası") + sebep("Açıklanamıyor → bölge müdürüne") + '</div>'
                  '<div style="border:1.5px solid ' + T["cizgi"] + ';border-radius:9px;padding:8px 10px;font-size:12px;color:' + T["ink2"] + ';margin-top:8px">'
                  'Not: 19:40 civarı kasa kapandı, iki sipariş deftere yazıldı</div>', "padding:11px 13px")
           + '<div style="background:' + T["yuzey2"] + ';border-radius:10px;padding:9px 11px;font-size:11.5px;line-height:1.45;color:' + T["ink2"] + '">'
           'Rapor şube ve vardiya düzeyindedir: kişi adı, kişi puanı ve biyometri yok. Açıklama girilmeden kayıt kapanmaz.</div></div>')
    sol = ('<div style="display:flex;flex-direction:column;gap:10px;min-width:0">'
           '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px">'
           + kpi("₺2.760", "açıklanamayan fark · bu vardiya", T["kritik"]) + kpi("%3,4", "üretime oran", T["uyari"]) + kpi("4", "açıklanan kalem", T["marka"]) + '</div>'
           + lbl("Üretim sayımı ↔ kasa satışı · Kadıköy · 13 Eylül") + tablo + '</div>')
    return ekran(W, H, "Üretim–satış mutabakatı", "Kadıköy · akşam vardiyası",
                 '<div style="display:grid;grid-template-columns:minmax(0,1.45fr) minmax(0,1fr);gap:14px;min-height:0">' + sol + sag + '</div>')

# --- S3 benzer fotoğraf tespiti
def scr_benzer(W=760, H=430):
    return ekran(W, H, "Benzer kanıt uyarısı", "Kadıköy · Kapanış · 13 Eylül",
                 '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px;min-height:0">'
                 '<div style="display:flex;gap:9px">' + foto("12 · 23:33 · Emre T.") + foto("15 · 23:39 · Emre T.", "benzer %94") + '</div>'
                 '<div style="display:flex;flex-direction:column;gap:9px">'
                 + card('<b style="font-size:13.5px">İki kanıt neredeyse aynı</b>'
                        '<div style="font-size:12px;line-height:1.45;color:' + T["ink2"] + ';margin-top:4px">'
                        'Çöp alanı ve kepenk maddelerinin fotoğrafları 6 saniye arayla, aynı açıdan çekilmiş. '
                        'Dosyalar farklı olduğu için gönderim engellenmedi; kayıt incelenmek üzere işaretlendi.</div>'
                        '<div style="display:flex;gap:8px;margin-top:9px">'
                        '<div style="padding:7px 12px;border-radius:9px;background:' + T["ink"] + ';color:#fff;font-weight:600;font-size:12.5px">Şube müdürüne sor</div>'
                        '<div style="padding:7px 12px;border-radius:9px;border:1.5px solid ' + T["cizgi"] + ';font-size:12.5px;color:' + T["ink2"] + '">Uygun, işareti kaldır</div></div>', "padding:11px 13px")
                 + '<div style="background:' + T["yuzey2"] + ';border-radius:10px;padding:9px 11px;font-size:11.5px;line-height:1.45;color:' + T["ink2"] + '">'
                 'Eşik ayarlanabilir. Karar insanda kalır: sistem yalnızca “şuna bakın” der.</div></div></div>')

# --- S4 duyuru ve okundu onayı
def scr_duyuru(W=900, H=520):
    tablo = satir([["Kadıköy", "Ayşe K.", "13.09 09:12", chip("onayladı", "ok")],
                   ["Üsküdar", "Mehmet T.", "13.09 10:40", chip("onayladı", "ok")],
                   ["Bakırköy", "Deniz A.", "—", chip("okunmadı", "crit")],
                   ["Ataşehir", "Burak S.", "13.09 11:05", chip("okudu", "warn")],
                   ["Bornova", "Elif Y.", "13.09 08:55", chip("onayladı", "ok")]],
                  ["Şube", "Sorumlu", "Okundu", "Durum"], ["26%", "28%", "26%", "20%"])
    return ekran(W, H, "Duyuru ve okundu onayı", "Yeni fiyat listesi · 13 Eylül",
                 '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:13px;min-height:0">'
                 '<div style="display:flex;flex-direction:column;gap:9px">'
                 + card('<b style="font-family:' + SERIF + ';font-size:15px">Yeni fiyat listesi 15 Eylül’de geçerli</b>'
                        '<div style="font-size:12px;line-height:1.5;color:' + T["ink2"] + ';margin-top:5px">'
                        'Menü fiyatları güncellendi. Kasadaki fiyat etiketlerini 14 Eylül kapanışında değiştirin, '
                        'eski etiketleri atmayın — sayım yapılacak.</div>'
                        '<div style="display:flex;gap:7px;align-items:center;margin-top:9px;font-size:11.5px;color:' + T["sessiz"] + '">'
                        '<span style="padding:3px 9px;border-radius:999px;background:' + T["yuzey2"] + '">fiyat-listesi-eylul.pdf</span>'
                        '<span>· onay istendi</span></div>', "padding:11px 13px")
                 + '<div style="background:' + T["markaA"] + ';border-radius:10px;padding:10px 12px">'
                 '<div style="font-family:' + SERIF + ';font-size:20px;font-weight:700;color:' + T["marka"] + '">10 / 12</div>'
                 '<div style="font-size:11.5px;color:' + T["ink2"] + '">şube onayladı · 1 okudu, 1 okumadı</div>'
                 '<div style="font-size:11.5px;color:' + T["ink2"] + ';margin-top:6px">Okumayana 14:00’te hatırlatma gider.</div></div></div>'
                 '<div style="display:flex;flex-direction:column;gap:7px;min-width:0">' + lbl("Okundu raporu") + tablo + '</div></div>')

# --- S5 koşullu maddeler
def scr_kosul(W=900, H=520):
    kural = lambda a, b, sec=False: ('<div style="border:1.5px solid ' + (T["marka"] if sec else T["cizgi"]) + ';background:' + (T["markaA"] if sec else T["yuzey"]) +
                                     ';border-radius:10px;padding:9px 11px;font-size:12px;line-height:1.5">'
                                     '<b>Eğer</b> ' + a + '<br><b>o zaman</b> ' + b + '</div>')
    onizleme = ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:12px;padding:11px 13px">'
                + lbl("Personel ne görür")
                + '<div style="font-size:12.5px;display:flex;flex-direction:column;gap:7px">'
                '<div style="display:flex;gap:8px;align-items:center">' + box("") + '<div>Fritöz kapatıldı, yağ süzüldü</div></div>'
                '<div style="display:flex;gap:8px;align-items:center;opacity:.5">' + box("") + '<div>Yağ polar madde ölçümü <span style="color:' + T["sessiz"] + '">(gizli)</span></div></div>'
                '<div style="border-left:3px solid ' + T["marka"] + ';padding-left:9px;color:' + T["ink2"] + '">“Hayır” seçilirse alttaki iki madde açılır: sebep ve fotoğraf.</div></div></div>')
    return ekran(W, H, "Koşullu maddeler", "Şablon editörü · Kapanış v4 taslak",
                 '<div style="display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:13px;min-height:0">'
                 '<div style="display:flex;flex-direction:column;gap:9px">' + lbl("Maddeye bağlı kurallar")
                 + kural("“Fritöz kapatıldı” = <b>Hayır</b>", "<b>Sebep</b> ve <b>fotoğraf</b> maddelerini aç", True)
                 + kural("“Ekipman arızalı” seçildi", "<b>Servis çağrıldı mı?</b> maddesini aç ve şube müdürüne iş aç")
                 + kural("Sıcaklık <b>aralık dışı</b>", "<b>İkinci ölçüm (30 dk sonra)</b> maddesini aç")
                 + '<div style="padding:8px 12px;border-radius:9px;border:1.5px dashed ' + T["cizgi"] + ';font-size:12.5px;color:' + T["sessiz"] + ';text-align:center">+ Kural ekle</div></div>'
                 + onizleme + '</div>')

# --- S6 ayrıntılı raporlar
def scr_raporlar(W=1100, H=620):
    sekme = lambda t, s=False: ('<div style="padding:6px 11px;border-radius:999px;font-size:12.5px;background:' + (T["ink"] if s else T["yuzey"]) +
                                ';color:' + ("#fff" if s else T["ink2"]) + ';border:1px solid ' + (T["ink"] if s else T["cizgi"]) + '">' + t + '</div>')
    maddeler = ["Buzdolabı sıcaklığı", "Zemin paspas", "Çöp alanı", "Fritöz yağı", "Tuvalet kontrol", "Kasa sayımı"]
    subeler = ["Kadıköy", "Üsküdar", "Bakırköy", "Ataşehir", "Bornova", "Kartal", "Şişli"]
    yogun = {("Kadıköy", 0): 3, ("Bakırköy", 1): 2, ("Bakırköy", 0): 3, ("Kartal", 3): 2, ("Şişli", 4): 1, ("Bornova", 2): 2, ("Ataşehir", 5): 1, ("Üsküdar", 1): 1}
    renk = {0: "#e8e6dd", 1: T["uyariA"], 2: "#e9b071", 3: T["kritik"]}
    hucre = ""
    for s in subeler:
        hucre += '<div style="font-size:11px;color:' + T["ink2"] + ';display:flex;align-items:center">' + s + '</div>'
        for i in range(len(maddeler)):
            hucre += '<div style="height:20px;border-radius:4px;background:' + renk[yogun.get((s, i), 0)] + '"></div>'
    isi = ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:11px;padding:11px 13px">'
           + lbl("En çok başarısız olan maddeler · Eylül")
           + '<div style="display:grid;grid-template-columns:84px repeat(6, minmax(0,1fr));gap:4px 5px;align-items:center">'
           + '<div></div>' + "".join('<div style="font-size:9.5px;color:' + T["sessiz"] + ';text-align:center;line-height:1.2">' + m + '</div>' for m in maddeler)
           + hucre + '</div></div>')
    siralama = satir([["1 · Üsküdar", "%96", "2", "0"], ["2 · Ataşehir", "%94", "3", "1"], ["3 · Maltepe", "%92", "4", "0"],
                      ["…", "", "", ""], ["11 · Bakırköy", "%71", "14", "6"], ["12 · Kadıköy", "%68", "17", "8"]],
                     ["Şube", "Zamanında", "Yapılamadı", "Başarısız"], ["38%", "22%", "20%", "20%"])
    sebepler = ""
    for ad, yuzde in [("Malzeme yok", 38), ("Ekipman arızalı", 27), ("Zaman yetmedi", 19), ("Yetkim yok", 9), ("Diğer", 7)]:
        sebepler += ('<div style="display:flex;gap:9px;align-items:center;font-size:11.5px;padding:3px 0">'
                     '<div style="width:92px;flex:none;color:' + T["ink2"] + '">' + ad + '</div>'
                     '<div style="flex:1;height:9px;background:' + T["yuzey2"] + ';border-radius:5px;overflow:hidden">'
                     '<div style="width:' + str(yuzde) + '%;height:100%;background:' + T["marka"] + '"></div></div>'
                     '<div style="width:30px;text-align:right;color:' + T["sessiz"] + '">%' + str(yuzde) + '</div></div>')
    return ekran(W, H, "Raporlar", "Eylül 2026 · 12 şube",
                 '<div style="display:flex;gap:8px">' + sekme("Tamamlanma", True) + sekme("Maddeler") + sekme("Yapılamadı sebepleri")
                 + sekme("Ölçümler") + sekme("Aksiyonlar") + '<div style="margin-left:auto;display:flex;gap:8px">'
                 '<div style="padding:6px 11px;border:1.5px solid ' + T["cizgi"] + ';border-radius:9px;font-size:12.5px;background:' + T["yuzey"] + '">Excel</div>'
                 '<div style="padding:6px 11px;border-radius:9px;background:' + T["marka"] + ';color:#fff;font-size:12.5px;font-weight:600">Paylaşım bağlantısı</div></div></div>'
                 '<div style="display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:13px;min-height:0">' + isi
                 + '<div style="display:flex;flex-direction:column;gap:9px">' + siralama
                 + '<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:11px;padding:11px 13px">'
                 + lbl("Yapılamadı sebepleri") + sebepler + '</div></div></div>')

# --- S7 denetim izi ekranı
def scr_izi(W=1000, H=560):
    olay = lambda t, kim, ne, h: [t, kim, ne, '<span style="font:11px ui-monospace,Menlo,Consolas,monospace;color:' + T["sessiz"] + '">' + h + '</span>']
    tablo = satir([olay("13.09 22:58", "Emre T.", "Çalıştırma açıldı · kiosk KDK-T1 · konum şube içinde", "a91f…6c2d"),
                   olay("13.09 23:20", "Emre T.", "Madde 4 cevaplandı: 6,0 °C · aralık dışı · 1 kanıt", "4b07…11ae"),
                   olay("13.09 23:20", "sistem", "Aksiyon #418 açıldı · kritik · Ayşe K.", "77c3…90f1"),
                   olay("13.09 23:41", "Emre T.", "Çalıştırma gönderildi · sonuç: başarısız · kilitlendi", "e2aa…35bd"),
                   olay("14.09 08:05", "Ayşe K.", "Aksiyon #418 kapatıldı · not + 1 kanıt", "1d58…77c0"),
                   olay("14.09 08:06", "sistem", "Günlük kökü zaman damgası alındı", "0f92…ab41")],
                  ["Zaman", "Kim", "Olay", "Özet"], ["16%", "14%", "52%", "18%"], size=12)
    return ekran(W, H, "Denetim izi", "Kadıköy · 13–14 Eylül",
                 '<div style="display:flex;gap:8px;align-items:center">'
                 '<div style="padding:6px 10px;border:1.5px solid ' + T["cizgi"] + ';border-radius:9px;font-size:12.5px;background:' + T["yuzey"] + '">Şube: Kadıköy ▾</div>'
                 '<div style="padding:6px 10px;border:1.5px solid ' + T["cizgi"] + ';border-radius:9px;font-size:12.5px;background:' + T["yuzey"] + '">Olay türü: tümü ▾</div>'
                 '<div style="padding:6px 10px;border:1.5px solid ' + T["cizgi"] + ';border-radius:9px;font-size:12.5px;background:' + T["yuzey"] + '">13–14 Eylül ▾</div>'
                 '<div style="margin-left:auto">' + chip("zincir doğrulandı · 6 olay", "ok") + '</div></div>'
                 + tablo
                 + '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px">'
                 + card(lbl("Zincir doğrulama") + '<div style="font-size:12px;line-height:1.5;color:' + T["ink2"] + '">'
                        'Her olay bir öncekinin özetini taşır. Tek bir kaydı değiştirmek zinciri kırar ve bu sayfada kırmızı görünür. '
                        'Kayıt silinmez; düzeltme ayrı bir olaydır.</div>', "padding:11px 13px")
                 + card(lbl("Zaman damgası") + '<div style="font-size:12px;line-height:1.5;color:' + T["ink2"] + '">'
                        'Günlük kök, bağımsız bir zaman damgası hizmetinden onay alır: kaydın o tarihte var olduğu üçüncü tarafça doğrulanabilir. '
                        '<b style="color:' + T["ink"] + '">14.09 08:06</b> · TSA onayı</div>', "padding:11px 13px") + '</div>')

# --- S8 denetim dosyası ve denetçi bağlantısı (E-13)
def scr_denetimdosyasi(W=1000, H=560):
    icerik = satir([["<b>Sıcaklık ve ölçüm günlüğü</b>", "90 gün · 268 ölçüm", "4 aralık dışı, hepsi aksiyonla kapatıldı"],
                    ["<b>Çalıştırma özetleri</b>", "180 liste", "171 zamanında · 6 geç · 3 kaçırıldı"],
                    ["<b>Belge takvimi</b>", "7 belge", "Yangın tüpü 12 gün sonra doluyor"],
                    ["<b>Kanıt örnekleri</b>", "24 fotoğraf", "Rastgele seçildi · damgalı"],
                    ["<b>Olay izi özeti</b>", "doğrulama kodu", "TN-K7F3A-9C2D"]],
                   ["Bölüm", "Kapsam", "Not"], ["34%", "22%", "44%"], size=12)
    baglanti = card(lbl("Denetçi bağlantısı")
                    + '<div style="font:12px ui-monospace,Menlo,Consolas,monospace;background:' + T["yuzey2"] + ';border-radius:8px;padding:7px 9px;color:' + T["ink2"] + '">'
                      'talimatname.app/d/7F3A-9C2D</div>'
                    + '<div style="display:flex;gap:7px;flex-wrap:wrap;margin-top:8px">' + chip("48 saat kalan: 41 sa", "warn")
                    + chip("yalnızca Kadıköy · 90 gün", "n") + chip("personel adı maskeli", "ok") + '</div>'
                    + '<div style="font-size:12px;line-height:1.5;color:' + T["ink2"] + ';margin-top:8px">'
                      'Hesap açılmaz, indirilemez tek sayfa. İki açılış kayıtlı: <b style="color:' + T["ink"] + '">bugün 10:42</b> ve '
                      '<b style="color:' + T["ink"] + '">10:55</b>. İstediğiniz an iptal edebilirsiniz.</div>', "padding:11px 13px")
    ornek = card(lbl("Dosyadan bir sayfa")
                 + '<div style="display:flex;gap:9px">' + foto("KDK · 13.09 23:20 · aralık dışı", "işaretli", T["kritik"], "33%")
                 + foto("KDK · 14.09 08:05 · aksiyon kapanışı", None, None, "33%")
                 + foto("KDK · 15.09 23:11 · kepenk", None, None, "33%") + '</div>', "padding:11px 13px")
    return ekran(W, H, "Denetim dosyası", "Kadıköy · 16 Haz – 14 Eyl",
                 '<div style="display:flex;gap:8px;align-items:center">'
                 '<div style="padding:6px 10px;border:1.5px solid ' + T["cizgi"] + ';border-radius:9px;font-size:12.5px;background:' + T["yuzey"] + '">Şube: Kadıköy ▾</div>'
                 '<div style="padding:6px 10px;border:1.5px solid ' + T["cizgi"] + ';border-radius:9px;font-size:12.5px;background:' + T["yuzey"] + '">Dönem: son 90 gün ▾</div>'
                 '<div style="margin-left:auto">' + chip("PDF hazır · 38 sayfa", "ok") + '</div></div>'
                 + icerik
                 + '<div style="display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:12px">' + baglanti + ornek + '</div>')

# --- D1 franchise marka kütüphanesi
def scr_franchise(W=1000, H=560):
    tablo = satir([["Kahve Durağı Kadıköy", "şirket", "v4", "%96", chip("uyumlu", "ok")],
                   ["KD Bostancı (franchise)", "franchise", "v4", "%91", chip("uyumlu", "ok")],
                   ["KD Çekmeköy (franchise)", "franchise", "v3", "%78", chip("eski sürüm", "warn")],
                   ["KD Gebze (franchise)", "franchise", "v4", "%64", chip("takipte", "crit")],
                   ["KD İzmit (franchise)", "franchise", "—", "—", chip("kurulmadı", "crit")]],
                  ["İşletme", "Tip", "Liste sürümü", "Zamanında", "Durum"], ["34%", "16%", "16%", "16%", "18%"])
    return ekran(W, H, "Marka kütüphanesi", "Kahve Durağı · 4 franchise · 12 şirket şubesi",
                 '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.55fr);gap:13px;min-height:0">'
                 '<div style="display:flex;flex-direction:column;gap:9px">'
                 + card(lbl("Yayınlanan standart") + '<b style="font-family:' + SERIF + ';font-size:15px">Kapanış listesi v4</b>'
                        '<div style="font-size:12px;line-height:1.5;color:' + T["ink2"] + ';margin-top:4px">'
                        '15 madde · 4 kritik · 2 Eylül’de yayınlandı. Franchise işletmeleri maddeyi silemez, '
                        'yalnızca kendi maddelerini ekleyebilir.</div>'
                        '<div style="display:flex;gap:7px;margin-top:9px">'
                        '<div style="padding:7px 12px;border-radius:9px;background:' + T["marka"] + ';color:#fff;font-weight:600;font-size:12.5px">v5 yayınla</div>'
                        '<div style="padding:7px 12px;border-radius:9px;border:1.5px solid ' + T["cizgi"] + ';font-size:12.5px;color:' + T["ink2"] + '">Değişikliği gör</div></div>', "padding:11px 13px")
                 + '<div style="background:' + T["yuzey2"] + ';border-radius:10px;padding:9px 11px;font-size:11.5px;line-height:1.45;color:' + T["ink2"] + '">'
                 'Marka merkezi uyum oranını ve liste sürümünü görür; franchise işletmesinin kendi personel verisini görmez.</div></div>'
                 '<div style="display:flex;flex-direction:column;gap:7px;min-width:0">' + lbl("Uyum tablosu") + tablo + '</div></div>')

# --- D2 başka sektör paketleri
def scr_paketler(W=900, H=500):
    pk = lambda ad, n, ornek: ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:11px;padding:11px 13px">'
                               '<b style="font-size:13.5px">' + ad + '</b>'
                               '<div style="font-size:11.5px;color:' + T["sessiz"] + ';margin-top:2px">' + n + '</div>'
                               '<div style="font-size:11.5px;color:' + T["ink2"] + ';line-height:1.4;margin-top:5px">' + ornek + '</div>'
                               '<div style="margin-top:8px;padding:6px 10px;border:1.5px solid ' + T["cizgi"] + ';border-radius:8px;font-size:12px;color:' + T["ink2"] + ';display:inline-block">Önizle</div></div>')
    return ekran(W, H, "Sektör paketleri", "Hazır şablon ve madde setleri",
                 '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">'
                 + pk("Perakende zinciri", "7 liste · 86 madde", "Kepenk ve alarm, kasa devri, reyon sıcaklığı, son kullanma tarihi taraması, vitrin standardı")
                 + pk("Otel ve konaklama", "9 liste · 112 madde", "Kat temizliği kontrolü, havuz kimyasal ölçümü, kahvaltı açılışı, yangın kaçış yolu turu")
                 + pk("Akaryakıt istasyonu", "6 liste · 74 madde", "Tank ölçümü, pompa kontrolü, yangın tüpü turu, tuvalet saatlik kontrol, kasa devri")
                 + pk("Üretim ve depo", "8 liste · 98 madde", "Hat temizliği, metal dedektör doğrulama, soğuk oda ölçümü, forklift günlük kontrol")
                 + '</div>'
                 '<div style="background:' + T["yuzey2"] + ';border-radius:10px;padding:10px 12px;font-size:12px;line-height:1.5;color:' + T["ink2"] + '">'
                 'Paketler aynı çekirdeği kullanır: tekrarlı liste, kanıt, aksiyon ve denetim PDF’i. Değişen yalnızca maddeler, '
                 'ölçüm aralıkları ve mevzuat notlarıdır.</div>')

# --- D3 POS ve İK entegrasyonları
def scr_entegrasyon(W=900, H=520):
    kutu = lambda ad, durum, alt, ok=True: ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + (T["cizgi"] if ok else T["uyari"]) + ';border-radius:11px;padding:11px 13px">'
                                            '<div style="display:flex;align-items:center;justify-content:space-between;gap:8px">'
                                            '<b style="font-size:13.5px">' + ad + '</b>' + chip(durum, "ok" if ok else "warn") + '</div>'
                                            '<div style="font-size:11.5px;color:' + T["ink2"] + ';margin-top:4px;line-height:1.45">' + alt + '</div></div>')
    tablo = satir([["Kadıköy", "KD-01", chip("eşleşti", "ok")], ["Üsküdar", "KD-02", chip("eşleşti", "ok")],
                   ["Bakırköy", "KD-07", chip("eşleşti", "ok")], ["Bornova", "—", chip("eşleşmedi", "crit")]],
                  ["Şube", "Kasa mağaza kodu", "Durum"], ["40%", "35%", "25%"])
    return ekran(W, H, "Entegrasyonlar", "Kahve Durağı",
                 '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:13px;min-height:0">'
                 '<div style="display:flex;flex-direction:column;gap:9px">'
                 + kutu("Kasa (POS)", "bağlı", "Satış ve iptal verisi 15 dakikada bir alınır. Üretim–satış mutabakatı bu veriyle çalışır. Son senk: 09:42")
                 + kutu("İK / bordro", "bağlı değil", "Personel ve vardiya bilgisi elle giriliyor. Bağlanırsa işe giriş–çıkış ve vardiya atamaları kendiliğinden güncellenir.", ok=False)
                 + '<div style="background:' + T["yuzey2"] + ';border-radius:10px;padding:9px 11px;font-size:11.5px;line-height:1.45;color:' + T["ink2"] + '">'
                 'Bağlantı tek yönlüdür: veriler okunur, karşı sisteme yazılmaz. Hangi alanların alındığı sözleşme ekinde listelenir.</div></div>'
                 '<div style="display:flex;flex-direction:column;gap:7px;min-width:0">' + lbl("Şube ↔ kasa eşlemesi") + tablo
                 + '<div style="font-size:11.5px;color:' + T["sessiz"] + ';line-height:1.45">Eşleşmeyen şube mutabakat raporuna girmez; '
                 'kurulumda bir kez eşlenir.</div></div></div>')

# --- D4 kamera ile üretim sayımı
def scr_kamera(W=1000, H=560):
    saatler = [("12:00", 18, 17), ("13:00", 26, 25), ("14:00", 21, 20), ("15:00", 12, 12), ("16:00", 15, 14),
               ("17:00", 19, 13), ("18:00", 24, 15), ("19:00", 28, 19), ("20:00", 22, 21)]
    cub = ""
    for s, u, sa in saatler:
        fark = u - sa
        cub += ('<div style="display:flex;flex-direction:column;align-items:center;gap:3px;flex:1">'
                '<div style="height:92px;display:flex;align-items:flex-end;gap:3px">'
                '<div style="width:11px;height:' + str(int(u * 3.2)) + 'px;background:' + T["ink"] + ';border-radius:2px 2px 0 0"></div>'
                '<div style="width:11px;height:' + str(int(sa * 3.2)) + 'px;background:' + (T["kritik"] if fark > 3 else T["marka"]) + ';border-radius:2px 2px 0 0"></div></div>'
                '<div style="font-size:9.5px;color:' + T["sessiz"] + '">' + s + '</div></div>')
    return ekran(W, H, "Üretim sayımı (kamera)", "Kadıköy · fırın ağzı · 13 Eylül",
                 '<div style="display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:13px;min-height:0">'
                 '<div style="display:flex;flex-direction:column;gap:9px;min-width:0">'
                 + card(lbl("Saat başına üretilen (koyu) ve kasaya giren (renkli)")
                        + '<div style="display:flex;gap:4px;align-items:flex-end">' + cub + '</div>'
                        '<div style="font-size:11px;color:' + T["sessiz"] + ';margin-top:7px">17:00–19:00 arasında üretim kasayı aşıyor: 24 adet fark.</div>', "padding:11px 13px")
                 + '<div style="display:flex;gap:9px">' + foto("fırın ağzı · 18:12 · yalnızca tezgâh", "sayım", T["ink"], "46%")
                 + '<div style="flex:1;background:' + T["yuzey2"] + ';border-radius:10px;padding:10px 12px;font-size:11.5px;line-height:1.5;color:' + T["ink2"] + '">'
                 'Kamera yalnızca tezgâh yüzeyini görür ve <b>ürün sayar</b>. Yüz tanıma, kimlik tespiti ve kişi takibi yok; '
                 'görüntü saklanmaz, yalnızca sayı ve zaman kaydedilir.</div></div></div>'
                 '<div style="display:flex;flex-direction:column;gap:9px">'
                 + card('<div style="font-family:' + SERIF + ';font-size:22px;font-weight:700;color:' + T["kritik"] + '">24 adet</div>'
                        '<div style="font-size:11.5px;color:' + T["sessiz"] + '">açıklanamayan fark · 13 Eylül</div>'
                        '<div style="font-size:12px;line-height:1.5;color:' + T["ink2"] + ';margin-top:7px">'
                        'Sayım ±%3 doğrulukla çalışır; eşiğin altındaki farklar rapor edilmez. Fark, sebep girilmeden kapanmaz.</div>', "padding:11px 13px")
                 + '<div style="background:' + T["uyariA"] + ';border-radius:10px;padding:10px 12px;font-size:11.5px;line-height:1.5;color:' + T["ink2"] + '">'
                 'Kamera kurulumu işyeri kamera mevzuatına tabidir: personele duyuru, yasak alan kuralları ve hukuk görüşü olmadan kurulmaz.</div></div></div>')


def taslak_bant(metin):
    return ('<div style="background:' + T["uyariA"] + ';border-left:3px solid ' + T["uyari"] + ';border-radius:0 11px 11px 0;padding:10px 13px;'
            'font-size:12px;line-height:1.5;color:' + T["ink2"] + '">' + metin + '</div>')

def kart_genis(no, baslik, ozet, liste, gorsel, cap):
    bas = ('<div style="display:flex;align-items:center;gap:9px;flex-wrap:wrap">'
           '<span style="font-family:' + SERIF + ';font-size:19px;font-weight:700;color:' + T["marka"] + ';line-height:1">' + str(no) + '</span>'
           '<span style="font-family:' + SERIF + ';font-size:16.5px;font-weight:700;line-height:1.2">' + baslik + '</span>' + rozet("tasarım taslağı", "taslak") + '</div>')
    alt = ('<div style="display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:18px;margin-top:8px">'
           '<div style="font-size:13px;line-height:1.5;color:' + T["ink2"] + '">' + ozet + '</div>'
           '<div>' + bullets(liste).replace('margin-top:7px', 'margin-top:0') + '</div></div>')
    return ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:13px;padding:13px 15px;display:flex;flex-direction:column;gap:7px">'
            + bas + '<div style="display:flex;justify-content:center">' + gorsel + '</div>'
            '<div style="font-size:10.5px;color:' + T["sessiz"] + ';text-align:center">' + cap + '</div>' + alt + '</div>')

def s5():
    ilke = ('<div style="background:' + T["markaA"] + ';border-radius:12px;padding:11px 14px">'
            '<b style="font-family:' + SERIF + ';font-size:14.5px;color:' + T["marka"] + '">İlk sürümü neden dar tuttuk</b>'
            '<div style="font-size:12px;line-height:1.5;color:' + T["ink2"] + ';margin-top:3px;max-width:90ch">'
            'Bir özellik ancak şu üç sorudan birini geçerse bugünkü sürüme girdi: personel görmese liste tamamlanmaz mı, '
            'yönetici görmese kaçırılan iş görünmez mi, bu olmadan denetimde kanıt verilemez mi. '
            'Geri kalanı silinmedi — tasarlandı, sıraya alındı.</div></div>')
    s1k = kart("S1", "Liste yazmak yerine kütüphaneden seçmek", "tasarım taslağı", "taslak",
               "İşletme türünüze göre hazır madde paketleri gelir; kütüphaneden seçip şubenize uyarlarsınız. "
               "Yeni şube açtığınızda ya da menü değiştiğinde listeyi baştan kurmazsınız.",
               ["Kafe, fırın, hızlı servis, lokanta paketleri — her biri liste ve madde seti",
                "Kütüphanedeki madde güncellenince kopyanız bozulmaz, “güncelleme var” uyarısı alır",
                "Kendi maddenizi eklersiniz; kütüphane maddesini şubeye göre değiştirebilirsiniz"],
               scaled(scr_kutuphane(1100, 620), 1100, 620, 0.31), "Madde kütüphanesi ve paketler")
    s2k = kart("S2", "Üretilen ile satılan karşılaştırılır", "tasarım taslağı", "taslak",
               "Kapanışta girilen üretim adedi kasa satışıyla karşılaştırılır; aradaki <b>açıklanamayan fark</b> sebepleriyle raporlanır. "
               "Amaç kimseyi yakalamak değil, farkı ölçülebilir hâle getirmek.",
               ["Fire, personel yemeği, ikram, kasaya geç giriş gibi sebepler seçilir; açıklama girilmeden kayıt kapanmaz",
                "Rapor şube ve vardiya düzeyinde: kişi adı, kişi puanı ve biyometri yok",
                "“Açıklanamıyor” cevabı bölge müdürüne yükselir"],
               scaled(scr_mutabakat(1100, 620), 1100, 620, 0.31), "Üretim–satış mutabakatı")
    return page(head("Sıradaki sürüm") + h1("Sonra ne geliyor", 27)
                + p("Bugün teslim edilen sürüm bilerek dar tutuldu; aşağıdakiler kapsam dışında kaldı ama silinmedi. "
                    "Bu bölümdeki on iki ekran, o satırların nasıl görüneceğini gösterir.")
                + ilke
                + taslak_bant("<b>Bu bölümdeki ekranlar tasarım taslağıdır.</b> Özellikler henüz geliştirilmedi; sıraları pilotta sizin "
                              "şubelerinizden çıkan ihtiyaca göre belirlenir. Sözleşme ve pilot ölçütleri yalnızca bugünkü sürümü kapsar.")
                + s1k + s2k + foot(5), gap=11)

def s6():
    s3k = kart("S3", "Neredeyse aynı iki fotoğraf işaretlenir", "tasarım taslağı", "taslak",
               "Aynı dosyanın ikinci kez gönderilmesi bugün de engelleniyor. Bu adımda, dosya farklı olsa bile "
               "birkaç saniye arayla aynı açıdan çekilmiş kareler “benzer kanıt” olarak işaretlenir.",
               ["Gönderim engellenmez; kayıt incelenmek üzere panoya düşer",
                "Benzerlik eşiği ayarlanır — gereksiz uyarı istemezsiniz",
                "Karar insanda kalır: sistem yalnızca “şuna bakın” der"],
               scaled(scr_benzer(760, 430), 760, 430, 0.45), "Benzer kanıt uyarısı")
    s4k = kart("S4", "Duyuruyu kimin okuduğu kayda geçer", "tasarım taslağı", "taslak",
               "Merkez duyurusu şubelere düşer; kimin okuduğu ve onayladığı rapor olur. "
               "“Gruba yazdım, gördü mü” sorusu sayıya dönüşür.",
               ["Ek dosya eklenir: fiyat listesi, mevzuat yazısı, görsel standart",
                "Okumayana otomatik hatırlatma gider",
                "Onay istenen duyuruda kişi “okudum” değil “uygulayacağım” der"],
               scaled(scr_duyuru(900, 520), 900, 520, 0.38), "Duyuru ve okundu raporu")
    s5k = kart("S5", "Liste yalnızca gerektiğinde uzar", "tasarım taslağı", "taslak",
               "Cevaba göre ek madde açılır: “Hayır” denince sebep ve fotoğraf, “ekipman arızalı” denince servis sorusu. "
               "Bugünkü sürümde kural tek ve sabittir; bu adımda şablona özel kural tanımlanır.",
               ["Normal gecede liste kısa kalır, sorun çıkınca derinleşir",
                "Aralık dışı ölçümde 30 dakika sonra ikinci ölçüm maddesi açılabilir",
                "Kurallar şablonda tanımlanır; personel tarafında görünmez"],
               scaled(scr_kosul(900, 520), 900, 520, 0.38), "Koşullu madde kuralları")
    return page(head("Sıradaki sürüm") + s3k + s4k + s5k + foot(6), gap=11)

def s7():
    s6k = kart_genis("S6", "Tek seferlik soruların cevabı raporda",
                     "Şube sıralaması, en çok başarısız olan maddeler, yapılamadı sebeplerinin dağılımı ve gecikme takibi tek sayfada; "
                     "Excel’e aktarılır ya da hesap açmadan açılan bir bağlantıyla paylaşılır.",
                     ["Isı haritası: hangi madde hangi şubede tekrar tekrar düşüyor",
                      "Sebep dağılımı “malzeme yok %38” diyorsa sorun operasyonda değil tedarikte",
                      "Aylık toplantıya hazır çıktı: ekran görüntüsü almaya gerek kalmaz"],
                     scaled(scr_raporlar(1100, 620), 1100, 620, 0.46), "Raporlar · ısı haritası, şube sıralaması, sebep dağılımı")
    s7k = kart_genis("S7", "Kaydın değişmediğini ekranda görmek",
                     "Her olay bugün de değiştirilemez biçimde kaydediliyor; bu adımda o kayıt arayüzden okunur hâle gelir "
                     "ve bağımsız bir zaman damgasıyla onaylanır.",
                     ["Filtreli olay listesi: kim, ne zaman, ne yaptı",
                      "Zincir doğrulama: tek bir kaydı değiştirmek zinciri kırar ve sayfada görünür",
                      "Zaman damgası: kaydın o tarihte var olduğunu üçüncü taraf doğrular"],
                     scaled(scr_izi(1000, 560), 1000, 560, 0.49), "Denetim izi · olay listesi ve zincir doğrulama")
    return page(head("Sıradaki sürüm") + s6k + s7k + foot(7), gap=11)

def s7b():
    s8k = kart_genis("S8", "Denetçi gelince dosyayı aramazsınız",
                     "Seçtiğiniz dönem için tek dosya: sıcaklık günlüğü, o dönemin listeleri, belge durumu ve rastgele seçilmiş kanıt örnekleri. "
                     "Denetçiye ya da marka merkezine, hesap açmadan, <b>48 saat</b> açık kalan salt-okunur bir bağlantı verirsiniz.",
                     ["Dosyada doğrulama kodu var: kaydın sonradan değişmediği aynı sayfadan kontrol edilir",
                      "Bağlantı tek şube ve tek dönem; istediğiniz an iptal edersiniz, her açılış kayda geçer",
                      "Personel adları maskelenir — denetçi işi görür, kişisel veri paylaşılmaz"],
                     scaled(scr_denetimdosyasi(1000, 560), 1000, 560, 0.49), "Denetim dosyası · içindekiler ve süreli denetçi bağlantısı")
    adim = lambda n, bas, met: ('<div style="flex:1;min-width:0;background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:11px;padding:11px 13px">'
                                '<div style="display:flex;align-items:center;gap:8px"><div style="width:22px;height:22px;border-radius:7px;background:' + T["marka"] +
                                ';color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none">' + str(n) + '</div>'
                                '<b style="font-size:13px">' + bas + '</b></div>'
                                '<div style="font-size:12px;line-height:1.5;color:' + T["ink2"] + ';margin-top:5px">' + met + '</div></div>')
    akis = ('<div style="display:flex;gap:10px">'
            + adim(1, "Dönemi seçin", "Şube ve tarih aralığı. Varsayılan son 90 gün; denetçi genelde bu kadarını ister.")
            + adim(2, "Dosya üretilir", "Günlükler, listeler, belgeler ve kanıt örnekleri tek PDF'te; kapakta doğrulama kodu.")
            + adim(3, "Bağlantıyı verin", "48 saat açık, salt-okunur. İş bitince iptal edersiniz; kim ne zaman açtı kayıtlıdır.")
            + '</div>')
    sinir = ('<div style="background:' + T["yuzey2"] + ';border-radius:12px;padding:11px 14px;font-size:12px;line-height:1.55;color:' + T["ink2"] + '">'
             '<b style="color:' + T["ink"] + '">Bağlantının sınırları:</b> tek şube ve tek dönem gösterir, indirilemez, arama motorlarına kapalıdır; '
             'personel adları maskelenir; süre dolunca ya da siz iptal edince aynı dakikada kapanır. Açılışlar (zaman ve IP) olay izine yazılır, '
             'yani dosyayı kimin gördüğü sonradan da bellidir.</div>')
    neden = ('<div style="background:' + T["markaA"] + ';border-radius:12px;padding:11px 14px">'
             '<b style="font-family:' + SERIF + ';font-size:14.5px;color:' + T["marka"] + '">Bugün de verebilirsiniz, ama üç dosya hâlinde</b>'
             '<div style="font-size:12px;line-height:1.5;color:' + T["ink2"] + ';margin-top:3px;max-width:90ch">'
             'İlk sürümde sıcaklık günlüğü, çalıştırma PDF\'i ve belge takvimi ayrı ayrı iniyor; denetçinin önüne koymadan önce '
             'birleştirmek sizin işiniz. Bu adım o işi kaldırır ve dosyayı kapıdan içeri girmeden paylaşılabilir hâle getirir.</div></div>')
    return page(head("Sıradaki sürüm") + s8k + akis + sinir + neden + foot(8), gap=11)

def s8():
    d1k = kart("D1", "Franchise’ta standart merkezden yayınlanır", "tasarım taslağı", "taslak",
               "Marka merkezi standart listeyi yayınlar; franchise işletmeleri kendi hesabında kullanır, uyum merkezden izlenir. "
               "Marka standardı ile işletmenin kendi verisi birbirine karışmaz.",
               ["Franchise standart maddeyi silemez, kendi maddesini ekleyebilir",
                "Merkez uyum oranını ve liste sürümünü görür; personel verisini görmez",
                "Yeni sürüm yayınlanınca eski sürümde kalan işletmeler işaretlenir"],
               scaled(scr_franchise(1000, 560), 1000, 560, 0.34), "Marka kütüphanesi ve uyum tablosu")
    d2k = kart("D2", "Aynı çekirdek, başka sektörler", "tasarım taslağı", "taslak",
               "Perakende zinciri, otel, akaryakıt istasyonu ve üretim için hazır şablon setleri. "
               "Zincirinizin birden fazla işi varsa hepsi tek hesapta yürür.",
               ["Değişen yalnızca maddeler, ölçüm aralıkları ve mevzuat notları",
                "Tekrarlı liste, kanıt, aksiyon ve denetim PDF’i aynı kalır",
                "Bir paketle başlar, kendi maddelerinizle devam edersiniz"],
               scaled(scr_paketler(900, 500), 900, 500, 0.38), "Sektör paketleri")
    d3k = kart("D3", "Kasadan ve İK’dan veri kendiliğinden gelir", "tasarım taslağı", "taslak",
               "Satış verisi kasadan, personel ve vardiya bilgisi İK sisteminden alınır; atamalar ve mutabakat "
               "elle veri girişi olmadan çalışır.",
               ["Bağlantı tek yönlü: veri okunur, karşı sisteme yazılmaz",
                "Şube ↔ kasa eşlemesi kurulumda bir kez yapılır",
                "Hangi alanların alındığı sözleşme ekinde listelenir"],
               scaled(scr_entegrasyon(900, 520), 900, 520, 0.38), "Entegrasyon ayarları ve eşleme")
    return page(head("Daha sonra") + h1("Büyüyünce gerekecekler", 27)
                + p("Bu satırlar birkaç yüz şubeye, birden fazla markaya ya da başka bir sektöre geçildiğinde anlamlı olur; "
                    "bugünkü sürümün sahada çalıştığını görmeden sıraya alınmazlar.")
                + d1k + d2k + d3k + foot(9), gap=11)

def s9():
    d4k = kart_genis("D4", "Beyana değil ölçüme dayanan sayaç",
                     "Fırın ağzı veya tezgâh kamerası üretilen adedi sayar ve kasa satışıyla karşılaştırır. "
                     "Sayımı yapan kişi işin içindeyse beyan tek başına yetmez; bu sayaç bağımsız ikinci kaynaktır.",
                     ["Kamera yalnızca tezgâhı görür ve ürün sayar: yüz tanıma, kimlik tespiti ve kişi takibi yok",
                      "Hedef doğruluk ±%3; eşiğin altındaki farklar raporlanmaz",
                      "Hukuk görüşü, personele duyuru ve yasak alan kuralları olmadan kurulmaz"],
                     scaled(scr_kamera(1000, 560), 1000, 560, 0.66), "Kamera ile üretim sayımı · saatlik üretim ve kasa karşılaştırması")
    siralama = ('<div style="background:' + INK_BAND + ';border-radius:13px;padding:15px 20px;display:flex;flex-direction:column;gap:6px">'
                + label("Sıradakini siz belirlersiniz", "rgba(255,255,255,.55)")
                + h1("Yol haritası tahminle değil sayıyla sıralanır", 22, "#fff", "40ch")
                + p("Pilot boyunca hangi eksiğin canınızı yaktığını ölçeriz: kaç kez “bu listeyi kütüphaneden alabilsem”, "
                    "kaç kez “bu raporu Excel’e alsam” dediniz. Sıradaki sürümün içeriği bu sayılardan çıkar — tahminimizden değil.",
                    12.5, "rgba(255,255,255,.78)", "88ch") + '</div>')
    kapanis = taslak_bant("<b>Bu bölümdeki ekranlar üründe yok.</b> Tasarım taslağı olarak hazırlandılar; ne zaman geliştirilecekleri "
                          "pilot sonrası kararlaştırılır. Satın aldığınız ve pilot ölçütlerinin bağladığı kapsam, bu föyün ilk dört sayfasıdır.")
    iletisim = ('<div style="display:flex;align-items:center;justify-content:space-between;gap:16px;border-top:1px solid ' + T["cizgi"] + ';padding-top:11px">'
                '<div style="display:flex;flex-direction:column;gap:3px">' + w(21) +
                '<div style="font-size:11.5px;color:' + T["sessiz"] + '">Şube operasyonları, kanıtıyla.</div></div>'
                '<div style="font-size:13px;color:' + T["ink"] + ';text-align:right;line-height:1.55">'
                '<b>[Ad Soyad]</b> · [telefon]<br><span style="color:' + T["ink2"] + '">[e-posta] · [alan adı]</span></div></div>')
    return page(head("Daha sonra") + d4k + siralama + kapanis + iletisim
                + foot(10, "Talimatname çalışma adıdır; ekranlardaki veriler örnektir."), gap=11)

# ---------------------------------------------------------------- üretim
PAGES = {"Main.dc.html": s1, "O2.dc.html": s2, "O3.dc.html": s3, "O4.dc.html": s4,
         "O5.dc.html": s5, "O6.dc.html": s6, "O7.dc.html": s7, "O7b.dc.html": s7b, "O8.dc.html": s8, "O9.dc.html": s9}
SCREENS = {"Sablonlar.dc.html": scr_sablon, "Cevrimdisi.dc.html": scr_offline, "Bayraklar.dc.html": scr_bayrak, "BelgeTakvimi.dc.html": scr_belge,
           "Kutuphane.dc.html": scr_kutuphane, "Mutabakat.dc.html": scr_mutabakat, "BenzerKanit.dc.html": scr_benzer,
           "Duyuru.dc.html": scr_duyuru, "KosulluMadde.dc.html": scr_kosul, "Raporlar.dc.html": scr_raporlar,
           "DenetimIzi.dc.html": scr_izi, "Franchise.dc.html": scr_franchise, "SektorPaketleri.dc.html": scr_paketler,
           "Entegrasyon.dc.html": scr_entegrasyon, "KameraSayim.dc.html": scr_kamera,
           "DenetimDosyasi.dc.html": scr_denetimdosyasi}

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    for name, fn in list(PAGES.items()) + list(SCREENS.items()):
        open(os.path.join(OUTDIR, name), "w", encoding="utf-8").write(B.dc(fn()))
    ab = [{"file": n, "title": "Özellik föyü · sayfa " + str(i + 1), "x": i * 880, "y": 0, "w": 794, "h": 1123, "print": "fixed"}
          for i, n in enumerate(PAGES)]
    for i, (n, t, ww, hh) in enumerate([("Sablonlar.dc.html", "Ekran · şablonlar (web)", 1200, 760),
                                        ("Kutuphane.dc.html", "Taslak · madde kütüphanesi", 1100, 620),
                                        ("Mutabakat.dc.html", "Taslak · üretim–satış mutabakatı", 1100, 620),
                                        ("BenzerKanit.dc.html", "Taslak · benzer kanıt uyarısı", 760, 430),
                                        ("Duyuru.dc.html", "Taslak · duyuru ve okundu onayı", 900, 520),
                                        ("KosulluMadde.dc.html", "Taslak · koşullu maddeler", 900, 520),
                                        ("Raporlar.dc.html", "Taslak · ayrıntılı raporlar", 1100, 620),
                                        ("DenetimIzi.dc.html", "Taslak · denetim izi", 1000, 560),
                                        ("Franchise.dc.html", "Taslak · franchise marka kütüphanesi", 1000, 560),
                                        ("SektorPaketleri.dc.html", "Taslak · sektör paketleri", 900, 500),
                                        ("Entegrasyon.dc.html", "Taslak · POS ve İK entegrasyonları", 900, 520),
                                        ("KameraSayim.dc.html", "Taslak · kamera ile üretim sayımı", 1000, 560),
                                        ("DenetimDosyasi.dc.html", "Taslak · denetim dosyası ve denetçi bağlantısı (E-13)", 1000, 560),
                                        ("Cevrimdisi.dc.html", "Ekran · çevrimdışı (mobil)", 390, 844),
                                        ("Bayraklar.dc.html", "Ekran · kanıt bayrakları (web)", 900, 520),
                                        ("BelgeTakvimi.dc.html", "Ekran · belge takvimi (web, SCR-W-14)", 1200, 760)]):
        ab.append({"file": n, "title": t, "x": i * 1320, "y": 1280, "w": ww, "h": hh})
    json.dump({"artboards": ab, "launch": {"view": "canvas"}}, open(os.path.join(OUTDIR, "canvas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    css = ("body{margin:0;background:#e9e6de;font-family:" + SANS + "} .sheet{margin:18px auto;box-shadow:0 10px 30px rgba(28,33,40,.14);width:794px} "
           "@media print{body{background:#fff}.sheet{margin:0;box-shadow:none}.sheet+.sheet{break-before:page}@page{size:A4;margin:0}}")
    html = ('<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Talimatname özellik föyü</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bitter:wght@700&display=swap">'
            '<style>' + css + '</style></head><body>'
            + "".join('<div class="sheet">' + fn() + '</div>' for fn in PAGES.values()) + '</body></html>')
    out = os.path.join(HERE, "talimatname-ozellikler.html")
    open(out, "w", encoding="utf-8").write(html)

    css2 = ("body{margin:0;background:#e9e6de;font-family:" + SANS + "}"
            ".page{width:100%;display:flex;justify-content:center;padding:14px 8px}"
            ".box{width:794px;transform-origin:top center;box-shadow:0 10px 30px rgba(28,33,40,.14)}"
            "@media print{body{background:#fff}.page{padding:0}.box{transform:none!important;box-shadow:none}"
            ".page+.page{break-before:page}@page{size:A4;margin:0}}")
    js = ("<script>(function(){function f(){var w=Math.min(document.documentElement.clientWidth-16,794);var s=w/794;"
          "document.querySelectorAll('.page').forEach(function(pg){var b=pg.querySelector('.box');b.style.transform='scale('+s+')';"
          "pg.style.height=(1123*s+28)+'px';});}f();addEventListener('resize',f);})();</script>")
    html2 = ('<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
             '<title>Talimatname Özellik Föyü</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bitter:wght@700&display=swap">'
             '<style>' + css2 + '</style>'
             + "".join('<div class="page"><div class="box">' + fn() + '</div></div>' for fn in PAGES.values()) + js)
    open(os.path.join(HERE, "talimatname-ozellikler-sayfa.html"), "w", encoding="utf-8").write(html2)
    print("ok:", len(PAGES), "sayfa,", len(SCREENS), "yeni ekran")

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
        print(pdf, "ok" if os.path.exists(pdf) else "HATA")

if __name__ == "__main__":
    main()
