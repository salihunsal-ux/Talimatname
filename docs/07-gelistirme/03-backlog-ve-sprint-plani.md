# Backlog ve sprint planı (v1 çekirdek)

ADR-0008 ile yeniden çizildi (13 Eylül 2026). Epic = yetenek (CAP). Hikâye = kullanıcı bakışıyla, FR'lere bağlı, kabul testi (TC) ile kapanır. Boyut: S (≤ 2 gün), M (3–5 gün), L (6–10 gün; bölünmeli). Ekip: 1 mobil, 1 backend/web (Sprint 5'ten itibaren yarı zamanlı web desteği), kurucu-PO, yarı zamanlı tasarımcı, Sprint 6'dan itibaren yarı zamanlı QA. Sprint = 2 hafta, ~16 geliştirici günü. **Hikâye numaraları eski plandan korunur;** v1'de daraltılan hikâyeler "(v1: …)" notuyla, ertelenenler alttaki v1.1 listesinde. Yeni hikâyeler ST-139'dan başlar.

## Kilometre taşları

| Sprint | Taş | Ölçüt |
|---|---|---|
| S6 sonu | **Alfa** | 1 tasarım-ortağı zincir, 5 şube, kapanış listesi kioskta; kanıt ve sabah özeti çalışıyor |
| S8 sonu | **Beta** | 3 pilot zincir, 30+ şube; açılış + kapanış + soğuk zincir; ızgara, PDF |
| S10 sonu | **GA** | v1 satırlarının tamamı; 89 v1 kabul testi %100; pilot UAT imzası |
| S11–S12 | Tampon / v1.1 başlangıcı | Pilot bulguları; v1.1 sırasının ilk maddeleri |

## Epic listesi

| EP | Epic | CAP | Sprint |
|---|---|---|---|
| EP-01 | Hesap, organizasyon, içe aktarma, sihirbaz | CAP-01, CAP-14 | S1–S2 |
| EP-02 | Kimlik, 4 rol, kiosk | CAP-02 | S1, S6 |
| EP-03 | Basit şablon editörü, 8 şablon, sabit kural | CAP-03, CAP-04 | S2, S4, S9 |
| EP-04 | Planlama ve çalıştırma motoru | CAP-05 | S3 |
| EP-05 | Mobil yürütme ve kanıt | CAP-06 | S2–S5 |
| EP-06 | Çevrimdışı senk | CAP-07 | S5–S6 |
| EP-07 | Yapılamadı, sorun, aksiyon (açık/kapalı), sabit eskalasyon, sabah özeti | CAP-08, CAP-09, CAP-10 | S5–S6, S8 |
| EP-08 | Istisna odaklı pano, detay, galeri, Bölgem | CAP-12 | S7 |
| EP-09 | Sıcaklık günlüğü, PDF'ler, aylık özet | CAP-12 | S8 |
| EP-10 | Hash zinciri, KVKK süreçleri, güvenlik temel | CAP-13 | S9 |
| EP-11 | Sertleştirme, performans, GA | — | S10 |
| EP-12 | v1.1 | CAP-11, 15–18 ve ertelenenler | S11+ |

## Sprint planı ve hikâyeler

Biçim: ST · hikâye · FR · TC · boyut. Kabul kriteri = bağlı TC'ler (v1 sürüm etiketli) + kart notları.

### S0 — Altyapı (02-repo kontrol listesi)
Depolar, CI, dev compose, staging (TR), sağlayıcı hesapları, tasarım token'ları kodda, tohum v0, spesifikasyon fikstürleri (pencere/durum, puan, sabit kural), backlog aracı.

### S1 — Temel: hesap, hiyerarşi, OTP, 4 rol
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-001 | Backend: hesap/kiracı modeli, RLS, `audit.emit()` altyapısı | FR-0101, FR-1301 | TC-011, TC-100 | M |
| ST-002 | Backend: hiyerarşi (bölge, şube, istasyon, takvim) CRUD | FR-0102…0104, FR-0515 | TC-001 | M |
| ST-003 | Backend: Excel içe aktarma (şube/istasyon) + doğrulama raporu | FR-0105, FR-0106 | TC-001…003 | M |
| ST-004 | Backend: OTP giriş, belirteçler, oturum yönetimi, hız sınırı | FR-0201, 0203, 0204 | TC-009 | M |
| ST-005 | Backend: 4 rol × kapsam yetki katmanı (bağımlılık) | FR-0205 | TC-006, 010 | M |
| ST-006 | Web: giriş (e-posta/şifre, şifre politikası), kabuk (menü, rol kapsamı) | FR-0202 | — | S |
| ST-007 | Web: şubeler sayfası (ağaç + detay + takvim) | FR-0102, 0103 | TC-001 | M |
| ST-008 | Web: kurulum sihirbazı adım 1–2 (marka + şubeler) | FR-1401 | TC-004 | M |
| ST-009 | Mobil: giriş (OTP), aydınlatma, konum izni ekranları | FR-0201, 1307, 1308 | TC-012 | M |
| ST-010 | Tohum betiği v0 + CI E2E iskeleti | — | — | S |

### S2 — Personel, basit şablon editörü, mobil Bugün
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-011 | Backend: kullanıcı CRUD, davet SMS'i, pasifleştirme; maskeleme destek betiği | FR-0107…0110 | TC-005, 007, 104 | M |
| ST-013 | Web: personel sayfası, rol/kapsam, davet (v1: grup yok) | FR-0107, 0205 | TC-005…007 | M |
| ST-014 | Backend: şablon/sürüm/bölüm/madde modeli ve yayın doğrulaması (v1: 6 tür, 3 ayar) | FR-0301…0304, 0312 | TC-021, 022 | M |
| ST-015 | Backend: yüzde puan + kritik kuralı saf fonksiyonu, fikstürler | FR-0306, 0307 | TC-020 | S |
| ST-016 | Web: şablon listesi ve basit editör (madde listesi, tür, 3 kutu, sıcaklık aralığı) | FR-0302…0305 | TC-018 | M |
| ST-017 | Web: yayın (hemen) ve sürüm görünümü | FR-0301 | TC-021 | S |
| ST-018 | Mobil: kabuk, sekmeler, tema token'ları, Bugün ekranı (çevrimiçi) | FR-0601 | TC-039 | M |
| ST-019 | Mobil: üretilmiş API istemcisi, oturum yenileme | FR-0203 | — | S |
| ST-021 | Web: kurulum sihirbazı adım 3–4 (kapanış şablonu + plan önerisi + personel), yayın | FR-1401 | TC-004 | M |
| ST-024 | Sentetik fotoğraf üreteci (tohum) | — | — | S |

### S3 — Plan ve çalıştırma motoru; madde cevaplama
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-025 | Backend: plan modeli, RRULE, pencere/tolerans, gece yarısı, DST | FR-0501…0507 | TC-025…028, 032 | L→2 |
| ST-026 | Backend: çalıştırma üretimi (7 gün, benzersiz), kapalı gün | FR-0513, 0515 | TC-030, 033 | M |
| ST-027 | Backend: durum makinesi (tablo güdümlü), zamanlayıcı geçişleri | FR-0514 | TC-034 | M |
| ST-028 | Backend: atama modeli (v1: rol/kişi/şubedeki herkes, biri tamamlasın) | FR-0508 | — | S |
| ST-139 | Backend + mobil: çalıştırma kilidi — ilk açan alır, "X yapıyor" rozeti, kilit yenileme/bırakma, şube müdürü kaldırır (E-2) | FR-0521, BR-26 | TC-039 | M |
| ST-029 | Web: plan editörü (kapsam, tekrar, pencere, atama; sabit hatırlatma/eskalasyon bilgisi) + 7 gün önizleme | FR-0501…0512 | TC-030, 031 | M |
| ST-030 | Backend: cevap yazma (idempotent), gönderim, puan/durum | FR-0602, 0607 | TC-040 | M |
| ST-031 | Mobil: liste çalıştırma ekranı (bölümler, ilerleme, geri sayım) | FR-0601, 0603, 0610 | TC-039, 048 | M |
| ST-032 | Mobil: madde bileşenleri (onay, seçim, sayı, sıcaklık, metin, talimat) | FR-0303, 0305 | TC-018, 019 | M |
| ST-033 | Mobil: gönderim kilidi ve sonuç | FR-0607 | TC-040 | S |
| ST-034 | Spesifikasyon fikstürleri: pencere/durum | — | TC-025, 034 | S |
| ST-035 | Backend: plan değişikliği yeniden hesap; çakışma engeli | FR-0516, 0517 | TC-031, 037 | S |
| ST-037 | Backend: tek seferlik liste | FR-0512 | — | S |
| ST-038 | Tohum: 25 şube, 8 plan, 30 gün geçmiş | — | — | M |

### S4 — Kanıt, damga, sabit kural, push
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-039 | Backend: ön imzalı yükleme, tamamlama, hash doğrulama | FR-0606 | TC-043 | M |
| ST-040 | İşçi: damgalama ve küçük resim | FR-0606 | TC-043 | M |
| ST-041 | Mobil: kamera doğrudan açılır (2 dokunuş), yalnızca kamera, 1–3 fotoğraf, sıkıştırma | FR-0604, 0605 | TC-041, 042 | M |
| ST-043 | Mobil: konum yakalama ve bayraklar | FR-0606, BR-15 | TC-044 | S |
| ST-140 | Backend + mobil: sabit kural — başarısız cevapta fotoğraf + not; kritik → aksiyon; ortak fikstürler (E-… FR-0405) | FR-0405, BR-06, BR-08 | TC-019, 023, 046 | M |
| ST-044 | Backend: bildirim servisi (kanal-bağımsız), push sürücüsü, teslimat izi | FR-1001, 1005…1007 | TC-035 | M |
| ST-045 | Backend: sabit iki hatırlatma (açılış, −30 dk) | FR-0509 | TC-035 | S |
| ST-046 | Mobil: push alma, derin bağlantı | FR-1001 | TC-035 | S |
| ST-048 | Web: çalıştırma detayı v1 (cevaplar, kanıt) | FR-1202 | TC-087 | M |
| ST-049 | Backend: imzalı süreli kanıt URL'leri | FR-1305 | TC-087 | S |
| ST-050 | Performans ölçüm protokolü ilk koşu (Galaxy A05) | NFR-02 | — | S |

### S5 — Çevrimdışı; yapılamadı; dün gece özeti
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-051 | Mobil: yerel veritabanı (şifreli), önbellek manifesti | FR-0701 | TC-051 | M |
| ST-052 | Mobil: yazma kuyruğu (cevap + kanıt), "bekliyor" rozeti | FR-0702 | TC-051 | M |
| ST-053 | Mobil: arka plan senk servisi, üstel yeniden deneme | FR-0703, 0707 | TC-051, 053 | L→2 |
| ST-054 | Backend: `/sync/manifest`, `/sync/batch`, zaman düzeltmesi | FR-0704 | TC-052, 053 | M |
| ST-057 | Mobil: yapılamadı alt sayfası (sabit sebep seti, kritikte yok) | FR-0801, 0803, 0804 | TC-057…060 | M |
| ST-059 | Mobil: senk durumu ekranı | FR-0708 | TC-056 | S |
| ST-060 | Backend: kuyruk sınırları ve geç senk bayrağı | FR-0706 | TC-054 | S |
| ST-061 | Mobil: kaldığı yerden devam (tek kullanıcı) | FR-0603 | TC-048 | S |
| ST-141 | Backend + mobil: açılış listesinde "dün gece" bloğu (E-3) | FR-0613 | TC-039 | S |
| ST-062 | Web: pano hücre → detay, durum lejantı | FR-1201 | TC-085 | S |

### S6 — Senk dayanıklılığı; aksiyon (açık/kapalı); sabit eskalasyon; kiosk; sabah özeti → Alfa
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-063 | Backend: senk çakışma kuralı ve 100 tekrar dayanıklılık testi | FR-0705 | TC-055 | M |
| ST-064 | Backend: aksiyon modeli (açık/kapalı), otomatik oluşturma (idempotent), sabit vadeler | FR-0901…0903 | TC-065, 069, 070 | M |
| ST-065 | Backend: kapatma (not zorunlu), not ekleme | FR-0904, 0905 | TC-066, 067 | S |
| ST-066 | Backend: sabit eskalasyon kuralı (kaçırıldı → şube müdürü anında; kritik → anında + SMS gecikmesi; sabah özetine biriktirme) | FR-0911…0915, FR-1008 | TC-073…077 | M |
| ST-143 | Backend + e-posta: sabah özeti 07:00 (bölge müdürü, yönetici) push + e-posta (E-5) | FR-1212, BR-27 | TC-074 | M |
| ST-067 | Backend: SMS sürücüsü (OTP + kritik yedek), sabit sessiz saat | FR-1002, 1004 | TC-036, 078 | S |
| ST-068 | Mobil: aksiyonlarım listesi ve detay (açık/kapalı, not, kapatma) | FR-0907, 0905 | TC-065…067 | M |
| ST-069 | Web: aksiyonlar sayfası (basit) | FR-0907 | TC-065 | S |
| ST-070 | Backend: kiosk cihaz kaydı (QR), PIN, kısa ömürlü belirteç | FR-0207, 0208, 0210 | TC-008, 013, 015 | M |
| ST-071 | Mobil: kiosk kilit ekranı, hareketsizlik, PIN sıfırlama | FR-0208…0210 | TC-013…016 | M |
| ST-142 | Backend + mobil: şube müdürü personele başlangıç PIN'i atar (E-1) | FR-0211 | TC-013 | S |
| ST-072 | Web: cihaz yönetimi (kiosk QR, kaldırma) | FR-0207 | TC-008 | S |
| ST-073 | Backend: yapılmayacak akışı | BR-04, FR-0914 | TC-038 | S |
| ST-075 | Backend: aksiyon bildirimleri (atandı anında; gecikti sabah özetinde) | FR-0910 | TC-071 | S |
| ST-076 | Alfa hazırlığı: tasarım ortağı hesabı, 5 şube, kapanış şablonu, kiosk kurulumu | — | — | S |

### S7 — İstisna odaklı pano, detay, galeri, Bölgem
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-077 | Backend: ızgara sorgusu (gün, filtre, istisna görünümü), 60 sn yenileme, performans | FR-1201, 1219, NFR-03 | TC-085, 086 | M |
| ST-078 | Web: pano (istisna odaklı varsayılan, "her şey yolunda", tümünü göster, KPI) | FR-1201, 1219 | TC-085 | M |
| ST-079 | Web: çalıştırma detayı tam (kanıt tam boy, damga meta, aksiyonlar, olay izi özeti) | FR-1202 | TC-087 | M |
| ST-080 | Backend + web: kanıt galerisi (şube + tarih) | FR-1208 | TC-092 | S |
| ST-081 | Backend: günlük yeniden atama | FR-0519, 0520 | TC-108, 110 | S |
| ST-144 | Mobil: "Bölgem/Şubem" listesi (şube × dün gece durumu → detay) + şube müdürü günlük atama | FR-1211, 0519 | TC-094, 108 | M |
| ST-083 | Web: günlük atama (pano) | FR-0519 | TC-108 | S |
| ST-084 | Alfa geri bildirim düzeltmeleri | — | — | M |
| ST-086 | Mobil: sorun bildir (sabit kategori) | FR-0806 | TC-062 | S |
| ST-093 | Backend + web: sorun → aksiyona çevir / kapat | FR-0807 | TC-063 | S |

### S8 — Sıcaklık günlüğü, PDF'ler, aylık özet → Beta
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-088 | Backend: ölçüm günlüğü sorgusu (ekipman zaman serisi, aralık dışı) | FR-1207 | TC-091 | M |
| ST-091 | İşçi: çalıştırma PDF'i (markalı, doğrulama kodu) | FR-1213, 1218 | TC-095 | M |
| ST-092 | İşçi: dönem PDF'i (sıcaklık günlüğü), arka plan üretim | FR-1214, 1217 | TC-096, 099 | M |
| ST-145 | Backend + web: aylık tek sayfa özet (E-7) + PDF | FR-1220 | TC-088 | M |
| ST-090 | Web: raporlar sayfası (aylık özet, sıcaklık günlüğü, galeri) | FR-1207, 1208, 1220 | TC-088, 091, 092 | M |
| ST-094 | Web: personel oturum sonlandırma; hesap sayfası (marka, tatil takvimi, aydınlatma metni) | FR-0203, 1402 (minimal) | TC-007 | S |
| ST-097 | Mobil: erişilebilirlik geçişi (44 px, etiketler, %130) | FR-0611 | TC-050 | S |
| ST-098 | Cihaz matrisi otomasyonu (Firebase Test Lab gece) | NFR-06 | — | S |
| ST-106 | Beta hazırlığı: 3 pilot hesabı, veri işleme sözleşmesi, staging zaman aracı | — | — | M |
| ST-107 | Backend: personel Excel içe aktarma | FR-0105 | TC-005 | S |

### S9 — Hash zinciri, 8 şablon, KVKK süreçleri, güvenlik
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-099 | Backend: hash zinciri ve günlük kök (TSA v1.1) | FR-1301 | TC-100, 101 | M |
| ST-100 | Backend: zincir doğrulama komutu (iç araç) | FR-1304 | TC-101 | S |
| ST-102 | İçerik: 8 Türkçe yeme-içme şablonu (kalite incelemeli) | FR-0311 | TC-017 | M (PO + danışman) |
| ST-103 | Backend + web: kütüphane kopyalama, merkezî güncelleme | FR-0311 | TC-017 | S |
| ST-104 | Web: şablon editörü — şablon ayarları (yalnızca kamera, başarısızda kanıt), önizleme, doğrulama tam | FR-0308, 0309, 0312 | TC-022 | M |
| ST-105 | Mobil: tolerans/kilit davranışları, geç gönderim | FR-0610, BR-02/03 | TC-045 | S |
| ST-109 | Backend: aydınlatma sürümleri, yeniden onay | FR-1307 | TC-107 | S |
| ST-112 | Zamanlayıcı: saklama silme (sabit 24 ay) ve rapor | FR-1311 | TC-105 | M |
| ST-118 | Güvenlik: ASVS/MASVS kontrol listesi, bağımlılık taraması, hız sınırları | NFR-09 | — | M |
| ST-119 | Backend: faturalama sayacı | FR-1403 | — | S |
| ST-108 | Beta düzeltmeleri | — | — | M |
| ST-146 | Destek betiği: KVKK dışa aktarma / maskeleme (süreç belgesiyle) | FR-1309, 1310 | TC-104, 106 | S |

### S10 — Sertleştirme ve GA
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-126 | Performans: ızgara 100 şube, PDF < 30 sn, k6 yük profili (22:00–01:00) | NFR-03, 04 | TC-086 | M |
| ST-129 | Mobil: düşük cihaz optimizasyonu (soğuk açılış < 3 sn) | NFR-02 | — | M |
| ST-131 | Dış sızma testi bulgularının kapatılması | NFR-09 | — | M |
| ST-132 | Kurtarma tatbikatı (yedekten geri yükleme), RPO/RTO doğrulama | NFR-13 | — | S |
| ST-133 | v1 kabul testleri (89) %100 koşusu ve hata kapanışı | — | — | L |
| ST-134 | Mağaza yayın hazırlığı (gizlilik etiketleri, ekran görüntüleri, sürüm notları) | — | — | S |
| ST-135 | Uyum kontrol listesi (06-kvkk) kapanışı | NFR-10 | — | S |
| ST-136 | İzleme ve uyarılar üretim ayarı; çalışma kitapları | NFR-12 | — | M |
| ST-137 | Onboarding oyun kitabı ve destek SSS | NFR-16 | — | S |
| ST-120 | Beta/pilot düzeltmeleri | — | — | M |

### S11–S12 — Tampon ve v1.1 başlangıcı
Pilot bulguları önce. Kalan kapasite v1.1 sırasına göre (aşağıdaki liste).

## v1.1 backlog'u (ertelenen hikâyeler, ID'ler korundu)

| Sıra | Konu | ST'ler | FR |
|---|---|---|---|
| 1 | Duyuru ve onay (+ imza) | ST-114, 115, 116, 125, 095 | FR-1101…1106 |
| 2 | Koşul editörü ve kural deneme | ST-055, 056 | FR-0401…0404 |
| 3 | "Herkes tamamlasın" ve madde bazlı kilit | ST-028 (kalan), ST-047 | FR-0508 (kalan), 0609 |
| 4 | Aksiyon durum makinesi, yorum dizisi, onaylı kapanış | ST-065 (kalan), ST-124 | FR-0904 (kalan), 0906, 0909 |
| 5 | Raporlar: tamamlanma/sıralama, başarısız madde ısı haritası, sebep dağılımı, aksiyon raporu, kişi takibi | ST-087, 089, 085 | FR-1203…1206, 1209, 1210, 0805 |
| 6 | Denetim izi ekranı, RFC 3161 | ST-101, ST-099 (TSA) | FR-1302, 1303 |
| 7 | KVKK talep ekranı, ayarlanabilir saklama | ST-110, 111, 113 | FR-1309, 1310 (ekran), 1311 (ayar) |
| 8 | 2FA | ST-117 | FR-0202 (2FA) |
| 9 | Ayarlar paneli (parametreler, eskalasyon şablonları, sebep/kategori setleri, tercihler) | ST-022, 023, 096 | FR-1402, 0802, 0809, 1003, 0510 |
| 10 | Excel dışa aktarım, paylaşım bağlantısı | ST-092 (kalan) | FR-1215, 1216 |
| 11 | Video, imza, barkod/QR, tarih-saat bileşenleri; ek kayıt | ST-042, ST-047 | FR-0303 (kalan), 0608 |
| 12 | QR ile istasyondan başlatma; sorun yükseltme | ST-121 | FR-0612, 0808 |
| 13 | Akıllı gruplar, Gözlemci rolü | ST-012 | FR-0206 |
| 14 | Şube türü varyantı; AI taslak şablon; tarihli yayın | ST-127, 138 | FR-1501, 1502, 0310 |
| 15 | Salt okunur API, webhook; sabah özeti dışındaki planlı raporlar | — | FR-1801, 1802 |
| — | Yerine E-3 geçti: vardiya devri notu | ST-122 | FR-1601 |
| — | Destek modu (tam) | ST-130 | NFR-16 |

## Kapasite notu

v1'de 102 hikâye (S1–S10), 7'si L (bölünmüş). 10 sprint × ~16 gün ≈ 160 geliştirici günü; S/M/L ortalaması 1,5/4/8 gün kabulüyle ~150 gün → **plan artık tampon içeriyor** (S11–S12 ayrıca). Riskli sprintler S3–S6 (motor + çevrimdışı) değişmedi; kayma olursa S8 (PDF/aylık özet) S9'a kayar, Beta bir sprint ötelenir, GA S10 korunur.
