# Kodlama hazırlık indeksi

Bir geliştiricinin ilk hafta okuması gereken belgeler, sırayla; ardından "hazır mıyız?" kontrol listesi. Toplam okuma ~4 saat.

## Okuma sırası

| Sıra | Belge | Neden | Süre |
|---|---|---|---|
| 1 | [Ürün merkezi](../00-urun-merkezi.md) | Ürün özeti, karar haritası, kimlik şeması | 10 dk |
| 2 | [Vizyon ve konumlanma](../02-urun/01-urun-vizyonu-ve-konumlanma.md) · [Personalar](../02-urun/02-personalar.md) | Kim için, neyi çözüyor; personel ekranı neden 3 ekran | 20 dk |
| 3 | [v1 çekirdek kapsamı](../02-urun/06-v1-cekirdek-kapsam.md) · [Yetenek haritası](../02-urun/04-yetenek-haritasi.md) | Neyin v1, neyin v1.1 olduğu; sabitler tablosu | 15 dk |
| 4 | [Use case detayları](../03-analiz/03-usecase-detaylari.md) · [Senaryolar](../03-analiz/04-senaryolar.md) | Akışlar adım adım; "Kahve Durağı" örnek zinciri | 45 dk |
| 5 | [İş kuralları](../04-gereksinimler/03-is-kurallari.md) | Kodun tek referansı: pencere, tolerans, puan, eskalasyon, kanıt | 25 dk |
| 6 | [Fonksiyonel gereksinimler](../04-gereksinimler/01-fonksiyonel-gereksinimler.md) | FR tablosu (hikâyelerin bağlandığı yer) | 40 dk (tarama) |
| 7 | [Veri modeli](../04-gereksinimler/04-veri-modeli.md) · [API taslağı](../04-gereksinimler/05-api-taslagi.md) | Varlıklar, enum'lar, uç noktalar, senk sözleşmesi | 30 dk |
| 8 | [ADR'ler](../adr) | Neden Flutter/FastAPI, TR barındırma, hash zinciri, RRULE, WhatsApp yok, kişi skoru yok | 20 dk |
| 9 | [Teknik mimari](01-teknik-mimari.md) · [Repo ve ortam](02-repo-ve-ortam-kurulumu.md) | Bileşenler, arka plan işleri, depolar, CI, Sprint 0 | 30 dk |
| 10 | [Ekran envanteri](../05-tasarim/01-ekran-envanteri-ve-navigasyon.md) · [Mobil](../05-tasarim/02-mobil-ekranlar.html) · [Web](../05-tasarim/03-web-ekranlar.html) · [Tasarım sistemi](../05-tasarim/04-tasarim-sistemi.md) | Ekranlar ve FR bağları; token'lar | 30 dk |
| 11 | [Fonksiyonel olmayan](../04-gereksinimler/02-fonksiyonel-olmayan.md) · [KVKK ve güvenlik](../04-gereksinimler/06-kvkk-ve-guvenlik.md) | Eşikler, yetki matrisi, veri envanteri | 20 dk |
| 12 | [Test stratejisi](../06-test/01-test-stratejisi.md) · [Kabul testleri](../06-test/02-kabul-test-senaryolari.md) · [Test verisi](../06-test/03-test-verisi-ve-ortam.md) | Neyin nasıl test edileceği; tohum seti | 30 dk |
| 13 | [Backlog ve sprint planı](03-backlog-ve-sprint-plani.md) · [DoR/DoD](04-tanimlar-dor-dod.md) | İlk sprint hikâyeleri ve çalışma kuralları | 20 dk |

## Hazırlık kontrol listesi

### Belge tamlığı (BA/PO)
- [x] v1 çekirdek kapsamı (ADR-0008): 43 satır v1, 27 v1.1, 6 v2; sabitler tablosu; yetenek haritası
- [x] 14 aktör, 20 use case (ana/alternatif/istisna akışlarıyla), 8 uçtan uca senaryo
- [x] 173 fonksiyonel gereksinim (123 v1, 50 v1.1), 16 NFR, 27 iş kuralı (v1 sabit parametre tablosuyla)
- [x] Veri modeli (ER + alanlar + enum'lar), API taslağı (uç noktalar + senk sözleşmesi + olay sözlüğü)
- [x] 26 ekran envanteri (v1: 10 mobil + 13 web), 21 tel-çerçeve v1'e göre güncellendi (SCR-W-14 belge takvimi hi-fi aşamasında çizilecek), navigasyon haritası, tasarım token'ları
- [x] 125 kabul testi (102 v1, 23 v1.1), test stratejisi, test verisi, cihaz matrisi, UAT planı
- [x] Mimari, depolar/CI/ortamlar, v1 sprint planı (GA 10. sprint + 2 tampon), DoR/DoD, 11 ADR
- [ ] Hi-fi tasarım (F8) — tel-çerçeve yeterli, Sprint 4'e kadar hi-fi gerekli (kamera ve madde bileşenleri)
- [ ] Hukuki metinler (aydınlatma, veri işleme sözleşmesi) — taslaklar hazır (04-gereksinimler/hukuki), avukat incelemesi pilot öncesi
- [x] 8 şablon içeriği (ST-102) — taslak hazır (02-urun/07), sahada doğrulanır; Sprint 9'a kadar kesinleşir

### Kararlar (pilot görüşmelerinden beklenen)
- [ ] Kiosk modu Must kalıyor mu (tablet oranı)
- [ ] Barındırma: TR bulut vs AB + standart sözleşme
- [ ] Franchise sahibi rolü
- [ ] Sıcaklık probu (Could → Should?)
- [ ] Kesin marka adı

### Sprint 0 (02-repo kontrol listesi)
- [ ] Depolar, CI, dev compose, staging (TR), sağlayıcı hesapları, token'lar kodda, tohum v0, spesifikasyon fikstürleri, backlog aracı

## Sık sorulan geliştirici soruları

- **Kural motoru nerede yaşar?** v1'de kural sabittir (FR-0405): backend ve mobil aynı JSON spesifikasyon fikstürlerini (`talimatname-api/spec/`, Sprint 0) geçer; kural editörü v1.1'de bu motorun üstüne gelir.
- **v1'de ne yok?** Duyuru, koşul editörü, ağırlıklı puan, herkes-tamamlasın, ek kayıt, aksiyon yorum/onay akışı, eskalasyon editörü, gruplar, ayarlar paneli, 2FA, denetim izi ekranı, TSA, KVKK ekranı, Excel/paylaşım, raporların çoğu, video/imza/barkod/tarih-saat, QR, AI taslak — tam liste 02-urun/06.
- **Zaman nasıl tutulur?** UTC saklanır; şube saat dilimi çalıştırmada; iş günü = pencere başlangıç tarihi (BR-01). Cihaz saati güvenilmez (BR-13).
- **Kanıt neden iki kopya?** Ham (bütünlük, hash) + damgalı (insan okunur). ADR-0004.
- **Silme var mı?** Yok; durum/maskeleme. Yalnızca nesne depodaki dosya saklama/KVKK ile silinir (BR-21, BR-22).
- **Kişi skoru?** Yok, ADR-0007; kişi düzeyi yalnızca gecikme/eksik listesi.
- **WhatsApp?** MVP dışı; bildirim servisi kanal-bağımsız (ADR-0006).

## Sprint 0 için ek

- [06-ilk-gun-paketi.md](06-ilk-gun-paketi.md) — geliştiriciye gönderilecek ilk gün/ilk hafta paketi (gün 0 kurucu listesi, e-posta şablonu, hesaplar, ortam, okuma, spike, çalışma kuralları, ritim).
- [07-serbest-gelistirici-secimi.md](07-serbest-gelistirici-secimi.md) — ilan, görüşme soruları, ücretli mini görevler ve rubrik, sözleşme başlıkları; gönderilebilir ilan [ilan/](ilan/serbest-gelistirici-ilani.html).

- [05-sprint0-ve-teknik-spike.md](05-sprint0-ve-teknik-spike.md) — takvim (kritik yol), ekip seçenekleri, 2 haftalık Sprint 0 takvimi, dört teknik spike (çevrimdışı senk, RRULE pencere, kamera-damga-hash, push→SMS) ve DoD.
- [sablonlar/](sablonlar/) — kurulum sihirbazının içe aktarma dosyaları: `subeler.xlsx`, `personel.xlsx` (doğrulama kuralları "Açıklama" sayfasında; `build_sablonlar.py` üretir).

