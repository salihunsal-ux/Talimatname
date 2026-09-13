# KVKK ve güvenlik

Talimatname, müşteri (zincir) adına **veri işleyen**dir; zincir **veri sorumlusu**dur. Ürün, veri sorumlusunun yükümlülüklerini (aydınlatma, saklama, silme, erişim) yerine getirebilmesi için araç ve şablon sağlar. Bu belge veri envanteri, rol matrisi, saklama ve güvenlik kontrollerini tanımlar; hukuki metinler (veri işleme sözleşmesi, aydınlatma şablonu) ürün içinde indirilebilir belgeler olarak ayrıca hazırlanır (FR-1312) ve avukat incelemesinden geçer.

## Kişisel veri envanteri

| Veri | Kimin | Amaç | Hukuki dayanak (zincir için) | Saklama | Not |
|---|---|---|---|---|---|
| Ad, telefon, rol, şube | Personel, yöneticiler | Hesap, atama, bildirim | Sözleşmenin ifası / meşru menfaat | Çalışma süresi + saklama süresi (maskeleme) | E-posta yalnızca yöneticide |
| PIN/şifre/TOTP (hash) | Tümü | Kimlik doğrulama | Meşru menfaat | Hesap aktifken | Düz metin asla saklanmaz |
| Cevaplar, zaman damgaları | Personel | İşin kanıtı, denetim | Meşru menfaat, yasal yükümlülük (gıda güvenliği kayıtları) | Saklama süresi (varsayılan 24 ay); değerler anonim kalır | Kişi skoru üretilmez (BR-20) |
| Kanıt fotoğraf/video | Personel (çeken) | İşin kanıtı | Meşru menfaat | Saklama süresi; sonra silinir | İş fotoğraflanır, kişi değil; yüz içeren kanıt için personel bilgilendirilir |
| Konum (cevap anı, tek nokta) | Personel | Kanıtın yerinin doğrulanması | Meşru menfaat; ayrı bilgilendirme | Cevapla birlikte | İzin reddedilebilir; sürekli takip yok (BR-15) |
| Cihaz kimliği, IP | Tümü | Güvenlik, denetim izi | Meşru menfaat | Olay günlüğü süresi | |
| Aydınlatma onayı | Tümü | Kanıt | Yasal yükümlülük | Kalıcı (log) | Sürümlü metin |
| Duyuru onayı / imza | Personel | Prosedür bildirimi kanıtı | Meşru menfaat | Saklama süresi | |
| Biyometrik veri | — | — | — | — | **İşlenmez** (Kurul 2026/921) |

## Rol × yetki matrisi (uygulama uç noktalarında zorunlu)

> v1'de Hesap yön., Op. müdürü ve Kalite sütunları tek **Yönetici** rolüdür (üçünün birleşimi); Gözlemci v1.1 (ADR-0008). Duyuru, denetim izi ekranı ve KVKK talep ekranı satırları v1.1'de devreye girer; v1'de KVKK talepleri destek betiğiyle, Yönetici talebiyle işlenir.

| Kaynak / eylem | Hesap yön. | Op. müdürü | Kalite | Bölge müd. | Şube müd. | Personel | Gözlemci |
|---|---|---|---|---|---|---|---|
| Hesap ayarları, saklama, KVKK talepleri | RW | R | R | – | – | – | – |
| Şube/istasyon/cihaz | RW | RW (meta) | R | R (bölge) | R (şube), cihaz RW | – | R (şube) |
| Kullanıcı ve roller | RW | R | R | R (bölge) | Personel RW (şube) | Kendi profili | – |
| Şablon ve kütüphane | R | RW | RW | R | R | – | – |
| Plan | R | RW | RW | RW (bölge) | R | – | – |
| Günlük atama | – | RW | – | RW (bölge) | RW (şube) | – | – |
| Çalıştırma cevaplama | – | – | – | – | RW (şube) | RW (atanan) | – |
| Yapılmayacak | – | RW | – | RW (bölge) | RW (şube) | – | – |
| Sorun bildir | – | – | – | – | RW | RW | – |
| Aksiyon (oluştur/ata/geçiş) | – | RW | RW | RW (bölge) | RW (şube) | Kapanış kanıtı | – |
| Duyuru | – | RW | RW | RW (bölge) | RW (şube) | Onay | R |
| Izgara ve raporlar | R | R | R | R (bölge) | R (şube) | Kendi kaydı | R (şube) |
| Kanıt galerisi (tam boy) | R | R | R | R (bölge) | R (şube) | Kendi kanıtı | R (şube) |
| Kişi düzeyi takip | – | – | – | R (bölge) | R (şube) | Kendi | – |
| Denetim izi, doğrulama | R | R | R | – | – | – | – |
| Dışa aktarım (PDF/Excel) | R | RW | RW | RW (bölge) | RW (şube) | – | R (şube, PDF) |

Kapsam: R/RW yetkisi her zaman rol atamasının kapsamıyla (hesap/bölge/şube) sınırlıdır; sunucu, istenen nesnenin kapsamda olduğunu doğrular (yatay yetki ihlali testi zorunlu — TC-010, TC-011).

## Aydınlatma ve izin akışı (ürün içi)

1. İlk girişte (OTP sonrası) aydınlatma metni: veri sorumlusu (zincir) adı, işlenen veriler, amaçlar, aktarım (Talimatname veri işleyen; barındırma TR), haklar, başvuru kanalı. "Okudum" onayı zaman damgalı; metin sürümü değişince yeniden gösterilir.
2. Konum izni ayrı ekranda: "Konum yalnızca bir maddeyi tamamladığınız anda, kanıtın şubede çekildiğini doğrulamak için alınır; sürekli takip yapılmaz." Reddedilirse kanıt "konum yok" bayrağıyla kaydedilir; kullanım engellenmez.
3. Kamera izni: sistem izni; şablon "yalnızca kamera" ise gerekçe gösterilir.
4. Kiosk modunda aydınlatma metni her kullanıcının ilk PIN geçişinde gösterilir.
5. Hesap yöneticisi aydınlatma metnini düzenleyebilir (şablon + zincir bilgileri); değişiklik sürümlenir.

## Kişi hakları ve talepler

- Erişim/dışa aktarma: `KVKK_TALEP` → ZIP (profil JSON, cevaplar CSV, kanıt dosyaları) ≤ 30 gün; hesap yöneticisi onaylar.
- Silme: kimlik alanları maskelenir; kişisel içerik taşıyan kanıt dosyaları silinir; iş kaydı (cevap değeri, zaman, şube) anonim kalır — gıda güvenliği kayıtlarının bütünlüğü için gerekçe aydınlatma metninde.
- İtiraz (konum, fotoğraf): izin reddi ürün içinde; itiraz kaydı hesap yöneticisine.

## Güvenlik kontrolleri

| Alan | Kontrol |
|---|---|
| Aktarım | TLS 1.2+; HSTS; sertifika sabitleme mobilde (isteğe bağlı, sürüm 2) |
| Depolama | Veritabanı ve nesne depo şifreli (sağlayıcı KMS); yedekler şifreli; mobil yerel kuyruk şifreli (cihaz anahtar zinciri) |
| Kimlik | OTP (5 dk, 3 deneme/15 dk blok); yönetici şifre politikası (≥ 12 karakter, sızmış parola kontrolü); TOTP 2FA; oturum ve cihaz listesi, uzaktan sonlandırma |
| Yetki | Rol × kapsam her uç noktada; satır düzeyi güvenlik (hesap_id); yönetim işlemleri olay günlüğünde |
| Kanıt erişimi | İmzalı, 15 dk süreli URL'ler; doğrudan nesne yolu yok; paylaşım bağlantıları süreli ve iptal edilebilir |
| Uygulama | OWASP ASVS L1 (API) ve MASVS-L1 (mobil) kontrol listesi; girdi doğrulama; hız sınırlama; CSRF (web); güvenli başlıklar |
| Tedarik zinciri | Bağımlılık taraması CI'da; imzalı derlemeler; gizli anahtarlar yönetici kasasında, depoda yok |
| İzleme | Başarısız giriş, yetki reddi, olağandışı dışa aktarım uyarıları; olay günlüğü zincir doğrulaması günlük |
| Test | GA öncesi dış sızma testi; yatay/dikey yetki testleri kabul setinde |
| Olay müdahale | Veri ihlali prosedürü: 72 saat içinde Kurul ve veri sorumlusuna bildirim akışı; iletişim şablonu |
| Destek erişimi | Destek modu: kanıt içeriği maskeli, yalnızca teknik izler; müşteri onayıyla süreli tam erişim, logda |

## Barındırma ve alt işleyenler

- Birincil bölge: Türkiye (ADR-0003). Alt işleyenler listesi (bulut, SMS, push, e-posta, zaman damgası) veri işleme sözleşmesi ekinde; değişiklikte 30 gün önceden bildirim.
- Push bildirimleri (FCM/APNs) yurt dışı sunucudan geçer: içerik kişisel veri taşımaz (yalnızca "Kapanış listesi açıldı" ve derin bağlantı kimliği).

## Uyum kontrol listesi (GA öncesi)

- [ ] Aydınlatma metni ve veri işleme sözleşmesi avukat onaylı
- [ ] VERBİS kaydı (Talimatname şirketi için, eşik değerlendirmesi)
- [ ] Saklama politikası uygulanıyor ve test edildi (TC-105)
- [ ] Silme/maskeleme akışı test edildi (TC-104)
- [ ] Biyometri yok — kod incelemesi
- [ ] Sızma testi raporu ve kapatılan bulgular
- [ ] Alt işleyen listesi ve bölgeler belgelendi
- [ ] Olay müdahale prosedürü ve iletişim şablonları hazır
