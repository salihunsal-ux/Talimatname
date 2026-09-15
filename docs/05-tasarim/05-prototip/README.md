# Prototipler

İki tıklanabilir prototip, tek dosya, bağımlılık yok, veri kaydetmez.

## 1. Blok 8 prototipi (personel + bölge müdürü, telefon)

`blok8-prototip.html` — görüşme rehberi Blok 8'de gösterilen tıklanabilir prototip (tek dosya, bağımlılık yok, telefonda tam ekran). Akış: kiosk PIN → Bugün → kapanış listesi → gönderim → bölge müdürünün sabah özeti → çalıştırma detayı ve olay izi. Sağdaki görüşmeci panelinden ekranlara atlanır; isim testi için marka seçici (Talimatname, yap lütfen, tamamlist, tembihle) — sırayı her görüşmede değiştirin.

Kapanış listesi, [şablon kütüphanesindeki](../../02-urun/07-sablon-kutuphanesi.md) 1 numaralı şablonun 15 maddesidir (A bar ve mutfak · B salon ve tuvalet · C güvenlik). Görüşülen kişi madde ekleyip çıkardıkça önce şablon belgesi, sonra prototip güncellenir.

Gösterilen davranışlar: onay maddesine ikinci dokunuş → "Yapılamadı" veya "İşareti kaldır"; fotoğraf maddesinde kamera doğrudan açılır, sağ üstte "Yapılamadı"; sıcaklıkta madde başına kabul aralığı (dolaplar 0–4 °C, dondurucu −30…−18 °C), aralık dışı → not + fotoğraf + kritik aksiyon; gönderimde "Başarısız (kritik madde)" ve puan (bilgi). Aynı senaryonun basılı çıktısı: [kanıt raporu örnekleri](../06-kanit-raporu/README.md) (çalıştırma raporu 13 Eylül, Kadıköy).

**Kiosk modu:** adrese `?kiosk=1` eklenince görüşmeci paneli gizlenir, ekran tam boy olur (tablet, yatay), avatar ızgarası genişler, 2 dakika dokunulmazsa kilit ekranına döner ve PIN'le kaldığı yerden devam eder. Saha kiosk denemesi için: [01-strateji/dogrulama-sprinti/07-kiosk-saha-denemesi.md](../../01-strateji/dogrulama-sprinti/07-kiosk-saha-denemesi.md).

Veri kaydetmez; kamera sahtedir; sıcaklık ± ile girilir. Canlı sürüm (telefon için): bkz. 00-urun-merkezi.md dış bağlantılar.

## 2. Yönetici web prototipi (LOI turu, karar verici)

`yonetici-web-prototip.html` — masaüstü yönetim paneli: **kurulum sihirbazı** (4 adım: marka ve şubeler → kapanış şablonu → plan → personel ve kiosk; yayınlayınca "bu gece başlar"), **pano** (istisna odaklı: yalnızca dikkat isteyenler; gün seçici ile "her şey yolunda" durumu; "tümünü göster" ile şube × liste ızgarası, hücrede tooltip), **çalıştırma detayı** (maddeler, damgalı fotoğraflar, aksiyona not ekleme ve kapatma — kapatırken not zorunlu, olay izi, çalıştırma PDF'i bağlantısı), **aksiyon listesi** (filtreler: açık, gecikmiş, bölgem), **şablonlar / planlar / şubeler / raporlar** sayfaları (v1 kapsamı; v1.1 olanlar menüde etiketli) ve **07:00 sabah özeti** (e-posta + push; "her şey yolunda" varyantı). Sağ altta görüşmeci paneli: isim seçici ve senaryo sırası.

İddia: "Kurulum bir saat, sabah iki dakika." Görüşmede sorulacak: "Bunu her sabah açar mıydınız? Kim açar? Kurulumu kim yapar?" Pano ve e-posta verisi örnektir (yayından bir ay sonrası); Blok 8 prototipi ve kanıt raporlarıyla aynı Kadıköy senaryosu.

Sıra: Blok 8 prototipi ilk görüşmede (personel akışı); web prototipi K1 sonrası LOI turunda, karar vericiyle ikinci görüşmede.
