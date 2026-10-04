# Tanıtım belgeleri: 2 sayfalık broşür + 8 sayfalık tanıtım dosyası + 5 sayfalık özellik föyü

Ne zaman kullanılır: **Blok 8'den sonra** (görüşme rehberi kuralı: ürün ilk 40 dakika anlatılmaz), LOI turunda karar vericiye, tanıştıran kişi "bir şey gönder" dediğinde ve aday geliştiricilere. Ulaşım mesajlarına eklenmez.

| Dosya | Ne |
|---|---|
| `talimatname-brosur.html` / `.pdf` | Yazdırmaya hazır 2 sayfalık broşür (3 Ekim'de tanıtım dosyasının tasarım diline çekildi): sayfa 1 koyu hero bandı + dört ölçü + "ne değişir" + üç adım; sayfa 2 açıklamalı pano ekranı, alternatif karşılaştırması, iki itiraz cevabı, koyu pilot bandı ve iletişim |
| `Main.dc.html`, `Sayfa2.dc.html` | Aynı iki sayfanın tasarım tuvali sürümü (düzenlenebilir) |
| `KioskListe.dc.html`, `Sicaklik.dc.html`, `SabahOzeti.dc.html`, `Pano.dc.html` | Gerçeğe yakın ekran tasarımları (390×844 telefon, 1200×760 web); tasarım sistemi token'larıyla (05-tasarim/04) |
| `canvas.json` | Tuval yerleşimi |
| `build_brosur.py` | Hepsini üretir; `--pdf` ile Edge headless PDF. **Ortak pazarlama bileşenleri burada** (koyu bant, h1/h2, ölçü kartı, tablo, numaralı ekran işaretleri, itiraz kutusu) — `build_tanitim.py` bunları içe aktarır, iki belge tek tasarım dilini paylaşır |

Canlı tuval (düzenle, PNG/PDF al): https://claude.ai/artifact/3LpwvVXZczJMNLqnKrBVn2

Doldurulacaklar: sayfa 2 altındaki `[Ad Soyad] · [telefon] · [e-posta] · [alan adı]`. Fiyat bilerek yok (van Westendorp ölçümünü bozmamak için: "şube başına aylık ücret görüşmede belirlenir"). Ekranlardaki veri örnektir (Kahve Durağı); isim Talimatname çalışma adıdır — kesin isim kararında wordmark `build_brosur.py` içinde tek yerden değişir.

Ekranlar prototiplerle aynı Kadıköy senaryosunu anlatır: 13 Eylül kapanışı, mutfak buzdolabı 6,0 °C, aksiyon #418, sabah özeti.

## Tanıtım dosyası — 8 sayfa (tek başına ürün tanıtımı)

`build_tanitim.py` → `tanitim/` artboard'ları (8 sayfa + 3 ekran) + `talimatname-tanitim.html` (yazdırma), `.pdf`, `talimatname-tanitim-sayfa.html` (yayın sürümü; dar ekranda sayfa ölçeklenir). Canlı: https://claude.ai/artifact/NDJqDvhikUbqqgtFNTZpQk

| Sayfa | İçerik |
|---|---|
| 1 | Kapak: koyu hero bandı (konumlanma cümlesi + iki ekran kompozisyonu), dört rozet, dört ölçü, "kim için ne kazanır" tablosu, içindekiler |
| 2 | Sorun ve bedeli: "tanıdık geliyorsa" kontrol listesi, maliyet hesabı (varsayım etiketli), görünmeyen kayıp (kayıt dışı satış), "ne zaman fark edilir" karşılaştırması |
| 3 | Nasıl çalışır: üç adım + bir gecenin zaman çizelgesi (22:00 → 08:05), "gece kimse aranmaz" kuralı |
| 4 | Personel deneyimi: iki açıklamalı ekran (numaralı işaretler + açıklama listesi), altı madde türü tablosu, sahadaki gerçekler |
| 5 | Yönetici deneyimi: sabah özeti ve istisna panosu (açıklamalı), sabit eskalasyon, iki ölçüt |
| 6 | Kanıt ve uyum: kanıt zinciri altı adım, çalıştırma raporu ekranı, KVKK soru-cevap tablosu |
| 7 | Karşılaştırma: WhatsApp / kâğıt-Excel / Talimatname tablosu, altı itiraz ve cevabı, "ne değil" |
| 8 | Pilot ve sonraki adım: koyu CTA bandı (8 haftalık pilot + üç ölçüt), pilot takvimi, yol haritası, iletişim |

Pazarlama düzenlemesi (3 Ekim): sayfa sayısı 6 → 8; maliyet hesabı, alternatif karşılaştırması, itiraz cevapları, pilot takvimi ve CTA eklendi; ekranlara numaralı açıklama işaretleri kondu; kapak ve kapanış koyu banda alındı.

Ekran tasarımları: `tanitim/Yapilamadi.dc.html` (mobil alt sayfa), `tanitim/Detay.dc.html` (web çalıştırma detayı), `tanitim/Sihirbaz.dc.html` (web kurulum sihirbazı adım 3). Ortak bileşenler `build_brosur.py`'den gelir; iki belge aynı Kadıköy senaryosunu anlatır.

## Özellik föyü — 5 sayfa (hangi özellik ne yapar, ekranda nasıl görünür)

`build_ozellikler.py` → `ozellikler/` artboard'ları (5 sayfa + 4 yeni ekran) + `talimatname-ozellikler.html` (yazdırma), `.pdf`, `talimatname-ozellikler-sayfa.html` (yayın sürümü). Canlı: https://claude.ai/artifact/JDHxYmF8ZnShvi78khafDD

Kime: **müşteriye** (zincir merkezi: operasyon müdürü, kalite sorumlusu). Dili fayda önce; ADR/FR/SCR/E-kodları, sürüm numaraları ve iç terimler bilerek yok. Sıralama satış mantığına göre: önce merkezin kazancı, sonra kanıt/denetim, sonra sahada benimseme, en son kurulum kolaylığı.

Neden var: tanıtım dosyasının 8. sayfasındaki yol haritası tablosunda her özellik tek cümleydi. Föy, **bugünkü sürümde gelen 11 özelliği** birer ekran görseli, iki cümlelik açıklama ve üç maddelik ayrıntıyla gösterir; sıradaki sürüm ve sonrası son sayfada yalnızca metinle anlatılır (ekranları henüz çizilmedi, çizilmiş gibi gösterilmez).

| Sayfa | Tema | İçerik |
|---|---|---|
| 1 | Merkez ne görür | Koyu giriş bandı + gruplu içindekiler; 1 her sabah iki dakika (SabahOzeti), 2 sorunsuz gün tek cümledir (Pano) |
| 2 | Kanıt ve denetim | 3 denetim geldiğinde üç dakika (üç PDF küçük resmi), 4 “fotoğrafı dün çekmiş” tartışması biter (**yeni ekran: Bayraklar**), 5 belge süresi kaçmaz (**yeni ekran: BelgeTakvimi**) |
| 3 | Şubede nasıl yürür | 6 personel altı dakikada bitirir (KioskListe), 7 soğuk zincir kendini savunur (Sicaklik), 8 yapılamayan iş kaybolmaz (Yapilamadi) |
| 4 | Başlamak | 9 Wi-Fi gidince iş durmaz (**yeni ekran: Cevrimdisi**), 10 liste yazmakla uğraşmazsınız (**yeni ekran: Sablonlar**), 11 bir günde kurulur (Sihirbaz) |
| 5 | Yol haritası | “İlk sürümü neden dar tuttuk” kutusu; sıradaki sürüm (7 satır) ve daha sonrası (4 satır), her biri iki cümleyle; ekran yok notu |

Yeni ekranlar `ozellikler/Sablonlar.dc.html`, `Cevrimdisi.dc.html`, `Bayraklar.dc.html`, `BelgeTakvimi.dc.html`. BelgeTakvimi aynı zamanda **SCR-W-14'ün tel-çerçevesi yerine geçer** (ekran envanteri 05-tasarim/01). Ortak bileşenler yine `build_brosur.py`'den gelir; mevcut ekranlar `build_tanitim.py`'den içe aktarılır.

Hangisi ne zaman: **2 sayfalık broşür** görüşmede bırakılır; **8 sayfalık tanıtım dosyası** üzerinden ürün anlatılır; **özellik föyü** “bu tam olarak ne yapıyor” sorusu geldiğinde bırakılır (müşteri dili; geliştiriciye kapsam belgesi ve gereksinimler verilir) (ekran paylaşımı veya basılı), karar vericiye ve aday geliştiriciye gönderilir. İkisinde de fiyat yoktur ve iletişim alanları köşeli parantezlidir.
