# -*- coding: utf-8 -*-
"""Talimatname tanıtım broşürü (A4, 2 sayfa) + gerçeğe yakın ekran tasarımları.
Üretir: Main.dc.html (sayfa 1), Sayfa2.dc.html, KioskListe/Sicaklik/SabahOzeti/Pano .dc.html (ekranlar), canvas.json
(tasarım tuvali için) ve talimatname-brosur.html (yazdırma; --pdf ile PDF).
Token’lar 05-tasarim/04-tasarim-sistemi.md’den; marka işareti marka/build_refined.py (Mühür sistemi)."""
import os, sys, subprocess, tempfile, time, json

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
T = dict(zemin="#f7f5ef", yuzey="#ffffff", yuzey2="#efece4", ink="#1c2128", ink2="#4b5560", sessiz="#7b8590", cizgi="#d6d9d2",
         marka="#1f6f5b", markaA="#dcebe5", kritik="#b8452f", kritikA="#f3ddd8", uyari="#b7791f", uyariA="#f6ebd2", pasif="#c9ced6")
SANS = '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif'  # tırnaksız: style="..." içinde çift tırnak attribute'u keser
SERIF = 'Bitter, Georgia, Times New Roman, serif'
MARK = ('<svg viewBox="0 0 64 64" width="{s}" height="{s}" style="flex:none"><path d="M14 4 H38 L48 14 V56 A4 4 0 0 1 44 60 H14 A4 4 0 0 1 10 56 V8 A4 4 0 0 1 14 4 Z" fill="#1c2128"></path>'
        '<path d="M38 4 V14 H48 Z" fill="#f7f5ef"></path><rect x="17" y="22" width="20" height="4" rx="2" fill="#f7f5ef"></rect><rect x="17" y="31" width="14" height="4" rx="2" fill="#f7f5ef"></rect>'
        '<circle cx="46" cy="46" r="14" fill="#1f6f5b" stroke="#f7f5ef" stroke-width="3"></circle><path d="M39 46.5 L44 51.5 L53.5 41" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>')

def _pdf_damga(pdf_yolu):
    """PDF üretilince yan damga dosyası: bayat PDF'i uretim_kontrol.py yakalar."""
    import uretim_kontrol as UK
    ad = os.path.basename(os.path.abspath(__file__))
    kaynak = next((y for y in UK.PDF_HARITA if os.path.basename(y) == ad), None)
    if kaynak and os.path.exists(pdf_yolu):
        UK.pdf_damgala(pdf_yolu, ad, UK.ozet(kaynak))


def mark(s=28): return MARK.format(s=s)
def wordmark(size=22, color=T["ink"]):
    return f'<div style="display:flex;align-items:center;gap:8px"><span style="display:inline-flex">{mark(int(size*1.15))}</span><span style="font-family:{SERIF};font-weight:700;font-size:{size}px;letter-spacing:-0.01em;color:{color}">talimatname</span></div>'

# ---------------------------------------------------------------- ikonlar (çizgi, 20px ızgara)
def ico_check(c="#fff", s=14): return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l4 4L19 6"></path></svg>'
def ico_bang(c="#fff", s=14): return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round"><path d="M12 5v9"></path><circle cx="12" cy="18.5" r="1.2" fill="{c}" stroke="none"></circle></svg>'
def ico_cam(c=T["sessiz"], s=16): return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"><path d="M4 8h3l2-2h6l2 2h3v11H4z"></path><circle cx="12" cy="13" r="3.2"></circle></svg>'
def ico_therm(c=T["sessiz"], s=16): return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round"><path d="M10 14V5a2 2 0 0 1 4 0v9"></path><circle cx="12" cy="17" r="3"></circle></svg>'
def ico_bell(c="#fff", s=18): return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"></path><path d="M10 20a2 2 0 0 0 4 0"></path></svg>'

# ---------------------------------------------------------------- ekran parçaları
def box(kind):
    base = f"width:26px;height:26px;border-radius:7px;flex:none;display:flex;align-items:center;justify-content:center;"
    if kind == "ok": return f'<div style="{base}background:{T["marka"]}">{ico_check()}</div>'
    if kind == "crit": return f'<div style="{base}background:{T["kritikA"]};border:2px solid {T["kritik"]}">{ico_bang(T["kritik"])}</div>'
    return f'<div style="{base}border:2px solid {T["ink"]};background:{T["yuzey"]}"></div>'

def chip(text, kind=""):
    bg, fg = T["yuzey2"], T["ink2"]
    if kind == "crit": bg, fg = T["kritikA"], T["kritik"]
    if kind == "ok": bg, fg = T["markaA"], T["marka"]
    if kind == "warn": bg, fg = T["uyariA"], T["uyari"]
    return f'<span style="display:inline-block;padding:2px 9px;border-radius:999px;font-size:11.5px;font-weight:600;background:{bg};color:{fg};white-space:nowrap">{text}</span>'

def row(kind, title, chips="", meta="", thumb=False, last=False):
    border = "" if last else f"border-bottom:1px solid {T['cizgi']};"
    th = f'<div style="width:56px;height:42px;border-radius:8px;flex:none;background:repeating-linear-gradient(135deg,#dfe3e8 0 8px,#eef1f4 8px 16px);border:1px solid {T["cizgi"]}"></div>' if thumb else ""
    metacol = T["kritik"] if kind == "crit" else T["sessiz"]
    return (f'<div style="display:flex;align-items:center;gap:12px;padding:12px 0;min-height:56px;{border}">{box(kind)}'
            f'<div style="flex:1;min-width:0;font-size:15px;line-height:1.3;color:{T["ink"]}">{title}{(" " + chips) if chips else ""}</div>{th}'
            f'<div style="font-size:12px;color:{metacol};white-space:nowrap;text-align:right;font-weight:{600 if kind=="crit" else 400}">{meta}</div></div>')

def phone_header(right_top, right_bottom):
    return (f'<div style="display:flex;align-items:center;gap:10px;padding:16px 16px 10px;border-bottom:1px solid {T["cizgi"]};background:{T["zemin"]}">{wordmark(19)}'
            f'<div style="margin-left:auto;text-align:right;font-size:12px;color:{T["sessiz"]};line-height:1.35"><span style="display:inline-block;padding:4px 10px;border-radius:999px;background:{T["markaA"]};color:{T["marka"]};font-weight:600">{right_top}</span><br>{right_bottom}</div></div>')

def card(inner, style=""):
    return f'<div style="background:{T["yuzey"]};border:1px solid {T["cizgi"]};border-radius:14px;padding:14px 16px;{style}">{inner}</div>'

def section_label(t):
    return f'<div style="font-size:11px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;color:{T["sessiz"]};margin:4px 0 2px">{t}</div>'

def kiosk_list_body(dim=False):
    rows = "".join([
        row("ok", "Espresso makinesi geri yıkama; süt hortumları temizlendi", meta="23:02"),
        row("ok", "Kahve makinesi ve öğütücü temizlendi", chip("fotoğraf"), meta="23:06", thumb=True),
        row("ok", "Süt dolabı sıcaklığı", chip("kritik", "crit"), meta="3,1 °C"),
        row("crit", "Mutfak buzdolabı sıcaklığı", chip("kritik", "crit"), meta="6,0 °C · aralık dışı"),
        row("ok", "Dondurucu sıcaklığı", chip("kritik", "crit"), meta="−19,5 °C"),
        row("", "Açık ürünler etiketlendi ve dolaba kaldırıldı", chip("Evet / Hayır")),
        row("", "Fritöz kapatıldı, yağ süzüldü, kapağı kapatıldı", chip("Evet / Hayır"), last=True),
    ])
    rows2 = "".join([
        row("", "Masalar, sandalyeler ve servis istasyonu silindi"),
        row("", "Zemin süpürüldü ve paspaslandı", chip("fotoğraf"), last=True),
    ])
    op = "opacity:.45;" if dim else ""
    return (f'<div style="flex:1;overflow:hidden;padding:14px 16px 0;display:flex;flex-direction:column;gap:12px;{op}">'
            f'<div><div style="display:flex;align-items:baseline;justify-content:space-between"><div style="font-size:22px;font-weight:700;color:{T["ink"]}">Kapanış listesi</div><div style="font-size:13px;color:{T["sessiz"]}">9 / 15</div></div>'
            f'<div style="font-size:13px;color:{T["sessiz"]};margin-top:2px">22:00 – 01:30 · şube tableti · Emre yapıyor</div>'
            f'<div style="height:8px;border-radius:4px;background:{T["yuzey2"]};margin-top:10px;overflow:hidden"><div style="width:60%;height:100%;background:{T["marka"]}"></div></div></div>'
            f'{card(section_label("A · Bar ve mutfak") + rows)}{card(section_label("B · Salon ve tuvalet") + rows2)}</div>')

def phone(inner, w=390, h=844):
    return (f'<div style="box-sizing:border-box;width:{w}px;height:{h}px;background:{T["zemin"]};border:2px solid {T["ink"]};border-radius:34px;overflow:hidden;display:flex;flex-direction:column;position:relative;font-family:{SANS};color:{T["ink"]};box-shadow:0 18px 40px rgba(28,33,40,.18)">{inner}</div>')

def scr_kiosk():
    bottom = (f'<div style="padding:12px 16px 20px;border-top:1px solid {T["cizgi"]};background:{T["zemin"]}">'
              f'<div style="display:flex;align-items:center;justify-content:center;min-height:52px;border-radius:12px;background:{T["marka"]};color:#fff;font-weight:600;font-size:16px;opacity:.5">Gönder</div>'
              f'<div style="font-size:12px;color:{T["sessiz"]};margin-top:6px;text-align:center">6 zorunlu madde eksik — gönderim pasif · gönderince liste kilitlenir</div></div>')
    return phone(phone_header("Emre T.", "Kadıköy · Cts 13 Eyl") + kiosk_list_body() + bottom)

def scr_temp():
    sheet = (f'<div style="position:absolute;left:0;right:0;bottom:0;background:{T["yuzey"]};border-radius:22px 22px 0 0;padding:18px 18px 24px;box-shadow:0 -12px 30px rgba(0,0,0,.18);display:flex;flex-direction:column;gap:10px">'
             f'<div style="font-size:18px;font-weight:700">Mutfak buzdolabı sıcaklığı</div>'
             f'<div style="font-size:13px;color:{T["sessiz"]}">Kabul aralığı <b style="color:{T["ink"]}">0 – 4 °C</b> · kritik madde</div>'
             f'<div style="display:flex;align-items:center;justify-content:center;gap:14px;margin:6px 0">'
             f'<div style="width:56px;height:56px;border-radius:14px;border:1.5px solid {T["ink"]};display:flex;align-items:center;justify-content:center;font-size:26px">−</div>'
             f'<div style="font-size:44px;font-weight:700;min-width:130px;text-align:center;color:{T["kritik"]};font-variant-numeric:tabular-nums">6,0</div>'
             f'<div style="width:56px;height:56px;border-radius:14px;border:1.5px solid {T["ink"]};display:flex;align-items:center;justify-content:center;font-size:26px">+</div></div>'
             f'<div style="background:{T["kritikA"]};border:1px solid {T["kritik"]};border-radius:12px;padding:12px 14px;display:flex;gap:10px;align-items:flex-start">{box("crit")}<div style="font-size:13.5px;line-height:1.4"><b style="color:{T["kritik"]}">Aralık dışı.</b> Fotoğraf ve not zorunlu. Şube müdürüne 4 saatlik aksiyon açılır; şube ve bölge müdürüne anında bildirilir.</div></div>'
             f'<div style="border:1.5px solid {T["cizgi"]};border-radius:10px;padding:10px 12px;font-size:14px;color:{T["ink2"]}">Kapı contası gevşek, ürünler süt dolabına taşındı</div>'
             f'<div style="display:flex;gap:10px"><div style="flex:1;min-height:48px;border-radius:12px;border:1.5px solid {T["cizgi"]};display:flex;align-items:center;justify-content:center;font-weight:600;color:{T["sessiz"]}">Vazgeç</div>'
             f'<div style="flex:2;min-height:48px;border-radius:12px;background:{T["marka"]};color:#fff;display:flex;align-items:center;justify-content:center;gap:8px;font-weight:600">{ico_cam("#fff",18)} Kaydet ve fotoğraf çek</div></div></div>')
    return phone(phone_header("Emre T.", "Kadıköy · Cts 13 Eyl") + kiosk_list_body(dim=True) + sheet)

def scr_morning():
    push = (f'<div style="position:absolute;left:12px;right:12px;top:12px;background:{T["ink"]};color:#fff;border-radius:16px;padding:12px 14px;display:flex;gap:10px;box-shadow:0 10px 26px rgba(0,0,0,.28);z-index:2">'
            f'<div style="width:36px;height:36px;border-radius:9px;background:{T["marka"]};display:flex;align-items:center;justify-content:center;flex:none">{ico_bell()}</div>'
            f'<div style="font-size:13px;line-height:1.35"><b>Sabah özeti · Anadolu · 07:00</b><br><span style="opacity:.85">2 şube dikkat istiyor: Kadıköy kritik açık, Bakırköy kaçırdı. 3 açık aksiyon.</span></div></div>')
    kpi = lambda n, l, c: f'<div style="flex:1;background:{T["yuzey"]};border:1px solid {T["cizgi"]};border-radius:12px;padding:10px;text-align:center"><div style="font-size:24px;font-weight:700;color:{c}">{n}</div><div style="font-size:11px;color:{T["sessiz"]}">{l}</div></div>'
    body = (f'<div style="flex:1;padding:96px 16px 0;display:flex;flex-direction:column;gap:12px;overflow:hidden">'
            f'<div><div style="font-size:22px;font-weight:700">Dün gece: 12 şubeden 10’u yolunda</div><div style="font-size:13px;color:{T["sessiz"]};margin-top:2px">Anadolu · Pzr 14 Eyl · Murat D.</div></div>'
            f'<div style="display:flex;gap:8px">{kpi("10","zamanında",T["marka"])}{kpi("1","başarısız",T["kritik"])}{kpi("1","kaçırıldı",T["kritik"])}</div>'
            + card(f'<div style="display:flex;gap:12px;align-items:center">{box("crit")}<div style="flex:1"><b>Kadıköy · Kapanış</b><div style="font-size:13px;color:{T["sessiz"]}">23:41 · başarısız — mutfak buzdolabı 6,0 °C</div><div style="font-size:13px;color:{T["kritik"]};font-weight:600;margin-top:3px">Aksiyon #418 · Ayşe K. · açık, vadesi geçti</div></div><span style="color:{T["sessiz"]}">›</span></div>', f"border-color:{T['kritik']}")
            + card(f'<div style="display:flex;gap:12px;align-items:center">{box("crit")}<div style="flex:1"><b>Bakırköy · Kapanış</b><div style="font-size:13px;color:{T["sessiz"]}">Kaçırıldı · 03:30 şube müdürüne bildirildi</div></div><span style="color:{T["sessiz"]}">›</span></div>', f"border-color:{T['kritik']}")
            + card(f'<div style="display:flex;gap:12px;align-items:center">{box("ok")}<div style="flex:1"><b>10 şube yolunda</b><div style="font-size:13px;color:{T["sessiz"]}">Üsküdar, Ataşehir, Maltepe, Kartal (geç, tolerans içinde), Pendik …</div></div><span style="color:{T["sessiz"]}">›</span></div>')
            + f'<div style="font-size:12px;color:{T["sessiz"]}">Yalnızca dikkat isteyenler listelenir; ızgara için "Tümünü göster".</div></div>')
    tabs = "".join(f'<div style="flex:1;text-align:center;font-size:11px;padding:10px 0 14px;color:{T["marka"] if i==2 else T["sessiz"]};font-weight:{700 if i==2 else 400}">{t}</div>' for i, t in enumerate(["Bugün", "Aksiyonlar", "Bölgem", "Menü"]))
    return phone(push + phone_header("Murat D.", "Bölge müdürü") + body + f'<div style="display:flex;border-top:1px solid {T["cizgi"]};background:{T["zemin"]}">{tabs}</div>')

def scr_pano(w=1200, h=760):
    nav = "".join(f'<div style="padding:8px 10px;border-radius:8px;font-size:14px;color:{T["marka"] if i==0 else T["ink"]};background:{T["markaA"] if i==0 else "transparent"};font-weight:{600 if i==0 else 400};display:flex;justify-content:space-between">{n}{"<span style=\'font-size:11px;background:"+T["kritikA"]+";color:"+T["kritik"]+";border-radius:999px;padding:1px 7px;font-weight:600\'>6</span>" if i==0 else ""}</div>'
                  for i, n in enumerate(["Pano", "Aksiyonlar", "Şablonlar", "Planlar", "Şubeler ve personel", "Raporlar"]))
    kpi = lambda n, l, c: f'<div style="background:{T["yuzey"]};border:1px solid {T["cizgi"]};border-radius:12px;padding:12px 14px"><div style="font-family:{SERIF};font-size:26px;font-weight:700;color:{c};line-height:1.1">{n}</div><div style="font-size:12px;color:{T["sessiz"]};margin-top:3px">{l}</div></div>'
    kpis = f'<div style="display:grid;grid-template-columns:repeat(6, minmax(0, 1fr));gap:10px">{kpi("38","zamanında",T["marka"])}{kpi("3","geç (tolerans içinde)",T["uyari"])}{kpi("1","başarısız (kritik)",T["kritik"])}{kpi("2","kaçırıldı",T["kritik"])}{kpi("5","yapılamadı (madde)",T["ink"])}{kpi("6","açık aksiyon",T["uyari"])}</div>'
    def tr(s, l, st, d, last=False):
        c = chip("başarısız", "crit") if st == "fail" else chip("kaçırıldı", "crit") if st == "miss" else chip("geç", "warn")
        return f'<tr><td style="padding:9px 11px;border-bottom:{"0" if last else "1px solid "+T["cizgi"]};font-weight:600">{s}</td><td style="padding:9px 11px;border-bottom:{"0" if last else "1px solid "+T["cizgi"]}">{l}</td><td style="padding:9px 11px;border-bottom:{"0" if last else "1px solid "+T["cizgi"]}">{c}</td><td style="padding:9px 11px;border-bottom:{"0" if last else "1px solid "+T["cizgi"]};color:{T["ink2"]}">{d}</td><td style="padding:9px 11px;border-bottom:{"0" if last else "1px solid "+T["cizgi"]};text-align:right;color:{T["sessiz"]}">›</td></tr>'
    rows = (tr("Kadıköy", "Kapanış", "fail", "23:41 · Emre T. · mutfak buzdolabı 6,0 °C · aksiyon #418 açık") + tr("Bakırköy", "Kapanış", "miss", "gönderim yok · şube müdürüne 03:30 push")
            + tr("Bornova", "Soğuk zincir", "miss", "20:00 ölçüm yok · aksiyon #422") + tr("Kartal", "Kapanış", "late", "01:52 · Burak S. · tolerans içinde")
            + tr("Şişli", "Açılış", "late", "08:41 · 1 yapılamadı: su filtresi (ekipman arızalı)") + tr("Ataşehir", "Saatlik hijyen", "late", "5/6 · 18:00 geç", last=True))
    th = "".join(f'<th style="text-align:left;padding:8px 11px;font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:{T["sessiz"]};background:{T["yuzey2"]};border-bottom:1px solid {T["cizgi"]}">{h}</th>' for h in ["Şube", "Liste", "Durum", "Ayrıntı", ""])
    table = f'<div style="border:1px solid {T["cizgi"]};border-radius:10px;overflow:hidden;background:{T["yuzey"]}"><table style="border-collapse:collapse;width:100%;font-size:13.5px"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>'
    grid_cells = ""
    subeler = ["Kadıköy", "Üsküdar", "Bakırköy", "Beşiktaş", "Bornova", "Karşıyaka", "Ataşehir", "Maltepe", "Kartal", "Pendik", "Ümraniye", "Şişli"]
    state = {"Kadıköy": [T["kritik"], T["marka"], T["marka"], T["marka"]], "Bakırköy": [T["kritik"], T["marka"], T["marka"], T["marka"]], "Bornova": [T["marka"], T["marka"], T["kritik"], T["marka"]],
             "Kartal": [T["uyari"], T["marka"], T["marka"], T["marka"]], "Şişli": [T["marka"], T["uyari"], T["marka"], T["marka"]], "Ataşehir": [T["marka"], T["marka"], T["marka"], T["uyari"]], "Ümraniye": [T["pasif"]] * 4}
    for s in subeler:
        cols = state.get(s, [T["marka"]] * 4)
        grid_cells += f'<div style="font-size:12px;color:{T["ink2"]};display:flex;align-items:center">{s}</div>' + "".join(f'<div style="height:22px;border-radius:4px;background:{c}"></div>' for c in cols)
    grid = (f'<div style="display:grid;grid-template-columns:96px repeat(4, minmax(0, 1fr));gap:4px 6px;align-items:center">'
            f'<div></div>' + "".join(f'<div style="font-size:11px;color:{T["sessiz"]};text-align:center">{l}</div>' for l in ["Kapanış", "Açılış", "Soğuk zincir", "Saatlik"]) + grid_cells + '</div>')
    return (f'<div style="box-sizing:border-box;width:{w}px;height:{h}px;background:{T["zemin"]};font-family:{SANS};color:{T["ink"]};display:grid;grid-template-columns:200px minmax(0,1fr);grid-template-rows:52px minmax(0,1fr);overflow:hidden;border:1px solid {T["cizgi"]};border-radius:12px;box-shadow:0 18px 40px rgba(28,33,40,.14)">'
            f'<div style="grid-column:1 / 3;display:flex;align-items:center;gap:14px;padding:0 18px;background:{T["yuzey"]};border-bottom:1px solid {T["cizgi"]}">{wordmark(19)}<div style="padding-left:16px;border-left:1px solid {T["cizgi"]};font-size:13px;color:{T["ink2"]}">Hesap: <b style="color:{T["ink"]}">Kahve Durağı</b> · 12 şube · 3 bölge</div><div style="margin-left:auto;font-size:13px;color:{T["ink2"]};display:flex;align-items:center;gap:8px"><span style="width:26px;height:26px;border-radius:50%;background:{T["markaA"]};color:{T["marka"]};display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:11px">SY</span>Selin Y.</div></div>'
            f'<div style="background:{T["yuzey"]};border-right:1px solid {T["cizgi"]};padding:14px 10px;display:flex;flex-direction:column;gap:2px">{nav}</div>'
            f'<div style="padding:18px 22px;display:flex;flex-direction:column;gap:12px;overflow:hidden"><div style="display:flex;align-items:flex-end;justify-content:space-between"><div><div style="font-family:{SERIF};font-size:22px;font-weight:700">Pano</div><div style="font-size:13px;color:{T["ink2"]}">Yalnızca dikkat isteyenler; her şey yolundaysa sayfa bunu söyler.</div></div><div style="display:flex;gap:8px"><div style="padding:6px 10px;border:1.5px solid {T["cizgi"]};border-radius:8px;font-size:13px;background:{T["yuzey"]}">Dün gece · Cts 13 Eyl ▾</div><div style="padding:6px 10px;border:1.5px solid {T["cizgi"]};border-radius:8px;font-size:13px;background:{T["yuzey"]}">Tüm bölgeler ▾</div></div></div>'
            f'{kpis}<div style="font-family:{SERIF};font-size:16px;font-weight:700;margin-top:4px">Dikkat isteyenler (6)</div>{table}'
            f'<div style="display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:16px;align-items:start"><div style="background:{T["yuzey"]};border:1px solid {T["cizgi"]};border-radius:12px;padding:12px 14px"><div style="font-size:12px;color:{T["sessiz"]};margin-bottom:8px">Şube × liste — tümünü göster</div>{grid}</div>'
            f'<div style="background:{T["markaA"]};border-radius:12px;padding:14px 16px;font-size:13.5px;line-height:1.45;color:{T["ink2"]}"><b style="font-family:{SERIF};font-size:16px;color:{T["marka"]};display:block;margin-bottom:4px">Her şey yolundaysa</b>Sorunsuz günde bu sayfa tek satırdır: "Dün gece 12 şubenin 12’si yolunda." Sabah özeti e-postası da aynı kaynaktan gider.</div></div></div></div>')

# ---------------------------------------------------------------- broşür sayfaları (A4 794×1123)
def scaled(inner, w, h, s):
    return f'<div style="width:{int(w*s)}px;height:{int(h*s)}px;flex:none;overflow:visible"><div style="transform:scale({s});transform-origin:top left;width:{w}px;height:{h}px">{inner}</div></div>'

def step(no, title, text):
    return (f'<div style="display:flex;flex-direction:column;gap:6px;background:{T["yuzey"]};border:1px solid {T["cizgi"]};border-radius:12px;padding:14px 16px">'
            f'<div style="font-family:{SERIF};font-size:28px;font-weight:700;color:{T["marka"]};line-height:1">{no}</div><div style="font-size:15px;font-weight:600">{title}</div><div style="font-size:13.5px;line-height:1.45;color:{T["ink2"]}">{text}</div></div>')


# ---------------------------------------------------------------- pazarlama bileşenleri (iki broşür de kullanır)
INK_BAND = "#171c21"

def h1(t, size=40, color=None, mw="22ch"):
    return ('<h1 style="font-family:' + SERIF + ';font-size:' + str(size) + 'px;line-height:1.06;font-weight:700;margin:0;'
            'letter-spacing:-0.015em;max-width:' + mw + ';color:' + (color or T["ink"]) + '">' + t + '</h1>')

def h2(t, size=23, color=None):
    return ('<h2 style="font-family:' + SERIF + ';font-size:' + str(size) + 'px;font-weight:700;margin:0;line-height:1.15;'
            'letter-spacing:-0.01em;color:' + (color or T["ink"]) + '">' + t + '</h2>')

def h3(t, color=None):
    return ('<h3 style="font-family:' + SERIF + ';font-size:16px;font-weight:700;margin:0 0 4px;color:' + (color or T["ink"]) + '">' + t + '</h3>')

def mp(t, size=14, color=None, mw="76ch"):
    return ('<p style="margin:0;font-size:' + str(size) + 'px;line-height:1.52;color:' + (color or T["ink2"]) + ';max-width:' + mw + '">' + t + '</p>')

def label(t, color=None):
    return ('<div style="font-size:10.5px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:' + (color or T["sessiz"]) + '">' + t + '</div>')

def pin(n, color=None):
    return ('<span style="display:inline-flex;width:19px;height:19px;border-radius:50%;background:' + (color or T["marka"]) +
            ';color:#fff;font:700 11px ' + SANS + ';align-items:center;justify-content:center;flex:none">' + str(n) + '</span>')

def shot(inner, w_, h_, sc, caption, pins=None):
    marks = ""
    for n, x, y in (pins or []):
        marks += ('<div style="position:absolute;left:' + str(x) + '%;top:' + str(y) + '%;transform:translate(-50%,-50%);'
                  'box-shadow:0 0 0 3px ' + T["zemin"] + ';border-radius:50%">' + pin(n) + '</div>')
    return ('<div style="display:flex;flex-direction:column;gap:7px"><div style="position:relative;width:' + str(int(w_ * sc)) + 'px">'
            + scaled(inner, w_, h_, sc) + marks + '</div>'
            '<div style="font-size:11.5px;color:' + T["ink2"] + ';font-weight:600">' + caption + '</div></div>')

def legend(items, color=None):
    out = ""
    for n, t in items:
        out += ('<div style="display:flex;gap:9px;align-items:flex-start">' + pin(n, color) +
                '<div style="font-size:13px;line-height:1.45;color:' + T["ink2"] + '">' + t + '</div></div>')
    return '<div style="display:flex;flex-direction:column;gap:7px">' + out + '</div>'

def stat(n, l, c=None, dark=False):
    return ('<div style="flex:1;min-width:0;background:' + ("rgba(255,255,255,.06)" if dark else T["yuzey"]) +
            ';border:1px solid ' + ("rgba(255,255,255,.14)" if dark else T["cizgi"]) + ';border-radius:12px;padding:12px 14px">'
            '<div style="font-family:' + SERIF + ';font-size:25px;font-weight:700;line-height:1.05;color:' + (c or ("#fff" if dark else T["ink"])) + '">' + n + '</div>'
            '<div style="font-size:12px;line-height:1.35;margin-top:4px;color:' + ("rgba(255,255,255,.72)" if dark else T["ink2"]) + '">' + l + '</div></div>')

def table(cols, rows, widths=None, size=12.5, head_bg=None):
    wc = "".join('<col style="width:' + x + '">' for x in widths) if widths else ""
    th = "".join('<th style="text-align:left;padding:8px 10px;font-size:10px;letter-spacing:.07em;text-transform:uppercase;color:' + T["sessiz"] +
                 ';background:' + (head_bg or T["yuzey2"]) + ';border-bottom:1px solid ' + T["cizgi"] + ';font-weight:700">' + c + '</th>' for c in cols)
    tr = ""
    for i, r in enumerate(rows):
        bb = "0" if i == len(rows) - 1 else "1px solid " + T["cizgi"]
        tr += "<tr>" + "".join('<td style="padding:8px 10px;border-bottom:' + bb + ';vertical-align:top;line-height:1.42">' + c + '</td>' for c in r) + "</tr>"
    return ('<div style="border:1px solid ' + T["cizgi"] + ';border-radius:11px;overflow:hidden;background:' + T["yuzey"] + '">'
            '<table style="border-collapse:collapse;width:100%;font-size:' + str(size) + 'px">' + wc + '<thead><tr>' + th + '</tr></thead><tbody>' + tr + '</tbody></table></div>')

def quote(t, who):
    return ('<div style="border-left:3px solid ' + T["marka"] + ';padding:6px 0 6px 14px">'
            '<div style="font-family:' + SERIF + ';font-size:17px;line-height:1.35;color:' + T["ink"] + '">“' + t + '”</div>'
            '<div style="font-size:11.5px;color:' + T["sessiz"] + ';margin-top:5px">' + who + '</div></div>')

def check(t, d=""):
    return ('<div style="display:flex;gap:9px;align-items:flex-start">' + box("ok") +
            '<div style="font-size:13.5px;line-height:1.45"><b>' + t + '</b>' + ((" " + d) if d else "") + '</div></div>')

def qa(q, a):
    return ('<div style="background:' + T["yuzey"] + ';border:1px solid ' + T["cizgi"] + ';border-radius:11px;padding:11px 13px">'
            '<div style="font-size:13.5px;font-weight:700;margin-bottom:3px">' + q + '</div>'
            '<div style="font-size:12.5px;line-height:1.45;color:' + T["ink2"] + '">' + a + '</div></div>')

def sheet(inner, gap=16):
    return ('<div style="box-sizing:border-box;width:794px;height:1123px;background:' + T["zemin"] + ';font-family:' + SANS + ';color:' + T["ink"] +
            ';padding:38px 44px 26px;display:flex;flex-direction:column;gap:' + str(gap) + 'px;overflow:hidden">' + inner + '</div>')

def brosur_foot(no, note=""):
    return ('<div style="margin-top:auto;display:flex;align-items:center;justify-content:space-between;border-top:1px solid ' + T["cizgi"] +
            ';padding-top:9px;font-size:10.5px;color:' + T["sessiz"] + '"><span>' + (note or "Ekranlar ürün tasarımındandır; veriler örnektir.") +
            '</span><span>Talimatname · ' + str(no) + ' / 2</span></div>')

def page1():
    hero = ('<div style="background:' + INK_BAND + ';border-radius:16px;padding:26px 28px;display:flex;gap:22px;align-items:center;overflow:hidden">'
            '<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:12px">'
            + label("Çok şubeli yeme-içme zincirleri için", "rgba(255,255,255,.55)")
            + h1("Şube talimatları,<br>kanıtıyla.", 40, "#fff", "16ch")
            + mp("Açılış, kapanış, hijyen ve soğuk zincir listeleri merkez tarafından bir kez kurulur; her gece şubede kendiliğinden açılır; "
                 "personel fotoğraf ve ölçümle kapatır. Merkez sabah yalnızca aksayanı görür, denetim kaydını tek tuşla alır.", 14, "rgba(255,255,255,.78)", "44ch")
            + '<div style="display:flex;gap:7px;flex-wrap:wrap">'
            + "".join('<span style="font-size:11px;font-weight:600;color:#fff;background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.18);'
                      'border-radius:999px;padding:4px 10px">' + x + '</span>' for x in ["5\u2013100 \u015fube", "T\u00fcrk\u00e7e", "Veriler T\u00fcrkiye\u2019de", "Ki\u015fi puan\u0131 yok"])
            + '</div></div>'
            '<div style="flex:none;position:relative;width:240px;height:300px">'
            '<div style="position:absolute;left:-4px;top:-12px">' + scaled(scr_kiosk(), 390, 844, 0.40) + '</div>'
            '<div style="position:absolute;left:92px;top:122px;border-radius:10px;box-shadow:0 18px 38px rgba(0,0,0,.4)">' + scaled(scr_morning(), 390, 844, 0.26) + '</div>'
            '</div></div>')
    stats = ('<div style="display:flex;gap:10px">'
             + stat("6\u20138 dk", "kapanış listesinin personele maliyeti")
             + stat("3 dk", "denetim kaydının PDF olarak çıkması")
             + stat("1 saat", "ilk şubenin kurulumu; aynı gece başlar")
             + stat("0", "kişi puanı, biyometri, sohbet", T["marka"]) + '</div>')
    nicin = ('<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px 20px">'
             + check("WhatsApp gruplarının yerine.", "Tekrarlı listeler kendiliğinden açılır; “yapıldı abi” yerine damgalı fotoğraf ve ölçüm — aynı fotoğraf ikinci kez gönderilemez.")
             + check("Yapılmayan iş sabah masanızda.", "Kaçırılan liste ve kritik madde yöneticiye düşer; aksiyon açılır, kapanınca not kalır.")
             + check("Denetim kaydı dakikalar içinde.", "Sıcaklık günlüğü, çalıştırma raporu ve belge takvimi doğrulama kodlu PDF; kayıt sonradan değiştirilemez.")
             + check("Mutfakta çalışır.", "Ortak tablet, PIN ile geçiş; Wi-Fi gidince kayıt cihazda bekler, bağlanınca senklenir.") + '</div>')
    steps = ('<div style="display:grid;grid-template-columns:repeat(3, minmax(0, 1fr));gap:11px">'
             + step("1", "Merkez kurar — 1 saat", "Şubeler Excel’den, kapanış listesi 8 hazır şablondan; pencere şube saatinden hesaplanır. Bu gece başlar.")
             + step("2", "Personel tamamlar — 6 dakika", "Kioskta adına dokunur, PIN girer; maddeleri işaretler, fotoğrafı uygulama içinden çeker, sıcaklığı girer.")
             + step("3", "Merkez görür — 07:00", "Sabah özeti: kaçıran, başarısız, yapılamayan. Panoda yalnızca dikkat isteyenler; gerisi “her şey yolunda”.") + '</div>')
    return sheet(wordmark(25) + hero + stats + label("Ne değişir") + nicin + steps + brosur_foot(1), gap=16)

def pdf_thumb():
    line = lambda w, c=T["cizgi"]: f'<div style="height:5px;width:{w}%;background:{c};border-radius:2px"></div>'
    return (f'<div style="box-sizing:border-box;width:150px;height:200px;background:{T["yuzey"]};border:1px solid {T["cizgi"]};box-shadow:0 8px 20px rgba(28,33,40,.14);padding:12px;display:flex;flex-direction:column;gap:6px;flex:none">'
            f'<div style="display:flex;justify-content:space-between;align-items:center"><div style="font-family:{SERIF};font-size:9px;font-weight:700">Çalıştırma raporu</div><div style="width:18px;height:18px;background:{T["ink"]};border-radius:2px"></div></div>'
            f'<div style="font-size:7px;color:{T["kritik"]};font-weight:700">BAŞARISIZ · kritik madde</div>{line(90)}{line(70)}{line(85)}{line(60,T["kritikA"])}{line(80)}{line(75)}'
            f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-top:2px">' + "".join(f'<div style="height:22px;background:repeating-linear-gradient(135deg,#e6e3da 0 4px,#cbc8be 4px 8px);border-radius:2px"></div>' for _ in range(3)) + '</div>'
            f'{line(88)}{line(64)}<div style="margin-top:auto;font-size:6.5px;color:{T["sessiz"]};font-family:ui-monospace,Menlo,monospace">Doğrulama TN-K7F3A-9C2D</div></div>')

def page2():
    ekranlar = ('<div style="display:flex;gap:14px;align-items:flex-start">'
                + shot(scr_pano(1200, 760), 1200, 760, 0.26, "İstisna panosu · merkez", [(1, 22, 34), (2, 50, 60), (3, 84, 85)])
                + '<div style="flex:1;min-width:0">'
                + legend([(1, "Altı sayıda gece özeti: zamanında, geç, başarısız, kaçırıldı, yapılamadı, açık aksiyon."),
                          (2, "Yalnızca sorunlu satırlar listelenir — “her şey yolunda” da bir cevaptır."),
                          (3, "Şube × liste ızgarası: tüm gün tek bakışta, hücreden detaya.")])
                + '</div></div>')
    karsilastirma = table(["", "WhatsApp grupları", "Kâğıt / Excel", "<b>Talimatname</b>"],
                          [["Liste kendiliğinden açılır", "<span style='color:" + T["sessiz"] + "'>yok</span>", "<span style='color:" + T["sessiz"] + "'>yok</span>", "<span style='color:" + T["marka"] + ";font-weight:700'>var</span>"],
                           ["Yapılmayan iş yöneticiye düşer", "<span style='color:" + T["sessiz"] + "'>yok</span>", "<span style='color:" + T["sessiz"] + "'>yok</span>", "<span style='color:" + T["marka"] + ";font-weight:700'>var</span>"],
                           ["Kanıt aranabilir, değiştirilemez", "<span style='color:" + T["sessiz"] + "'>yok</span>", "<span style='color:" + T["uyari"] + "'>kısmen</span>", "<span style='color:" + T["marka"] + ";font-weight:700'>var</span>"],
                           ["Denetim kaydı dakikalar içinde", "<span style='color:" + T["sessiz"] + "'>yok</span>", "<span style='color:" + T["uyari"] + "'>kısmen</span>", "<span style='color:" + T["marka"] + ";font-weight:700'>var</span>"]],
                          widths=["40%", "20%", "18%", "22%"])
    sonraki = ('<div style="background:' + T["yuzey2"] + ';border-radius:11px;padding:8px 13px;font-size:11.5px;line-height:1.5;color:' + T["ink2"] + '">'
               '<span style="font-size:10px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:' + T["sessiz"] + '">Sıradaki sürüm · henüz geliştirilmedi</span> &nbsp;'
               '<b style="color:' + T["ink"] + '">Denetçiye tek dosya ve süreli bağlantı:</b> dönemin günlükleri, listeleri, belgeleri ve kanıt örnekleri tek PDF; '
               'hesap açmadan 48 saat açık, salt-okunur bağlantı (adlar maskeli, açılışlar kayıtlı). Ekranı <b>föyün 8. sayfasında</b>; pilot sözleşmesi bugünkü sürümü bağlar.</div>')
    itiraz = ('<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">'
              + qa("“Personel kullanmaz.”", "Üç ekran, iki dokunuş; kioskta PIN’le giriş. Mesaj “seni izliyoruz” değil, “yaptığını kanıtlıyorsun”.")
              + qa("“KVKK sorun çıkarır mı?”", "Kişi puanı ve biyometri yok, konum tek nokta; aydınlatma metni ve veri işleme sözleşmesi hazır.") + '</div>')
    kutu = lambda n, l: ('<div style="background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:11px;padding:9px 12px;flex:1;min-width:0">'
                         '<div style="font-family:' + SERIF + ';font-size:20px;font-weight:700;color:#fff">' + n + '</div>'
                         '<div style="font-size:11px;line-height:1.35;color:rgba(255,255,255,.72);margin-top:3px">' + l + '</div></div>')
    pilot = ('<div style="background:' + INK_BAND + ';border-radius:16px;padding:16px 24px;display:flex;flex-direction:column;gap:9px">'
             + label("Sonraki adım", "rgba(255,255,255,.55)") + h1("8 haftalık ücretli pilot", 26, "#fff", "22ch")
             + mp("Seçtiğiniz 5–15 şubede kapanış ve soğuk zincir listeleriyle başlarız. Kurulum bir gün: kiosk, PIN’ler, şablon uyarlaması, şube müdürüne 30 dk ve personele 10 dk eğitim.", 13, "rgba(255,255,255,.78)", "92ch")
             + '<div style="display:flex;gap:9px">' + kutu("≥ %80", "liste pencere içinde tamamlanır") + kutu("≥ %95", "fotoğraf zorunlu maddede kanıt")
             + kutu("≥ %80", "kritik aksiyon vadesinde kapanır") + '</div>'
             + mp("4. hafta sonunda birlikte ölçeriz: ölçütler tutarsa yıllık sözleşmeyi konuşuruz, tutmazsa kalan aylar iade edilir. Ücret görüşmede belirlenir.", 11.5, "rgba(255,255,255,.62)", "92ch") + '</div>')
    contact = ('<div style="display:flex;align-items:center;justify-content:space-between;gap:16px;border-top:1px solid ' + T["cizgi"] + ';padding-top:12px">'
               '<div style="display:flex;flex-direction:column;gap:3px">' + wordmark(22) +
               '<div style="font-size:12px;color:' + T["sessiz"] + '">Şube operasyonları, kanıtıyla.</div>'
               '<div style="font-size:11.5px;color:' + T["ink2"] + ';margin-top:2px">Her özelliğin açıklaması ve ekranı: <b>özellik föyü</b> (A4, ' + str(S["foy_sayfa"]) + ' sayfa)</div></div>'
               '<div style="font-size:13.5px;color:' + T["ink"] + ';text-align:right;line-height:1.55">'
               '<b>[Ad Soyad]</b> · [telefon]<br><span style="color:' + T["ink2"] + '">[e-posta] · [alan adı]</span></div></div>')
    return sheet(h2("Merkez ne görür", 26)
                 + mp("07:00’de sabah özeti; panoda yalnızca dikkat isteyen şube × liste hücreleri; her çalıştırma için doğrulama kodlu PDF.")
                 + ekranlar + label("Alternatifle yan yana") + karsilastirma + sonraki + itiraz + pilot + contact
                 + brosur_foot(2, "Talimatname çalışma adıdır."), gap=8)

# ---------------------------------------------------------------- dosyalar
HEAD = '<!doctype html>\n<html>\n<head>\n  <meta charset="utf-8">\n  <script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bitter:wght@700&display=swap">\n  <style>\n    body { margin: 0; background: #e9e6de; }\n    a { color: #1f6f5b; } a:hover { color: #174f41; }\n  </style>\n</helmet>\n'
TAIL = '\n</x-dc>\n</body>\n</html>\n'

def dc(inner): return HEAD + inner + TAIL

def main():
    files = {"Main.dc.html": page1(), "Sayfa2.dc.html": page2(), "KioskListe.dc.html": scr_kiosk(), "Sicaklik.dc.html": scr_temp(), "SabahOzeti.dc.html": scr_morning(), "Pano.dc.html": scr_pano()}
    for name, inner in files.items():
        open(os.path.join(HERE, name), "w", encoding="utf-8").write(dc(inner))
    canvas = {"artboards": [
        {"file": "Main.dc.html", "title": "Broşür · sayfa 1", "x": 0, "y": 0, "w": 794, "h": 1123, "print": "fixed"},
        {"file": "Sayfa2.dc.html", "title": "Broşür · sayfa 2", "x": 900, "y": 0, "w": 794, "h": 1123, "print": "fixed"},
        {"file": "KioskListe.dc.html", "title": "Ekran · kapanış listesi (kiosk)", "x": 0, "y": 1260, "w": 390, "h": 844},
        {"file": "Sicaklik.dc.html", "title": "Ekran · sıcaklık aralık dışı", "x": 480, "y": 1260, "w": 390, "h": 844},
        {"file": "SabahOzeti.dc.html", "title": "Ekran · sabah özeti (bölge müdürü)", "x": 960, "y": 1260, "w": 390, "h": 844},
        {"file": "Pano.dc.html", "title": "Ekran · web pano (istisna görünümü)", "x": 1440, "y": 1260, "w": 1200, "h": 760}],
        "launch": {"view": "canvas"}}
    json.dump(canvas, open(os.path.join(HERE, "canvas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    # yazdırma sürümü
    css = ("body{margin:0;background:#e9e6de;font-family:" + SANS + "} .sheet{margin:18px auto;box-shadow:0 10px 30px rgba(28,33,40,.14)} "
           "@media print{body{background:#fff}.sheet{margin:0;box-shadow:none}.sheet+.sheet{break-before:page}@page{size:A4;margin:0}}")
    html = (f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Talimatname tanıtım broşürü</title>'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bitter:wght@700&display=swap"><style>{css}</style></head><body>'
            f'<div class="sheet" style="width:794px">{page1()}</div><div class="sheet" style="width:794px">{page2()}</div></body></html>')
    out = os.path.join(HERE, "talimatname-brosur.html"); open(out, "w", encoding="utf-8").write(_damga(html))
    print("ok:", ", ".join(files), "canvas.json, talimatname-brosur.html")
    if "--pdf" in sys.argv:
        edge = next((p for p in [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"] if os.path.exists(p)), None)
        if not edge: print("Edge yok"); return
        pdf = out.replace(".html", ".pdf")
        if os.path.exists(pdf): os.remove(pdf)
        prof = tempfile.mkdtemp(prefix="talimatname-pdf-")
        subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={prof}", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", "--virtual-time-budget=6000", "file:///" + out.replace(os.sep, "/")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        for _ in range(120):
            if os.path.exists(pdf) and os.path.getsize(pdf) > 10_000: break
            time.sleep(0.5)
        _pdf_damga(pdf)
        print(pdf, "ok" if os.path.exists(pdf) else "HATA")

if __name__ == "__main__":
    main()
