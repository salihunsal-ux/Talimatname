# Test verisi ve ortam

## Sentetik zincir: Kahve Durağı

Tüm test seviyeleri ve UAT aynı sentetik veri setini kullanır; gerçek müşteri verisi test ortamlarına kopyalanmaz. Set, tohum (seed) betiğiyle üretilir (`seed/kahve_duragi.py`, kod deposunda) ve deterministiktir (sabit rastgele tohum) — aynı veri her ortamda.

| Nesne | Adet | Not |
|---|---|---|
| Hesap | 1 (+1 yalıtım testi için ikinci hesap "Simit Evi") | Ayarlar varsayılan; saklama 24 ay |
| Bölge | 3 (Anadolu 12, Avrupa 9, Ege 4) | |
| Şube | 25 | Saat dilimi 24 × Europe/Istanbul + 1 × Europe/Berlin (DST testi); 2 şube pazar kapalı; çalışma saatleri çeşitli (09–24, 08–23, 10–22) |
| İstasyon | 100 (şube başına 4: bar, mutfak, kasa, tuvalet) | Her birinin QR'ı |
| Kullanıcı | 412: 1 hesap yöneticisi, 1 operasyon müdürü, 1 kalite, 3 bölge müdürü, 25 şube müdürü, 380 personel, 1 gözlemci | Telefonlar sahte (+90 500 …); 10 kullanıcı pasif, 3 maskeli, 18 davet bekliyor |
| Cihaz | 25 kiosk tablet + 60 kişisel telefon | Push token'ları sahte sağlayıcıya bağlı |
| Şablon | 6: Kapanış (kafe), Açılış, Saatlik hijyen, Soğuk zincir, Haftalık derin temizlik, Alerjen kontrolü | Kapanış v1 ve v2 (sürümleme testleri); 11 madde türünün tamamı en az bir şablonda |
| Plan | 8 | Günlük (gece yarısı aşan), saatlik, haftalık (herkes tamamlasın), aylık, tek seferlik; biri DST şubesinde |
| Çalıştırma | ~30 gün geçmiş (~5.500) + 7 gün gelecek | Durum dağılımı: %80 tamamlandı, %8 geç, %5 kaçırıldı, %2 yapılmayacak, %5 kapalı; %6 başarısız |
| Cevap ve kanıt | ~60.000 cevap, ~18.000 sentetik fotoğraf (renkli düz kare + metin), damgalı kopyalar | Bayraklar: %3 galeri, %2 uzak, %5 konum yok, %1 saat farkı |
| Aksiyon | ~900 (kritik/yüksek/orta/düşük; açık, devam, kapalı, reddedildi, gecikmiş) | Kaynak dağılımı: madde %60, yapılamadı %25, sorun %10, kaçırma %5 |
| Duyuru | 4 (biri imza zorunlu; onay oranları %40–96) | |
| Olay günlüğü | Yukarıdakilerin tamamı, hash zinciri tutarlı; bir "kırık zincir" fikstürü ayrı | TC-101 |

Kişi adları ve fotoğraflar gerçek kişi içermez; şube adları semt adlarıdır.

## Ortamlar

| Ortam | Amaç | Sağlayıcılar | Veri | Erişim |
|---|---|---|---|---|
| dev | Geliştirici makinesi (docker compose: PostgreSQL, Redis, MinIO, sahte SMS/push/TSA) | Sahte | Tohum | Geliştirici |
| test | CI: her PR'da birim/sözleşme/entegrasyon; gece E2E | Sahte | Tohum | CI |
| staging | Üretim benzeri; pilot UAT; performans testi | Gerçek test hesapları (SMS, push, TSA test uç noktası) | Tohum + pilot zincir verisi (pilot sözleşmesiyle) | Ekip + pilot kullanıcıları |
| prod | Üretim | Gerçek | Gerçek | Müşteriler |

Staging'de "zaman ilerlet" yönetici aracı: zamanlayıcı testleri için sunucu saatini ileri alır (yalnızca staging; prod'da derlenmez).

## Sahte sağlayıcılar (test ve dev)

- SMS: gönderilen mesajları listeleyen sahte uç nokta; OTP kodları test API'siyle okunur.
- Push: token doğrulama simülasyonu (geçersiz token senaryosu için "bad_token" ön eki).
- TSA (RFC 3161): imza üreten yerel sahte servis.
- Nesne depo: MinIO (S3 uyumlu).

## Cihaz laboratuvarı

Fiziksel cihazlar (04-cihaz-matrisi) ekip ofisinde; bulut cihaz çiftliği (Firebase Test Lab / BrowserStack) gece koşuları için. Kiosk tabletleri gerçek şube koşullarını taklit eden standda (yatay, kılıf, %50 parlaklık).

## Test verisi yönetimi

- Tohum betiği sürümlenir; şema değişince güncellenir (DoD).
- Fikstürler (belirli TC'ler için küçük setler) `tests/fixtures/` altında; büyük set yalnızca staging ve gece koşusunda.
- Kişisel veri içermediği için ortamlar arası kopyalanabilir; yine de prod'a asla yüklenmez.
