# Test stratejisi

Amaç: ürünün değer önerisi "kanıt ve kayıt" olduğu için doğruluk (zaman, durum geçişleri, puan, eskalasyon) ve dayanıklılık (çevrimdışı, çakışma, düşük cihaz) en yüksek risklerdir; test yatırımı buraya yoğunlaşır. Test, geliştirmeyle aynı sprintte yazılır (DoD'un parçası, bkz. 07-gelistirme/04).

## Risk temelli önceliklendirme

| Risk alanı | Neden yüksek | Test yaklaşımı |
|---|---|---|
| Pencere/durum motoru (BR-01…04, FR-0513/0514) | Yanlış "kaçırıldı" = müşteri güveni; gece yarısı, saat dilimi, tolerans | Birim testleri (tablo güdümlü, 200+ vaka), zaman dondurma (frozen clock), saat dilimi matrisi |
| Puan ve kritik kuralı (BR-06…08) | Yanlış "başarısız" = yanlış eskalasyon | Birim + kabul; sınır değerleri (4,0 / 4,1) |
| Çevrimdışı senk ve çakışma (CAP-07, BR-13, BR-24) | Veri kaybı = ürün kaybı | Cihaz üstü otomasyon (uçak modu), idempotency ve çakışma özellik testleri, 100 tekrar dayanıklılık |
| Kanıt bütünlüğü (ADR-0004) | Denetimde çürütülürse değer sıfır | Hash doğrulama, zincir kırılma testi, damga doğrulama, galeri/kamera ayarı |
| Eskalasyon ve bildirim (BR-11, BR-23) | Gece bildirimi gitmezse kimse görmez | Zamanlayıcı testleri (zaman dondurma), teslimat izi doğrulama, SMS yedek senaryoları (sağlayıcı sahte servisi) |
| Yetki (FR-0205) | Kiracı/kapsam sızıntısı | Otomatik yatay/dikey yetki testleri her uç noktada; kiracı yalıtım testi |
| Düşük cihaz performansı (NFR-02/06) | Personel sabrı 1 sn | Cihaz matrisi üzerinde ölçüm; kamera → sonraki madde süresi |
| KVKK akışları (FR-1307…1311) | Hukuki | Kabul testleri + uyum kontrol listesi |

## Test seviyeleri

| Seviye | Kapsam | Araç | Hedef |
|---|---|---|---|
| Birim | Kural motoru (RRULE/pencere, durum makinesi, puan, koşullu mantık), senk çakışma, hash zinciri | pytest (backend), Flutter test, Vitest (web) | Kural kodunda ≥ %90 satır kapsamı; her BR için en az bir test |
| Sözleşme (API) | OpenAPI'ye uygunluk; istemci üretimi | Schemathesis / Dredd; üretilen istemci derlemesi CI'da | Her uç nokta |
| Entegrasyon | Veritabanı, kuyruk, nesne depo, bildirim (sahte sağlayıcılar) | Docker compose test ortamı | Kritik akışlar (UC-07, UC-08, UC-09, UC-13) |
| Uçtan uca (E2E) | Senaryolar S-01…S-08 | Web: Playwright; mobil: Patrol/integration_test (Flutter) | Her senaryo en az bir E2E; gece koşusu |
| Kabul (UAT) | TC-001…TC-112 | Elle + otomasyon; pilot zincirlerle UAT | GA öncesi %100 geçiş |
| Performans/yük | NFR-02/03/04 | k6 (API), cihaz ölçümü | Eşiklerin altında |
| Güvenlik | NFR-09 | ZAP/Burp, bağımlılık taraması, dış sızma testi | Kritik/yüksek bulgu sıfır |
| Erişilebilirlik | NFR-11 | Flutter semantics denetimi, axe (web), elle kontrol | Kontrol listesi |
| Kurtarma | NFR-13 | Yedekten geri yükleme tatbikatı | Yılda 2 |

## Ortamlar

`dev` (geliştirici, docker compose) → `test` (CI, her PR; sahte SMS/push/zaman damgası) → `staging` (üretim benzeri, gerçek sağlayıcı test hesapları; pilot UAT burada) → `prod`. Staging'de zaman dondurma ve "saat ilerlet" yönetici aracı (zamanlayıcı testleri için) bulunur; prod'da yoktur.

## Test verisi

Sentetik zincir "Kahve Durağı" (03-analiz/04 ve 06-test/03): 25 şube, 3 bölge, 100 istasyon, 412 kullanıcı, 6 şablon, 8 plan, 30 günlük geçmiş çalıştırma ve kanıt (sentetik fotoğraflar, damgalı). Gerçek müşteri verisi test ortamlarına asla kopyalanmaz.

## Giriş/çıkış ölçütleri

- Sprint DoD: yeni FR için birim + kabul testi yazılmış ve geçmiş; CI yeşil; kritik hata sıfır.
- Beta (4,5. ay): TC'lerin ≥ %80'i otomasyonda; E2E gece koşusu; performans ölçümü cihaz matrisinde.
- GA: v1 etiketli 89 kabul testi %100 geçiş (v1.1 testleri ilgili sürümde); sızma testi kapanmış; kurtarma tatbikatı yapılmış; pilot UAT imzası (3 zincir).

## Hata sınıflandırma

| Sınıf | Tanım | SLA (düzeltme) |
|---|---|---|
| S1 Kritik | Veri kaybı, yanlış kaçırıldı/başarısız, yetki sızıntısı, kanıt bütünlüğü | Anında; sürüm durdurulur |
| S2 Yüksek | Ana akış çalışmıyor (liste tamamlama, senk, bildirim) | Sprint içinde |
| S3 Orta | Yan akış, rapor, kullanılabilirlik | Sonraki sprint |
| S4 Düşük | Görsel, metin | Backlog |
