# Saha demosu · v1 gereksinim denetimi

Üretim: 5 Ekim 2026 · kaynak: [01-fonksiyonel-gereksinimler.md](../04-gereksinimler/01-fonksiyonel-gereksinimler.md) (123 v1 FR'si) · hedef: [saha-demosu.html](../05-tasarim/05-prototip/saha-demosu.html)

Bu belge, çalışan saha demosunun v1 kapsamını ne kadar karşıladığını satır satır gösterir. Demo bir **satış ve saha denemesi aracıdır**, ürün değildir: sunucu gerektiren maddeler bilerek dışarıda, ama hiçbiri sessizce atlanmamıştır — her biri ya "Üründe var" sekmesinde etiketli ekranla ya da bu tabloda gerekçesiyle durur.

| Durum | Anlamı | Sayı |
|---|---|---|
| ✅ çalışıyor | Demoda gerçekten çalışır, veriyle doğrulanır | 42 |
| 🟡 kısmen | Davranış var, gereksinimin bir parçası eksik (notta yazılı) | 23 |
| 🏷️ etiketli gösterim | "Üründe var" sekmesinde rozetli ekran/simülasyon; çalışmaz | 30 |
| ⚪ demo dışı | Sunucu/altyapı işi; demoda ekranı yok | 28 |

**Okuma kuralı:** 🟡 ve 🏷️ satırlar pilot sözleşmesinde taahhüt değildir; taahhüt edilen kapsam [06-v1-cekirdek-kapsam.md](../02-urun/06-v1-cekirdek-kapsam.md) ve ona bağlı FR listesidir. Demo, o kapsamın saha davranışını gösterir.

### CAP-01 · Hesap ve organizasyon

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-0101 | Sistem, her zinciri ayrı bir hesap (kiracı) olarak tutar | ⚪ demo dışı | Tek hesaplı demo; kiracı ayrımı sunucu işi |
| FR-0102 | Sistem dört seviyeli hiyerarşi tutar: Marka › Bölge › Şube › İstasyon | 🟡 kısmen | Şube düzeyi var; bölge ve istasyon yok |
| FR-0103 | Şube kaydı en az şunları taşır: kod (hesap içinde benzersiz), ad, adres, konum (enlem/boylam), saat dilimi, ha | 🟡 kısmen | Şube adı, kapanış/açılış saati var; adres, konum, tatil takvimi yok |
| FR-0104 | İstasyon kaydı şubeye bağlıdır (mutfak, bar, kasa, tuvalet, depo…) | ⚪ demo dışı | İstasyon ve QR demoda yok |
| FR-0105 | Sistem, bölge/şube/istasyon/personel için Excel şablonu sunar ve toplu yükler | 🏷️ etiketli gösterim | Kurulum sihirbazı · Excel adımı gösterim |
| FR-0106 | Toplu yüklemede satır bazlı doğrulama yapılır (zorunlu alan, benzersiz kod, geçerli saat dilimi, telefon forma | 🏷️ etiketli gösterim | Sihirbazda 23 kayıt / 2 hatalı satır gösterimi |
| FR-0107 | Yönetici personel ekler/düzenler: ad, telefon, şube(ler), istasyon(lar), rol, dil tercihi (i18n hazırlığı) | 🏷️ etiketli gösterim | Sihirbaz 4. adım: personel listesi |
| FR-0108 | Yeni personel için davet SMS'i (uygulama bağlantısı + tek kullanımlık kod) gönderilir | 🏷️ etiketli gösterim | Davet SMS'i gösterimde; demo göndermez |
| FR-0109 | Kullanıcı pasifleştirilebilir: giriş kapanır, gelecekteki atamaları kaldırılır, geçmiş cevap/kanıt/loglar deği | ⚪ demo dışı | Kullanıcı yönetimi demoda yok |
| FR-0110 | Pasif kullanıcının kimlik alanları (ad, telefon, avatar) maskelenebilir ("Eski personel #id") | ⚪ demo dışı | Maskeleme sunucu işi |

### CAP-02 · Kimlik ve yetki

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-0201 | Saha kullanıcıları telefon numarası + 6 haneli SMS OTP ile giriş yapar | 🏷️ etiketli gösterim | Telefon + 6 hane OTP akışı simülasyon (doğrulama sahte) |
| FR-0202 | Yönetici kullanıcılar e-posta + şifre ile giriş yapar (şifre politikası: ≥ 12 karakter, sızmış parola kontrolü | 🏷️ etiketli gösterim | Yönetici girişi gösterim kartında |
| FR-0203 | Mobil oturum 30 gün yenilenen belirteçle açık kalır | ⚪ demo dışı | Oturum/cihaz yönetimi demoda yok |
| FR-0204 | OTP: 60 sn'de bir yeniden gönderim | 🏷️ etiketli gösterim | Kurallar OTP ekranında yazılı, uygulanmıyor |
| FR-0205 | Roller (v1): Yönetici (merkez), Bölge müdürü, Şube müdürü, Personel | 🏷️ etiketli gösterim | Rol × kapsam matrisi gösterim kartında |
| FR-0207 | Şube cihazı (kiosk) kaydı: panelden üretilen QR'ı tablet okutur | ⚪ demo dışı | Cihaz kaydı (QR) demoda yok |
| FR-0208 | Kiosk modunda personel 4 haneli PIN ile geçiş yapar | 🟡 kısmen | 4 haneli PIN çalışıyor; PIN'i kullanıcı belirleme akışı yok (demoda PIN ekranda yazılı) |
| FR-0209 | Kiosk 2 dk hareketsizlikte kilitlenir | ✅ çalışıyor | 2 dk hareketsizlikte kilit, PIN'le kaldığı yerden devam |
| FR-0210 | 5 hatalı PIN → 1 dk blok | ⚪ demo dışı | Hatalı PIN bloğu demoda yok |
| FR-0211 | Şube müdürü, şubesindeki personele kioskta başlangıç PIN'i atayabilir (telefonu olmayan personel için) | 🏷️ etiketli gösterim | Şube müdürünün PIN ataması Blok 8 prototipinde; saha demosunda yok |

### CAP-03 · Şablon tasarımı

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-0301 | Şablonlar sürümlüdür: taslak → yayında → arşiv | 🏷️ etiketli gösterim | Şablon sürümleme kütüphane kartında anlatılıyor; editör yok |
| FR-0302 | Şablon bölümlerden, bölümler maddelerden oluşur | 🟡 kısmen | Bölüm–madde yapısı listelerde var; editör yok |
| FR-0303 | Madde türleri (v1): onay | ✅ çalışıyor | onay · seçim · sayı · sıcaklık · metin + fotoğraf zorunluluğu |
| FR-0304 | Madde ayarları (v1): zorunlu | ✅ çalışıyor | zorunlu / fotoğraf zorunlu / kritik / kabul aralığı |
| FR-0305 | Sıcaklık maddesinde kabul aralığı (min–maks) tanımlanır | ✅ çalışıyor | Aralık dışı değer maddeyi başarısız yapar |
| FR-0306 | Puan = geçen madde sayısı / puanlanan madde sayısı × 100 (bilgi amaçlı | ✅ çalışıyor | Puan = geçen zorunlu madde yüzdesi (bilgi) |
| FR-0307 | Kritik madde başarısızsa çalıştırma puandan bağımsız "Başarısız" işaretlenir | ✅ çalışıyor | Kritik başarısızsa çalıştırma Başarısız |
| FR-0308 | Şablon ayarları (v1): yalnızca kamera (galeri kapalı, varsayılan açık) | 🟡 kısmen | Kamera doğrudan açılır; şablon ayar ekranı yok (kural sabit) |
| FR-0309 | Editörde mobil önizleme (gerçek madde bileşenleriyle) | ⚪ demo dışı | Editör önizlemesi yok |
| FR-0311 | Kütüphane (v1): 9 Türkçe yeme-içme şablonu (kapanış, açılış, saatlik tuvalet/hijyen, soğuk zincir, haftalık de | 🏷️ etiketli gösterim | 8 şablon listeleniyor; 2'si çalışıyor, 6'sı madde önizlemesi |
| FR-0312 | Yayın doğrulaması: kritik + yapılamadı izinli çelişkisi, boş bölüm, kanıt zorunlu ama tür fotoğraf/video değil | ⚪ demo dışı | Yayın doğrulaması editörle gelir |

### CAP-04 · Koşullu mantık

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-0405 | Sabit kural (v1): 'Hayır / Uygun değil / aralık dışı' cevapta fotoğraf + not zorunlu ('başarısız cevapta kanıt | ✅ çalışıyor | Tek sabit kural: olumsuz cevap → fotoğraf + not, kritikse aksiyon |

### CAP-05 · Planlama ve pencereler

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-0501 | Plan = şablon sürümü + kapsam + tekrar + pencere + atama + hatırlatma + eskalasyon | 🟡 kısmen | Planlar sabit (açılış/kapanış); plan ekranı yok |
| FR-0502 | Kapsam: hiyerarşi ağacından çoklu seçim veya tek şube | ⚪ demo dışı | Kapsam seçimi plan ekranıyla gelir |
| FR-0503 | Tekrar RRULE olarak saklanır | ⚪ demo dışı | RRULE demoda yok (günlük sabit tekrar) |
| FR-0504 | Pencere: başlangıç ve bitiş saati şube saat diliminde | ✅ çalışıyor | Pencere başlangıç/bitiş şube saatinden hesaplanır |
| FR-0505 | Gece yarısını aşan pencere (örn | ✅ çalışıyor | Gece yarısını aşan kapanış penceresi aynı iş gününe yazılır |
| FR-0506 | Tolerans (geç gönderim süresi) plan bazında 0–240 dk | ✅ çalışıyor | Tolerans içinde gönderim 'Geç tamamlandı' |
| FR-0507 | "Çalışma saatlerinden türet" seçeneği: açılış listesi açılıştan 60 dk önce–60 dk sonra | ✅ çalışıyor | Pencere şube açılış/kapanış saatinden türetiliyor |
| FR-0508 | Atama modeli (v1): rol (o şubede o role sahip herkes), kişi veya şubedeki herkes (varsayılan) | 🟡 kısmen | Şubedeki herkes görür; 'biri tamamlasın' kilidi yok |
| FR-0509 | Hatırlatma (v1, sabit): pencere açılışında ve bitişe 30 dk kala push | 🏷️ etiketli gösterim | Hatırlatma bildirimi gösterim kartında |
| FR-0511 | Plan kaydetmeden önce 7 günlük çalıştırma önizlemesi (şube × pencere), kapalı günler düşülmüş | ⚪ demo dışı | 7 günlük önizleme plan ekranıyla gelir |
| FR-0512 | Tek seferlik liste: tarih, son saat, hedef şubeler, atanan | ⚪ demo dışı | Tek seferlik liste demoda yok |
| FR-0513 | Zamanlayıcı her saat başı tüm aktif planlar için 7 gün ileriye çalıştırma üretir | 🟡 kısmen | Pencereler anlık hesaplanıyor; zamanlayıcı üretimi sunucu işi |
| FR-0514 | Çalıştırma durumları ve geçişleri: Planlandı → Açık → Devam ediyor → Tamamlandı / Geç tamamlandı / Kaçırıldı | ✅ çalışıyor | Planlandı → açık → tamamlandı / geç / kaçırıldı / yapılmayacak + başarısız |
| FR-0515 | Şube kapalı gün takviminde çalıştırma üretilmez | ⚪ demo dışı | Kapalı gün takvimi demoda yok |
| FR-0516 | Plan değişince yalnızca "Planlandı" durumundaki gelecek çalıştırmalar yeniden hesaplanır | ⚪ demo dışı | Plan değişikliği demoda yok |
| FR-0517 | Aynı şube + şablon + çakışan pencere için ikinci plan kaydedilemez | ⚪ demo dışı | Çakışan plan kontrolü demoda yok |
| FR-0519 | Şube müdürü günün çalıştırmalarında atananı değiştirebilir | ⚪ demo dışı | Atama değiştirme Blok 8 prototipinde |
| FR-0520 | Atama değişikliği yeni atanana anında bildirilir | ⚪ demo dışı | Atama bildirimi sunucu işi |
| FR-0521 | Atanmamış çalıştırma şubedeki herkeste görünür | 🟡 kısmen | 'X yapıyor' bilgisi var; 30 dk'lık çalıştırma kilidi yok |
| FR-0522 | Belge kaydı: ad, tür (yangın tüpü · baca temizliği · su deposu · periyodik elektrik kontrolü · hijyen eğitimi  | ✅ çalışıyor | 7 belge türü, şube, bitiş, sorumlu, belge fotoğrafı |
| FR-0523 | Belge uyarıları: geçerlilik bitişine 30 ve 7 gün kala sorumluya ve şube müdürüne push + sabah özeti satırı | ✅ çalışıyor | 30/7 gün eşikleri, süresi geçende yüksek öncelikli iş; push etiketli |
| FR-0524 | Belge görünümü: zincir genelinde "yaklaşanlar ve süresi geçenler" listesi (şube × belge türü), dönem PDF'i | ✅ çalışıyor | Zincir geneli liste + dönem PDF'i |

### CAP-06 · Mobil yürütme ve kanıt

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-0601 | Bugün ekranı: kullanıcıya/şubesine atanan bugünkü çalıştırmalar | ✅ çalışıyor | Bugün ekranı: durum rengi, geri sayım, ilerleme, tek dokunuşla başlat |
| FR-0602 | Madde cevaplama bileşenleri tür bazında (onay, seçim düğmeleri, sayısal klavye, sıcaklık, metin, kamera, video | 🟡 kısmen | Beş tür çalışıyor; video, imza, barkod, tarih bileşenleri yok |
| FR-0603 | İlerleme çubuğu | ✅ çalışıyor | İlerleme çubuğu; cevaplar anında saklanır, kapanınca devam eder |
| FR-0604 | Kanıt yakalama: fotoğraf zorunlu maddede kamera doğrudan açılır, çekim madde cevabını tamamlar (2 dokunuş) | ✅ çalışıyor | Fotoğraf zorunlu maddede kamera doğrudan açılır (capture) |
| FR-0605 | Fotoğraf cihazda ~300 KB'a (uzun kenar 1600 px, JPEG %75) sıkıştırılır | 🟡 kısmen | 900 px / JPEG %55 (artifact belge sınırı); üründe 1600 px / %75 |
| FR-0606 | Sunucu, kanıta sunucu zamanı, (izin varsa) konum, şube mesafesi, kullanıcı, cihaz ve dosya SHA-256'sını bağlar | 🟡 kısmen | SHA-256 ve damga tarayıcıda; sunucu zamanı, konum ve mesafe yok |
| FR-0607 | Zorunlu maddeler cevaplanmadan gönderim düğmesi pasif | ✅ çalışıyor | Eksik zorunlu maddede gönderim pasif; gönderilen kayıt salt okunur |
| FR-0610 | Pencere geri sayımı ve tolerans göstergesi | ✅ çalışıyor | Geri sayım · pencere kapanınca geç uyarısı · tolerans dolunca kilit |
| FR-0611 | Dokunma hedefleri ≥ 44 px, ikon + kısa etiket, yüksek kontrast, tek elle akış | 🟡 kısmen | Ana hedefler ≥ 44 px; bazı ikincil düğmeler 33–40 px |
| FR-0613 | Açılış listesinin başında 'dün gece' bloğu: önceki iş gününün kapanış çalıştırmasında yapılamayan ve başarısız | ✅ çalışıyor | Açılış listesinin başında dün gece bloğu |
| FR-0614 | Kanıt tekilliği: yüklenen dosyanın SHA-256 özeti aynı hesapta daha önce kullanılmışsa yükleme reddedilir | ✅ çalışıyor | Aynı dosya ikinci kez reddedilir, deneme olay izinde |
| FR-0615 | Kanıt bayrakları: galeriden yükleme denemesi, konum şube dışında (> 150 m), konum yok, cihaz saati farkı > 10  | 🟡 kısmen | İki bayrak çalışıyor (galeri/eski dosya); konum, cihaz saati, geç senk sunucu işi |

### CAP-07 · Çevrimdışı çalışma

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-0701 | Uygulama açılışta ve her 15 dk'da sonraki 48 saatin çalıştırmalarını, şablon sürümlerini, sebep setlerini önbe | 🏷️ etiketli gösterim | Önbellek çevrimdışı kartında anlatılıyor |
| FR-0702 | Bağlantı yokken cevaplar ve kanıtlar yerel kuyrukta (SQLite + dosya sistemi, şifreli) | 🏷️ etiketli gösterim | Kuyruk simülasyonu: iki kayıt bekliyor rozetiyle |
| FR-0703 | Bağlantı gelince arka planda senk: önce cevaplar, sonra kanıtlar | 🏷️ etiketli gösterim | Bağlantı gelince sırayla gönderim simülasyonu |
| FR-0704 | Sunucu, cihaz–sunucu saat farkını senk anında hesaplar | 🏷️ etiketli gösterim | Sunucu saat farkı kartta yazılı |
| FR-0705 | Çakışma kuralı: madde bazlı son yazan kazanır | ⚪ demo dışı | Çakışma kuralı sunucu işi |
| FR-0706 | Kuyruk sınırı 500 kanıt / 72 saat | 🏷️ etiketli gösterim | 500 kanıt / 72 saat sınırı kartta yazılı |
| FR-0707 | Yükleme idempotent (istemci üretimli UUID) | ⚪ demo dışı | İdempotent yükleme sunucu işi |
| FR-0708 | Senk durumu ekranı: bekleyen kayıt/kanıt sayısı, son senk zamanı, hata ayrıntısı (destek için kopyalanabilir) | 🏷️ etiketli gösterim | Senk durumu kuyruk kartında |

### CAP-08 · Yapılamadı ve sorun bildirimi

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-0801 | Madde ekranında 'Yapılamadı': sebep seçimi zorunlu (sabit set: malzeme yok, ekipman arızalı, zaman yetmedi, ye | ✅ çalışıyor | Sebep seti, not/fotoğraf isteğe bağlı, aksiyon açılır |
| FR-0803 | "Diğer" seçilirse not zorunlu (≥ 5 karakter) | ✅ çalışıyor | 'Diğer' seçilince not zorunlu |
| FR-0804 | Kritik maddede veya şablon kapatmışsa "Yapılamadı" düğmesi görünmez | ✅ çalışıyor | Kritik maddede Yapılamadı düğmesi yok + açıklama |
| FR-0806 | Liste dışı sorun bildirimi: sabit kategori (ekipman, tedarik, hijyen, güvenlik, diğer), 1–3 fotoğraf, not | ✅ çalışıyor | Beş kategori, fotoğraf, not; güvenlik sınırı ekranda |
| FR-0807 | Şube müdürü sorunu tek dokunuşla aksiyona çevirir (atanan varsayılan kendisi, vade orta | 🟡 kısmen | Sorun doğrudan aksiyon kuyruğuna düşer; şube müdürünün 'çevir/kapat' ayrımı yok |

### CAP-09 · Aksiyon ve eskalasyon

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-0901 | Aksiyon alanları (v1): başlık, kaynak (madde cevabı / sorun / elle / kaçırma), şube, atanan, vade, öncelik (or | ✅ çalışıyor | Başlık, kaynak, şube, atanan, vade, öncelik, durum, notlar |
| FR-0902 | Koşullu mantık, aralık dışı ölçüm, "yapılamadı" ve kaçırılan çalıştırma otomatik aksiyon oluşturur | ✅ çalışıyor | Aralık dışı, yapılamadı, kaçırılan çalıştırma ve sorun aksiyon açar |
| FR-0903 | Varsayılan atanan: şube müdürü (tanımlı değilse bölge müdürü) | ✅ çalışıyor | Varsayılan atanan şube müdürü; vade kritik 4 / yüksek 24 / orta 72 sa |
| FR-0904 | Durum (v1): açık → kapalı | 🟡 kısmen | Açık → kapalı ve olay kaydı var; rol bazlı kapatma yetkisi yok |
| FR-0905 | Kapatırken not zorunlu, fotoğraf isteğe bağlı | ✅ çalışıyor | Kapatırken not zorunlu |
| FR-0907 | Aksiyon listeleri: bana atananlar, şubem, bölgem, gecikmişler, kritikler | 🟡 kısmen | Açık / gecikmiş / tümü filtreleri; bana atananlar, şubem, bölgem yok |
| FR-0908 | Elle aksiyon oluşturma (yetkili roller) | ✅ çalışıyor | Elle aksiyon: başlık, şube, öncelik, not |
| FR-0910 | Aksiyon olayları (v1): atandı (anında push), gecikti (sabah özetinde) | 🟡 kısmen | Gecikmiş aksiyon listede işaretli; atama push'u gösterim |
| FR-0911 | Eskalasyon tetikleri: çalıştırma "Kaçırıldı" | 🟡 kısmen | Kaçırıldı ve kritik başarısız tetikleri var; vade aşımı bildirimi gösterim |
| FR-0912 | Eskalasyon (v1, sabit): kaçırılan liste → şube müdürüne anında push, bölge müdürüne 07:00 sabah özeti (FR-1212 | 🏷️ etiketli gösterim | Eskalasyon merdiveni bildirim kartında anlatılıyor |
| FR-0913 | Her eskalasyon adımı olay günlüğüne ve ilgili aksiyonun yorum dizisine yazılır | 🟡 kısmen | Olay izi var; aksiyon yorum dizisi yok |
| FR-0914 | Çalıştırma "Yapılmayacak" işaretlenince veya aksiyon kapanınca merdiven durur | ✅ çalışıyor | Yapılmayacak işaretlenince ve aksiyon kapanınca merdiven durur |
| FR-0915 | Adımın alıcısı yoksa (rol boş, kullanıcı pasif) bir üst adıma geçilir | ⚪ demo dışı | Alıcı yok durumu sunucu işi |

### CAP-10 · Bildirimler

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-1001 | Push bildirimleri (FCM/APNs): liste açıldı, hatırlatma, pencere kapandı, aksiyon olayları, duyuru, eskalasyon | 🏷️ etiketli gösterim | Push türleri bildirim kartında; demo göndermez |
| FR-1002 | SMS (v1): OTP | 🏷️ etiketli gösterim | SMS yalnızca OTP ve kritik teslimat — kartta yazılı |
| FR-1004 | Sessiz saatler sabit (23:00–07:00): yönetici push'ları sabah özetine ertelenir | 🏷️ etiketli gösterim | Sessiz saat kuralı sabah özeti bandında |
| FR-1005 | Teslimat izi: her bildirim için kanal, alıcı, gönderim, teslim/okunma durumu, hata kodu | 🏷️ etiketli gösterim | Kanal, alıcı ve zaman bildirim kartında |
| FR-1006 | Cihaz token yönetimi: geçersiz token temizlenir | ⚪ demo dışı | Token yönetimi sunucu işi |
| FR-1007 | Bildirim servisi kanal-bağımsız arayüz sunar (kanal eklenmesi — WhatsApp v1 | ⚪ demo dışı | Kanal arayüzü mimari gereksinim |
| FR-1008 | Kritik madde başarısız olduğunda şube müdürü ve bölge müdürüne anında push | 🏷️ etiketli gösterim | Kritik bildirim kartı: anında push, 10 dk'da SMS |

### CAP-12 · Raporlama ve dışa aktarım

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-1201 | Operasyon ızgarası: şube × liste hücreleri (gün seçici) | ✅ çalışıyor | Şube × liste ızgarası + istisna görünümü (geç/kaçırıldı/başarısız/yapılamadı) |
| FR-1202 | Çalıştırma detayı: madde cevapları, kanıt küçük resimleri ve tam boy görüntü, damga bilgisi, puan, aksiyonlar, | ✅ çalışıyor | Madde cevapları, kanıtlar, damga, puan, aksiyonlar, olay izi |
| FR-1207 | Ölçüm günlüğü: ekipman/istasyon bazlı zaman serisi | ✅ çalışıyor | Ölçüm günlüğü: zaman serisi, aralık dışı işaretli, dönem çıktısı |
| FR-1208 | Kanıt galerisi (v1): şube ve tarih filtresi | ✅ çalışıyor | Kanıt galerisi: şube ve gün filtresi, ızgara, damga meta verisi |
| FR-1211 | Yönetici mobil görünümü (v1): 'Bölgem/Şubem' listesi — şube × dün gece durumu (renk + ikon), dokununca çalıştı | 🟡 kısmen | Pano telefonda çalışıyor; ayrı 'Bölgem' mobil görünümü yok |
| FR-1212 | Sabah özeti (v1): her gün 07:00 push + e-posta — bölge müdürüne bölgesi, yöneticiye tüm hesap: dün gece kaçıra | ✅ çalışıyor | Sabah özeti ekranda hesaplanıyor; gönderim etiketli |
| FR-1213 | Çalıştırma PDF'i: markalı | ✅ çalışıyor | Çalıştırma PDF'i: maddeler, kanıtlar, damga, olay izi, doğrulama kodu |
| FR-1214 | Dönem PDF'i: şube + şablon + tarih aralığı | ✅ çalışıyor | Dönem PDF'i: ölçüm günlüğü ve belge takvimi |
| FR-1217 | Büyük çıktılar (≥ 500 çalıştırma) arka planda üretilir | ⚪ demo dışı | Arka plan üretimi sunucu işi |
| FR-1218 | PDF doğrulama kodu olay günlüğü zincirine bağlıdır | 🟡 kısmen | Doğrulama kodu üretiliyor; zincire bağlama hash kartında simülasyon |
| FR-1219 | İstisna görünümü: FR-1201'in varsayılanı | ✅ çalışıyor | İstisna görünümü varsayılan; 'her şey yolunda' durumu var |
| FR-1220 | Aylık tek sayfa özet: seçilen ay için % zamanında, geç, kaçırıldı, yapılmayacak | ✅ çalışıyor | Aylık özet: zamanında, geç, kaçırılan, yapılmayacak, başarısız, yapılamadı |

### CAP-13 · Denetim izi ve uyum

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-1301 | Ekle-yalnız olay günlüğü: aktör, olay türü, nesne, önce/sonra özeti, zaman (sunucu), IP, cihaz | 🟡 kısmen | Ekle-yalnız olay izi çalışıyor; hash zinciri simülasyon kartında hesaplanıyor |
| FR-1304 | Zincir doğrulama komutu (iç araç): seçilen aralıkta hash zinciri yeniden hesaplanır, kırılma raporlanır | 🏷️ etiketli gösterim | Zincir doğrulama/bozma denemesi gösterimde |
| FR-1305 | Güvenlik: TLS 1 | ⚪ demo dışı | Altyapı güvenliği demo dışı |
| FR-1306 | Biyometrik veri işlenmez | ✅ çalışıyor | Biyometri yok; kimlik PIN (ADR-0007 sınırı korunuyor) |
| FR-1307 | İlk girişte aydınlatma metni (hesap yöneticisi özelleştirir | 🏷️ etiketli gösterim | Aydınlatma metni KVKK kartında |
| FR-1308 | Konum izni ayrı ekranda, amaç açıklamasıyla | ⚪ demo dışı | Konum izni demoda alınmıyor (ayar notunda yazılı) |
| FR-1310 | Silme/maskeleme (v1: destek betiği, hesap yöneticisinin talebiyle, ≤ 30 gün): kimlik alanları maskelenir | 🏷️ etiketli gösterim | Silme/maskeleme talebi KVKK akışında (kayıt oluşmaz) |
| FR-1311 | Saklama sabit 24 ay: süresi dolan kanıt dosyaları arka planda silinir, cevap değerleri ve olay günlüğü özeti k | 🏷️ etiketli gösterim | 24 ay saklama KVKK kartında |
| FR-1312 | Veri işleme sözleşmesi ve aydınlatma metni şablonları ürün içinde indirilebilir (doküman) | ⚪ demo dışı | Sözleşme şablonları depoda, demoda değil |

### CAP-14 · Yönetim paneli ve platform

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-1401 | Kurulum sihirbazı (v1, 4 adım): marka + şubeler (Excel/elle) → kapanış şablonu (kütüphaneden, düzenlenebilir)  | 🏷️ etiketli gösterim | Kurulum sihirbazı 4 adım gezilebilir, kaydetmez |
| FR-1403 | Aktif şube sayacı ve dönem raporu (manuel faturalama için) | 🏷️ etiketli gösterim | Aktif şube sayacı ve dönem faturası önizlemesi |

### CAP-15 / 16 / 17 / 18 · v1.1 (FR-1803 hariç)

| FR | Gereksinim (özet) | Durum | Not |
|---|---|---|---|
| FR-1803 | Arayüz metinleri kaynak dosyada (i18n) | ⚪ demo dışı | i18n kaynak dosyası demo dışı |
