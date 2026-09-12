# -*- coding: utf-8 -*-
"""Tel-çerçeve üretici: 02-mobil-ekranlar.html ve 03-web-ekranlar.html. Çalıştır: python build_wireframes.py (05-tasarim/ekranlar içinden)"""
import html, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

CSS = """
<style>
:root{--ink:#1c2128;--mut:#6b7480;--line:#c9ced6;--fill:#eceff3;--fill2:#f7f8fa;--acc:#1f6f5b;--accs:#dcebe5;--warn:#b8452f;--warns:#f3ddd8;--amber:#b7791f;--ambers:#f6ebd2;--bg:#f4f4f2}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Segoe UI",Roboto,Arial,sans-serif;font-size:14px;line-height:1.4}
.wrap{max-width:1500px;margin:0 auto;padding:28px 24px 80px}
h1{font-size:26px;margin:0 0 6px}
.sub{color:var(--mut);margin:0 0 22px;max-width:90ch}
.legend{display:flex;flex-wrap:wrap;gap:10px 18px;font-size:12px;color:var(--mut);margin-bottom:26px}
.legend span b{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;margin-right:5px}
.grid{display:grid;gap:34px 28px}
.grid.mobile{grid-template-columns:repeat(auto-fill,minmax(400px,1fr))}
.grid.web{grid-template-columns:1fr}
.fr{display:flex;flex-direction:column;gap:10px}
.fr .hd{display:flex;align-items:baseline;gap:10px}
.fr .hd .id{font-family:Consolas,monospace;font-size:12px;color:var(--acc);font-weight:700}
.fr .hd .t{font-weight:700;font-size:15px}
.fr .hd .uc{color:var(--mut);font-size:12px;margin-left:auto}
.phone{width:390px;height:780px;background:#fff;border:2px solid var(--ink);border-radius:26px;padding:12px 12px 10px;display:flex;flex-direction:column;gap:8px;overflow:hidden;position:relative}
.tablet{width:100%;max-width:640px;height:420px;background:#fff;border:2px solid var(--ink);border-radius:18px;padding:12px;display:flex;flex-direction:column;gap:8px;overflow:hidden}
.desk{width:100%;height:720px;background:#fff;border:2px solid var(--ink);border-radius:8px;display:grid;grid-template-columns:200px 1fr;overflow:hidden}
.desk .side{background:var(--fill2);border-right:1px solid var(--line);padding:14px 12px;display:flex;flex-direction:column;gap:6px;font-size:13px}
.desk .side .brand{font-weight:700;margin-bottom:8px}
.desk .side .nav{padding:6px 8px;border-radius:5px;color:var(--mut)}
.desk .side .nav.on{background:var(--accs);color:var(--acc);font-weight:600}
.desk .main{padding:16px 18px;display:flex;flex-direction:column;gap:10px;overflow:hidden}
.top{display:flex;align-items:center;gap:8px;font-weight:700;font-size:15px;padding:2px 2px 6px;border-bottom:1px solid var(--line)}
.top .r{margin-left:auto;font-weight:400;color:var(--mut);font-size:12px}
.box{border:1px dashed var(--line);border-radius:6px;padding:8px 10px;background:var(--fill2)}
.box.solid{border-style:solid;background:#fff}
.box .h{font-weight:600;font-size:13px;margin-bottom:4px}
.box .s{color:var(--mut);font-size:12px}
.li{display:flex;align-items:center;gap:8px;padding:8px 6px;border-bottom:1px solid var(--line);font-size:13px}
.li:last-child{border-bottom:0}
.li .ic{width:22px;height:22px;border-radius:5px;border:1.5px solid var(--ink);flex:none;display:grid;place-items:center;font-size:12px}
.li .ic.ok{background:var(--acc);border-color:var(--acc);color:#fff}
.li .ic.x{background:var(--warns);border-color:var(--warn);color:var(--warn)}
.li .ic.w{background:var(--ambers);border-color:var(--amber);color:var(--amber)}
.li .m{margin-left:auto;color:var(--mut);font-size:12px;white-space:nowrap}
.btn{display:inline-block;padding:10px 14px;border-radius:8px;border:1.5px solid var(--ink);font-weight:600;font-size:13px;text-align:center}
.btn.p{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.big{padding:14px;width:100%}
.btn.g{color:var(--mut);border-color:var(--line)}
.btn.d{border-color:var(--warn);color:var(--warn)}
.row{display:flex;gap:8px;align-items:center}
.row.sb{justify-content:space-between}
.grow{flex-grow:1}
.chip{display:inline-block;padding:2px 8px;border-radius:10px;background:var(--fill);font-size:11px;color:var(--mut)}
.chip.ok{background:var(--accs);color:var(--acc)} .chip.x{background:var(--warns);color:var(--warn)} .chip.w{background:var(--ambers);color:var(--amber)}
.tabs{display:flex;margin-top:auto;border-top:1px solid var(--line);padding-top:8px}
.tabs div{flex:1;text-align:center;font-size:11px;color:var(--mut)}
.tabs div.on{color:var(--acc);font-weight:700}
.img{background:repeating-linear-gradient(45deg,#e4e7ec,#e4e7ec 6px,#f0f2f5 6px,#f0f2f5 12px);border:1px solid var(--line);border-radius:6px;display:grid;place-items:center;color:var(--mut);font-size:12px}
.prog{height:8px;background:var(--fill);border-radius:4px;overflow:hidden}
.prog i{display:block;height:100%;background:var(--acc)}
.n{display:inline-grid;place-items:center;width:18px;height:18px;border-radius:50%;background:var(--ink);color:#fff;font-size:11px;font-weight:700;margin-left:4px;vertical-align:1px}
.notes{font-size:12.5px;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:8px;padding:10px 12px;line-height:1.5}
.notes b{font-family:Consolas,monospace;color:var(--acc);font-weight:600}
.notes div{margin-bottom:3px}
table.wt{width:100%;border-collapse:collapse;font-size:12px}
table.wt th{text-align:left;color:var(--mut);font-weight:600;border-bottom:1px solid var(--ink);padding:5px 6px}
table.wt td{border-bottom:1px solid var(--line);padding:5px 6px}
.cell{width:100%;aspect-ratio:1;border-radius:4px}
.gridcells{display:grid;grid-template-columns:repeat(7,1fr);gap:4px}
.k{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.k div{border:1px solid var(--line);border-radius:8px;padding:12px;text-align:center;font-size:16px;font-weight:600}
.kbd{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.kbd div{border:1px solid var(--line);border-radius:6px;text-align:center;padding:8px;font-weight:600}
.three{display:grid;grid-template-columns:260px 1fr 300px;gap:12px;height:100%;min-height:0}
.col{border:1px dashed var(--line);border-radius:6px;padding:10px;display:flex;flex-direction:column;gap:8px;overflow:hidden;background:var(--fill2)}
.col .h{font-weight:700;font-size:13px}
.field{border:1px solid var(--line);border-radius:5px;padding:6px 8px;font-size:12px;background:#fff}
.field span{color:var(--mut);display:block;font-size:11px}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.kpi div{border:1px solid var(--line);border-radius:6px;padding:10px;background:#fff}
.kpi b{display:block;font-size:20px}
.kpi span{font-size:11px;color:var(--mut)}
</style>
"""

def n(i): return f'<span class="n">{i}</span>'
def li(text, ic="", meta="", cls=""):
    icon = f'<span class="ic {cls}">{ic}</span>' if ic or cls else '<span class="ic"></span>'
    return f'<div class="li">{icon}<span>{text}</span><span class="m">{meta}</span></div>'
def box(h, s="", solid=False, extra=""):
    return f'<div class="box{" solid" if solid else ""}"><div class="h">{h}</div>{f"<div class=s>{s}</div>" if s else ""}{extra}</div>'
def btn(t, cls=""): return f'<div class="btn {cls}">{t}</div>'
def tabs(active):
    names = ["Bugün", "Aksiyonlar", "Şubem", "Menü"]
    return '<div class="tabs">' + "".join(f'<div class="{"on" if a == active else ""}">{a}</div>' for a in names) + "</div>"
def top(t, r=""): return f'<div class="top">{t}<span class="r">{r}</span></div>'
def notes(items):
    return '<div class="notes">' + "".join(f'<div>{n(i+1)} {t}</div>' for i, t in enumerate(items)) + "</div>"
def frame(scr, title, uc, body, note_items, kind="phone"):
    inner = body if kind == "desk" else f'<div class="{kind}">{body}</div>'  # desk gövdesi zaten çerçeveyi içerir
    return (f'<div class="fr"><div class="hd"><span class="id">{scr}</span><span class="t">{html.escape(title)}</span><span class="uc">{uc}</span></div>'
            f'{inner}{notes(note_items)}</div>')

# ================================================================== MOBİL
M = []
M.append(frame("SCR-M-01", "Giriş", "UC-03",
    top("Talimatname") +
    box("Telefon numarası" + n(1), "+90 5__ ___ __ __") +
    btn("Kod gönder", "p big") +
    box("6 haneli kod" + n(2), "SMS ile geldi · 04:59 · <u>Tekrar gönder</u> (60 sn)") +
    '<div class="kbd"><div>1</div><div>2</div><div>3</div><div>4</div><div>5</div><div>6</div><div>7</div><div>8</div><div>9</div><div></div><div>0</div><div>⌫</div></div>' +
    box("Aydınlatma metni" + n(3), "Zincir adı · işlenen veriler · amaçlar · haklar … [Okudum ve anladım]") +
    box("Konum izni" + n(4), "Yalnızca bir maddeyi tamamladığınız anda, kanıtın şubede çekildiğini doğrulamak için. Sürekli takip yok. [İzin ver] [Şimdi değil]"),
    ["FR-0201 telefon + OTP; e-posta yok", "FR-0204 OTP 5 dk, 60 sn'de yeniden gönder, 3 hata → 15 dk blok", "FR-1307 sürümlü aydınlatma, onay zaman damgalı; metin değişince yeniden", "FR-1308 konum izni ayrı ekranda, gerekçeli; reddedilebilir (BR-15)"]))

M.append(frame("SCR-M-02", "Kiosk kilit ekranı (tablet, yatay)", "UC-04",
    top("Kadıköy şubesi · Şube cihazı", "Senk ✓ 21:58") +
    '<div class="k"><div>AY<br><small>Ayşe K.</small></div><div>EM<br><small>Emre T.</small></div><div>ZE<br><small>Zeynep A.</small></div><div>BU<br><small>Burak S.</small></div><div>SE<br><small>Selin Y.</small></div><div>+3</div></div>' +
    box("Emre T. — PIN" + n(1), "● ● ○ ○") +
    '<div class="kbd"><div>1</div><div>2</div><div>3</div><div>4</div><div>5</div><div>6</div><div>7</div><div>8</div><div>9</div><div>PIN unuttum' + n(2) + '</div><div>0</div><div>⌫</div></div>' +
    box("2 dk hareketsizlikte bu ekrana dönülür" + n(3), "Tamamlanmamış cevaplar korunur"),
    ["FR-0208 4 haneli PIN, ilk girişte belirlenir", "FR-0208 şube müdürü PIN sıfırlar; olay logda", "FR-0209 kilit süresi ayar (varsayılan 2 dk); FR-0210 5 hata → 1 dk blok (BR-19)"], kind="tablet"))

M.append(frame("SCR-M-03", "Bugün", "UC-08, UC-11, UC-14",
    top("Bugün · 12 Eyl", "Emre T. · Kadıköy") +
    box("Onay bekleyen duyuru" + n(1), "Alerjen prosedürü v2 — Okudum ve anladım →", solid=True) +
    li("Kapanış listesi <span class=chip>22:00–01:30</span>", "▶", "1 sa 12 dk kaldı" + n(2)) +
    li("Saatlik tuvalet kontrolü", "✓", "22:00 yapıldı", "ok") +
    li("Soğuk zincir ölçümü", "!", "Pencere kapandı · 40 dk tolerans" + n(3), "w") +
    li("Haftalık derin temizlik (pazartesi)", "", "Planlandı") +
    box("Bekleyen senk: 2 kayıt, 5 fotoğraf" + n(4), "Bağlantı gelince otomatik gönderilir") +
    btn("Sorun bildir" + n(5), "big") +
    tabs("Bugün"),
    ["FR-1103 onay bekleyen duyuru Bugün'ün üstünde", "FR-0601/0610 pencere geri sayımı ve durum rengi", "BR-02 tolerans içinde 'geç' uyarısı; BR-03 tolerans sonu kilit", "FR-0702/0708 çevrimdışı kuyruk rozeti", "FR-0806 liste dışı sorun bildirimi"]))

M.append(frame("SCR-M-04", "Liste çalıştırma", "UC-08, UC-09",
    top("Kapanış listesi", "01:30'a kadar · 48 dk") +
    '<div class="prog"><i style="width:58%"></i></div><div class="s" style="font-size:12px;color:var(--mut)">7 / 12 madde · bekliyor (çevrimdışı)' + n(1) + '</div>' +
    '<div class="box solid"><div class="h">Bölüm 1 · Bar</div>' +
    li("Kahve makinesi temizlendi <span class=chip>fotoğraf</span>", "✓", "23:02", "ok") +
    li("Süt dolabı sıcaklığı <span class=chip>0–4 °C</span>", "✓", "3,2 °C", "ok") +
    li("Tezgâh dezenfekte edildi", "", "") + "</div>" +
    '<div class="box solid"><div class="h">Bölüm 2 · Mutfak</div>' +
    li("Buzdolabı 2 sıcaklığı <span class=chip x>kritik</span>", "!", "6,0 °C → aksiyon" + n(2), "x") +
    li("Zemin yıkandı", "✗", "Yapılamadı: malzeme yok" + n(3), "w") +
    li("Çöpler alındı <span class=chip>fotoğraf</span>", "", "") + "</div>" +
    box("Sabahçıya not (isteğe bağlı)" + n(4), "…") +
    btn("Gönder (5 zorunlu madde eksik)" + n(5), "g big") +
    tabs("Bugün"),
    ["FR-0603 ilerleme ve kaldığı yerden devam; FR-0702 yerel kuyruk", "BR-06/08 kritik + aralık dışı → başarısız, fotoğraf+not, kritik aksiyon", "FR-0801 yapılamadı sebebiyle işaretli madde", "FR-1601 vardiya devri notu (Should)", "BR-05 zorunlu maddeler bitmeden gönderim pasif"]))

M.append(frame("SCR-M-05", "Madde bileşenleri", "UC-08",
    top("Buzdolabı 2 sıcaklığı", "Madde 8/12") +
    box("Sıcaklık (°C) · kabul 0–4" + n(1), '<div class="row"><div class="btn">−</div><div class="grow" style="text-align:center;font-size:28px;font-weight:700">6,0</div><div class="btn">+</div></div>') +
    box("Aralık dışı!" + n(2), "Fotoğraf ve not zorunlu; aksiyon şube müdürüne 4 saat vadeyle açılacak", solid=True) +
    '<div class="img" style="height:120px">Kamera · yalnızca uygulama içi çekim' + n(3) + '</div>' +
    box("Not", "Kompresör sesi geliyor…") +
    '<div class="row"><div class="btn d grow">Yapılamadı' + n(4) + '</div><div class="btn p grow">Kaydet ve ileri</div></div>' +
    box("Diğer bileşenler", "Onay ✓/✗ · Seçim (büyük düğmeler) · Sayı+birim · Metin · Video ≤20 sn · İmza · Barkod/QR · Tarih-saat · Talimat (görsel/PDF)" + n(5)) +
    tabs("Bugün"),
    ["FR-0305 kabul aralığı; ± adım düğmeleri", "BR-08 aralık dışı → koşullu mantık (fotoğraf, not, aksiyon)", "FR-0604/BR-14 yalnızca kamera; galeri yok; FR-0606 damga", "FR-0804 kritik maddede 'Yapılamadı' görünmez (bu maddede kritik olduğu için gerçek ekranda gizli)", "FR-0303 madde türleri; FR-0611 44 px hedefler"]))

M.append(frame("SCR-M-06", "Yapılamadı", "UC-10",
    top("Yapılamadı — Zemin yıkandı") +
    box("Sebep" + n(1), "") +
    li("Malzeme yok", "●", "", "ok") + li("Ekipman arızalı") + li("Zaman yetmedi") + li("Yetkim yok") + li("Diğer (not zorunlu)" + n(2)) +
    box("Not", "Deterjan bitti, tedarik gelmedi") +
    '<div class="img" style="height:90px">Fotoğraf (isteğe bağlı)</div>' +
    box("Kaydedince" + n(3), "Madde 'yapılamadı' olur · şube müdürüne aksiyon açılır (orta, 72 sa)") +
    btn("Kaydet", "p big") + tabs("Bugün"),
    ["FR-0801/0802 sebep seti (hesap düzeyinde düzenlenir)", "FR-0803 'Diğer' → not ≥ 5 karakter", "BR-10 otomatik aksiyon, atanan şube müdürü, vade önceliğe göre"]))

M.append(frame("SCR-M-07", "Sorun bildir", "UC-11",
    top("Sorun bildir") +
    box("Kategori" + n(1), "Ekipman · Tedarik · Hijyen · Güvenlik · Diğer") +
    box("İstasyon", "Mutfak ▾") +
    '<div class="img" style="height:130px">1–3 fotoğraf</div>' +
    box("Not", "Fritöz termostatı çalışmıyor") +
    box("Gönderince" + n(2), "Şube müdürüne düşer; aksiyona çevrilebilir veya sebep yazılarak kapatılır") +
    btn("Gönder", "p big") + tabs("Bugün"),
    ["FR-0806/0809 kategori seti hesap düzeyinde", "FR-0807/0808 aksiyona çevirme, yükseltme"]))

M.append(frame("SCR-M-08", "Aksiyonlarım ve aksiyon detayı", "UC-12",
    top("Aksiyonlar", "Bana · Şubem · Gecikmiş" + n(1)) +
    li("Buzdolabı 2 sıcaklık aralık dışı <span class=chip x>kritik</span>", "!", "3 sa 12 dk", "x") +
    li("Zemin yıkanamadı — deterjan", "", "2 gün") +
    li("Fritöz termostatı (sorun)", "", "gecikti" + n(2), "w") +
    box("Aksiyon: Buzdolabı 2 sıcaklık" + n(3), "Kaynak: kapanış listesi madde 8 · Kadıköy / Mutfak · Atanan: Ayşe K. · Vade: 03:41 · Durum: devam ediyor", solid=True) +
    box("Yorumlar" + n(4), "Ayşe 00:10: Servisi aradım, sabah geliyor · [fotoğraf]") +
    '<div class="row"><div class="btn grow">Devam</div><div class="btn p grow">Kapat (fotoğraf + not)' + n(5) + '</div></div>' +
    tabs("Aksiyonlar"),
    ["FR-0907 listeler ve filtreler; toplu kapatma yok", "FR-0910 gecikme bildirimi; BR-11 eskalasyon", "FR-0901 aksiyon alanları", "FR-0906 yorum dizisi (@bahsetme)", "FR-0905 kapanış kanıtı zorunlu; FR-0909 onaylı kapanış (Should)"]))

M.append(frame("SCR-M-09", "Duyuru onayı", "UC-14",
    top("Duyuru") +
    box("Alerjen prosedürü v2" + n(1), "Selin Y. · 10 Eyl · Tüm personel") +
    '<div class="img" style="height:170px">PDF önizleme</div>' +
    box("Metin", "1 Ekim'den itibaren … (zengin metin)") +
    box("İmza (bu duyuruda zorunlu)" + n(2), '<div class="img" style="height:60px">imza alanı</div>') +
    btn("Okudum ve anladım" + n(3), "p big") + tabs("Bugün"),
    ["FR-1101/1102 hedefli duyuru, ek", "FR-1106 imza zorunlu duyuru (Should)", "FR-1103 onay zaman damgalı; BR-25 48 sa sonra hatırlatma"]))

M.append(frame("SCR-M-10", "Yönetici görünümü (şube/bölge müdürü)", "UC-15, UC-19, UC-20",
    top("Bölgem · Anadolu", "12 şube · dün gece") +
    '<div class="gridcells">' + "".join(f'<div class="cell" style="background:{c}"></div>' for c in ["#1f6f5b"]*9 + ["#b7791f", "#b8452f", "#c9ced6"]) + "</div>" +
    '<div class="row" style="font-size:11px;color:var(--mut)"><span>■ tamamlandı 9</span><span>■ geç 1</span><span>■ kaçırıldı 1</span><span>■ kapalı 1</span>' + n(1) + "</div>" +
    li("Bakırköy — Kapanış <span class=chip x>kaçırıldı</span>", "!", "eskalasyon 2. adım" + n(2), "x") +
    li("Kadıköy — Kapanış <span class=chip w>başarısız %88</span>", "", "2 aksiyon", "w") +
    box("Bugünkü atamalar (şube müdürü)" + n(3), "Kapanış → Emre T. ▾ · Saatlik tuvalet → Zeynep A. ▾") +
    box("Gözden geçir" + n(4), "Kadıköy kapanış · [Gözden geçirildi] · not") +
    tabs("Şubem"),
    ["FR-1211 yönetici mobil özet ızgarası", "FR-0912/0913 eskalasyon adımı görünür", "FR-0519/0520 günlük yeniden atama, anında bildirim", "FR-1701 gözden geçirme (Should)"]))

M.append(frame("SCR-M-11", "Senk durumu ve profil", "UC-09",
    top("Menü") +
    box("Senkronizasyon" + n(1), "Bekleyen: 2 kayıt · 5 fotoğraf (1,4 MB) · Son senk 21:58 · [Şimdi senkle]") +
    box("Hata ayrıntısı" + n(2), "kanıt 7f3a… yükleme 3/5 deneme · [Destek için kopyala]") +
    li("Profil · Emre T. · +90 5…") + li("PIN değiştir") + li("Bildirim tercihleri" + n(3)) + li("Aydınlatma metni v3") + li("Kullanıcı değiştir (kiosk)") + li("Çıkış") +
    tabs("Menü"),
    ["FR-0708 senk durumu; FR-0706 kuyruk sınırı 500 / 72 sa", "NFR-12 cihaz günlükleri destek için", "FR-1003 tercihler; kritik olaylar kapatılamaz"]))

# ================================================================== WEB
def side(active):
    items = ["Pano", "Şubeler", "Personel", "Şablonlar", "Planlar", "Aksiyonlar", "Duyurular", "Raporlar", "Denetim izi", "Ayarlar"]
    return '<div class="side"><div class="brand">Talimatname</div>' + "".join(f'<div class="nav {"on" if i == active else ""}">{i}</div>' for i in items) + '<div style="margin-top:auto;font-size:11px;color:var(--mut)">Selin Y. · Operasyon müdürü</div></div>'
def desk(active, main): return f'<div class="desk">{side(active)}<div class="main">{main}</div></div>'
def field(l, v=""): return f'<div class="field"><span>{l}</span>{v}</div>'

W = []
W.append(frame("SCR-W-01", "Kurulum sihirbazı", "UC-01",
    desk("Pano",
        top("Kurulum · Adım 2/5 · Şubeler", "Marka ✓ · Şubeler · Şablon · Plan · Personel") +
        '<div class="row"><div class="box grow"><div class="h">Excel şablonu' + n(1) + '</div><div class="s">İndir → doldur → yükle (bölge, şube kodu, ad, adres, saat dilimi, çalışma saatleri, istasyonlar)</div></div><div class="box grow"><div class="h">Yükleme sonucu' + n(2) + '</div><div class="s">25 satır · 23 geçerli · 2 hatalı (saat dilimi boş) → hatalı satırları indir</div></div></div>' +
        '<table class="wt"><tr><th>Kod</th><th>Şube</th><th>Bölge</th><th>Saat dilimi</th><th>Saatler</th><th>Durum</th></tr><tr><td>KDK</td><td>Kadıköy</td><td>Anadolu</td><td>Europe/Istanbul</td><td>09–24</td><td><span class="chip ok">geçerli</span></td></tr><tr><td>BKR</td><td>Bakırköy</td><td>Avrupa</td><td>—</td><td>08–23</td><td><span class="chip x">saat dilimi eksik</span></td></tr></table>' +
        '<div class="row" style="margin-top:auto"><div class="btn g">Geri</div><div class="grow"></div><div class="btn">Elle şube ekle</div><div class="btn p">Devam → Şablon seç' + n(3) + '</div></div>'),
    ["FR-0105 Excel şablonu sürümlü", "FR-0106 satır bazlı doğrulama; %20 üstü hata → yükleme reddi; hatalı satır raporu", "FR-1401 sihirbaz kaldığı yerden devam; hedef 1 saatte ilk liste"], kind="desk"))

W.append(frame("SCR-W-02", "Şubeler ve hiyerarşi", "UC-01, UC-02",
    desk("Şubeler",
        top("Şubeler", "25 şube · 3 bölge") +
        '<div class="three" style="grid-template-columns:240px 1fr 280px"><div class="col"><div class="h">Hiyerarşi' + n(1) + '</div>' + li("Kahve Durağı") + li("— Anadolu (12)") + li("—— Kadıköy", "●", "", "ok") + li("—— Üsküdar") + li("— Avrupa (9)") + li("— Ege (4)") + '</div>' +
        '<div class="col"><div class="h">Kadıköy · KDK</div>' + field("Adres / konum", "… · 40.99, 29.02") + field("Saat dilimi", "Europe/Istanbul") + field("Çalışma saatleri" + n(2), "Pzt–Cmt 09:00–24:00 · Paz 10:00–22:00") + field("Kapalı günler", "1 Oca, 29 Eki + şube: 15 Eyl (envanter)") + field("Şube türü", "cadde") + '<div class="h">İstasyonlar' + n(3) + '</div>' + li("Bar · QR") + li("Mutfak · QR") + li("Kasa · QR") + li("Tuvalet · QR") + '</div>' +
        '<div class="col"><div class="h">Cihazlar' + n(4) + '</div>' + li("Samsung Tab A9 · kiosk", "●", "21:58", "ok") + li("Ayşe K. telefonu", "", "aktif") + btn("Cihaz ekle (QR)", "p") + '<div class="h">İçe aktar</div>' + btn("Excel yükle") + '</div></div>'),
    ["FR-0102 dört seviyeli hiyerarşi", "FR-0103/0507 çalışma saatleri → pencere türetme; FR-0515 kapalı gün takvimi", "FR-0104 istasyon ve QR", "FR-0207 kiosk kaydı QR ile"], kind="desk"))

W.append(frame("SCR-W-03", "Personel ve roller", "UC-02",
    desk("Personel",
        top("Personel", "412 kişi · 18 davet bekliyor") +
        '<div class="row">' + field("Ara", "ad / telefon") + field("Şube", "Kadıköy ▾") + field("Rol", "Tümü ▾") + field("Durum", "Aktif ▾") + '<div class="grow"></div>' + btn("Excel yükle") + btn("Personel ekle", "p") + '</div>' +
        '<table class="wt"><tr><th>Ad</th><th>Telefon</th><th>Şube</th><th>Rol · kapsam' + n(1) + '</th><th>Davet' + n(2) + '</th><th>Durum</th><th></th></tr>' +
        '<tr><td>Emre T.</td><td>+90 5…</td><td>Kadıköy</td><td>Personel · Bar</td><td><span class="chip ok">girdi</span></td><td>aktif</td><td>…</td></tr>' +
        '<tr><td>Murat D.</td><td>+90 5…</td><td>—</td><td>Bölge müdürü · Anadolu</td><td><span class="chip ok">girdi</span></td><td>aktif</td><td>…</td></tr>' +
        '<tr><td>Zeynep A.</td><td>+90 5…</td><td>Kadıköy</td><td>Personel · Mutfak</td><td><span class="chip w">iletilemedi · tekrar gönder</span></td><td>davet</td><td>…</td></tr>' +
        '<tr><td>Eski personel #4821' + n(3) + '</td><td>—</td><td>Kadıköy</td><td>—</td><td>—</td><td>maskeli</td><td></td></tr></table>' +
        '<div class="row"><div class="box grow"><div class="h">Akıllı gruplar' + n(4) + '</div><div class="s">"Anadolu mutfak personeli" = rol Personel ∧ bölge Anadolu ∧ istasyon Mutfak → 46 üye (canlı)</div></div><div class="box grow"><div class="h">Yan panel</div><div class="s">Rol ve kapsam düzenle · Pasifleştir · Kimliği maskele · Oturumları sonlandır</div></div></div>'),
    ["FR-0205 rol × kapsam", "FR-0108 davet SMS teslim durumu", "FR-0109/0110 pasifleştirme ve maskeleme (BR-22)", "FR-0206 dinamik gruplar"], kind="desk"))

W.append(frame("SCR-W-05", "Şablon editörü", "UC-05",
    desk("Şablonlar",
        top("Kapanış — kafe · v2 (taslak)", "v1 yayında · 3 plan kullanıyor" + n(1)) +
        '<div class="three"><div class="col"><div class="h">Yapı</div>' + li("Bölüm 1 · Bar") + li("— Kahve makinesi temizlendi <span class=chip>foto</span>") + li("— Süt dolabı °C") + li("Bölüm 2 · Mutfak") + li("— Buzdolabı 2 °C <span class=chip x>kritik</span>", "●", "", "ok") + li("— Zemin yıkandı") + li("— Çöpler alındı <span class=chip>foto</span>") + btn("+ Madde") + btn("+ Bölüm", "g") + '</div>' +
        '<div class="col"><div class="h">Madde ayarları' + n(2) + '</div>' + field("Tür", "Sıcaklık (°C)") + field("Kabul aralığı", "0 – 4") + '<div class="row">' + field("Zorunlu", "✓") + field("Kanıt zorunlu", "✓ foto") + field("Ağırlık", "3") + field("Kritik", "✓") + '</div>' + field("Yapılamadı izinli", "hayır (kritik)") + field("İstasyon", "Mutfak") + '<div class="h">Koşullu mantık' + n(3) + '</div>' + field("Eğer", "değer aralık dışı") + field("Yap", "fotoğraf iste · not iste · aksiyon oluştur (şube müdürü, kritik) · bildir (kalite)") + '<div class="h">Puanlama' + n(4) + '</div>' + field("Eşik", "%90 · kritik kuralı açık") + '</div>' +
        '<div class="col"><div class="h">Mobil önizleme' + n(5) + '</div><div class="img" style="flex-grow:1">390×… gerçek bileşenler</div><div class="row">' + btn("Doğrula") + btn("Yayınla ▾", "p") + '</div><div class="s" style="font-size:11px">Yayınla: hemen / tarihli · etkilenen planlar listelenir</div></div></div>'),
    ["FR-0301/0310 sürümleme ve yayın; BR-18", "FR-0304/0305 madde ayarları, kabul aralığı", "FR-0401/0402 kural ve eylemler", "FR-0306/0307 puan ve kritik", "FR-0309 önizleme; FR-0312 yayın doğrulaması"], kind="desk"))

W.append(frame("SCR-W-06", "Plan editörü", "UC-06",
    desk("Planlar",
        top("Plan · Kapanış (tüm şubeler)", "Şablon: Kapanış — kafe v1") +
        '<div class="three" style="grid-template-columns:1fr 1fr 320px"><div class="col"><div class="h">Kapsam' + n(1) + '</div>' + field("Şubeler", "Tümü (25) · grup: — ") + '<div class="h">Tekrar' + n(2) + '</div>' + field("Sıklık", "Her gün") + field("Pencere", "22:00 → 01:30 (+1 gün) · tolerans 120 dk") + field("Çalışma saatinden türet", "kapanış −120 / +90 dk ✓") + field("Bitiş", "—") + '</div>' +
        '<div class="col"><div class="h">Atama' + n(3) + '</div>' + field("Kime", "Rol: Kapanış sorumlusu") + field("Tamamlama", "Biri tamamlasın") + '<div class="h">Hatırlatma</div>' + field("Zamanlar", "açılışta · bitişe 30 dk · bitişte") + field("Kanal", "push · kritik listede SMS") + '<div class="h">Eskalasyon' + n(4) + '</div>' + field("Merdiven", "0: şube müdürü · +2 sa bölge (SMS) · +24 sa merkez") + '</div>' +
        '<div class="col"><div class="h">7 gün önizleme' + n(5) + '</div><div class="gridcells" style="grid-template-columns:repeat(7,1fr)">' + "".join('<div class="cell" style="background:#dcebe5"></div>' for _ in range(21)) + '<div class="cell" style="background:#c9ced6"></div>' + "".join('<div class="cell" style="background:#dcebe5"></div>' for _ in range(6)) + '</div><div class="s" style="font-size:11px">25 şube × 7 gün = 173 çalıştırma (2 kapalı gün düşüldü)</div><div class="row">' + btn("İptal", "g") + btn("Kaydet", "p") + '</div></div></div>'),
    ["FR-0502 kapsam", "FR-0503…0507 RRULE, pencere, gece yarısı (BR-01), tolerans (BR-02)", "FR-0508 atama modeli (BR-16)", "FR-0510 merdiven (BR-11)", "FR-0511 önizleme, FR-0515 kapalı gün"], kind="desk"))

cells = []
import random
random.seed(7)
for r in range(6):
    for c in range(5):
        cells.append(random.choice(["#1f6f5b"]*7 + ["#b7791f", "#b8452f", "#c9ced6", "#dcebe5"]))
W.append(frame("SCR-W-07", "Operasyon panosu (ızgara)", "UC-15, UC-19",
    desk("Pano",
        top("Pano · 12 Eylül (dün gece)", "◀ gün ▶ · Bölge: Tümü ▾ · Şube türü ▾ · canlı ●" + n(1)) +
        '<div class="kpi"><div><b>22/25</b><span>zamanında</span></div><div><b>1</b><span>geç</span></div><div><b>1</b><span>kaçırıldı</span></div><div><b>3</b><span>açık kritik aksiyon</span></div></div>' +
        '<table class="wt"><tr><th>Şube</th><th>Kapanış</th><th>Saatlik hijyen</th><th>Soğuk zincir</th><th>Açılış</th><th>Haftalık</th></tr>' +
        "".join(f'<tr><td>{s}</td>' + "".join(f'<td><div style="height:22px;border-radius:4px;background:{cells[i*5+j]}"></div></td>' for j in range(5)) + '</tr>' for i, s in enumerate(["Kadıköy", "Üsküdar", "Bakırköy", "Beşiktaş", "Bornova", "Karşıyaka"])) + '</table>' +
        '<div class="row" style="font-size:11px;color:var(--mut)"><span>■ tamamlandı</span><span>■ geç</span><span>■ kaçırıldı</span><span>■ kapalı</span><span>■ planlı/devam</span>' + n(2) + '<div class="grow"></div><span>Hücreye tıkla → çalıştırma detayı' + n(3) + '</span></div>' +
        '<div class="box"><div class="h">Bakırköy · Kapanış · kaçırıldı</div><div class="s">Eskalasyon: 03:30 şube müdürü ✓ · 05:30 bölge (SMS) ✓ · 03:30+24 sa merkez · [Yapılmayacak işaretle' + n(4) + '] [Aksiyon oluştur]</div></div>'),
    ["FR-1201 gün seçici, filtreler, 60 sn yenileme", "Durum lejantı (FR-0514); renk + ikon", "FR-1202 detay", "BR-04 yapılmayacak (yönetici + sebep) eskalasyonu durdurur"], kind="desk"))

W.append(frame("SCR-W-08", "Çalıştırma detayı", "UC-15, UC-16, UC-17",
    desk("Pano",
        top("Kadıköy · Kapanış · 12 Eyl · Tamamlandı 23:41 · <span class='chip x'>başarısız %88</span>", "[PDF" + n(1) + "] [Denetim izi] [Ek kayıt]") +
        '<div class="three" style="grid-template-columns:1fr 360px 260px"><div class="col"><div class="h">Maddeler</div>' + li("Kahve makinesi temizlendi", "✓", "23:02 · Emre T. · foto", "ok") + li("Süt dolabı °C · 3,2", "✓", "23:05", "ok") + li("Buzdolabı 2 °C · 6,0 <span class=chip x>kritik</span>", "!", "23:20 · aksiyon #418", "x") + li("Zemin yıkandı · yapılamadı: malzeme yok", "✗", "23:30 · aksiyon #419", "w") + li("Çöpler alındı", "✓", "23:38 · foto", "ok") + '</div>' +
        '<div class="col"><div class="h">Kanıt' + n(2) + '</div><div class="img" style="height:150px">damgalı fotoğraf · Kadıköy · 12.09 23:02 · Emre T.</div><div class="s" style="font-size:11px">sha256 7f3a… · konum 38 m · cihaz: şube tableti · saat farkı 0 sn · [ham dosya]</div><div class="h">Aksiyonlar</div>' + li("#418 kritik · devam · vade 03:41") + li("#419 orta · açık · vade 3 gün") + '</div>' +
        '<div class="col"><div class="h">Olay izi' + n(3) + '</div><div class="s" style="font-size:11px">22:00 pencere açıldı (sistem)<br>22:58 Emre T. başladı (tablet)<br>23:20 madde 8 aralık dışı → aksiyon #418<br>23:41 gönderildi · puan 88<br>23:41 kritik kural → başarısız<br>23:41 bildirim: Ayşe K. push ✓</div><div class="h">Gözden geçirme' + n(4) + '</div><div class="s">[Gözden geçirildi] not · ikinci imza</div></div></div>'),
    ["FR-1213 markalı PDF + doğrulama kodu", "FR-0606 damga ve meta; FR-1208 galeri", "FR-1301/1303 olay izi", "FR-1701/1702 gözden geçirme ve imza (Should)"], kind="desk"))

W.append(frame("SCR-W-09", "Aksiyonlar", "UC-12, UC-13",
    desk("Aksiyonlar",
        top("Aksiyonlar", "Açık 37 · Gecikmiş 6 · Kritik 3") +
        '<div class="row">' + field("Görünüm", "Bölgem ▾") + field("Durum", "Açık ▾") + field("Öncelik", "Tümü ▾") + field("Şube", "Tümü ▾") + '<div class="grow"></div>' + btn("Aksiyon oluştur", "p") + '</div>' +
        '<table class="wt"><tr><th>#</th><th>Başlık</th><th>Kaynak' + n(1) + '</th><th>Şube</th><th>Atanan</th><th>Öncelik</th><th>Vade</th><th>Durum</th></tr>' +
        '<tr><td>418</td><td>Buzdolabı 2 aralık dışı</td><td>madde</td><td>Kadıköy</td><td>Ayşe K.</td><td><span class="chip x">kritik</span></td><td>03:41</td><td>devam</td></tr>' +
        '<tr><td>417</td><td>Kapanış kaçırıldı</td><td>kaçırma</td><td>Bakırköy</td><td>Bölge: Murat D.</td><td><span class="chip x">kritik</span></td><td>gecikti 2 sa</td><td>açık</td></tr>' +
        '<tr><td>412</td><td>Fritöz termostatı</td><td>sorun</td><td>Kadıköy</td><td>Ayşe K.</td><td><span class="chip w">yüksek</span></td><td>yarın 10:00</td><td>kapatma bekliyor' + n(2) + '</td></tr></table>' +
        '<div class="row"><div class="box grow"><div class="h">#417 · eskalasyon adımları' + n(3) + '</div><div class="s">0 · 03:30 şube müdürü push ✓ okundu 07:12 · 1 · 05:30 bölge push+SMS ✓ · 2 · 03:30+24 sa merkez (planlı)</div></div><div class="box grow"><div class="h">Geçişler' + n(4) + '</div><div class="s">açık → devam → kapatma bekliyor → kapalı · reddedildi (sebep) · kapatırken foto/not zorunlu</div></div></div>'),
    ["FR-0901/0902 kaynak türleri, otomatik oluşturma", "FR-0904/0909 durum akışı, onaylı kapanış", "FR-0912/0913 merdiven ve log (BR-11)", "FR-0905 kapanış kanıtı"], kind="desk"))

W.append(frame("SCR-W-11", "Raporlar", "UC-15, UC-16",
    desk("Raporlar",
        top("Raporlar", "Tamamlanma · Başarısız maddeler · Sebepler · Ölçüm günlüğü · Kanıt galerisi · Aksiyonlar · Kişi takibi" + n(1)) +
        '<div class="row">' + field("Dönem", "1–12 Eyl") + field("Bölge", "Tümü") + field("Şablon", "Kapanış") + '<div class="grow"></div>' + btn("Excel") + btn("Dönem PDF" + n(2), "p") + '</div>' +
        '<div class="kpi"><div><b>%91</b><span>pencere içi</span></div><div><b>%5</b><span>geç</span></div><div><b>%3</b><span>kaçırıldı</span></div><div><b>%1</b><span>yapılmayacak</span></div></div>' +
        '<div class="row"><div class="img grow" style="height:170px">trend çizgisi · şube sıralaması (şube düzeyi' + n(3) + ')</div><div class="img grow" style="height:170px">şube × madde ısı haritası · en çok başarısız 10 madde</div></div>' +
        '<div class="box"><div class="h">Ölçüm günlüğü · Kadıköy · Buzdolabı 2 · 30 gün' + n(4) + '</div><div class="s">zaman serisi; aralık dışı 2 ölçüm işaretli; denetim formatında PDF (sayfa damgası, doğrulama kodu)</div></div>' +
        '<div class="box"><div class="h">Kişi takibi (yalnızca şube/bölge müdürü)' + n(5) + '</div><div class="s">Emre T.: 1 eksik madde, 0 gecikmiş aksiyon · puan/sıralama yok</div></div>'),
    ["FR-1203…1209 rapor sekmeleri", "FR-1214/1215/1216 dışa aktarım ve paylaşım; FR-1217 arka plan üretim", "FR-1204 sıralama şube/bölge düzeyinde (BR-20)", "FR-1207 ölçüm günlüğü", "FR-1210 kişi düzeyi takip — skor yok"], kind="desk"))

W.append(frame("SCR-W-12 · SCR-W-13", "Denetim izi ve Ayarlar", "UC-17, UC-18",
    desk("Ayarlar",
        '<div class="three" style="grid-template-columns:1fr 1fr"><div class="col"><div class="h">Denetim izi' + n(1) + '</div>' + field("Filtre", "nesne: çalıştırma #9021 · 12 Eyl") + '<table class="wt"><tr><th>Zaman</th><th>Aktör</th><th>Olay</th><th>Cihaz/IP</th></tr><tr><td>23:20:14</td><td>Emre T.</td><td>madde 8 cevap 6,0 (aralık dışı)</td><td>tablet KDK-1</td></tr><tr><td>23:41:02</td><td>Emre T.</td><td>gönderim · puan 88 · başarısız</td><td>tablet KDK-1</td></tr><tr><td>07:12:40</td><td>Ayşe K.</td><td>aksiyon #418 devam</td><td>iOS · 88.x</td></tr></table><div class="box"><div class="h">Zincir doğrulama' + n(2) + '</div><div class="s">12 Eyl: 18.204 olay · zincir tutarlı ✓ · günlük kök a91c… · RFC 3161 damgası 04:00 ✓</div></div></div>' +
        '<div class="col"><div class="h">Ayarlar' + n(3) + '</div>' + li("Hesap ve marka (logo, renk)") + li("Bildirim varsayılanları · sessiz saatler 23–07") + li("Eskalasyon şablonları") + li("Sebep ve kategori setleri") + li("Tatil takvimi") + li("Saklama süresi: 24 ay" + n(4)) + li("KVKK talepleri · aydınlatma metni v3") + li("Faturalama sayacı: 25 aktif şube") + li("API ve webhook (Should)") + '</div></div>'),
    ["FR-1303 denetim izi görüntüleyici", "FR-1302/1304 kök özeti ve doğrulama", "FR-1402 hesap ayarları (BR parametre tablosu)", "FR-1311 saklama; FR-1309/1310 KVKK talepleri"], kind="desk"))

def page(title, sub, frames, kind):
    legend = ('<div class="legend"><span><b style="background:#1f6f5b"></b>tamamlandı / birincil eylem</span><span><b style="background:#b7791f"></b>geç / uyarı</span>'
              '<span><b style="background:#b8452f"></b>kaçırıldı / kritik</span><span><b style="background:#c9ced6"></b>kapalı / pasif</span><span>Numaralı daireler → çerçeve altındaki FR notları</span></div>')
    return (f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>{CSS}</head>'
            f'<body><div class="wrap"><h1>{title}</h1><p class="sub">{sub}</p>{legend}<div class="grid {kind}">{"".join(frames)}</div></div></body></html>')

open(os.path.join(OUT, "02-mobil-ekranlar.html"), "w", encoding="utf-8").write(page(
    "Talimatname · Mobil tel-çerçeveler",
    "Düşük doğruluklu tel-çerçeveler: yapı, akış ve gereksinim bağları. Görsel dil için 04-tasarim-sistemi.md; yüksek doğruluklu tasarım F8'de. Telefon çerçevesi 390×780; kiosk ekranı tablet yatay. Sahte durum çubuğu ve klavye çizilmez.",
    M, "mobile"))
open(os.path.join(OUT, "03-web-ekranlar.html"), "w", encoding="utf-8").write(page(
    "Talimatname · Web tel-çerçeveler",
    "Yönetim paneli tel-çerçeveleri (1200 px). Sol menü rol kapsamına göre daralır. Her çerçevenin altındaki numaralı notlar fonksiyonel gereksinimlere (FR) bağlanır.",
    W, "web"))
print("yazıldı: 02-mobil-ekranlar.html (%d çerçeve), 03-web-ekranlar.html (%d çerçeve)" % (len(M), len(W)))
