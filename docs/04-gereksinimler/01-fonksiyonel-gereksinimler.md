# Fonksiyonel gereksinimler

Kimlik: `FR-CCNN` (CC = yetenek numarası, NN = sıra). Öncelik: **M** MVP zorunlu · **S** süre izin verirse MVP · **C** v1.x. Her satır en az bir use case'e bağlıdır; kabul kriterleri 06-test/02'de TC olarak açılır. "Sistem" = Talimatname (mobil + web + backend).

## CAP-01 · Hesap ve organizasyon

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-0101 | Sistem, her zinciri ayrı bir hesap (kiracı) olarak tutar; bir hesabın verisi başka hesaptan hiçbir uç noktada okunamaz. | M | UC-01 |
| FR-0102 | Sistem dört seviyeli hiyerarşi tutar: Marka › Bölge › Şube › İstasyon; bölge isteğe bağlıdır (şube doğrudan markaya bağlanabilir). | M | UC-01 |
| FR-0103 | Şube kaydı en az şunları taşır: kod (hesap içinde benzersiz), ad, adres, konum (enlem/boylam), saat dilimi, haftalık çalışma saatleri, kapalı gün takvimi, şube türü (etiket). | M | UC-01 |
| FR-0104 | İstasyon kaydı şubeye bağlıdır (mutfak, bar, kasa, tuvalet, depo…); madde ve kanıt istasyona bağlanabilir; istasyon QR kodu üretilebilir. | M | UC-01 |
| FR-0105 | Sistem, bölge/şube/istasyon/personel için Excel şablonu sunar ve toplu yükler; şablon sürümü dosyada yazılıdır. | M | UC-01 |
| FR-0106 | Toplu yüklemede satır bazlı doğrulama yapılır (zorunlu alan, benzersiz kod, geçerli saat dilimi, telefon formatı); %20'den fazla satır hatalıysa yükleme reddedilir; hatalı satırlar indirilebilir rapor olarak döner. | M | UC-01 |
| FR-0107 | Yönetici personel ekler/düzenler: ad, telefon, şube(ler), istasyon(lar), rol, dil tercihi (i18n hazırlığı). | M | UC-02 |
| FR-0108 | Yeni personel için davet SMS'i (uygulama bağlantısı + tek kullanımlık kod) gönderilir; teslim durumu panelde görünür; yeniden gönderilebilir. | M | UC-02 |
| FR-0109 | Kullanıcı pasifleştirilebilir: giriş kapanır, gelecekteki atamaları kaldırılır, geçmiş cevap/kanıt/loglar değişmeden kalır. | M | UC-02 |
| FR-0110 | Pasif kullanıcının kimlik alanları (ad, telefon, avatar) maskelenebilir ("Eski personel #id"); işletme kayıtları anonim kalır. | M | UC-02, UC-18 |

## CAP-02 · Kimlik ve yetki

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-0201 | Saha kullanıcıları telefon numarası + 6 haneli SMS OTP ile giriş yapar; e-posta zorunlu değildir. | M | UC-03 |
| FR-0202 | Yönetici kullanıcılar e-posta + şifre ile giriş yapar; TOTP tabanlı 2FA isteğe bağlı, hesap yöneticisi için zorunlu kılınabilir. | M | UC-03 |
| FR-0203 | Mobil oturum 30 gün yenilenen belirteçle açık kalır; web oturumu 12 saat; cihaz/oturum listesi ve uzaktan sonlandırma. | M | UC-03 |
| FR-0204 | OTP: 60 sn'de bir yeniden gönderim; 3 hatalı denemede 15 dk blok; OTP 5 dk geçerli. | M | UC-03 |
| FR-0205 | Roller: Hesap yöneticisi, Operasyon müdürü, Kalite, Bölge müdürü, Şube müdürü, Personel, Gözlemci. Yetki = rol × kapsam (hesap/bölge/şube); matris 06-kvkk-ve-guvenlik.md'de; her uç nokta sunucu tarafında kapsam denetler. | M | UC-02 |
| FR-0206 | Akıllı gruplar: rol, bölge, şube, istasyon ve şube türü kurallarıyla dinamik üyelik; atama ve duyuru hedeflemesinde kullanılır; üyelik her değerlendirmede yeniden hesaplanır. | M | UC-02, UC-06, UC-14 |
| FR-0207 | Şube cihazı (kiosk) kaydı: panelden üretilen QR'ı tablet okutur; cihaz şubeye bağlanır; cihaz adı, model, son görülme kaydedilir; panelden kaldırılabilir. | M | UC-02, UC-04 |
| FR-0208 | Kiosk modunda personel 4 haneli PIN ile geçiş yapar; PIN ilk girişte kullanıcı tarafından belirlenir; şube müdürü sıfırlayabilir (olay logda). | M | UC-04 |
| FR-0209 | Kiosk 2 dk hareketsizlikte kilitlenir; tamamlanmamış madde cevapları yerelde korunur ve aynı kullanıcı geri dönünce devam eder. | M | UC-04 |
| FR-0210 | 5 hatalı PIN → 1 dk blok; art arda 3 blok → şube müdürüne bildirim. | M | UC-04 |

## CAP-03 · Şablon tasarımı

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-0301 | Şablonlar sürümlüdür: taslak → yayında → arşiv; yayındaki sürüm değiştirilemez, düzenleme yeni taslak sürüm açar. | M | UC-05 |
| FR-0302 | Şablon bölümlerden, bölümler maddelerden oluşur; sürükle-bırak sıralama; madde kopyalama. | M | UC-05 |
| FR-0303 | Madde türleri: onay; çoktan seçmeli (tek/çok seçim, küresel yanıt setleri); sayı + birim; sıcaklık (°C); metin; fotoğraf (1–5); video (≤20 sn); imza; barkod/QR; tarih-saat; talimat (metin, görsel, PDF, video bağlantısı — cevap gerektirmez). | M | UC-05 |
| FR-0304 | Madde ayarları: zorunlu; kanıt zorunlu (fotoğraf/video); puan ağırlığı (0–10); kritik; ipucu metni; istasyon bağı; yapılamadı izinli (varsayılan evet, kritik maddede hayır). | M | UC-05 |
| FR-0305 | Sıcaklık maddesinde kabul aralığı (min–maks) tanımlanır; aralık dışı değer maddeyi "başarısız" yapar ve koşullu mantık tetiklenebilir. | M | UC-05, UC-08 |
| FR-0306 | Puanlama: liste puanı = Σ(geçen madde ağırlığı) / Σ(puanlanan madde ağırlığı); başarı eşiği şablon bazında (varsayılan %90); talimat ve "yapılmayacak" maddeleri puanlanmaz. | M | UC-05 |
| FR-0307 | Kritik madde başarısızsa çalıştırma puandan bağımsız "Başarısız" işaretlenir. | M | UC-05, UC-08 |
| FR-0308 | Şablon ayarları: yalnızca kamera (galeri kapalı), tolerans varsayılanı, sebep seti seçimi, gözden geçirme gerekli mi (Should). | M | UC-05 |
| FR-0309 | Editörde mobil önizleme (gerçek madde bileşenleriyle). | M | UC-05 |
| FR-0310 | Yayın: hemen veya tarihli; yayınla birlikte hangi planların etkileneceği listelenir. | M | UC-05 |
| FR-0311 | Kütüphane: en az 30 Türkçe yeme-içme şablonu (açılış, kapanış, saatlik hijyen, soğuk zincir, yağ değişimi, kasa devri, haftalık derin temizlik, alerjen, zararlı kontrolü, teslimat kabul…); kopyala-düzenle; kütüphane merkezî güncellenir, kopyalar bağımsız. | M | UC-05 |
| FR-0312 | Yayın doğrulaması: kritik + yapılamadı izinli çelişkisi, boş bölüm, kanıt zorunlu ama tür fotoğraf/video değil → yayın engellenir, açıklama. | M | UC-05 |

## CAP-04 · Koşullu mantık

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-0401 | Madde bazında kural: koşul = (cevap eşittir / içerir / aralık dışı / boş); bir maddede birden çok kural. | M | UC-05 |
| FR-0402 | Eylemler: ek soru göster (aynı bölümde dinamik madde), not iste, fotoğraf iste, aksiyon oluştur (atanan kuralı: şube müdürü / bölge müdürü / kişi; öncelik), bildir (rol/kişi, kanal), bölüm atla. | M | UC-05, UC-08 |
| FR-0403 | Kurallar mobilde çevrimdışı da değerlendirilir; aksiyon ve bildirim eylemleri senk anında sunucuda yürütülür (çift oluşturma yok — idempotent anahtar). | M | UC-08, UC-09 |
| FR-0404 | Editörde "kuralı dene": örnek cevapla tetiklenen eylemler listelenir. | S | UC-05 |

## CAP-05 · Planlama ve pencereler

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-0501 | Plan = şablon sürümü + kapsam + tekrar + pencere + atama + hatırlatma + eskalasyon; aktif/pasif. | M | UC-06 |
| FR-0502 | Kapsam: hiyerarşi ağacından çoklu seçim, akıllı grup veya tek şube; kapsam değişince gelecekteki üretim güncellenir. | M | UC-06 |
| FR-0503 | Tekrar RRULE olarak saklanır; arayüz seçenekleri: günlük (birden çok saat), her N saat (başlangıç–bitiş aralığında), haftanın günleri, aylık (ayın günü veya n'inci hafta günü), bitiş tarihi. | M | UC-06 |
| FR-0504 | Pencere: başlangıç ve bitiş saati şube saat diliminde; süre ≤ 24 sa (tolerans dahil). | M | UC-06 |
| FR-0505 | Gece yarısını aşan pencere (örn. 22:00–01:30) açılış gününe ait "iş günü" olarak raporlanır. | M | UC-06, UC-07 |
| FR-0506 | Tolerans (geç gönderim süresi) plan bazında 0–240 dk; tolerans içinde gönderim "Geç tamamlandı". | M | UC-06 |
| FR-0507 | "Çalışma saatlerinden türet" seçeneği: açılış listesi açılıştan 60 dk önce–60 dk sonra; kapanış listesi kapanıştan 120 dk önce–90 dk sonra (varsayılanlar düzenlenebilir); şube saatleri değişince pencere kendiliğinden güncellenir. | M | UC-06 |
| FR-0508 | Atama modeli: rol (o şubede o role sahip herkes), kişi, grup, istasyon; tamamlama kuralı "biri tamamlasın" (ilk gönderim listeyi kapatır) veya "herkes tamamlasın" (her atanan kendi bölümünü gönderir). | M | UC-06, UC-19 |
| FR-0509 | Hatırlatma politikası: açılışta, bitişe N dk kala, bitişte; kanal seçimi (push; kritik listede SMS ek). | M | UC-06, UC-07 |
| FR-0510 | Eskalasyon merdiveni: sıralı adımlar (alıcı rolü/kişi, gecikme süresi, kanal); varsayılan üç adım (BR-11); plan bazında özelleştirilebilir. | M | UC-06, UC-13 |
| FR-0511 | Plan kaydetmeden önce 7 günlük çalıştırma önizlemesi (şube × pencere), kapalı günler düşülmüş. | M | UC-06 |
| FR-0512 | Tek seferlik liste: tarih, son saat, hedef şubeler, atanan; tekrar üretmez. | M | UC-06 |
| FR-0513 | Zamanlayıcı her saat başı tüm aktif planlar için 7 gün ileriye çalıştırma üretir; aynı (plan, şube, pencere başlangıcı) için tek kayıt (benzersiz anahtar). | M | UC-07 |
| FR-0514 | Çalıştırma durumları ve geçişleri: Planlandı → Açık → Devam ediyor → Tamamlandı / Geç tamamlandı / Kaçırıldı; Planlandı/Açık → Yapılmayacak (yönetici + sebep); Tamamlandı/Geç → Başarısız (puan/kritik). Geçişler zamanlayıcı ve gönderim olaylarıyla tetiklenir; her geçiş logda. | M | UC-07, UC-08 |
| FR-0515 | Şube kapalı gün takviminde çalıştırma üretilmez; rapor hücresi "kapalı"; hesap düzeyi resmî tatil takvimi şubeye devralınır, şube geçersiz kılabilir. | M | UC-07 |
| FR-0516 | Plan değişince yalnızca "Planlandı" durumundaki gelecek çalıştırmalar yeniden hesaplanır; Açık/Devam olanlar korunur. | M | UC-07 |
| FR-0517 | Aynı şube + şablon + çakışan pencere için ikinci plan kaydedilemez. | M | UC-06 |
| FR-0518 | Vardiya bazlı tekrar: şube vardiya saatleri tanımıyla "her vardiya devrinde" penceresi. | S | UC-06 |
| FR-0519 | Şube müdürü günün çalıştırmalarında atananı değiştirebilir; "herkes tamamlasın" listelerinde kişi ekleyip çıkarabilir. | M | UC-19 |
| FR-0520 | Atama değişikliği yeni atanana anında bildirilir; eski atanandan kaldırılır; olay logda. | M | UC-19 |

## CAP-06 · Mobil yürütme ve kanıt

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-0601 | Bugün ekranı: kullanıcıya/şubesine atanan bugünkü çalıştırmalar; durum rengi, pencere geri sayımı, ilerleme; tek dokunuşla başlat. | M | UC-08 |
| FR-0602 | Madde cevaplama bileşenleri tür bazında (onay, seçim düğmeleri, sayısal klavye, sıcaklık, metin, kamera, video, imza alanı, barkod tarayıcı, tarih-saat). | M | UC-08 |
| FR-0603 | İlerleme çubuğu; uygulama kapansa da kaldığı yerden devam; cevaplar yerelde anında saklanır. | M | UC-08 |
| FR-0604 | Kanıt yakalama uygulama içi kamerayla; şablon "yalnızca kamera" ise galeri seçeneği görünmez; madde başına 1–5 fotoğraf, video ≤ 20 sn. | M | UC-08 |
| FR-0605 | Fotoğraf cihazda ~300 KB (uzun kenar 1600 px, JPEG %75), video ≤ 3 MB'a sıkıştırılır; ham EXIF'ten yalnızca çekim zamanı ve konum alınır. | M | UC-08 |
| FR-0606 | Sunucu, kanıta sunucu zamanı, (izin varsa) konum, şube mesafesi, kullanıcı, cihaz ve dosya SHA-256'sını bağlar; görünür damgalı (şube · tarih-saat · kullanıcı) kopya üretir; ham dosya saklanır. | M | UC-08 |
| FR-0607 | Zorunlu maddeler cevaplanmadan gönderim düğmesi pasif; gönderimde puan ve durum hesaplanır; gönderilen çalıştırma salt okunur. | M | UC-08 |
| FR-0608 | Gönderim sonrası düzeltme "ek kayıt" olarak eklenir (yeni cevap + not); eski cevap görünür kalır. | M | UC-08 |
| FR-0609 | Aynı çalıştırmada birden çok kullanıcı: madde bazlı kilit (60 sn), çakışmada son yazan kazanır, kanıt silinmez. | M | UC-08, UC-09 |
| FR-0610 | Pencere geri sayımı ve tolerans göstergesi; pencere kapanınca "geç" uyarısı; tolerans bitince düzenleme kilidi. | M | UC-08 |
| FR-0611 | Dokunma hedefleri ≥ 44 px, ikon + kısa etiket, yüksek kontrast, tek elle akış; ekran okuyucu etiketleri. | M | UC-08 |
| FR-0612 | İstasyon QR'ı taranınca o istasyonun açık listesi/maddeleri açılır; kanıt istasyona bağlanır. | S | UC-08 |

## CAP-07 · Çevrimdışı çalışma

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-0701 | Uygulama açılışta ve her 15 dk'da sonraki 48 saatin çalıştırmalarını, şablon sürümlerini, sebep setlerini önbelleğe alır. | M | UC-09 |
| FR-0702 | Bağlantı yokken cevaplar ve kanıtlar yerel kuyrukta (SQLite + dosya sistemi, şifreli); ekranda "bekliyor" rozeti. | M | UC-09 |
| FR-0703 | Bağlantı gelince arka planda senk: önce cevaplar, sonra kanıtlar; kullanıcı etkileşimi gerekmez; başarısız parçalar üstel geri çekilmeyle yeniden denenir. | M | UC-09 |
| FR-0704 | Sunucu, cihaz–sunucu saat farkını senk anında hesaplar; çekim zamanını düzeltir; ham cihaz zamanı ve fark logda. | M | UC-09 |
| FR-0705 | Çakışma kuralı: madde bazlı son yazan kazanır; kanıt dosyaları hiçbir durumda silinmez; çakışma olayı logda. | M | UC-09 |
| FR-0706 | Kuyruk sınırı 500 kanıt / 72 saat; sınırda yeni fotoğraf engellenir ve uyarı; 72 saatten eski kayıtlar "geç senk" bayrağıyla senklenir. | M | UC-09 |
| FR-0707 | Yükleme idempotent (istemci üretimli UUID); yarım kalan yükleme kaldığı yerden devam eder. | M | UC-09 |
| FR-0708 | Senk durumu ekranı: bekleyen kayıt/kanıt sayısı, son senk zamanı, hata ayrıntısı (destek için kopyalanabilir). | M | UC-09 |

## CAP-08 · Yapılamadı ve sorun bildirimi

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-0801 | Madde ekranında "Yapılamadı": sebep seçimi zorunlu, not ve fotoğraf isteğe bağlı; madde "yapılamadı" durumuyla puanlamaya girer (geçmedi). | M | UC-10 |
| FR-0802 | Sebep setleri hesap düzeyinde yönetilir (varsayılan: malzeme yok, ekipman arızalı, zaman yetmedi, yetkim yok, diğer); şablon bazında farklı set seçilebilir. | M | UC-10 |
| FR-0803 | "Diğer" seçilirse not zorunlu (≥ 5 karakter). | M | UC-10 |
| FR-0804 | Kritik maddede veya şablon kapatmışsa "Yapılamadı" düğmesi görünmez; madde atlanamaz. | M | UC-10 |
| FR-0805 | Yapılamadı sebepleri raporlanır (şube × sebep × dönem). | M | UC-15 |
| FR-0806 | Liste dışı sorun bildirimi: kategori, istasyon, 1–3 fotoğraf, not; şube müdürüne push. | M | UC-11 |
| FR-0807 | Şube müdürü sorunu aksiyona çevirir (atanan, vade, öncelik) veya sebep yazarak kapatır. | M | UC-11 |
| FR-0808 | Sorun bölge müdürüne yükseltilebilir; yükseltme olay logda. | M | UC-11 |
| FR-0809 | Sorun kategorileri hesap düzeyinde düzenlenebilir (varsayılan: ekipman, tedarik, hijyen, güvenlik, diğer). | M | UC-11 |

## CAP-09 · Aksiyon ve eskalasyon

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-0901 | Aksiyon alanları: başlık, açıklama, kaynak (madde cevabı / sorun / elle), şube, istasyon, atanan, vade, öncelik (düşük/orta/yüksek/kritik), durum, oluşturan, etiketler. | M | UC-12 |
| FR-0902 | Koşullu mantık, aralık dışı ölçüm, "yapılamadı" ve kaçırılan çalıştırma otomatik aksiyon oluşturur; aynı kaynak için tek aksiyon (idempotent). | M | UC-08, UC-10, UC-13 |
| FR-0903 | Varsayılan atanan kural bazlı (şube müdürü → bölge müdürü); vade önceliğe göre: kritik 4 sa, yüksek 24 sa, orta 72 sa, düşük 7 gün (hesap düzeyinde düzenlenebilir). | M | UC-12 |
| FR-0904 | Durum akışı: açık → devam ediyor → kapatma bekliyor → kapalı; açık → reddedildi (sebep). Geçişler yetkiye tabi; her geçiş logda. | M | UC-12 |
| FR-0905 | Kapatırken fotoğraf ve/veya not zorunlu (aksiyon tipine göre); "onaylı kapanış" isteyen şablonlarda bölge müdürü onayı (Should). | M | UC-12 |
| FR-0906 | Aksiyon üzerinde yorum dizisi (metin, fotoğraf, @bahsetme); yorumlar bildirim üretir; sohbet değil, kayda bağlı. | M | UC-12 |
| FR-0907 | Aksiyon listeleri: bana atananlar, şubem, bölgem, gecikmişler, kritikler; sıralama vade/öncelik; toplu kapatma yok. | M | UC-12 |
| FR-0908 | Elle aksiyon oluşturma (yetkili roller). | M | UC-12 |
| FR-0909 | Onaylı kapanış akışı. | S | UC-12, UC-20 |
| FR-0910 | Aksiyon olayları (atandı, vade yaklaşıyor 2 sa, gecikti, kapatma bekliyor, kapatıldı) bildirim üretir. | M | UC-12 |
| FR-0911 | Eskalasyon tetikleri: çalıştırma "Kaçırıldı"; aksiyon vadesi geçti; kritik madde başarısız (anında). | M | UC-13 |
| FR-0912 | Merdiven yürütme: adım gecikmeleri zamanlayıcıyla; her adımda alıcıya bildirim; kanal politikası (push, kritik/eskalasyonda SMS). | M | UC-13 |
| FR-0913 | Her eskalasyon adımı olay günlüğüne ve ilgili aksiyonun yorum dizisine yazılır. | M | UC-13 |
| FR-0914 | Çalıştırma "Yapılmayacak" işaretlenince veya aksiyon kapanınca merdiven durur. | M | UC-13 |
| FR-0915 | Adımın alıcısı yoksa (rol boş, kullanıcı pasif) bir üst adıma geçilir; "alıcı yok" olayı logda ve hesap yöneticisine uyarı. | M | UC-13 |

## CAP-10 · Bildirimler

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-1001 | Push bildirimleri (FCM/APNs): liste açıldı, hatırlatma, pencere kapandı, aksiyon olayları, duyuru, eskalasyon; derin bağlantı ilgili ekrana. | M | UC-07 |
| FR-1002 | SMS yedek: OTP; kritik liste hatırlatmaları; eskalasyon adımları (plan ayarına göre); push teslim edilemediğinde kritik olaylar. | M | UC-07, UC-13 |
| FR-1003 | Rol bazlı bildirim tercihleri (hesap varsayılanı + kullanıcı kısıtlı değişiklik); kritik olaylar kapatılamaz. | M | UC-07 |
| FR-1004 | Sessiz saatler yönetici bildirimlerine uygulanır; kritik/eskalasyon hariç. | M | UC-07 |
| FR-1005 | Teslimat izi: her bildirim için kanal, alıcı, gönderim, teslim/okunma durumu, hata kodu; destek panelinde görünür. | M | UC-07 |
| FR-1006 | Cihaz token yönetimi: geçersiz token temizlenir; kullanıcı birden çok cihaza sahip olabilir. | M | UC-07 |
| FR-1007 | Bildirim servisi kanal-bağımsız arayüz sunar (kanal eklenmesi — WhatsApp v1.x — uygulama katmanını değiştirmez). | M | UC-13 |

## CAP-11 · Duyuru ve onay

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-1101 | Duyuru: başlık, zengin metin, görsel/PDF eki, yayın zamanı (hemen/tarihli), onay gerekli mi. | M | UC-14 |
| FR-1102 | Hedefleme: hesap, bölge, şube, rol, akıllı grup; hedef kitle sayısı yayın öncesi gösterilir. | M | UC-14 |
| FR-1103 | "Okudum ve anladım" onayı zaman damgalı; onay bekleyen duyuru mobilde Bugün ekranının üstünde görünür. | M | UC-14 |
| FR-1104 | 48 saat sonra onaylamayanlara otomatik hatırlatma; yönetici elle hatırlatabilir. | M | UC-14 |
| FR-1105 | Onay raporu: oran, onaylayan/onaylamayan listesi, dışa aktarım. | M | UC-14 |
| FR-1106 | İmza zorunlu duyuru: onay ancak imza alanıyla tamamlanır; imza kaydı kişi dosyasında. | S | UC-14 |

## CAP-12 · Raporlama ve dışa aktarım

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-1201 | Operasyon ızgarası: bugün (ve seçilen gün) şube × liste hücreleri; durum renkleri; bölge/şube türü filtresi; 60 sn'de bir yenilenir. | M | UC-15 |
| FR-1202 | Çalıştırma detayı: madde cevapları, kanıt küçük resimleri ve tam boy görüntü, damga bilgisi, puan, aksiyonlar, olay izi. | M | UC-15 |
| FR-1203 | Tamamlanma ve zamanındalık raporu: şube/bölge/liste/dönem; pencere içi, geç, kaçırıldı, yapılmayacak, kapalı ayrımı; trend. | M | UC-15 |
| FR-1204 | Şube sıralaması (tamamlanma, zamanındalık, puan) — yalnızca şube ve bölge düzeyinde. | M | UC-15 |
| FR-1205 | Başarısız madde analizi: en çok başarısız ilk 10 madde; şube × madde ısı haritası. | M | UC-15 |
| FR-1206 | "Yapılamadı" sebepleri dağılımı. | M | UC-15 |
| FR-1207 | Ölçüm günlüğü: ekipman/istasyon bazlı zaman serisi; aralık dışı işaretli; denetim formatında dönem çıktısı. | M | UC-15, UC-16 |
| FR-1208 | Kanıt galerisi: şube, istasyon, madde, kullanıcı, tarih filtreleri; küçük resim ızgarası; tam boy ve damga meta verisi. | M | UC-15 |
| FR-1209 | Aksiyon raporu: açık/gecikmiş sayıları, ortalama kapanış süresi, şube/öncelik kırılımı. | M | UC-15 |
| FR-1210 | Kişi düzeyi takip: yalnızca şube/bölge müdürüne; kişinin gecikmiş/eksik maddeleri ve açık aksiyonları; puan, sıralama, karşılaştırma yok; personel kendi kaydını görür. | M | UC-15 |
| FR-1211 | Yönetici mobil görünümü: bölge/şube özet ızgarası, aksiyon kapatma, kanıt görüntüleme. | M | UC-15 |
| FR-1212 | Planlı e-posta özeti: bölge müdürüne her sabah 07:00 "dün gece"; merkeze haftalık. | S | UC-15 |
| FR-1213 | Çalıştırma PDF'i: markalı; maddeler, cevaplar, kanıt küçük resimleri, imzalar, zaman damgaları; denetim izi özeti ve doğrulama kodu. | M | UC-16 |
| FR-1214 | Dönem PDF'i: şube + şablon + tarih aralığı; ölçüm günlüğü formatı. | M | UC-16 |
| FR-1215 | Excel dışa aktarım: çalıştırmalar, cevaplar, aksiyonlar (ham veri, filtreli). | M | UC-16 |
| FR-1216 | Süreli paylaşım bağlantısı (7 gün, isteğe bağlı parola) — PDF için. | M | UC-16 |
| FR-1217 | Büyük çıktılar (≥ 500 çalıştırma) arka planda üretilir; hazır olunca bildirim ve indirme bağlantısı. | M | UC-16 |
| FR-1218 | PDF doğrulama kodu olay günlüğü zincirine bağlıdır; doğrulama sayfası (v1.x) koda göre kaydı gösterir. | M | UC-16, UC-17 |

## CAP-13 · Denetim izi ve uyum

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-1301 | Ekle-yalnız olay günlüğü: aktör, olay türü, nesne, önce/sonra özeti, zaman (sunucu), IP, cihaz; her kayıt önceki kaydın hash'ini içerir (zincir); silme/güncelleme yok. | M | UC-17 |
| FR-1302 | Günlük kök özeti her gün 04:00'te RFC 3161 zaman damgası servisine yazılır; damga kaydı saklanır. | M | UC-17 |
| FR-1303 | Denetim izi görüntüleyici: çalıştırma/aksiyon/kullanıcı bazında filtre; okunabilir olay metni; PDF eki. | M | UC-17 |
| FR-1304 | Zincir doğrulama aracı: seçilen aralıkta hash zinciri yeniden hesaplanır, kırılma raporlanır. | M | UC-17 |
| FR-1305 | Güvenlik: TLS 1.2+; depoda şifreleme; kanıt URL'leri imzalı ve 15 dk süreli; hız sınırlama; yönetici 2FA; OWASP MASVS-L1 / ASVS L1 kontrol listesi. | M | UC-03 |
| FR-1306 | Biyometrik veri işlenmez; kimlik OTP/PIN/şifre. | M | UC-03 |
| FR-1307 | İlk girişte aydınlatma metni (hesap yöneticisi özelleştirir; sürümlü); onay zaman damgalı; metin değişince yeniden onay. | M | UC-03, UC-18 |
| FR-1308 | Konum izni ayrı ekranda, amaç açıklamasıyla; reddedilebilir; konum yalnızca cevap anında nokta olarak alınır, iz tutulmaz. | M | UC-03, UC-08 |
| FR-1309 | Kişi bazlı veri dışa aktarma: profil, cevaplar, kanıt dosyaları (ZIP + JSON). | M | UC-18 |
| FR-1310 | Silme/maskeleme: kimlik alanları maskelenir; kişisel içerik taşıyan kanıtlar silinir; işletme kaydı anonim kalır; işlem logda. | M | UC-18 |
| FR-1311 | Saklama politikası hesap düzeyinde (varsayılan 24 ay, 6–60 ay); süresi dolan kanıt dosyaları silinir, özet log kalır; silme raporu. | M | UC-18 |
| FR-1312 | Veri işleme sözleşmesi ve aydınlatma metni şablonları ürün içinde indirilebilir (doküman). | M | UC-18 |

## CAP-14 · Yönetim paneli ve platform

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-1401 | Kurulum sihirbazı: marka → şubeler → şablon → plan → personel → yayın; kaldığı yerden devam; 1 saatte ilk liste hedefi. | M | UC-01 |
| FR-1402 | Hesap ayarları: bildirim varsayılanları, eskalasyon şablonları, sebep ve kategori setleri, tatil takvimi, saklama süresi, marka (logo, renk) — PDF ve duyurularda. | M | UC-01 |
| FR-1403 | Aktif şube sayacı ve dönem raporu (manuel faturalama için); sözleşme bilgileri. | M | UC-01 |

## CAP-15 / 16 / 17 / 18 · Should

| ID | Gereksinim | Ö | UC |
|---|---|---|---|
| FR-1501 | Şube türüne göre madde açma/kapama (varyant). | S | UC-05 |
| FR-1502 | SOP/PDF/Word yükle → AI taslak şablon (madde, tür, kritik önerisi); yayın öncesi düzenleme zorunlu; yükleme KVKK notu. | S | UC-05 |
| FR-1601 | Vardiya devri notu: kapanış listesinin sonunda "sabahçıya not"; açılış listesinde gösterilir. | S | UC-08 |
| FR-1701 | Tamamlanmış çalıştırmaya "gözden geçirildi" işareti ve not (bölge müdürü/kalite). | S | UC-20 |
| FR-1702 | İkinci imza alanı (kalite). | S | UC-20 |
| FR-1703 | Duyuru → şablon sürümü bağlantısı; onaylamayan kullanıcıya liste açılmaz seçeneği. | S | UC-14 |
| FR-1801 | Salt okunur REST API (çalıştırmalar, cevaplar, aksiyonlar, ölçümler) — hesap belirteciyle. | S | UC-15 |
| FR-1802 | Webhook'lar: liste kaçırıldı, kritik madde başarısız, aksiyon gecikti. | S | UC-13 |
| FR-1803 | Arayüz metinleri kaynak dosyada (i18n); MVP yalnızca Türkçe. | S | — |

## CAP-19 · Could (v1.x)

FR-1901 SSO/dizin senkronu · FR-1902 formül alanı, kaydırıcı, tekrarlanan bölüm · FR-1903 özel aksiyon tipleri, tekrarlı aksiyon · FR-1904 özel pano oluşturucu · FR-1905 PDKS/POS/İK bağlayıcıları.
