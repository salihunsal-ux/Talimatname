# -*- coding: utf-8 -*-
"""Altı logo yönü için .dc.html artboard'ları ve canvas.json üretir. Çalıştır: python build_artboards.py"""
import json, html

F = json.load(open("fonts/fonts.json", encoding="utf-8"))
W, H = 920, 660

# ------------------------------------------------------------------ ikonlar (inline SVG, 64x64 ızgara)
def ico_bubble_check(fill, check, tail="left"):
    tail_path = "M18 46 L14 60 L30 48 Z" if tail == "left" else "M46 46 L50 60 L34 48 Z"
    return (f'<svg viewBox="0 0 64 64" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">'
            f'<rect x="4" y="6" width="56" height="44" rx="16" fill="{fill}"></rect>'
            f'<path d="{tail_path}" fill="{fill}"></path>'
            f'<path d="M20 29 L28 37 L44 21" fill="none" stroke="{check}" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"></path>'
            f'</svg>')

def ico_checkbox(stroke, check, bg="none"):
    return (f'<svg viewBox="0 0 64 64" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">'
            f'<rect x="7" y="7" width="50" height="50" rx="13" fill="{bg}" stroke="{stroke}" stroke-width="6"></rect>'
            f'<path d="M19 33 L28 42 L46 22" fill="none" stroke="{check}" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"></path>'
            f'</svg>')

def ico_note(fill, fold, check):
    return (f'<svg viewBox="0 0 64 64" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">'
            f'<g transform="rotate(-6 32 32)">'
            f'<path d="M10 8 H54 V42 L42 54 H10 Z" fill="{fill}"></path>'
            f'<path d="M54 42 L42 42 L42 54 Z" fill="{fold}"></path>'
            f'<path d="M19 31 C22 33 25 37 27 40 C31 31 36 24 45 18" fill="none" stroke="{check}" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"></path>'
            f'</g></svg>')

def ico_list(tile, line, check, checkbg):
    return (f'<svg viewBox="0 0 64 64" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">'
            f'<rect x="4" y="4" width="56" height="56" rx="15" fill="{tile}"></rect>'
            f'<circle cx="18" cy="20" r="4" fill="none" stroke="{line}" stroke-width="3"></circle>'
            f'<rect x="27" y="18" width="22" height="4" rx="2" fill="{line}"></rect>'
            f'<circle cx="18" cy="32" r="4" fill="none" stroke="{line}" stroke-width="3"></circle>'
            f'<rect x="27" y="30" width="16" height="4" rx="2" fill="{line}"></rect>'
            f'<circle cx="18" cy="44" r="6" fill="{checkbg}"></circle>'
            f'<path d="M14.5 44 L17 46.5 L21.5 41.5" fill="none" stroke="{check}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"></path>'
            f'<rect x="27" y="42" width="19" height="4" rx="2" fill="{line}"></rect>'
            f'</svg>')

def ico_seal(ring, check):
    return (f'<svg viewBox="0 0 64 64" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">'
            f'<circle cx="32" cy="32" r="27" fill="none" stroke="{ring}" stroke-width="5"></circle>'
            f'<circle cx="32" cy="32" r="20" fill="none" stroke="{ring}" stroke-width="2" stroke-dasharray="3 4"></circle>'
            f'<path d="M22 33 L29 40 L43 24" fill="none" stroke="{check}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"></path>'
            f'</svg>')

# ------------------------------------------------------------------ yönler
DIRS = [
 dict(file="Main.dc.html", name="yap lütfen", key="A", title="Rica", fonts=["baloo"],
      idea="Mesaj balonu: WhatsApp'taki ricanın kendisi. Balonun kuyruğu var, içinde tik — soru değil, sıcak bir istek.",
      bg="#fbf6f1", surface="#ffffff", ink="#1e2230", muted="#7a7f8a", accent="#e96a48", dark="#191c24", dark_ink="#f6f1ea", dark_accent="#f08a6c",
      icon=lambda a, c: ico_bubble_check(a, c, "left"),
      word=lambda ink, acc, size: f'<span style="font-family:\'Baloo 2\',\'Segoe UI\',Arial,sans-serif;font-weight:800;font-size:{size}px;line-height:1;letter-spacing:-0.02em;color:{ink}">yap lütfen</span>',
      note="A · Rica — Artı: en sıcak ton, personel tarafında 'gözetim' okunmuyor; balon = yerine geçtiği WhatsApp mesajı. Eksi: yuvarlak font ve balon tüketici uygulaması gibi durabilir; kurumsal alıcıya 'ciddi araç' hissi zayıf."),
 dict(file="YapLutfenB.dc.html", name="yap lütfen", key="B", title="Kutu", fonts=["bricolage"],
      idea="Kontrol kutusu: liste maddesi işaretlenir. Raporlardaki Bricolage Grotesque ile aynı aile — ürün ve belgeler tek sesle konuşur.",
      bg="#f3f6f4", surface="#ffffff", ink="#151c22", muted="#77838c", accent="#1e7c79", dark="#0f1315", dark_ink="#e7ece9", dark_accent="#4fb8b3",
      icon=lambda a, c: ico_checkbox(a, c),
      word=lambda ink, acc, size: f'<span style="font-family:\'Bricolage Grotesque\',\'Trebuchet MS\',Arial,sans-serif;font-weight:700;font-size:{size}px;line-height:1;letter-spacing:-0.025em;color:{ink}">yap <span style="color:{acc}">lütfen</span></span>',
      note="B · Kutu — Artı: kanıt/denetim ürünü gibi duruyor, B2B alıcıya güven verir; fizibilite ve kapsam belgeleriyle aynı görsel dil. Eksi: kontrol kutusu ikonu kategoride en çok kullanılan motif; ayırt ediciliği kelimeye ve renge kalıyor."),
 dict(file="YapLutfenC.dc.html", name="yap lütfen", key="C", title="Not", fonts=["barlow", "caveat"],
      idea="Şef notu: 'lütfen' el yazısıyla. Mutfak kapısına yapıştırılan not kâğıdı — talimatın en insani hâli.",
      bg="#faf8f2", surface="#ffffff", ink="#232323", muted="#8a857a", accent="#e4b23f", dark="#1b1a17", dark_ink="#f4efe3", dark_accent="#e9be55",
      icon=lambda a, c: ico_note(a, "#c9992e" if a == "#e4b23f" else "#cfa640", c),
      word=lambda ink, acc, size: (f'<span style="display:inline-flex;align-items:baseline;gap:{round(size*0.18)}px">'
                                   f'<span style="font-family:\'Barlow Semi Condensed\',\'Arial Narrow\',Arial,sans-serif;font-weight:700;font-size:{size}px;line-height:1;letter-spacing:-0.01em;color:{ink}">yap</span>'
                                   f'<span style="font-family:Caveat,\'Segoe Print\',cursive;font-weight:700;font-size:{round(size*1.22)}px;line-height:1;color:{ink}">lütfen</span></span>'),
      note="C · Not — Artı: rica tonu görsel olarak da rica; yeme-içme sektörünün kâğıt-not kültürüne bağlanıyor, akılda kalıcı. Eksi: iki font + el yazısı küçük boyutta (uygulama ikonu, favicon) zayıflar; yurt dışına taşınmaz; 'ciddiyet' itirazı gelebilir."),
 dict(file="TamamlistA.dc.html", name="tamamlist", key="A", title="Tik-liste", fonts=["outfit"],
      idea="Üç satırlık liste, son madde tamam: ürünün kendisi ikon olmuş. 'list' vurgusu renkle.",
      bg="#f2f7f4", surface="#ffffff", ink="#142230", muted="#6f7d86", accent="#1c9c76", dark="#0f1a17", dark_ink="#e9f1ec", dark_accent="#3fbf95",
      icon=lambda a, c: ico_list(a, c, a, c),
      word=lambda ink, acc, size: f'<span style="font-family:Outfit,\'Segoe UI\',Arial,sans-serif;font-weight:700;font-size:{size}px;line-height:1;letter-spacing:-0.03em;color:{ink}">tamam<span style="color:{acc}">list</span></span>',
      note="A · Tik-liste — Artı: ne olduğu bir bakışta anlaşılır; uygulama ikonu olarak güçlü; yeşil-teal 'tamam' rengi evrensel. Eksi: kategori ikonografisi (liste + tik) ile ayırt edicilik düşük; 'tamam' kelimesindeki sıcaklık ikonda görünmüyor."),
 dict(file="TamamlistB.dc.html", name="tamamlist", key="B", title="Mesaj", fonts=["jakarta"],
      idea="'Tamam' cevabı: sağ kuyruklu balon, büyük tik. Yapılan işin bildirimi — merkezde biten döngü.",
      bg="#f4f4fb", surface="#ffffff", ink="#1b1b2e", muted="#767690", accent="#4b4fd6", dark="#14142a", dark_ink="#ecebf7", dark_accent="#8b8ff0",
      icon=lambda a, c: ico_bubble_check(a, c, "right"),
      word=lambda ink, acc, size: f'<span style="font-family:\'Plus Jakarta Sans\',\'Segoe UI\',Arial,sans-serif;font-weight:800;font-size:{size}px;line-height:1;letter-spacing:-0.035em;color:{ink}">tamamlist</span>',
      note="B · Mesaj — Artı: hikâyeyi taşıyor (personelin 'tamam' cevabı), indigo B2B yazılım kategorisinde tanıdık ve güvenilir; yurt dışına doğrudan taşınır. Eksi: balon+tik kombinasyonu mesajlaşma uygulamalarına (WhatsApp, Telegram) fazla yakın; yap lütfen A ile aynı motif — ikisi birlikte finale kalırsa biri değişmeli."),
 dict(file="TamamlistC.dc.html", name="tamamlist", key="C", title="Damga", fonts=["archivo"],
      idea="Onay mührü: kanıt ve denetim izi. Dar, büyük harf; damga kırmızısı yalnızca mühürde.",
      bg="#f8f5f1", surface="#ffffff", ink="#23201f", muted="#857d76", accent="#c3402c", dark="#1a1817", dark_ink="#f3ede6", dark_accent="#e46f5a",
      icon=lambda a, c: ico_seal(a, c if c != "#ffffff" else a),
      word=lambda ink, acc, size: f'<span style="font-family:\'Archivo Narrow\',\'Arial Narrow\',Arial,sans-serif;font-weight:700;font-size:{size}px;line-height:1;letter-spacing:0.08em;color:{ink}">TAMAMLIST</span>',
      note="C · Damga — Artı: 'kanıt' fikrini tek başına taşıyan yön; denetim PDF'i ve kalite ekibi persona'sıyla örtüşür; tescilde ayırt edici. Eksi: resmî/soğuk; personel uygulamasında 'kontrol ediliyorum' hissi verebilir; büyük harf Türkçe I/İ tuzağına açık (TAMAMLİST değil TAMAMLIST — bilinçli)."),
]

def seal_icon_fix(d, a, c):
    return d["icon"](a, c)

def artboard(d):
    fonts_css = "".join(F[k]["css"] for k in d["fonts"])
    ink, acc, bg, sf, mut = d["ink"], d["accent"], d["bg"], d["surface"], d["muted"]
    dk, dki, dka = d["dark"], d["dark_ink"], d["dark_accent"]
    # ikon varyantları
    if d["key"] == "B" and d["name"] == "yap lütfen":
        ic_light = d["icon"](acc, acc); ic_dark = d["icon"](dka, dka); ic_mono = d["icon"](ink, ink)
        ic_app = ico_checkbox("#ffffff", "#ffffff"); app_bg = acc
    elif d["title"] == "Damga":
        ic_light = ico_seal(acc, acc); ic_dark = ico_seal(dka, dka); ic_mono = ico_seal(ink, ink)
        ic_app = ico_seal("#ffffff", "#ffffff"); app_bg = acc
    elif d["title"] == "Not":
        ic_light = d["icon"](acc, ink); ic_dark = d["icon"](dka, "#1b1a17"); ic_mono = ico_note(ink, "#4a4a4a", "#ffffff")
        ic_app = ico_note("#ffffff", "#d9d4c7", ink); app_bg = acc
    elif d["title"] == "Tik-liste":
        ic_light = ico_list(acc, "#ffffff", acc, "#ffffff"); ic_dark = ico_list(dka, "#0f1a17", dka, "#0f1a17"); ic_mono = ico_list(ink, "#ffffff", ink, "#ffffff")
        ic_app = ico_list("#ffffff", acc, "#ffffff", acc); app_bg = acc
    else:  # balonlar
        ic_light = d["icon"](acc, "#ffffff"); ic_dark = d["icon"](dka, dk); ic_mono = d["icon"](ink, "#ffffff")
        ic_app = d["icon"]("#ffffff", acc); app_bg = acc
    word = d["word"]
    eyebrow = f'{d["name"].upper()} · YÖN {d["key"]}'
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
    a {{ color: {acc}; }} a:hover {{ color: {ink}; }}
  </style>
</helmet>
<div style="width: {W}px; height: {H}px; box-sizing: border-box; background: {bg}; color: {ink}; padding: 28px 32px; display: flex; flex-direction: column; gap: 18px; font-family: 'Segoe UI', Arial, sans-serif;">
  <div style="display: flex; flex-direction: column; gap: 4px;">
    <div style="font-size: 11px; font-weight: 700; letter-spacing: 0.14em; color: {mut};">{html.escape(eyebrow)}</div>
    <div style="display: flex; align-items: baseline; gap: 14px;">
      <div style="font-size: 22px; font-weight: 700; color: {ink};">{html.escape(d["title"])}</div>
      <div style="font-size: 13px; color: {mut}; line-height: 1.4;">{html.escape(d["idea"])}</div>
    </div>
  </div>
  <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; flex-grow: 1;">
    <div style="grid-column: span 2; display: flex; flex-direction: column; gap: 18px;">
      <div style="background: {sf}; border: 1px solid rgba(0,0,0,0.06); border-radius: 12px; padding: 36px 40px; display: flex; align-items: center; gap: 26px; flex-grow: 1;">
        <div style="width: 96px; height: 96px; flex: none;">{ic_light}</div>
        {word(ink, acc, 64)}
      </div>
      <div style="background: {dk}; border-radius: 12px; padding: 36px 40px; display: flex; align-items: center; gap: 26px; flex-grow: 1;">
        <div style="width: 96px; height: 96px; flex: none;">{ic_dark}</div>
        {word(dki, dka, 64)}
      </div>
    </div>
    <div style="display: flex; flex-direction: column; gap: 18px;">
      <div style="background: {sf}; border: 1px solid rgba(0,0,0,0.06); border-radius: 12px; padding: 22px; display: flex; flex-direction: column; align-items: center; gap: 12px; flex-grow: 1;">
        <div style="width: 116px; height: 116px; border-radius: 26px; background: {app_bg}; padding: 20px; box-sizing: border-box; box-shadow: 0 10px 24px rgba(0,0,0,0.12);">{ic_app}</div>
        <div style="font-size: 12px; color: {mut}; letter-spacing: 0.06em; font-weight: 600;">UYGULAMA İKONU</div>
      </div>
      <div style="background: {sf}; border: 1px solid rgba(0,0,0,0.06); border-radius: 12px; padding: 18px 22px; display: flex; flex-direction: column; gap: 14px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <div style="width: 32px; height: 32px; flex: none;">{ic_mono}</div>
          {word(ink, ink, 22)}
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
          <div style="width: 20px; height: 20px; flex: none;">{ic_light}</div>
          {word(ink, acc, 14)}
        </div>
        <div style="font-size: 12px; color: {mut}; letter-spacing: 0.06em; font-weight: 600;">TEK RENK · KÜÇÜK BOY</div>
      </div>
    </div>
  </div>
  <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: {mut};">
    <div>{"Yap lütfen, dedin. Yapıldı, kanıtıyla." if d["name"] == "yap lütfen" else "Yapılacak, yapıldı, tamam — kanıtıyla."}</div>
    <div style="display: flex; gap: 10px; align-items: center;">
      <span style="display: inline-block; width: 14px; height: 14px; border-radius: 4px; background: {acc};"></span><span>{acc}</span>
      <span style="display: inline-block; width: 14px; height: 14px; border-radius: 4px; background: {ink};"></span><span>{ink}</span>
      <span style="display: inline-block; width: 14px; height: 14px; border-radius: 4px; background: {bg}; border: 1px solid rgba(0,0,0,0.15);"></span><span>{bg}</span>
    </div>
  </div>
</div>
</x-dc>
</body>
</html>
'''

for d in DIRS:
    open(d["file"], "w", encoding="utf-8").write(artboard(d))

GAP_X, ROW_Y = 80, 860
boards, notes = [], []
for i, d in enumerate(DIRS):
    row, col = divmod(i, 3)
    x, y = col * (W + GAP_X), row * ROW_Y
    boards.append(dict(file=d["file"], x=x, y=y, w=W, h=H, title=f'{d["name"]} · {d["key"]} · {d["title"]}'))
    notes.append(dict(id=f"not-{d['file'].split('.')[0].lower()}", x=x, y=y + H + 34, w=W, text=d["note"]))
canvas = dict(artboards=boards, annotations=notes, launch=dict(view="canvas"))
json.dump(canvas, open("canvas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("artboards:", [d["file"] for d in DIRS])
