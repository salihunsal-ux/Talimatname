# -*- coding: utf-8 -*-
p='build_index.py'; s=open(p,encoding='utf-8').read()
old = """        (D+"02-urun/06-v1-cekirdek-kapsam.md", "v1 çekirdek kapsamı", "Kapsamın tek kaynağı: sabitler tablosu ve M1–M9 satırları (v1 / v1.1 / v2)", ["kaynak"]),
    ]),"""
new = """        (D+"02-urun/06-v1-cekirdek-kapsam.md", "v1 çekirdek kapsamı", "Kapsamın tek kaynağı: sabitler tablosu ve M1–M9 satırları (v1 / v1.1 / v2)", ["kaynak"]),
        (D+"02-urun/07-sablon-kutuphanesi.md", "Şablon kütüphanesi (8 şablon)", "Kapanış, açılış, saatlik hijyen, soğuk zincir, haftalık temizlik, yağ, kasa devri, teslimat kabul — madde madde; taslak, sahada doğrulanır", ["kit", "taslak"]),
    ]),"""
assert old in s; s = s.replace(old, new)
old2 = """        (D+"05-tasarim/05-prototip/README.md", "Prototip kullanım notu", "Görüşmede nasıl kullanılır, hangi akışlar gösterilir", []),"""
new2 = """        (D+"05-tasarim/05-prototip/README.md", "Prototip kullanım notu", "Görüşmede nasıl kullanılır, hangi akışlar gösterilir", []),
        (D+"05-tasarim/06-kanit-raporu/README.md", "Kanıt raporu örnekleri — not", "Üç basılı örnek: ne gösterir, hangi kapsam satırına bağlı, nasıl üretilir", ["kit"]),
        (D+"05-tasarim/06-kanit-raporu/01-calistirma-raporu.html", "Çalıştırma raporu (örnek PDF)", "Kadıköy kapanışı 13 Eylül: başarısız (kritik), 15 madde, damgalı fotoğraflar, aksiyonlar, olay izi, doğrulama kodu — 2 sayfa", ["kit", "basılı"]),
        (D+"05-tasarim/06-kanit-raporu/02-aylik-ozet.html", "Aylık özet (örnek PDF)", "Ağustos 2026, 25 şube: zamanında %81, kırılımlar, en sık yapılamayanlar, kritik kaynakları — 1 sayfa", ["kit", "basılı"]),
        (D+"05-tasarim/06-kanit-raporu/03-sicaklik-gunlugu.html", "Sıcaklık günlüğü (örnek PDF)", "Kadıköy 1–14 Eylül, 4 ekipman × 3 ölçüm/gün, aralık dışı işaretli, mini grafik — 1 sayfa", ["kit", "basılı"]),
        (D+"05-tasarim/06-kanit-raporu/01-calistirma-raporu.pdf", "Çalıştırma raporu — PDF dosyası", "Yazdırmaya hazır A4, 2 sayfa", ["basılı"]),
        (D+"05-tasarim/06-kanit-raporu/02-aylik-ozet.pdf", "Aylık özet — PDF dosyası", "Yazdırmaya hazır A4, 1 sayfa", ["basılı"]),
        (D+"05-tasarim/06-kanit-raporu/03-sicaklik-gunlugu.pdf", "Sıcaklık günlüğü — PDF dosyası", "Yazdırmaya hazır A4, 1 sayfa", ["basılı"]),
        (D+"05-tasarim/06-kanit-raporu/build_reports.py", "Rapor üretici (build_reports.py)", "Üç örneği ve PDF'lerini üretir (Edge headless)", ["betik"]),"""
assert old2 in s; s = s.replace(old2, new2)
# 'link' türü: yerel dosya bağlantısı da göster
old3 = """      body.innerHTML = '<p>Bu dosya sayfaya gömülmez. <a href="' + esc(e.gh) + '" target="_blank" rel="noopener">GitHub\'da aç ↗</a> veya depodaki yol: <code>' + esc(p) + '</code></p>';"""
new3 = """      body.innerHTML = '<p>Bu dosya sayfaya gömülmez. <a class="btn" href="' + esc(p) + '" target="_blank" rel="noopener">Dosyayı aç ↗</a> <a class="btn" href="' + esc(e.gh) + '" target="_blank" rel="noopener">GitHub\'da aç ↗</a></p><p class="mut small">Depodaki yol: <code>' + esc(p) + '</code></p>';"""
assert old3 in s; s = s.replace(old3, new3)
open(p,'w',encoding='utf-8').write(s); print('registry patched')
