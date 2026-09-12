# Backlog ve sprint planı

Epic = yetenek (CAP). Hikâye = kullanıcı bakışıyla, FR'lere bağlı, kabul testi (TC) ile kapanır. Boyut: S (≤ 2 gün), M (3–5 gün), L (6–10 gün; bölünmeli). Ekip: 1 mobil, 1 backend/web (Sprint 5'ten itibaren yarı zamanlı web desteği), kurucu-PO, yarı zamanlı tasarımcı, Sprint 7'den itibaren yarı zamanlı QA. Sprint = 2 hafta. Kapasite: ~16 geliştirici günü/sprint.

## Epic listesi

| EP | Epic | CAP | Hedef sprint |
|---|---|---|---|
| EP-01 | Hesap, organizasyon, içe aktarma | CAP-01, CAP-14 | S1–S2 |
| EP-02 | Kimlik, yetki, kiosk | CAP-02 | S1–S2, S8 |
| EP-03 | Şablon editörü ve kütüphane | CAP-03, CAP-04 | S2–S3, S9 |
| EP-04 | Planlama ve çalıştırma motoru | CAP-05 | S3–S4 |
| EP-05 | Mobil yürütme ve kanıt | CAP-06 | S3–S5 |
| EP-06 | Çevrimdışı senk | CAP-07 | S5–S6 |
| EP-07 | Yapılamadı, sorun, aksiyon, eskalasyon | CAP-08, CAP-09 | S5–S6 |
| EP-08 | Bildirimler | CAP-10 | S4, S6 |
| EP-09 | Duyuru ve onay | CAP-11 | S10 |
| EP-10 | Pano, raporlar, dışa aktarım | CAP-12 | S7–S8 |
| EP-11 | Denetim izi, KVKK, güvenlik | CAP-13 | S9–S10 |
| EP-12 | Should'lar (QR, devir notu, sabah özeti, AI taslak, gözden geçirme) | CAP-15…18 | S11–S12 (kalan süreye göre) |
| EP-13 | Sertleştirme, performans, pilot düzeltmeleri, GA | — | S11–S12 |

## Sprint planı

| Sprint | Hedef | Hikâyeler (ST) | Kilometre taşı |
|---|---|---|---|
| S0 | Altyapı (02-repo) | iskeletler, CI, staging, token'lar, spesifikasyon fikstürleri | — |
| S1 | Temel: hesap, hiyerarşi, OTP | ST-001…ST-010 | |
| S2 | Personel/rol, şablon editörü v1, mobil iskelet + Bugün | ST-011…ST-024 | |
| S3 | Plan, RRULE, çalıştırma üretimi; madde cevaplama | ST-025…ST-038 | |
| S4 | Kanıt yakalama, damga, gönderim/puan; push | ST-039…ST-050 | |
| S5 | Çevrimdışı kuyruk; yapılamadı, koşullu mantık | ST-051…ST-062 | |
| S6 | Senk çakışma; aksiyonlar, eskalasyon, SMS yedek; kiosk | ST-063…ST-076 | **Alfa (S6 sonu): 1 tasarım ortağı, 5 şube, kapanış** |
| S7 | Pano ızgarası, çalıştırma detayı, kanıt galerisi | ST-077…ST-086 | |
| S8 | Raporlar, PDF/Excel, sorun bildir, yönetici mobil | ST-087…ST-098 | |
| S9 | Olay günlüğü ve zincir, denetim izi, kütüphane 30 şablon | ST-099…ST-108 | **Beta (S9 sonu): 3 pilot, 30+ şube** |
| S10 | KVKK akışları, saklama, duyuru-onay, 2FA, güvenlik | ST-109…ST-120 | |
| S11 | Pilot geri bildirimi, Should'lar (QR, devir notu, sabah özeti), performans | ST-121…ST-130 | |
| S12 | Sertleştirme, yük/sızma testi, kurtarma tatbikatı, GA | ST-131…ST-138 | **GA (S12 sonu)** |

## Hikâyeler

Biçim: `ST · [rol] olarak … istiyorum, böylece … · FR · TC · boyut`. Kabul kriteri = bağlı TC'ler; ek kriterler hikâye kartında.

### S1 — Temel
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-001 | Backend: hesap/kiracı modeli, RLS, `audit.emit()` altyapısı | FR-0101, FR-1301 | TC-011, TC-100 | M |
| ST-002 | Backend: hiyerarşi (bölge, şube, istasyon, takvim) CRUD | FR-0102…0104, FR-0515 | TC-001 | M |
| ST-003 | Backend: Excel içe aktarma (şube/istasyon) + doğrulama raporu | FR-0105, FR-0106 | TC-001…003 | M |
| ST-004 | Backend: OTP giriş, belirteçler, oturum yönetimi, hız sınırı | FR-0201, 0203, 0204 | TC-009 | M |
| ST-005 | Backend: rol × kapsam yetki katmanı (bağımlılık) | FR-0205 | TC-006, 010 | M |
| ST-006 | Web: giriş (e-posta/şifre), kabuk (menü, rol kapsamı) | FR-0202 | — | S |
| ST-007 | Web: şubeler sayfası (ağaç + detay) | FR-0102, 0103 | TC-001 | M |
| ST-008 | Web: kurulum sihirbazı adım 1–2 | FR-1401 | TC-004 | M |
| ST-009 | Mobil: giriş (OTP), aydınlatma, konum izni ekranları | FR-0201, 1307, 1308 | TC-012 | M |
| ST-010 | Tohum betiği v0 + CI E2E iskeleti | — | — | S |

### S2 — Personel, şablon, mobil Bugün
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-011 | Backend: kullanıcı CRUD, davet SMS'i, pasifleştirme, maskeleme | FR-0107…0110 | TC-005, 007 | M |
| ST-012 | Backend: akıllı gruplar (kural + üyelik değerlendirme) | FR-0206 | TC-079 | M |
| ST-013 | Web: personel sayfası, rol düzenleme, davet, gruplar | FR-0107, 0205, 0206 | TC-005…007 | M |
| ST-014 | Backend: şablon/sürüm/bölüm/madde modeli ve doğrulama | FR-0301…0304, 0312 | TC-021, 022 | L→2 |
| ST-015 | Backend: puanlama saf fonksiyonu + spesifikasyon fikstürleri | FR-0306, 0307 | TC-020 | S |
| ST-016 | Web: şablon listesi ve editör v1 (yapı + madde ayarları) | FR-0302…0304 | TC-018 | L→2 |
| ST-017 | Web: şablon yayın (hemen/tarihli) ve sürüm görünümü | FR-0301, 0310 | TC-021, 024 | S |
| ST-018 | Mobil: kabuk, sekmeler, tema token'ları, Bugün ekranı (çevrimiçi) | FR-0601 | TC-039 | M |
| ST-019 | Mobil: üretilmiş API istemcisi, oturum yenileme | FR-0203 | — | S |
| ST-020 | Kural spesifikasyon fikstürleri: puan | — | TC-020 | S |
| ST-021 | Web: kurulum sihirbazı adım 3–5 | FR-1401 | TC-004 | M |
| ST-022 | Backend: hesap ayarları (parametre tablosu) | FR-1402 | TC-069 | S |
| ST-023 | Web: ayarlar sayfası v1 | FR-1402 | — | S |
| ST-024 | Sentetik fotoğraf üreteci (tohum) | — | — | S |

### S3 — Plan ve çalıştırma motoru; madde cevaplama
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-025 | Backend: plan modeli, RRULE değerlendirme, pencere/tolerans hesabı, DST | FR-0501…0507 | TC-025…028, 032 | L→2 |
| ST-026 | Backend: çalıştırma üretimi (7 gün, benzersiz), kapalı gün | FR-0513, 0515 | TC-030, 033 | M |
| ST-027 | Backend: durum makinesi (tablo güdümlü), zamanlayıcı geçişleri | FR-0514 | TC-034 | M |
| ST-028 | Backend: atama modeli (rol/kişi/grup/istasyon; biri/herkes) | FR-0508 | TC-029 | M |
| ST-029 | Web: plan editörü + 7 gün önizleme | FR-0501…0512 | TC-030, 031 | L→2 |
| ST-030 | Backend: cevap yazma (idempotent), gönderim, puan/durum | FR-0602, 0607 | TC-040 | M |
| ST-031 | Mobil: liste çalıştırma ekranı (bölümler, ilerleme, geri sayım) | FR-0601, 0603, 0610 | TC-039, 048 | M |
| ST-032 | Mobil: madde bileşenleri (onay, seçim, sayı, sıcaklık, metin, tarih-saat, talimat) | FR-0303, 0305 | TC-018, 019 | L→2 |
| ST-033 | Mobil: gönderim kilidi ve sonuç | FR-0607 | TC-040 | S |
| ST-034 | Spesifikasyon fikstürleri: pencere/durum | — | TC-025, 034 | S |
| ST-035 | Backend: plan değişikliği yeniden hesap; çakışma engeli | FR-0516, 0517 | TC-031, 037 | S |
| ST-036 | Web: pano ızgarası v0 (salt durum) | FR-1201 | TC-085 | M |
| ST-037 | Backend: tek seferlik liste | FR-0512 | — | S |
| ST-038 | Tohum: 25 şube, 8 plan, 30 gün geçmiş | — | — | M |

### S4 — Kanıt, damga, push
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-039 | Backend: ön imzalı yükleme, tamamlama, hash doğrulama | FR-0606 | TC-043 | M |
| ST-040 | İşçi: damgalama ve küçük resim | FR-0606 | TC-043 | M |
| ST-041 | Mobil: uygulama içi kamera, yalnızca kamera ayarı, sıkıştırma | FR-0604, 0605 | TC-041, 042 | L→2 |
| ST-042 | Mobil: video ≤ 20 sn, imza, barkod/QR bileşenleri | FR-0303 | TC-018 | M |
| ST-043 | Mobil: konum yakalama ve bayraklar | FR-0606, BR-15 | TC-044 | S |
| ST-044 | Backend: bildirim servisi (kanal-bağımsız), push sürücüsü, teslimat izi | FR-1001, 1005…1007 | TC-035 | M |
| ST-045 | Backend: hatırlatma politikası (açılış, −30 dk, bitiş) | FR-0509 | TC-035 | S |
| ST-046 | Mobil: push alma, derin bağlantı | FR-1001 | TC-035 | S |
| ST-047 | Backend: ek kayıt (düzeltme) | FR-0608 | TC-049 | S |
| ST-048 | Web: çalıştırma detayı v1 (cevaplar, kanıt) | FR-1202 | TC-087 | M |
| ST-049 | Backend: imzalı süreli kanıt URL'leri | FR-1305 | TC-087 | S |
| ST-050 | Performans ölçüm protokolü ilk koşu (Galaxy A05) | NFR-02 | — | S |

### S5 — Çevrimdışı; yapılamadı; koşullu mantık
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-051 | Mobil: yerel veritabanı (Drift, şifreli), önbellek manifesti | FR-0701 | TC-051 | M |
| ST-052 | Mobil: yazma kuyruğu (cevap + kanıt), "bekliyor" rozeti | FR-0702 | TC-051 | M |
| ST-053 | Mobil: arka plan senk servisi, üstel yeniden deneme | FR-0703, 0707 | TC-051, 053 | L→2 |
| ST-054 | Backend: `/sync/manifest`, `/sync/batch`, zaman düzeltmesi | FR-0704 | TC-052, 053 | M |
| ST-055 | Backend + mobil: koşullu mantık değerlendirici (ortak fikstürler) | FR-0401…0403 | TC-023 | L→2 |
| ST-056 | Web: koşul editörü, kural deneme | FR-0401, 0404 | TC-023 | M |
| ST-057 | Mobil: yapılamadı alt sayfası, sebep seti, kritik yasak | FR-0801…0804 | TC-057…060 | M |
| ST-058 | Backend: sebep/kategori setleri yönetimi | FR-0802, 0809 | — | S |
| ST-059 | Mobil: senk durumu ekranı | FR-0708 | TC-056 | S |
| ST-060 | Backend: kuyruk sınırları ve geç senk bayrağı | FR-0706 | TC-054 | S |
| ST-061 | Mobil: kaldığı yerden devam, madde bazlı kilit | FR-0603, 0609 | TC-047, 048 | M |
| ST-062 | Web: pano hücre → detay, durum lejantı | FR-1201 | TC-085 | S |

### S6 — Çakışma; aksiyon ve eskalasyon; kiosk; SMS
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-063 | Backend: çakışma kuralı, 100 tekrar dayanıklılık testi | FR-0705 | TC-055 | M |
| ST-064 | Backend: aksiyon modeli, otomatik oluşturma (idempotent), vade kuralı | FR-0901…0903 | TC-065, 069, 070 | M |
| ST-065 | Backend: durum akışı, kapanış kanıtı, yorumlar | FR-0904…0906 | TC-066…068 | M |
| ST-066 | Backend: eskalasyon merdiveni (adım tablosu, zamanlayıcı), durdurma, alıcı yok | FR-0911…0915 | TC-073…077 | L→2 |
| ST-067 | Backend: SMS sürücüsü, kritik/eskalasyon kanal politikası, sessiz saatler | FR-1002…1004 | TC-036, 078 | M |
| ST-068 | Mobil: aksiyonlarım listesi ve detay, kapatma kanıtı, yorum | FR-0907, 0905, 0906 | TC-065…068 | L→2 |
| ST-069 | Web: aksiyonlar sayfası, eskalasyon adımları görünümü | FR-0907, 0913 | TC-065, 075 | M |
| ST-070 | Backend: kiosk cihaz kaydı (QR), PIN, kısa ömürlü belirteç | FR-0207, 0208, 0210 | TC-008, 013, 015 | M |
| ST-071 | Mobil: kiosk kilit ekranı, hareketsizlik, PIN sıfırlama | FR-0208…0210 | TC-013…016 | M |
| ST-072 | Web: cihaz yönetimi (kiosk QR, kaldırma) | FR-0207 | TC-008 | S |
| ST-073 | Backend: yapılmayacak akışı | BR-04, FR-0914 | TC-038 | S |
| ST-074 | Web: yapılmayacak ve aksiyon oluştur (panodan) | FR-0908 | TC-038 | S |
| ST-075 | Backend: aksiyon bildirimleri | FR-0910 | TC-071 | S |
| ST-076 | Alfa hazırlığı: tasarım ortağı hesabı, 5 şube, kapanış şablonu, kiosk kurulumu | — | — | S |

### S7 — Pano, detay, galeri
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-077 | Backend: ızgara sorgusu (gün, filtre), 60 sn yenileme, performans | FR-1201, NFR-03 | TC-085, 086 | M |
| ST-078 | Web: pano tam (KPI, filtreler, canlı) | FR-1201 | TC-085 | M |
| ST-079 | Web: çalıştırma detayı tam (kanıt tam boy, damga meta, aksiyonlar, olay izi) | FR-1202 | TC-087 | M |
| ST-080 | Backend + web: kanıt galerisi | FR-1208 | TC-092 | M |
| ST-081 | Backend: günlük yeniden atama | FR-0519, 0520 | TC-108…110 | S |
| ST-082 | Mobil: yönetici görünümü (özet ızgara, atama) | FR-1211, 0519 | TC-094, 108 | L→2 |
| ST-083 | Web: günlük atama (pano) | FR-0519 | TC-108 | S |
| ST-084 | Alfa geri bildirim düzeltmeleri | — | — | M |
| ST-085 | Backend: materialized view altyapısı (raporlar) | FR-1203 | — | S |
| ST-086 | Mobil: sorun bildir | FR-0806 | TC-062 | S |

### S8 — Raporlar ve dışa aktarım; sorun akışı
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-087 | Backend: tamamlanma/zamanındalık, şube sıralaması | FR-1203, 1204 | TC-088, 089 | M |
| ST-088 | Backend: başarısız madde, yapılamadı sebepleri, ölçüm günlüğü, aksiyon raporu | FR-1205…1207, 1209 | TC-090, 091, 061 | M |
| ST-089 | Backend: kişi düzeyi takip (yetki: şube/bölge müdürü) | FR-1210 | TC-093 | S |
| ST-090 | Web: raporlar sayfası (sekmeler, filtreler, grafikler) | FR-1203…1210 | TC-088…093 | L→2 |
| ST-091 | İşçi: çalıştırma PDF'i (markalı, doğrulama kodu) | FR-1213, 1218 | TC-095 | M |
| ST-092 | İşçi: dönem PDF'i ve Excel; arka plan üretim; paylaşım bağlantısı | FR-1214…1217 | TC-096…099 | M |
| ST-093 | Backend + web: sorun → aksiyon/kapat/yükselt | FR-0807, 0808 | TC-063, 064 | S |
| ST-094 | Web: personel maskeleme ve oturum sonlandırma | FR-0110, 0203 | TC-007 | S |
| ST-095 | Mobil: duyuru şeridi altyapısı (Bugün) | FR-1103 | TC-083 | S |
| ST-096 | Web: ayarlar — eskalasyon şablonları, sebep setleri, tatil takvimi | FR-1402 | — | M |
| ST-097 | Mobil: erişilebilirlik geçişi (44 px, etiketler, %130) | FR-0611 | TC-050 | S |
| ST-098 | Cihaz matrisi otomasyonu (Firebase Test Lab gece) | NFR-06 | — | S |

### S9 — Denetim izi, kütüphane, Beta
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-099 | Backend: hash zinciri, günlük kök, TSA entegrasyonu | FR-1301, 1302 | TC-100…102 | M |
| ST-100 | Backend: zincir doğrulama aracı | FR-1304 | TC-101 | S |
| ST-101 | Web: denetim izi görüntüleyici | FR-1303 | TC-103 | M |
| ST-102 | İçerik: 30 Türkçe yeme-içme şablonu (kalite incelemeli) | FR-0311 | TC-017 | M (PO + tasarımcı) |
| ST-103 | Backend + web: kütüphane kopyalama, merkezî güncelleme | FR-0311 | TC-017 | S |
| ST-104 | Web: şablon editörü — şablon ayarları, önizleme, yayın doğrulaması tam | FR-0308, 0309, 0312 | TC-022 | M |
| ST-105 | Mobil: tolerans/kilit davranışları, geç gönderim | FR-0610, BR-02/03 | TC-045 | S |
| ST-106 | Beta hazırlığı: 3 pilot hesabı, veri işleme sözleşmesi, staging zaman aracı | — | — | M |
| ST-107 | Backend: içe aktarma — personel Excel | FR-0105 | TC-005 | S |
| ST-108 | Alfa/Beta düzeltmeleri | — | — | M |

### S10 — KVKK, duyuru, güvenlik
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-109 | Backend: aydınlatma sürümleri, yeniden onay | FR-1307 | TC-107 | S |
| ST-110 | Backend: KVKK dışa aktarma (ZIP) | FR-1309 | TC-106 | M |
| ST-111 | Backend: maskeleme + kanıt silme akışı | FR-1310 | TC-104 | M |
| ST-112 | Zamanlayıcı: saklama silme ve rapor | FR-1311 | TC-105 | M |
| ST-113 | Web: KVKK talepleri, saklama ayarı, aydınlatma editörü | FR-1309…1312 | TC-104…107 | M |
| ST-114 | Backend: duyuru, hedefleme, onay, hatırlatma | FR-1101…1105 | TC-079…082 | M |
| ST-115 | Web: duyurular sayfası ve onay raporu | FR-1101…1105 | TC-082 | M |
| ST-116 | Mobil: duyuru ekranı ve onay | FR-1103 | TC-080, 083 | S |
| ST-117 | Backend + web: 2FA (TOTP), şifre politikası, cihaz/oturum listesi | FR-0202, 0203 | — | M |
| ST-118 | Güvenlik: ASVS/MASVS kontrol listesi, bağımlılık taraması, hız sınırları | NFR-09 | — | M |
| ST-119 | Backend: faturalama sayacı | FR-1403 | — | S |
| ST-120 | Beta düzeltmeleri | — | — | M |

### S11 — Pilot geri bildirimi ve Should'lar
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-121 | Mobil: QR ile istasyondan başlatma | FR-0612 | — | M |
| ST-122 | Mobil + backend: vardiya devri notu | FR-1601 | — | S |
| ST-123 | İşçi: sabah/haftalık e-posta özeti | FR-1212 | — | M |
| ST-124 | Web: gözden geçirme ve ikinci imza | FR-1701, 1702 | TC-111, 112 | M |
| ST-125 | Backend: imzalı duyuru | FR-1106 | TC-084 | S |
| ST-126 | Performans: ızgara 100 şube, PDF < 30 sn, k6 yük profili (22:00–01:00) | NFR-03, 04 | TC-086 | M |
| ST-127 | Web: şube türü varyantı (şablon) | FR-1501 | — | M |
| ST-128 | Pilot geri bildirimi paketi 1 | — | — | L |
| ST-129 | Mobil: düşük cihaz optimizasyonu (soğuk açılış < 3 sn) | NFR-02 | — | M |
| ST-130 | Destek modu (maskeli kanıt, tanı raporu) | NFR-16 | — | M |

### S12 — Sertleştirme ve GA
| ST | Hikâye | FR | TC | Boyut |
|---|---|---|---|---|
| ST-131 | Dış sızma testi bulgularının kapatılması | NFR-09 | — | M |
| ST-132 | Kurtarma tatbikatı (yedekten geri yükleme), RPO/RTO doğrulama | NFR-13 | — | S |
| ST-133 | Kabul testleri %100 koşusu ve hata kapanışı | TC-001…112 | — | L |
| ST-134 | Mağaza yayın hazırlığı (gizlilik etiketleri, ekran görüntüleri, sürüm notları) | — | — | S |
| ST-135 | Uyum kontrol listesi (06-kvkk) kapanışı | NFR-10 | — | S |
| ST-136 | İzleme ve uyarılar üretim ayarı; çalışma kitapları (runbook) | NFR-12 | — | M |
| ST-137 | Onboarding oyun kitabı ve destek SSS | NFR-16 | — | S |
| ST-138 | AI taslak şablon (SOP/PDF) — süre kalırsa | FR-1502 | — | M |

## Kapasite notu

Toplam ~138 hikâye; L'ler bölündüğünde ~160 iş. 12 sprint × ~16 gün ≈ 190 geliştirici günü; S/M/L ortalaması 1,5/4/8 gün kabulüyle ~200 gün → plan sıkı; **Should'lar (S11) ve ST-138 doğal tampon**. Riskli sprintler S3–S6 (motor + çevrimdışı); burada kayma olursa S8 raporlarının bir kısmı S10'a kayar, Beta tarihi korunur.
