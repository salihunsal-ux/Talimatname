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
| F7 · Doğrulama sprinti (saha) | 20 görüşme, 8 şube ziyareti, isim testi, 5 LOI | Görüşme notları (01-strateji/gorusmeler/), karar güncellemeleri, ADR | ⏳ Başlamadı — 12 hafta |
| F8 · Hi-fi tasarım ve prototip | Tel-çerçevelerin Talimatname tasarım sistemiyle yüksek doğruluklu sürümü; Blok 8 tıklanabilir prototip | 05-tasarim/05-prototip | ⏳ F7 ile paralel, 2–3 hafta |
| F9 · Sprint 0 | Repo'lar, CI, ortamlar, tasarım token'ları kodda, örnek veri, ilk hikâyeler hazır | Kod depoları | ⏳ F8 sonrası, 2 hafta |

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
