# Prototipler

İki tıklanabilir prototip (veri kaydetmez) ve bir **çalışan saha demosu** (veri saklar). Hepsi tek dosya, bağımlılık yok.

## 0. Saha demosu — çalışan sürüm (4 Ekim 2026)

`saha-demosu.html` → https://claude.ai/artifact/WGKqPtVDturkaRaoLRtiRy

Tıklanabilir prototiplerden farkı: **kayıt tutar**. Pencere ve tolerans gerçek saatle işler, madde cevapları ve cihaz kamerasıyla çekilen kanıt saklanır, kritik madde ve yapılamadı aksiyon açar, gönderim kaydı kilitler, merkez panosu aynı kaydı görür ve doğrulama kodlu raporu yazdırır.

**İki mod.** Artifact veri tabanına yalnızca yazma yetkisi olan hesaplar (sahibi ve e-postayla davet edilen düzenleyiciler; kurumsal planda şirket üyeleri) yazabilir — onlarda *paylaşımlı mod* çalışır: tablette doldurulan liste merkez panosunda canlı görünür. Diğer herkeste *yerel mod*: akış birebir aynıdır, veriler yalnızca o cihazda kalır. Mod üst çubukta yazar.

**Demoda olmayan (üründe var):** push ve SMS, gerçek kimlik ve rol güvenliği, 72 saatlik çevrimdışı kuyruk, sunucu tarafı damga ve hash zinciri, belge takvimi, aylık özet ve sıcaklık günlüğü PDF'leri, madde kütüphanesi. Veriler **Türkiye'de değil** (Anthropic altyapısı): gerçek personel adı, gerçek müşteri verisi ve kişi yüzü içeren fotoğraf girilmez — ADR-0003 gereği gerçek pilot bu demoyla yapılmaz.

**İki liste ve sabah özeti (5 Ekim).** Demo artık tek listeli değil: **açılış** (9 madde, şubenin açılış saatinden türetilen pencere: −45/+30 dk, tolerans 60) ve **kapanış** (15 madde, −60/+90 dk, tolerans 120) listeleri birlikte çalışır; kiosk ikisini de gösterir, pano ızgarası iki sütunlu, çalıştırma kaydı `şube_gün_liste` kimliğiyle ayrılır. Açılış listesinin başında **“dün gece” bloğu** (E-3) durur: önceki gecenin başarısız ve yapılamayan maddeleri, sebepleri ve hâlâ açık aksiyon sayısı; kayıt yoksa “dün gece kapanış gönderilmemiş” uyarısı, sorun yoksa yeşil “dün gece sorun yok”. Dördüncü sekme **Sabah özeti** (E-5): bölge müdürünün 07:00 görünümü — bildirim kartı, dört sayı, sorunlu şube kartları (tıklayınca panodaki detaya gider) ve “bu özet gerçek üründe push + e-posta olarak gider, demoda gönderilmez” bandı.

**Belge takvimi ve aylık özet (5 Ekim).** Broşürde ve föyde v1 özelliği olarak satılan iki satır demoda da çalışıyor:

- **E-12 · belge takvimi:** beşinci sekme. Yangın tüpü dolumu, baca ve su deposu temizliği, periyodik elektrik kontrolü, hijyen eğitimi, portör muayenesi ve ruhsat kayıtları şube, geçerlilik bitişi, sorumlu ve isteğe bağlı belge fotoğrafıyla tutulur; kalan gün sayısı demo saatine göre hesaplanır, 30 ve 7 gün eşikleri renklenir, süresi geçen kayıt “belge eksik” sayılır. Belge ekleme (tür seçilince bitiş tarihi türün süresine göre önerilir), yenileme, silme, “yaklaşan ve geçmiş” filtresi ve doğrulama kodlu **dönem PDF'i**. Boş ekranda “örnek kayıtları oluştur” düğmesi var.
- **E-7 · aylık tek sayfa özet:** panodaki düğme; ayın başından bugüne şube × liste beklentisine göre gönderilen, zamanında, geç, kaçırılan, başarısız, yapılamadı, kanıt ve açık aksiyon sayıları, toplam satırıyla. Rapor katmanında açılır, yazdırılır.

**Kanıt bütünlüğü ve sıcaklık günlüğü (5 Ekim).** Demo artık iki v1 satırını daha gerçekten çalıştırıyor:

- **E-11 · kanıt bütünlüğü:** yüklenen dosyanın SHA-256 özeti tarayıcıda hesaplanır; aynı dosya ikinci kez gönderilmek istenirse **reddedilir** ("bu fotoğraf daha önce gönderildi — madde X, saat, kişi") ve deneme olay izine yazılır. Dosyanın `lastModified` damgası 15 dakikadan eskiyse kanıt **"fotoğraf şimdi çekilmemiş"** işaretiyle kabul edilir; işaret çalıştırma detayında, raporda ve panodaki **"şüpheli kanıt"** filtresinde görünür. Konum ve cihaz saati bayrakları ile yakın kopya (benzer kare) tespiti demoda yok — tarayıcıda dürüstçe yapılamaz, üründe sunucu tarafında olacak.
- **R-4 · sıcaklık / ölçüm günlüğü:** panodaki "Sıcaklık günlüğü" düğmesi son 30 günün tüm ölçümlerini tarih, saat, şube, liste, ölçüm noktası, değer, kabul aralığı ve kişi sütunlarıyla listeler; aralık dışı satırlar kırmızı, notu ve açılan aksiyonu görünür. Çalıştırma raporuyla aynı sayfa-içi katmanda açılır, doğrulama kodu taşır, "Yazdır / PDF" ile iner.

**Kanıt ne zaman istenir (4 Ekim düzeltmesi).** Fotoğraf ve not her maddede değil, yalnızca iki durumda zorunludur: (1) cevap olumsuzsa — “Hayır”, “uygun değil” veya ölçüm aralık dışı (tek sabit kural, FR-0405): fotoğraf + not, madde kritikse aksiyon; (2) maddenin kendisi *fotoğraf zorunlu* işaretliyse — kapanış listesinde 15 maddenin **4'ü** (kahve makinesi, zemin, çöp alanı, kepenk). Normal gecede 11 madde tek dokunuşla kapanır. İlk sürümde arayüz her maddede “Not (zorunlu)” ve “Fotoğraf çek” gösteriyordu — kural doğruydu ama ekran yanlış şey söylüyordu; not/fotoğraf bloğu artık yalnızca gerektiğinde açılır, gerekmediğinde “Not veya fotoğraf ekle” bağlantısı durur ve onay maddesinde “Evet” tek dokunuşta kaydeder.

**Tablet testi (5 Ekim, 768×1024, ikinci tur).** İki bulgu: (1) **mantık hatası** — seçim maddesinde olumlu cevaplar koda gömülüydü ("Yapıldı"/"Uygun değil"); açılış listesindeki "Zamanında" cevabı başarısız sayılıp fotoğraf ve not istiyordu. Olumlu cevaplar artık maddede tanımlı (`olumlu`); açılış saati maddesi de listeden çıkarıldı (bu konu büyüme listesinde A20). (2) Alt sayfa açıkken sekme değiştirilince alt sayfa ekranda kalıyordu → sekme değişiminde kapanıyor. Tablette üst çubuk 88 px, dört ekranda yatay taşma yok, sıcaklık günlüğünün sekiz sütunu tam sığıyor.

**Mobil testi (5 Ekim, 375×812, ikinci tur).** Dört özellik eklendikten sonra tekrar denendi; iki hata çıktı: (1) **ikonlar hiç çizilmiyordu** — `el()` yardımcısı `document.createElement` kullandığı için `<svg>` ve `<path>` XHTML ad alanında oluşuyor, 0×0 kalıyordu (onay işaretleri, bildirim zili); yardımcı ad alanı farkında hâle getirildi. (2) Sıcaklık günlüğü raporunun sekiz sütunlu tablosu telefonda sayfayı yatay taşırıyordu → rapor tabloları dar ekranda kendi içinde kayıyor. Ayrıca dördüncü sekme eklenince üst çubuk 137 px'e çıkmıştı; dar ekranda sekme etiketleri kısaltıldı (Tablet · Özet · Pano · Ayar) ve çubuk 74 px'e indi.

**Tablet testi (5 Ekim, 768×1024).** Merkez panosu ve kiosk tablette denendi; üç düzeltme çıktı: (1) kaçırılan listede kayıt belgesi olmadığı için pano satırı çöküyordu (`k.aksiyonlar` null) — düzeltildi; (2) çalıştırma raporu yeni sekmede açılıyordu, açılır pencere engelliyse hiç açılmıyordu — rapor artık **sayfa içinde** tam ekran açılıyor, “Yazdır / PDF” ve “Kapat” düğmeleriyle; yazdırmada yalnızca rapor basılıyor (A4, 14 mm kenar); (3) KPI şeridi tablette 5+1 bölünüyordu, altı kutu tek satıra alındı. Kiosk alt sayfası tablette 560 px ortalanmış diyalog olarak açılıyor.

**Demo saati.** "Demo ayarı" sekmesinden saat ilerletilir: *pencereyi aç*, *toleransı doldur (kaçırıldı)*, *sıfırla*. Paylaşımlı modda kaydırma tüm cihazlarda ortaktır, böylece tablet ve pano aynı saati görür.

**Nerede kullanılır:** görüşmede iki cihazla canlı gösterim (tablet + dizüstü, ikisi de sizin hesabınızla), kendi test şubenizde bir gecelik deneme, saha kiosk denemesi kitinin ([07-kiosk-saha-denemesi](../../01-strateji/dogrulama-sprinti/07-kiosk-saha-denemesi.md)) sahte ekran yerine çalışan sürümle koşulması.


## 1. Blok 8 prototipi (personel + bölge müdürü, telefon)

`blok8-prototip.html` — görüşme rehberi Blok 8'de gösterilen tıklanabilir prototip (tek dosya, bağımlılık yok, telefonda tam ekran). Akış: kiosk PIN → Bugün → kapanış listesi → gönderim → bölge müdürünün sabah özeti → çalıştırma detayı ve olay izi. Sağdaki görüşmeci panelinden ekranlara atlanır; isim testi için marka seçici (Talimatname, yap lütfen, tamamlist, tembihle) — sırayı her görüşmede değiştirin.

Kapanış listesi, [şablon kütüphanesindeki](../../02-urun/07-sablon-kutuphanesi.md) 1 numaralı şablonun 15 maddesidir (A bar ve mutfak · B salon ve tuvalet · C güvenlik). Görüşülen kişi madde ekleyip çıkardıkça önce şablon belgesi, sonra prototip güncellenir.

Gösterilen davranışlar: onay maddesine ikinci dokunuş → "Yapılamadı" veya "İşareti kaldır"; fotoğraf maddesinde kamera doğrudan açılır, sağ üstte "Yapılamadı"; sıcaklıkta madde başına kabul aralığı (dolaplar 0–4 °C, dondurucu −30…−18 °C), aralık dışı → not + fotoğraf + kritik aksiyon; gönderimde "Başarısız (kritik madde)" ve puan (bilgi). Aynı senaryonun basılı çıktısı: [kanıt raporu örnekleri](../06-kanit-raporu/README.md) (çalıştırma raporu 13 Eylül, Kadıköy).

**Şube müdürü akışı (Ayşe):** kilit ekranında "Ayşe K." + PIN → "Şubem": dün gece (başarısız/yapılamadı → aksiyon), bugünün listeleri, **kapanışı kişiye verme** (UC-19), **"Yapılmayacak"** işaretleme (su kesintisi → eskalasyon durur), personelin bildirdiği **sorunları aksiyona çevirme**, **PIN atama** (E-1). Aksiyon ekranı: not ekle (silinmez), kapatırken not zorunlu, fotoğraf isteğe bağlı. Bölge müdürü detayındaki "Aksiyonu aç" da aynı ekrana gider.

**Çevrimdışı simülasyonu:** görüşmeci panelinde "Wi-Fi kes" — şerit belirir, cevaplar ve fotoğraflar "senk bekliyor" sayacına yazılır, gönderim cihazda kalır; "Wi-Fi bağla" ile senk olur ve zaman damgaları sunucu saatiyle düzeltilir (S-02 Beşiktaş). **Pencere kapandı senaryosu:** 03:45'te listeyi açınca "kilitli — kaçırıldı" sayfası (S-07). **Sorun bildir:** kategori + not + isteğe bağlı fotoğraf → şube müdürüne düşer (UC-11).

**Kiosk modu:** adrese `?kiosk=1` eklenince görüşmeci paneli gizlenir, ekran tam boy olur (tablet, yatay), avatar ızgarası genişler, 2 dakika dokunulmazsa kilit ekranına döner ve PIN'le kaldığı yerden devam eder. Saha kiosk denemesi için: [01-strateji/dogrulama-sprinti/07-kiosk-saha-denemesi.md](../../01-strateji/dogrulama-sprinti/07-kiosk-saha-denemesi.md).

Veri kaydetmez; kamera sahtedir; sıcaklık ± ile girilir. Canlı sürüm (telefon için): bkz. 00-urun-merkezi.md dış bağlantılar.

## 2. Yönetici web prototipi (LOI turu, karar verici)

`yonetici-web-prototip.html` — masaüstü yönetim paneli: **kurulum sihirbazı** (4 adım: marka ve şubeler → kapanış şablonu → plan → personel ve kiosk; yayınlayınca "bu gece başlar"), **pano** (istisna odaklı: yalnızca dikkat isteyenler; gün seçici ile "her şey yolunda" durumu; "tümünü göster" ile şube × liste ızgarası, hücrede tooltip), **çalıştırma detayı** (maddeler, damgalı fotoğraflar, aksiyona not ekleme ve kapatma — kapatırken not zorunlu, olay izi, çalıştırma PDF'i bağlantısı), **aksiyon listesi** (filtreler: açık, gecikmiş, bölgem), **şablonlar / planlar / şubeler / raporlar** sayfaları (v1 kapsamı; v1.1 olanlar menüde etiketli) ve **07:00 sabah özeti** (e-posta + push; "her şey yolunda" varyantı). Sağ altta görüşmeci paneli: isim seçici ve senaryo sırası.

İddia: "Kurulum bir saat, sabah iki dakika." Görüşmede sorulacak: "Bunu her sabah açar mıydınız? Kim açar? Kurulumu kim yapar?" Pano ve e-posta verisi örnektir (yayından bir ay sonrası); Blok 8 prototipi ve kanıt raporlarıyla aynı Kadıköy senaryosu.

Sıra: Blok 8 prototipi ilk görüşmede (personel akışı); web prototipi K1 sonrası LOI turunda, karar vericiyle ikinci görüşmede.
