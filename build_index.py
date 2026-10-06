# -*- coding: utf-8 -*-
"""Ürün dosyası üretici → index.html

docs/ altındaki Markdown belgeleri HTML'e çevirip tek dosyaya gömer; HTML teslimatları (fizibilite, ekranlar,
prototip, marka) göreli yolla çerçevede açar; ürün merkezi, çalışma planı, sprint planı ve gorusmeler/00-ozet.md'den
fazları, karar haritasını, açık kararları, kapı sayaçlarını ve izlenebilirlik sayılarını okur. Böylece sayfa
belgelerle birlikte güncel kalır.

Çalıştır (depo kökünde):  python build_index.py
Bağımlılık: pip install markdown
"""
import os, re, sys, json, html, posixpath, datetime, subprocess
import markdown
from markdown.extensions.toc import slugify_unicode

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "index.html")
GH = "https://github.com/salihunsal-ux/Talimatname"
GH_BLOB = GH + "/blob/main/"
GH_TREE = GH + "/tree/main/"

# Canlı sayfalar (claude.ai artifact)
LIVE = {
    "docs/01-strateji/01-fizibilite.html": "https://claude.ai/code/artifact/7624c049-c18f-45d6-b7c5-c750bcd7798f",
    "docs/02-urun/03-mvp-kapsam.html": "https://claude.ai/code/artifact/c7feaa95-847e-473e-bd87-8f95646bb515",
    "docs/01-strateji/02-pilot-gorusme-rehberi.html": "https://claude.ai/code/artifact/7dda6bc8-bf82-4c28-a572-b6572652e421",
    "docs/05-tasarim/marka/Main.dc.html": "https://claude.ai/code/artifact/96cf8183-a732-4988-acd2-731b83545950",
    "docs/05-tasarim/05-prototip/blok8-prototip.html": "https://claude.ai/code/artifact/229e7396-313c-487b-9a31-ada9caa05e69",
    "docs/05-tasarim/05-prototip/yonetici-web-prototip.html": "https://claude.ai/code/artifact/96276ca2-4d59-49b2-8bb2-50ec77e394f5",
    "docs/05-tasarim/05-prototip/saha-demosu.html": "https://claude.ai/artifact/WGKqPtVDturkaRaoLRtiRy",
    "docs/05-tasarim/07-brosur/talimatname-brosur.html": "https://claude.ai/artifact/3LpwvVXZczJMNLqnKrBVn2",
    "docs/05-tasarim/07-brosur/talimatname-tanitim.html": "https://claude.ai/artifact/NDJqDvhikUbqqgtFNTZpQk",
    "docs/05-tasarim/07-brosur/talimatname-ozellikler.html": "https://claude.ai/artifact/JDHxYmF8ZnShvi78khafDD",
}

# (yol, başlık, açıklama, etiketler) — tür uzantıdan: .md gömülü, .py/.txt kod, .html çerçeve, diğer bağlantı
D = "docs/"
REGISTRY = [
    ("Başlangıç", [
        ("README.md", "Depo haritası", "Depo yapısı, güncel ürün kararları, çalışma kuralları, geliştirici hızlı başlangıcı", []),
        (D+"00-urun-merkezi.md", "Ürün merkezi", "Tek sayfalık özet, karar haritası, açık kararlar, belge navigasyonu, kimlik şeması", ["kaynak"]),
        (D+"00-calisma-plani.md", "Çalışma planı", "İş analizi ve ürün sahipliği fazları F0–F9, teslimatlar, durum, çalışma kuralları", []),
    ]),
    ("01 Strateji", [
        (D+"01-strateji/01-fizibilite.html", "Fizibilite raporu", "Pazar ve rakipler, 60 aylık finansal model, dört senaryo, duyarlılık, risk, karar: Koşullu GO", ["canlı sayfa"]),
        (D+"01-strateji/fizibilite-modeli/model.py", "Fizibilite modeli (model.py)", "Finansal modelin kaynak kodu: senaryolar, aylık simülasyon, birim ekonomi, DCF, beklenen değer", ["betik"]),
        (D+"01-strateji/fizibilite-modeli/model_output.txt", "Model çıktısı", "Senaryo özetleri, TAM/SAM, duyarlılık tabloları (ham çıktı)", []),
        (D+"01-strateji/fizibilite-modeli/build_report.py", "Rapor üretici (build_report.py)", "results.json → fizibilite raporu HTML", ["betik"]),
        (D+"01-strateji/fizibilite-modeli/results.json", "Model sonuçları (results.json)", "Modelin ham sonuç dosyası", []),
        (D+"01-strateji/02-pilot-gorusme-rehberi.html", "Pilot görüşme rehberi", "Görüşme soru blokları, örneklem karışımı, isim ve fiyat testi, gözlem listesi, puanlama rubriği", ["canlı sayfa"]),
        (D+"01-strateji/04-buyume-firsatlari.md", "Büyüme fırsatları ve boşluklar", "Park listesi: ARPU artıran modüller (sensör, denetim formu, franchise kütüphanesi…), yeni segmentler, gelir kalemleri, kanallar, rakiplere göre boşluklar; K/R/E puanı ve tetikleyici sinyaller", ["park"]),
        (D+"01-strateji/03-isim-ve-marka.md", "İsim ve marka", "Aday isimler, alan adı sorguları (RDAP/TRABIS), marka sistemi, bekleyen işler", []),
        (D+"01-strateji/dogrulama-sprinti/00-sprint-plani.md", "Doğrulama sprinti planı", "12 hafta; K1/K2/K3 kapıları, haftalık plan ve ritim, örneklem dengesi, roller, riskler, bütçe", ["kit"]),
        (D+"01-strateji/dogrulama-sprinti/01-hedef-liste.md", "Hedef zincir listesi", "23 birincil aday (5–100 şube) + ikinci dalga (100+); kutu/format/model etiketli; kişi bilgisi yok", ["kit"]),
        (D+"01-strateji/dogrulama-sprinti/02-ulasim-kiti.md", "Ulaşım kiti", "Kanal sırası ve T1–T7 mesaj şablonları (tanıştırma, LinkedIn, ana mesaj, takip, teyit, teşekkür)", ["kit"]),
        (D+"01-strateji/dogrulama-sprinti/03-gorusme-not-sablonu.md", "Görüşme not şablonu", "Makine-okur YAML başlık: rubrik 16 puan, fiyat 4 soru, isim kartı, kapsam sinyalleri, kötü sinyaller", ["kit"]),
        (D+"01-strateji/dogrulama-sprinti/puanla.py", "Puanlama betiği (puanla.py)", "Notlardan kapı sayacı, pilot adayları, örneklem dengesi, isim testi, van Westendorp → gorusmeler/00-ozet.md", ["betik", "kit"]),
        (D+"01-strateji/dogrulama-sprinti/04-loi-sablonu.md", "Pilot niyet mektubu (LOI)", "8 haftalık ücretli pilot; başarı ölçütleri; yalnızca gizlilik maddesi bağlayıcı; görüşmeci kontrol listesi", ["kit"]),
        (D+"01-strateji/dogrulama-sprinti/05-gozlem-formu.md", "Şube ziyareti gözlem formu", "Kapanış vardiyası: fiziksel ortam, davranış, personel sohbeti, merkez–saha farkı", ["kit"]),
        (D+"01-strateji/dogrulama-sprinti/06-haftalik-rapor-sablonu.md", "Haftalık rapor şablonu", "Cuma raporu: sayılar, sinyaller, kapsam kararlarına etki; 4. ve 8. hafta kapı bölümü", ["kit"]),
        (D+"01-strateji/dogrulama-sprinti/07-kiosk-saha-denemesi.md", "Saha kiosk denemesi", "Gerçek tablet + kilit modu + prototip ile kapanış: ölçütler, karar kuralı, donanım, kurulum, ziyaret akışı, not şablonu", ["kit"]),
        (D+"01-strateji/gorusmeler/README.md", "Görüşme notları — akış", "Görüşme → 10 dk not → puanla.py → commit; dosya adlandırma", []),
        (D+"01-strateji/gorusmeler/00-ozet.md", "Görüşme özeti ve kapı sayacı", "puanla.py çıktısı (otomatik): K1/K2, pilot adayları, örneklem, isim testi, fiyat", ["otomatik"]),
        (D+"01-strateji/gorusmeler/ornek-gorusme.md", "Örnek görüşme notu", "Doldurulmuş örnek (ornek: true — puanlamaya girmez)", []),
    ]),
    ("02 Ürün", [
        (D+"02-urun/01-urun-vizyonu-ve-konumlanma.md", "Vizyon ve konumlanma", "Sorun, çözüm, hedef müşteri, konumlanma cümlesi, neden şimdi, değer kanıtı, başarı ölçütleri", []),
        (D+"02-urun/02-personalar.md", "Personalar", "Selin, Murat, Ayşe, Emre, Deniz, Cem — cihaz, sıklık, acı, ürün için anlamı", []),
        (D+"02-urun/03-mvp-kapsam.html", "İlk MVP kapsamı (tarihsel)", "Rakip iyi özellikleriyle ilk kapsam raporu; ADR-0008 sonrası tarihsel referans", ["canlı sayfa", "tarihsel"]),
        (D+"02-urun/04-yetenek-haritasi.md", "Yetenek haritası", "CAP-01…19 yetenekler, v1/v1.1 sürümleri, aktör ve UC bağları", []),
        (D+"02-urun/05-v1-cekirdek-gozden-gecirme.md", "v1 çekirdek — aktör gözüyle gözden geçirme", "Altı aktörün gözüyle inceleme; K1–K21 kesinti, E1–E7 ekleme; sıra ilkesi", []),
        (D+"02-urun/06-v1-cekirdek-kapsam.md", "v1 çekirdek kapsamı", "Kapsamın tek kaynağı: sabitler tablosu ve M1–M9 satırları (v1 / v1.1 / v2)", ["kaynak"]),
        (D+"02-urun/08-madde-kutuphanesi.md", "Madde kütüphanesi ve paketler (v1.1)", "Kavramlar, Selin'in akışları, içerik planı (200–300 madde, 4 paket), kaynak takibi ve güncelleme bandı, aşamalar, FR-0313…0318", ["v1.1"]),
        (D+"02-urun/07-sablon-kutuphanesi.md", "Şablon kütüphanesi (8 şablon)", "Kapanış, açılış, saatlik hijyen, soğuk zincir, haftalık temizlik, yağ, kasa devri, teslimat kabul — madde madde; taslak, sahada doğrulanır", ["kit", "taslak"]),
    ]),
    ("03 Analiz", [
        (D+"03-analiz/01-aktorler.md", "Aktörler", "A-01…14 aktörler, sorumluluklar; v1'de dört rol", []),
        (D+"03-analiz/02-usecase-katalogu.md", "Use case kataloğu", "UC-01…20, aktör–UC diyagramı, sürüm sütunu", []),
        (D+"03-analiz/03-usecase-detaylari.md", "Use case detayları", "Her UC için ön koşul, ana akış, alternatifler, son koşul, v1 notu", []),
        (D+"03-analiz/04-senaryolar.md", "Uçtan uca senaryolar", "S-01…08: Kahve Durağı zincirinde gerçek gün akışları", []),
    ]),
    ("04 Gereksinimler", [
        (D+"04-gereksinimler/01-fonksiyonel-gereksinimler.md", "Fonksiyonel gereksinimler", "FR-0101…1803; her satır UC'ye bağlı, sürüm bayraklı (v1 / v1.1)", []),
        (D+"04-gereksinimler/02-fonksiyonel-olmayan.md", "Fonksiyonel olmayan gereksinimler", "NFR-01…16: performans, çevrimdışı, güvenlik, erişilebilirlik, işletim", []),
        (D+"04-gereksinimler/03-is-kurallari.md", "İş kuralları", "BR-01…27 ve v1 sabit parametre tablosu (tolerans, vade, sessiz saat, saklama)", []),
        (D+"04-gereksinimler/04-veri-modeli.md", "Veri modeli", "ER diyagramı, tablolar ve alanlar, v1 enum notu", []),
        (D+"04-gereksinimler/05-api-taslagi.md", "API taslağı", "REST uç noktaları, kimlik, senk, kanıt yükleme, v1.1 işaretleri", []),
        (D+"04-gereksinimler/06-kvkk-ve-guvenlik.md", "KVKK ve güvenlik", "Roller (sorumlu/işleyen), aydınlatma, saklama, biyometri yok, güvenlik kontrolleri", []),
        (D+"04-gereksinimler/hukuki/README.md", "Hukuki metinler — durum ve avukata sorular", "Taslakların durumu, nerede kullanılacağı, sekiz avukat sorusu (m.9 push, hukuki sebep, maskeleme, kiosk onayı, VERBİS, saklama, ihlal süresi)", ["taslak"]),
        (D+"04-gereksinimler/hukuki/01-aydinlatma-metni-personel.md", "Personel aydınlatma metni (taslak)", "KVKK m.10 tam metin + uygulama içi kısa katman + konum, kamera ve kiosk ekran metinleri", ["taslak"]),
        (D+"04-gereksinimler/hukuki/02-veri-isleme-sozlesmesi.md", "Veri işleme sözleşmesi (taslak)", "Veri sorumlusu–veri işleyen sözleşmesi; Ek-1 işleme kapsamı, Ek-2 alt işleyenler, Ek-3 tedbirler", ["taslak"]),
    ]),
    ("05 Tasarım", [
        (D+"05-tasarim/01-ekran-envanteri-ve-navigasyon.md", "Ekran envanteri ve navigasyon", "SCR-M / SCR-W envanteri, navigasyon haritası, sürüm sütunu", []),
        (D+"05-tasarim/02-mobil-ekranlar.html", "Mobil tel-çerçeveler", "Personel ve yönetici mobil ekranları (v1)", []),
        (D+"05-tasarim/03-web-ekranlar.html", "Web tel-çerçeveler", "Yönetim paneli ekranları (v1)", []),
        (D+"05-tasarim/04-tasarim-sistemi.md", "Tasarım sistemi", "Renk, tipografi, boşluk, bileşen kuralları, erişilebilirlik (token'lar)", []),
        (D+"05-tasarim/ekranlar/build_wireframes.py", "Tel-çerçeve üretici (build_wireframes.py)", "02 ve 03 HTML dosyalarını üretir", ["betik"]),
        (D+"05-tasarim/05-prototip/blok8-prototip.html", "Blok 8 prototipi", "Tıklanabilir: kiosk PIN → kapanış listesi → sabah özeti; isim kartı seçici", ["canlı sayfa", "kit"]),
        (D+"05-tasarim/05-prototip/yonetici-web-prototip.html", "Yönetici web prototipi", "Kurulum sihirbazı (4 adım) → istisna odaklı pano ve ızgara → çalıştırma detayı ve aksiyon → sabah özeti e-postası; LOI turu için", ["kit", "canlı sayfa"]),
        (D+"05-tasarim/05-prototip/saha-demosu.html", "Saha demosu (çalışan)", "Veri saklayan demo: kiosk PIN → gerçek pencere ve tolerans → madde cevapları, cihaz kamerasıyla kanıt, yapılamadı ve aksiyon → gönderim ve kilit; merkez panosu aynı kaydı canlı görür, doğrulama kodlu rapor yazdırılır. Paylaşımlı mod yalnızca yazma yetkisi olan hesaplarda; diğerlerinde yerel mod", ["prototip", "canlı sayfa"]),
        (D+"05-tasarim/05-prototip/README.md", "Prototip kullanım notu", "İki prototip: Blok 8 (personel, telefon) ve yönetici web (LOI turu); ne gösterir, ne sorulur", []),
        (D+"05-tasarim/06-kanit-raporu/README.md", "Kanıt raporu örnekleri — not", "Üç basılı örnek: ne gösterir, hangi kapsam satırına bağlı, nasıl üretilir", ["kit"]),
        (D+"05-tasarim/06-kanit-raporu/01-calistirma-raporu.html", "Çalıştırma raporu (örnek PDF)", "Kadıköy kapanışı 13 Eylül: başarısız (kritik), 15 madde, damgalı fotoğraflar, aksiyonlar, olay izi, doğrulama kodu — 2 sayfa", ["kit", "basılı"]),
        (D+"05-tasarim/06-kanit-raporu/02-aylik-ozet.html", "Aylık özet (örnek PDF)", "Ağustos 2026, 25 şube: zamanında %81, kırılımlar, en sık yapılamayanlar, kritik kaynakları — 1 sayfa", ["kit", "basılı"]),
        (D+"05-tasarim/06-kanit-raporu/03-sicaklik-gunlugu.html", "Sıcaklık günlüğü (örnek PDF)", "Kadıköy 1–14 Eylül, 4 ekipman × 3 ölçüm/gün, aralık dışı işaretli, mini grafik — 1 sayfa", ["kit", "basılı"]),
        (D+"05-tasarim/06-kanit-raporu/01-calistirma-raporu.pdf", "Çalıştırma raporu — PDF dosyası", "Yazdırmaya hazır A4, 2 sayfa", ["basılı"]),
        (D+"05-tasarim/06-kanit-raporu/02-aylik-ozet.pdf", "Aylık özet — PDF dosyası", "Yazdırmaya hazır A4, 1 sayfa", ["basılı"]),
        (D+"05-tasarim/06-kanit-raporu/03-sicaklik-gunlugu.pdf", "Sıcaklık günlüğü — PDF dosyası", "Yazdırmaya hazır A4, 1 sayfa", ["basılı"]),
        (D+"05-tasarim/06-kanit-raporu/build_reports.py", "Rapor üretici (build_reports.py)", "Üç örneği ve PDF'lerini üretir (Edge headless)", ["betik"]),
        (D+"05-tasarim/07-brosur/README.md", "Broşür — kullanım notu", "Ne zaman verilir (Blok 8 sonrası, LOI turu), dosyalar, doldurulacak alanlar, fiyat neden yok", []),
        (D+"05-tasarim/07-brosur/talimatname-brosur.html", "Tanıtım broşürü (A4, 2 sayfa)", "İddia + kapanış ve sıcaklık ekranları + üç adım; merkez görünümü, neden Talimatname, 8 haftalık pilot, iletişim — canlı tuvalde düzenlenebilir", ["kit", "basılı", "canlı sayfa"]),
        (D+"05-tasarim/07-brosur/talimatname-brosur.pdf", "Broşür — PDF", "Yazdırmaya hazır A4, 2 sayfa", ["basılı"]),
        (D+"05-tasarim/07-brosur/talimatname-tanitim.html", "Tanıtım dosyası (A4, 8 sayfa)", "Anlatım belgesi: bir gecenin akışı, personel ve yönetici ekranları, kanıt zinciri ve KVKK, kurulum ve pilot, yol haritası", ["kit", "basılı", "canlı sayfa"]),
        (D+"05-tasarim/07-brosur/talimatname-tanitim.pdf", "Tanıtım dosyası — PDF", "Yazdırmaya hazır A4, 8 sayfa", ["basılı"]),
        (D+"05-tasarim/07-brosur/talimatname-ozellikler.html", "Özellik föyü (A4, 9 sayfa)", "Müşteri dili, satış sıralaması: bugünkü sürümün 11 özelliği gerçek ekranlarla (s.1–4), yol haritasının 11 satırı tasarım taslağı ekranlarıyla (s.5–9)", ["kit", "basılı", "canlı sayfa"]),
        (D+"05-tasarim/07-brosur/talimatname-ozellikler.pdf", "Özellik föyü — PDF", "Yazdırmaya hazır A4, 9 sayfa", ["basılı"]),
        (D+"05-tasarim/07-brosur/ozellikler/BelgeTakvimi.dc.html", "Ekran tasarımı: belge takvimi (web, SCR-W-14)", "Yaklaşan ve süresi geçen belgeler, belge kartı ve dosyası, otomatik aksiyon, dönem PDF'i", ["tasarım"]),
        (D+"05-tasarim/07-brosur/ozellikler/Bayraklar.dc.html", "Ekran tasarımı: kanıt bütünlüğü bayrakları (web)", "Aynı dosyanın reddi, konum/cihaz saati/galeri bayrakları, şüpheli kanıt filtresi", ["tasarım"]),
        (D+"05-tasarim/07-brosur/ozellikler/Sablonlar.dc.html", "Ekran tasarımı: şablonlar (web)", "Sekiz hazır şablon, sürüm ve kullanım bilgisi, altı madde türü ve işaretler", ["tasarım"]),
        (D+"05-tasarim/07-brosur/ozellikler/Cevrimdisi.dc.html", "Ekran tasarımı: çevrimdışı (mobil)", "Kuyrukta bekleyen kayıtlar, 72 saat, damga sunucu saatiyle", ["tasarım"]),
        (D+"05-tasarim/07-brosur/ozellikler/Kutuphane.dc.html", "Taslak: madde kütüphanesi (web)", "İşletme türü paketleri, kütüphaneden madde seçme, “güncelleme var” uyarısı", ["taslak"]),
        (D+"05-tasarim/07-brosur/ozellikler/Mutabakat.dc.html", "Taslak: üretim–satış mutabakatı (web)", "Üretilen/satılan tablosu, açıklanamayan fark, sebep seti, vardiya düzeyi", ["taslak"]),
        (D+"05-tasarim/07-brosur/ozellikler/BenzerKanit.dc.html", "Taslak: benzer kanıt uyarısı (web)", "İki yakın kare, benzerlik yüzdesi, incele/kabul et", ["taslak"]),
        (D+"05-tasarim/07-brosur/ozellikler/Duyuru.dc.html", "Taslak: duyuru ve okundu onayı (web)", "Duyuru kartı, ek dosya, şube bazında okundu/onay raporu", ["taslak"]),
        (D+"05-tasarim/07-brosur/ozellikler/KosulluMadde.dc.html", "Taslak: koşullu maddeler (web)", "Eğer/o zaman kuralları ve personel önizlemesi", ["taslak"]),
        (D+"05-tasarim/07-brosur/ozellikler/Raporlar.dc.html", "Taslak: ayrıntılı raporlar (web)", "Isı haritası (şube × madde), şube sıralaması, yapılamadı sebep dağılımı, Excel/paylaşım", ["taslak"]),
        (D+"05-tasarim/07-brosur/ozellikler/DenetimIzi.dc.html", "Taslak: denetim izi ekranı (web)", "Filtreli olay listesi, özet sütunu, zincir doğrulama ve zaman damgası", ["taslak"]),
        (D+"05-tasarim/07-brosur/ozellikler/Franchise.dc.html", "Taslak: franchise marka kütüphanesi (web)", "Yayınlanan standart sürümü ve franchise uyum tablosu", ["taslak"]),
        (D+"05-tasarim/07-brosur/ozellikler/SektorPaketleri.dc.html", "Taslak: sektör paketleri (web)", "Perakende, otel, akaryakıt, üretim paketleri", ["taslak"]),
        (D+"05-tasarim/07-brosur/ozellikler/Entegrasyon.dc.html", "Taslak: POS ve İK entegrasyonları (web)", "Bağlantı durumu, son senk, şube ↔ kasa eşlemesi", ["taslak"]),
        (D+"05-tasarim/07-brosur/ozellikler/KameraSayim.dc.html", "Taslak: kamera ile üretim sayımı (web)", "Saatlik üretim/satış çubukları, açıklanamayan fark, KVKK sınırları", ["taslak"]),
        (D+"05-tasarim/07-brosur/build_ozellikler.py", "Özellik föyü üretici (build_ozellikler.py)", "9 sayfayı, 15 ekranı, yazdırma HTML/PDF ve yayın sürümünü üretir", ["betik"]),
        (D+"05-tasarim/07-brosur/tanitim/Detay.dc.html", "Ekran tasarımı: çalıştırma detayı (web)", "Maddeler, damgalı kanıt fotoğrafları, aksiyon, hash zincirli olay izi, doğrulama kodu", ["tasarım"]),
        (D+"05-tasarim/07-brosur/tanitim/Sihirbaz.dc.html", "Ekran tasarımı: kurulum sihirbazı (web)", "Adım 3: tekrar ve pencere, atama, sabit eskalasyon, şube başına hesaplanan pencere", ["tasarım"]),
        (D+"05-tasarim/07-brosur/tanitim/Yapilamadi.dc.html", "Ekran tasarımı: yapılamadı (mobil)", "Sebep seti, not, işareti kaldır; şube müdürüne bildirim", ["tasarım"]),
        (D+"05-tasarim/07-brosur/build_tanitim.py", "Tanıtım dosyası üretici (build_tanitim.py)", "8 sayfayı, 3 ekranı, yazdırma HTML/PDF ve yayın sürümünü üretir", ["betik"]),
        (D+"05-tasarim/07-brosur/KioskListe.dc.html", "Ekran tasarımı: kapanış listesi (kiosk)", "Gerçeğe yakın, 390×844; tasarım sistemi token'larıyla", ["tasarım"]),
        (D+"05-tasarim/07-brosur/Sicaklik.dc.html", "Ekran tasarımı: sıcaklık aralık dışı", "Alt sayfa: kabul aralığı, ± giriş, kritik uyarısı, not, fotoğraf", ["tasarım"]),
        (D+"05-tasarim/07-brosur/SabahOzeti.dc.html", "Ekran tasarımı: sabah özeti (bölge müdürü)", "Push bildirimi + Bölgem listesi: 12 şubeden 10'u yolunda", ["tasarım"]),
        (D+"05-tasarim/07-brosur/Pano.dc.html", "Ekran tasarımı: web pano (istisna görünümü)", "1200×760: KPI'lar, dikkat isteyenler tablosu, şube × liste ızgarası", ["tasarım"]),
        (D+"05-tasarim/07-brosur/build_brosur.py", "Broşür üretici (build_brosur.py)", "Artboard'ları, yazdırma HTML'ini ve PDF'i üretir", ["betik"]),
        (D+"05-tasarim/marka/Main.dc.html", "Marka: Talimatname Mühür sistemi", "Logo artboard'ları (sayfa + mühür işareti, Bitter wordmark)", ["canlı sayfa"]),
        (D+"05-tasarim/marka/YapLutfenA.dc.html", "Marka: yap lütfen A", "İsim testi kartı logo taslağı", []),
        (D+"05-tasarim/marka/YapLutfenB.dc.html", "Marka: yap lütfen B", "İsim testi kartı logo taslağı", []),
        (D+"05-tasarim/marka/YapLutfenC.dc.html", "Marka: yap lütfen C", "İsim testi kartı logo taslağı", []),
        (D+"05-tasarim/marka/TamamlistA.dc.html", "Marka: tamamlist A", "İsim testi kartı logo taslağı", []),
        (D+"05-tasarim/marka/TamamlistB.dc.html", "Marka: tamamlist B", "İsim testi kartı logo taslağı", []),
        (D+"05-tasarim/marka/TamamlistC.dc.html", "Marka: tamamlist C", "İsim testi kartı logo taslağı", []),
        (D+"05-tasarim/marka/Tembihle.dc.html", "Marka: tembihle", "İsim testi kartı logo taslağı", []),
        (D+"05-tasarim/marka/build_refined.py", "Marka üretici (build_refined.py)", "Rafine logo sistemlerini üretir", ["betik"]),
    ]),
    ("06 Test", [
        (D+"06-test/01-test-stratejisi.md", "Test stratejisi", "Katmanlar, kapsam, araçlar, çıkış ölçütleri", []),
        (D+"06-test/02-kabul-test-senaryolari.md", "Kabul test senaryoları", "TC-001…126; her TC FR ve UC'ye bağlı; sürüm sütunu", []),
        (D+"06-test/03-test-verisi-ve-ortam.md", "Test verisi ve ortam", "Kahve Durağı test zinciri, kullanıcılar, şablonlar, ortamlar", []),
        (D+"06-test/04-cihaz-matrisi.md", "Cihaz matrisi", "Android/iOS sürümleri, tablet ve telefon modelleri, tarayıcılar", []),
        (D+"06-test/05-pilot-uat-plani.md", "Pilot UAT planı", "8 haftalık pilot kabul planı ve K3 ölçümü", []),
        (D+"06-test/06-demo-kapsam-denetimi.md", "Demo kapsam denetimi", "123 v1 FR'si saha demosuna karşı işaretli: çalışıyor / kısmen / etiketli gösterim / demo dışı", []),
    ]),
    ("07 Geliştirme", [
        (D+"07-gelistirme/00-kodlama-hazirlik-indeksi.md", "Kodlama hazırlık indeksi", "Kodlamaya başlamadan okunacaklar (sıralı) ve hazırlık kontrol listesi", ["kaynak"]),
        (D+"07-gelistirme/01-teknik-mimari.md", "Teknik mimari", "Bileşenler, akışlar, çevrimdışı senk, bildirim, altyapı diyagramı", []),
        (D+"07-gelistirme/02-repo-ve-ortam-kurulumu.md", "Repo ve ortam kurulumu", "Kod depoları, CI, ortamlar, sırlar, kalite kapıları", []),
        (D+"07-gelistirme/03-backlog-ve-sprint-plani.md", "Backlog ve sprint planı", "EP-01…12, 112 hikâye, S1–S10 (Alfa S6, Beta S8, GA S10), tampon S11–S12, v1.1 listesi", []),
        (D+"07-gelistirme/04-tanimlar-dor-dod.md", "DoR / DoD", "Hazır ve bitti tanımları", []),
        (D+"07-gelistirme/07-serbest-gelistirici-secimi.md", "Serbest geliştirici seçimi", "İki rol, ilan metni, seçim adımları, 45 dk görüşme soruları, 3 saatlik ücretli mini görevler ve rubrik, mesaj şablonları, sözleşme başlıkları, kurucu hazırlık listesi", ["kaynak"]),
        (D+"07-gelistirme/ilan/serbest-gelistirici-ilani.html", "İlan (gönderilebilir)", "Tek sayfa A4: ürün, iki rol, çalışma şekli, seçim, başvuru — PDF'i aynı klasörde", ["basılı"]),
        (D+"07-gelistirme/ilan/serbest-gelistirici-ilani.pdf", "İlan — PDF", "Yazdırmaya/göndermeye hazır", ["basılı"]),
        (D+"07-gelistirme/06-ilk-gun-paketi.md", "Geliştirici ilk gün paketi", "Hesaplar, ortam, okuma sırası, ilk hafta spike'ları, çalışma kuralları, ritim, sağlayıcı soruları", ["kaynak"]),
        (D+"07-gelistirme/05-sprint0-ve-teknik-spike.md", "Sprint 0 ve teknik spike'lar", "Takvim (kritik yol), ekip seçenekleri, 2 haftalık plan, dört spike: çevrimdışı senk, RRULE pencere, kamera-damga-hash, push→SMS; DoD", ["kaynak"]),
        (D+"07-gelistirme/sablonlar/subeler.xlsx", "İçe aktarma: subeler.xlsx", "Kurulum sihirbazı adım 1 — şube listesi şablonu (örnek satır + Açıklama sayfası)", ["dosya"]),
        (D+"07-gelistirme/sablonlar/personel.xlsx", "İçe aktarma: personel.xlsx", "Kurulum sihirbazı adım 4 — personel ve roller şablonu (örnek satırlar + Açıklama sayfası)", ["dosya"]),
        (D+"07-gelistirme/sablonlar/build_sablonlar.py", "Şablon üretici (build_sablonlar.py)", "İki Excel şablonunu üretir (openpyxl)", ["betik"]),
    ]),
    ("Karar kayıtları (ADR)", [
        (D+"adr/0001-calisma-adi-talimatname.md", "ADR-0001 Çalışma adı: Talimatname", "İsim değerlendirmesi ve geçici karar", []),
        (D+"adr/0002-mobil-flutter-web-react.md", "ADR-0002 Flutter · React · FastAPI · PostgreSQL", "Teknoloji seçimi", []),
        (D+"adr/0003-veri-tr-barindirma.md", "ADR-0003 Veri Türkiye'de barındırılır", "Barındırma kararı; pilot BT şartına göre gözden geçirilir", []),
        (D+"adr/0004-kanit-butunlugu-hash-zinciri.md", "ADR-0004 Kanıt bütünlüğü", "Sunucu zamanı, dosya hash'i, ekle-yalnız olay günlüğü", []),
        (D+"adr/0005-tekrar-kurallari-rrule.md", "ADR-0005 Tekrar kuralları: RRULE + pencere", "Tekrar ve pencere modeli", []),
        (D+"adr/0006-whatsapp-mvp-disi.md", "ADR-0006 WhatsApp MVP dışı", "Push + SMS yedek; kanal-bağımsız bildirim", []),
        (D+"adr/0007-kisi-skoru-yok.md", "ADR-0007 Kişi skoru yok", "Skor şube düzeyinde", []),
        (D+"adr/0008-v1-cekirdek.md", "ADR-0008 v1 çekirdek", "Basit, ilk gün kullanılabilir çekirdek; K1–K21, E1–E7", []),
        (D+"adr/0009-ekip-modeli-serbest-gelistirici.md", "ADR-0009 Ekip modeli: iki serbest geliştirici", "Seçenek A; Sprint 2 sonu devam/dur kapısı; hedef başlangıç 5 Ekim", []),
        (D+"adr/0011-uretim-satis-mutabakati.md", "ADR-0011 Üretim–satış mutabakatı (kayıt dışı satış)", "Çıktı suçlama değil açıklanamayan fark; L0 sayım → L1 tüketim mutabakatı → L2 kamera sayımı → L3 POS eşleştirme; doğrulama kapıları ve KVKK sınırları", []),
        (D+"adr/0010-madde-kutuphanesi-v1-1.md", "ADR-0010 Madde kütüphanesi ve paketler: v1.1", "v1 değişmez; madde kütüphanesi, kaynak takibi, işletme türü paketleri v1.1 ilk epic; başka dikeyler ve marka kütüphanesi v2", []),
    ]),
]

ALL = [(g, p, t, d, tags) for g, items in REGISTRY for (p, t, d, tags) in items]
PATHS = {p for _, p, _, _, _ in ALL}
ORDER = [p for _, p, _, _, _ in ALL]

def kind(p):
    ext = p.rsplit(".", 1)[-1].lower()
    if ext == "md": return "md"
    if ext == "html": return "html"
    if ext in ("py", "txt"): return "code"
    return "link"

def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()

# ---------- Markdown → HTML
MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"],
                       extension_configs={"toc": {"slugify": slugify_unicode, "toc_depth": "2-3"}})

def inline(s):
    MD.reset()
    h = MD.convert(s.strip())
    return re.sub(r"^<p>|</p>$", "", h.strip())

def resolve_links(h, docpath):
    def rep(m):
        href = m.group(1)
        if re.match(r"^(https?:|mailto:|tel:)", href):
            return f'href="{href}" target="_blank" rel="noopener"'
        if href.startswith("#"):
            return f'href="#d/{docpath}@{href[1:]}"'
        target, _, frag = href.partition("#")
        base = posixpath.dirname(docpath)
        p = posixpath.normpath(posixpath.join(base, target)) if target else docpath
        if p in PATHS:
            return f'href="#d/{p}' + (f"@{frag}" if frag else "") + '"'
        url = (GH_BLOB if "." in posixpath.basename(p) else GH_TREE) + p
        return f'href="{url}" target="_blank" rel="noopener"'
    return re.sub(r'href="([^"]*)"', rep, h)

def md_to_html(text, docpath):
    # YAML başlık bloğu → yaml kod bloğu
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
    if m:
        text = "```yaml\n" + m.group(1) + "\n```\n" + text[m.end():]
    MD.reset()
    h = MD.convert(text)
    toc = [t for t in MD.toc_tokens if t["level"] == 2]
    h = re.sub(r"<pre><code class=\"language-mermaid\">(.*?)</code></pre>",
               r'<div class="mmd"><pre class="mmd-src">\1</pre></div>', h, flags=re.S)
    h = h.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    h = re.sub(r"<li>\[ \] ", '<li class="task"><i class="cb"></i>', h)
    h = re.sub(r"<li>\[x\] ", '<li class="task"><i class="cb on"></i>', h, flags=re.I)
    h = re.sub(r'<(h[1-6]) id="([^"]+)"', r'<\1 id="h-\2"', h)
    h = re.sub(r"^\s*<h1[^>]*>.*?</h1>\s*", "", h, count=1, flags=re.S)  # başlık üstte zaten var
    h = resolve_links(h, docpath)
    if len(toc) >= 4:
        chips = "".join(f'<a href="#d/{docpath}@{t["id"]}">{html.escape(t["name"])}</a>' for t in toc)
        h = f'<nav class="toc"><span>Bu belgede</span>{chips}</nav>' + h
    return h

def code_to_html(text):
    return f'<pre class="code"><code>{html.escape(text)}</code></pre>'

# ---------- Belge tabloları (dinamik içerik)
def section(text, heading):
    m = re.search(r"^## " + re.escape(heading) + r".*?$\n(.*?)(?=^## |\Z)", text, flags=re.S | re.M)
    return m.group(1) if m else ""

def table_rows(sec):
    rows = [l for l in sec.split("\n") if l.startswith("|")]
    out = []
    for l in rows[2:]:
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        out.append(cells)
    return out

def status_chip(s):
    if "✅" in s: cls, txt = "done", s.replace("✅", "").strip()
    elif "🟡" in s: cls, txt = "active", s.replace("🟡", "").strip()
    else: cls, txt = "todo", s.replace("⏳", "").strip()
    return f'<span class="chip {cls}">{html.escape(txt)}</span>'

def count_ids(path, prefix):
    ids = set(re.findall(r"^\| (%s-\d+)" % prefix, read(path), flags=re.M))
    return len(ids)

def count_versions(path, prefix):
    """'Sürüm' sütunlu tablolarda id'li satırları sürüme göre sayar."""
    total = v1 = 0
    col = None
    lines = read(path).split("\n")
    for i, l in enumerate(lines):
        if not l.startswith("|"): continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if i + 1 < len(lines) and re.match(r"^\|\s*-", lines[i + 1]):
            col = next((j for j, c in enumerate(cells) if c.startswith("Sürüm")), None)
            continue
        if re.match(r"^%s-\d+" % prefix, cells[0]) and col is not None and col < len(cells):
            total += 1
            v = cells[col]
            if v.startswith("v1") and not v.startswith("v1.1"): v1 += 1
    return total, v1

def git_info():
    try:
        out = subprocess.check_output(["git", "-C", ROOT, "log", "-1", "--format=%h %cs"], text=True).strip()
        return out.split(" ", 1)
    except Exception:
        return ("—", "—")

# ---------- Sayfa parçaları
def build_docs():
    docs, groups = {}, []
    for g, items in REGISTRY:
        groups.append((g, [p for p, _, _, _ in items]))
        for p, t, d, tags in items:
            k = kind(p)
            entry = {"t": t, "g": g, "k": k, "d": d, "tags": tags, "live": LIVE.get(p, ""), "gh": GH_BLOB + p}
            if k == "md":
                entry["h"] = md_to_html(read(p), p)
            elif k == "code":
                entry["h"] = code_to_html(read(p))
            else:
                entry["h"] = ""
            docs[p] = entry
    return docs, groups

def nav_html(groups, docs):
    out = []
    for g, paths in groups:
        items = "".join(
            f'<a class="nl" data-p="{p}" href="#d/{p}"><span>{html.escape(docs[p]["t"])}</span>'
            f'<span class="k">{docs[p]["k"] if docs[p]["k"] != "code" else "kod"}</span></a>' for p in paths)
        out.append(f'<div class="grp" data-g="{html.escape(g)}"><div class="grp-t">{html.escape(g)}</div>{items}</div>')
    return "".join(out)

def cards_html(groups, docs):
    out = []
    for g, paths in groups:
        cards = []
        for p in paths:
            e = docs[p]
            tags = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in e["tags"])
            live = f'<a class="tag live" href="{e["live"]}" target="_blank" rel="noopener">canlı sayfa ↗</a>' if e["live"] else ""
            tags = tags.replace('<span class="tag">canlı sayfa</span>', "")
            cards.append(f'<div class="card"><a class="t" href="#d/{p}">{html.escape(e["t"])}</a>'
                         f'<div class="d">{html.escape(e["d"])}</div><div class="m">{tags}{live}</div></div>')
        out.append(f'<h3 id="grp-{len(out)}">{html.escape(g)}</h3><div class="cards">{"".join(cards)}</div>')
    return "".join(out)

def phases_html():
    rows = table_rows(section(read(D + "00-calisma-plani.md"), "Fazlar ve teslimatlar"))
    tr = []
    for c in rows:
        if len(c) < 4: continue
        tr.append(f"<tr><td class=\"nw\"><strong>{inline(c[0])}</strong></td><td>{resolve_links(inline(c[1]), D+'00-calisma-plani.md')}</td>"
                  f"<td class=\"mut\">{resolve_links(inline(c[2]), D+'00-calisma-plani.md')}</td><td class=\"nw\">{status_chip(c[3])}</td></tr>")
    return ("<div class=\"tw\"><table class=\"plain\"><thead><tr><th>Faz</th><th>İçerik</th><th>Teslimatlar</th><th>Durum</th></tr></thead>"
            f"<tbody>{''.join(tr)}</tbody></table></div>")

def decisions_html():
    hub = D + "00-urun-merkezi.md"
    rows = table_rows(section(read(hub), "Karar haritası"))
    tr = "".join(f"<tr><td class=\"nw\"><strong>{inline(c[0])}</strong></td><td>{inline(c[1])}</td><td class=\"nw\">{resolve_links(inline(c[2]), hub)}</td></tr>"
                 for c in rows if len(c) >= 3)
    return f"<div class=\"tw\"><table class=\"plain\"><thead><tr><th>Karar</th><th>Seçim</th><th>Kayıt</th></tr></thead><tbody>{tr}</tbody></table></div>"

OPEN_NOTES = [
    (r"kiosk", "Sinyal: görüşme notlarındaki <code>tablet_sube_orani</code> ve şube gözlemleri (puanla.py “Tablet” satırı). Eşik: şubelerin ≥ %50'sinde ortak tablet varsa kiosk v1'de kalır; altındaysa personel telefonu birincil, kiosk isteğe bağlı."),
    (r"self-servis", "v1'de yok. K2 sonrası gelen talep sayısına göre v1.x'e alınır; fizibilitede tekil segmentin birim ekonomisi zincirden zayıf (Baz LTV/CAC 2,7'ye karşı 6,3)."),
    (r"franchise", "Sinyal: <code>franchise_bayi_gorsun</code> cevapları ve franchise ağırlıklı 4 görüşme. Varsayılan: bayi sahibi kendi şubesini şube müdürü yetkisiyle görür; ayrı “Gözlemci” rolü v1.1."),
    (r"barındırma", "Sinyal: <code>barindirma_sarti</code> sayımı (TR sunucu / on-premise / sözleşme yeter / şart yok). Varsayılan ADR-0003: Türkiye'de yerel bulut; “AB + standart sözleşme yeter” çoğunluksa ikinci bölge seçeneği açılır."),
    (r"prob", "Sinyal: <code>prob_talebi</code> oranı ve sıcaklık defteri gözlemi (kaç ekipman, hangi alet). v1'de manuel giriş; görüşmelerin ≥ 1/3'ü isterse v1.1'e Should olarak girer."),
    (r"ekip", "Sinyal: K1 öncesi başlamak riskli ama beklemek pilotu kaydırır (07-gelistirme/05 §1). Öneri: seçenek A veya C ile Sprint 0'ı 28 Eylül'de başlat; Sprint 2 sonunda K1 raporuyla devam/dur kapısı."),
    (r"marka adı|isim", "Sinyal: isim testi kartları (<code>isim_tercihi</code> sayımı; Talimatname her görüşmede masada). Karar 9–12. haftada ADR ile; alan adları 12 Eylül'de 4/4 boştu — karar günü kapatılır."),
]

def open_html():
    sec = section(read(D + "00-urun-merkezi.md"), "Açık kararlar")
    items = re.findall(r"^\d+\.\s+(.*)$", sec, flags=re.M)
    out = []
    for it in items:
        note = next((n for pat, n in OPEN_NOTES if re.search(pat, it, flags=re.I)), "")
        out.append(f"<li><strong>{inline(it)}</strong>{('<p>' + note + '</p>') if note else ''}</li>")
    return f"<ul class=\"open\">{''.join(out)}</ul>"

def gates_html():
    plan = read(D + "01-strateji/dogrulama-sprinti/00-sprint-plani.md")
    rows = table_rows(section(plan, "Kapılar"))
    ozet = read(D + "01-strateji/gorusmeler/00-ozet.md")
    notes = re.search(r"(\d+) görüşme notu", ozet)
    k1 = re.search(r"\*\*K1\*\*.*?\*\*(\d+) / (\d+)\*\*", ozet)
    k2 = re.search(r"\*\*K2\*\*.*?\*\*(\d+)\*\*", ozet)
    cur = {"K1": f"{k1.group(1)} / {k1.group(2)} not (hedef 12 / 20)" if k1 else "—",
           "K2": f"{k2.group(1)} LOI" if k2 else "—",
           "K3": "pilot başlamadı"}
    tr = "".join(f"<tr><td class=\"nw\"><strong>{inline(c[0])}</strong></td><td class=\"nw\">{inline(c[1])}</td><td>{inline(c[2])}</td>"
                 f"<td class=\"nw\"><span class=\"chip todo\">{cur.get(c[0].strip('* '), '—')}</span></td><td class=\"mut\">{inline(c[3])}</td></tr>"
                 for c in rows if len(c) >= 4)
    n = notes.group(1) if notes else "0"
    return (f"<div class=\"tw\"><table class=\"plain\"><thead><tr><th>Kapı</th><th>Hafta</th><th>Ölçüt</th><th>Bugün</th><th>Geçmezse</th></tr></thead><tbody>{tr}</tbody></table></div>"
            f"<p class=\"mut small\">Sayaç: <a href=\"#d/{D}01-strateji/gorusmeler/00-ozet.md\">gorusmeler/00-ozet.md</a> — {n} görüşme notu işlendi. Karar kuralı: üç kapıdan ikisi tutmazsa proje burada biter; kural sprint başında yazılıdır.</p>")

def risks_html():
    plan = read(D + "01-strateji/dogrulama-sprinti/00-sprint-plani.md")
    rows = table_rows(section(plan, "Riskler"))
    tr = "".join(f"<tr><td><strong>{inline(c[0])}</strong></td><td class=\"mut\">{inline(c[1])}</td><td>{inline(c[2])}</td></tr>" for c in rows if len(c) >= 3)
    return f"<div class=\"tw\"><table class=\"plain\"><thead><tr><th>Risk</th><th>Belirti</th><th>Önlem</th></tr></thead><tbody>{tr}</tbody></table></div>"

def stats():
    import sayilar as SAY                          # sayilarin tek kaynagi (bkz. sayilar.py)
    s = SAY.hepsi()
    fr_t, fr_v1 = s["fr"], s["fr_v1"]
    tc_t, tc_v1 = s["tc"], s["tc_v1"]
    scr_t, scr_v1 = s["scr"], s["scr_v1"]
    br, st = s["br"], s["st"]
    return [
        ("11", "ADR karar kaydı"),
        (str(count_ids(D + "02-urun/04-yetenek-haritasi.md", "CAP")), "yetenek (CAP)"),
        (str(count_ids(D + "03-analiz/02-usecase-katalogu.md", "UC")), "use case"),
        (str(len(re.findall(r"^## S-\d+", read(D + "03-analiz/04-senaryolar.md"), flags=re.M))), "uçtan uca senaryo"),
        (f"{fr_t}", f"fonksiyonel gereksinim · {fr_v1} v1"),
        (str(br), "iş kuralı"),
        (str(count_ids(D + "04-gereksinimler/02-fonksiyonel-olmayan.md", "NFR")), "fonksiyonel olmayan"),
        (f"{scr_t}", f"ekran · {scr_v1} v1"),
        (f"{tc_t}", f"kabul testi · {tc_v1} v1"),
        (str(st), "hikâye · 10 sprint"),
    ]

def stats_html(items):
    return '<div class="stats">' + "".join(f'<div class="stat"><div class="n">{n}</div><div class="l">{l}</div></div>' for n, l in items) + "</div>"

# ---------- Şablon
TEMPLATE = r"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Talimatname Ürün Dosyası</title>
<meta name="description" content="Talimatname ürününün tek sayfalık özeti, hazırlık belgeleri ve açık konular">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root{--zemin:#f7f5ef;--yuzey:#ffffff;--yuzey2:#efece4;--murekkep:#1c2128;--murekkep2:#4b5560;--sessiz:#7b8590;--cizgi:#d6d9d2;
--marka:#1f6f5b;--marka-acik:#dcebe5;--kritik:#b8452f;--kritik-acik:#f3ddd8;--uyari:#b7791f;--uyari-acik:#f6ebd2;--pasif:#c9ced6;
--kod:#f1efe8;--golge:0 10px 30px rgba(28,33,40,.10);--serif:Bitter,Georgia,"Times New Roman",serif;
--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--zemin:#15191c;--yuzey:#1d2226;--yuzey2:#262c31;--murekkep:#f1eee6;--murekkep2:#b5bcc4;--sessiz:#8a9299;--cizgi:#2f373d;
--marka:#3fa98c;--marka-acik:#173a31;--kritik:#e46f5a;--kritik-acik:#3a201b;--uyari:#e0a640;--uyari-acik:#33290f;--pasif:#3a424a;--kod:#12161a;--golge:0 10px 30px rgba(0,0,0,.45)}}
:root[data-theme="dark"]{--zemin:#15191c;--yuzey:#1d2226;--yuzey2:#262c31;--murekkep:#f1eee6;--murekkep2:#b5bcc4;--sessiz:#8a9299;--cizgi:#2f373d;
--marka:#3fa98c;--marka-acik:#173a31;--kritik:#e46f5a;--kritik-acik:#3a201b;--uyari:#e0a640;--uyari-acik:#33290f;--pasif:#3a424a;--kod:#12161a;--golge:0 10px 30px rgba(0,0,0,.45)}
*{box-sizing:border-box}
html{color-scheme:light dark;scroll-behavior:smooth}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{margin:0;background:var(--zemin);color:var(--murekkep);font:16px/1.5 var(--sans);-webkit-font-smoothing:antialiased}
a{color:var(--marka)}
a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--marka);outline-offset:2px}
h1,h2,h3,h4,.wm{font-family:var(--serif);font-weight:600;line-height:1.2;text-wrap:balance;margin:0}
h1{font-size:clamp(30px,4.5vw,40px);font-weight:700}
h2{font-size:26px;margin-top:8px}
h3{font-size:19px}
h4{font-size:16px}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--sessiz)}
.mut{color:var(--murekkep2)} .small{font-size:14px} .nw{white-space:nowrap}
code{font:.9em var(--mono);background:var(--kod);padding:1px 5px;border-radius:5px}
pre{background:var(--kod);border:1px solid var(--cizgi);border-radius:10px;padding:12px 14px;overflow-x:auto;font:13px/1.55 var(--mono)}
pre code{background:none;padding:0;font:inherit}
.app{display:grid;grid-template-columns:296px minmax(0,1fr);min-height:100vh}
aside{position:sticky;top:0;height:100vh;overflow-y:auto;border-right:1px solid var(--cizgi);background:var(--yuzey);padding:20px 14px 32px;scrollbar-width:thin}
.brand{display:flex;align-items:center;gap:10px;padding:0 8px 14px;text-decoration:none;color:inherit}
.brand .wm{font-size:22px;font-weight:700;letter-spacing:-.01em}
.brand .sub{display:block;font:12px var(--sans);color:var(--sessiz);letter-spacing:.06em;text-transform:uppercase}
.mark{width:34px;height:34px;flex:none}
#q{width:100%;padding:8px 10px;border:1px solid var(--cizgi);border-radius:8px;background:var(--zemin);color:inherit;font:14px var(--sans);margin:2px 0 6px}
#qn{font-size:12px;color:var(--sessiz);padding:0 8px;min-height:16px}
.grp-t{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--sessiz);margin:16px 0 4px;padding:0 8px}
.nl{display:flex;justify-content:space-between;gap:8px;padding:5px 8px;border-radius:8px;color:var(--murekkep);text-decoration:none;font-size:14px;line-height:1.35}
.nl:hover{background:var(--yuzey2)} .nl.on{background:var(--marka-acik);color:var(--marka);font-weight:600}
.nl .k{font:11px var(--mono);color:var(--sessiz);flex:none;padding-top:3px}
.nl.hid,.grp.hid{display:none}
.nav-home .nl{font-weight:500}
main{padding:0 clamp(16px,4vw,48px) 56px;max-width:1160px;width:100%}
.top{display:flex;align-items:center;gap:12px;padding:14px 0;border-bottom:1px solid var(--cizgi);position:sticky;top:0;background:var(--zemin);z-index:5}
#menu{display:none;border:1px solid var(--cizgi);background:var(--yuzey);color:inherit;border-radius:8px;padding:6px 10px;font:14px var(--sans);cursor:pointer}
.crumb{font-size:14px;color:var(--murekkep2);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.crumb b{color:var(--murekkep);font-weight:600}
.backdrop{display:none;position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:15}
/* --- genel bakış */
.hero{padding:40px 0 28px;border-bottom:1px solid var(--cizgi)}
.hero .tag{font-family:var(--serif);font-size:22px;color:var(--marka);margin:6px 0 14px}
.lead{font-size:18px;line-height:1.55;max-width:70ch;margin:0}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.chip{display:inline-flex;align-items:center;gap:7px;padding:3px 11px;border-radius:999px;font-size:13px;font-weight:500;border:1px solid transparent;background:var(--yuzey2);color:var(--murekkep2);white-space:nowrap}
.chip::before{content:"";width:8px;height:8px;border-radius:50%;background:currentColor;flex:none}
.chip.done{background:var(--marka-acik);color:var(--marka)} .chip.active{background:var(--uyari-acik);color:var(--uyari)} .chip.todo{background:var(--yuzey2);color:var(--murekkep2)}
.chip.crit{background:var(--kritik-acik);color:var(--kritik)}
.chip.plain::before{display:none}
.ctas{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 14px;border-radius:10px;border:1px solid var(--cizgi);background:var(--yuzey);color:var(--murekkep);text-decoration:none;font-size:14px;font-weight:500}
.btn:hover{border-color:var(--marka);color:var(--marka)} .btn.pri{background:var(--marka);border-color:var(--marka);color:#fff} .btn.pri:hover{color:#fff;filter:brightness(1.08)}
section.blk{padding:36px 0 8px}
section.blk>.eyebrow{margin-bottom:6px}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;margin-top:16px}
.grid2 p,.grid2 li{max-width:62ch}
.loop{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin-top:16px}
.step{background:var(--yuzey);border:1px solid var(--cizgi);border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:6px}
.step .no{font:700 30px/1 var(--serif);color:var(--marka);font-variant-numeric:tabular-nums}
.step h4{font-size:17px} .step p{margin:0;font-size:14px;color:var(--murekkep2)}
.kv{display:grid;grid-template-columns:max-content 1fr;gap:8px 18px;margin-top:16px;font-size:15px}
.kv dt{color:var(--murekkep2);font-weight:500} .kv dd{margin:0;max-width:78ch}
.mods{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin-top:16px}
.mod{background:var(--yuzey);border:1px solid var(--cizgi);border-radius:12px;padding:14px 16px}
.mod h4{font-size:15px;margin-bottom:6px;color:var(--marka)} .mod p{margin:0;font-size:14px;color:var(--murekkep2)}
.callout{border-left:3px solid var(--marka);background:var(--marka-acik);padding:12px 16px;border-radius:0 10px 10px 0;margin-top:18px;max-width:80ch}
.callout p{margin:0} .callout ol{margin:8px 0 0;padding-left:20px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--cizgi);border:1px solid var(--cizgi);border-radius:12px;overflow:hidden;margin-top:16px}
.stat{background:var(--yuzey);padding:14px 16px}
.stat .n{font:700 28px/1.1 var(--serif);font-variant-numeric:tabular-nums} .stat .l{font-size:13px;color:var(--murekkep2);margin-top:4px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin:12px 0 26px}
.card{background:var(--yuzey);border:1px solid var(--cizgi);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:6px}
.card a.t{font-weight:600;color:inherit;text-decoration:none} .card a.t:hover{color:var(--marka)}
.card .d{font-size:14px;color:var(--murekkep2)} .card .m{margin-top:auto;display:flex;gap:6px;flex-wrap:wrap;padding-top:6px}
.tag{font:12px var(--sans);color:var(--sessiz);background:var(--yuzey2);border-radius:6px;padding:1px 7px;text-decoration:none}
.tag.live{color:var(--marka);background:var(--marka-acik)}
table.plain{border-collapse:collapse;width:100%;font-size:14px;background:var(--yuzey)}
table.plain th,table.plain td{border-bottom:1px solid var(--cizgi);padding:9px 11px;text-align:left;vertical-align:top}
table.plain th{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--murekkep2);background:var(--yuzey2)}
.tw{overflow-x:auto;margin:14px 0;border:1px solid var(--cizgi);border-radius:10px}
.tw table{margin:0}
ul.open{list-style:none;padding:0;margin:14px 0 0;display:grid;gap:10px}
ul.open li{background:var(--yuzey);border:1px solid var(--cizgi);border-left:3px solid var(--uyari);border-radius:10px;padding:12px 16px}
ul.open li p{margin:6px 0 0;font-size:14px;color:var(--murekkep2);max-width:90ch}
.todo{list-style:none;padding:0;margin:14px 0 0;display:grid;gap:6px;max-width:80ch}
.todo li{display:flex;gap:10px;align-items:flex-start}
.todo input{margin-top:5px;accent-color:var(--marka);width:16px;height:16px;flex:none}
.todo label{cursor:pointer} .todo .why{display:block;font-size:13px;color:var(--sessiz)}
.scen{font-variant-numeric:tabular-nums}
.stamp{margin-top:56px;display:inline-block;padding:12px 16px;border:1.5px solid var(--kritik);color:var(--kritik);border-radius:6px;font:12px/1.6 var(--mono);letter-spacing:.05em;text-transform:uppercase;transform:rotate(-1deg)}
.stamp a{color:inherit}
.foot{margin-top:14px;font-size:13px;color:var(--sessiz)}
/* --- belge görünümü */
.dochead{padding:26px 0 14px;border-bottom:1px solid var(--cizgi);margin-bottom:20px;display:flex;flex-direction:column;gap:10px}
.dochead h1{font-size:clamp(24px,3.4vw,32px)}
.dochead .acts{display:flex;flex-wrap:wrap;gap:8px}
.dochead .acts a{font-size:13px;padding:5px 10px}
.dochead .desc{color:var(--murekkep2);max-width:80ch;margin:0}
.frame{width:100%;height:calc(100vh - 190px);min-height:560px;border:1px solid var(--cizgi);border-radius:12px;background:#fff}
.toc{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:13px;margin:0 0 18px;padding:10px 12px;background:var(--yuzey2);border-radius:10px}
.toc span{color:var(--sessiz);margin-right:4px} .toc a{text-decoration:none;background:var(--yuzey);border:1px solid var(--cizgi);border-radius:999px;padding:2px 10px;color:var(--murekkep)}
.prose{font-size:15.5px}
.prose>h1{font-size:28px;margin:0 0 14px}
.prose h2{font-size:22px;margin:34px 0 10px;padding-top:6px}
.prose h3{font-size:18px;margin:24px 0 8px}
.prose h4{font-size:16px;margin:18px 0 6px}
.prose p,.prose li{max-width:80ch}
.prose ul,.prose ol{padding-left:22px}
.prose li{margin:3px 0}
.prose hr{border:0;border-top:1px solid var(--cizgi);margin:24px 0}
.prose blockquote{margin:14px 0;padding:8px 16px;border-left:3px solid var(--cizgi);color:var(--murekkep2)}
.prose table{border-collapse:collapse;width:100%;font-size:14px;background:var(--yuzey)}
.prose th,.prose td{border-bottom:1px solid var(--cizgi);padding:7px 10px;text-align:left;vertical-align:top}
.prose th{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--murekkep2);background:var(--yuzey2);white-space:nowrap}
.prose tr:last-child td{border-bottom:0}
.prose img{max-width:100%}
li.task{list-style:none;margin-left:-22px;display:flex;gap:8px;align-items:flex-start}
.cb{display:inline-block;width:15px;height:15px;border:1.5px solid var(--sessiz);border-radius:4px;margin-top:4px;flex:none}
.cb.on{background:var(--marka);border-color:var(--marka)}
.mmd{overflow-x:auto;padding:10px;background:var(--yuzey);border:1px solid var(--cizgi);border-radius:12px;margin:14px 0}
.mmd svg{max-width:100%;height:auto}
.mmd-src{margin:0;border:0;background:none;color:var(--sessiz);font-size:12px;white-space:pre}
.pn{display:flex;justify-content:space-between;gap:12px;margin-top:44px;padding-top:16px;border-top:1px solid var(--cizgi);font-size:14px}
.pn a{text-decoration:none;max-width:48%} .pn .lab{display:block;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--sessiz)}
.pn .r{text-align:right;margin-left:auto}
@media (max-width: 900px){
  .app{grid-template-columns:1fr}
  aside{position:fixed;left:0;top:0;width:min(330px,88vw);transform:translateX(-102%);transition:transform .2s ease;z-index:20;box-shadow:var(--golge)}
  .app.open aside{transform:none} .app.open .backdrop{display:block}
  #menu{display:inline-flex}
  .frame{height:78vh}
  .kv{grid-template-columns:1fr;gap:2px 0} .kv dt{margin-top:8px}
}
</style>

<div class="app" id="app">
<div class="backdrop" id="backdrop"></div>
<aside id="side">
  <a class="brand" href="#">
    <svg class="mark" viewBox="0 0 34 34" aria-hidden="true"><path d="M6 3h15l7 7v21H6z" fill="var(--yuzey)" stroke="var(--murekkep)" stroke-width="2" stroke-linejoin="round"/><path d="M21 3v7h7" fill="none" stroke="var(--murekkep)" stroke-width="2" stroke-linejoin="round"/><path d="M10 15h14M10 20h14M10 25h8" stroke="var(--murekkep2)" stroke-width="2" stroke-linecap="round"/><rect x="18" y="19" width="13" height="13" rx="3" fill="var(--kritik)" transform="rotate(-8 24.5 25.5)"/><path d="M21.5 25.5l2.2 2.2 4.3-4.6" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" transform="rotate(-8 24.5 25.5)"/></svg>
    <span><span class="wm">Talimatname</span><span class="sub">Ürün dosyası</span></span>
  </a>
  <input id="q" type="search" placeholder="Belgelerde ara…" aria-label="Belgelerde ara" autocomplete="off">
  <div id="qn"></div>
  <nav id="nav">
    <div class="nav-home">
      <a class="nl" data-h="" href="#"><span>Genel bakış</span></a>
      <a class="nl" data-h="urun" href="#urun"><span>Ürün</span></a>
      <a class="nl" data-h="hazirlik" href="#hazirlik"><span>Hazırlıklar</span></a>
      <a class="nl" data-h="acik" href="#acik"><span>Açık konular</span></a>
    </div>
    {{NAV}}
  </nav>
</aside>
<main id="main">
  <header class="top"><button id="menu" type="button" aria-controls="side">☰ Belgeler</button><div class="crumb" id="crumb"><b>Genel bakış</b></div></header>

  <section id="home">
    <div class="hero">
      <div class="eyebrow">Ürün dosyası · iş analizi ve ürün sahipliği · {{DATE_TR}}</div>
      <h1>Talimatname</h1>
      <div class="tag">Şube operasyonları, kanıtıyla.</div>
      <p class="lead">Çok şubeli yeme-içme zincirlerinin şubelere verdiği tekrarlı talimatları — açılış, kapanış, hijyen, soğuk zincir, haftalık temizlik — WhatsApp gruplarından çıkarıp <strong>kanıtlı, kayıtlı ve raporlanabilir</strong> hâle getiren mobil + web ürün. Personel listeyi şube tabletinden veya telefonundan tamamlar, fotoğraf ve ölçümle kanıtlar, yapamadığını sebebiyle bildirir; merkez her sabah hangi şubede neyin yapılıp yapılmadığını kanıtıyla görür.</p>
      <div class="chips">
        <span class="chip active">Durum · doğrulama sprinti, hafta 0</span>
        <span class="chip done">Fizibilite · Koşullu GO</span>
        <span class="chip done">Kapsam · v1 çekirdek (ADR-0008)</span>
        <span class="chip todo">Çalışma adı · geçici, isim testi sürüyor</span>
      </div>
      <div class="ctas">
        <a class="btn pri" href="#d/docs/02-urun/06-v1-cekirdek-kapsam.md">v1 çekirdek kapsamı</a>
        <a class="btn" href="#d/docs/01-strateji/01-fizibilite.html">Fizibilite raporu</a>
        <a class="btn" href="https://claude.ai/code/artifact/229e7396-313c-487b-9a31-ada9caa05e69" target="_blank" rel="noopener">Prototipi telefonda aç ↗</a>
        <a class="btn" href="{{GH}}" target="_blank" rel="noopener">GitHub deposu ↗</a>
      </div>
    </div>

    <section class="blk" id="urun">
      <div class="eyebrow">Ürün</div>
      <h2>WhatsApp'ta “yapıldı abi 👍” yerine kanıt</h2>
      <div class="grid2">
        <div>
          <h3>Sorun</h3>
          <p>Zincir merkezleri şubelere talimatları WhatsApp gruplarından verir. Tekrarlı işler unutulur; “yapıldı” mesajı kanıt değildir; fotoğraflar arşivde bulunmaz; yapılmayan iş ancak müşteri şikâyeti veya denetimle ortaya çıkar; gıda denetiminde kayıt bulmak saatler sürer; bölge müdürleri ziyaret zamanını kontrolle harcar.</p>
        </div>
        <div>
          <h3>Çözüm</h3>
          <ul>
            <li>Merkez tekrarlı listeleri bir kez kurar; listeler her pencere için şubelerde kendiliğinden açılır.</li>
            <li>Personel listeyi tablet veya telefondan tamamlar; fotoğraf/ölçüm kanıtı çeker; yapamadığını sebebiyle işaretler.</li>
            <li>Başarısız madde ve “yapılamadı” otomatik aksiyona dönüşür; zamanında kapanmazsa yukarı taşınır.</li>
            <li>Merkez her sabah şube × liste ızgarasında durumu görür; denetim kaydı markalı PDF olarak 3 dakikada çıkar.</li>
            <li>Her olay değiştirilemez günlükte; kanıt sunucu zamanı ve hash ile mühürlenir.</li>
          </ul>
        </div>
      </div>

      <h3 style="margin-top:28px">Çekirdek döngü (v1)</h3>
      <div class="loop">
        <div class="step"><div class="no">1</div><h4>Merkez kurar</h4><p>Kapanış, açılış, hijyen ve soğuk zincir listelerini 8 hazır şablondan bir kez kurar; tekrar kuralı ve pencere (ör. 22:00–01:30, tolerans 120 dk) belirler. Kurulum sihirbazı 4 adım.</p></div>
        <div class="step"><div class="no">2</div><h4>Personel tamamlar</h4><p>Kioskta adına dokunup PIN girer; maddeleri işaretler, fotoğraf çeker (kamera doğrudan açılır), sıcaklık girer; yapamadığını sebebiyle işaretler. Kapanış 6–8 dakika; çevrimdışı çalışır.</p></div>
        <div class="step"><div class="no">3</div><h4>Sistem izler</h4><p>Pencereyi izler; kaçırılanı şube müdürüne anında, bölge müdürüne 07:00 özetiyle bildirir. Kritik madde başarısızsa anında push, teslim olmazsa SMS. Her olay hash zincirli günlükte.</p></div>
        <div class="step"><div class="no">4</div><h4>Yönetici görür</h4><p>İstisna odaklı şube × liste ızgarası, sabah özeti, çalıştırma detayı ve fotoğraflar, sıcaklık günlüğü, aylık tek sayfa, doğrulama kodlu PDF.</p></div>
      </div>

      <h3 style="margin-top:28px">Kimin için</h3>
      <dl class="kv">
        <dt>Satın alan</dt><dd>Zincir merkezi operasyon müdürü (5–100 şube)</dd>
        <dt>Kullanan</dt><dd>Şube müdürü ve personel (tablet/telefon), bölge müdürü, kalite sorumlusu</dd>
        <dt>Neyin yerine</dt><dd>WhatsApp grupları, kâğıt formlar, Excel, sıcaklık defteri</dd>
        <dt>İlk pazar</dt><dd>Türkiye · yeme-içme zincirleri (kafe, restoran, fırın, hızlı servis; franchise veren markalar dahil). Tekil işletme self-servisi MVP dışı</dd>
        <dt>Fiyat çıpası</dt><dd>~₺730 / şube / ay (Baz senaryo 15 $) — pilot görüşmelerinde van Westendorp ile test edilir</dd>
        <dt>Değer kanıtı</dt><dd>25 şubelik zincir ayda ~₺18 bin öder; karşılığı şube müdürü başına ~6 saat/ay WhatsApp takibi (≈ ₺37,5 bin), bölge müdürü ziyaretlerinin yarıya inmesi, bir denetim cezasından kaçınma — rakamlar sahadan düzeltilecek</dd>
      </dl>

      <h3 style="margin-top:28px">v1 çekirdek <span class="mut" style="font-weight:400">— ADR-0008, 13 Eylül 2026</span></h3>
      <p style="max-width:80ch">İlk kapsam rakiplerin iyi özelliklerini toplayınca bir “ikinci yıl” ürünü tarif etti (57 Must satırı, 138 hikâye, 25 ekran, 7 rol). Aktör gözüyle gözden geçirme sonrası v1 yalnızca çekirdek döngüyü içerir; ertelenenler silinmedi, <em>v1.1</em> etiketiyle aynı belgelerde duruyor.</p>
      <div class="chips">
        <span class="chip plain">4 rol</span><span class="chip plain">6 madde türü + talimat</span><span class="chip plain">tek sabit kural</span><span class="chip plain">puan = yüzde; başarısız = kritik madde</span><span class="chip plain">8 şablon</span><span class="chip plain">sabit eskalasyon + 07:00 sabah özeti</span><span class="chip plain">sessiz saat 23:00–07:00</span><span class="chip plain">saklama 24 ay</span>
      </div>
      <div class="mods">
        <div class="mod"><h4>M1 Organizasyon ve kimlik</h4><p>Çok kiracılı hesap; Marka › Bölge › Şube; 4 rol; personel telefon + OTP, yönetici e-posta; kiosk (QR kayıt, PIN, 2 dk kilit); şube müdürü PIN atar; Excel içe aktarma.</p></div>
        <div class="mod"><h4>M2 Şablon</h4><p>Bölüm/madde editörü, taslak → yayında → arşiv; onay, çoktan seçmeli, sayı, sıcaklık, metin, fotoğraf (1–3); zorunlu / fotoğraf zorunlu / kritik; 8 şablon.</p></div>
        <div class="mod"><h4>M3 Planlama</h4><p>RRULE tekrar (günlük saatler, her N saat, haftalık, aylık); pencere, tolerans, gece yarısı aşımı; 7 gün ileri üretim; tatil takvimi; tek seferlik liste; “biri tamamlasın” — ilk açan alır.</p></div>
        <div class="mod"><h4>M4 Yürütme (mobil)</h4><p>Bugün ekranı; kamera doğrudan, damga + hash; yapılamadı sebep seti; çevrimdışı 72 saat; sorun bildir; açılış listesinde “dün gece” özeti; yönetici için “Bölgem” listesi.</p></div>
        <div class="mod"><h4>M5 Aksiyon ve eskalasyon</h4><p>Kritik madde, yapılamadı ve kaçırılan listeden otomatik aksiyon; açık/kapalı + not; sabit eskalasyon; 07:00 sabah özeti (push + e-posta); kritikte anında bildirim.</p></div>
        <div class="mod"><h4>M7 Raporlama</h4><p>İstisna odaklı ızgara (“her şey yolunda” durumu); aylık tek sayfa; sıcaklık günlüğü; kanıt galerisi; çalıştırma ve dönem PDF'i, doğrulama kodlu.</p></div>
        <div class="mod"><h4>M8 Denetim izi ve uyum</h4><p>Ekle-yalnız olay günlüğü, hash zinciri (arka plan); KVKK aydınlatma; 24 ay saklama; biyometri yok; TLS, şifreleme, rol × kapsam, hız sınırı.</p></div>
        <div class="mod"><h4>M9 Yönetim paneli</h4><p>4 adımlı kurulum sihirbazı (tek plan); şube/personel yönetimi; aktif şube sayacı; yalnızca Türkçe, i18n hazır. Duyuru modülü (M6) v1.1.</p></div>
      </div>
      <div class="callout">
        <p><strong>Sıra ilkesi.</strong> Bir özellik v1'e ancak şu üç sorudan birine “evet” alırsa girer:</p>
        <ol><li>Personel bunu görmese kapanış listesi tamamlanmaz mı?</li><li>Yönetici bunu görmese kaçırılan iş görünmez mi?</li><li>Bu olmadan denetimde kanıt verilemez mi?</li></ol>
      </div>
      <div class="grid2">
        <div>
          <h3>v1'de bilinçli olarak yok — v1.1 sırası pilotla belirlenir</h3>
          <p class="mut">Duyuru / okundu onayı / imza · koşul editörü · “herkes tamamlasın” · aksiyon yorum dizisi ve onaylı kapanış · ayrıntılı raporlar ve kişi düzeyi takip · denetim izi ekranı ve RFC 3161 zaman damgası · KVKK talep ekranı · 2FA · ayarlar paneli · Excel ve paylaşım bağlantısı · video / imza / barkod maddeleri · QR ile istasyondan başlatma · WhatsApp kanalı.</p>
        </div>
        <div>
          <h3>Hiç yapmadıklarımız (MVP)</h3>
          <p class="mut">Sohbet, mesai/PDKS, vardiya planlama, eğitim/LMS, sensör ve prob entegrasyonu, varlık/bakım iş emri, AI fotoğraf değerlendirme, self-servis kayıt ve ödeme, kişi bazlı performans skoru (ADR-0007), franchise sahibi portalı.</p>
        </div>
      </div>

      <h3 style="margin-top:28px">Neden şimdi</h3>
      <ul style="max-width:80ch">
        <li>Kategori küresel olarak kanıtlı: SafetyCulture (Ağustos 2026'da Mitti oldu) 1,7 mlr $ değerleme; Jolt 145,5 M$'a Digi/SmartSense'e satıldı (2025); Connecteam 800 M$.</li>
        <li>Türkiye'de yerel oyuncu yeni (CheckMaster, Haziran 2025); küreseller Türkçe, TL fiyat ve saha satışı olmadan.</li>
        <li>KVKK Kurulu 2026/921 ilke kararı biyometrik mesai takibini kısıtladı; “kanıt, kişi değil iş” yaklaşımı uyum avantajı.</li>
      </ul>

      <h3 style="margin-top:28px">Fizibilite özeti <span class="mut" style="font-weight:400">— 60 aylık model, sabit USD, 48,6 ₺/$</span></h3>
      <div class="stats">
        <div class="stat"><div class="n">99.700</div><div class="l">lokasyon SAM · $15,7M/yıl</div></div>
        <div class="stat"><div class="n">$1,55M</div><div class="l">Baz senaryo 5. yıl ARR</div></div>
        <div class="stat"><div class="n">$1,13M</div><div class="l">Baz tepe sermaye (Yalın $0,63M)</div></div>
        <div class="stat"><div class="n">57. ay</div><div class="l">Baz başabaş (İyimser 34, Kötümser yok)</div></div>
        <div class="stat"><div class="n">$3,35M</div><div class="l">olasılık ağırlıklı beklenen değer</div></div>
      </div>
      <div class="tw"><table class="plain scen"><thead><tr><th>Senaryo</th><th>Lansman</th><th>Başabaş</th><th>Tepe sermaye</th><th>5. yıl lokasyon</th><th>5. yıl ARR</th><th>MOIC / IRR</th></tr></thead><tbody>
        <tr><td>Kötümser</td><td>8. ay</td><td>—</td><td>$1,63M</td><td>4.182</td><td>$0,49M</td><td>0,8x / −13%</td></tr>
        <tr><td>Yalın</td><td>7. ay</td><td>55. ay</td><td>$0,63M</td><td>5.688</td><td>$0,93M</td><td>6,0x / 73%</td></tr>
        <tr><td><strong>Baz</strong></td><td>6. ay</td><td>57. ay</td><td>$1,13M</td><td>9.510</td><td>$1,55M</td><td>5,5x / 74%</td></tr>
        <tr><td>İyimser</td><td>5. ay</td><td>34. ay</td><td>$0,64M</td><td>20.486</td><td>$4,33M</td><td>42,7x / 171%</td></tr>
      </tbody></table></div>
      <p style="max-width:80ch"><strong>Karar: Koşullu GO.</strong> Belirsiz üç girdi — ödeme isteği, benimseme, edinme hızı — 90 günlük doğrulama sprintiyle sahadan ölçülür (20 görüşme → 5 LOI → 3 pilot); 24. ayda büyüt/kapat kapısı. Ayrıntı: <a href="#d/docs/01-strateji/01-fizibilite.html">fizibilite raporu</a>, <a href="#d/docs/01-strateji/fizibilite-modeli/model.py">model.py</a>.</p>
    </section>

    <section class="blk" id="hazirlik">
      <div class="eyebrow">Hazırlıklar</div>
      <h2>Kodlamaya başlamadan önce geliştirme ekibinin ihtiyaç duyacağı her şey</h2>
      <p style="max-width:80ch">Strateji, kapsam, analiz, gereksinim, ekran, test ve geliştirme hazırlığı tek depoda ve izlenebilir: <code>CAP → UC → FR → SCR → TC → ST</code>. Her FR en az bir UC'ye, her TC en az bir FR'ye bağlı; kimlikler kalıcı, ertelenen satırlar <em>v1.1</em> etiketiyle yerinde.</p>
      {{STATS}}
      <h3 style="margin-top:28px">Fazlar ve durum</h3>
      {{PHASES}}
      <h3 style="margin-top:28px">Karar haritası</h3>
      {{DECISIONS}}
      <h3 style="margin-top:28px" id="belgeler">Belge haritası</h3>
      <p class="mut small">Belgeye tıklayınca bu sayfada açılır; “canlı sayfa” bağlantıları telefonda da çalışan yayınlanmış sürümlerdir.</p>
      {{CARDS}}
    </section>

    <section class="blk" id="acik">
      <div class="eyebrow">Açık konular</div>
      <h2>Sahadan gelecek kararlar, kapılar ve bekleyen işler</h2>
      <h3 style="margin-top:20px">Pilot görüşmelerinden beslenecek ürün kararları</h3>
      {{OPEN}}
      <h3 style="margin-top:28px">Doğrulama kapıları</h3>
      {{GATES}}
      <h3 style="margin-top:28px">Sizin tarafınızda bekleyenler</h3>
      <p class="mut small">İşaretler yalnızca bu tarayıcıda saklanır.</p>
      <ul class="todo" id="todo">
        <li><input type="checkbox" id="t1"><label for="t1">Hedef listeyi onayla; kendi işlettiğin veya tanıdık olduğun zincirleri “sıcak ulaşım” olarak ekle<span class="why">01-hedef-liste “Eksik profil” — ilk 5 mesaj bu hafta</span></label></li>
        <li><input type="checkbox" id="t2"><label for="t2">İlk 30 ulaşım mesajını gönder (T1 tanıştırma / T3 ana mesaj)<span class="why">Hafta 0 hedefi; 1. hafta 40 ulaşım, 5 randevu</span></label></li>
        <li><input type="checkbox" id="t3"><label for="t3">Alan adlarını kaydet: talimatname.com / .com.tr / .app (+ yedek yaplutfen, tamamlist, tembihle)<span class="why">12 Eylül'de 4/4 boştu; durum günlük değişir</span></label></li>
        <li><input type="checkbox" id="t4"><label for="t4">TÜRKPATENT 9 / 35 / 42 sınıflarında “talimatname” sorgusu; temizse kelime + şekil başvurusu<span class="why">Çevrimiçi sorgu oturum istiyor — kullanıcı yapar</span></label></li>
        <li><input type="checkbox" id="t5"><label for="t5">Sosyal hesap adları: @talimatname (Instagram, LinkedIn, X)</label></li>
        <li><input type="checkbox" id="t6"><label for="t6">Hukuk incelemesi: LOI 7. maddesi + aydınlatma metni ve veri işleme sözleşmesi taslakları (sekiz soru hazır)<span class="why">04-gereksinimler/hukuki — pilot kurulumundan (7. hafta) önce; ~2 saat avukat</span></label></li>
        <li><input type="checkbox" id="t7"><label for="t7">Blok 8 prototipini telefonda baştan sona dene (PIN → liste → aralık dışı → yapılamadı → gönder → sabah özeti)</label></li>
        <li><input type="checkbox" id="t8"><label for="t8">İkinci görüşmeci / not tutan kişiyi belirle<span class="why">Sprint planı roller; yoksa izinle kayıt + aynı gün not</span></label></li>
        <li><input type="checkbox" id="t9"><label for="t9">İlanı yayınla (LinkedIn, topluluklar, tanıdık tavsiyesi) ve 25–30 Eylül görüşmelerini planla<span class="why">07-gelistirme/07 + ilan/ PDF; mini görev ücreti bütçesi ₺3–5 bin × 3–4 aday; Sprint 0 hedefi 5 Ekim</span></label></li>
        <li><input type="checkbox" id="t10"><label for="t10">Gün 0 hazırlığı: GitHub organizasyonu ve depolar, Projects panosu, sözleşme + NDA, sağlayıcı hesapları (Apple/Google mağaza başvuruları erken), alan adı<span class="why">06-ilk-gun-paketi "Gün 0" listesi</span></label></li>
      </ul>
      <h3 style="margin-top:28px">Henüz başlamadı</h3>
      <ul style="max-width:80ch">
        <li><strong>Hukuki metinler:</strong> aydınlatma metni, veri işleme sözleşmesi (pilot öncesi; KVKK ve güvenlik belgesi §aydınlatma).</li>
        <li><strong>8 şablonun içeriği:</strong> kapanış, açılış, saatlik tuvalet/hijyen, soğuk zincir, haftalık derin temizlik, yağ değişimi, kasa devri, teslimat kabul — pilot zincirlerle uyarlanacak.</li>
        <li><strong>F8 hi-fi ekranlar</strong> (Sprint 4'e kadar) ve <strong>F9 Sprint 0</strong>: kod depoları, CI, ortamlar, tasarım token'ları kodda.</li>
        <li><strong>Fizibilite girdilerinin sahadan güncellenmesi:</strong> ARPU (₺730), benimseme, CAC — K2 sonrası model yeniden koşulur.</li>
        <li><strong>Kesin isim ADR'si</strong> (9–12. hafta) ve marka başvurusu.</li>
      </ul>
      <h3 style="margin-top:28px">Sprint riskleri</h3>
      {{RISKS}}
    </section>

    <div class="stamp">Talimatname · ürün dosyası · üretim {{DATE}} · commit {{COMMIT}} · {{NDOC}} belge · <a href="{{GH}}/blob/main/build_index.py" target="_blank" rel="noopener">build_index.py</a></div>
    <p class="foot">Bu sayfa depodaki belgelerden üretilir; belgeler değişince <code>python build_index.py</code> ile yenilenir. Kaynak: <a href="{{GH}}" target="_blank" rel="noopener">github.com/salihunsal-ux/Talimatname</a>.</p>
  </section>

  <section id="doc" hidden>
    <div class="dochead" id="dochead"></div>
    <article id="docbody" class="prose"></article>
    <nav class="pn" id="pn"></nav>
  </section>
</main>
</div>

<script id="docs" type="application/json">{{DOCS}}</script>
<script>
(function(){
  var DATA = JSON.parse(document.getElementById('docs').textContent);
  var DOCS = DATA.d, ORDER = DATA.o;
  var app = document.getElementById('app'), home = document.getElementById('home'), doc = document.getElementById('doc');
  var head = document.getElementById('dochead'), body = document.getElementById('docbody'), pn = document.getElementById('pn'), crumb = document.getElementById('crumb');
  var esc = function(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };

  function isDark(){ var t = document.documentElement.getAttribute('data-theme'); if(t) return t === 'dark'; return matchMedia('(prefers-color-scheme: dark)').matches; }
  function ensureMermaid(cb){
    if(window.mermaid){ cb(); return; }
    var s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.1/mermaid.min.js';
    s.onload = function(){ window.mermaid.initialize({ startOnLoad:false, theme: isDark() ? 'dark' : 'neutral', securityLevel:'loose' }); cb(); };
    document.head.appendChild(s);
  }
  var seq = 0;
  function renderDiagrams(root){
    var els = root.querySelectorAll('.mmd:not([data-done])');
    if(!els.length) return;
    ensureMermaid(function(){
      Array.prototype.forEach.call(els, function(el){
        var src = el.querySelector('.mmd-src').textContent;
        el.setAttribute('data-done', '1');
        window.mermaid.render('mmd' + (++seq), src).then(function(r){ el.innerHTML = r.svg; }).catch(function(){});
      });
    });
  }

  function setActive(key){
    var nls = document.querySelectorAll('.nl');
    for(var i=0;i<nls.length;i++){ var a = nls[i]; var on = a.dataset.p ? a.dataset.p === key : (a.dataset.h !== undefined && a.dataset.h === key); a.classList.toggle('on', on); }
  }
  function closeNav(){ app.classList.remove('open'); }

  function showHome(id){
    doc.hidden = true; home.hidden = false;
    crumb.innerHTML = '<b>Genel bakış</b>' + (id ? ' › ' + esc({urun:'Ürün',hazirlik:'Hazırlıklar',acik:'Açık konular'}[id] || id) : '');
    document.title = 'Talimatname Ürün Dosyası';
    setActive(id || '');
    var el = id && document.getElementById(id);
    if(el) el.scrollIntoView(); else window.scrollTo(0,0);
    closeNav();
  }
  function showDoc(p, slug){
    var e = DOCS[p]; if(!e){ showHome(''); return; }
    home.hidden = true; doc.hidden = false;
    var acts = '';
    if(e.live) acts += '<a class="btn" href="' + esc(e.live) + '" target="_blank" rel="noopener">Canlı sayfa ↗</a>';
    if(e.k === 'html') acts += '<a class="btn" href="' + esc(p) + '" target="_blank" rel="noopener">Yeni sekmede aç ↗</a>';
    acts += '<a class="btn" href="' + esc(e.gh) + '" target="_blank" rel="noopener">GitHub\'da aç ↗</a>';
    var tags = (e.tags||[]).map(function(t){ return '<span class="tag">' + esc(t) + '</span>'; }).join('');
    head.innerHTML = '<div class="eyebrow">' + esc(e.g) + '</div><h1>' + esc(e.t) + '</h1><p class="desc">' + esc(e.d) + '</p><div class="acts">' + acts + tags + '</div>';
    if(e.k === 'html'){
      body.innerHTML = '<iframe class="frame" src="' + esc(p) + '" title="' + esc(e.t) + '" loading="lazy"></iframe>';
    } else if(e.k === 'link'){
      body.innerHTML = '<p>Bu dosya sayfaya gömülmez. <a class="btn" href="' + esc(p) + '" target="_blank" rel="noopener">Dosyayı aç ↗</a> <a class="btn" href="' + esc(e.gh) + '" target="_blank" rel="noopener">GitHub\'da aç ↗</a></p><p class="mut small">Depodaki yol: <code>' + esc(p) + '</code></p>';
    } else {
      body.innerHTML = e.h;
    }
    var i = ORDER.indexOf(p), prev = i > 0 ? ORDER[i-1] : null, next = i < ORDER.length-1 ? ORDER[i+1] : null;
    pn.innerHTML = (prev ? '<a href="#d/' + esc(prev) + '"><span class="lab">Önceki</span>' + esc(DOCS[prev].t) + '</a>' : '<span></span>') +
                   (next ? '<a class="r" href="#d/' + esc(next) + '"><span class="lab">Sonraki</span>' + esc(DOCS[next].t) + '</a>' : '');
    crumb.innerHTML = '<a href="#">Genel bakış</a> › ' + esc(e.g) + ' › <b>' + esc(e.t) + '</b>';
    document.title = e.t + ' · Talimatname';
    setActive(p);
    var target = slug && document.getElementById('h-' + slug);
    if(target) target.scrollIntoView(); else window.scrollTo(0,0);
    renderDiagrams(body);
    closeNav();
    var on = document.querySelector('.nl.on'); if(on && on.scrollIntoView) { try { on.scrollIntoView({block:'nearest'}); } catch(err){} }
  }
  function route(){
    var h = location.hash || '';
    try { h = decodeURIComponent(h); } catch(err){}
    if(h.indexOf('#d/') === 0){ var rest = h.slice(3), at = rest.indexOf('@'); var p = at >= 0 ? rest.slice(0, at) : rest, slug = at >= 0 ? rest.slice(at+1) : ''; if(DOCS[p]){ showDoc(p, slug); return; } }
    showHome(h.slice(1));
  }
  window.addEventListener('hashchange', route);
  route();

  // menü
  document.getElementById('menu').addEventListener('click', function(){ app.classList.toggle('open'); });
  document.getElementById('backdrop').addEventListener('click', closeNav);
  document.addEventListener('keydown', function(ev){ if(ev.key === 'Escape') closeNav(); });

  // arama
  var q = document.getElementById('q'), qn = document.getElementById('qn');
  q.addEventListener('input', function(){
    var s = q.value.trim().toLowerCase(), n = 0, groups = document.querySelectorAll('#nav .grp');
    for(var i=0;i<groups.length;i++){
      var g = groups[i], vis = 0, links = g.querySelectorAll('.nl');
      for(var j=0;j<links.length;j++){
        var a = links[j], e = DOCS[a.dataset.p], hit = !s || ((e.t + ' ' + e.d + ' ' + a.dataset.p + ' ' + (e.h||'')).toLowerCase().indexOf(s) >= 0);
        a.classList.toggle('hid', !hit); if(hit){ vis++; n++; }
      }
      g.classList.toggle('hid', vis === 0);
    }
    qn.textContent = s ? n + ' belge eşleşti' : '';
  });

  // yapılacaklar (yalnızca bu tarayıcı)
  var KEY = 'talimatname-todo';
  var boxes = document.querySelectorAll('#todo input');
  var saved = {}; try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch(err){}
  for(var b=0;b<boxes.length;b++){ boxes[b].checked = !!saved[boxes[b].id]; boxes[b].addEventListener('change', function(){ var st = {}; for(var c=0;c<boxes.length;c++) st[boxes[c].id] = boxes[c].checked; try { localStorage.setItem(KEY, JSON.stringify(st)); } catch(err){} }); }
})();
</script>
"""

AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

def main():
    docs, groups = build_docs()
    commit, cdate = git_info()
    today = datetime.date.today()
    payload = json.dumps({"d": docs, "o": ORDER}, ensure_ascii=False).replace("</", "<\\/")
    ndoc = sum(1 for p in ORDER if docs[p]["k"] != "link")
    page = (TEMPLATE
            .replace("{{NAV}}", nav_html(groups, docs))
            .replace("{{CARDS}}", cards_html(groups, docs))
            .replace("{{STATS}}", stats_html(stats()))
            .replace("{{PHASES}}", phases_html())
            .replace("{{DECISIONS}}", decisions_html())
            .replace("{{OPEN}}", open_html())
            .replace("{{GATES}}", gates_html())
            .replace("{{RISKS}}", risks_html())
            .replace("{{DOCS}}", payload)
            .replace("{{DATE_TR}}", f"{today.day} {AYLAR[today.month-1]} {today.year}")
            .replace("{{DATE}}", today.isoformat())
            .replace("{{COMMIT}}", commit)
            .replace("{{NDOC}}", str(ndoc))
            .replace("{{GH}}", GH))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"{OUT}: {len(page)/1024:.0f} KB, {ndoc} belge, commit {commit}")

if __name__ == "__main__":
    main()
