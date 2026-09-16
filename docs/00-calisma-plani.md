# Çalışma planı — iş analizi ve ürün sahipliği

Amaç: kodlamaya başlamadan önce bir geliştirme ekibinin ihtiyaç duyacağı her şeyin (kapsam, aktör/use case, senaryo, gereksinim, ekran, test, teknik hazırlık) tek depoda, izlenebilir ve güncel tutulması. Plan iki ana hatta ilerler: **doğrulama** (pilot görüşmeleri, sahadan gelen kararlar) ve **hazırlık** (geliştirme paketi). İkisi paralel yürür; sahadan gelen her karar ilgili belgeyi ve ADR'yi günceller.

## Fazlar ve teslimatlar

| Faz | İçerik | Teslimatlar | Durum |
|---|---|---|---|
| F0 · Depo ve plan | Klasör yapısı, ürün merkezi, çalışma planı, mevcut çıktıların taşınması, ADR'ler | README, 00-urun-merkezi, 00-calisma-plani, adr/0001–0007, 01-strateji/* | ✅ Tamamlandı |
| F1 · Ürün tanımı | Vizyon ve konumlanma, personalar, yetenek haritası (CAP) | 02-urun/01, 02, 04 (+03 kapsam taşındı) | ✅ Tamamlandı |
| F2 · Analiz | Aktörler, use case kataloğu ve detayları, uçtan uca senaryolar | 03-analiz/01–04 | ✅ Tamamlandı |
| F3 · Gereksinimler | Fonksiyonel (FR), fonksiyonel olmayan (NFR), iş kuralları (BR), veri modeli, API taslağı, KVKK/güvenlik | 04-gereksinimler/01–06 | ✅ Tamamlandı |
| F4 · Tasarım | Ekran envanteri ve navigasyon haritası, mobil ve web tel-çerçeveler, tasarım sistemi | 05-tasarim/01–04 | ✅ Tamamlandı |
| F5 · Test hazırlığı | Test stratejisi, kabul test senaryoları (TC), test verisi ve ortam, cihaz matrisi, pilot UAT planı | 06-test/01–05 | ✅ Tamamlandı |
| F6 · Geliştirme hazırlığı | Kodlama hazırlık indeksi, teknik mimari, repo/ortam kurulumu, backlog ve sprint planı, DoR/DoD | 07-gelistirme/00–04 | ✅ Tamamlandı |
| F6b · v1 çekirdek yeniden çizimi | Aktör gözüyle gözden geçirme (02-urun/05) onaylanınca kapsam, FR, UC, ekran, TC ve backlog'un çekirdeğe göre yeniden çizilmesi (ID'ler korunur, ertelenenler v1.1 etiketi) | Güncellenmiş belgeler, ADR-0008, 02-urun/06 | ✅ Tamamlandı (13 Eylül 2026) |
| F7 · Doğrulama sprinti (saha) | 20 görüşme, 8 şube ziyareti, isim testi, 5 LOI — kit: 01-strateji/dogrulama-sprinti/ (plan, hedef liste, ulaşım, not şablonu + puanla.py, LOI, gözlem, rapor), prototip 05-tasarim/05-prototip | Görüşme notları (01-strateji/gorusmeler/), 00-ozet.md, haftalık raporlar, karar güncellemeleri, ADR | 🟡 Kit hazır (14 Eylül 2026) — hafta 0 |
| F8 · Hi-fi tasarım ve prototip | Tel-çerçevelerin Talimatname tasarım sistemiyle yüksek doğruluklu sürümü; Blok 8 tıklanabilir prototip (✅), yönetici web prototipi (✅), basılı kanıt raporu örnekleri (✅), 8 şablon içeriği (✅ taslak), tanıtım broşürü + 4 hi-fi ekran (✅) | 05-tasarim/05-prototip, 06-kanit-raporu, 07-brosur, 02-urun/07 | 🟡 Görüşme kiti tamam; kalan hi-fi ekranlar (kamera, madde bileşenleri) Sprint 4'e kadar |
| F9 · Sprint 0 | Repo'lar, CI, ortamlar, tasarım token'ları kodda, örnek veri, ilk hikâyeler hazır; dört teknik spike (07-gelistirme/05) | Kod depoları, spike sonuçları → ADR notları | 🟡 Ekip kararı A (ADR-0009); ilan ve seçim kiti hazır (07-gelistirme/07, ilan/), ilk gün paketi hazır (06); hedef başlangıç **5 Ekim** |

## Çalışma kuralları

- **Tek kaynak:** bir bilgi tek belgede yaşar, diğerleri ona bağlanır. Kapsam tablosu (02-urun/03) kaynak; FR'ler ondan türer; ekranlar FR'ye, testler FR ve UC'ye bağlanır.
- **ID'ler kalıcıdır.** Silinen madde "İptal" işaretlenir; numara yeniden kullanılmaz.
- **Her saha bulgusu bir yere düşer:** belge güncellemesi + gerekiyorsa ADR. "Konuştuk ama yazmadık" yok.
- **Commit disiplini:** her faz veya anlamlı iş paketi ayrı commit; mesaj Türkçe, ne değiştiğini söyler.
- **Belge biçimi:** Markdown (GitHub'da doğrudan okunur, mermaid diyagramları çizilir); ekranlar ve raporlar HTML (tarayıcıda açılır, bağımsız).

## Sıradaki üç iş

1. Uzak depo: GitHub'da `Talimatname` (özel) oluşturup `git push` (kullanıcı kimlik doğrulamasıyla; bkz. README).
2. Doğrulama sprinti takvimi: 20 zincirin listesi ve ilk 5 görüşmenin randevusu (01-strateji/02 rehberi §03 örneklem karışımı).
3. Alan adı ve marka: talimatname.com / .com.tr / .app kaydı; TÜRKPATENT 9/35/42 sorgusu.
