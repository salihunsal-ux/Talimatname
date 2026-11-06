# Oturum süresi: yenileme belirteci yok

- Tarih: 2026-11-06 · Durum: **karar bekliyor**
- İlgili: FR-0203, FR-0205, TC-128, [API taslağı](05-api-taslagi.md),
  [teknik mimari](../07-gelistirme/01-teknik-mimari.md), ADR-0013

## Durum

Bugün oturum **30 dakika** yaşıyor (`settings.access_token_minutes`,
varsayılan 30; demo da varsayılanı kullanıyor). Süre dolunca belirteç
geçersiz oluyor ve kullanıcı yeniden giriş yapmak zorunda.

**Yenileme belirteci yok.** Ne uç nokta var, ne saklama, ne iptal.
Panel 6 Kasım'da şunu öğrendi: süre dolunca uygulama belirteci bırakıp
giriş ekranına dönüyor ve sebebini yazıyor. Bu, sorunu görünür kılıyor
ama çözmüyor.

## Açık

Üç belge bundan başka bir şey söylüyor:

| Kaynak | Ne diyor |
|---|---|
| **FR-0203** (v1) | "Mobil oturum 30 gün yenilenen belirteçle açık kalır; **web oturumu 12 saat**; cihaz/oturum listesi ve uzaktan sonlandırma." |
| [API taslağı](05-api-taslagi.md) | "Erişim 15 dk, yenileme belirteci mobilde 30 gün / web 12 sa." |
| [Teknik mimari](../07-gelistirme/01-teknik-mimari.md) | "Belirteç: JWT (RS256), kısa ömür; **yenileme belirteci DB'de iptal edilebilir**." |
| **TC-128** | "…oturum süresi dolunca belirteç yenilenir." |

Yani tasarım kararını vermiş: kısa ömürlü erişim belirteci + iptal
edilebilir yenileme belirteci. Uygulanan ise tek başına 30 dakikalık
bir erişim belirteci. Erişim süresi de taslaktakiyle tutmuyor (15 dk
yazıyor, 30 dk uygulanmış) ama asıl eksik yenileme belirteci.

Buna bağlı olarak **uygulanamayan** iki şey daha var:

- FR-0203'ün ikinci yarısı: cihaz/oturum listesi ve uzaktan sonlandırma.
  Bunun için sunucuda oturum kaydı gerekiyor; JWT durumsuz olduğu için
  bugün bir oturumu iptal etmenin yolu yok.
- TC-128 bugünkü kodla geçemez.

## Neden bugün acıtıyor, yarın daha çok acıtacak

**Panelde:** kurulum sihirbazını doldururken ya da uzun bir şablonu
düzenlerken oturum ortadan kalkabiliyor. Taslak kaydedilmediyse
kayboluyor.

**Mobilde:** şube personeli listeyi vardiya boyunca açık tutuyor.
Otuz dakikada bir PIN/OTP istemek sahada kullanılamaz. Faz B'nin
çalışması buna bağlı — ADR-0013 md.4 mobil başlamadan önce üç API
sözleşmesinin yazılı olmasını şart koşmuştu (idempotent cevap, kanıt
yükleme, senk uç noktaları); **oturum yenileme o listede yoktu ve
atlandı**. Dördüncü sözleşme olmalıydı.

## Seçenekler

| | Kurgu | Artısı | Eksisi |
|---|---|---|---|
| **A** | FR-0203'ü uygula: kısa erişim belirteci + DB'de saklanan, iptal edilebilir yenileme belirteci (web 12 sa, mobil 30 gün) | Gereksinim karşılanır; oturum listesi ve uzaktan sonlandırma mümkün olur; mobil sahada çalışabilir | Tablo + iki uç nokta + istemcide sessiz yenileme; iptal kuralları ve hız sınırı düşünülmeli |
| **B** | Yalnızca `ACCESS_TOKEN_MINUTES`'i büyüt (örn. 480) | Tek satır | **Güvenlik gerilemesi**: `localStorage`'daki uzun ömürlü belirteç iptal edilemiyor; çalınan belirteç sekiz saat geçerli kalır. FR-0203'ün sonlandırma yarısı yine yok |
| **C** | 30 dakikada kal, FR-0203'ü v1.1'e at | Maliyet yok | Mobil Faz B'de kullanılamaz; TC-128 düşer; kâğıt üstünde v1 duran bir gereksinim yapılmamış olur |

## Tavsiye

**A, Faz B başlamadan.** Gerekçe B'nin eksisi: tek satırlık çözüm,
ürünün "kim ne zaman yaptı" iddiasını taşıyan bir sistemde iptal
edilemeyen uzun ömürlü belirteç bırakıyor. Ve mobil geliştirici
geldiğinde oturum yenileme hazır olmazsa, istemci onsuz yazılır;
ADR-0013'ün "API panelin çevrimiçi istek-cevap şekline oturur ve Faz B
onu söker" uyarısı burada da geçerli.

Ara önlem gerekirse: panelde `ACCESS_TOKEN_MINUTES` değerini
yükseltmek yerine, kaybolan işi azaltmak (taslağı yerelde tutmak) daha
ucuz ve geri alınabilir.

## Yapılacaklar (A seçilirse)

1. Yenileme belirteci tablosu: kullanıcı, cihaz, verilme ve son
   kullanma zamanı, iptal durumu.
2. `POST /auth/refresh` ve `POST /auth/logout` (bu oturumu iptal et).
3. İstemcide sessiz yenileme: 401/403 öncesi, erişim belirteci dolmadan.
4. FR-0203'ün ikinci yarısı: oturum listesi + uzaktan sonlandırma.
5. Erişim belirteci süresi taslakla hizalanır (15 dk) ya da taslak
   güncellenir — ikisi bir arada tutmalı.
6. `web/src/api/oturum.ts` içindeki "ST-044'te ele alınacak" notu
   düzeltilir: ST-044 bildirim servisi, bu işle ilgisi yok.
