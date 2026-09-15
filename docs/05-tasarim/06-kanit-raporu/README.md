# Kanıt raporu örnekleri (basılı — görüşme kiti)

"Denetim kaydı 3 dakikada PDF" iddiasının elle tutulur hâli. Blok 8'de prototiple birlikte masaya konur; kalite sorumlusu (Deniz) ve operasyon müdürü (Selin) için. Veri **sentetiktir** (Kahve Durağı test zinciri, 06-test/03); her sayfada "ÖRNEK VERİ" filigranı vardır — gerçek kayıt gibi sunulmaz.

| Dosya | İçerik | Kapsam bağı |
|---|---|---|
| `01-calistirma-raporu.html` / `.pdf` (2 sayfa) | Tek çalıştırma: Kadıköy kapanışı, 13 Eylül 2026 — sonuç "başarısız (kritik madde)", puan %87, 15 madde, 4 kanıt fotoğrafı (damgalı), 2 aksiyon, olay izi, doğrulama kodu ve nasıl doğrulanır kutusu | R-6 çalıştırma PDF'i, U-1, ADR-0004; prototipteki senaryonun aynısı |
| `02-aylik-ozet.html` / `.pdf` (1 sayfa) | Ağustos 2026, 25 şube: zamanında %81, kaçırılan, başarısız, yapılamadı; haftalık eğilim, bölge ve şube kırılımı, en sık yapılamayan maddeler, kritik kaynakları, "bu ay dikkat" | E-7 aylık tek sayfa, E-5 sabah özeti |
| `03-sicaklik-gunlugu.html` / `.pdf` (1 sayfa) | Kadıköy 1–14 Eylül, 4 ekipman × 3 ölçüm/gün: tablo, aralık dışı işaretleri, mini grafik, olaylar, denetçi notu | R-4 sıcaklık günlüğü, şablon 4 |

Tasarım kuralları 04-tasarim-sistemi.md "PDF çıktıları" bölümünden: markalı başlık (zincir + "Talimatname ile oluşturuldu"), her sayfada doğrulama kodu ve üretim zamanı, kanıt küçük resimleri ızgarada, sıcaklık günlüğü tablo + mini grafik, siyah-beyaz baskıda durumlar ikonla okunur.

Üretim: `python build_reports.py` (HTML) · `python build_reports.py --pdf` (Edge/Chrome headless ile PDF; Edge süreç döndükten birkaç saniye sonra yazar, betik bekler). Tarayıcıdan yazdırırken A4, kenar boşlukları varsayılan, arka plan grafikleri açık.

Görüşmede sorulacak: "Bunu denetçiye verir miydiniz? Eksik ne?" — cevaplar 01-strateji/gorusmeler notlarına, gerekli değişiklikler bu klasöre ve FR-12xx/13xx'e işlenir.
