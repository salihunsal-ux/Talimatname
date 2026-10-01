# Sprint 0 planı ve teknik spike'lar

Tarih: 16 Eylül 2026 · **takvim yeniden kuruldu 1 Ekim 2026** (§1). Sprint 0'ın kontrol listesi [02-repo-ve-ortam-kurulumu.md](02-repo-ve-ortam-kurulumu.md) içinde; bu belge **takvimi**, **ekip kararını** ve mimari kararların (ADR-0002/0004/0005) riskli kısımlarını kanıtlayacak **dört spike'ı** tanımlar. Spike = zaman kutulu deney; ürün kodu değildir, sonucu bir ADR notu ve (geçerse) Sprint 1–4 hikâyelerine giren örnek kodudur.

## 1. Takvim (1 Ekim 2026'da yeniden kuruldu)

Eylül planı ilanın 17 Eylül'de çıkmasını ve Sprint 0'ın 5 Ekim'de başlamasını varsayıyordu; ikisi de olmadı (depoda 16 Eylül'den beri hareket yok, görüşme notu yok). İki haftalık kayma **telafi edilebilir**: ilan bu hafta çıkar ve saha 5 Ekim'de başlarsa pilot ölçümü Şubat 2027'ye gelir — fizibilitenin Baz senaryosundaki lansman varsayımına (6. ay) iki hafta mesafede, tampon S11–S12 duruyor.

**Yeni taban:** ilan 2 Ekim (Cuma) · saha ulaşımı 5 Ekim · Sprint 0 19–30 Ekim · Sprint 1 2 Kasım.

| | Tarih | Not |
|---|---|---|
| İlan yayını, ilk 30 ulaşım mesajı | **2 Ekim** | İlan metni ve PDF hazır; tek eksik iletişim adresi |
| Doğrulama haftası 1 — ilk görüşmeler | **5 Ekim** | 40 ulaşım, hedef 5 randevu |
| Aday görüşmeleri + ücretli mini görev | 6–15 Ekim | 07-serbest-gelistirici-secimi §3 |
| Sözleşme, gün 0 hazırlığı | 16 Ekim | 06-ilk-gun-paketi "Gün 0" |
| **Sprint 0** (iskelet + 4 spike) | **19–30 Ekim** | Doğrulama haftası 3–4 |
| Sprint 1 | 2–13 Kasım | |
| **K1 kapısı** (≥ 12/20 görüşme) | **26 Ekim** (doğrulama haftası 4) | |
| **Devam/dur kapısı** (K1 raporu + Sprint 2 sonu) | **27 Kasım** | K1 geçmezse geliştirme durur; iki sprintlik iş iskelet + spike olarak kalır |
| K2 kapısı (≥ 5 LOI) | 23 Kasım (hafta 8) | |
| **Alfa (S6)** | **22 Ocak 2027** | Pilot kurulumu burada başlar |
| **Beta (S8)** | **19 Şubat 2027** | 3 pilot zincir, 30+ şube |
| **GA (S10)** | **19 Mart 2027** | 89 v1 kabul testi %100, pilot UAT imzası |
| Tampon S11–S12 | 22 Mart – 16 Nisan | |
| **K3 ölçümü** (pilot 4. hafta) | **Şubat 2027** | Alfa'dan 4 hafta sonra |

Daha fazla gecikmenin maliyeti: her hafta kayma pilot ölçümünü bir hafta öteler; **Sprint 0 Kasım'a sarkarsa** K3 Mart'a, lansman 8. aya gider ve tampon tükenir (fizibilite Baz senaryosu yeniden koşulmalı). Görüşmeler geliştirmeyi beklemez — saha hattı ekip kararından bağımsız 5 Ekim'de başlayabilir ve başlamalı.

## 2. Ekip kararı — **A seçildi** (ADR-0009, 16 Eylül); seçim süreci [07-serbest-gelistirici-secimi.md](07-serbest-gelistirici-secimi.md), ilan [ilan/](ilan/serbest-gelistirici-ilani.html). Hedef başlangıç **19 Ekim** (yeniden kurulan takvim, §1).

| Seçenek | Aylık maliyet (tahmin) | Artı | Eksi | Ne zaman uygun |
|---|---|---|---|---|
| A · 2 serbest geliştirici (1 Flutter, 1 backend/web), yarı zamanlı tasarımcı | ₺250–400 bin | Hızlı başlangıç, esnek | Koordinasyon kurucuda; bilgi kişide kalır | K1 öncesi, risk düşük tutulacaksa |
| B · Yazılım evi (sabit kapsam, 10 sprint) | ₺3–5 milyon toplam | Tek muhatap, süreç | Kapsam değişikliği pahalı; pilot geri bildirimi zor girer | Kapsam donmuşsa (bizde donmadı: v1.1 sırası pilotla) |
| C · Teknik kurucu ortak + 1 serbest | Hisse + ₺150–250 bin | Ürün bilgisi içeride kalır, uzun vade | Bulmak zaman alır (4–8 hafta) | Fizibilite GO'ya yaklaşınca |

Tahminler 2026 İstanbul piyasası için kaba aralıklardır; teklif alınca güncellenir. Kararı etkileyen tek soru: **K1 geçmezse ne olacak?** A ve C'de durmak kolay; B'de sözleşme.

Ne olursa olsun Sprint 0'da gereken profil: Python/FastAPI + PostgreSQL bilen bir backend geliştirici (RLS, Alembic, kuyruk), Flutter bilen bir mobil geliştirici (çevrimdışı, kamera). Web (React) Sprint 5'e kadar backend geliştiricinin yarı zamanıyla gider (ekip notu, 03-backlog).

## 3. Sprint 0 takvimi (2 hafta, iki kişi)

| Gün | Backend | Mobil | Ortak |
|---|---|---|---|
| 1–2 | Depolar, CI iskeleti, dev compose, sahte servisler | Flutter iskelet, tema token'ları (05-tasarim/04), Riverpod + Drift | Backlog aracı; DoR/DoD; kural fikstürü formatı |
| 3–5 | **Spike B** (RRULE pencere motoru) | **Spike A** (çevrimdışı kuyruk + idempotent senk) | Fikstürler: pencere/durum, puan, sabit kural |
| 6–7 | **Spike D** (push → SMS teslim izi, sahte sağlayıcı) | **Spike C** (kamera → damga → SHA-256, galeri kapalı) | Staging (TR bölgesi) sağlayıcı seçimi |
| 8–9 | `audit.emit()` + RLS iskeleti; OpenAPI yayını; tohum v0 | Üretilmiş istemci; giriş ekranı iskeleti | Spike sonuçları → ADR notları |
| 10 | Sprint 0 gözden geçirme: DoD kontrolü, Sprint 1 planlama | | Devam/dur kapısı hazırlığı (Sprint 2 sonu) |

## 4. Spike'lar

Her spike için: soru, deney, kabul ölçütü, süre, çıktı. "Geçmedi" bir sonuçtur — ADR güncellenir, alternatif Sprint 1'e girer.

### Spike A · Çevrimdışı kuyruk ve idempotent senk (Flutter + API) — 3 gün

- **Soru:** 72 saat çevrimdışı, 500 kanıt, iki cihaz aynı çalıştırma: kanıt kaybı sıfır ve tek kayıt garantisi verilebilir mi? (Y-5, FR-0701…0708, BR-24, TC-051…055)
- **Deney:** Drift'te cevap + kanıt kuyruğu; her kayıt cihazda üretilen UUID (idempotency key) ile; API `PUT /answers/{uuid}` tekrar gönderimde 200 + aynı kayıt. Uçak modunda 20 madde + 5 fotoğraf; bağlantı gelince arka planda senk (WorkManager/BGTask). Aynı çalıştırmayı iki cihazda karışık çevrimdışı doldur, 100 tekrar.
- **Kabul:** 100 tekrarda sıfır kayıp, sıfır çift kayıt; senk 2 dk içinde; uygulama öldürülüp açılınca kuyruk duruyor; 500 kanıtta yeni fotoğraf engelleniyor ve uyarı veriyor; senk durumu ekranda (bekleyen sayısı).
- **Çıktı:** kuyruk şeması, senk döngüsü, idempotency sözleşmesi (OpenAPI), TC-051/054/055 fikstürleri. Geçmezse: senk sıklığı/parti boyutu değişir; ikinci seçenek olarak "yalnızca çevrimiçi gönder, çevrimdışı taslak" modeline ADR notu.

### Spike B · RRULE pencere motoru ve gece yarısı (Python) — 2 gün

- **Soru:** RRULE + pencere + tolerans + kapalı gün + saat dilimi tek fonksiyonla, mobil ve backend'de aynı sonucu verecek şekilde yazılabilir mi? (ADR-0005, P-1/P-2, FR-0501…0507, TC-025, TC-032)
- **Deney:** `dateutil.rrule` üzerine `pencere(kural, şube_saat_dilimi, tarih)` → (başlangıç, bitiş, tolerans_sonu, iş_günü). Fikstür: 22:00–01:30 gece yarısı aşımı; her 2 saat 10–22; haftalık Pazartesi; kapalı gün; Europe/Berlin yaz saati geçişi; 7 gün ileri üretimde tekillik.
- **Kabul:** 40 fikstürün tamamı geçer; aynı fikstürler Dart'ta (mobil kural motoru) aynı sonucu verir (JSON fikstür paylaşımı); yaz saati gecesinde çift üretim yok; kural değişince başlanmamış çalıştırmalar yeniden hesaplanır, başlanmışlar korunur.
- **Çıktı:** `talimatname-spec/pencere.json` fikstürleri; motor iki dilde; ADR-0005'e "uygulama notu".

### Spike C · Kamera → damga → SHA-256, galeri kapalı (Flutter + API) — 2 gün

- **Soru:** Uygulama içi kamera, ≤ 300 KB sıkıştırma, sunucu damgası ve dosya özeti düşük segment Android'de 2 dokunuşla ve 3 saniyenin altında olur mu? (ADR-0004, Y-3, FR-0601…0606, TC-039…044)
- **Deney:** `camera` eklentisiyle doğrudan çekim (galeri seçici yok); cihazda sıkıştırma + SHA-256; yükleme imzalı URL ile; sunucu görünür damga (şube · tarih-saat · kullanıcı · cihaz) basar, ham dosyayı ayrıca saklar; cihaz saati farkı kaydedilir. Test cihazı: 2 GB RAM Android 10 (04-cihaz-matrisi en düşük satır) + tablet.
- **Kabul:** çekim → madde tamam ≤ 3 sn (düşük cihazda ≤ 5); dosya ≤ 300 KB, okunur; özet sunucuda doğrulanır; galeri yoluyla yükleme mümkün değil (kod incelemesi + deneme); damgalı ve ham dosya ikisi de nesne depoda; 50 fotoğraflık çevrimdışı kuyruk Spike A ile birlikte çalışır.
- **Çıktı:** kanıt yükleme sözleşmesi, damga bileşeni, cihaz matrisinde ölçülen süreler.

### Spike D · Push → teslim izi → SMS yedeği (API + sahte sağlayıcılar) — 1,5 gün

- **Soru:** "Kritik madde başarısız → 10 dk içinde teslim/okunma yoksa SMS" ve sessiz saat kuralı, teslim izi olay günlüğünde kalacak şekilde güvenilir çalışır mı? (E-6, FR-1001…1008, BR-11/23, TC-036, TC-078, TC-117)
- **Deney:** Bildirim servisi arayüzü (kanal, alıcı, olay, içerik, teslim izi); FCM/APNs sahte sağlayıcı (geçersiz token senaryosu), SMS sahte sağlayıcı; Redis gecikmeli iş ("10 dk sonra teslim yoksa SMS"); sessiz saat 23:00–07:00 ertelemesi (kritik hariç).
- **Kabul:** kritik olayda push anında + 10 dk sonra SMS (okunduysa gitmez); geçersiz token → SMS ve token temizliği; 02:00'de orta öncelik → 07:00'ye ertelendi; her adım `audit.emit()` ile logda; gerçek sağlayıcı seçimi (SMS: yerel; push: FCM) ve maliyeti not edildi.
- **Çıktı:** bildirim servisi iskeleti, gecikmeli iş deseni, sağlayıcı kararı.

## 5. Sprint 0 bitti tanımı (DoD)

- 02-repo kontrol listesinin tamamı işaretli; `make dev` tek komutla ayağa kalkıyor; CI üç depoda yeşil.
- Dört spike'ın sonucu yazılı (geçti / geçmedi + ne değişecek); ADR-0004/0005'e uygulama notu; Spike A/C kabul ölçütleri TC-051/054/055 ve TC-039…044'e fikstür olarak bağlı.
- Tasarım token'ları kodda (Flutter `ThemeData`, web CSS değişkenleri) ve tel-çerçevedeki iki ekran (kiosk kilit, kapanış listesi) iskelet olarak derleniyor.
- Tohum v0 (hesap, 3 şube, 5 kullanıcı, 1 şablon, 1 plan) ve backlog aracında S1–S2 hikâyeleri hazır (DoR).
- Staging ortamı TR bölgesinde ayakta; sağlayıcı hesapları (nesne depo, SMS, push) test modunda.

## 6. Karar noktaları

| Ne | Kim | Ne zaman |
|---|---|---|
| ~~Ekip seçeneği~~ A seçildi; ilan **2 Ekim**, seçim 15 Ekim, Sprint 0 **19 Ekim** | Kurucu | İlan bu hafta; 15 Ekim teklif |
| Spike sonuçlarına göre ADR güncellemeleri | Ekip + PO | Sprint 0 gün 9 |
| Devam/dur kapısı: K1 raporu + Sprint 2 sonu | Kurucu | 27 Kasım (K1: 26 Ekim) |
| Sağlayıcı seçimleri (TR bulut, SMS, push) | Backend + PO | Sprint 0 gün 7 |
