# Kodlama hazırlık indeksi

Bir geliştiricinin ilk hafta okuması gereken belgeler, sırayla; ardından "hazır mıyız?" kontrol listesi. Toplam okuma ~4 saat.

## Okuma sırası

| Sıra | Belge | Neden | Süre |
|---|---|---|---|
| 1 | [Ürün merkezi](../00-urun-merkezi.md) | Ürün özeti, karar haritası, kimlik şeması | 10 dk |
| 2 | [Vizyon ve konumlanma](../02-urun/01-urun-vizyonu-ve-konumlanma.md) · [Personalar](../02-urun/02-personalar.md) | Kim için, neyi çözüyor; personel ekranı neden 3 ekran | 20 dk |
| 3 | [Yetenek haritası](../02-urun/04-yetenek-haritasi.md) | Modüller ve öncelikler (M/S/C) | 10 dk |
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
- [x] Kapsam ve yetenekler (CAP-01…19) tanımlı, öncelikli
- [x] 14 aktör, 20 use case (ana/alternatif/istisna akışlarıyla), 8 uçtan uca senaryo
- [x] ~140 fonksiyonel gereksinim, 16 NFR, 25 iş kuralı (parametre tablosuyla)
- [x] Veri modeli (ER + alanlar + enum'lar), API taslağı (uç noktalar + senk sözleşmesi + olay sözlüğü)
- [x] 24 ekran (11 mobil, 13 web) envanteri, tel-çerçeveler, navigasyon haritası, tasarım token'ları
- [x] 112 kabul testi (UC/FR/BR bağlı, otomasyon düzeyi), test stratejisi, test verisi, cihaz matrisi, UAT planı
- [x] Mimari, depolar/CI/ortamlar, 138 hikâyelik 12 sprint planı, DoR/DoD, 7 ADR
- [ ] Hi-fi tasarım (F8) — tel-çerçeve yeterli, Sprint 4'e kadar hi-fi gerekli (kamera ve madde bileşenleri)
- [ ] Hukuki metinler (aydınlatma, veri işleme sözleşmesi) — avukat; Beta'ya kadar
- [ ] 30 şablon içeriği (ST-102) — PO + kalite danışmanı; Sprint 9'a kadar

### Kararlar (pilot görüşmelerinden beklenen)
- [ ] Kiosk modu Must kalıyor mu (tablet oranı)
- [ ] Barındırma: TR bulut vs AB + standart sözleşme
- [ ] Franchise sahibi rolü
- [ ] Sıcaklık probu (Could → Should?)
- [ ] Kesin marka adı

### Sprint 0 (02-repo kontrol listesi)
- [ ] Depolar, CI, dev compose, staging (TR), sağlayıcı hesapları, token'lar kodda, tohum v0, spesifikasyon fikstürleri, backlog aracı

## Sık sorulan geliştirici soruları

- **Kural motoru nerede yaşar?** Backend `templates.rules` ve mobil `rules/` aynı JSON spesifikasyonunu geçer; fikstürler `talimatname-api/spec/` altında (Sprint 0). Kural değişikliği = fikstür değişikliği + iki uygulama.
- **Zaman nasıl tutulur?** UTC saklanır; şube saat dilimi çalıştırmada; iş günü = pencere başlangıç tarihi (BR-01). Cihaz saati güvenilmez (BR-13).
- **Kanıt neden iki kopya?** Ham (bütünlük, hash) + damgalı (insan okunur). ADR-0004.
- **Silme var mı?** Yok; durum/maskeleme. Yalnızca nesne depodaki dosya saklama/KVKK ile silinir (BR-21, BR-22).
- **Kişi skoru?** Yok, ADR-0007; kişi düzeyi yalnızca gecikme/eksik listesi.
- **WhatsApp?** MVP dışı; bildirim servisi kanal-bağımsız (ADR-0006).
