# Prototipler

İki tıklanabilir prototip (veri kaydetmez) ve bir **çalışan saha demosu** (veri saklar). Hepsi tek dosya, bağımlılık yok.

## 0. Saha demosu — çalışan sürüm (4 Ekim 2026)

`saha-demosu.html` → https://claude.ai/artifact/WGKqPtVDturkaRaoLRtiRy

Tıklanabilir prototiplerden farkı: **kayıt tutar**. Pencere ve tolerans gerçek saatle işler, madde cevapları ve cihaz kamerasıyla çekilen kanıt saklanır, kritik madde ve yapılamadı aksiyon açar, gönderim kaydı kilitler, merkez panosu aynı kaydı görür ve doğrulama kodlu raporu yazdırır.

**İki mod.** Artifact veri tabanına yalnızca yazma yetkisi olan hesaplar (sahibi ve e-postayla davet edilen düzenleyiciler; kurumsal planda şirket üyeleri) yazabilir — onlarda *paylaşımlı mod* çalışır: tablette doldurulan liste merkez panosunda canlı görünür. Diğer herkeste *yerel mod*: akış birebir aynıdır, veriler yalnızca o cihazda kalır. Mod üst çubukta yazar.

**Demoda olmayan (üründe var):** push ve SMS, gerçek kimlik ve rol güvenliği, 72 saatlik çevrimdışı kuyruk, sunucu tarafı damga ve hash zinciri, belge takvimi, aylık özet ve sıcaklık günlüğü PDF'leri, madde kütüphanesi. Veriler **Türkiye'de değil** (Anthropic altyapısı): gerçek personel adı, gerçek müşteri verisi ve kişi yüzü içeren fotoğraf girilmez — ADR-0003 gereği gerçek pilot bu demoyla yapılmaz.

**Kanıt ne zaman istenir (4 Ekim düzeltmesi).** Fotoğraf ve not her maddede değil, yalnızca iki durumda zorunludur: (1) cevap olumsuzsa — “Hayır”, “uygun değil” veya ölçüm aralık dışı (tek sabit kural, FR-0405): fotoğraf + not, madde kritikse aksiyon; (2) maddenin kendisi *fotoğraf zorunlu* işaretliyse — kapanış listesinde 15 maddenin **4'ü** (kahve makinesi, zemin, çöp alanı, kepenk). Normal gecede 11 madde tek dokunuşla kapanır. İlk sürümde arayüz her maddede “Not (zorunlu)” ve “Fotoğraf çek” gösteriyordu — kural doğruydu ama ekran yanlış şey söylüyordu; not/fotoğraf bloğu artık yalnızca gerektiğinde açılır, gerekmediğinde “Not veya fotoğraf ekle” bağlantısı durur ve onay maddesinde “Evet” tek dokunuşta kaydeder.

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
