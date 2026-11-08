# Aktörler

> **v1 notu (ADR-0008):** ilk sürümde **beş** rol vardır — **Yönetici** (A-01 Hesap yöneticisi + A-02 Operasyon müdürü + A-03 Kalite tek rolde), **Bölge müdürü** (A-04), **Denetçi** (A-11), **Şube müdürü** (A-05), **Personel** (A-06). Gözlemci (A-07) v1.1. Aşağıdaki aktör listesi ve matris tam modeli anlatır; v1'de A-01/A-02/A-03 satırları Yönetici olarak okunur.

Aktör = sistemle etkileşen rol (kişi veya dış sistem). Personalar (02-urun/02) aktörlerin somut örnekleridir. Yetki ayrıntısı 04-gereksinimler/01 (FR-CAP02) ve 06 (rol matrisi).

## İnsan aktörler

| ID | Aktör | Kapsam (görebildiği) | Ana amaçları | Kullandığı yüzey |
|---|---|---|---|---|
| A-01 | Hesap yöneticisi | Tüm hesap | Kurulum, şube/personel/rol/cihaz yönetimi, KVKK talepleri, faturalama sayacı | Web |
| A-02 | Operasyon müdürü (merkez) | Tüm şubeler | Şablon ve plan kurmak, ızgarayı izlemek, duyuru yayınlamak, raporlamak, eskalasyonun son halkası | Web + mobil özet |
| A-03 | Kalite / gıda güvenliği sorumlusu | Tüm şubeler (kalite verisi) | Ölçüm günlükleri, kritik madde kuralları, denetim PDF'i, denetim izi, gözden geçirme | Web |
| A-04 | Bölge müdürü | Kendi bölgesi | Sabah kontrolü, eskalasyon alma, aksiyon atama/kapatma, kanıt inceleme | Mobil (yönetici görünümü) + web |
| A-05 | Şube müdürü / vardiya amiri | Kendi şubesi | Günlük atama, yapılamadı onayı, sorun bildirme, aksiyon kapatma, kiosk cihazı yönetme | Mobil (kiosk + kendi telefonu) |
| A-06 | Personel | Kendisine/istasyonuna atananlar | Listeyi tamamlamak, kanıt yüklemek, yapılamadı/sorun bildirmek, duyuru onaylamak | Mobil (kiosk PIN veya kendi telefonu) |
| A-07 | Gözlemci (franchise sahibi vb.) | Atandığı şubeler, salt okunur | Kendi şubesinin durumunu ve kanıtlarını görmek | Web + mobil |
| A-11 | Denetçi | Atandığı bölge(ler) | Şubeye gidip denetim listesini **kendisi** doldurmak, bulguyu aksiyona çevirmek | Mobil (saha) + web (okuma) |
| A-09 | Destek uzmanı (Talimatname) | Müşteri hesabı, destek modu (yalnızca teknik izler, kanıt içeriği maskeli) | Bildirim teslimatı, senk ve cihaz sorunlarını çözmek | İç araç |

## Sistem aktörleri

| ID | Aktör | Rolü |
|---|---|---|
| A-08 | Zamanlayıcı (sistem) | Çalıştırma üretimi (7 gün ileri), pencere açılış/bitiş geçişleri, hatırlatma ve eskalasyon zamanlayıcıları, saklama süresi silmeleri, günlük kök özeti |
| A-10 | Push servisi (FCM / APNs) | Mobil bildirim teslimatı |
| A-11 | SMS sağlayıcı | Yedek kanal (OTP, kritik/eskalasyon bildirimleri) |
| A-12 | Zaman damgası servisi (RFC 3161) | Olay günlüğü günlük kök özetinin dış damgalanması |
| A-13 | Nesne depolama (S3 uyumlu) | Kanıt dosyaları (ham + damgalı), PDF çıktıları |
| A-14 | E-posta servisi | Yönetici davetleri, planlı raporlar (Should), PDF paylaşım bağlantıları |

## Rol × yetki özeti (ayrıntı: 04-gereksinimler/06)

| Eylem | A-01 | A-02 | A-03 | A-04 | A-05 | A-06 | A-07 |
|---|---|---|---|---|---|---|---|
| Şube/personel/rol yönet | ✓ | ✓ (şube meta) | – | – | Kendi şubesi (personel) | – | – |
| Şablon oluştur/yayınla | – | ✓ | ✓ | – | – | – | – |
| Plan tanımla | – | ✓ | ✓ | Kendi bölgesi | – | – | – |
| Günlük atama | – | ✓ | – | ✓ | ✓ | – | – |
| Listeyi tamamla, kanıt yükle | – | – | – | – | ✓ | ✓ | – |
| Yapılamadı / sorun bildir | – | – | – | – | ✓ | ✓ | – |
| "Yapılmayacak" işaretle | – | ✓ | – | ✓ | ✓ | – | – |
| Aksiyon oluştur/ata/kapat | – | ✓ | ✓ | ✓ | ✓ (şube) | Kapatma kanıtı yükler | – |
| Duyuru yayınla | – | ✓ | ✓ | Bölgesine | Şubesine | – | – |
| Rapor ve kanıt görüntüle | ✓ | ✓ | ✓ | Bölgesi | Şubesi | Kendi kaydı | Şubesi (salt okunur) |
| Denetim izi | ✓ | ✓ | ✓ | – | – | – | – |
| KVKK talebi işle, saklama ayarı | ✓ | – | – | – | – | – | – |
