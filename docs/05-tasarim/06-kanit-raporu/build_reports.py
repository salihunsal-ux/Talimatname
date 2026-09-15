# -*- coding: utf-8 -*-
"""Kanıt raporu örnekleri (basılabilir HTML → PDF): çalıştırma raporu, aylık tek sayfa özet, sıcaklık günlüğü.
Veri sentetiktir (Kahve Durağı test zinciri, 06-test/03); sayfalarda "ÖRNEK VERİ" filigranı vardır.
Çalıştır: python build_reports.py  → 01-calistirma-raporu.html, 02-aylik-ozet.html, 03-sicaklik-gunlugu.html
PDF: Edge/Chrome ile yazdır (build_reports.py --pdf, msedge bulunursa)."""
import os, sys, random, html, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
KOD = "TN-K7F3A-9C2D"
HASH = "9f1c4e0b…c3e7f3a"
URETIM = "14.09.2026 07:02:11"

CSS = """
:root{--ink:#1c2128;--ink2:#4b5560;--mut:#7b8590;--line:#d6d9d2;--paper:#fff;--bg:#e9e6de;--soft:#f3f1ea;--brand:#1f6f5b;--brand2:#dcebe5;--crit:#b8452f;--crit2:#f3ddd8;--warn:#b7791f;--warn2:#f6ebd2}
*{box-sizing:border-box}
html{color-scheme:light}
body{margin:0;background:var(--bg);color:var(--ink);font:10.5pt/1.42 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.sheet{width:210mm;min-height:297mm;margin:18px auto;background:var(--paper);padding:13mm 14mm 10mm;box-shadow:0 10px 30px rgba(28,33,40,.14);position:relative;display:flex;flex-direction:column;overflow:hidden}
.wm{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;pointer-events:none}
.wm span{font:700 64pt Bitter,Georgia,serif;color:rgba(184,69,47,.07);transform:rotate(-26deg);letter-spacing:.06em;white-space:nowrap}
.hd{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;border-bottom:2px solid var(--ink);padding-bottom:8px}
.logo{display:flex;align-items:center;gap:10px}
.mono{width:34px;height:34px;border:2px solid var(--ink);border-radius:8px;display:flex;align-items:center;justify-content:center;font:700 14pt Bitter,Georgia,serif;flex:none}
.chain{font:700 13pt Bitter,Georgia,serif;line-height:1.1}
.chain small{display:block;font:9pt system-ui,sans-serif;color:var(--ink2);font-weight:400;margin-top:2px}
h1{font:700 18pt/1.15 Bitter,Georgia,serif;margin:8px 0 1px}
.sub{color:var(--ink2);font-size:10pt}
.ver{text-align:right;font-size:8.5pt;color:var(--ink2);display:flex;gap:10px;align-items:flex-start;flex:none}
.ver b{display:block;font:700 10pt ui-monospace,Menlo,Consolas,monospace;color:var(--ink);letter-spacing:.04em}
.ver .h{font:8pt ui-monospace,Menlo,Consolas,monospace;color:var(--mut);white-space:nowrap}
.qr{width:64px;height:64px;flex:none}
.tn{font:700 10.5pt Bitter,Georgia,serif;color:var(--brand)}
.ft{margin-top:auto;border-top:1px solid var(--line);padding-top:6px;font-size:8pt;color:var(--mut);display:flex;justify-content:space-between;gap:12px}
.ft b{color:var(--ink2);font-weight:600}
.sum{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:6px;margin:9px 0 6px}
.box{border:1px solid var(--line);border-radius:6px;padding:5px 9px}
.box .l{font-size:8pt;text-transform:uppercase;letter-spacing:.06em;color:var(--mut)}
.box .v{font:700 13pt/1.15 Bitter,Georgia,serif;margin-top:1px;font-variant-numeric:tabular-nums}
.box .s{font-size:8pt;color:var(--ink2);margin-top:1px;line-height:1.3}
.box.crit{border-color:var(--crit);background:var(--crit2)} .box.crit .v{color:var(--crit)}
.box.ok{border-color:var(--brand);background:var(--brand2)} .box.ok .v{color:var(--brand)}
h2{font:700 11.5pt Bitter,Georgia,serif;margin:10px 0 5px;padding-bottom:2px;border-bottom:1px solid var(--line)}
h3{font:600 9pt system-ui,sans-serif;margin:8px 0 3px;color:var(--ink2);text-transform:uppercase;letter-spacing:.05em}
table{border-collapse:collapse;width:100%;font-size:9pt;font-variant-numeric:tabular-nums}
th,td{padding:3px 5px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{font-size:8pt;text-transform:uppercase;letter-spacing:.05em;color:var(--mut);font-weight:600;background:var(--soft)}
td.n,th.n{text-align:right;white-space:nowrap}
td.c{text-align:center;white-space:nowrap}
.st{display:inline-flex;align-items:center;gap:4px;font-weight:600;white-space:nowrap}
.st i{font-style:normal;display:inline-flex;width:14px;height:14px;border-radius:50%;align-items:center;justify-content:center;font-size:9pt;line-height:1;color:#fff;background:var(--brand)}
.st.x i{background:var(--crit)} .st.u i{background:var(--ink2)} .st.w i{background:var(--warn)} .st.o i{background:#fff;color:var(--mut);border:1px solid var(--mut)}
.st.x{color:var(--crit)}
.mut{color:var(--mut)} .small{font-size:8.5pt}
.note{font-size:8.5pt;color:var(--ink2);background:var(--soft);border-radius:4px;padding:2px 6px;display:inline-block;margin-top:2px}
.photos{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:4px}
.ph{position:relative;aspect-ratio:4/3;border-radius:5px;overflow:hidden;background:linear-gradient(135deg,#e6e3da,#cbc8be)}
.ph svg{position:absolute;inset:0;margin:auto;width:34%;height:34%;opacity:.35}
.ph .stp{position:absolute;left:0;right:0;bottom:0;background:rgba(28,33,40,.84);color:#fff;font:7pt/1.3 ui-monospace,Menlo,Consolas,monospace;padding:3px 6px}
.cap{font-size:8.5pt;color:var(--ink2);margin-top:3px} .cap b{color:var(--ink)}
.tl{list-style:none;margin:2px 0 0;padding:0;font-size:8.6pt}
.tl li{display:grid;grid-template-columns:58px 1fr;gap:8px;padding:1px 0;border-bottom:1px dotted var(--line)}
.tl .t{font:9pt ui-monospace,Menlo,Consolas,monospace;color:var(--ink2)}
.tl .crit{color:var(--crit);font-weight:600}
.verify{border:1.5px solid var(--ink);border-radius:6px;padding:6px 10px;font-size:8.3pt;margin-top:8px;display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center}
.verify p{margin:0 0 3px}
.kpi{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin:9px 0 6px}
.kpi .box .v{font-size:15pt}
.bars{display:grid;gap:3px;font-size:8.5pt;margin-top:4px}
.bar{display:grid;grid-template-columns:150px 1fr 44px;gap:6px;align-items:center}
.bar .tr{height:9px;background:var(--soft);border-radius:2px;overflow:hidden;border:1px solid var(--line)}
.bar .fl{height:100%;background:var(--brand)} .bar .fl.w{background:var(--warn)} .bar .fl.x{background:var(--crit)}
.bar .n{text-align:right;font-variant-numeric:tabular-nums}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.cols3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}
.oor{color:var(--crit);font-weight:700}
.miss{color:var(--mut)}
.tight th,.tight td{padding:2px 4px}
.legend{font-size:8.5pt;color:var(--ink2);display:flex;gap:14px;flex-wrap:wrap;margin-top:4px}
.legend span{display:inline-flex;align-items:center;gap:5px}
.sw{width:12px;height:12px;border-radius:3px;display:inline-block;border:1px solid var(--line)}
@media print{
  body{background:#fff}
  .sheet{width:auto;min-height:auto;margin:0;padding:0;box-shadow:none;overflow:visible}
  .sheet + .sheet{break-before:page}
  @page{size:A4;margin:12mm 14mm}
}
@media screen and (max-width:820px){.sheet{width:auto;margin:0;padding:16px;min-height:0}.sum,.kpi{grid-template-columns:1fr 1fr}.cols,.cols3{grid-template-columns:1fr}.photos{grid-template-columns:1fr 1fr}}
"""

QR = """<svg class="qr" viewBox="0 0 21 21" shape-rendering="crispEdges" aria-label="Doğrulama karekodu (örnek)"><rect width="21" height="21" fill="#fff"/><path fill="#1c2128" d="M0 0h7v7H0zM1 1v5h5V1zM2 2h3v3H2zM14 0h7v7h-7zM15 1v5h5V1zM16 2h3v3h-3zM0 14h7v7H0zM1 15v5h5v-5zM2 16h3v3H2zM8 0h1v1H8zM10 0h2v1h-2zM8 2h2v1H8zM11 2h1v2h-1zM9 4h2v1H9zM8 6h1v1H8zM10 5h1v3h-1zM12 5h1v1h-1zM0 8h1v1H0zM2 8h2v1H2zM5 8h3v1H5zM9 8h1v2H9zM11 8h2v1h-2zM14 8h1v1h-1zM16 8h1v2h-1zM18 8h1v1h-1zM20 8h1v1h-1zM1 10h2v1H1zM4 10h1v1H4zM6 10h2v1H6zM10 10h2v1h-2zM13 10h1v2h-1zM15 10h1v1h-1zM17 10h2v1h-2zM20 10h1v2h-1zM0 12h2v1H0zM3 12h1v1H3zM5 12h3v1H5zM9 12h1v1H9zM11 12h1v1h-1zM14 12h2v1h-2zM17 12h1v2h-1zM19 12h1v1h-1zM8 14h2v1H8zM11 14h2v1h-2zM14 14h1v1h-1zM16 14h1v1h-1zM18 14h3v1h-3zM8 16h1v2H8zM10 16h1v1h-1zM12 16h1v2h-1zM14 16h2v1h-2zM17 16h1v1h-1zM19 16h1v1h-1zM9 18h2v1H9zM13 18h1v1h-1zM15 18h2v1h-2zM18 18h1v2h-1zM20 18h1v1h-1zM8 20h1v1H8zM10 20h3v1h-3zM14 20h1v1h-1zM16 20h2v1h-2z"/></svg>"""

CAM = """<svg viewBox="0 0 24 24" fill="none" stroke="#1c2128" stroke-width="1.6" stroke-linejoin="round"><path d="M4 8h3l2-2h6l2 2h3v11H4z"/><circle cx="12" cy="13" r="3.2"/></svg>"""

def head(title, sub, chain="Kahve Durağı", chain_sub="Anadolu bölgesi · Kadıköy şubesi"):
    return f"""<div class="wm"><span>ÖRNEK VERİ</span></div>
<div class="hd"><div><div class="logo"><div class="mono">KD</div><div class="chain">{chain}<small>{chain_sub}</small></div></div>
<h1>{title}</h1><div class="sub">{sub}</div></div>
<div class="ver"><div><span class="tn">Talimatname</span><br>Doğrulama kodu<b>{KOD}</b><span class="h">olay zinciri özeti sha256 {HASH}</span><br>Üretim {URETIM} (sunucu saati)</div>{QR}</div></div>"""

def foot(p, n):
    return f"""<div class="ft"><span><b>Talimatname ile oluşturuldu</b> · kayıt değiştirilemez; düzeltmeler ek kayıt olarak görünür</span><span>Doğrulama {KOD} · üretim {URETIM}</span><span>Sayfa {p} / {n}</span></div>"""

def page(title, body_html):
    return f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{body_html}</body></html>"""

def st(kind, text):
    m = {"ok": ("", "✓"), "x": ("x", "✕"), "u": ("u", "–"), "w": ("w", "⏱"), "o": ("o", "○")}
    cls, ic = m[kind]
    return f'<span class="st {cls}"><i>{ic}</i>{text}</span>'

def photo(idx, item, when, hashv):
    return f"""<div><div class="ph">{CAM}<div class="stp">Kadıköy · {when} · Emre T. · KDK-T1</div></div><div class="cap"><b>Fotoğraf {idx}</b> · madde {item} · sha256 …{hashv}</div></div>"""

# ---------------------------------------------------------------- 1. Çalıştırma raporu
def calistirma():
    A = [  # (no, madde, tür, cevap html, saat, kanıt)
        (1, "Espresso makinesi geri yıkama; süt hortumları ve buhar çubuğu temizlendi", "onay", st("ok", "Yapıldı"), "23:02", ""),
        (2, "Kahve makinesi ve öğütücü temizlendi", "fotoğraf", st("ok", "Yapıldı"), "23:06", "Fotoğraf 1"),
        (3, "Süt dolabı sıcaklığı", "sıcaklık 0–4 °C · kritik", st("ok", "3,1 °C"), "23:09", ""),
        (4, "Mutfak buzdolabı sıcaklığı", "sıcaklık 0–4 °C · kritik", st("x", "6,0 °C · aralık dışı") + '<br><span class="note">Not: kapı contası gevşek, ürünler süt dolabına taşındı</span>', "23:20", "Fotoğraf 2 · aksiyon #418"),
        (5, "Dondurucu sıcaklığı", "sıcaklık −30…−18 °C · kritik", st("ok", "−19,5 °C"), "23:21", ""),
        (6, "Açık ürünler etiketlendi ve dolaba kaldırıldı", "çoktan seçmeli", st("ok", "Evet"), "23:24", ""),
        (7, "Fritöz kapatıldı, yağ süzüldü, kapağı kapatıldı", "çoktan seçmeli", st("ok", "Evet"), "23:25", ""),
        (8, "Tezgâh, kesme yüzeyleri ve lavabo dezenfekte; bulaşık bitti, makine kapağı açık", "onay", st("ok", "Yapıldı"), "23:27", ""),
    ]
    B = [
        (9, "Masalar, sandalyeler ve servis istasyonu silindi", "onay", st("ok", "Yapıldı"), "23:29", ""),
        (10, "Zemin süpürüldü ve paspaslandı", "fotoğraf · zorunlu", st("u", "Yapılamadı · malzeme yok") + '<br><span class="note">Not: paspas deterjanı bitti</span>', "23:30", "aksiyon #419"),
        (11, "Tuvaletler temizlendi; sabun, kâğıt havlu, tuvalet kâğıdı dolduruldu", "onay", st("ok", "Yapıldı"), "23:32", ""),
        (12, "Çöpler dışarı çıkarıldı, kovalara yeni poşet takıldı", "fotoğraf", st("ok", "Yapıldı"), "23:35", "Fotoğraf 3"),
    ]
    C = [
        ("—", "Kasa kapanışını “Kasa devri” listesinde tamamlayın", "talimat", '<span class="mut">cevap istemez</span>', "", ""),
        (13, "Gaz vanası kapatıldı", "çoktan seçmeli · kritik", st("ok", "Evet"), "23:37", ""),
        (14, "Ocak, fırın, ızgara, tost makinesi kapalı ve fişleri çekili; ışıklar, klima, tabela kapalı; su vanası kapalı", "onay", st("ok", "Yapıldı"), "23:38", ""),
        (15, "Kapı ve kepenk kilitlendi, alarm kuruldu", "fotoğraf", st("ok", "Yapıldı"), "23:41", "Fotoğraf 4"),
    ]
    def rows(items):
        return "".join(f"<tr><td class=\"c\">{n}</td><td>{m} <span class=\"mut small\">· {t}</span></td><td>{c}</td><td class=\"c\">{s}</td><td class=\"small\">{k}</td></tr>" for n, m, t, c, s, k in items)
    def sec(name, items):
        return f"<h3>{name}</h3><table><colgroup><col style=\"width:5%\"><col style=\"width:50%\"><col style=\"width:25%\"><col style=\"width:7%\"><col style=\"width:13%\"></colgroup><thead><tr><th class=\"c\">#</th><th>Madde</th><th>Cevap</th><th class=\"c\">Saat</th><th>Kanıt / bağ</th></tr></thead><tbody>{rows(items)}</tbody></table>"
    p1 = f"""<div class="sheet">{head("Çalıştırma raporu — Kapanış", "13 Eylül 2026 Cumartesi · pencere 22:00–01:30 (tolerans 120 dk) · şablon “Kapanış (kafe)” sürüm 3 · çalıştırma #KDK-2026-0913-KAP")}
<div class="sum">
<div class="box crit"><div class="l">Sonuç</div><div class="v">BAŞARISIZ</div><div class="s">kritik madde: mutfak buzdolabı 6,0 °C (madde 4)</div></div>
<div class="box"><div class="l">Puan (bilgi)</div><div class="v">%87</div><div class="s">13 / 15 geçti · 1 aralık dışı · 1 yapılamadı</div></div>
<div class="box"><div class="l">Zaman</div><div class="v">22:58 → 23:41</div><div class="s">pencere içinde · 43 dk · cihaz saati farkı +3 sn</div></div>
<div class="box"><div class="l">Kim / nerede</div><div class="v">Emre T.</div><div class="s">şube tableti KDK-T1 · konum: şube içinde (14 m) · kilit: ilk açan</div></div>
</div>
{sec("A · Bar ve mutfak", A)}{sec("B · Salon ve tuvalet", B)}{sec("C · Güvenlik ve kapanış", C)}
{foot(1, 2)}</div>"""
    photos = "".join([photo(1, "2 · Kahve makinesi ve öğütücü", "13.09.2026 23:06:41", "7f3a"),
                      photo(2, "4 · Mutfak buzdolabı (aralık dışı)", "13.09.2026 23:20:48", "c21e"),
                      photo(3, "12 · Çöp alanı", "13.09.2026 23:35:10", "0be4"),
                      photo(4, "15 · Kepenk ve kapı", "13.09.2026 23:41:00", "a90d")])
    p2 = f"""<div class="sheet">{head("Çalıştırma raporu — Kapanış (devam)", "Kanıt fotoğrafları, aksiyonlar, olay izi ve doğrulama")}
<h2>Kanıt fotoğrafları (4)</h2>
<div class="photos">{photos}</div><p class="cap" style="margin:4px 0 0"><b>Damga</b>: şube · tarih-saat · kullanıcı · cihaz, sunucu tarafında basılır; ham dosya ayrıca saklanır. Bayrak yok: kamera içinden çekildi, konum şube içinde, cihaz saati farkı +3 sn.</p>
<h2>Aksiyonlar (2)</h2>
<table><thead><tr><th>#</th><th>Kaynak</th><th>Öncelik</th><th>Atanan</th><th>Vade</th><th>Durum</th><th>Kapanış notu</th></tr></thead><tbody>
<tr><td>#418</td><td>Madde 4 · mutfak buzdolabı 6,0 °C</td><td>{st("x", "kritik")}</td><td>Ayşe K. (şube müdürü)</td><td>14 Eyl 03:20</td><td>{st("ok", "kapalı 14 Eyl 08:05")}</td><td class="small">“Servis geldi, kapı contası değişti; sabah ölçüm 3,4 °C.” · 1 fotoğraf</td></tr>
<tr><td>#419</td><td>Madde 10 · zemin yapılamadı (malzeme yok)</td><td>{st("w", "orta")}</td><td>Ayşe K.</td><td>16 Eyl 23:30</td><td>{st("o", "açık")}</td><td class="small">—</td></tr>
</tbody></table>
<h2>Olay izi (ekle-yalnız günlük)</h2>
<ul class="tl">
<li><span class="t">22:00:00</span><span>Pencere açıldı (sistem) · çalıştırma üretildi 7 gün önce</span></li>
<li><span class="t">22:58:12</span><span>Emre T. PIN ile giriş — şube tableti KDK-T1 · konum şube içinde</span></li>
<li><span class="t">22:58:30</span><span>Çalıştırma alındı (kilit: Emre T.); diğer kullanıcılar “Emre yapıyor” gördü</span></li>
<li><span class="t">23:06:41</span><span>Madde 2 fotoğraf yüklendi · sha256 …7f3a · damga basıldı</span></li>
<li><span class="t">23:20:05</span><span class="crit">Madde 4: 6,0 °C aralık dışı → kritik → aksiyon #418 açıldı (Ayşe K., vade 4 sa) · push Ayşe K. teslim 23:20:07 · push Murat D. teslim 23:20:09</span></li>
<li><span class="t">23:20:48</span><span>Madde 4 fotoğraf + not kaydedildi · sha256 …c21e</span></li>
<li><span class="t">23:30:15</span><span>Madde 10 yapılamadı (malzeme yok) → aksiyon #419 (Ayşe K., orta, vade 72 sa) · push Ayşe K. teslim 23:30:16</span></li>
<li><span class="t">23:41:02</span><span><b>Gönderildi</b> · sonuç: başarısız (kritik madde) · puan %87 · kayıt kilitlendi</span></li>
<li><span class="t">23:41:03</span><span>Olay zinciri özeti güncellendi (önceki_hash + olay)</span></li>
<li><span class="t">07:00:00</span><span>Sabah özeti gönderildi: Murat D. (push + e-posta), Selin Y. (e-posta)</span></li>
<li><span class="t">08:05:30</span><span>Aksiyon #418 kapatıldı — Ayşe K. · not + 1 fotoğraf</span></li>
</ul>
<p class="small mut" style="margin:6px 0 0">Cevap saatleri sunucu zamanıdır (Europe/Istanbul). Yapılamadı sebebi personel tarafından seçilmiş, not personelin kendi ifadesidir. Kritik maddede aralık dışı ölçüm çalıştırmayı “başarısız” yapar; puan yalnızca bilgi amaçlıdır (BR-07).</p>
<div class="verify"><div><p><b>Bu rapor nasıl doğrulanır?</b> Doğrulama kodu ve olay zinciri özeti, Talimatname sunucusundaki ekle-yalnız günlükten türetilir (ADR-0004). Gönderilmiş kayıt değiştirilemez; sonradan yapılan her düzeltme ayrı bir “ek” kaydı olarak eski kaydın yanında görünür. Kanıt dosyalarının SHA-256 özetleri cevaba bağlıdır; damga sunucu zamanıyla basılır.</p><p class="mut">Çevrimiçi doğrulama sayfası (kod girip zincir kontrolü) v1.x kapsamındadır; v1'de kod ve özet raporda taşınır.</p></div>{QR}</div>
{foot(2, 2)}</div>"""
    return page("Çalıştırma raporu — Kapanış · Kadıköy · 13.09.2026", p1 + p2)

# ---------------------------------------------------------------- 2. Aylık tek sayfa
def aylik():
    def bar(label, pct, n, cls=""):
        return f'<div class="bar"><span>{label}</span><div class="tr"><div class="fl {cls}" style="width:{pct}%"></div></div><span class="n">{n}</span></div>'
    weeks = "".join(bar(w, p, f"%{p}") for w, p in [("Hafta 32 (3–9 Ağu)", 78), ("Hafta 33", 80), ("Hafta 34", 83), ("Hafta 35 (24–31 Ağu)", 84)])
    bolge = "".join(f"<tr><td>{b}</td><td class=\"n\">{s}</td><td class=\"n\">{z}</td><td class=\"n\">{k}</td><td class=\"n\">{f}</td><td class=\"n\">{y}</td></tr>" for b, s, z, k, f, y in
                    [("Anadolu", 12, "%83", 61, 38, 96), ("Avrupa", 9, "%80", 58, 41, 94), ("Ege", 4, "%76", 36, 17, 50)])
    low = "".join(bar(s, p, f"%{p}", "x" if p < 75 else "w") for s, p in [("Bornova", 68), ("Bakırköy", 71), ("Kartal", 74), ("Pendik", 77), ("Karşıyaka", 78)])
    high = "".join(bar(s, p, f"%{p}") for s, p in [("Kadıköy", 94), ("Ataşehir", 92), ("Üsküdar", 91)])
    unable = "".join(f"<tr><td>{m}</td><td class=\"n\">{n}</td><td class=\"small\">{r}</td></tr>" for m, n, r in
                     [("Zemin süpürüldü ve paspaslandı (kapanış)", 38, "malzeme yok 26 · zaman yetmedi 9 · diğer 3"), ("Davlumbaz filtreleri (haftalık)", 22, "zaman yetmedi 14 · ekipman arızalı 6"), ("Çöpler dışarı çıkarıldı (kapanış)", 19, "zaman yetmedi 11 · yetkim yok 5"), ("Tuvaletler temizlendi (kapanış)", 15, "malzeme yok 9 · zaman yetmedi 6"), ("Fritöz yağı süzüldü (kapanış)", 12, "ekipman arızalı 8 · diğer 4")])
    crit = "".join(bar(l, p, n, "x") for l, p, n in [("Sıcaklık aralık dışı", 66, "63"), ("Kasa farkı (± ₺50 dışı)", 28, "27"), ("Haşere izi", 4, "4"), ("Gaz vanası açık kaldı", 2, "2")])
    body = f"""<div class="sheet">{head("Aylık özet — Ağustos 2026", "1–31 Ağustos 2026 · 25 şube · 3 bölge · 8 şablon · 11.240 planlı çalıştırma", chain_sub="Tüm zincir · operasyon özeti")}
<div class="kpi">
<div class="box ok"><div class="l">Zamanında</div><div class="v">%81</div><div class="s">hedef ≥ %80 · 9.104 çalıştırma</div></div>
<div class="box"><div class="l">Geç</div><div class="v">%8</div><div class="s">899 · tolerans içinde</div></div>
<div class="box crit"><div class="l">Kaçırıldı</div><div class="v">%5</div><div class="s">562 · şube müdürüne düştü</div></div>
<div class="box crit"><div class="l">Başarısız (kritik)</div><div class="v">96</div><div class="s">%0,9 · sıcaklık 63, kasa 27</div></div>
<div class="box"><div class="l">Yapılamadı</div><div class="v">240</div><div class="s">madde · malzeme yok %41</div></div>
<div class="box crit"><div class="l">Aksiyon vadesinde</div><div class="v">%78</div><div class="s">hedef ≥ %80 · 898 açıldı · 41 açık (9 gecikmiş)</div></div>
</div>
<p class="small mut" style="margin:0 0 6px">Kapalı gün 450 (%4) ve “yapılmayacak” 225 (%2) çalıştırma pay hesabında değildir. Sıcaklık: 12.980 ölçüm, 63 aralık dışı (%0,5). Fotoğraf zorunlu maddelerde kanıt %97.</p>
<div class="cols">
<div><h2>Haftalık zamanında tamamlama</h2><div class="bars">{weeks}</div>
<h2>Bölgeler</h2><table><thead><tr><th>Bölge</th><th class="n">Şube</th><th class="n">Zamanında</th><th class="n">Kaçırıldı</th><th class="n">Başarısız</th><th class="n">Yapılamadı</th></tr></thead><tbody>{bolge}</tbody></table>
<h2>Kritik başarısızlık kaynağı (96)</h2><div class="bars">{crit}</div></div>
<div><h2>En düşük 5 şube (zamanında)</h2><div class="bars">{low}</div>
<h2>En yüksek 3 şube</h2><div class="bars">{high}</div>
<h2>En sık yapılamayan maddeler</h2><table><thead><tr><th>Madde</th><th class="n">Adet</th><th>Sebepler</th></tr></thead><tbody>{unable}</tbody></table></div>
</div>
<h2>Bu ay dikkat</h2>
<ul class="small" style="margin:4px 0 0;padding-left:18px">
<li><b>Bornova ve Bakırköy</b> üst üste 3 hafta %75 altında; kaçırılan kapanışların %60'ı Cumartesi — vardiya planı sinyali.</li>
<li>Sıcaklık aralık dışı ölçümlerin 41'i <b>dondurucu</b> (Bakırköy 14, Kartal 9): iki şubede servis çağrılmış, biri açık aksiyon.</li>
<li>“Malzeme yok” sebebi ayın ikinci yarısında iki katına çıktı (paspas deterjanı, poşet) — merkez tedarik ritmi.</li>
<li>Aksiyon vadesinde kapanma %78, hedefin altında: gecikmiş 9 aksiyonun 7'si Ege bölgesinde.</li>
</ul>
<p class="small mut" style="margin:8px 0 0">Bu özet 07:00 sabah özetiyle aynı kaynaktan üretilir; şube kırılımı ve dönem PDF'leri panelden alınır. Kişi bazlı skor yoktur (ADR-0007).</p>
{foot(1, 1)}</div>"""
    return page("Aylık özet — Ağustos 2026 · Kahve Durağı", body)

# ---------------------------------------------------------------- 3. Sıcaklık günlüğü
def sicaklik():
    rnd = random.Random(20260913)
    eq = [("Süt dolabı", 0, 4, 2.9, 0.5), ("Mutfak buzdolabı", 0, 4, 3.2, 0.4), ("Teşhir vitrini", 0, 5, 3.6, 0.6), ("Dondurucu", -30, -18, -20.2, 0.6)]
    times = ["08:00", "14:00", "20:00"]
    days = [datetime.date(2026, 9, d) for d in range(1, 15)]
    data = {}
    for di, d in enumerate(days):
        for ti, t in enumerate(times):
            for ei, (name, lo, hi, mu, sd) in enumerate(eq):
                if d.day == 2 and t == "20:00":
                    data[(di, ti, ei)] = None; continue
                v = round(rnd.gauss(mu, sd), 1)
                v = max(lo + 0.3, min(hi - 0.3, v)) if hi > 0 else max(lo + 1, min(hi - 0.5, v))
                data[(di, ti, ei)] = v
    data[(12, 2, 1)] = 5.2   # 13 Eyl 20:00 mutfak buzdolabı
    data[(6, 1, 2)] = 5.6    # 7 Eyl 14:00 teşhir vitrini
    gun = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cts", "Paz"]
    def cell(v, lo, hi):
        if v is None: return '<td class="n miss">—</td>'
        s = f"{v:.1f}".replace(".", ",")
        if v < lo or v > hi: return f'<td class="n oor">▲ {s}</td>'
        return f'<td class="n">{s}</td>'
    rows = ""
    for di, d in enumerate(days):
        rows += f"<tr><td>{d.day} Eyl {gun[d.weekday()]}</td>" + "".join(cell(data[(di, ti, ei)], eq[ei][1], eq[ei][2]) for ei in range(4) for ti in range(3)) + "</tr>"
    thead1 = "<tr><th rowspan=\"2\">Gün</th>" + "".join(f"<th colspan=\"3\" class=\"c\">{n} <span class=\"mut\">({lo}…{hi} °C)</span></th>" for n, lo, hi, _, _ in eq) + "</tr>"
    thead2 = "<tr>" + "".join(f"<th class=\"n\">{t}</th>" for _ in eq for t in times) + "</tr>"
    # mini grafik: mutfak buzdolabı
    pts = [data[(di, ti, 1)] for di in range(14) for ti in range(3)]
    W, H, L, T = 560, 100, 30, 6
    def x(i): return L + i * (W - L - 6) / 41
    def y(v): return T + (7 - v) * (H - T - 18) / 7
    poly = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(pts) if v is not None)
    dots = "".join(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="3.2" fill="#b8452f"/>' for i, v in enumerate(pts) if v is not None and v > 4)
    chart = f"""<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:100%;height:auto" aria-label="Mutfak buzdolabı 1–14 Eylül">
<rect x="{L}" y="{y(4):.1f}" width="{W-L-6}" height="{y(0)-y(4):.1f}" fill="#dcebe5"/>
<line x1="{L}" x2="{W-6}" y1="{y(4):.1f}" y2="{y(4):.1f}" stroke="#1f6f5b" stroke-dasharray="3 3"/>
<line x1="{L}" x2="{W-6}" y1="{y(0):.1f}" y2="{y(0):.1f}" stroke="#1f6f5b" stroke-dasharray="3 3"/>
<text x="{L-4}" y="{y(4)+3:.0f}" font-size="9" text-anchor="end" fill="#4b5560">4 °C</text><text x="{L-4}" y="{y(0)+3:.0f}" font-size="9" text-anchor="end" fill="#4b5560">0 °C</text><text x="{L-4}" y="{y(7)+3:.0f}" font-size="9" text-anchor="end" fill="#4b5560">7 °C</text>
<polyline points="{poly}" fill="none" stroke="#1c2128" stroke-width="1.4"/>{dots}
{"".join(f'<text x="{x(di*3):.0f}" y="{H-3}" font-size="8.5" fill="#7b8590">{days[di].day}</text>' for di in range(0,14,2))}
<text x="{W-6}" y="{H-3}" font-size="8.5" fill="#7b8590" text-anchor="end">Eylül</text></svg>"""
    body = f"""<div class="sheet">{head("Sıcaklık günlüğü — Soğuk zincir", "1–14 Eylül 2026 · şablon “Soğuk zincir sıcaklık kaydı” · 3 ölçüm/gün (08:00, 14:00, 20:00) · 4 ekipman")}
<div class="sum">
<div class="box"><div class="l">Ölçüm</div><div class="v">164 / 168</div><div class="s">4 eksik: 2 Eyl 20:00 penceresi kaçırıldı (aksiyon #371, kapalı)</div></div>
<div class="box crit"><div class="l">Aralık dışı</div><div class="v">2</div><div class="s">7 Eyl vitrin 5,6 °C · 13 Eyl buzdolabı 5,2 °C</div></div>
<div class="box"><div class="l">Aksiyon</div><div class="v">2 / 2</div><div class="s">vadesinde kapalı (#392, #418)</div></div>
<div class="box"><div class="l">Ölçen</div><div class="v">4 kişi</div><div class="s">şube tableti · 6 ölçüm kişisel telefon</div></div>
</div>
<div style="overflow-x:auto"><table style="font-size:8pt" class="tight"><thead>{thead1}{thead2}</thead><tbody>{rows}</tbody></table></div>
<div class="legend"><span><span class="oor">▲</span> aralık dışı — fotoğraf + not zorunlu, kritik aksiyon</span><span><span class="miss">—</span> ölçüm yok (pencere kaçırıldı)</span><span>Değerler personelin girdiği ölçümdür; sunucu zamanıyla damgalanır, sonradan değiştirilemez</span></div>
<h2>Mutfak buzdolabı — 42 ölçüm</h2>
{chart}
<div class="cols" style="margin-top:8px">
<div><h3>Aralık dışı olaylar</h3><table><tbody>
<tr><td>7 Eyl 14:12</td><td>Teşhir vitrini 5,6 °C</td><td class="small">Zeynep A. · not: “kapı uzun açık kaldı, 20 dk sonra 4,1” · foto · aksiyon #392 Ayşe K., kapalı 7 Eyl 16:40</td></tr>
<tr><td>13 Eyl 20:04</td><td>Mutfak buzdolabı 5,2 °C</td><td class="small">Burak S. · not: “conta gevşek” · foto · aksiyon #418 (kapanışta 23:20 ölçüm 6,0 °C ile birleşti), kapalı 14 Eyl 08:05 — servis, conta değişimi</td></tr>
</tbody></table></div>
<div><h3>Denetçi notu</h3><p class="small" style="margin:0">Bu günlük, şubenin HACCP soğuk zincir kaydıdır. Kapanış ve açılış listelerindeki sıcaklık maddeleri ayrı çalıştırma raporlarında yer alır; istenirse aynı dönem için birleşik dönem PDF'i üretilir. Kabul aralıkları zincirin HACCP planından gelir; sıcak tutma ölçümü bu şubede yoktur.</p></div>
</div>
{foot(1, 1)}</div>"""
    return page("Sıcaklık günlüğü — Kadıköy · 1–14 Eylül 2026", body)

def main():
    out = {"01-calistirma-raporu.html": calistirma(), "02-aylik-ozet.html": aylik(), "03-sicaklik-gunlugu.html": sicaklik()}
    for name, content in out.items():
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
            f.write(content)
        print(name, f"{len(content)/1024:.0f} KB")
    if "--pdf" in sys.argv:
        edge = next((p for p in [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                                 r"C:\Program Files\Google\Chrome\Application\chrome.exe"] if os.path.exists(p)), None)
        if not edge:
            print("Edge/Chrome bulunamadı; PDF'i tarayıcıdan yazdırın."); return
        import time, tempfile
        for name in out:
            prof = tempfile.mkdtemp(prefix="talimatname-pdf-")  # her dosya için ayrı profil: Edge aynı profili paylaşınca ikinci isteği yutuyor
            src = "file:///" + os.path.join(HERE, name).replace("\\", "/")
            pdf = os.path.join(HERE, name.replace(".html", ".pdf"))
            if os.path.exists(pdf): os.remove(pdf)
            subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={prof}", "--no-pdf-header-footer",
                            f"--print-to-pdf={pdf}", "--virtual-time-budget=5000", src], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            for _ in range(120):  # Edge süreç döndükten 5–20 sn sonra yazıyor
                if os.path.exists(pdf) and os.path.getsize(pdf) > 10_000: break
                time.sleep(0.5)
            print(pdf, "ok" if os.path.exists(pdf) else "HATA")

if __name__ == "__main__":
    main()
