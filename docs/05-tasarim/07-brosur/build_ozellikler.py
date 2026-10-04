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

SAYFA = 5

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
    return ('<div style="width:150px;height:200px;background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';box-shadow:0 8px 20px rgba(28,33,40,.14);'
            'padding:12px;display:flex;flex-direction:column;gap:6px;flex:none">'
            '<div style="display:flex;justify-content:space-between;align-items:center">'
            '<div style="font-family:' + SERIF + ';font-size:9px;font-weight:700">' + baslik + '</div>'
            '<div style="width:16px;height:16px;background:' + T["ink"] + ';border-radius:2px"></div></div>'
            '<div style="font-size:7px;color:' + rozet_c + ';font-weight:700">' + rozet_t + '</div>'
            + "".join(line(x, c) for x, c in satirlar) + kareler
            + '<div style="margin-top:auto;font-size:6.5px;color:' + T["sessiz"] + ';font-family:ui-monospace,Menlo,monospace">Doğrulama ' + kod + '</div></div>')

# ---------------------------------------------------------------- sayfalar
def icindekiler():
    oge = lambda n, t, sf: ('<div style="display:flex;gap:7px;align-items:baseline;font-size:11.5px;line-height:1.4">'
                            '<span style="color:' + T["marka"] + ';font-weight:700;width:14px;flex:none">' + str(n) + '</span>'
                            '<span style="flex:1;min-width:0">' + t + '</span>'
                            '<span style="color:' + T["sessiz"] + ';flex:none">s.' + str(sf) + '</span></div>')
    ler = [("Kurulum sihirbazı ve dört rol", 1), ("Sekiz hazır şablon, altı madde türü", 1), ("Kiosk ve PIN ile giriş", 2),
           ("Ölçüm maddeleri ve tek sabit kural", 2), ("Yapılamadı akışı", 2), ("Çevrimdışı çalışma", 3),
           ("Sabit eskalasyon ve 07:00 sabah özeti", 3), ("İstisna panosu", 3), ("Çalıştırma detayı ve kanıt bütünlüğü", 4),
           ("Belge ve periyodik bakım takvimi", 4), ("Denetimde verilen belgeler", 4)]
    kol = "".join(oge(i + 1, t, sf) for i, (t, sf) in enumerate(ler))
    return ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:12px;padding:12px 15px">'
            + label("v1'de gelen on bir özellik") +
            '<div style="column-count:2;column-gap:26px;margin-top:7px">' + kol + '</div>'
            '<div style="font-size:11px;color:' + T["sessiz"] + ';margin-top:8px;border-top:1px solid ' + T["cizgi"] + ';padding-top:7px">'
            'Son sayfada v1.1 ve v2: bilerek ertelenen satırlar, neden ertelendikleriyle.</div></div>')

def s1():
    giris = ('<div style="background:' + INK_BAND + ';border-radius:14px;padding:20px 24px;display:flex;flex-direction:column;gap:9px">'
             + label("Yol haritasının uzun hâli", "rgba(255,255,255,.55)")
             + h1("Hangi özellik ne yapar,<br>ekranda nasıl görünür", 28, "#fff", "26ch")
             + p("Broşürdeki yol haritası tablosunda her satır tek cümleydi. Bu föy, <b>v1'de gelen on bir özelliği</b> birer ekranla "
                 "ve kısa açıklamayla gösterir; v1.1 ve v2 satırları son sayfada, henüz ekranı olmadığı için yalnızca metinle anlatılır.",
                 13, "rgba(255,255,255,.78)", "70ch") + '</div>')
    k1 = kart(1, "Kurulum sihirbazı ve dört rol", "web", "web",
              "Merkez hesabı dört adımda kurar: marka ve şubeler (Excel'den), şablon, plan, personel. Roller sabittir — Yönetici, "
              "Bölge müdürü, Şube müdürü, Personel — ve herkes yalnızca kendi kapsamını görür.",
              ["25 satırlık şube dosyası tek seferde yüklenir; hatalı satırlar rapor olarak döner",
               "Pencere saatleri şubenin kendi çalışma saatinden hesaplanır; gece yarısını aşan pencere aynı iş gününe yazılır",
               "İlk şubenin kurulumu ~1 saat; liste aynı gece açılır"],
              scaled(TT.scr_wizard(1200, 760), 1200, 760, 0.28), "Kurulum sihirbazı · adım 3")
    k2 = kart(2, "Sekiz hazır şablon, altı madde türü", "web", "web",
              "Kapanış, açılış, saatlik hijyen, soğuk zincir, haftalık derin temizlik, fritöz yağı, kasa devri ve teslimat kabul "
              "listeleri 73 maddeyle hazır gelir. Kopyalanır, şubeye göre düzenlenir; yayındaki sürüm bozulmaz.",
              ["Altı madde türü: onay, çoktan seçmeli, sayı, sıcaklık, metin, fotoğraf (1–3) — artı talimat satırı",
               "Her madde zorunlu / fotoğraf zorunlu / kritik olarak işaretlenebilir",
               "Şablon sürümlenir: düzenleme yeni sürüm açar, çalışan planlar etkilenmez"],
              scaled(scr_sablon(1200, 760), 1200, 760, 0.28), "Şablonlar ve madde türleri")
    return page(head("v1 · 1–2") + giris + icindekiler() + k1 + k2 + foot(1), gap=13)

def s2():
    k3 = kart(3, "Kiosk ve PIN ile giriş", "kiosk / mobil", "mobil",
              "Şube tableti tek hesapla açık durur; personel kendi adına dokunup dört haneli PIN'ini girer. Telefonu olmayan "
              "personel de kayıt dışı kalmaz — şube müdürü PIN'i kendisi atar.",
              ["İki dakika hareketsizlikte kilitlenir, kaldığı yerden devam eder",
               "Listeyi ilk açan alır; diğer cihazlarda “Emre yapıyor” görünür",
               "İsteyen kendi telefonundan tamamlar; kiosk zorunlu değil"],
              scaled(B.scr_kiosk(), 390, 844, 0.30), "Kapanış listesi · şube tableti")
    k4 = kart(4, "Ölçüm maddeleri ve tek sabit kural", "mobil", "mobil",
              "Sıcaklık gibi ölçümlerde kabul aralığı maddenin içinde yazar. “Hayır”, “uygun değil” veya aralık dışı cevap tek bir "
              "sabit kuralı işletir: fotoğraf ve not zorunlu; madde kritikse aksiyon açılır ve anında bildirilir.",
              ["Kural v1'de ayarlanmaz — her şubede aynı çalışır, ayar labirenti yok",
               "Kritik maddede şube ve bölge müdürüne anında push; 10 dakikada okunmazsa SMS",
               "Girilen her ölçüm sıcaklık günlüğüne düşer"],
              scaled(B.scr_temp(), 390, 844, 0.30), "Aralık dışı ölçüm · kural devrede")
    k5 = kart(5, "Yapılamadı akışı", "mobil", "mobil",
              "Personel yapamadığı maddeyi sebebiyle bildirir. İş sessizce kaybolmaz: şube müdürüne 72 saatlik aksiyon olarak düşer "
              "ve ertesi sabah açılış listesinin başında görünür.",
              ["Sabit sebep seti: malzeme yok · ekipman arızalı · zaman yetmedi · yetkim yok · diğer (not zorunlu)",
               "“Dün gece” bloğu: önceki vardiyanın yapılamayan ve başarısız maddeleri",
               "Aksiyon kapanırken not zorunlu; kapanış olay izine yazılır"],
              scaled(TT.scr_unable(), 390, 844, 0.30), "Yapılamadı · sebep seçimi")
    return page(head("v1 · 3–5") + k3 + k4 + k5 + foot(2), gap=12)

def s3():
    k6 = kart(6, "Çevrimdışı çalışma", "mobil", "mobil",
              "Mutfakta bağlantı kesilse de liste cihazda devam eder. Kayıtlar 72 saate kadar kuyrukta bekler, bağlantı gelince "
              "sırayla gönderilir; hiçbir cevap “internet yoktu” diye kaybolmaz.",
              ["Fotoğraf cihazda ~300 KB'a sıkıştırılır, kuyrukta saklanır",
               "Zaman damgası cihaz saatiyle değil sunucu saatiyle düzeltilir",
               "24 saatten geç senkronlanan kayıt bayrakla işaretlenir"],
              scaled(scr_offline(), 390, 844, 0.30), "Çevrimdışı · kuyrukta bekleyen kayıtlar")
    k7 = kart(7, "Sabit eskalasyon ve 07:00 sabah özeti", "mobil / e-posta", "mobil",
              "Kimin neyi ne zaman öğreneceği sabittir ve tek yerde yazar. Gece kimse aranmaz: yalnızca kritik maddeler anında "
              "bildirilir, gerisi sabah 07:00 özetinde toplanır.",
              ["Kaçırılan liste → şube müdürüne anında, bölge müdürüne 07:00 özetinde",
               "Sessiz saat 23:00–07:00; yöneticiye gece yalnızca kritik bildirim",
               "Özet push ve e-posta olarak aynı metinle gider"],
              scaled(B.scr_morning(), 390, 844, 0.30), "Sabah özeti · bölge müdürü")
    k8 = kart(8, "İstisna panosu", "web", "web",
              "Merkez ekranının varsayılanı “her şey yolunda”dır: yalnızca dikkat isteyen şube × liste hücreleri listelenir. "
              "Sorunsuz bir gün tek cümleyle cevaplanır.",
              ["Altı sayı: zamanında, geç, başarısız, kaçırıldı, yapılamadı, açık aksiyon",
               "Izgarada tüm gün tek bakışta; hücreden çalıştırma detayına tek tıkla",
               "Gün, bölge ve “şüpheli kanıt” filtreleri"],
              scaled(B.scr_pano(1200, 760), 1200, 760, 0.28), "Operasyon panosu · merkez")
    return page(head("v1 · 6–8") + k6 + k7 + k8 + foot(3), gap=12)

def s4():
    k9 = kart(9, "Çalıştırma detayı ve kanıt bütünlüğü", "web", "web",
              "Bir gecenin tamamı tek sayfada: madde madde cevaplar, fotoğraflar, aksiyonlar ve olay izi. Kanıt sonradan "
              "değiştirilemez — dosya sunucuda damgalanır, SHA-256 özeti cevaba bağlanır, kayıt kilitlenir.",
              ["Aynı fotoğraf ikinci kez gönderilemez; deneme olay izine yazılır",
               "Galeri denemesi, şube dışı konum, cihaz saati farkı ve geç senk bayrak olarak görünür",
               "Bayrak suçlama değil, incelemeye çağrıdır — kişi puanına dönüşmez"],
              scaled(scr_bayrak(900, 520), 900, 520, 0.36), "Kanıtlar ve bütünlük bayrakları")
    k10 = kart(10, "Belge ve periyodik bakım takvimi", "web", "web",
               "Yangın tüpü dolumu, baca ve su deposu temizliği, periyodik elektrik kontrolü, hijyen eğitimi ve portör belgeleri "
               "tarihleriyle kayıtlıdır. Süre dolmadan uyarır; geçerse kendiliğinden iş açar.",
               ["Bitişe 30 ve 7 gün kala sorumluya ve şube müdürüne bildirim",
                "Tarih geçince yüksek öncelikli aksiyon açılır, şube “belge eksik” işaretlenir",
                "Zincir genelinde yaklaşanlar ve geçmişler tek listede; dönem PDF'i denetimde verilir"],
               scaled(scr_belge(1200, 760), 1200, 760, 0.28), "Belge takvimi · zincir görünümü")
    pdf_grup = ('<div style="display:flex;gap:9px">'
              + paper("Çalıştırma raporu", "BAŞARISIZ · kritik madde", T["kritik"],
                      [("90", None), ("70", None), ("85", None), ("60", T["kritikA"]), ("80", None)], kare=True)
              + paper("Aylık özet", "EYLÜL · 12 ŞUBE", T["marka"],
                      [("85", None), ("65", T["markaA"]), ("75", None), ("55", None), ("80", None), ("70", T["markaA"]), ("60", None)], kod="TN-9B2E1-44AC")
              + paper("Sıcaklık günlüğü", "1–30 EYLÜL · 3 ÖLÇÜM/GÜN", T["marka"],
                      [("90", None), ("88", None), ("86", None), ("84", T["kritikA"]), ("88", None), ("85", None), ("80", None)], kod="TN-3C7D0-18BF") + '</div>')
    pdfler = scaled(pdf_grup, 468, 200, 0.64)
    k11 = kart(11, "Denetimde verilen belgeler", "PDF", "pdf",
               "Üç çıktı doğrulama kodlu PDF olarak iner: bir gecenin tamamını fotoğraflarıyla gösteren çalıştırma raporu, "
               "aylık tek sayfa özet ve HACCP sıcaklık günlüğü. Denetçi kaydı sayfadan okur.",
               ["Her PDF üretim zamanı ve doğrulama kodu taşır",
                "Hangi ölçümün ne zaman, kim tarafından girildiği satır satır görünür",
                "Kanıt dosyaları 24 ay saklanır, sonra otomatik silinir"],
               pdfler, "Çalıştırma raporu · aylık özet · sıcaklık günlüğü", sol_w=302)
    ilke = ('<div style="background:' + T["markaA"] + ';border-radius:12px;padding:12px 15px">'
            '<b style="font-family:' + SERIF + ';font-size:15px;color:' + T["marka"] + '">Bir özellik v1’e nasıl girdi?</b>'
            '<div style="font-size:12.5px;line-height:1.5;color:' + T["ink2"] + ';margin-top:4px;max-width:80ch">'
            'Üç sorudan birine “evet” gerekiyordu: <b>1)</b> Personel bunu görmese kapanış listesi tamamlanmaz mı? '
            '<b>2)</b> Yönetici bunu görmese kaçırılan iş görünmez mi? <b>3)</b> Bu olmadan denetimde kanıt verilemez mi? '
            'Hayır olan her satır v1.1’e yazıldı, silinmedi (ADR-0008).</div></div>')
    return page(head("v1 · 9–11") + k9 + k10 + k11 + ilke + foot(4), gap=12)

def s5():
    def oge(ad, aciklama):
        return ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:11px;padding:10px 12px">'
                '<b style="font-size:13px">' + ad + '</b>'
                '<div style="font-size:12px;line-height:1.45;color:' + T["ink2"] + ';margin-top:3px">' + aciklama + '</div></div>')
    v11 = ("".join([
        oge("Madde kütüphanesi ve işletme türü paketleri",
            "Şablon sıfırdan yazılmaz: kafe, fırın, hızlı servis gibi türlere göre hazır madde paketleri gelir; kütüphaneden seçip şubeye uyarlarsınız. "
            "Kütüphane maddesi güncellenince türetilmiş maddeler “güncelleme var” işareti alır (ADR-0010)."),
        oge("Yakın kopya fotoğraf tespiti",
            "Aynı dosya v1'de zaten engelleniyor. v1.1'de birkaç saniye arayla çekilmiş, neredeyse aynı kareler de algısal karşılaştırmayla “benzer kanıt” olarak işaretlenir."),
        oge("Üretim–satış mutabakatı",
            "Kapanışta girilen üretim adedi POS satışıyla karşılaştırılır; aradaki <b>açıklanamayan fark</b> sebep setiyle birlikte raporlanır. "
            "Şube ve vardiya düzeyinde; kişi puanı ve biyometri yok (ADR-0011)."),
        oge("Duyuru ve okundu onayı",
            "Merkez duyurusu şubelere düşer, kimin okuduğu ve onayladığı rapor olur — “gruba yazdım, gördü mü” sorusu biter."),
        oge("Koşul editörü",
            "Madde cevabına göre ek madde açılır: “ekipman arızalı” denince servis bilgisi, “Hayır” denince ek fotoğraf. v1'de kural tek ve sabittir."),
        oge("Ayrıntılı raporlar",
            "Şube sıralaması, başarısız madde ısı haritası, yapılamadı sebep dağılımı, kişi düzeyinde gecikme takibi, Excel ve paylaşım bağlantısı."),
        oge("Denetim izi ekranı",
            "Olay günlüğü v1'de de tutuluyor ama ekranı yok; v1.1'de filtrelenebilir liste, zincir doğrulama ve RFC 3161 zaman damgası gelir."),
    ]))
    v2 = ("".join([
        oge("Franchise marka kütüphanesi",
            "Marka merkezi standart listeyi yayınlar, franchise işletmeleri kendi hesabında kullanır; uyum merkezden izlenir."),
        oge("Başka sektör paketleri",
            "Perakende zinciri, otel, akaryakıt istasyonu, üretim gibi dikeylere hazır şablon ve madde paketleri."),
        oge("POS ve İK entegrasyonları",
            "Personel ve vardiya bilgisi İK sisteminden, satış verisi POS'tan gelir; atama ve mutabakat elle veri girişi olmadan çalışır."),
        oge("Kamera ile üretim sayımı",
            "Fırın ağzı veya tezgâh kamerası üretilen adedi sayar, satışla karşılaştırır. Hukuk görüşü ve ölçüm doğrulaması (±%3 hedefi) olmadan başlanmaz; "
            "kimlik tanıma ve biyometri hiçbir kademede yok."),
    ]))
    not_ = ('<div style="background:' + T["uyariA"] + ';border-radius:11px;padding:11px 13px;font-size:12px;line-height:1.5;color:' + T["ink2"] + '">'
            '<b>Bu sayfada ekran yok, çünkü henüz çizilmedi.</b> v1.1 ve v2 satırlarının kapsamı ve sırası pilot bulgularına göre belirlenir; '
            'bir özellik yol haritasına ancak sahadan gelen bir sinyalle girer. Taahhüt edilen tek şey v1’lerdir.</div>')
    return page(head("v1.1 ve v2") + h1("Sonra ne geliyor", 28)
                + p("Bu satırlar v1'in kapsamı dışında. Burada olmaları “yapılacak” sözü değil, “bilerek ertelendi” kaydıdır: "
                    "ilk sürüm dar tutuldu ki pilot dört haftada ölçülebilsin.")
                + label("v1.1 — pilot sonrası, sıra bulgularla belirlenir")
                + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">' + v11 + '</div>'
                + label("v2 — entegrasyon ve yeni dikeyler")
                + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">' + v2 + '</div>'
                + not_ + foot(5, "Talimatname çalışma adıdır; ekranlardaki veriler örnektir."), gap=11)

# ---------------------------------------------------------------- üretim
PAGES = {"Main.dc.html": s1, "O2.dc.html": s2, "O3.dc.html": s3, "O4.dc.html": s4, "O5.dc.html": s5}
SCREENS = {"Sablonlar.dc.html": scr_sablon, "Cevrimdisi.dc.html": scr_offline, "Bayraklar.dc.html": scr_bayrak, "BelgeTakvimi.dc.html": scr_belge}

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    for name, fn in list(PAGES.items()) + list(SCREENS.items()):
        open(os.path.join(OUTDIR, name), "w", encoding="utf-8").write(B.dc(fn()))
    ab = [{"file": n, "title": "Özellik föyü · sayfa " + str(i + 1), "x": i * 880, "y": 0, "w": 794, "h": 1123, "print": "fixed"}
          for i, n in enumerate(PAGES)]
    for i, (n, t, ww, hh) in enumerate([("Sablonlar.dc.html", "Ekran · şablonlar (web)", 1200, 760),
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
