# Backlog ve sprint planı (v1 çekirdek)

ADR-0008 ile yeniden çizildi (13 Eylül 2026). Epic = yetenek (CAP). Hikâye = kullanıcı bakışıyla, FR'lere bağlı, kabul testi (TC) ile kapanır. Boyut: S (≤ 2 gün), M (3–5 gün), L (6–10 gün; bölünmeli). Ekip: 1 mobil, 1 backend/web (Sprint 5'ten itibaren yarı zamanlı web desteği), kurucu-PO, yarı zamanlı tasarımcı, Sprint 6'dan itibaren yarı zamanlı QA. Sprint = 2 hafta, ~16 geliştirici günü. **Hikâye numaraları eski plandan korunur;** v1'de daraltılan hikâyeler "(v1: …)" notuyla, ertelenenler alttaki v1.1 listesinde. Yeni hikâyeler ST-139'dan başlar.

## Kilometre taşları

| Sprint | Taş | Ölçüt |
|---|---|---|
| S6 sonu | **Alfa** | 1 tasarım-ortağı zincir, 5 şube, kapanış listesi kioskta; kanıt ve sabah özeti çalışıyor |
| S8 sonu | **Beta** | 3 pilot zincir, 30+ şube; açılış + kapanış + soğuk zincir; ızgara, PDF |
| S10 sonu | **GA** | v1 satırlarının tamamı; 104 v1 kabul testi %100; pilot UAT imzası |
| S11–S12 | Tampon / v1.1 başlangıcı | Pilot bulguları; v1.1 sırasının ilk maddeleri |

## Faz planı (ADR-0013)

İş iki hatta bölünür: **Faz A** panel ve arka uç (tek geliştiriciyle hemen başlar), **Faz B** mobil (ikinci geliştirici Faz A'nın 6.–8. haftasında katılır). Sprint tabloları bağımlılık sırasını koruduğu için olduğu gibi duruyor; her hikâyenin hangi hatta olduğu **Faz** kolonundadır.

| Hat | Hikâye | Gün | İçerik |
|---|---|---|---|
| **A · panel + arka uç** | 82 | **244** | Hesap/RLS/olay izi, hiyerarşi, OTP ve roller, personel, şablon editörü, plan ve çalıştırma motoru, kanıt sunucu tarafı, bildirim servisi, pano ve raporlar, PDF'ler, hash zinciri, KVKK süreçleri, tohum ve içerik, Spike B ve D |
| **B · mobil** | 25 | **74** | Giriş, kabuk ve Bugün, liste çalıştırma, madde bileşenleri, kamera ve kanıt, çevrimdışı kuyruk ve senk, yapılamadı, aksiyonlarım, kiosk, Bölgem, erişilebilirlik, cihaz matrisi, mağaza, Spike A ve C |
| **A+B · ortak** | 11 | **40** | İki istemciyi birlikte etkileyen işler (çalıştırma kilidi, sabit kural, kanıt bayrakları, dün gece bloğu, PIN atama) + Alfa/Beta/GA hazırlıkları ve düzeltmeleri |

Ortağı yarı yarıya saydığımızda **A ≈ 264 gün, B ≈ 94 gün** — yani iş **2,8 kat asimetrik**. Bunun iki sonucu var ve ikisi de ADR-0013'te yazılı: mobil geliştirici kuyruğunu bitirince web hattına geçer; üçüncü geliştirici gerekirse **web** geliştiricisi olur, mobil değil.

### Hat kapasitesi ve takvim

Tek geliştirici sprint başına ~9 gün (2 hafta × 5 iş günü, tören ve saha günü düşülmüş).

| | İş | Tek kişiyle | İki kişiyle |
|---|---|---|---|
| Faz A | 264 gün | ~29 sprint (~14 ay) | ~15 sprint (~7 ay) |
| Faz B | 94 gün | ~10 sprint (~5 ay) | — |

Tabloyu okumanın doğru yolu: **darboğaz A hattıdır.** İki kişi (1 panel + 1 mobil) çalıştığında mobil 5. ayda biter, panel 14. ayda — yani takvimi mobil değil panel belirler. Kapasite kaldıracı kararı (bkz. kapasite notu) bu yüzden "üçüncü geliştirici **web**" yönünde ağırlaşmıştır.

### Devir kapısı: mobil başlamadan önce yazılı olacak üç sözleşme

Faz A'nın bitti tanımına eklenir; yazılmazsa Faz B, Faz A'yı söker (API panelin çevrimiçi istek-cevap şekline oturur):

1. **Cevap yazma idempotent** — cihazda üretilen UUID anahtarıyla `PUT`, tekrar gönderimde aynı kayıt (ST-030, FR-0602/0607).
2. **Kanıt yükleme akışı** — ön imzalı URL → tamamlama → sunucu damgası + SHA-256 doğrulaması (ST-039/040, FR-0606).
3. **Senk uç noktaları taslağı** — `/sync/manifest` ve `/sync/batch` şekli ve zaman düzeltmesi OpenAPI'de (ST-054, FR-0704); uygulanması Faz B'de.

### Faz B'nin ilk iki haftası

Ekran değil **spike**: Spike A (çevrimdışı kuyruk + idempotent senk) ve Spike C (kamera → damga → SHA-256), stub API ile. Gerekçe: planın en riskli iki maddesi bunlar; sona bırakılırsa kötü haber projenin sonunda gelir ([05-sprint0-ve-teknik-spike.md](05-sprint0-ve-teknik-spike.md) §4).

### Pilot taahhüdü

Alfa, pilot kurulumu ve K3 ölçümü **mobil olmadan yapılamaz**. Pilot zincirlere tarih verilirken Faz B'nin başlangıcından en az 10 hafta sayılır; bu tarih ikinci geliştiricinin bulunma tarihine bağlıdır, Faz A'nın hızına değil.

## Epic listesi

| EP | Epic | CAP | Sprint |
|---|---|---|---|
| EP-01 | Hesap, organizasyon, içe aktarma, sihirbaz | CAP-01, CAP-14 | S1–S2 |
| EP-02 | Kimlik, 4 rol, kiosk | CAP-02 | S1, S6 |
| EP-03 | Basit şablon editörü, 9 şablon, sabit kural | CAP-03, CAP-04 | S2, S4, S9 |
| EP-04 | Planlama ve çalıştırma motoru | CAP-05 | S3 |
| EP-05 | Mobil yürütme ve kanıt | CAP-06 | S2–S5 |
| EP-06 | Çevrimdışı senk | CAP-07 | S5–S6 |
| EP-07 | Yapılamadı, sorun, aksiyon (açık/kapalı), sabit eskalasyon, sabah özeti | CAP-08, CAP-09, CAP-10 | S5–S6, S8 |
| EP-08 | Istisna odaklı pano, detay, galeri, Bölgem | CAP-12 | S7 |
| EP-09 | Sıcaklık günlüğü, PDF'ler, aylık özet | CAP-12 | S8 |
| EP-10 | Hash zinciri, KVKK süreçleri, güvenlik temel | CAP-13 | S9 |
| EP-11 | Sertleştirme, performans, GA | — | S10 |
| EP-12 | v1.1 | CAP-11, 15–18 ve ertelenenler | S11+ |
| EP-13 | Madde kütüphanesi ve işletme türü paketleri (v1.1 ilk sıra, ADR-0010) | CAP-20 | S11–S12 |

## Sprint planı ve hikâyeler

Biçim: ST · hikâye · FR · TC · boyut. Kabul kriteri = bağlı TC'ler (v1 sürüm etiketli) + kart notları.

### S0 — Altyapı (02-repo kontrol listesi) · **Faz A, tek kişi**
Mobil iskelet ve Spike A/C bu listeden çıktı, Faz B'nin ilk haftasına geçti (ADR-0013). Depolar, CI, dev compose, staging (ücretsiz/AB altyapı yeterli; yalnızca fikstür verisi — ADR-0012), taşınabilirlik kontrolü (sağlayıcıya özel hizmet yok), günlük yedek + geri yükleme provası, üretim TR sağlayıcı kısa listesi (karar Sprint 2 sonu), sağlayıcı test hesapları, tasarım token'ları kodda, tohum v0, spesifikasyon fikstürleri (pencere/durum, puan, sabit kural), backlog aracı.

### S1 — Temel: hesap, hiyerarşi, OTP, 4 rol

**Sprint hedefi (izleyici kurşun):** bir yönetici web'den girip şube ağacını kurabiliyor; bir personel mobilden OTP ile girip (henüz boş) Bugün ekranına ulaşıyor. Gösterimde bu iki yol uçtan uca çalışır — yarım kalan bir giriş ekranı sprint hedefi değildir.

**Dağılım (ADR-0013):** S1'in tamamı **Faz A**, yani tek kişide — ST-001…008 aynı geliştiricinin işi. **ST-009 (mobil giriş) Faz B'ye düşer**, mobil geliştirici katılınca ilk ekran işi olarak yapılır; S1 onsuz kapanabilir, çünkü sprint hedefinin mobil yarısı Faz B'nin ilk haftalarına taşındı. Tek kişiyle S1'in yükü (ST-009 hariç ≈ 31 gün) sprint kapasitesinin üç katıdır: S1 takvimde ~3 sprinte yayılır ya da esnek maddeler düşer (aşağıda).

**Sıra ve bağımlılık:** ST-001 → ST-002 → ST-004 → ST-007 → ST-005; tek kişide paralellik yok, zincirin tamamı seridir. **ST-003 ve ST-008 esnektir:** sprint taşarsa S2'ye düşerler (sihirbazın 3.–4. adımı zaten S2'de, ST-021; Excel içe aktarma ilk olarak sihirbazda gerekir).

| ST | Hikâye | FR | TC | Boyut | Faz |
|---|---|---|---|---|---|
| ST-001 | Backend: hesap/kiracı modeli, RLS, `audit.emit()` altyapısı | FR-0101, FR-1301 | TC-011, TC-100 | M | A |
| ST-002 | Backend: hiyerarşi (bölge, şube, istasyon, takvim) CRUD | FR-0102…0104, FR-0515 | TC-001 | M | A |
| ST-003 | Backend: Excel içe aktarma (şube/istasyon) + doğrulama raporu | FR-0105, FR-0106 | TC-001…003 | M | A |
| ST-004 | Backend: OTP giriş, belirteçler, oturum yönetimi, hız sınırı | FR-0201, 0203, 0204 | TC-009 | M | A |
| ST-005 | Backend: 4 rol × kapsam yetki katmanı (bağımlılık) | FR-0205 | TC-006, 010 | M | A |
| ST-006 | Web: giriş (e-posta/şifre, şifre politikası), kabuk (menü, rol kapsamı); arayüz metinleri kaynak dosyada (i18n) | FR-0202, 1803 | TC-128 | S | A |
| ST-007 | Web: şubeler sayfası (ağaç + detay + takvim) | FR-0102, 0103 | TC-001 | M | A |
| ST-008 | Web: kurulum sihirbazı adım 1–2 (marka + şubeler) | FR-1401 | TC-004 | M | A |
| ST-009 | Mobil: giriş (OTP), aydınlatma, konum izni ekranları | FR-0201, 1307, 1308 | TC-012 | M | B |
| ST-010 | Tohum betiği v0 + CI E2E iskeleti | — | — (DoD: S1 hikâyelerinin TC'leri CI'da koşar) | S | A |

### S2 — Personel, basit şablon editörü, mobil Bugün
| ST | Hikâye | FR | TC | Boyut | Faz |
|---|---|---|---|---|---|
| ST-011 | Backend: kullanıcı CRUD, davet SMS'i, pasifleştirme; maskeleme destek betiği | FR-0107…0110 | TC-005, 007, 104 | M | A |
| ST-013 | Web: personel sayfası, rol/kapsam, davet (v1: grup yok) | FR-0107, 0205 | TC-005…007 | M | A |
| ST-014 | Backend: şablon/sürüm/bölüm/madde modeli ve yayın doğrulaması (v1: 6 tür, 3 ayar) | FR-0301…0304, 0312 | TC-021, 022 | M | A |
| ST-015 | Backend: yüzde puan + kritik kuralı saf fonksiyonu, fikstürler | FR-0306, 0307 | TC-020 | S | A |
| ST-016 | Web: şablon listesi ve basit editör (madde listesi, tür, 3 kutu, sıcaklık aralığı) | FR-0302…0305 | TC-018 | M | A |
| ST-017 | Web: yayın (hemen) ve sürüm görünümü | FR-0301 | TC-021 | S | A |
| ST-018 | Mobil: kabuk, sekmeler, tema token'ları, Bugün ekranı (çevrimiçi); arayüz metinleri kaynak dosyada (i18n) | FR-0601, 1803 | TC-039 | M | B |
| ST-019 | Mobil: üretilmiş API istemcisi, oturum yenileme | FR-0203 | — | S | B |
| ST-021 | Web: kurulum sihirbazı adım 3–4 (kapanış şablonu + plan önerisi + personel), yayın | FR-1401 | TC-004 | M | A |
| ST-024 | Sentetik fotoğraf üreteci (tohum) | — | — | S | A |
| ST-153 | Altyapı: üretim ortamı Türkiye'de kurulur (dağıtım hattı, kasa, günlük yedek, geri yükleme provası) — [ADR-0012](../adr/0012-barindirma-saglayici-ve-ortamlar.md); staging bu ortama taşınır, gerçek veriden önce biter | NFR-10, NFR-13 | — (DoD: geri yükleme provası kaydı) | M | A |

### S3 — Plan ve çalıştırma motoru; madde cevaplama
| ST | Hikâye | FR | TC | Boyut | Faz |
|---|---|---|---|---|---|
| ST-025 | Backend: plan modeli, RRULE, pencere/tolerans, gece yarısı, DST | FR-0501…0507 | TC-025…028, 032 | L→2 | A |
| ST-026 | Backend: çalıştırma üretimi (7 gün, benzersiz), kapalı gün | FR-0513, 0515 | TC-030, 033 | M | A |
| ST-027 | Backend: durum makinesi (tablo güdümlü), zamanlayıcı geçişleri | FR-0514 | TC-034 | M | A |
| ST-028 | Backend: atama modeli (v1: rol/kişi/şubedeki herkes, biri tamamlasın) | FR-0508 | — | S | A |
| ST-139 | Backend + mobil: çalıştırma kilidi — ilk açan alır, "X yapıyor" rozeti, kilit yenileme/bırakma, şube müdürü kaldırır (E-2) | FR-0521, BR-26 | TC-039, 115 | M | A+B |
| ST-029 | Web: plan editörü (kapsam, tekrar, pencere, atama; sabit hatırlatma/eskalasyon bilgisi) + 7 gün önizleme | FR-0501…0512 | TC-030, 031 | M | A |
| ST-030 | Backend: cevap yazma (idempotent), gönderim, puan/durum | FR-0602, 0607 | TC-040 | M | A |
| ST-031 | Mobil: liste çalıştırma ekranı (bölümler, ilerleme, geri sayım) | FR-0601, 0603, 0610 | TC-039, 048 | M | B |
| ST-032 | Mobil: madde bileşenleri (onay, seçim, sayı, sıcaklık, metin, talimat) | FR-0303, 0305 | TC-018, 019 | M | B |
| ST-033 | Mobil: gönderim kilidi ve sonuç | FR-0607 | TC-040 | S | B |
| ST-034 | Spesifikasyon fikstürleri: pencere/durum | — | TC-025, 034 | S | A |
| ST-035 | Backend: plan değişikliği yeniden hesap; çakışma engeli | FR-0516, 0517 | TC-031, 037 | S | A |
| ST-037 | Backend: tek seferlik liste | FR-0512 | — | S | A |
| ST-038 | Tohum: 25 şube, 8 plan, 30 gün geçmiş | — | — | M | A |

### S4 — Kanıt, damga, sabit kural, push
| ST | Hikâye | FR | TC | Boyut | Faz |
|---|---|---|---|---|---|
| ST-039 | Backend: ön imzalı yükleme, tamamlama, hash doğrulama | FR-0606 | TC-043 | M | A |
| ST-040 | İşçi: damgalama ve küçük resim | FR-0606 | TC-043 | M | A |
| ST-041 | Mobil: kamera doğrudan açılır (2 dokunuş), yalnızca kamera, 1–3 fotoğraf, sıkıştırma | FR-0604, 0605 | TC-041, 042 | M | B |
| ST-043 | Mobil: konum yakalama ve bayraklar | FR-0606, BR-15 | TC-044 | S | B |
| ST-147 | Backend + mobil: kanıt tekilliği (aynı SHA-256 reddi, olay kaydı) ve kanıt bayrakları (galeri · şube dışı konum · cihaz saati · geç senk) (E-11) | FR-0614, 0615 | TC-120, 121 | M | A+B |
| ST-140 | Backend + mobil: sabit kural — başarısız cevapta fotoğraf + not; kritik → aksiyon; ortak fikstürler (E-… FR-0405) | FR-0405, BR-06, BR-08 | TC-019, 023, 046, 114 | M | A+B |
| ST-044 | Backend: bildirim servisi (kanal-bağımsız), push sürücüsü, teslimat izi | FR-1001, 1005…1007 | TC-035 | M | A |
| ST-045 | Backend: sabit iki hatırlatma (açılış, −30 dk) | FR-0509 | TC-035 | S | A |
| ST-046 | Mobil: push alma, derin bağlantı | FR-1001 | TC-035 | S | B |
| ST-048 | Web: çalıştırma detayı v1 (cevaplar, kanıt) | FR-1202 | TC-087 | M | A |
| ST-049 | Backend: imzalı süreli kanıt URL'leri | FR-1305 | TC-087 | S | A |
| ST-050 | Performans ölçüm protokolü ilk koşu (Galaxy A05) | NFR-02 | — | S | B |

### S5 — Çevrimdışı; yapılamadı; dün gece özeti
| ST | Hikâye | FR | TC | Boyut | Faz |
|---|---|---|---|---|---|
| ST-051 | Mobil: yerel veritabanı (şifreli), önbellek manifesti | FR-0701 | TC-051 | M | B |
| ST-052 | Mobil: yazma kuyruğu (cevap + kanıt), "bekliyor" rozeti | FR-0702 | TC-051 | M | B |
| ST-053 | Mobil: arka plan senk servisi, üstel yeniden deneme | FR-0703, 0707 | TC-051, 053 | L→2 | B |
| ST-054 | Backend: `/sync/manifest`, `/sync/batch`, zaman düzeltmesi | FR-0704 | TC-052, 053 | M | A |
| ST-057 | Mobil: yapılamadı alt sayfası (sabit sebep seti, kritikte yok) | FR-0801, 0803, 0804 | TC-057…060 | M | B |
| ST-059 | Mobil: senk durumu ekranı | FR-0708 | TC-056 | S | B |
| ST-060 | Backend: kuyruk sınırları ve geç senk bayrağı | FR-0706 | TC-054 | S | A |
| ST-061 | Mobil: kaldığı yerden devam (tek kullanıcı) | FR-0603 | TC-048 | S | B |
| ST-141 | Backend + mobil: açılış listesinde "dün gece" bloğu (E-3) | FR-0613 | TC-039, TC-116 | S | A+B |
| ST-062 | Web: pano hücre → detay, durum lejantı | FR-1201 | TC-085 | S | A |

### S6 — Senk dayanıklılığı; aksiyon (açık/kapalı); sabit eskalasyon; kiosk; sabah özeti → Alfa
| ST | Hikâye | FR | TC | Boyut | Faz |
|---|---|---|---|---|---|
| ST-063 | Backend: senk çakışma kuralı ve 100 tekrar dayanıklılık testi | FR-0705 | TC-055 | M | A |
| ST-064 | Backend: aksiyon modeli (açık/kapalı), otomatik oluşturma (idempotent), sabit vadeler | FR-0901…0903 | TC-065, 069, 070 | M | A |
| ST-065 | Backend: kapatma (not zorunlu), not ekleme | FR-0904, 0905 | TC-066, 067 | S | A |
| ST-152 | Backend + web: elle aksiyon oluşturma (yetkili roller; şube, sorumlu, vade, öncelik) | FR-0908 | TC-065 | S | A |
| ST-066 | Backend: sabit eskalasyon kuralı (kaçırıldı → şube müdürü anında; kritik → anında + SMS gecikmesi; sabah özetine biriktirme) | FR-0911…0915, FR-1008 | TC-073…077 | M | A |
| ST-143 | Backend + e-posta: sabah özeti 07:00 (bölge müdürü, yönetici) push + e-posta (E-5) | FR-1212, BR-27 | TC-074 | M | A |
| ST-067 | Backend: SMS sürücüsü (OTP + kritik yedek), sabit sessiz saat | FR-1002, 1004 | TC-036, 078, 117 | S | A |
| ST-068 | Mobil: aksiyonlarım listesi ve detay (açık/kapalı, not, kapatma) | FR-0907, 0905 | TC-065…067 | M | B |
| ST-069 | Web: aksiyonlar sayfası (basit) | FR-0907 | TC-065, 072 | S | A |
| ST-070 | Backend: kiosk cihaz kaydı (QR), PIN, kısa ömürlü belirteç | FR-0207, 0208, 0210 | TC-008, 013, 015 | M | A |
| ST-071 | Mobil: kiosk kilit ekranı, hareketsizlik, PIN sıfırlama | FR-0208…0210 | TC-013…016 | M | B |
| ST-142 | Backend + mobil: şube müdürü personele başlangıç PIN'i atar (E-1) | FR-0211 | TC-013, TC-113 | S | A+B |
| ST-072 | Web: cihaz yönetimi (kiosk QR, kaldırma) | FR-0207 | TC-008 | S | A |
| ST-073 | Backend: yapılmayacak akışı | BR-04, FR-0914 | TC-038 | S | A |
| ST-075 | Backend: aksiyon bildirimleri (atandı anında; gecikti sabah özetinde) | FR-0910 | TC-071 | S | A |
| ST-076 | Alfa hazırlığı: tasarım ortağı hesabı, 5 şube, kapanış şablonu, kiosk kurulumu | — | — | S | A+B |

### S7 — İstisna odaklı pano, detay, galeri, Bölgem
| ST | Hikâye | FR | TC | Boyut | Faz |
|---|---|---|---|---|---|
| ST-077 | Backend: ızgara sorgusu (gün, filtre, istisna görünümü), 60 sn yenileme, performans | FR-1201, 1219, NFR-03 | TC-085, 086 | M | A |
| ST-078 | Web: pano (istisna odaklı varsayılan, "her şey yolunda", tümünü göster, KPI) | FR-1201, 1219 | TC-085, 118 | M | A |
| ST-079 | Web: çalıştırma detayı tam (kanıt tam boy, damga meta, aksiyonlar, olay izi özeti) | FR-1202 | TC-087 | M | A |
| ST-080 | Backend + web: kanıt galerisi (şube + tarih) | FR-1208 | TC-092 | S | A |
| ST-081 | Backend: günlük yeniden atama | FR-0519, 0520 | TC-108, 109, 110 | S | A |
| ST-149 | Backend: belge kaydı ve dosyası; 30/7 gün uyarıları, süresi geçende yüksek öncelikli aksiyon ve "belge eksik" işareti (E-12) | FR-0522, 0523 | TC-123, 124 | M | A |
| ST-144 | Mobil: "Bölgem/Şubem" listesi (şube × dün gece durumu → detay) + şube müdürü günlük atama; **Bugün ekranında çok şubeli kullanıcı için şube gruplaması** (bölge müdürü denetimi, FR-0601) | FR-1211, 0519, 0601 | TC-094, 108 | M | B |
| ST-083 | Web: günlük atama (pano) | FR-0519 | TC-108 | S | A |
| ST-148 | Web: çalıştırma detayında kanıt bayrakları ve panoda "şüpheli kanıt" filtresi (E-11) | FR-0615 | TC-121, 122 | S | A |
| ST-084 | Alfa geri bildirim düzeltmeleri | — | — | M | A+B |
| ST-086 | Mobil: sorun bildir (sabit kategori: güvenlik dâhil) | FR-0806 | TC-062, 126 | S | B |
| ST-093 | Backend + web: sorun → aksiyona çevir / kapat | FR-0807 | TC-063 | S | A |

### S8 — Sıcaklık günlüğü, PDF'ler, aylık özet → Beta
| ST | Hikâye | FR | TC | Boyut | Faz |
|---|---|---|---|---|---|
| ST-088 | Backend: ölçüm günlüğü sorgusu (ekipman zaman serisi, aralık dışı) | FR-1207 | TC-091 | M | A |
| ST-091 | İşçi: çalıştırma PDF'i (markalı, doğrulama kodu) | FR-1213, 1218 | TC-095 | M | A |
| ST-092 | İşçi: dönem PDF'i (sıcaklık günlüğü), arka plan üretim | FR-1214, 1217 | TC-096, 099 | M | A |
| ST-145 | Backend + web: aylık tek sayfa özet (E-7) + PDF | FR-1220 | TC-088, TC-119 | M | A |
| ST-090 | Web: raporlar sayfası (aylık özet, sıcaklık günlüğü, galeri) | FR-1207, 1208, 1220 | TC-088, 091, 092 | M | A |
| ST-150 | Web + işçi: belge takvimi ekranı (SCR-W-14, yaklaşan ve süresi geçen) + dönem PDF'i (E-12) | FR-0524 | TC-125 | M | A |
| ST-094 | Web: personel oturum sonlandırma; hesap sayfası (marka, tatil takvimi, aydınlatma metni) | FR-0203, 1402 (minimal) | TC-007 | S | A |
| ST-097 | Mobil: erişilebilirlik geçişi (44 px, etiketler, %130) | FR-0611 | TC-050 | S | B |
| ST-098 | Cihaz matrisi otomasyonu (Firebase Test Lab gece) | NFR-06 | — | S | B |
| ST-106 | Beta hazırlığı: 3 pilot hesabı, veri işleme sözleşmesi, staging zaman aracı | — | — | M | A+B |
| ST-107 | Backend: personel Excel içe aktarma | FR-0105 | TC-005 | S | A |

### S9 — Hash zinciri, 9 şablon, KVKK süreçleri, güvenlik
| ST | Hikâye | FR | TC | Boyut | Faz |
|---|---|---|---|---|---|
| ST-099 | Backend: hash zinciri ve günlük kök (TSA v1.1) | FR-1301 | TC-100, 101 | M | A |
| ST-100 | Backend: zincir doğrulama komutu (iç araç) | FR-1304 | TC-101 | S | A |
| ST-102 | İçerik: 9 Türkçe yeme-içme şablonu (kalite incelemeli) | FR-0311 | TC-017 | M (PO + danışman) | A |
| ST-103 | Backend + web: kütüphane kopyalama, merkezî güncelleme | FR-0311 | TC-017 | S | A |
| ST-104 | Web: şablon editörü — şablon ayarları (yalnızca kamera, başarısızda kanıt), önizleme, doğrulama tam | FR-0308, 0309, 0312 | TC-022 | M | A |
| ST-105 | Mobil: tolerans/kilit davranışları, geç gönderim | FR-0610, BR-02/03 | TC-045 | S | B |
| ST-109 | Backend: aydınlatma sürümleri, yeniden onay; aydınlatma ve veri işleme sözleşmesi şablonları ürün içinden indirilebilir | FR-1307, 1312 | TC-107 | S | A |
| ST-112 | Zamanlayıcı: saklama silme (sabit 24 ay) ve rapor | FR-1311 | TC-105 | M | A |
| ST-118 | Güvenlik: ASVS/MASVS kontrol listesi, bağımlılık taraması, hız sınırları | NFR-09 | — | M | A |
| ST-119 | Backend: faturalama sayacı | FR-1403 | — | S | A |
| ST-108 | Beta düzeltmeleri | — | — | M | A+B |
| ST-146 | Destek betiği: KVKK dışa aktarma / maskeleme (süreç belgesiyle) | FR-1309, 1310 | TC-104, 106 | S | A |

### S10 — Sertleştirme ve GA
| ST | Hikâye | FR | TC | Boyut | Faz |
|---|---|---|---|---|---|
| ST-126 | Performans: ızgara 100 şube, PDF < 30 sn, k6 yük profili (22:00–01:00) | NFR-03, 04 | TC-086 | M | A |
| ST-129 | Mobil: düşük cihaz optimizasyonu (soğuk açılış < 3 sn) | NFR-02 | — | M | B |
| ST-131 | Dış sızma testi bulgularının kapatılması | NFR-09 | — | M | A |
| ST-132 | Kurtarma tatbikatı (yedekten geri yükleme), RPO/RTO doğrulama | NFR-13 | — | S | A |
| ST-133 | v1 kabul testleri (104) %100 koşusu ve hata kapanışı | — | — | L | A+B |
| ST-134 | Mağaza yayın hazırlığı (gizlilik etiketleri, ekran görüntüleri, sürüm notları) | — | — | S | B |
| ST-135 | Uyum kontrol listesi (06-kvkk) kapanışı; biyometri kullanılmadığının kod ve mağaza beyanıyla doğrulanması | NFR-10, FR-1306 | — | S | A |
| ST-136 | İzleme ve uyarılar üretim ayarı; çalışma kitapları | NFR-12 | — | M | A |
| ST-137 | Onboarding oyun kitabı ve destek SSS | NFR-16 | — | S | A |
| ST-120 | Beta/pilot düzeltmeleri | — | — | M | A+B |

### S11–S12 — Tampon ve v1.1 başlangıcı
Pilot bulguları önce. Kalan kapasite v1.1 sırasına göre (aşağıdaki liste).

## v1.1 backlog'u (ertelenen hikâyeler, ID'ler korundu)

| Sıra | Konu | ST'ler | FR |
|---|---|---|---|
| 0 | **Madde kütüphanesi ve paketler** (EP-13): ST-154 kütüphane maddesi varlığı + tohum (JSON içerik) · ST-155 editörde kütüphaneden ekle / hesap kütüphanesine kaydet · ST-156 kaynak takibi ve güncelleme bandı · ST-157 işletme türü paketleri + sihirbaz adımı · ST-158 hesap içi set uygulama; içerik: 200–300 madde, 4 paket (PO + kalite danışmanı, S8'den itibaren) | ST-154…158 | FR-0313…0318 |
| 1 | **Denetim dosyası ve denetçi bağlantısı** (E-13, v1.1 adayı — K1 sinyaline bağlı): ST-159 dönem dosyasının derlenmesi ve PDF'i (ölçüm günlüğü, çalıştırma özetleri, belge durumu, kanıt örnekleri, doğrulama kodu) · ST-160 süreli salt-okunur bağlantı (48 sa, tek şube/dönem, iptal, her açılış olay izinde, personel adı maskeli) | ST-159, 160 | FR-1221, 1313 |
| 2 | Duyuru ve onay (+ imza) | ST-114, 115, 116, 125, 095 | FR-1101…1106 |
| 3 | Koşul editörü ve kural deneme | ST-055, 056 | FR-0401…0404 |
| 4 | "Herkes tamamlasın" ve madde bazlı kilit | ST-028 (kalan), ST-047 | FR-0508 (kalan), 0609 |
| 5 | Aksiyon durum makinesi, yorum dizisi, onaylı kapanış | ST-065 (kalan), ST-124 | FR-0904 (kalan), 0906, 0909 |
| 6 | Raporlar: tamamlanma/sıralama, başarısız madde ısı haritası, sebep dağılımı, aksiyon raporu, kişi takibi | ST-087, 089, 085 | FR-1203…1206, 1209, 1210, 0805 |
| 7 | Denetim izi ekranı, RFC 3161 | ST-101, ST-099 (TSA) | FR-1302, 1303 |
| 8 | KVKK talep ekranı, ayarlanabilir saklama | ST-110, 111, 113 | FR-1309, 1310 (ekran), 1311 (ayar) |
| 9 | 2FA | ST-117 | FR-0202 (2FA) |
| 10 | Ayarlar paneli (parametreler, eskalasyon şablonları, sebep/kategori setleri, tercihler) | ST-022, 023, 096 | FR-1402, 0802, 0809, 1003, 0510 |
| 11 | Excel dışa aktarım, paylaşım bağlantısı | ST-092 (kalan) | FR-1215, 1216 |
| 12 | Video, imza, barkod/QR, tarih-saat bileşenleri; ek kayıt | ST-042, ST-047 | FR-0303 (kalan), 0608 |
| 13 | QR ile istasyondan başlatma; sorun yükseltme | ST-121 | FR-0612, 0808 |
| 14 | Akıllı gruplar, Gözlemci rolü | ST-012 | FR-0206 |
| 15 | Şube türü varyantı; AI taslak şablon; tarihli yayın | ST-127, 138 | FR-1501, 1502, 0310 |
| 16 | Salt okunur API, webhook; sabah özeti dışındaki planlı raporlar | — | FR-1801, 1802 |
| — | Yerine E-3 geçti: vardiya devri notu | ST-122 | FR-1601 |
| — | Destek modu (tam) | ST-130 | NFR-16 |

## Kapasite notu

v1'de **118 hikâye** (S1–S10), 3'ü L (bölünmüş); eski planın 138 hikâyesinden 34'ü v1.1'e gitti, 14 yeni hikâye (E-1…E-7, E-11, E-12, KVKK betiği, elle aksiyon, üretim ortamı) eklendi. Boyut ortalaması **S/M/L = 1,5 / 4 / 8 gün** kabulüyle sprint yükleri:

| | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | S9 | S10 | Toplam |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Hikâye | 10 | 11 | 14 | 12 | 10 | 16 | 12 | 11 | 12 | 10 | **118** |
| Tahmini gün | 35 | 34 | 48 | 36 | 32 | 42 | 33 | 34 | 33 | 34 | **359** |
| İyimser (1/3/6) | 26 | 25 | 35 | 26 | 23 | 30 | 24 | 25 | 24 | 25 | **263** |

İki kişilik ekibin kapasitesi sprint başına **16–18 geliştirici günü** (2 kişi × 10 iş günü, törenler ve aylık saha günü düşülmüş). 10 sprint ≈ **160–180 gün**, tampon S11–S12 ile ≈ **192–216 gün**.

> **Bu plan kendi kapasitesinin ~2 katı.** 359 güne karşı en iyi hâlde 216 gün var; iyimser boyutlarla (263) bile açık ~50 gün. Bu notta daha önce yazan "~178 gün" **aritmetik hataydı**: hikâye başına ortalama 1,5 gün alınmış, yani 118 hikâyenin tamamı S sayılmıştı. Boyutlar geliştirici olmadan, PO tahminidir; gerçek sayı ilk planlama toplantısında ekibin kendi tahminiyle çıkar — ama hata payı ne olursa olsun **10 sprintte iki kişiyle bitmiyor**.

Açığı kapatmanın üç yolu var; **karar PO'nundur** ve geç kalırsa kendiliğinden 3. seçenek olur:

| | Ne | Etki |
|---|---|---|
| 1 | **Üçüncü geliştirici (web)** | Kapasite sprint başına ~25 güne çıkar, v1 ≈ 14 sprint; ekip maliyeti ADR-0009 tahmininin ~%50 üstüne gelir (₺375–600 bin/ay) |
| 2 | **Kapsamı daraltmak** | En büyük kalemler: PDF üretimi + aylık özet (S8 ≈ 34 gün), belge takvimi E-12 (≈ 14 gün), kiosk (≈ 12 gün), hash zinciri (≈ 10 gün). Dördü de satış argümanı; kesmek fizibiliteyi ve broşürü etkiler |
| 3 | **Takvimi uzatmak** | GA S10 yerine S14–S16 (Mayıs–Haziran 2027); fizibilitedeki "5–6 ay" ve ilandaki "Sprint 0 + 10 sprint ≈ 22 hafta" birlikte güncellenir |

Karar verilene kadar plan **olduğu gibi kalıyor**: sprint sınırları hedef, taahhüt değil. Her sprintte taşan iş sonraki sprinte düşer ve bu nottaki tablo (yük / kapasite) planlama toplantısının ilk gündem maddesidir. Riskli sprintler S3–S6 (motor + çevrimdışı) değişmedi; eski planda tampon sıfırdı ve kapsam %30 daha büyüktü.
