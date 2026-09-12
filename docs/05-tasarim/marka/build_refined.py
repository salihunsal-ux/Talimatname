# -*- coding: utf-8 -*-
"""Seçilen iki yönün rafine logo sistemleri: Main.dc.html (yap lütfen · Rica) ve TamamlistB.dc.html (tamamlist · Mesaj).
Çalıştır: python build_refined.py  (canvas.json'u sayfalı yapıya yeniden yazar)"""
import json, html

F = json.load(open("fonts/fonts.json", encoding="utf-8"))
W, H = 1400, 1000

# ------------------------------------------------------------------ işaretler
def mark_rica(fill, check, size="100%"):
    """Kuyruğu sol-altta, yumuşak hatlı istek balonu."""
    return (f'<svg viewBox="0 0 64 64" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="M21 6 H43 A17 17 0 0 1 60 23 V33 A17 17 0 0 1 43 50 H34 L22 61 L21 50 A17 17 0 0 1 4 33 V23 A17 17 0 0 1 21 6 Z" fill="{fill}"></path>'
            f'<path d="M20 28 L28 36 L44 20" fill="none" stroke="{check}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"></path>'
            f'</svg>')

def mark_rica_tile(fill, check, size="100%"):
    """16 px için sadeleştirilmiş: kuyruksuz."""
    return (f'<svg viewBox="0 0 64 64" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">'
            f'<rect x="4" y="8" width="56" height="48" rx="18" fill="{fill}"></rect>'
            f'<path d="M20 32 L28 40 L44 24" fill="none" stroke="{check}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"></path>'
            f'</svg>')

def mark_mesaj(fill, check, size="100%"):
    """Kuyruğu sağ-altta, kart gibi köşeli cevap balonu."""
    return (f'<svg viewBox="0 0 64 64" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="M16 4 H48 A12 12 0 0 1 60 16 V38 A12 12 0 0 1 48 50 H46 L58 61 L34 50 H16 A12 12 0 0 1 4 38 V16 A12 12 0 0 1 16 4 Z" fill="{fill}"></path>'
            f'<path d="M19 28 L28 37 L46 19" fill="none" stroke="{check}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"></path>'
            f'</svg>')

def mark_mesaj_tile(fill, check, size="100%"):
    return (f'<svg viewBox="0 0 64 64" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">'
            f'<rect x="4" y="6" width="56" height="52" rx="13" fill="{fill}"></rect>'
            f'<path d="M19 33 L28 42 L46 24" fill="none" stroke="{check}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"></path>'
            f'</svg>')

def mark_tembih(fill, check, size="100%"):
    """Tekrar halkası (dairesel ok) içinde tik: tembih = tekrar tekrar hatırlatmak."""
    return (f'<svg viewBox="0 0 64 64" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="M50.5 22.5 A21 21 0 1 0 53 32" fill="none" stroke="{fill}" stroke-width="7" stroke-linecap="round"></path>'
            f'<path d="M44 12 L52 24 L38 26 Z" fill="{fill}"></path>'
            f'<path d="M22 32 L29 39 L43 24" fill="none" stroke="{check}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"></path>'
            f'</svg>')

def mark_tembih_tile(fill, check, size="100%"):
    return (f'<svg viewBox="0 0 64 64" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">'
            f'<circle cx="32" cy="32" r="27" fill="{fill}"></circle>'
            f'<path d="M20 33 L28 41 L45 23" fill="none" stroke="{check}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"></path>'
            f'</svg>')

def mark_name(page, lines, seal, check, ring, size="100%"):
    """Talimatname: belge sayfası + sağ altta mühür. page: sayfa dolgusu, lines: satırlar, seal: mühür, check: tik, ring: mühür halkası (zemin rengi)."""
    return (f'<svg viewBox="0 0 64 64" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="M14 4 H38 L48 14 V56 A4 4 0 0 1 44 60 H14 A4 4 0 0 1 10 56 V8 A4 4 0 0 1 14 4 Z" fill="{page}"></path>'
            f'<path d="M38 4 V14 H48 Z" fill="{lines}"></path>'
            f'<rect x="17" y="22" width="20" height="4" rx="2" fill="{lines}"></rect>'
            f'<rect x="17" y="31" width="14" height="4" rx="2" fill="{lines}"></rect>'
            f'<circle cx="46" cy="46" r="14" fill="{seal}" stroke="{ring}" stroke-width="3"></circle>'
            f'<path d="M39 46.5 L44 51.5 L53.5 41" fill="none" stroke="{check}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"></path>'
            f'</svg>')

def mark_name_tile(seal, check, size="100%"):
    """16 px: yalnızca mühür."""
    return (f'<svg viewBox="0 0 64 64" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">'
            f'<circle cx="32" cy="32" r="27" fill="{seal}"></circle>'
            f'<path d="M20 33 L28 41 L45 23" fill="none" stroke="{check}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"></path>'
            f'</svg>')

# ------------------------------------------------------------------ sistemler
SYS = {
 "name": dict(
    file="Main.dc.html", name="talimatname", dir_title="Mühür", fonts=["bitter"],
    font_css="font-family:Bitter,Georgia,'Times New Roman',serif;font-weight:700;letter-spacing:-0.012em;",
    font_spec="Bitter · Bold 700 · harf aralığı −1,2% · yalnızca küçük harf (slab serif: belge ve kayıt tınısı)",
    mark=None, tile=None,
    accent="#1f6f5b", accent_name="Defter yeşili", ink="#1c2128", ink_name="Mürekkep", paper="#f7f5ef", paper_name="Parşömen",
    tint="#dcebe5", tint_name="Defter açık", second="#b8452f", second_name="Mühür kızılı (kritik / başarısız)",
    dark="#15191c", dark_ink="#f1eee6", dark_accent="#3fa98c",
    notif_title="talimatname", notif_body="Kapanış talimatnamesi açıldı · 01:30'a kadar", notif_time="22:00",
    tagline="Talimat yazıldı, iş yapıldı, mühür basıldı.",
    stage="ÇALIŞMA ADI · RAFİNE SÜRÜM", small_note="16 px'te sayfa okunmuyor; favicon yalnızca mühür.",
    wordmark=lambda ink, size, css: f'<span style="{css}font-size:{size}px;line-height:1;color:{ink};">talimatname</span>',
    note="talimatname · çalışma adı (12 Eylül 2026) — 'nâme' = belge; işaret sayfa + mühür: talimat yazılır (sayfa), iş yapılır, kanıt mühürlenir. Slab serif eski kelimeyi modern tutar. Artı: 4/4 alan adı boş, uydurma-derecesinde ayırt edici (tescil kolay), kanıt/kayıt hikâyesini isim taşıyor. Eksi: 11 harf, bürokrasi tınısı; personel tarafında 'resmî' algılanabilir — isim testinde ölçülecek; yurt dışına taşınmaz."),
 "rica": dict(
    file="YapLutfenA.dc.html", name="yap lütfen", dir_title="Rica", fonts=["baloo"],
    font_css="font-family:'Baloo 2','Segoe UI',Arial,sans-serif;font-weight:800;letter-spacing:-0.02em;",
    font_spec="Baloo 2 · ExtraBold 800 · harf aralığı −2% · yalnızca küçük harf",
    mark=mark_rica, tile=mark_rica_tile,
    accent="#e96a48", accent_name="Mercan", ink="#1e2230", ink_name="Mürekkep", paper="#fbf6f1", paper_name="Kâğıt",
    tint="#fbe3da", tint_name="Mercan açık", second="#2fa38a", second_name="Nane (yapıldı durumu)",
    dark="#191c24", dark_ink="#f6f1ea", dark_accent="#f08a6c",
    notif_title="yap lütfen", notif_body="Kapanış listesi açıldı · 01:30'a kadar", notif_time="22:00",
    tagline="Yap lütfen, dedin. Yapıldı, kanıtıyla.",
    wordmark=lambda ink, size, css: f'<span style="{css}font-size:{size}px;line-height:1;color:{ink};">yap lütfen</span>',
    note="yap lütfen · rafine — Balonun kuyruğu gövdeye kaynaştı (tek çizgi), tik gövdenin optik merkezinde. 16 px'te kuyruk kayboluyor: favicon için kuyruksuz sürüm. Koruma alanı = ikon yüksekliğinin yarısı. Nane yeşili yalnızca arayüzde 'yapıldı' durumu için; logoda kullanılmaz."),
 "mesaj": dict(
    file="TamamlistB.dc.html", name="tamamlist", dir_title="Mesaj", fonts=["jakarta"],
    font_css="font-family:'Plus Jakarta Sans','Segoe UI',Arial,sans-serif;font-weight:800;letter-spacing:-0.035em;",
    font_spec="Plus Jakarta Sans · ExtraBold 800 · harf aralığı −3,5% · yalnızca küçük harf",
    mark=mark_mesaj, tile=mark_mesaj_tile,
    accent="#4b4fd6", accent_name="Çivit", ink="#1b1b2e", ink_name="Gece", paper="#f4f4fb", paper_name="Kâğıt",
    tint="#e1e2f8", tint_name="Çivit açık", second="#1c9c76", second_name="Tamam yeşili (yapıldı durumu)",
    dark="#14142a", dark_ink="#ecebf7", dark_accent="#8b8ff0",
    notif_title="tamamlist", notif_body="Kapanış listesi tamamlandı · 12/12 · kanıt yüklendi", notif_time="23:41",
    tagline="Yapılacak, yapıldı, tamam — kanıtıyla.",
    wordmark=lambda ink, size, css: f'<span style="{css}font-size:{size}px;line-height:1;color:{ink};">tamamlist</span>',
    note="tamamlist · rafine — Rica'dan ayrışması için balon köşeli (kart) ve kuyruk sağ-altta: gelen istek değil, giden cevap. Tik aynı kalınlıkta. 'list' iki tonlu yazılmadı; tek renk daha sakin. Çivit, B2B yazılımda tanıdık; Rica'nın mercanıyla yan yana konunca sıcak/soğuk farkı isim kararını kolaylaştırır."),
 "tembih": dict(
    file="Tembihle.dc.html", name="tembihle", dir_title="Tekrar", fonts=["sora"],
    font_css="font-family:Sora,'Segoe UI',Arial,sans-serif;font-weight:700;letter-spacing:-0.02em;",
    font_spec="Sora · Bold 700 · harf aralığı −2% · yalnızca küçük harf",
    mark=mark_tembih, tile=mark_tembih_tile,
    accent="#d9971c", accent_name="Safran", ink="#242018", ink_name="Kahve", paper="#faf7f0", paper_name="Kâğıt",
    tint="#f7e8c4", tint_name="Safran açık", second="#2e8b6a", second_name="Yeşil (yapıldı durumu)",
    dark="#1c1913", dark_ink="#f5efe2", dark_accent="#e8ad3a",
    notif_title="tembihle", notif_body="Kapanış listesi açıldı · 01:30'a kadar", notif_time="22:00",
    tagline="Bir kez tembihle, her vardiya yapılsın — kanıtıyla.",
    stage="İSİM TESTİ KARTI", small_note="16 px'te ok ucu kayboluyor; favicon halkasız daire sürümünü kullanır.",
    wordmark=lambda ink, size, css: f'<span style="{css}font-size:{size}px;line-height:1;color:{ink};">tembihle</span>',
    note="tembihle · isim testi kartı — 'Tembih etmek' = tekrar tekrar, önceden hatırlatmak; işaret tekrar halkası içinde tik (tekrarlı liste + yapıldı). Safran: uyarı/hatırlatma rengi, mercan ve çivitten ayrışır. Artı: 4/4 alan adı boş, anlam ürünün tam kendisi, sıcak. Eksi: hafif ebeveyn/anne tınısı — personel 'patron' değil 'anne' mi duyar, sahada test edilecek; yurt dışına taşınmaz."),
}

def swatch(hexv, name, ink, mut):
    return (f'<div style="display:flex;flex-direction:column;gap:6px;align-items:flex-start;">'
            f'<div style="width:100%;height:44px;border-radius:8px;background:{hexv};border:1px solid rgba(0,0,0,0.08);"></div>'
            f'<div style="font-size:11px;font-weight:600;color:{ink};">{html.escape(name)}</div>'
            f'<div style="font-size:11px;color:{mut};font-family:Consolas,monospace;">{hexv}</div></div>')

def panel(bg, extra=""):
    return f'style="background:{bg};border:1px solid rgba(0,0,0,0.06);border-radius:12px;{extra}"'

def label(text, mut):
    return f'<div style="font-size:11px;font-weight:700;letter-spacing:0.1em;color:{mut};">{html.escape(text)}</div>'

def system(s):
    fonts_css = "".join(F[k]["css"] for k in s["fonts"])
    a, ink, paper, mut = s["accent"], s["ink"], s["paper"], "#7d8590"
    dk, dki, dka = s["dark"], s["dark_ink"], s["dark_accent"]
    css = s["font_css"]; wm = s["wordmark"]; mark = s["mark"]; tile = s["tile"]
    # ana ikon renkleri
    if s["file"] == "Main.dc.html":  # talimatname
        m_light = mark_name(ink, paper, a, "#ffffff", paper); m_dark = mark_name(dki, dk, dka, dk, dk)
        m_mono = mark_name(ink, "#ffffff", ink, "#ffffff", "#ffffff"); m_mono_dark = mark_name(dki, dk, dki, dk, dk)
        app_color = mark_name("#ffffff", a, a, "#ffffff", "#ffffff"); app_dark = mark_name(dki, dk, dka, dk, dk)
        m_accent = mark_name(a, "#ffffff", a, "#ffffff", "#ffffff"); m_tile = mark_name_tile(a, "#ffffff")
    elif s["file"] == "Tembihle.dc.html":
        m_light = mark(a, ink); m_dark = mark(dka, dki); m_mono = mark(ink, ink); m_mono_dark = mark(dki, dki)
        app_color = mark("#ffffff", "#ffffff"); app_dark = mark(dka, dki)
    else:
        m_light = mark(a, "#ffffff"); m_dark = mark(dka, dk); m_mono = mark(ink, "#ffffff"); m_mono_dark = mark(dki, dk)
        app_color = mark("#ffffff", a); app_dark = mark(dka, dk)
    if s["file"] != "Main.dc.html":
        m_accent = mark(a, ink) if s["file"] == "Tembihle.dc.html" else mark(a, "#ffffff")
        m_tile = tile(a, ink) if s["file"] == "Tembihle.dc.html" else tile(a, "#ffffff")
    return f'''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <style>
    {fonts_css}
    body {{ margin: 0; font-family: 'Segoe UI', Arial, sans-serif; }}
    a {{ color: {a}; }} a:hover {{ color: {ink}; }}
  </style>
</helmet>
<div style="width: {W}px; height: {H}px; box-sizing: border-box; background: {paper}; color: {ink}; padding: 30px 34px; display: flex; flex-direction: column; gap: 18px; font-family: 'Segoe UI', Arial, sans-serif;">
  <div style="display: flex; justify-content: space-between; align-items: flex-end;">
    <div style="display: flex; flex-direction: column; gap: 4px;">
      <div style="font-size: 11px; font-weight: 700; letter-spacing: 0.14em; color: {mut};">{html.escape(s["name"].upper())} · {html.escape(s["dir_title"].upper())} · {html.escape(s.get("stage", "RAFİNE SÜRÜM"))}</div>
      <div style="font-size: 24px; font-weight: 700; color: {ink};">Logo sistemi</div>
    </div>
    <div style="font-size: 12px; color: {mut};">{html.escape(s["tagline"])}</div>
  </div>

  <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px;">
    <div {panel("#ffffff", "grid-column: span 2; padding: 34px 40px; display: flex; flex-direction: column; gap: 22px;")}>
      {label("ANA LOCKUP · YATAY", mut)}
      <div style="display: flex; align-items: center; gap: 30px; padding: 26px 30px; border: 1px dashed rgba(0,0,0,0.14); border-radius: 10px; align-self: flex-start;">
        <div style="width: 104px; height: 104px; flex: none;">{m_light}</div>
        {wm(ink, 72, css)}
      </div>
      <div style="font-size: 12px; color: {mut};">Kesikli çerçeve = koruma alanı (ikon yüksekliğinin yarısı). İkon–yazı boşluğu ikon genişliğinin 0,28'i; tik, x-yüksekliğinin ortasına hizalı.</div>
    </div>
    <div {panel("#ffffff", "padding: 30px 28px; display: flex; flex-direction: column; gap: 18px; align-items: center;")}>
      {label("DİKEY LOCKUP", mut)}
      <div style="display: flex; flex-direction: column; align-items: center; gap: 18px; padding: 16px 10px;">
        <div style="width: 120px; height: 120px;">{m_light}</div>
        {wm(ink, 44, css)}
      </div>
      <div style="font-size: 12px; color: {mut}; text-align: center;">Kare alanlar, sosyal profil, kartvizit.</div>
    </div>
  </div>

  <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px;">
    <div style="grid-column: span 2; background: {dk}; border-radius: 12px; padding: 30px 40px; display: flex; align-items: center; justify-content: space-between; gap: 30px;">
      <div style="display: flex; align-items: center; gap: 24px;">
        <div style="width: 84px; height: 84px; flex: none;">{m_dark}</div>
        {wm(dki, 58, css)}
      </div>
      <div style="display: flex; align-items: center; gap: 18px;">
        <div style="width: 56px; height: 56px; flex: none;">{m_mono_dark}</div>
        {wm(dki, 30, css)}
      </div>
    </div>
    <div {panel("#ffffff", "padding: 24px 28px; display: flex; flex-direction: column; gap: 14px;")}>
      {label("TEK RENK", mut)}
      <div style="display: flex; align-items: center; gap: 14px;">
        <div style="width: 44px; height: 44px; flex: none;">{m_mono}</div>
        {wm(ink, 26, css)}
      </div>
      <div style="display: flex; align-items: center; gap: 14px;">
        <div style="width: 44px; height: 44px; flex: none;">{m_accent}</div>
        {wm(a, 26, css)}
      </div>
      <div style="font-size: 12px; color: {mut};">Damga, faks, tek renkli baskı; ikinci satır tam vurgu rengi.</div>
    </div>
  </div>

  <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; flex-grow: 1;">
    <div {panel("#ffffff", "padding: 24px 28px; display: flex; flex-direction: column; gap: 16px;")}>
      {label("UYGULAMA İKONU · FAVICON", mut)}
      <div style="display: flex; gap: 16px; align-items: flex-end;">
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
          <div style="width: 96px; height: 96px; border-radius: 22px; background: {a}; padding: 16px; box-sizing: border-box; box-shadow: 0 8px 20px rgba(0,0,0,0.12);">{app_color}</div>
          <div style="font-size: 11px; color: {mut};">renkli</div>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
          <div style="width: 96px; height: 96px; border-radius: 22px; background: {dk}; padding: 16px; box-sizing: border-box; box-shadow: 0 8px 20px rgba(0,0,0,0.12);">{app_dark}</div>
          <div style="font-size: 11px; color: {mut};">koyu</div>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
          <div style="width: 96px; height: 96px; border-radius: 22px; background: #ffffff; border: 1px solid rgba(0,0,0,0.1); padding: 16px; box-sizing: border-box;">{m_light}</div>
          <div style="font-size: 11px; color: {mut};">beyaz zemin</div>
        </div>
      </div>
      <div style="display: flex; gap: 22px; align-items: flex-end;">
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;"><div style="width: 32px; height: 32px;">{m_light}</div><div style="font-size: 11px; color: {mut};">32 px</div></div>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;"><div style="width: 16px; height: 16px;">{m_light}</div><div style="font-size: 11px; color: {mut};">16 px</div></div>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;"><div style="width: 16px; height: 16px;">{m_tile}</div><div style="font-size: 11px; color: {mut};">16 px sade</div></div>
        <div style="font-size: 12px; color: {mut}; max-width: 150px;">{html.escape(s.get("small_note", "16 px'te kuyruk çamura dönüyor; favicon kuyruksuz sürümü kullanır."))}</div>
      </div>
    </div>

    <div {panel("#ffffff", "padding: 24px 28px; display: flex; flex-direction: column; gap: 16px;")}>
      {label("BAĞLAM", mut)}
      <div style="background: {paper}; border-radius: 12px; padding: 14px 16px; display: flex; align-items: center; gap: 12px; box-shadow: 0 6px 18px rgba(0,0,0,0.08);">
        <div style="width: 40px; height: 40px; border-radius: 10px; background: {a}; padding: 7px; box-sizing: border-box; flex: none;">{app_color}</div>
        <div style="display: flex; flex-direction: column; gap: 2px; flex-grow: 1; min-width: 0;">
          <div style="display: flex; justify-content: space-between; gap: 8px;"><span style="font-size: 13px; font-weight: 700; color: {ink};">{html.escape(s["notif_title"])}</span><span style="font-size: 11px; color: {mut};">{html.escape(s["notif_time"])}</span></div>
          <div style="font-size: 12.5px; color: {ink};">{html.escape(s["notif_body"])}</div>
        </div>
      </div>
      <div style="display: flex; gap: 18px; justify-content: center; padding: 10px 0 0;">
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;"><div style="width: 54px; height: 54px; border-radius: 13px; background: #d7d9de;"></div><div style="font-size: 10px; color: {mut};">Takvim</div></div>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;"><div style="width: 54px; height: 54px; border-radius: 13px; background: #cfd3d8;"></div><div style="font-size: 10px; color: {mut};">Kamera</div></div>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;"><div style="width: 54px; height: 54px; border-radius: 13px; background: {a}; padding: 9px; box-sizing: border-box;">{app_color}</div><div style="font-size: 10px; font-weight: 700; color: {ink};">{html.escape(s["name"])}</div></div>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;"><div style="width: 54px; height: 54px; border-radius: 13px; background: #c7ccd2;"></div><div style="font-size: 10px; color: {mut};">Ayarlar</div></div>
      </div>
      <div style="font-size: 12px; color: {mut};">Bildirim kartı ve ana ekran sırası: komşu ikonlar nötr, bizimki tek renkli parlaklık.</div>
    </div>

    <div {panel("#ffffff", "padding: 24px 28px; display: flex; flex-direction: column; gap: 14px;")}>
      {label("RENK · TİPOGRAFİ", mut)}
      <div style="display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 10px;">
        {swatch(a, s["accent_name"], ink, mut)}
        {swatch(ink, s["ink_name"], ink, mut)}
        {swatch(paper, s["paper_name"], ink, mut)}
        {swatch(s["tint"], s["tint_name"], ink, mut)}
        {swatch(s["second"], s["second_name"], ink, mut)}
      </div>
      <div style="font-size: 12.5px; color: {ink}; line-height: 1.5;"><strong>Wordmark:</strong> {html.escape(s["font_spec"])}.<br><strong>Arayüz metni:</strong> sistem yazı tipi (Segoe UI / Roboto / SF); wordmark asla arayüz metninde kullanılmaz.<br><strong>En küçük boy:</strong> yatay lockup 120 px, ikon 16 px (sade sürüm).</div>
    </div>
  </div>
</div>
</x-dc>
</body>
</html>
'''

for s in SYS.values():
    open(s["file"], "w", encoding="utf-8").write(system(s))

# ------------------------------------------------------------------ canvas: sayfa 1 rafine, sayfa 2 ilk yönler
GAP = 100
SW, SH = 920, 660
canvas = dict(
    pages=[dict(id="page-1", name="Rafine"), dict(id="page-2", name="İlk yönler")],
    artboards=[
        dict(file="Main.dc.html", x=0, y=0, w=W, h=H, title="talimatname · çalışma adı", page="page-1"),
        dict(file="YapLutfenA.dc.html", x=W + GAP, y=0, w=W, h=H, title="yap lütfen · A · Rica", page="page-1"),
        dict(file="TamamlistB.dc.html", x=2 * (W + GAP), y=0, w=W, h=H, title="tamamlist · B · Mesaj", page="page-1"),
        dict(file="Tembihle.dc.html", x=3 * (W + GAP), y=0, w=W, h=H, title="tembihle · isim testi kartı", page="page-1"),
        dict(file="YapLutfenB.dc.html", x=0, y=0, w=SW, h=SH, title="yap lütfen · B · Kutu", page="page-2"),
        dict(file="YapLutfenC.dc.html", x=SW + 80, y=0, w=SW, h=SH, title="yap lütfen · C · Not", page="page-2"),
        dict(file="TamamlistA.dc.html", x=0, y=SH + 200, w=SW, h=SH, title="tamamlist · A · Tik-liste", page="page-2"),
        dict(file="TamamlistC.dc.html", x=SW + 80, y=SH + 200, w=SW, h=SH, title="tamamlist · C · Damga", page="page-2"),
    ],
    annotations=[
        dict(id="not-name", x=0, y=H + 34, w=W, text=SYS["name"]["note"], page="page-1"),
        dict(id="not-rica-rafine", x=W + GAP, y=H + 34, w=W, text=SYS["rica"]["note"], page="page-1"),
        dict(id="not-mesaj-rafine", x=2 * (W + GAP), y=H + 34, w=W, text=SYS["mesaj"]["note"], page="page-1"),
        dict(id="not-tembih", x=3 * (W + GAP), y=H + 34, w=W, text=SYS["tembih"]["note"], page="page-1"),
        dict(id="not-secim", x=0, y=-150, w=1400, text="Çalışma adı (12 Eylül 2026): talimatname — Mühür sistemi esas (önceki çalışma adları: Talimat, yap lütfen). İsim testi: Talimatname her görüşmede gösterilir; yanına yap lütfen / tamamlist / tembihle'den ikisi dönüşümlü. Kesin karar 20 tepkiden sonra. Elenen ilk yönler 'İlk yönler' sayfasında.", page="page-1"),
        dict(id="not-ilk", x=0, y=-120, w=900, text="İlk turdaki dört yön, referans için. Seçilmedi; rafine edilmedi.", page="page-2"),
    ],
    launch=dict(view="canvas", page="page-1"),
)
json.dump(canvas, open("canvas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rafine:", [s["file"] for s in SYS.values()])
