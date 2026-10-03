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

## Tanıtım dosyası — 6 sayfa (anlatım için)

`build_tanitim.py` → `tanitim/` artboard'ları + `talimatname-tanitim.html` (yazdırma), `.pdf`, `talimatname-tanitim-sayfa.html` (yayın sürümü; dar ekranda sayfa ölçeklenir). Canlı: https://claude.ai/artifact/NDJqDvhikUbqqgtFNTZpQk

| Sayfa | İçerik |
|---|---|
| 1 | Kapak, tek cümle, "bugün ne oluyor" (WhatsApp / "yapıldı" / saatler), kim için (4 rol), içindekiler |
| 2 | Bir gecenin akışı 22:00 → 08:05 (zaman çizelgesi), "gece kimse aranmaz" kutusu, önce/sonra karşılaştırması |
| 3 | Personel tarafı: üç ekran (liste, sıcaklık aralık dışı, yapılamadı), tek kural, 6 madde türü tablosu, kiosk / çevrimdışı / kamera / dün gece |
| 4 | Yönetici tarafı: sabah özeti ve istisna panosu ekranları, sabit eskalasyon kuralları, üç ölçüt |
| 5 | Kanıt ve uyum: kanıt zinciri (damga → hash → olay günlüğü → PDF), çalıştırma detayı ekranı, KVKK tablosu |
| 6 | Kurulum sihirbazı ekranı, 8 hazır şablon, 8 haftalık pilot ve ölçütleri, v1 / v1.1 / v2 yol haritası, iletişim |

Yeni ekran tasarımları: `tanitim/Yapilamadi.dc.html` (mobil alt sayfa), `tanitim/Detay.dc.html` (web çalıştırma detayı), `tanitim/Sihirbaz.dc.html` (web kurulum sihirbazı adım 3). Ortak bileşenler `build_brosur.py`'den gelir; iki belge aynı Kadıköy senaryosunu anlatır.

Hangisi ne zaman: **2 sayfalık broşür** görüşmede bırakılır; **6 sayfalık tanıtım dosyası** üzerinden ürün anlatılır (ekran paylaşımı veya basılı), karar vericiye ve aday geliştiriciye gönderilir. İkisinde de fiyat yoktur ve iletişim alanları köşeli parantezlidir.
