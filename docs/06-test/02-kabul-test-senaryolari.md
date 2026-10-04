# Kabul test senaryoları

125 kabul testi; her biri bir use case'e ve en az bir FR/BR'ye bağlı. TC-120…TC-125 E-11 ve E-12 ile, TC-113…TC-119, ADR-0008 ile eklenen v1 gereksinimlerini (E-1…E-7) kapsar. **Sürüm** sütunu ADR-0008'e göre: v1 (GA kapısı) / v1.1; parantez içi, testin v1'de daraltılmış kapsamını belirtir. Veri seti: "Kahve Durağı" (03-test-verisi-ve-ortam.md). Biçim: **Ön koşul → Adımlar → Beklenen**. Otomasyon sütunu: B = birim, A = API/entegrasyon, E = E2E, M = elle (cihaz/UAT).

## UC-01 · Hesap kurulumu

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-001 | Excel ile şube yükleme | Boş hesap → 25 satırlık geçerli dosya yükle → 3 bölge, 25 şube, 100 istasyon oluşur; özet doğru | FR-0105 | A | v1 |
| TC-002 | Hatalı satır raporu | Dosyada 2 satır saat dilimi boş → yükle → 23 kayıt oluşur, 2 hatalı satır raporu indirilebilir, hata nedenleri satır bazında | FR-0106 | A | v1 |
| TC-003 | %20 üstü hata reddi | 25 satırın 6'sı hatalı → yükle → hiçbir kayıt oluşmaz; uyarı ve rapor | FR-0106 | A | v1 |
| TC-004 | Sihirbaz kaldığı yerden | Adım 3'te tarayıcı kapat → tekrar gir → adım 3 açılır, önceki adımlar korunmuş; yayınla → ilk çalıştırmalar 7 gün ileriye üretilmiş | FR-1401, FR-0513 | E | v1 |

## UC-02 · Personel, rol, cihaz

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-005 | Davet SMS'i ve giriş | Personel ekle → SMS gönderilir (sahte sağlayıcı), teslim durumu "iletildi"; bağlantıyla giriş → OTP akışı | FR-0107, FR-0108 | A | v1 |
| TC-006 | Rol kapsamı | Murat'a Bölge müdürü · Anadolu ver → Avrupa şubesinin çalıştırmasına API ile erişim → 403 | FR-0205 | A | v1 (4 rol) |
| TC-007 | Pasifleştirme | Emre'yi pasifleştir → giriş reddedilir; gelecek atamaları kalkar; geçmiş cevap/kanıt aynen görünür | FR-0109, BR-22 | A | v1 |
| TC-008 | Kiosk cihaz kaydı | Panelden QR üret → tablette okut → cihaz şubeye bağlı, kiosk modu açık; panelden kaldır → tablet kilit ekranı "cihaz kaydı yok" | FR-0207 | M | v1 |

## UC-03 · Oturum

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-009 | OTP limitleri | 3 hatalı kod → 15 dk blok; 60 sn'den önce yeniden gönder → reddedilir; 5 dk sonra kod geçersiz | FR-0204 | A | v1 |
| TC-010 | Yatay yetki | Kadıköy şube müdürü, Üsküdar çalıştırma id'siyle GET → 403; liste uç noktaları yalnızca kapsam döner | FR-0205 | A | v1 |
| TC-011 | Kiracı yalıtımı | Hesap A belirteciyle hesap B nesne id'leri → 404/403; toplu listelerde sızıntı yok (fuzz) | FR-0101 | A | v1 |
| TC-012 | Aydınlatma ve konum izni | İlk giriş → aydınlatma gösterilir, onay zaman damgalı; metin sürümü değişince yeniden; konum reddi → uygulama çalışır, kanıt "konum yok" bayrağı | FR-1307, FR-1308 | E | v1 |

## UC-04 · Kiosk PIN

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-013 | PIN ile geçiş ve atıf | Emre PIN girer, maddeyi cevaplar → cevap kullanıcı=Emre, cihaz=KDK-1 | FR-0208 | M | v1 |
| TC-014 | Hareketsizlik kilidi | 2 dk dokunma yok → kilit; geri dönünce tamamlanmamış cevaplar duruyor | FR-0209 | M | v1 |
| TC-015 | PIN blok | 5 hatalı → 1 dk blok; 3 blok → şube müdürüne bildirim (teslimat izi) | FR-0210 | M | v1 |
| TC-016 | PIN sıfırlama | Şube müdürü sıfırlar → yeni PIN belirlenir; olay logda "pin_reset" aktör=şube müdürü | FR-0208 | E | v1 |

## UC-05 · Şablon

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-017 | Kütüphaneden kopyala | "Kapanış — kafe" kopyala → yeni şablon taslak v1, kütüphane kaydı bağımsız | FR-0311 | A | v1 |
| TC-018 | Madde türleri render | 11 madde türü içeren şablon → mobil önizleme ve gerçek cihazda her tür doğru bileşen | FR-0303 | E | v1 (6 tür) |
| TC-019 | Sıcaklık aralığı sınırı | 0–4 °C; 4,0 → geçer; 4,1 → başarısız + fotoğraf/not istenir | FR-0305, BR-08 | B | v1 |
| TC-020 | Puan hesabı | Ağırlıklar 3/2/1; iki madde geçmedi → puan doğru; talimat maddesi puanlanmaz; eşik %90 altı "Başarısız" | FR-0306, BR-07 | B | v1 (yüzde puan) |
| TC-021 | Sürümleme | v1 yayında, düzenle → v2 taslak; v1 değişmez; v2 yayınla → başlanmamış çalıştırmalar v2, başlanmış v1 | FR-0301, BR-18 | A | v1 |
| TC-022 | Yayın doğrulaması | Kritik + yapılamadı izinli → yayın engellenir, açıklama | FR-0312 | A | v1 |
| TC-023 | Koşullu mantık eylemleri | "Hayır" cevabında not+fotoğraf iste, aksiyon oluştur (bölge müdürü, yüksek), bildir (kalite) → mobilde istenir, senk sonrası tek aksiyon, bildirim izi | FR-0401…0403 | E | v1 (sabit kural FR-0405) |
| TC-024 | Tarihli yayın | Yayın 06:00 → o saate kadar v1 kullanılır, sonra v2 | FR-0310 | A | v1.1 |

## UC-06 · Plan

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-025 | Gece yarısı penceresi | 22:00–01:30 → iş günü açılış tarihi; 01:20 gönderim zamanında; 01:31–03:30 geç; 03:31 kilitli | FR-0505, BR-01…03 | B | v1 |
| TC-026 | Saatlik tekrar | 09:00–23:00 her saat, tolerans 0 → günde 15 çalıştırma; pencere bitişinde kaçırıldı | FR-0503 | B | v1 |
| TC-027 | Haftalık/aylık | Pazartesi 06:00–12:00; ayın ilk Pazartesi'si → doğru tarihler (RRULE) | FR-0503 | B | v1 |
| TC-028 | Çalışma saatinden türetme | Şube kapanışı 24:00 → pencere 22:00–01:30; şube saati 23:00 olunca pencere 21:00–00:30 | FR-0507 | B | v1 |
| TC-029 | Atama modeli | Rol ataması → o şubede o roldeki herkes görür; "herkes tamamlasın" → her atanan kendi bölümünü gönderir | FR-0508, BR-16 | E | v1.1 |
| TC-030 | Önizleme ve kapalı gün | 7 gün önizleme 173 çalıştırma (2 kapalı gün düşülmüş); ızgarada "kapalı" | FR-0511, FR-0515, BR-17 | A | v1 |
| TC-031 | Çakışan plan | Aynı şube-şablon-pencere için ikinci plan → kaydedilemez | FR-0517 | A | v1 |
| TC-032 | Saat dilimi ve DST | Şube dilimi Europe/Berlin (DST) ve Europe/Istanbul; geçiş gecelerinde tek üretim, doğru süre, doğru iş günü | NFR-14, ADR-0005 | B | v1 |

## UC-07 · Çalıştırma üretimi ve hatırlatma

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-033 | Benzersiz üretim | Zamanlayıcı 3 kez koşar → aynı pencere için tek çalıştırma | FR-0513 | B | v1 |
| TC-034 | Durum geçişleri | Planlandı → Açık (pencere başı) → Kaçırıldı (tolerans sonu) — zaman dondurmayla; her geçiş logda | FR-0514 | B | v1 |
| TC-035 | Hatırlatma zamanları | Açılışta, bitişe 30 dk, bitişte push; teslimat izinde 3 kayıt | FR-0509, FR-1001 | A | v1 (2 hatırlatma) |
| TC-036 | Push başarısız → SMS | Geçersiz token; kritik liste → SMS yedek gönderilir; token temizlenir | FR-1002, FR-1006 | A | v1 (kritik SMS) |
| TC-037 | Plan değişikliği | Pencereyi değiştir → gelecek "Planlandı" yeniden hesaplanır; "Açık" korunur | FR-0516 | B | v1 |
| TC-038 | Yapılmayacak | Şube müdürü sebeple işaretler → puanlanmaz, eskalasyon durur, rapor "yapılmayacak" | BR-04, FR-0914 | E | v1 |

## UC-08 · Liste tamamlama

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-039 | Bugün ekranı | 4 çalıştırma (açık, tamamlandı, geç, planlı) → doğru durum/geri sayım; boş gün ve kapalı gün durumları | FR-0601, FR-0610 | E | v1 |
| TC-040 | Zorunlu madde kilidi | 5 zorunlu eksikken "Gönder" pasif; tamamlanınca aktif | BR-05, FR-0607 | E | v1 |
| TC-041 | Yalnızca kamera | Şablon ayarı açık → galeri simgesi yok; kapalı → galeri kanıtı "galeri" bayrağı | FR-0604, BR-14 | M | v1 |
| TC-042 | Sıkıştırma | 12 MP fotoğraf → ≤ 300 KB, uzun kenar 1600; 25 sn video reddedilir, 20 sn ≤ 3 MB | FR-0605 | M | v1 (video hariç) |
| TC-043 | Damga ve hash | Yüklenen kanıt: sunucu zamanı, kullanıcı, cihaz, sha256 eşleşir; damgalı kopya görünür metin doğru; ham dosya erişilebilir | FR-0606 | A | v1 |
| TC-044 | Konum bayrakları | Şubeden 800 m → "uzak"; izin yok → "konum yok" | BR-15 | M | v1 |
| TC-045 | Geç gönderim | Pencere 01:30 bitti, 01:50 gönder → "Geç tamamlandı"; 03:40 → kilitli, "Kaçırıldı" | BR-02, BR-03 | E | v1 |
| TC-046 | Kritik kural | Buzdolabı 6,0 °C → madde başarısız, çalıştırma "Başarısız" (puan %95 olsa bile), kritik aksiyon 4 sa | BR-06, FR-0902 | E | v1 |
| TC-047 | Çoklu kullanıcı | İki cihaz aynı listede farklı maddeler → çakışma yok; aynı maddeye iki cevap → son yazan, eski cevap logda | FR-0609, BR-24 | A | v1.1 |
| TC-048 | Kaldığı yerden devam | 6 madde cevapla, uygulamayı öldür → aç → 6 cevap duruyor | FR-0603 | M | v1 |
| TC-049 | Ek kayıt | Gönderilmiş çalıştırmada madde düzelt → yeni ek kayıt, eski görünür, logda | FR-0608, BR-12 | E | v1.1 |
| TC-050 | Erişilebilirlik | Dokunma hedefleri ≥ 44 px; ekran okuyucu etiketleri; yazı %130'da düzen bozulmaz | FR-0611, NFR-11 | M | v1 |

## UC-09 · Çevrimdışı senk

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-051 | Uçak modunda tamamlama | 20 madde + 5 fotoğraf çevrimdışı → "bekliyor"; bağlantı → 2 dk içinde senk, sunucuda tam | FR-0702, FR-0703 | M | v1 |
| TC-052 | Zaman düzeltmesi | Cihaz saati 7 dk ileri → sunucu düzeltir; ham ve fark logda; 12 dk ileri → "saat farkı" bayrağı | FR-0704, BR-13 | A | v1 |
| TC-053 | Idempotent yükleme | Aynı cevap id iki kez → tek kayıt, "accepted"; yarım kalan kanıt yüklemesi devam eder | FR-0707 | A | v1 |
| TC-054 | Kuyruk sınırı | 500 kanıt → yeni fotoğraf engellenir, uyarı; 73 saatlik kayıt "geç senk" bayrağıyla senklenir | FR-0706 | M | v1 |
| TC-055 | Çakışma dayanıklılık | 100 tekrar: iki cihaz, aynı çalıştırma, karışık çevrimdışı → sıfır kanıt kaybı, tutarlı son durum | FR-0705, NFR-01 | A | v1 |
| TC-056 | Senk durumu ekranı | Bekleyen sayılar, son senk, hata ayrıntısı kopyalanabilir | FR-0708 | M | v1 |

## UC-10 · Yapılamadı

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-057 | Sebep zorunlu | Sebepsiz kaydet → engellenir | BR-09 | E | v1 |
| TC-058 | Diğer → not | "Diğer" + 3 karakter → engellenir; 5 karakter → kabul | FR-0803 | E | v1 |
| TC-059 | Otomatik aksiyon | Kayıt → şube müdürüne orta öncelik, vade 72 sa; push | BR-10 | A | v1 |
| TC-060 | Kritik maddede yok | Kritik maddede düğme görünmez; API ile deneme → 422 BR-09 | FR-0804 | A | v1 |
| TC-061 | Sebep raporu | 30 günlük veri → şube × sebep dağılımı doğru | FR-0805 | A | v1.1 |

## UC-11 · Sorun bildir

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-062 | Bildirim ve push | Sorun gönder → şube müdürüne push; panelde görünür | FR-0806 | E | v1 |
| TC-063 | Aksiyona çevir / kapat | Çevir → aksiyon alanları dolu; kapat → sebep zorunlu | FR-0807 | E | v1 |
| TC-064 | Yükseltme | Bölge müdürüne yükselt → bildirim ve log | FR-0808 | A | v1.1 |

## UC-12 · Aksiyon

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-065 | Alanlar ve listeler | Oluştur; "bana atananlar", "gecikmişler" filtreleri doğru | FR-0901, FR-0907 | A | v1 |
| TC-066 | Durum akışı | açık→devam→kapatma bekliyor→kapalı; reddedildi sebeple; yetkisiz geçiş 403 | FR-0904 | A | v1 (açık/kapalı) |
| TC-067 | Kapanış kanıtı | Fotoğrafsız kapat → engellenir; fotoğraf+not → kapalı | FR-0905 | E | v1 |
| TC-068 | Yorum ve bahsetme | @Murat → Murat'a bildirim; yorumda fotoğraf | FR-0906 | E | v1.1 |
| TC-069 | Vade hesabı | Kritik 4 sa, yüksek 24, orta 72, düşük 7 gün; hesap ayarı değişince yeni aksiyonlara uygulanır | FR-0903, BR-10 | B | v1 |
| TC-070 | Idempotent oluşturma | Aynı madde cevabı iki kez senklenir → tek aksiyon | FR-0902 | A | v1 |
| TC-071 | Aksiyon bildirimleri | Atandı, vadeye 2 sa, gecikti, kapatıldı → teslimat izi | FR-0910 | A | v1 |
| TC-072 | Toplu kapatma yok | Çoklu seçim + kapat → arayüzde yok; API toplu uç nokta yok | FR-0907 | M | v1 |

## UC-13 · Eskalasyon

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-073 | Kaçırılan çalıştırma merdiveni | Tolerans sonu → şube müdürü push; +2 sa bölge push+SMS (kritik liste); +24 sa merkez | BR-11, FR-0912 | B/A | v1 (sabit kural) |
| TC-074 | Gecikmiş aksiyon merdiveni | Vade + 0 atanan; +4 sa üst rol; +24 sa merkez | BR-11 | B | v1 (sabah özeti) |
| TC-075 | Adım logu | Her adım olay günlüğü ve aksiyon yorumunda | FR-0913 | A | v1 |
| TC-076 | Durdurma | "Yapılmayacak" veya aksiyon kapanışı → kalan adımlar iptal | FR-0914 | B | v1 |
| TC-077 | Alıcı yok | Şube müdürü pasif → adım bölgeye geçer, "alıcı yok" olayı, hesap yöneticisine uyarı | FR-0915 | A | v1 |
| TC-078 | Sessiz saatler | 02:00'de orta öncelikli bildirim → 07:00'ye ertelenir; kritik/eskalasyon anında | BR-23, FR-1004 | B | v1 (sabit) |

## UC-14 · Duyuru

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-079 | Hedefleme ve sayı | Akıllı grup hedefi → kitle sayısı doğru; yayın sonrası hedef dışı kullanıcı görmez | FR-1102 | A | v1.1 |
| TC-080 | Onay zaman damgası | "Okudum" → zaman damgalı; geri alınamaz | FR-1103, BR-25 | E | v1.1 |
| TC-081 | Hatırlatma | 48 sa sonra onaylamayanlara otomatik push; elle hatırlat | FR-1104 | B/A | v1.1 |
| TC-082 | Onay raporu | Oran, listeler, dışa aktarım | FR-1105 | A | v1.1 |
| TC-083 | Bugün şeridi | Onay bekleyen duyuru Bugün'ün üstünde; onaylanınca kaybolur | FR-1103 | E | v1.1 |
| TC-084 | İmza zorunlu (Should) | İmzasız onay → engellenir | FR-1106 | E | v1.1 |

## UC-15 · İzleme ve raporlar

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-085 | Izgara doğruluğu | 25 şube × 5 liste; durumlar veri ile birebir; 60 sn yenileme | FR-1201 | E | v1 |
| TC-086 | Izgara performansı | 100 şube × 5 liste ilk boyama < 2 sn | NFR-03 | A | v1 |
| TC-087 | Çalıştırma detayı | Cevaplar, kanıt küçük resim/tam boy (imzalı URL 15 dk), puan, aksiyonlar, olay izi | FR-1202 | E | v1 |
| TC-088 | Tamamlanma raporu | 30 gün: pencere içi/geç/kaçırıldı/yapılmayacak/kapalı oranları hesaplanmış veriyle eşleşir | FR-1203 | A | v1 |
| TC-089 | Şube sıralaması | Yalnızca şube/bölge düzeyi; kişi düzeyi sıralama uç noktası yok | FR-1204, BR-20 | A | v1.1 |
| TC-090 | Başarısız madde ısı haritası | İlk 10 madde ve şube × madde matrisi doğru | FR-1205 | A | v1.1 |
| TC-091 | Ölçüm günlüğü | Buzdolabı 2, 30 gün → seri, aralık dışı işaretli | FR-1207 | A | v1 |
| TC-092 | Kanıt galerisi filtreleri | Şube/istasyon/madde/tarih → doğru küme; yetki kapsamı | FR-1208 | A | v1 |
| TC-093 | Kişi düzeyi takip | Şube müdürü: Emre'nin eksik/gecikmiş maddeleri; personel kendi kaydını görür; puan alanı yok | FR-1210, BR-20 | A | v1.1 |
| TC-094 | Yönetici mobil görünümü | Bölge ızgarası, aksiyon kapatma, kanıt görüntüleme | FR-1211 | M | v1 (Bölgem listesi) |

## UC-16 · Dışa aktarım

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-095 | Çalıştırma PDF'i | İçerik tam: maddeler, cevaplar, küçük resimler, zaman damgaları, doğrulama kodu, marka | FR-1213 | E | v1 |
| TC-096 | Dönem PDF'i | 30 gün soğuk zincir → sayfa damgaları, aralık dışı işaretler | FR-1214 | E | v1 |
| TC-097 | Excel | Filtreli ham veri; sütunlar belgelenmiş | FR-1215 | A | v1.1 |
| TC-098 | Paylaşım bağlantısı | 7 gün süreli; süre sonunda 410; iptal edilebilir | FR-1216 | A | v1.1 |
| TC-099 | Arka plan üretim | 600 çalıştırma → asenkron; bildirim ve indirme | FR-1217 | A | v1 (dönem PDF) |

## UC-17 · Denetim izi

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-100 | Ekle-yalnız | Olay güncelleme/silme uç noktası yok; veritabanı rolü UPDATE/DELETE yetkisiz | FR-1301 | A | v1 |
| TC-101 | Zincir doğrulama | 18.000 olay → doğrulama tutarlı; bir kaydı elle değiştir → kırılma noktası raporlanır | FR-1304 | A | v1 |
| TC-102 | Günlük kök ve RFC 3161 | 04:00 kök hesaplanır, damga alınır (sahte TSA), saklanır | FR-1302 | A | v1.1 |
| TC-103 | Görüntüleyici | Çalıştırma bazlı olay listesi okunabilir; PDF eki | FR-1303 | E | v1.1 |

## UC-18 · KVKK

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-104 | Maskeleme | Talep → ad/telefon maskeli; cevaplar ve kanıtlar iş kaydı olarak duruyor; log | FR-1310 | A | v1 (destek betiği) |
| TC-105 | Saklama | Saklama 6 ay; 7 aylık kanıt → zamanlayıcı siler, KANIT.silindi_mi, cevap değeri kalır, rapor | FR-1311, BR-21 | A | v1 |
| TC-106 | Dışa aktarma | ZIP: profil JSON, cevaplar CSV, kanıt dosyaları; 30 gün içinde | FR-1309 | A | v1.1 |
| TC-107 | Aydınlatma sürümü | Metin güncellenir → tüm kullanıcılara yeniden gösterilir; eski onay kayıtları korunur | FR-1307 | E | v1 |

## UC-19 · Günlük atama

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-108 | Yeniden atama | Kapanış → Zeynep → Zeynep'te görünür, Emre'de kaybolur; push; log | FR-0519, FR-0520 | E | v1 |
| TC-109 | Herkes tamamlasın ekle/çıkar | Kişi ekle → bölüm açılır; çıkar → tamamlanma hesabı güncellenir | FR-0519 | A | v1 |
| TC-110 | Yetki | Personel API ile atama değiştirir → 403 | FR-0205 | A | v1 |

## UC-20 · Gözden geçirme (Should)

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-111 | Gözden geçirildi | Bölge müdürü işaret + not → detayda görünür; log | FR-1701 | E | v1.1 |
| TC-112 | İkinci imza | Kalite imzası kaydedilir, PDF'te görünür | FR-1702 | E | v1.1 |

## v1 eklemeleri (ADR-0008, E-1…E-7)

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-113 | Şube müdürü PIN atar | Telefonsuz personel kayıtlı → Ayşe kioskta "PIN ata" → 4 haneli PIN üretilir, logda "PIN atandı Ayşe → Deniz"; Deniz PIN ile girer → ilk girişte değiştirme istenir; eski PIN geçersiz | FR-0211 | E | v1 |
| TC-114 | Sabit kural: başarısız cevapta kanıt | "Hayır" / "Uygun değil" / aralık dışı → fotoğraf ve not olmadan kaydedilemez; kritik değilse aksiyon açılmaz; kritikse aksiyon (şube müdürü, 4 sa) | FR-0405, BR-06 | E | v1 |
| TC-115 | Çalıştırma kilidi: ilk açan alır | Atanmamış çalıştırma; Emre açar → diğer cihazlarda "Emre yapıyor", madde cevaplanamaz; 30 dk kilit yenileme; Emre kapatınca kilit düşer; şube müdürü kilidi kaldırabilir | FR-0521, BR-26 | E | v1 |
| TC-116 | Açılışta "dün gece" bloğu | Dün kapanışta 1 yapılamadı + 1 kritik başarısız → açılış listesinin başında blok (sebep ve notla); sorun yoksa "Dün gece sorun yok"; blok cevap istemez, sayılmaz; kapalı günden sonra son iş günü esas alınır | FR-0613 | E | v1 |
| TC-117 | Kritik anında bildirim ve SMS | 23:20 kritik aralık dışı → şube ve bölge müdürüne anında push (sessiz saat muaf); 10 dk içinde teslim/okunma yoksa SMS (sahte sağlayıcıda görünür); okunan push için SMS gitmez; teslim izi logda | FR-1008, BR-11 | B | v1 |
| TC-118 | İstisna görünümü ve "her şey yolunda" | Dün gece 2 sorunlu hücre → pano varsayılanı yalnızca bu satırları listeler, ızgara "tümünü göster" ile açılır; sorunsuz gün → "Dün gece her şey yolunda" durumu; mobil Bölgem listesi aynı kaynaktan | FR-1219, FR-1201 | E | v1 |
| TC-119 | Aylık tek sayfa özet | Ağustos verisiyle → % zamanında, geç, kaçırıldı, yapılmayacak; başarısız ve yapılamadı sayıları; şube kırılımı; PDF üretilir, doğrulama kodu ve üretim zamanı var; rakamlar hesaplanmış veriyle eşleşir | FR-1220 | A | v1 |

## v1 eklemeleri (E-11 kanıt bütünlüğü, E-12 belge takvimi)

| TC | Test | Ön koşul → Adımlar → Beklenen | FR/BR | Oto | Sürüm |
|---|---|---|---|---|---|
| TC-120 | Aynı fotoğrafın ikinci kez gönderilmesi | Emre dün kapanışta A fotoğrafını gönderdi → bugün aynı dosyayı yüklemeyi dener → yükleme reddedilir, "bu fotoğraf daha önce gönderildi, yeniden çekin"; deneme olay günlüğüne yazılır; farklı bir fotoğraf kabul edilir | FR-0614 | A | v1 |
| TC-121 | Kanıt bayrakları | Galeriden yükleme denemesi · konum şubeden 300 m uzakta · cihaz saati 25 dk ileri → üç bayrak cevapta saklanır; çalıştırma detayında ve çalıştırma PDF'inde görünür; bayrak metni suçlama değil "incelenmeli" ifadesidir | FR-0615 | E | v1 |
| TC-122 | Şüpheli kanıt filtresi | Panoda "şüpheli kanıt" filtresi açılır → yalnızca bayraklı çalıştırmalar listelenir; bayraksız gün için liste boş ve "bayrak yok" der | FR-0615 | E | v1 |
| TC-123 | Belge kaydı ve dosyası | Yangın tüpü dolum belgesi: şube, geçerlilik bitişi, sorumlu, PDF → kayıt oluşur, dosya damgalanır ve SHA-256'sı bağlanır; geçmiş tarihli bitiş girilirse uyarı ile kaydedilir ve "süresi geçmiş" işaretlenir | FR-0522 | E | v1 |
| TC-124 | Belge uyarıları ve süresi geçende aksiyon | Bitişe 30 ve 7 gün kala sorumluya ve şube müdürüne push + sabah özeti satırı; tarih geçince yüksek öncelikli aksiyon (7 gün vade) açılır ve şube "belge eksik" işaretlenir; belge yenilenince aksiyon kapanır ve işaret kalkar | FR-0523 | A | v1 |
| TC-125 | Belge görünümü ve dönem PDF'i | Zincir genelinde "yaklaşanlar ve süresi geçenler" listesi (şube × belge türü) sıralı gelir; dönem PDF'i doğrulama kodu ve üretim zamanı taşır | FR-0524 | E | v1 |
