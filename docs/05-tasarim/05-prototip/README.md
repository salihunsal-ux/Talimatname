# Prototipler

İki tıklanabilir prototip (veri kaydetmez) ve bir **çalışan saha demosu** (veri saklar). Hepsi tek dosya, bağımlılık yok.

## 0. Saha demosu — çalışan sürüm (4 Ekim 2026)

`saha-demosu.html` → https://claude.ai/artifact/WGKqPtVDturkaRaoLRtiRy

Tıklanabilir prototiplerden farkı: **kayıt tutar**. Pencere ve tolerans gerçek saatle işler, madde cevapları ve cihaz kamerasıyla çekilen kanıt saklanır, kritik madde ve yapılamadı aksiyon açar, gönderim kaydı kilitler, merkez panosu aynı kaydı görür ve doğrulama kodlu raporu yazdırır.

**İki mod.** Artifact veri tabanına yalnızca yazma yetkisi olan hesaplar (sahibi ve e-postayla davet edilen düzenleyiciler; kurumsal planda şirket üyeleri) yazabilir — onlarda *paylaşımlı mod* çalışır: tablette doldurulan liste merkez panosunda canlı görünür. Diğer herkeste *yerel mod*: akış birebir aynıdır, veriler yalnızca o cihazda kalır. Mod üst çubukta yazar.

**Demoda olmayan (üründe var):** push ve SMS, gerçek kimlik ve rol güvenliği, 72 saatlik çevrimdışı kuyruk, sunucu tarafı damga ve hash zinciri, belge takvimi, aylık özet ve sıcaklık günlüğü PDF'leri, madde kütüphanesi. Veriler **Türkiye'de değil** (Anthropic altyapısı): gerçek personel adı, gerçek müşteri verisi ve kişi yüzü içeren fotoğraf girilmez — ADR-0003 gereği gerçek pilot bu demoyla yapılmaz.

**İki liste ve sabah özeti (5 Ekim).** Demo artık tek listeli değil: **açılış** (9 madde, şubenin açılış saatinden türetilen pencere: −45/+30 dk, tolerans 60) ve **kapanış** (15 madde, −60/+90 dk, tolerans 120) listeleri birlikte çalışır; kiosk ikisini de gösterir, pano ızgarası iki sütunlu, çalıştırma kaydı `şube_gün_liste` kimliğiyle ayrılır. Açılış listesinin başında **“dün gece” bloğu** (E-3) durur: önceki gecenin başarısız ve yapılamayan maddeleri, sebepleri ve hâlâ açık aksiyon sayısı; kayıt yoksa “dün gece kapanış gönderilmemiş” uyarısı, sorun yoksa yeşil “dün gece sorun yok”. Dördüncü sekme **Sabah özeti** (E-5): bölge müdürünün 07:00 görünümü — bildirim kartı, dört sayı, sorunlu şube kartları (tıklayınca panodaki detaya gider) ve “bu özet gerçek üründe push + e-posta olarak gider, demoda gönderilmez” bandı.

**Mobil ve tablet üçüncü tur (5 Ekim).** Simülasyon katmanından sonra iki ekranda tekrar gezildi; tek hata çıktı ve düzeltildi: **bildirim kartı telefonda yapışkan “Gönder” çubuğunun üstüne biniyordu** (695–798 px ile 693–802 px çakışıyordu) — personel gönder düğmesine basamazdı. Kartlar artık üst çubuğun hemen altına, çubuğun gerçek yüksekliği ölçülerek yerleşiyor (telefonda 112 px, tablette 98 px). Kalan kontroller temiz: altı ekranda yatay taşma yok, konsol hatasız; OTP kutuları telefonda 51 px (dokunulabilir), şablon önizleme ve fatura raporu her iki ekranda sığıyor, “Üründe var” kartları tablette iki sütun.

**Simülasyon katmanı (5 Ekim).** Kullanıcı kararı: sunucu gerektiren yetenekler de *çalışıyormuş gibi* gösterilsin, ama her ekranda rozetle. Üç sınır konuldu ve koda yazıldı:

1. **Kanal eylemi taklit edilmez.** Hiçbir yerde “SMS gönderildi” yazmaz; “giderdi · demoda gönderilmez” denir. Demo, pilot sözleşmesinde taahhüt doğurmamalı.
2. **Sonuç iddiası üretilmez.** Kurgu müşteri sayısı, başarı yüzdesi, referans yoktur; veri yalnızca akışı gösterir.
3. **Gerçek risk gizlenmez.** Taklit edilen yerler Sprint 0'daki dört spike'ın konusu; demo onların yerine geçmez.

Eklenen davranışlar: kural tetiklendiği anda ekranda **bildirim kartı** (kritik madde, yapılamadı, gönderim, sorun) — “simülasyon” etiketli; **telefonla giriş akışı** (numara → 6 haneli kod → “doğrulandı (simülasyon)” + rol kapsamı); **şablon önizleme** (çalışmayan altı şablonun madde listesi); **KVKK talep akışı** (tür seç → kayıt no üretilir, kayıt oluşmaz); **dönem faturası önizlemesi** (aktif şube sayacından, tutar yok); **hash zincirini bozma denemesi** (bir olayı değiştir → zincir gerçekten yeniden hesaplanır ve “zincir kırıldı” çıkar).

**“Üründe var” sekmesi (5 Ekim).** v1'in sunucu gerektiren kısmı artık demoda **etiketli gösterim** olarak duruyor — çalışmıyor ama görülüyor. Kural: çalışmayan her öğede rozet var — *çalışmaz · gösterim*, *kısmen çalışır* ya da *simülasyon · gerçek veriden*. Sekiz kart:

| Kart | Durum | Ne gösterir |
|---|---|---|
| Bildirim ve eskalasyon | simülasyon | Demodaki gerçek kayıtlardan, kuralların bugün kime/ne zaman/hangi kanaldan bildirim göndereceğini listeler; hiçbiri gönderilmez |
| Kurulum sihirbazı ve Excel | kısmen | Dört adım gezilebilir, Excel hata raporu örneği; kaydetmez |
| Şablon kütüphanesi | kısmen | Sekiz şablon listelenir, ikisi demoda gerçekten çalışır |
| Giriş, roller ve yetki | çalışmaz | Telefon + OTP ekranı ve rol × kapsam tablosu |
| Çevrimdışı kuyruk | simülasyon | Bağlantı kesme/geri gelme ile kuyruk davranışı |
| Denetim izi ve hash zinciri | simülasyon | Olay zinciri **tarayıcıda gerçekten SHA-256 ile** hesaplanır; üründe sunucuda |
| KVKK ve saklama | çalışmaz | Aydınlatma metni özeti, talep akışı, 24 ay saklama |
| Faturalama ve hesap | çalışmaz | Aktif şube sayacı; tutar yok (fiyat görüşmede) |

Dar ekranda sekme şeridi tek sıra ve yatay kaydırmalı; etiketler `matchMedia` ile kısalır.

**Aksiyon listesi, sorun bildirimi, kiosk kilidi ve puan (5 Ekim).** v1'in eklenebilir kalan dört satırı:

- **A-6 · aksiyon listesi:** panodaki “Aksiyonlar (N)” düğmesi tüm aksiyonları tek listede toplar — çalıştırmalardan gelenler ve personelin bildirdiği sorunlar. Filtreler açık / gecikmiş / tümü; her kartta şube, kaynak, açılış ve **vade** (kritik madde 4 saat, yapılamadı ve sorun 72 saat), vadesi geçen kırmızı. Not yazmadan kapatılamaz; “Çalıştırmayı aç” ilgili geceye gider.
- **Y-7 · sorun bildir:** kiosk “Bugün” ekranında düğme. Sabit kategori (ekipman arızası, malzeme eksik, hijyen/haşere, güvenlik, diğer), zorunlu açıklama, isteğe bağlı fotoğraf; şube müdürüne iş olarak düşer ve aksiyon listesinde görünür.
- **O-5 · kiosk kilidi:** 2 dakika hareketsizlikte oturum kapanır, giriş ekranında “kilitlendi, PIN'inizle girince liste kaldığı yerden devam eder” uyarısı çıkar. Ayrıca elle “Çıkış” düğmesi.
- **Ş-5 · puan:** gönderimde zorunlu maddelerin yüzdesi hesaplanır; kiosk sonucunda, çalıştırma detayında ve raporda “puan %93 (bilgi)” olarak görünür. Sonucu belirleyen puan değil, kritik maddedir.

**Belge takvimi ve aylık özet (5 Ekim).** Broşürde ve föyde v1 özelliği olarak satılan iki satır demoda da çalışıyor:

- **E-12 · belge takvimi:** beşinci sekme. Yangın tüpü dolumu, baca ve su deposu temizliği, periyodik elektrik kontrolü, hijyen eğitimi, portör muayenesi ve ruhsat kayıtları şube, geçerlilik bitişi, sorumlu ve isteğe bağlı belge fotoğrafıyla tutulur; kalan gün sayısı demo saatine göre hesaplanır, 30 ve 7 gün eşikleri renklenir, süresi geçen kayıt “belge eksik” sayılır. Belge ekleme (tür seçilince bitiş tarihi türün süresine göre önerilir), yenileme, silme, “yaklaşan ve geçmiş” filtresi ve doğrulama kodlu **dönem PDF'i**. Boş ekranda “örnek kayıtları oluştur” düğmesi var.
- **E-7 · aylık tek sayfa özet:** panodaki düğme; ayın başından bugüne şube × liste beklentisine göre gönderilen, zamanında, geç, kaçırılan, başarısız, yapılamadı, kanıt ve açık aksiyon sayıları, toplam satırıyla. Rapor katmanında açılır, yazdırılır.

**Kanıt bütünlüğü ve sıcaklık günlüğü (5 Ekim).** Demo artık iki v1 satırını daha gerçekten çalıştırıyor:

- **E-11 · kanıt bütünlüğü:** yüklenen dosyanın SHA-256 özeti tarayıcıda hesaplanır; aynı dosya ikinci kez gönderilmek istenirse **reddedilir** ("bu fotoğraf daha önce gönderildi — madde X, saat, kişi") ve deneme olay izine yazılır. Dosyanın `lastModified` damgası 15 dakikadan eskiyse kanıt **"fotoğraf şimdi çekilmemiş"** işaretiyle kabul edilir; işaret çalıştırma detayında, raporda ve panodaki **"şüpheli kanıt"** filtresinde görünür. Konum ve cihaz saati bayrakları ile yakın kopya (benzer kare) tespiti demoda yok — tarayıcıda dürüstçe yapılamaz, üründe sunucu tarafında olacak.
- **R-4 · sıcaklık / ölçüm günlüğü:** panodaki "Sıcaklık günlüğü" düğmesi son 30 günün tüm ölçümlerini tarih, saat, şube, liste, ölçüm noktası, değer, kabul aralığı ve kişi sütunlarıyla listeler; aralık dışı satırlar kırmızı, notu ve açılan aksiyonu görünür. Çalıştırma raporuyla aynı sayfa-içi katmanda açılır, doğrulama kodu taşır, "Yazdır / PDF" ile iner.

**Kanıt ne zaman istenir (4 Ekim düzeltmesi).** Fotoğraf ve not her maddede değil, yalnızca iki durumda zorunludur: (1) cevap olumsuzsa — “Hayır”, “uygun değil” veya ölçüm aralık dışı (tek sabit kural, FR-0405): fotoğraf + not, madde kritikse aksiyon; (2) maddenin kendisi *fotoğraf zorunlu* işaretliyse — kapanış listesinde 15 maddenin **4'ü** (kahve makinesi, zemin, çöp alanı, kepenk). Normal gecede 11 madde tek dokunuşla kapanır. İlk sürümde arayüz her maddede “Not (zorunlu)” ve “Fotoğraf çek” gösteriyordu — kural doğruydu ama ekran yanlış şey söylüyordu; not/fotoğraf bloğu artık yalnızca gerektiğinde açılır, gerekmediğinde “Not veya fotoğraf ekle” bağlantısı durur ve onay maddesinde “Evet” tek dokunuşta kaydeder.

**Masaüstü testi (5 Ekim, 1280×900).** Altı sekme, kiosk akışı, raporlar ve simülasyon ekranları masaüstü genişliğinde denendi; **altı hata** çıktı, hepsi düzeltildi: (1) **“Yapılamadı” akışı tamamen kırıktı** — `SEBEPLER` sabiti dosyada hiç tanımlı değildi, düğmeye basınca alt sayfa açılmadan çöküyordu (önceki turlarda bu akış ekrandan değil kodla doldurulmuştu, o yüzden görülmemiş); FR-0801'in sabit sebep seti eklendi, not isteğe bağlı fotoğraf bloku da aynı kanıt bütünlüğü kurallarıyla çalışıyor. (2) **Kritik maddede “Yapılamadı” düğmesi duruyordu** — FR-0304 bunu yasaklıyor; düğme kaldırıldı, yerine kısa açıklama kondu. (3) **“Geç gönderildi” yanlış hesaplanıyordu** — gönderimde pencere liste parametresi verilmeden alınıyor, açılış çalıştırması kapanış penceresine göre ölçülüyordu; 09:30'da gönderilen açılış listesi “zamanında” görünüyordu. (4) **Geç tamamlanan çalıştırma hiçbir ekranda görünmüyordu** — FR-0514'teki “geç tamamlandı” durumu artık panoda ayrı KPI, ızgarada sarı hücre, “dikkat isteyenler” satırı (FR-1201: geç / kaçırıldı / başarısız / yapılamadı) ve sabah özetinde kart olarak çıkıyor; çalıştırma raporunun sonuç satırı da “geç tamamlandı” yazıyor. (5) **Aynı ekranda iki farklı “açık aksiyon” sayısı** vardı — KPI yalnızca bugünün hücrelerini, düğme tüm kuyruğu sayıyordu (3'e karşı 4); ikisi de açık iş kuyruğunu sayar oldu, aylık özetin “açık aksiyon” sütunu da bildirilen sorunları kapsıyor. (6) Giriş ve KVKK simülasyon ekranlarında `<br>` **metin olarak** görünüyordu; şablon önizlemesi ise “gösterim” olduğu hâlde “simülasyon · gerçek veriden” rozeti taşıyordu — rozet düzeltildi. Ayrıca şube tableti ekranı masaüstünde 1152 px'e yayılıyordu; 900 px üstünde 860 px'te ortalanıyor (üründe bu ekran tablette kullanılır), pano ve raporlar tam genişlikte kalıyor. Altı sekmede yatay taşma ve konsol hatası yok; bildirim şeridi üst çubuğun 10 px altında (62 px) duruyor, alt sayfa 560 px ortalanmış diyalog, raporlar 820 px sütun. Düzeltmelerden sonra tablet (768×1024) ve telefon (375×812) tekrar tarandı: taşma yok, yeni “geç” durumu ve yapılamadı alt sayfası iki boyutta da doğru. Masaüstünde kalan bilinçli sınır: sıcaklık değeri yalnızca ± düğmeleriyle giriliyor (0,1 adım), klavyeyle yazılamıyor — tablet için tasarlandı, üründe sayısal tuş takımı da olacak.

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
