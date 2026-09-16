# Tanıtım broşürü (A4, 2 sayfa) ve ekran tasarımları

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
