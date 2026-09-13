# Pilot UAT planı

Kullanıcı kabul testi, doğrulama sprintinden (fizibilite §10) gelen 3 pilot zincirle staging ortamında yürütülür; GA kararının girdisidir (kapı 3: 4. haftada tamamlanma ≥ %80, en az 2 zincir yıllık sözleşmeye geçer).

## Kapsam ve takvim (8 hafta)

| Hafta | Aşama | İçerik | Çıktı |
|---|---|---|---|
| 0 | Hazırlık | Pilot sözleşmesi ve veri işleme sözleşmesi; şube/personel Excel'i; şablon uyarlaması (kapanış + soğuk zincir); tablet kurulumu; aydınlatma metni | Hesap canlı, 15–30 şube |
| 1 | Kurulum ve eğitim | Yerinde 1 gün: kiosk kurulumu, personel PIN'leri, ilk kapanış birlikte; şube müdürü 30 dk, personel 10 dk eğitim | Tüm şubeler ilk listeyi tamamladı |
| 2–3 | Sessiz kullanım | Ekip müdahale etmez; günlük metrik takibi; destek kanalı | Haftalık rapor |
| 4 | Ara değerlendirme | Kapı ölçütleri: tamamlanma ≥ %80, kanıt ≥ %95, kritik aksiyon kapanışı ≥ %80; 30 dk geri bildirim görüşmesi (şube müdürü + operasyon müdürü) | Karar: devam / düzelt |
| 5–7 | Genişletme | Üçüncü liste (saatlik hijyen veya haftalık); duyuru-onay; raporların merkezde kullanımı | Kullanım verisi |
| 8 | Kapanış | Sonuç raporu, 3 soruluk memnuniyet anketi, yıllık sözleşme görüşmesi | UAT imzası / sözleşme |

## Başarı ölçütleri (GA kapısıyla aynı)

| Metrik | Hedef | Kaynak |
|---|---|---|
| Aktivasyon | Şubelerin %90'ı ilk 7 günde ≥ 1 liste | Izgara |
| Pencere içi tamamlanma (4. hafta) | ≥ %80 | Tamamlanma raporu |
| Kanıt yoğunluğu | Fotoğraf zorunlu maddelerde ≥ %95 | Rapor |
| Kritik aksiyon vadesinde kapanış | ≥ %80 | Aksiyon raporu |
| Yönetici alışkanlığı | Bölge müdürleri haftada ≥ 3 gün panelde | Kullanım logu |
| Destek yükü | ≤ 1 talep / şube / ay | Destek kanalı |
| S1/S2 hata | Sıfır açık | Hata takibi |
| Dönüşüm | ≥ 2 zincir yıllık sözleşme | Sözleşme |

## Roller

- Pilot sahibi (zincir): operasyon müdürü — haftalık 30 dk.
- Ürün sahibi (Talimatname): günlük metrik, geri bildirim toplama, backlog'a işleme.
- Destek: hafta içi 08–24 (kapanış saatleri kritik); ilk yanıt ≤ 30 dk.
- Geliştirme: haftalık düzeltme sürümü (S2 ve üstü).

## Geri bildirim toplama

- Her şubede haftalık 5 dakikalık personel sohbeti (görüşme rehberi C varyantı).
- Uygulama içi "geri bildirim gönder" (menü) → backlog.
- Gözlem ziyareti: 2. ve 6. haftalarda kapanış vardiyası (görüşme rehberi §07 gözlem listesi).
- İsim testi: pilot sonunda üç kart (Talimatname + iki dönüşümlü) — kesin isim kararı için.

## Çıkış kriterleri ve karar

- **Geç:** tüm hedefler tutuyor → GA hazırlığı; pilot verisi (izinle) referans vakası.
- **Düzelt:** 1–2 metrik hedefin altında ama eğilim yukarı → 4 hafta uzatma, backlog'da düzeltmeler.
- **Dur:** tamamlanma < %60 veya 2 zincir bırakırsa → fizibilite kapısı devreye girer (24. ay kapısından bağımsız erken sinyal); kök neden analizi (cihaz, alışkanlık, fiyat, ürün).

## UAT test seti

Kabul testlerinden (02) UAT alt kümesi (v1): TC-004, 005, 008, 013–016, 039–046, 051, 057–059, 062, 065–067, 073, 074, 085, 087, 088, 091, 095, 096, 104, 107, 108. (Duyuru testleri 079–083 v1.1.) Pilot kullanıcıları bunları gerçek iş akışında icra eder; ürün sahibi metrik ve logdan doğrular; elle test yalnızca kiosk ve kamera adımlarında.
