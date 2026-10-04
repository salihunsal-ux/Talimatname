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
            'Son sayfa: bugünkü sürümün dışında kalanlar ve neden beklediği.</div></div>')

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

def s5():
    def oge(ad, aciklama):
        return ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:11px;padding:9px 12px">'
                '<b style="font-size:13px">' + ad + '</b>'
                '<div style="font-size:12px;line-height:1.45;color:' + T["ink2"] + ';margin-top:3px">' + aciklama + '</div></div>')
    ilke = ('<div style="background:' + T["markaA"] + ';border-radius:12px;padding:12px 15px">'
            '<b style="font-family:' + SERIF + ';font-size:15px;color:' + T["marka"] + '">İlk sürümü neden dar tuttuk</b>'
            '<div style="font-size:12.5px;line-height:1.5;color:' + T["ink2"] + ';margin-top:4px;max-width:86ch">'
            'Bir özellik ancak şu üç sorudan birini geçerse ilk sürüme girdi: <b>1)</b> Personel bunu görmese kapanış listesi tamamlanmaz mı? '
            '<b>2)</b> Yönetici bunu görmese kaçırılan iş görünmez mi? <b>3)</b> Bu olmadan denetimde kanıt verilemez mi? '
            'Geri kalanı silinmedi, sıraya alındı — böylece pilot dört haftada ölçülebiliyor ve ürün ayar labirentine dönüşmüyor.</div></div>')
    v11 = ("".join([
        oge("Madde kütüphanesi ve işletme türü paketleri",
            "Kafe, fırın, hızlı servis gibi işletme türlerine göre hazır madde paketleri; listeyi sıfırdan yazmak yerine kütüphaneden seçip "
            "şubenize uyarlarsınız. Kütüphanedeki madde güncellenince türetilmiş maddeler uyarı alır."),
        oge("Benzer fotoğraf tespiti",
            "Aynı dosyanın yeniden gönderilmesi bugün de engelleniyor. Sıradaki sürümde birkaç saniye arayla çekilmiş, neredeyse aynı kareler de "
            "“benzer kanıt” olarak işaretlenir."),
        oge("Üretim–satış mutabakatı",
            "Kapanışta girilen üretim adedi POS satışıyla karşılaştırılır; aradaki <b>açıklanamayan fark</b> sebepleriyle birlikte raporlanır. "
            "Şube ve vardiya düzeyinde: kişi puanı ve biyometri yok."),
        oge("Duyuru ve okundu onayı",
            "Merkez duyurusu şubelere düşer; kimin okuduğu ve onayladığı rapor olur — “gruba yazdım, gördü mü” sorusu biter."),
        oge("Koşullu maddeler",
            "Cevaba göre ek madde açılır: “ekipman arızalı” denince servis bilgisi, “Hayır” denince ek fotoğraf. Bugünkü sürümde kural tek ve sabittir."),
        oge("Ayrıntılı raporlar",
            "Şube sıralaması, en çok başarısız olan maddeler, yapılamadı sebeplerinin dağılımı, gecikme takibi, Excel ve paylaşım bağlantısı."),
        oge("Denetim izi ekranı",
            "Her olay bugün de değiştirilemez biçimde kaydediliyor; sıradaki sürümde bu kayıt arayüzden okunur hâle gelir ve nitelikli zaman damgası eklenir."),
    ]))
    v2 = ("".join([
        oge("Franchise marka kütüphanesi",
            "Marka merkezi standart listeyi yayınlar, franchise işletmeleri kendi hesabında kullanır; uyum merkezden izlenir."),
        oge("Başka sektör paketleri",
            "Perakende zinciri, otel, akaryakıt istasyonu, üretim gibi alanlara hazır şablon ve madde paketleri."),
        oge("POS ve İK entegrasyonları",
            "Personel ve vardiya bilgisi İK sisteminden, satış verisi kasadan gelir; atamalar ve mutabakat elle veri girişi olmadan çalışır."),
        oge("Kamera ile üretim sayımı",
            "Fırın ağzı veya tezgâh kamerası üretilen adedi sayar ve satışla karşılaştırır. Hukuki görüş ve ölçüm doğrulaması olmadan başlanmaz; "
            "kimlik tanıma ve biyometri hiçbir aşamada yok."),
    ]))
    not_ = ('<div style="background:' + T["uyariA"] + ';border-radius:11px;padding:11px 13px;font-size:12px;line-height:1.5;color:' + T["ink2"] + '">'
            '<b>Bu sayfada ekran yok, çünkü bu özellikler henüz tasarlanmadı.</b> Pilot ölçütleri ve sözleşme yalnızca bugünkü sürümü kapsar; '
            'buradaki satırlar söz değil, sıraya alınmış işlerdir. Sıralarını pilotta sizin şubelerinizden çıkan ihtiyaç belirler.</div>')
    return page(head("Yol haritası") + h1("Sonra ne geliyor", 27)
                + p("Bugün teslim edilen sürüm bilerek dar tutuldu. Aşağıdakiler kapsam dışında kaldı — ama silinmedi, sıraya alındı.")
                + ilke
                + label("Sıradaki sürüm — pilot sonrası")
                + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">' + v11 + '</div>'
                + label("Daha sonra")
                + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">' + v2 + '</div>'
                + not_ + foot(5, "Talimatname çalışma adıdır; ekranlardaki veriler örnektir."), gap=9)

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
