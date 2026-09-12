# Cihaz ve tarayıcı matrisi

Hedef: personelin gerçek cihazları (düşük segment Android, şube tabletleri) ve yöneticilerin telefon/tarayıcıları. Matris pilot görüşmelerinde (Blok 5) sahadan gelen cihaz bilgisiyle güncellenir.

## Mobil (Flutter)

| Sınıf | Cihaz (örnek) | OS | RAM | Neden | Test sıklığı |
|---|---|---|---|---|---|
| Düşük Android | Samsung Galaxy A05 / A04, Redmi 9A, General Mobile GM 22 | Android 12–13 (Go dahil) | 2–3 GB | Personel telefonu gerçekliği; NFR-02/06 ölçümü burada | Her sürüm (elle + otomasyon) |
| Orta Android | Samsung A15/A25, Redmi Note 12 | Android 13–14 | 4–6 GB | En yaygın segment | Her sürüm |
| Eski Android | Android 9 (API 28) cihaz/emülatör | 9 | 2 GB | Alt sınır | Sürümde bir (emülatör), çeyrekte bir gerçek |
| Tablet Android (kiosk) | Samsung Galaxy Tab A9 / A8, Lenovo Tab M10 | Android 13–14 | 4 GB | Şube kiosk cihazı; yatay düzen, PIN | Her sürüm |
| iPhone eski | iPhone SE (2. nesil), iPhone 11 | iOS 15–17 | — | Şube müdürü / bölge müdürü | Her sürüm |
| iPhone güncel | iPhone 14/15 | iOS 17–18 | — | Yönetici | Her sürüm |
| iPad | iPad 9. nesil | iPadOS 16+ | — | Kiosk alternatifi (bazı zincirler) | Sürümde bir |

Zorunlu koşul testleri: uçak modu; zayıf ağ (3G kısıtlama); düşük pil modu; %130 yazı boyutu; koyu tema; yatay/dikey (tablet); kamera izni reddi; depolama dolu.

## Web (React)

| Tarayıcı | Sürüm | Not |
|---|---|---|
| Chrome / Edge | Son 2 | Birincil |
| Safari (macOS) | Son 2 | Yönetici Mac kullanıcıları |
| Firefox | Son 2 | İkincil |
| Mobil Safari / Chrome (telefon) | Son 2 | Yönetici mobil web yedeği (ana yol uygulama) |
| Çözünürlük | 1280×720 (alt sınır), 1440×900, 1920×1080 | Izgara 100 şubede yatay kaydırma testi |

## Performans ölçüm protokolü (NFR-02)

Cihaz: Galaxy A05 (2 GB RAM), Android 13, %50 pil, Wi-Fi + 3G kısıtlama. Ölçümler 10 tekrar, medyan raporlanır: soğuk açılış → Bugün; listeyi aç (önbellek); fotoğraf çek → sonraki madde; 20 maddelik listeyi gönder (çevrimiçi / çevrimdışı kuyruğa). Eşikler: < 3 sn / < 1 sn / < 1,5 sn / < 2 sn.
