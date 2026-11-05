# Fonksiyonel gereksinimler

Kimlik: `FR-CCNN` (CC = yetenek numarası, NN = sıra). Sürüm: **v1** ilk sürüm (ADR-0008, 13 Eylül 2026) · **v1.1** pilot sonrası · **v2** daha sonra; eski M/S/C bayrakları sürüm etiketine dönüştürüldü, ID'ler korundu. Her satır en az bir use case'e bağlıdır; kabul kriterleri 06-test/02'de TC olarak açılır. "Sistem" = Talimatname (mobil + web + backend).

## CAP-01 · Hesap ve organizasyon

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-0101 | Sistem, her zinciri ayrı bir hesap (kiracı) olarak tutar; bir hesabın verisi başka hesaptan hiçbir uç noktada okunamaz. | v1 | UC-01 |
| FR-0102 | Sistem dört seviyeli hiyerarşi tutar: Marka › Bölge › Şube › İstasyon; bölge isteğe bağlıdır (şube doğrudan markaya bağlanabilir). | v1 | UC-01 |
| FR-0103 | Şube kaydı en az şunları taşır: kod (hesap içinde benzersiz), ad, adres, konum (enlem/boylam), saat dilimi, haftalık çalışma saatleri, kapalı gün takvimi, şube türü (etiket). | v1 | UC-01 |
| FR-0104 | İstasyon kaydı şubeye bağlıdır (mutfak, bar, kasa, tuvalet, depo…); madde ve kanıt istasyona bağlanabilir; istasyon QR kodu üretilebilir. | v1 | UC-01 |
| FR-0105 | Sistem, bölge/şube/istasyon/personel için Excel şablonu sunar ve toplu yükler; şablon sürümü dosyada yazılıdır. | v1 | UC-01 |
| FR-0106 | Toplu yüklemede satır bazlı doğrulama yapılır (zorunlu alan, benzersiz kod, geçerli saat dilimi, telefon formatı); %20'den fazla satır hatalıysa yükleme reddedilir; hatalı satırlar indirilebilir rapor olarak döner. | v1 | UC-01 |
| FR-0107 | Yönetici personel ekler/düzenler: ad, telefon, şube(ler), istasyon(lar), rol, dil tercihi (i18n hazırlığı). | v1 | UC-02 |
| FR-0108 | Yeni personel için davet SMS'i (uygulama bağlantısı + tek kullanımlık kod) gönderilir; teslim durumu panelde görünür; yeniden gönderilebilir. | v1 | UC-02 |
| FR-0109 | Kullanıcı pasifleştirilebilir: giriş kapanır, gelecekteki atamaları kaldırılır, geçmiş cevap/kanıt/loglar değişmeden kalır. | v1 | UC-02 |
| FR-0110 | Pasif kullanıcının kimlik alanları (ad, telefon, avatar) maskelenebilir ("Eski personel #id"); işletme kayıtları anonim kalır. | v1 | UC-02, UC-18 |

## CAP-02 · Kimlik ve yetki

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-0201 | Saha kullanıcıları telefon numarası + 6 haneli SMS OTP ile giriş yapar; e-posta zorunlu değildir. | v1 | UC-03 |
| FR-0202 | Yönetici kullanıcılar e-posta + şifre ile giriş yapar (şifre politikası: ≥ 12 karakter, sızmış parola kontrolü). TOTP 2FA v1.1. | v1 | UC-03 |
| FR-0203 | Mobil oturum 30 gün yenilenen belirteçle açık kalır; web oturumu 12 saat; cihaz/oturum listesi ve uzaktan sonlandırma. | v1 | UC-03 |
| FR-0204 | OTP: 60 sn'de bir yeniden gönderim; 3 hatalı denemede 15 dk blok; OTP 5 dk geçerli. | v1 | UC-03 |
| FR-0205 | Roller (v1): Yönetici (merkez), Bölge müdürü, Şube müdürü, Personel. Yetki = rol × kapsam (hesap/bölge/şube); matris 06-kvkk-ve-guvenlik.md'de; her uç nokta sunucu tarafında kapsam denetler. Gözlemci rolü v1.1. | v1 | UC-02 |
| FR-0206 | Akıllı gruplar: rol, bölge, şube, istasyon ve şube türü kurallarıyla dinamik üyelik; atama ve duyuru hedeflemesinde kullanılır; üyelik her değerlendirmede yeniden hesaplanır. | v1.1 | UC-02, UC-06, UC-14 |
| FR-0207 | Şube cihazı (kiosk) kaydı: panelden üretilen QR'ı tablet okutur; cihaz şubeye bağlanır; cihaz adı, model, son görülme kaydedilir; panelden kaldırılabilir. | v1 | UC-02, UC-04 |
| FR-0208 | Kiosk modunda personel 4 haneli PIN ile geçiş yapar; PIN ilk girişte kullanıcı tarafından belirlenir; şube müdürü sıfırlayabilir (olay logda). | v1 | UC-04 |
| FR-0209 | Kiosk 2 dk hareketsizlikte kilitlenir; tamamlanmamış madde cevapları yerelde korunur ve aynı kullanıcı geri dönünce devam eder. | v1 | UC-04 |
| FR-0210 | 5 hatalı PIN → 1 dk blok; art arda 3 blok → şube müdürüne bildirim. | v1 | UC-04 |
| FR-0211 | Şube müdürü, şubesindeki personele kioskta başlangıç PIN'i atayabilir (telefonu olmayan personel için); personel ilk kullanımda değiştirebilir; işlem logda. (E-1) | v1 | UC-04 |

## CAP-03 · Şablon tasarımı

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-0301 | Şablonlar sürümlüdür: taslak → yayında → arşiv; yayındaki sürüm değiştirilemez, düzenleme yeni taslak sürüm açar; yayın hemen (tarihli yayın FR-0310, v1.1). | v1 | UC-05 |
| FR-0302 | Şablon bölümlerden, bölümler maddelerden oluşur; sürükle-bırak sıralama; madde kopyalama. | v1 | UC-05 |
| FR-0303 | Madde türleri (v1): onay; çoktan seçmeli (Evet / Hayır / Uygun değil — sabit yanıt seti); sayı + birim; sıcaklık (°C); metin; fotoğraf (1–3, varsayılan 1); talimat (metin/görsel, cevap gerektirmez). Video, imza, barkod/QR, tarih-saat v1.1. | v1 | UC-05 |
| FR-0304 | Madde ayarları (v1): zorunlu; fotoğraf zorunlu; kritik (kritik maddede 'yapılamadı' yoktur); sıcaklıkta kabul aralığı. Puan ağırlığı, ipucu, istasyon bağı v1.1. | v1 | UC-05 |
| FR-0305 | Sıcaklık maddesinde kabul aralığı (min–maks) tanımlanır; aralık dışı değer maddeyi "başarısız" yapar ve koşullu mantık tetiklenebilir. | v1 | UC-05, UC-08 |
| FR-0306 | Puan = geçen madde sayısı / puanlanan madde sayısı × 100 (bilgi amaçlı; talimat maddeleri puanlanmaz). Ağırlık ve eşik v1.1. | v1 | UC-05 |
| FR-0307 | Kritik madde başarısızsa çalıştırma puandan bağımsız "Başarısız" işaretlenir. | v1 | UC-05, UC-08 |
| FR-0308 | Şablon ayarları (v1): yalnızca kamera (galeri kapalı, varsayılan açık); başarısız cevapta kanıt iste (varsayılan açık). Tolerans planda; sebep seti sabit. | v1 | UC-05 |
| FR-0309 | Editörde mobil önizleme (gerçek madde bileşenleriyle). | v1 | UC-05 |
| FR-0310 | Yayın: hemen veya tarihli; yayınla birlikte hangi planların etkileneceği listelenir. | v1.1 | UC-05 |
| FR-0311 | Kütüphane (v1): 9 Türkçe yeme-içme şablonu (kapanış, açılış, saatlik tuvalet/hijyen, soğuk zincir, haftalık derin temizlik, yağ değişimi, kasa devri, teslimat kabul, bölge müdürü şube denetimi); kopyala-düzenle; kütüphane merkezî güncellenir, kopyalar bağımsız. 30'a genişleme v1.1. | v1 | UC-05 |
| FR-0312 | Yayın doğrulaması: kritik + yapılamadı izinli çelişkisi, boş bölüm, kanıt zorunlu ama tür fotoğraf/video değil → yayın engellenir, açıklama. | v1 | UC-05 |
| FR-0313 | Kütüphane maddesi: hesaplar arası paylaşılan, sürümlü, etiketli (alan, işletme türü) madde tanımı; önerilen ayarlarla (zorunlu, fotoğraf, kritik, aralık) gelir; yalnızca içerik ekibi düzenler. (E-8) | v1.1 | UC-05 |
| FR-0314 | Şablon editöründe "kütüphaneden madde ekle": alan / tür / işletme türü filtresi ve arama; eklenen madde kaynak_madde_id ve kaynak_surum taşır; ayarları değiştirilebilir. (E-8) | v1.1 | UC-05 |
| FR-0315 | Hesap kütüphanesi: zincir kendi maddesini kaydeder, etiketler, diğer şablonlarında yeniden kullanır; yalnızca o hesapta görünür. (E-8) | v1.1 | UC-05 |
| FR-0316 | Kaynak güncelleme: kütüphane maddesi/şablonu yeni sürüm alınca ilgili hesap şablonlarında bant; fark görünümü; "uygula" yeni taslak sürüm açar, "yoksay" kaydedilir; yayındaki sürüm kendiliğinden değişmez. (E-8) | v1.1 | UC-05 |
| FR-0317 | İşletme türü paketleri: paket = sıralı şablon seti + varsayılan planlar; sihirbaz adım 2'de tür seçimi paketi önerir; tek şablonla başlama seçeneği korunur. (E-9) | v1.1 | UC-01, UC-05 |
| FR-0318 | Hesap içi set uygulama: bir şubenin şablon + plan seti başka şube(ler)e tek işlemle uygulanır; çalıştırmalar 7 gün ileri üretilir. (E-9) | v1.1 | UC-06 |

## CAP-04 · Koşullu mantık

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-0401 | Madde bazında kural: koşul = (cevap eşittir / içerir / aralık dışı / boş); bir maddede birden çok kural. | v1.1 | UC-05 |
| FR-0402 | Eylemler: ek soru göster (aynı bölümde dinamik madde), not iste, fotoğraf iste, aksiyon oluştur (atanan kuralı: şube müdürü / bölge müdürü / kişi; öncelik), bildir (rol/kişi, kanal), bölüm atla. | v1.1 | UC-05, UC-08 |
| FR-0403 | Kurallar mobilde çevrimdışı da değerlendirilir; aksiyon ve bildirim eylemleri senk anında sunucuda yürütülür (çift oluşturma yok — idempotent anahtar). | v1.1 | UC-08, UC-09 |
| FR-0404 | Editörde "kuralı dene": örnek cevapla tetiklenen eylemler listelenir. | v1.1 | UC-05 |
| FR-0405 | Sabit kural (v1): 'Hayır / Uygun değil / aralık dışı' cevapta fotoğraf + not zorunlu ('başarısız cevapta kanıt iste' şablon ayarı açıksa); kritik maddede başarısız cevap aksiyon oluşturur (şube müdürü, kritik, 4 sa) ve FR-1008 bildirimini tetikler. Çevrimdışı da uygulanır; aksiyon senkte idempotent oluşur. | v1 | UC-08 |

## CAP-05 · Planlama ve pencereler

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-0501 | Plan = şablon sürümü + kapsam + tekrar + pencere + atama + hatırlatma + eskalasyon; aktif/pasif. | v1 | UC-06 |
| FR-0502 | Kapsam: hiyerarşi ağacından çoklu seçim veya tek şube; kapsam değişince gelecekteki üretim güncellenir. Akıllı grup v1.1. | v1 | UC-06 |
| FR-0503 | Tekrar RRULE olarak saklanır; arayüz seçenekleri: günlük (birden çok saat), her N saat (başlangıç–bitiş aralığında), haftanın günleri, aylık (ayın günü veya n'inci hafta günü), bitiş tarihi. | v1 | UC-06 |
| FR-0504 | Pencere: başlangıç ve bitiş saati şube saat diliminde; süre ≤ 24 sa (tolerans dahil). | v1 | UC-06 |
| FR-0505 | Gece yarısını aşan pencere (örn. 22:00–01:30) açılış gününe ait "iş günü" olarak raporlanır. | v1 | UC-06, UC-07 |
| FR-0506 | Tolerans (geç gönderim süresi) plan bazında 0–240 dk; tolerans içinde gönderim "Geç tamamlandı". | v1 | UC-06 |
| FR-0507 | "Çalışma saatlerinden türet" seçeneği: açılış listesi açılıştan 60 dk önce–60 dk sonra; kapanış listesi kapanıştan 120 dk önce–90 dk sonra (varsayılanlar düzenlenebilir); şube saatleri değişince pencere kendiliğinden güncellenir. | v1 | UC-06 |
| FR-0508 | Atama modeli (v1): rol (o şubede o role sahip herkes), kişi veya şubedeki herkes (varsayılan); tamamlama kuralı 'biri tamamlasın' — çalıştırmayı ilk açan kullanıcı alır (çalıştırma kilidi, FR-0521). 'Herkes tamamlasın' v1.1. | v1 | UC-06, UC-19 |
| FR-0509 | Hatırlatma (v1, sabit): pencere açılışında ve bitişe 30 dk kala push. Ayarlanabilir politika v1.1. | v1 | UC-06, UC-07 |
| FR-0510 | Eskalasyon merdiveni: sıralı adımlar (alıcı rolü/kişi, gecikme süresi, kanal); varsayılan üç adım (BR-11); plan bazında özelleştirilebilir. | v1.1 | UC-06, UC-13 |
| FR-0511 | Plan kaydetmeden önce 7 günlük çalıştırma önizlemesi (şube × pencere), kapalı günler düşülmüş. | v1 | UC-06 |
| FR-0512 | Tek seferlik liste: tarih, son saat, hedef şubeler, atanan; tekrar üretmez. | v1 | UC-06 |
| FR-0513 | Zamanlayıcı her saat başı tüm aktif planlar için 7 gün ileriye çalıştırma üretir; aynı (plan, şube, pencere başlangıcı) için tek kayıt (benzersiz anahtar). | v1 | UC-07 |
| FR-0514 | Çalıştırma durumları ve geçişleri: Planlandı → Açık → Devam ediyor → Tamamlandı / Geç tamamlandı / Kaçırıldı; Planlandı/Açık → Yapılmayacak (yönetici + sebep); Tamamlandı/Geç → Başarısız (puan/kritik). Geçişler zamanlayıcı ve gönderim olaylarıyla tetiklenir; her geçiş logda. | v1 | UC-07, UC-08 |
| FR-0515 | Şube kapalı gün takviminde çalıştırma üretilmez; rapor hücresi "kapalı"; hesap düzeyi resmî tatil takvimi şubeye devralınır, şube geçersiz kılabilir. | v1 | UC-07 |
| FR-0516 | Plan değişince yalnızca "Planlandı" durumundaki gelecek çalıştırmalar yeniden hesaplanır; Açık/Devam olanlar korunur. | v1 | UC-07 |
| FR-0517 | Aynı şube + şablon + çakışan pencere için ikinci plan kaydedilemez. | v1 | UC-06 |
| FR-0518 | Vardiya bazlı tekrar: şube vardiya saatleri tanımıyla "her vardiya devrinde" penceresi. | v1.1 | UC-06 |
| FR-0519 | Şube müdürü günün çalıştırmalarında atananı değiştirebilir; "herkes tamamlasın" listelerinde kişi ekleyip çıkarabilir. **Faz B'de: `CALISTIRMA_ATAMA` tablosu uygulanınca ([karar](07-calistirma-atamasi-acigi.md)); Faz A'nın bitti tanımında değil.** | v1 | UC-19 |
| FR-0520 | Atama değişikliği yeni atanana anında bildirilir; eski atanandan kaldırılır; olay logda. **FR-0519'a bağlı, Faz B ([karar](07-calistirma-atamasi-acigi.md)).** | v1 | UC-19 |
| FR-0521 | Atanmamış çalıştırma şubedeki herkeste görünür; çalıştırmayı ilk açan kullanıcı alır (çalıştırma kilidi, 30 dk'da yenilenir), diğerleri 'X yapıyor' görür; kilit sahibi bırakırsa veya kilit dolarsa liste serbest kalır; şube müdürü kilidi kaldırabilir. (E-2) | v1 | UC-08, UC-19 |
| FR-0522 | Belge kaydı: ad, tür (yangın tüpü · baca temizliği · su deposu · periyodik elektrik kontrolü · hijyen eğitimi · portör · ruhsat · diğer), şube (ve isteğe bağlı ekipman), düzenlenme ve geçerlilik bitiş tarihi, sorumlu, dosya (PDF/fotoğraf, damgalı), not. Belge dosyası kanıtla aynı bütünlük kurallarına tabidir. (E-12) | v1 | UC-06 |
| FR-0523 | Belge uyarıları: geçerlilik bitişine 30 ve 7 gün kala sorumluya ve şube müdürüne push + sabah özeti satırı; tarih geçtiğinde aksiyon açılır (yüksek öncelik, 7 gün vade) ve şube "belge eksik" işaretlenir. (E-12) | v1 | UC-12, UC-13 |
| FR-0524 | Belge görünümü: zincir genelinde "yaklaşanlar ve süresi geçenler" listesi (şube × belge türü), dönem PDF'i; denetimde tek sayfada sunulur. (E-12) | v1 | UC-15, UC-16 |

## CAP-06 · Mobil yürütme ve kanıt

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-0601 | Bugün ekranı: kullanıcıya/şubesine atanan bugünkü çalıştırmalar; durum rengi, pencere geri sayımı, ilerleme; tek dokunuşla başlat. **Birden çok şubede çalıştırması olan kullanıcıda (bölge müdürü denetimi) liste şubeye göre gruplanır ve şube adı başlıkta görünür.** | v1 | UC-08 |
| FR-0602 | Madde cevaplama bileşenleri tür bazında (onay, seçim düğmeleri, sayısal klavye, sıcaklık, metin, kamera, video, imza alanı, barkod tarayıcı, tarih-saat). | v1 | UC-08 |
| FR-0603 | İlerleme çubuğu; uygulama kapansa da kaldığı yerden devam; cevaplar yerelde anında saklanır. | v1 | UC-08 |
| FR-0604 | Kanıt yakalama: fotoğraf zorunlu maddede kamera doğrudan açılır, çekim madde cevabını tamamlar (2 dokunuş); şablon 'yalnızca kamera' ise galeri yok; madde başına 1–3 fotoğraf (varsayılan 1). Video v1.1. | v1 | UC-08 |
| FR-0605 | Fotoğraf cihazda ~300 KB'a (uzun kenar 1600 px, JPEG %75) sıkıştırılır; ham EXIF'ten yalnızca çekim zamanı ve konum alınır. | v1 | UC-08 |
| FR-0606 | Sunucu, kanıta sunucu zamanı, (izin varsa) konum, şube mesafesi, kullanıcı, cihaz ve dosya SHA-256'sını bağlar; görünür damgalı (şube · tarih-saat · kullanıcı) kopya üretir; ham dosya saklanır. | v1 | UC-08 |
| FR-0607 | Zorunlu maddeler cevaplanmadan gönderim düğmesi pasif; gönderimde puan ve durum hesaplanır; gönderilen çalıştırma salt okunur. | v1 | UC-08 |
| FR-0608 | Gönderim sonrası düzeltme "ek kayıt" olarak eklenir (yeni cevap + not); eski cevap görünür kalır. | v1.1 | UC-08 |
| FR-0609 | Aynı çalıştırmada birden çok kullanıcı: madde bazlı kilit (60 sn), çakışmada son yazan kazanır, kanıt silinmez. | v1.1 | UC-08, UC-09 |
| FR-0610 | Pencere geri sayımı ve tolerans göstergesi; pencere kapanınca "geç" uyarısı; tolerans bitince düzenleme kilidi. | v1 | UC-08 |
| FR-0611 | Dokunma hedefleri ≥ 44 px, ikon + kısa etiket, yüksek kontrast, tek elle akış; ekran okuyucu etiketleri. | v1 | UC-08 |
| FR-0612 | İstasyon QR'ı taranınca o istasyonun açık listesi/maddeleri açılır; kanıt istasyona bağlanır. | v1.1 | UC-08 |
| FR-0613 | Açılış listesinin başında 'dün gece' bloğu: önceki iş gününün kapanış çalıştırmasında yapılamayan ve başarısız maddeler (sebep ve notla); yoksa 'dün gece sorun yok'. (E-3) | v1 | UC-08 |
| FR-0614 | Kanıt tekilliği: yüklenen dosyanın SHA-256 özeti aynı hesapta daha önce kullanılmışsa yükleme reddedilir; kullanıcıya "bu fotoğraf daha önce gönderildi, yeniden çekin" denir; deneme olay günlüğüne yazılır. Yakın kopya (algısal hash) tespiti v1.1. (E-11) | v1 | UC-08 |
| FR-0615 | Kanıt bayrakları: galeriden yükleme denemesi, konum şube dışında (> 500 m; BR-15 parametresi), konum yok, cihaz saati farkı > 10 dk (BR-13), 72 saatten geç senk (cihaz kuyruğunun ömrü, FR-0706) — cevapta saklanır; çalıştırma detayında ve çalıştırma PDF'inde görünür; panoda "şüpheli kanıt" filtresi. Bayrak suçlama değil, incelemeye çağrıdır. (E-11) | v1 | UC-08, UC-15 |

## CAP-07 · Çevrimdışı çalışma

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-0701 | Uygulama açılışta ve her 15 dk'da sonraki 48 saatin çalıştırmalarını, şablon sürümlerini, sebep setlerini önbelleğe alır. | v1 | UC-09 |
| FR-0702 | Bağlantı yokken cevaplar ve kanıtlar yerel kuyrukta (SQLite + dosya sistemi, şifreli); ekranda "bekliyor" rozeti. | v1 | UC-09 |
| FR-0703 | Bağlantı gelince arka planda senk: önce cevaplar, sonra kanıtlar; kullanıcı etkileşimi gerekmez; başarısız parçalar üstel geri çekilmeyle yeniden denenir. | v1 | UC-09 |
| FR-0704 | Sunucu, cihaz–sunucu saat farkını senk anında hesaplar; çekim zamanını düzeltir; ham cihaz zamanı ve fark logda. | v1 | UC-09 |
| FR-0705 | Çakışma kuralı: madde bazlı son yazan kazanır; kanıt dosyaları hiçbir durumda silinmez; çakışma olayı logda. | v1 | UC-09 |
| FR-0706 | Kuyruk sınırı 500 kanıt / 72 saat; sınırda yeni fotoğraf engellenir ve uyarı; 72 saatten eski kayıtlar "geç senk" bayrağıyla senklenir. | v1 | UC-09 |
| FR-0707 | Yükleme idempotent (istemci üretimli UUID); yarım kalan yükleme kaldığı yerden devam eder. | v1 | UC-09 |
| FR-0708 | Senk durumu ekranı: bekleyen kayıt/kanıt sayısı, son senk zamanı, hata ayrıntısı (destek için kopyalanabilir). | v1 | UC-09 |

## CAP-08 · Yapılamadı ve sorun bildirimi

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-0801 | Madde ekranında 'Yapılamadı': sebep seçimi zorunlu (sabit set: malzeme yok, ekipman arızalı, zaman yetmedi, yetkim yok, diğer), not ve fotoğraf isteğe bağlı; madde 'yapılamadı' durumuyla puanlamaya girer (geçmedi); şube müdürüne bildirim ve aksiyon (onay/ret akışı yoktur). | v1 | UC-10 |
| FR-0802 | Sebep setleri hesap düzeyinde yönetilir (varsayılan: malzeme yok, ekipman arızalı, zaman yetmedi, yetkim yok, diğer); şablon bazında farklı set seçilebilir. | v1.1 | UC-10 |
| FR-0803 | "Diğer" seçilirse not zorunlu (≥ 5 karakter). | v1 | UC-10 |
| FR-0804 | Kritik maddede veya şablon kapatmışsa "Yapılamadı" düğmesi görünmez; madde atlanamaz. | v1 | UC-10 |
| FR-0805 | Yapılamadı sebepleri raporlanır (şube × sebep × dönem). | v1.1 | UC-15 |
| FR-0806 | Liste dışı sorun bildirimi: sabit kategori (ekipman, tedarik, hijyen, güvenlik, diğer), 1–3 fotoğraf, not; şube müdürüne push. Güvenlik = fiziksel güvenlik; ekranda “kişiyle ilgili şikâyetler bu kanala yazılmaz” uyarısı bulunur. | v1 | UC-11 |
| FR-0807 | Şube müdürü sorunu tek dokunuşla aksiyona çevirir (atanan varsayılan kendisi, vade orta; güvenlik ve hijyen kategorilerinde yüksek) veya not yazarak kapatır. | v1 | UC-11 |
| FR-0808 | Sorun bölge müdürüne yükseltilebilir; yükseltme olay logda. | v1.1 | UC-11 |
| FR-0809 | Sorun kategorileri hesap düzeyinde düzenlenebilir (varsayılan: ekipman, tedarik, hijyen, güvenlik, diğer). | v1.1 | UC-11 |

## CAP-09 · Aksiyon ve eskalasyon

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-0901 | Aksiyon alanları (v1): başlık, kaynak (madde cevabı / sorun / elle / kaçırma), şube, atanan, vade, öncelik (orta/yüksek/kritik), durum (açık/kapalı), notlar (eklenir, silinmez), oluşturan. | v1 | UC-12 |
| FR-0902 | Koşullu mantık, aralık dışı ölçüm, "yapılamadı" ve kaçırılan çalıştırma otomatik aksiyon oluşturur; aynı kaynak için tek aksiyon (idempotent). | v1 | UC-08, UC-10, UC-13 |
| FR-0903 | Varsayılan atanan: şube müdürü (tanımlı değilse bölge müdürü). Vade sabit: kritik 4 sa, yüksek 24 sa, orta 72 sa. | v1 | UC-12 |
| FR-0904 | Durum (v1): açık → kapalı; kapatma yetkisi atanan, şube müdürü ve üstü; her geçiş logda. Devam ediyor / kapatma bekliyor / reddedildi akışı v1.1. | v1 | UC-12 |
| FR-0905 | Kapatırken not zorunlu, fotoğraf isteğe bağlı. Onaylı kapanış v1.1. | v1 | UC-12 |
| FR-0906 | Aksiyon üzerinde yorum dizisi (metin, fotoğraf, @bahsetme); yorumlar bildirim üretir; sohbet değil, kayda bağlı. | v1.1 | UC-12 |
| FR-0907 | Aksiyon listeleri: bana atananlar, şubem, bölgem, gecikmişler, kritikler; sıralama vade/öncelik; toplu kapatma yok. | v1 | UC-12 |
| FR-0908 | Elle aksiyon oluşturma (yetkili roller). | v1 | UC-12 |
| FR-0909 | Onaylı kapanış akışı. | v1.1 | UC-12, UC-20 |
| FR-0910 | Aksiyon olayları (v1): atandı (anında push), gecikti (sabah özetinde). Diğer olaylar v1.1. | v1 | UC-12 |
| FR-0911 | Eskalasyon tetikleri: çalıştırma "Kaçırıldı"; aksiyon vadesi geçti; kritik madde başarısız (anında). | v1 | UC-13 |
| FR-0912 | Eskalasyon (v1, sabit): kaçırılan liste → şube müdürüne anında push, bölge müdürüne 07:00 sabah özeti (FR-1212); kritik madde başarısız → şube ve bölge müdürüne anında push, teslim olmazsa SMS (FR-1008); gecikmiş aksiyon → sabah özeti. Gece (23:00–07:00) SMS yalnızca kritik. Merdiven editörü v1.1. | v1 | UC-13 |
| FR-0913 | Her eskalasyon adımı olay günlüğüne ve ilgili aksiyonun yorum dizisine yazılır. | v1 | UC-13 |
| FR-0914 | Çalıştırma "Yapılmayacak" işaretlenince veya aksiyon kapanınca merdiven durur. | v1 | UC-13 |
| FR-0915 | Adımın alıcısı yoksa (rol boş, kullanıcı pasif) bir üst adıma geçilir; "alıcı yok" olayı logda ve hesap yöneticisine uyarı. | v1 | UC-13 |

## CAP-10 · Bildirimler

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-1001 | Push bildirimleri (FCM/APNs): liste açıldı, hatırlatma, pencere kapandı, aksiyon olayları, duyuru, eskalasyon; derin bağlantı ilgili ekrana. | v1 | UC-07 |
| FR-1002 | SMS (v1): OTP; kritik madde bildirimi push teslim edilemediğinde. Başka SMS yok. | v1 | UC-07, UC-13 |
| FR-1003 | Rol bazlı bildirim tercihleri (hesap varsayılanı + kullanıcı kısıtlı değişiklik); kritik olaylar kapatılamaz. | v1.1 | UC-07 |
| FR-1004 | Sessiz saatler sabit (23:00–07:00): yönetici push'ları sabah özetine ertelenir; kritik anında. | v1 | UC-07 |
| FR-1005 | Teslimat izi: her bildirim için kanal, alıcı, gönderim, teslim/okunma durumu, hata kodu; destek panelinde görünür. | v1 | UC-07 |
| FR-1006 | Cihaz token yönetimi: geçersiz token temizlenir; kullanıcı birden çok cihaza sahip olabilir. | v1 | UC-07 |
| FR-1007 | Bildirim servisi kanal-bağımsız arayüz sunar (kanal eklenmesi — WhatsApp v1.x — uygulama katmanını değiştirmez). | v1 | UC-13 |
| FR-1008 | Kritik madde başarısız olduğunda şube müdürü ve bölge müdürüne anında push; 10 dk içinde teslim/okunma yoksa SMS; sessiz saatlerden muaf. (E-6) | v1 | UC-13 |

## CAP-11 · Duyuru ve onay

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-1101 | Duyuru: başlık, zengin metin, görsel/PDF eki, yayın zamanı (hemen/tarihli), onay gerekli mi. | v1.1 | UC-14 |
| FR-1102 | Hedefleme: hesap, bölge, şube, rol, akıllı grup; hedef kitle sayısı yayın öncesi gösterilir. | v1.1 | UC-14 |
| FR-1103 | "Okudum ve anladım" onayı zaman damgalı; onay bekleyen duyuru mobilde Bugün ekranının üstünde görünür. | v1.1 | UC-14 |
| FR-1104 | 48 saat sonra onaylamayanlara otomatik hatırlatma; yönetici elle hatırlatabilir. | v1.1 | UC-14 |
| FR-1105 | Onay raporu: oran, onaylayan/onaylamayan listesi, dışa aktarım. | v1.1 | UC-14 |
| FR-1106 | İmza zorunlu duyuru: onay ancak imza alanıyla tamamlanır; imza kaydı kişi dosyasında. | v1.1 | UC-14 |

## CAP-12 · Raporlama ve dışa aktarım

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-1201 | Operasyon ızgarası: şube × liste hücreleri (gün seçici); varsayılan istisna görünümü — yalnızca geç / kaçırıldı / başarısız / yapılamadı olan hücreler ve 'her şey yolunda' durumu (FR-1219); 'tümünü göster' seçeneği; 60 sn yenileme. | v1 | UC-15 |
| FR-1202 | Çalıştırma detayı: madde cevapları, kanıt küçük resimleri ve tam boy görüntü, damga bilgisi, puan, aksiyonlar, olay izi. | v1 | UC-15 |
| FR-1203 | Tamamlanma ve zamanındalık raporu: şube/bölge/liste/dönem; pencere içi, geç, kaçırıldı, yapılmayacak, kapalı ayrımı; trend. | v1.1 | UC-15 |
| FR-1204 | Şube sıralaması (tamamlanma, zamanındalık, puan) — yalnızca şube ve bölge düzeyinde. | v1.1 | UC-15 |
| FR-1205 | Başarısız madde analizi: en çok başarısız ilk 10 madde; şube × madde ısı haritası. | v1.1 | UC-15 |
| FR-1206 | "Yapılamadı" sebepleri dağılımı. | v1.1 | UC-15 |
| FR-1207 | Ölçüm günlüğü: ekipman/istasyon bazlı zaman serisi; aralık dışı işaretli; denetim formatında dönem çıktısı. | v1 | UC-15, UC-16 |
| FR-1208 | Kanıt galerisi (v1): şube ve tarih filtresi; küçük resim ızgarası; tam boy ve damga meta verisi. İstasyon/madde/kullanıcı filtreleri v1.1. | v1 | UC-15 |
| FR-1209 | Aksiyon raporu: açık/gecikmiş sayıları, ortalama kapanış süresi, şube/öncelik kırılımı. | v1.1 | UC-15 |
| FR-1210 | Kişi düzeyi takip: yalnızca şube/bölge müdürüne; kişinin gecikmiş/eksik maddeleri ve açık aksiyonları; puan, sıralama, karşılaştırma yok; personel kendi kaydını görür. | v1.1 | UC-15 |
| FR-1211 | Yönetici mobil görünümü (v1): 'Bölgem/Şubem' listesi — şube × dün gece durumu (renk + ikon), dokununca çalıştırma detayı (cevaplar, fotoğraflar). Günlük yeniden atama şube müdürü için mobilde de (FR-0519); raporlar duyarlı web'de. | v1 | UC-15 |
| FR-1212 | Sabah özeti (v1): her gün 07:00 push + e-posta — bölge müdürüne bölgesi, yöneticiye tüm hesap: dün gece kaçıran, başarısız, yapılamayan maddeler, gecikmiş aksiyonlar; derin bağlantı ızgaraya. | v1 | UC-15 |
| FR-1213 | Çalıştırma PDF'i: markalı; maddeler, cevaplar, kanıt küçük resimleri, imzalar, zaman damgaları; denetim izi özeti ve doğrulama kodu. | v1 | UC-16 |
| FR-1214 | Dönem PDF'i: şube + şablon + tarih aralığı; ölçüm günlüğü formatı. | v1 | UC-16 |
| FR-1215 | Excel dışa aktarım: çalıştırmalar, cevaplar, aksiyonlar (ham veri, filtreli). | v1.1 | UC-16 |
| FR-1216 | Süreli paylaşım bağlantısı (7 gün, isteğe bağlı parola) — PDF için. | v1.1 | UC-16 |
| FR-1217 | Büyük çıktılar (≥ 500 çalıştırma) arka planda üretilir; hazır olunca bildirim ve indirme bağlantısı. | v1 | UC-16 |
| FR-1218 | PDF doğrulama kodu olay günlüğü zincirine bağlıdır; doğrulama sayfası (v1.x) koda göre kaydı gösterir. | v1 | UC-16, UC-17 |
| FR-1219 | İstisna görünümü: FR-1201'in varsayılanı; sorunlu hücre yoksa 'Dün gece her şey yolunda' durumu; sorunlu hücreler sıralı liste olarak da sunulur (mobil Bölgem listesiyle aynı veri). (E-4) | v1 | UC-15 |
| FR-1220 | Aylık tek sayfa özet: seçilen ay için % zamanında, geç, kaçırıldı, yapılmayacak; başarısız çalıştırma ve yapılamadı sayıları; şube kırılımı; PDF. (E-7) | v1 | UC-15, UC-16 |

## CAP-13 · Denetim izi ve uyum

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-1221 | Denetim dosyası: seçilen dönem (varsayılan son 90 gün) ve şube için tek PDF — ölçüm günlüğü, dönemdeki çalıştırma özetleri (geç/başarısız/yapılamadı ayrımıyla), belge takvimi durumu, rastgele seçilmiş kanıt örnekleri ve doğrulama kodu; kapak sayfasında dönem, üretim zamanı ve üreten kullanıcı. (E-13) | v1.1 | UC-16 |
| FR-1301 | Ekle-yalnız olay günlüğü: aktör, olay türü, nesne, önce/sonra özeti, zaman (sunucu), IP, cihaz; her kayıt önceki kaydın hash'ini içerir (zincir); silme/güncelleme yok. | v1 | UC-17 |
| FR-1302 | Günlük kök özeti her gün 04:00'te RFC 3161 zaman damgası servisine yazılır; damga kaydı saklanır. | v1.1 | UC-17 |
| FR-1303 | Denetim izi görüntüleyici: çalıştırma/aksiyon/kullanıcı bazında filtre; okunabilir olay metni; PDF eki. | v1.1 | UC-17 |
| FR-1313 | Denetçi/misafir bağlantısı: FR-1221 dosyasının süreli, salt-okunur, hesap gerektirmeyen bağlantısı — varsayılan 48 saat, tek şube ve tek dönem kapsamı, yetkili tarafından iptal edilebilir; oluşturma, her açılış (IP ve zaman) ve iptal olay günlüğüne yazılır; bağlantı kişisel veri içeren alanları (personel adı) maskeler. (E-13) | v1.1 | UC-16, UC-17 |
| FR-1304 | Zincir doğrulama komutu (iç araç): seçilen aralıkta hash zinciri yeniden hesaplanır, kırılma raporlanır. Ekran v1.1. | v1 | UC-17 |
| FR-1305 | Güvenlik: TLS 1.2+; depoda şifreleme; kanıt URL'leri imzalı ve 15 dk süreli; hız sınırlama; yönetici 2FA; OWASP MASVS-L1 / ASVS L1 kontrol listesi. | v1 | UC-03 |
| FR-1306 | Biyometrik veri işlenmez; kimlik OTP/PIN/şifre. | v1 | UC-03 |
| FR-1307 | İlk girişte aydınlatma metni (hesap yöneticisi özelleştirir; sürümlü); onay zaman damgalı; metin değişince yeniden onay. | v1 | UC-03, UC-18 |
| FR-1308 | Konum izni ayrı ekranda, amaç açıklamasıyla; reddedilebilir; konum yalnızca cevap anında nokta olarak alınır, iz tutulmaz. | v1 | UC-03, UC-08 |
| FR-1309 | Kişi bazlı veri dışa aktarma: profil, cevaplar, kanıt dosyaları (ZIP + JSON). | v1.1 | UC-18 |
| FR-1310 | Silme/maskeleme (v1: destek betiği, hesap yöneticisinin talebiyle, ≤ 30 gün): kimlik alanları maskelenir; kişisel içerik taşıyan kanıtlar silinir; işletme kaydı anonim kalır; işlem logda. Ekran v1.1. | v1 | UC-18 |
| FR-1311 | Saklama sabit 24 ay: süresi dolan kanıt dosyaları arka planda silinir, cevap değerleri ve olay günlüğü özeti kalır; silme logda. Ayarlanabilir süre v1.1. | v1 | UC-18 |
| FR-1312 | Veri işleme sözleşmesi ve aydınlatma metni şablonları ürün içinde indirilebilir (doküman). | v1 | UC-18 |

## CAP-14 · Yönetim paneli ve platform

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-1401 | Kurulum sihirbazı (v1, 4 adım): marka + şubeler (Excel/elle) → kapanış şablonu (kütüphaneden, düzenlenebilir) → plan (şube saatlerinden türetilen pencere) → personel (Excel/davet); yayın. Tek planla başlanır; kaldığı yerden devam. | v1 | UC-01 |
| FR-1402 | Hesap ayarları: bildirim varsayılanları, eskalasyon şablonları, sebep ve kategori setleri, tatil takvimi, saklama süresi, marka (logo, renk) — PDF ve duyurularda. | v1.1 | UC-01 |
| FR-1403 | Aktif şube sayacı ve dönem raporu (manuel faturalama için); sözleşme bilgileri. | v1 | UC-01 |

## CAP-15 / 16 / 17 / 18 · v1.1 (FR-1803 hariç)

| ID | Gereksinim | Sürüm | UC |
|---|---|---|---|
| FR-1501 | Şube türüne göre madde açma/kapama (varyant). | v1.1 | UC-05 |
| FR-1502 | SOP/PDF/Word yükle → AI taslak şablon (madde, tür, kritik önerisi); yayın öncesi düzenleme zorunlu; yükleme KVKK notu. | v1.1 | UC-05 |
| FR-1601 | v1.1 — yerine FR-0613 (açılış listesinde dün gece özeti). | v1.1 | UC-08 |
| FR-1701 | Tamamlanmış çalıştırmaya "gözden geçirildi" işareti ve not (bölge müdürü/kalite). | v1.1 | UC-20 |
| FR-1702 | İkinci imza alanı (kalite). | v1.1 | UC-20 |
| FR-1703 | Duyuru → şablon sürümü bağlantısı; onaylamayan kullanıcıya liste açılmaz seçeneği. | v1.1 | UC-14 |
| FR-1801 | Salt okunur REST API (çalıştırmalar, cevaplar, aksiyonlar, ölçümler) — hesap belirteciyle. | v1.1 | UC-15 |
| FR-1802 | Webhook'lar: liste kaçırıldı, kritik madde başarısız, aksiyon gecikti. | v1.1 | UC-13 |
| FR-1803 | Arayüz metinleri kaynak dosyada (i18n); MVP yalnızca Türkçe. | v1 | — |

## CAP-19 · v2

FR-1901 SSO/dizin senkronu · FR-1902 formül alanı, kaydırıcı, tekrarlanan bölüm · FR-1903 özel aksiyon tipleri, tekrarlı aksiyon · FR-1904 özel pano oluşturucu · FR-1905 PDKS/POS/İK bağlayıcıları.
