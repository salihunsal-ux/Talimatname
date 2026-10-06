# v1 çekirdek kapsamı (kaynak belge)

ADR-0008 ile kabul edildi (13 Eylül 2026). Bu belge kapsamın **tek kaynağı**dır; 03-mvp-kapsam.html tarihsel referanstır. Satır kodları (O-1, Ş-2, P-3…) korunur; **v1** = ilk sürümde, **v1.1** = ilk sürümden sonra pilot geri bildirimiyle sıralanır, **v2** = daha sonra. Yeni satırlar E-kodludur.

## v1'in tek cümlesi

Merkez kapanış/açılış/hijyen/soğuk zincir listelerini kurar; personel kioskta veya telefonda, fotoğraf ve ölçümle kanıtlayarak tamamlar; sistem pencereyi izler, kaçırılanı ve kritik olanı bildirir; yönetici istisna odaklı ızgara, sabah özeti ve doğrulama kodlu PDF ile görür.

## Sabitler (v1'de ayar ekranı yok)

| Sabit | Değer |
|---|---|
| Roller | Yönetici (merkez), Bölge müdürü, Şube müdürü, Personel |
| Madde türleri | onay · çoktan seçmeli (Evet/Hayır/Uygun değil) · sayı + birim · sıcaklık (°C, kabul aralığı) · metin · fotoğraf (1–3, varsayılan 1) · talimat (cevapsız) |
| Madde ayarları | zorunlu · fotoğraf zorunlu · kritik (+ sıcaklıkta min–maks) |
| Tek kural | "Hayır / Uygun değil / aralık dışı" → fotoğraf + not zorunlu; kritik maddede → aksiyon (şube müdürü, 4 sa). Kural editörü yok |
| Puan | Geçen madde yüzdesi (bilgi). "Başarısız çalıştırma" = herhangi bir kritik madde başarısız |
| Atama | rol · kişi · şubedeki herkes (varsayılan). "Biri tamamlasın": ilk açan alır |
| Tolerans | kapanış 120 dk · saatlik 0 · haftalık 240 dk (plan bazında değiştirilebilir, ayar paneli yok) |
| Hatırlatma | pencere açılışında + bitişe 30 dk kala (push) |
| Eskalasyon (sabit) | Kaçırılan liste → şube müdürüne anında push; bölge müdürüne 07:00 sabah özeti. Kritik madde başarısız → şube müdürü + bölge müdürü anında push, teslim olmazsa SMS. Gecikmiş aksiyon → sabah özetinde. Gece SMS yalnızca kritik |
| Sessiz saat | 23:00–07:00 yönetici push'ları için (kritik hariç) |
| Aksiyon | durum: açık / kapalı · kapatırken not zorunlu, fotoğraf isteğe bağlı · notlar eklenir, silinmez |
| Sebep seti (yapılamadı) | malzeme yok · ekipman arızalı · zaman yetmedi · yetkim yok · diğer (not zorunlu) |
| Sorun kategorisi | ekipman · tedarik · hijyen · güvenlik · diğer (UC-11). Güvenlik = fiziksel güvenlik (kapı, kilit, kepenk, alarm, yangın ekipmanı); kişiyle ilgili şikâyet kanalı değildir. Güvenlik ve hijyen sorunundan açılan aksiyon **yüksek** önceliklidir (BR-10: 24 sa), diğerleri orta (72 sa) |
| Saklama | 24 ay (kanıt dosyaları); olay günlüğü kalıcı |
| Kütüphane | 8 şablon: kapanış · açılış · saatlik tuvalet/hijyen · soğuk zincir · haftalık derin temizlik · yağ değişimi · kasa devri · teslimat kabul — madde içerikleri: [07-sablon-kutuphanesi.md](07-sablon-kutuphanesi.md) (taslak, sahada doğrulanır) |

## M1 · Organizasyon, kimlik ve yetki

| Kod | Özellik | v1 içeriği | Sürüm |
|---|---|---|---|
| O-1 | Çok kiracılı hesap | Aynen | v1 |
| O-2 | Hiyerarşi | Marka › Bölge › Şube › İstasyon (istasyon isteğe bağlı) | v1 |
| O-3 | Roller | 4 rol; yetki = rol × kapsam (hesap/bölge/şube) | v1 |
| O-4 | Telefonla giriş | Personel telefon + OTP; yönetici e-posta + şifre. 2FA | v1 (2FA v1.1) |
| O-5 | Ortak cihaz (kiosk) modu | QR ile cihaz kaydı, PIN ile geçiş, 2 dk kilit | v1 |
| E-1 | Şube müdürü personele PIN atar | Telefonu olmayan personel için; personel değiştirebilir | v1 |
| O-6 | Toplu içe aktarma | Şube ve personel Excel'i, hata raporu | v1 |
| O-7 | Akıllı gruplar | — | v1.1 |
| O-8 | İşten ayrılma | Pasifleştirme v1; kimlik maskeleme destek betiğiyle | v1 |
| O-9 | SSO / dizin senkronu | — | v2 |

## M2 · Şablon tasarımı

| Kod | Özellik | v1 içeriği | Sürüm |
|---|---|---|---|
| Ş-1 | Şablon editörü | Bölüm, madde, sıralama; sürüm: taslak → yayında (hemen) → arşiv | v1 (tarihli yayın v1.1) |
| Ş-2 | Madde türleri | 6 tür + talimat (sabitler tablosu). Video, imza, barkod/QR, tarih-saat | v1 (diğerleri v1.1) |
| Ş-3 | Madde ayarları | zorunlu · fotoğraf zorunlu · kritik · sıcaklık aralığı. Ağırlık, istasyon bağı, ipucu | v1 (diğerleri v1.1) |
| Ş-4 | Koşullu mantık | Tek sabit kural | v1 sabit; editör v1.1 |
| Ş-5 | Puanlama | Yüzde; başarısız = kritik | v1 sabit; ağırlık/eşik v1.1 |
| Ş-6 | Kütüphane | 8 şablon, kopyala-düzenle; maddeler şablonun içinde | v1 (madde kütüphanesi ve paketler v1.1 — E-8/E-9, ADR-0010) |
| Ş-7 | Şube türü varyantı | — | v1.1 |
| Ş-8 | SOP/PDF'ten AI taslak | — | v1.1 |
| Ş-9 | Formül, kaydırıcı, tekrarlanan bölüm | — | v2 |
| E-8 | Madde kütüphanesi | Sürümlü, etiketli kütüphane maddeleri; editörde "kütüphaneden ekle"; hesap kütüphanesi; kaynak takibi ve güncelleme bandı (FR-0313…0316) | v1.1 (veri modeli alanları v1'de boş) |
| E-9 | İşletme türü paketleri | Kafe / hızlı servis / restoran / fırın-pastane paketleri; sihirbazda tür seçimi; hesap içi set uygulama (FR-0317, 0318) | v1.1 |
| E-10 | Marka kütüphanesi (franchise) ve başka dikey paketleri | Merkez standart setini bayilere dağıtır; perakende/eczane/spor salonu paketleri | v2 |

## M3 · Planlama

| Kod | Özellik | v1 içeriği | Sürüm |
|---|---|---|---|
| P-1 | Tekrar kuralları | Günlük (saat listesi), her N saat, haftanın günleri, aylık; RRULE | v1 |
| P-2 | Pencereler | Başlangıç/bitiş, gece yarısı aşımı, çalışma saatinden türetme, tolerans | v1 |
| P-3 | Atama | rol · kişi · şubedeki herkes; biri tamamlasın. "Herkes tamamlasın" | v1 (herkes v1.1) |
| E-2 | Atanmamış liste varsayılanı | Şubedeki herkes görür, ilk açan alır (çalıştırma kilidi), diğerleri "X yapıyor" görür | v1 |
| P-4 | Otomatik çalıştırma üretimi | 7 gün ileri, benzersiz | v1 |
| P-5 | Tatil / kapalı gün | Hesap + şube takvimi | v1 |
| P-6 | Tek seferlik liste | Aynen | v1 |
| E-12 | Belge ve periyodik bakım takvimi | Tarihli belge kaydı (yangın tüpü dolum, baca ve su deposu temizliği, periyodik elektrik kontrolü, hijyen eğitimi ve portör belgeleri, ruhsat): şube/ekipman, geçerlilik bitişi, sorumlu, belge dosyası; 30/7/0 gün uyarıları ve süresi geçende aksiyon; zincir genelinde "yaklaşan ve geçmiş" listesi; dönem PDF'i | v1 |
| P-7 | Hatırlatma politikası | Sabit iki hatırlatma | v1 sabit; ayar v1.1 |
| P-8 | Vardiya bazlı tekrar | — | v1.1 |

## M4 · Yürütme (mobil)

| Kod | Özellik | v1 içeriği | Sürüm |
|---|---|---|---|
| Y-1 | Bugün ekranı | Aynen; duyuru şeridi yok | v1 |
| Y-2 | Madde tamamlama | Tek kullanıcı (ilk açan); kaldığı yerden devam. Çoklu kullanıcı/madde kilidi | v1 (çoklu v1.1) |
| Y-3 | Kanıt yakalama | Kamera doğrudan açılır, 1–3 fotoğraf (varsayılan 1), sıkıştırma, damga, hash. Video | v1 (video v1.1) |
| Y-4 | Yapılamadı akışı | Sabit sebep seti + not; kritik maddede yok | v1 |
| Y-5 | Çevrimdışı öncelikli | Aynen (72 sa, 500 kanıt, idempotent senk) | v1 |
| Y-6 | Gönderim ve kilit | Gönderilen değişmez. Ek kayıt | v1 (ek kayıt v1.1) |
| Y-7 | Sorun bildir | Fotoğraf + not + sabit kategori → şube müdürü | v1 |
| Y-8 | Bildirimler | Push; SMS yalnızca OTP + kritik | v1 |
| Y-9 | Düşük okuryazarlık tasarımı | Aynen | v1 |
| Y-10 | Vardiya devri notu | Yerine E-3 | — |
| E-3 | Açılışta dün gece özeti | Açılış listesinin başında "dün gece: yapılamayan / başarısız maddeler" | v1 |
| Y-11 | QR ile istasyondan başlatma | — | v1.1 |
| Y-12 | Yönetici mobil görünümü | "Bölgem/Şubem" listesi: şube × dün gece durumu → çalıştırma detayı (fotoğraflar). Atama ve raporlar duyarlı web | v1 (küçültüldü) |

## M5 · Aksiyon ve eskalasyon

| Kod | Özellik | v1 içeriği | Sürüm |
|---|---|---|---|
| A-1 | Aksiyon kaydı | Başlık, kaynak, şube, atanan, vade, öncelik, durum (açık/kapalı), notlar | v1 (durum makinesi v1.1) |
| A-2 | Otomatik oluşturma | Kritik madde, yapılamadı, kaçırılan liste; sabit vadeler | v1 |
| A-3 | Kapanış kanıtı | Not zorunlu, fotoğraf isteğe bağlı. Onaylı kapanış | v1 (onay v1.1) |
| A-4 | Eskalasyon | Sabit kural (sabitler tablosu). Merdiven editörü | v1 sabit; editör v1.1 |
| E-5 | Sabah özeti | 07:00 push + e-posta: dün gece kaçıran, başarısız, yapılamayan, gecikmiş aksiyon; bölge müdürü ve yönetici | v1 |
| E-6 | Kritik anında bildirim | Kritik madde başarısız → şube + bölge müdürü push; teslim olmazsa SMS | v1 |
| A-5 | Yorum dizisi | Tek "not ekle" (eklenir, silinmez). Yorum dizisi, @bahsetme | v1 not; dizi v1.1 |
| A-6 | Listeler ve filtreler | Bana / şubem / bölgem / gecikmiş | v1 |
| A-7 | Özel aksiyon tipleri, tekrarlı aksiyon | — | v2 |

## M6 · Duyuru ve onay

| Kod | Özellik | Sürüm |
|---|---|---|
| D-1…D-4 | Hedefli duyuru, okundu onayı, imzalı belge, duyuru→şablon bağı | v1.1 |

## M7 · Raporlama ve analitik

| Kod | Özellik | v1 içeriği | Sürüm |
|---|---|---|---|
| R-1 | Operasyon panosu | Şube × liste ızgarası; **istisna odaklı varsayılan** (yalnızca sorunlular; "her şey yolunda" durumu); tümünü göster seçeneği | v1 |
| E-4 | İstisna görünümü | R-1'in parçası | v1 |
| R-2 | Tamamlanma ve zamanındalık | Aylık tek sayfa özet (E-7) ile karşılanır; ayrıntılı rapor | v1.1 |
| E-7 | Aylık tek sayfa özet | % zamanında, kaçırma, başarısız, yapılamadı sayıları; şube kırılımı; PDF | v1 |
| R-3 | Başarısız madde analizi | — | v1.1 |
| R-4 | Sıcaklık / ölçüm günlüğü | Ekipman zaman serisi, aralık dışı işaretli, dönem PDF'i | v1 |
| R-5 | Kanıt galerisi | Şube + tarih filtresi, küçük resim, tam boy | v1 (istasyon/madde filtreleri v1.1) |
| R-6 | PDF ve Excel | Çalıştırma PDF'i + dönem PDF'i (doğrulama kodlu). Excel, paylaşım bağlantısı | v1 (Excel/paylaşım v1.1) |
| R-7 | Aksiyon raporu | — | v1.1 |
| R-8 | Planlı e-posta raporu | Sabah özeti (E-5) | v1 |
| R-9 | Kişi düzeyi takip | — | v1.1 |
| R-10 | Özel pano | — | v2 |

## M8 · Denetim izi, uyum ve güvenlik

| Kod | Özellik | v1 içeriği | Sürüm |
|---|---|---|---|
| U-1 | Değiştirilemez olay günlüğü | Ekle-yalnız, hash zinciri (arka plan). Dış zaman damgası (RFC 3161) | v1 (TSA v1.1) |
| U-2 | Denetim izi görüntüleyici | PDF'te olay özeti; ekran | v1.1 |
| E-13 | **Denetim dosyası ve denetçi bağlantısı** | Seçilen dönem için tek PDF: ölçüm günlüğü + ilgili çalıştırmalar + belge takvimi + kanıt örnekleri + doğrulama kodu. Denetçiye ya da franchise merkezine hesap açmadan **süreli, salt-okunur** bağlantı (varsayılan 48 sa, iptal edilebilir, her açılış logda). Büyüme listesinde A21; U-1'in doğrulama kodu ve E-12 belge takvimi üstüne kurulur | **v1.1 adayı** (K1 sinyaline bağlı) |
| U-3 | KVKK akışı | Aydınlatma metni + konum izni açıklaması v1; dışa aktarma/silme destek betiğiyle; ekran | v1 (ekran v1.1) |
| U-4 | Saklama politikası | Sabit 24 ay, arka plan silme | v1 |
| E-11 | Kanıt bütünlüğü bayrakları | Aynı dosyanın (SHA-256) ikinci kez gönderilmesi engellenir ve işaretlenir; galeri / konum şube dışında / cihaz saati farkı / toplu geç senk bayrakları çalıştırma detayında ve PDF'te görünür; şüpheli kanıt filtresi | v1 (yakın kopya tespiti v1.1) |
| U-5 | Güvenlik | TLS, şifreleme, imzalı URL, rol × kapsam, hız sınırı, şifre politikası. 2FA | v1 (2FA v1.1) |
| U-6 | Biyometri yok | Aynen | v1 |

## M9 · Yönetim paneli (web) ve platform

| Kod | Özellik | v1 içeriği | Sürüm |
|---|---|---|---|
| W-1 | Kurulum sihirbazı | 4 adım: marka+şubeler → kapanış şablonu → plan (saatler) → personel; tek plan | v1 |
| W-2 | Şube ve personel yönetimi | Aynen (davet SMS'i, cihaz kaydı) | v1 |
| W-3 | Bildirim ve eskalasyon ayarları | Sabit | v1.1 |
| W-4 | Faturalama | Aktif şube sayacı | v1 |
| W-5 | Dışa aktarım API'si ve webhook | — | v1.1 |
| W-6 | Entegrasyon iskeleti | — | v2 |
| W-7 | Çok dillilik | Metinler kaynak dosyada (i18n hazır), yalnızca Türkçe | v1 |

## Özet

| | v1 | v1.1 | v2 |
|---|---|---|---|
| Satır | 43 (34 mevcut + 9 E) | 28 (E-13 dahil, aday) | 6 |

v1.1 sıralaması pilot geri bildirimiyle yapılır; aday sıra: duyuru/onay → koşul editörü → herkes tamamlasın → aksiyon yorumları/onayı → raporlar → denetim izi ekranı + TSA → KVKK ekranı → 2FA → ayarlar paneli → Excel/paylaşım → video/imza/barkod → QR → gruplar → varyant → AI taslak.
