# -*- coding: utf-8 -*-
"""Gönderilebilir serbest geliştirici ilanı: serbest-gelistirici-ilani.html (+ --pdf ile Edge headless PDF).
Kaynak: ../07-serbest-gelistirici-secimi.md; ürün adı ve iletişim köşeli parantezle doldurulur."""
import os, sys, subprocess, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ILETISIM = "[e-posta]"

HTML = f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Talimatname — serbest geliştirici ilanı</title>
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@700&display=swap" rel="stylesheet">
<style>
:root{{--ink:#1c2128;--ink2:#4b5560;--mut:#7b8590;--line:#d6d9d2;--brand:#1f6f5b;--brand2:#dcebe5;--soft:#f3f1ea;--crit:#b8452f}}
*{{box-sizing:border-box}} html{{color-scheme:light}}
body{{margin:0;background:#e9e6de;color:var(--ink);font:10pt/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.sheet{{width:210mm;min-height:297mm;margin:18px auto;background:#fff;padding:14mm 16mm 12mm;box-shadow:0 10px 30px rgba(28,33,40,.14);display:flex;flex-direction:column}}
.wm{{font:700 20pt Bitter,Georgia,serif;color:var(--brand)}}
h1{{font:700 20pt/1.2 Bitter,Georgia,serif;margin:8px 0 4px}}
h2{{font:700 11.5pt Bitter,Georgia,serif;margin:10px 0 4px;padding-bottom:2px;border-bottom:1px solid var(--line)}}
p{{margin:4px 0}} .mut{{color:var(--mut)}} .small{{font-size:9pt}}
.lead{{font-size:10.5pt;color:var(--ink2)}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.role{{border:1.5px solid var(--line);border-radius:8px;padding:8px 10px}}
.role h3{{margin:0 0 4px;font:700 11pt Bitter,Georgia,serif;color:var(--brand)}}
ul{{margin:4px 0;padding-left:18px}} li{{margin:2px 0}}
table{{border-collapse:collapse;width:100%;font-size:9pt}} th,td{{padding:3px 6px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
th{{font-size:8pt;text-transform:uppercase;letter-spacing:.05em;color:var(--mut);background:var(--soft)}}
.box{{background:var(--brand2);border-radius:8px;padding:10px 12px;margin-top:10px}}
.ft{{margin-top:auto;border-top:1px solid var(--line);padding-top:6px;font-size:8.5pt;color:var(--mut);display:flex;justify-content:space-between}}
@media print{{body{{background:#fff}}.sheet{{width:auto;min-height:auto;margin:0;padding:0;box-shadow:none}}.sheet+.sheet{{break-before:page}}@page{{size:A4;margin:12mm 14mm}}}}
@media screen and (max-width:820px){{.sheet{{width:auto;margin:0;padding:16px;min-height:0}}.cols{{grid-template-columns:1fr}}}}
</style></head><body>
<div class="sheet">
<div class="wm">Talimatname</div>
<h1>İki serbest geliştirici arıyoruz: Flutter · Python/FastAPI</h1>
<p class="lead">Çok şubeli yeme-içme zincirleri için şube talimat listelerini <b>kanıtlı</b> hâle getiren bir ürün: personel açılış/kapanış/hijyen/soğuk zincir listesini şube tabletinden veya telefonundan tamamlar, fotoğraf ve sıcaklık ölçümüyle kanıtlar, yapamadığını sebebiyle bildirir; merkez her sabah yalnızca istisnaları görür ve denetim kaydını doğrulama kodlu PDF olarak alır. WhatsApp gruplarının yerine geçer.</p>
<p>İlk sürüm bilerek küçük ve net: 4 rol, 6 madde türü, tek sabit kural, sabit eskalasyon, kişi puanı yok. Kapsam, 175 gereksinim, ekranlar, 127 kabul testi ve 10 sprintlik backlog hazır; tıklanabilir prototipler ve örnek raporlar var. Ürünün ne yaptığını tek oturumda görmek için <b>10 sayfalık özellik föyü</b> (her özellik bir ekranla; son altı sayfası yol haritasının tasarım taslakları) başvuranlara gönderilir. İlk sürümün hemen ardındaki sıra da yazılı: v1.1'in ilk adayı <b>denetim dosyası ve denetçiye süreli, salt-okunur bağlantı</b> (E-13; gereksinimleri ve kabul testi hazır) — yani v1 biter bitmez ne yapılacağı belli. Sizden beklediğimiz: 2 haftalık sprintlerle, sağlam bir ilk sürümü <b>Mart 2027'de</b> yayına almak; ilk pilotlar Ocak–Şubat'ta.</p>

<div class="cols">
<div class="role"><h3>Backend / web geliştirici</h3>
<ul><li>Python 3.12 + FastAPI, PostgreSQL 16 (RLS, Alembic), Redis kuyruk, S3 uyumlu depo, OpenAPI</li>
<li>Tekrar kuralı ve pencere motoru (RRULE, saat dilimi, gece yarısı), bildirim servisi (push → SMS yedeği), PDF üretimi, hash zincirli olay günlüğü</li>
<li>Sprint 5'ten itibaren React + TypeScript yönetim paneli (yarı zaman)</li>
<li><b>Zorunlu:</b> üretimde çalışan en az bir API; test alışkanlığı; Docker. <b>Artı:</b> React, takvim/zaman dilimi işleri, KVKK farkındalığı, TR bulut/SMS sağlayıcıları</li></ul></div>
<div class="role"><h3>Mobil (Flutter) geliştirici</h3>
<ul><li>Flutter 3.x, Riverpod, Drift; iOS ve Android; düşük segment Android'de akıcılık</li>
<li>Çevrimdışı öncelikli: yerel kuyruk, idempotent senk, çakışma; kamera → damga → SHA-256, galeri kapalı; ortak cihaz (kiosk) modu, PIN, 2 dk kilit</li>
<li>Tasarım token'larıyla çalışma; Patrol/entegrasyon testleri</li>
<li><b>Zorunlu:</b> mağazada yayınlanmış en az bir Flutter uygulaması; yerel veritabanı ve senk deneyimi. <b>Artı:</b> arka plan işleri (WorkManager/BGTask), kiosk/ortak cihaz, erişilebilirlik</li></ul></div>
</div>

<h2>Çalışma şekli</h2>
<table><tbody>
<tr><th>Süre</th><td>Tam zamanlı, uzaktan; Sprint 0 (2 hafta) + 10 sprint ≈ 22 hafta, başlangıç <b>19 Ekim 2026</b>; 2 sprint tampon seçeneği</td></tr>
<tr><th>Ritim</th><td>Her gün 10:00'da 15 dk; 2 haftalık sprint (planlama, demo, geriye bakış); PR + inceleme + CI; ürün sahibi kurucu — sorularınıza 24 saat içinde cevap</td></tr>
<tr><th>Ücret</th><td>Sprint başına sabit ücret, sprint kabulüyle ödeme; teklifinizi günlük/sprint bazında yazın</td></tr>
<tr><th>Kapı</th><td>Sprint 2 sonunda pazar doğrulama sonucuyla devam/dur kararı (iki tarafa 2 hafta bildirim; yapılan iş ödenir). Şeffaf olalım: bu bir erken aşama ürünü</td></tr>
<tr><th>İlk iki hafta</th><td>Depo/CI/ortam kurulumu ve dört teknik spike: çevrimdışı senk, pencere motoru, kamera-damga-hash, push→SMS — kabul ölçütleri yazılı</td></tr>
<tr><th>Sözleşme</th><td>Serbest çalışan sözleşmesi: fikri mülkiyet devri, gizlilik ve KVKK taahhüdü; kod şirketin GitHub organizasyonunda</td></tr>
</tbody></table>

<h2>Seçim</h2>
<p>1) Başvuru eleme · 2) 45 dakikalık görüşme (prototip üzerinden konuşuruz) · 3) <b>3 saatlik ücretli mini görev</b> (backend: pencere motoru fikstürleri; mobil: çevrimdışı kuyruk + kamera) · 4) referans ve teklif. Takvim: başvuru 9 Ekim'e kadar, görüşmeler 10–15 Ekim.</p>
<div class="box"><b>Başvuru:</b> {ILETISIM} — CV veya portföy bağlantısı + üç satır: (1) neden bu ürün, (2) çözdüğünüz en zor çevrimdışı veya zaman dilimi problemi, (3) başlayabileceğiniz tarih ve tarifeniz. Konu satırı: "Talimatname — Backend" veya "Talimatname — Mobil".</div>
<p class="small mut" style="margin-top:8px">Talimatname çalışma adıdır. Ekip: kurucu (ürün sahibi), iki geliştirici, Sprint 3'ten itibaren yarı zamanlı tasarımcı, Sprint 6'dan itibaren yarı zamanlı QA. Teknoloji kararları ve gerekçeleri (ADR) ilk gün paylaşılır.</p>
<div class="ft"><span>Talimatname · serbest geliştirici ilanı · Ekim 2026</span><span>{ILETISIM}</span></div>
</div>
</body></html>"""

def main():
    out = os.path.join(HERE, "serbest-gelistirici-ilani.html")
    open(out, "w", encoding="utf-8").write(HTML); print(out)
    if "--pdf" in sys.argv:
        edge = next((p for p in [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"] if os.path.exists(p)), None)
        if not edge: print("Edge yok; tarayıcıdan yazdırın"); return
        pdf = out.replace(".html", ".pdf")
        if os.path.exists(pdf): os.remove(pdf)
        prof = tempfile.mkdtemp(prefix="talimatname-pdf-")
        subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={prof}", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", "--virtual-time-budget=5000", "file:///" + out.replace(os.sep, "/")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        for _ in range(120):
            if os.path.exists(pdf) and os.path.getsize(pdf) > 10_000: break
            time.sleep(0.5)
        print(pdf, "ok" if os.path.exists(pdf) else "HATA")

if __name__ == "__main__":
    main()
