# Tanıtım belgeleri: 2 sayfalık broşür + 6 sayfalık tanıtım dosyası

Ne zaman kullanılır: **Blok 8'den sonra** (görüşme rehberi kuralı: ürün ilk 40 dakika anlatılmaz), LOI turunda karar vericiye, tanıştıran kişi "bir şey gönder" dediğinde ve aday geliştiricilere. Ulaşım mesajlarına eklenmez.

| Dosya | Ne |
|---|---|
| `talimatname-brosur.html` / `.pdf` | Yazdırmaya hazır broşür: sayfa 1 iddia + kapanış listesi ve aralık dışı sıcaklık ekranları + üç adım; sayfa 2 merkez görünümü (pano, sabah özeti, çalıştırma PDF'i), neden Talimatname, 8 haftalık pilot, iletişim |
| `Main.dc.html`, `Sayfa2.dc.html` | Aynı iki sayfanın tasarım tuvali sürümü (düzenlenebilir) |
| `KioskListe.dc.html`, `Sicaklik.dc.html`, `SabahOzeti.dc.html`, `Pano.dc.html` | Gerçeğe yakın ekran tasarımları (390×844 telefon, 1200×760 web); tasarım sistemi token'larıyla (05-tasarim/04) |
| `canvas.json` | Tuval yerleşimi |
| `build_brosur.py` | Hepsini üretir; `--pdf` ile Edge headless PDF |

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

Hangisi ne zaman: **2 sayfalık broşür** görüşmede bırakılır; **6 sayfalık tanıtım dosyası** üzerinden ürün anlatılır (ekran paylaşımı veya basılı), karar vericiye ve aday geliştiriciye gönderilir. İkisinde de fiyat yoktur ve iletişim alanları köşeli parantezlidir.
