# Doğrulama sprinti planı (12 hafta)

Amaç: fizibilitenin üç belirsiz girdisini — ödeme isteği, benimseme, edinme hızı — sahadan ölçmek ve üç kapıdan geçmek. Yöntem ve sorular: [Pilot görüşme rehberi](../02-pilot-gorusme-rehberi.html). Çalışma ürünü değil, **kanıt** üretir: 20 görüşme notu, 8 gözlem, isim testi tepkileri, 5 LOI, 3 pilot.

Takvim (1 Ekim 2026'da yeniden kuruldu): hafta 0 = 28 Eylül–2 Ekim (ilan ve ilk ulaşım) · **hafta 1 = 5 Ekim** · K1 26 Ekim · K2 23 Kasım · pilot hazırlığı Aralık · K3 ölçümü Şubat 2027 (Alfa 22 Ocak). Geliştirme takvimi: 07-gelistirme/05 §1.

## Kapılar

| Kapı | Hafta | Ölçüt | Geçmezse |
|---|---|---|---|
| K1 | 4 | 20 görüşmeden ≥ 12'si "liste ≥ 2 ve acı ≥ 2" puanı (rubrik) | 4 hafta uzat, örneklemi değiştir (format/model); 8. haftada da tutmazsa dur |
| K2 | 8 | ≥ 5 ücretli pilot niyet mektubu (LOI) | Fiyat/paket revizyonu; 2 hafta uzat; ≤ 2 LOI ise dur |
| K3 | 12 (+8 hafta pilot) | 3 pilotta 4. hafta tamamlanma ≥ %80; ≥ 2 yıllık sözleşme | Kök neden (cihaz/alışkanlık/fiyat/ürün); fizibilite 24. ay kapısından bağımsız erken durdurma sinyali |

Karar kuralı: üç kapıdan ikisi tutmazsa proje burada biter (fizibilite §10). Bu kural sprint başında yazılıdır, sonda tartışılmaz.

## Haftalık plan

| Hafta | Odak | Yapılacaklar | Çıktı |
|---|---|---|---|
| 0 (hazırlık) | Kit | Hedef liste onayı (01), ulaşım mesajları (02), not şablonu ve puanlama betiği (03), prototip (05-tasarim/05-prototip), kanıt raporu örnekleri — basılı (05-tasarim/06-kanit-raporu), 8 şablonun madde listeleri (02-urun/07), isim kartları (logo tuvali), LOI (04) | Kit hazır; ilk 30 ulaşım mesajı gitti |
| 1 | Ulaşım + ilk görüşmeler | 40 ulaşım (LinkedIn/e-posta/tanıştırma); hedef 5 randevu; ilk 2–3 görüşme; notlar aynı gün | 3 not, puanlama tablosu dolmaya başladı |
| 2 | Görüşme | 4–5 görüşme; ilk şube ziyareti; haftalık rapor #1 | 8 not, 1 gözlem |
| 3 | Görüşme + prototip testi | 4–5 görüşme (Blok 8 prototip + isim kartları devrede); 2 gözlem — ilk **saha kiosk denemesi** (07, tabletle kapanış); fiyat testi cevapları toplanıyor | 13 not, 3 gözlem, 1 kiosk denemesi |
| 4 | **K1** | 4–5 görüşme; K1 sayımı; örneklem dengesi kontrolü (format/model/büyüklük); K1 kararı; 2. kiosk denemesi; haftalık rapor | 17–20 not; K1 raporu |
| 5 | LOI turu | En yüksek uyum puanlı 8 zincire LOI teklifi; ikinci görüşme (karar vericiyle); 2 gözlem | LOI görüşmeleri |
| 6 | LOI turu | LOI imzaları; fiyat testi analizi (van Westendorp); 3. kiosk denemesi → kiosk kararı (07 karar kuralı); ürün kararlarının güncellenmesi (kiosk, barındırma, prob, franchise) | ≥ 3 LOI; karar güncellemeleri |
| 7 | LOI + pilot hazırlığı | Kalan LOI'ler; 3 pilot seçimi (uyum puanı + çeşitlilik); veri işleme sözleşmesi; şube/personel Excel'i | ≥ 5 LOI hedefi |
| 8 | **K2** | K2 sayımı ve kararı; pilot kurulum planı; Alfa/Beta takvimiyle hizalama (S6 Alfa) | K2 raporu; 3 pilot sözleşmesi |
| 9–12 | Pilot ön hazırlık ve paralel iş | Pilot zincirlerde şablon uyarlaması (9 şablon), tablet envanteri, aydınlatma metni; geliştirme Alfa'ya kadar sürer; isim testi sonucu → kesin isim kararı (ADR) | Pilot hazır; isim kararı |
| Pilot (8 hafta, Alfa/Beta ile) | **K3** | 06-test/05 UAT planı | K3 raporu; yıllık sözleşmeler |

Not: K3, yazılım Alfa/Beta'ya ulaşınca ölçülür (S6–S8); sprintin 9–12. haftaları geliştirmeyle paralel hazırlıktır. Görüşmeler geliştirmeyi beklemez.

## Haftalık ritim

- **Pazartesi 30 dk:** haftanın randevuları, ulaşım hedefi, örneklem dengesi (aşağıdaki tablo).
- **Her görüşmeden sonra 10 dk:** not formu (03) doldurulur, `puanla.py` çalıştırılır, kapı sayacı güncellenir.
- **Cuma 30 dk:** haftalık rapor (07 şablonu) → depoya commit; karar gerektiren bulgular → ADR/karar günlüğü.
- **Her 2 görüşmeye 1 şube ziyareti** (rehber §07 gözlem listesi); 3 ziyaret tabletli kiosk denemesi (07).

## Örneklem dengesi (20 görüşme)

| Boyut | Hedef | Kaynak |
|---|---|---|
| 5–15 şube | 6 | 01-hedef-liste "A" |
| 16–50 şube | 9 | "B" |
| 51–100 şube | 5 | "C" |
| Format: kafe / hızlı servis-fırın / restoran | 7 / 7 / 6 | |
| Model: kendi işlettiği / karma / ağırlıkla franchise | 8 / 8 / 4 | |
| İstanbul dışı merkezli | ≥ 5 | |

Haftalık kontrol: bir kutu hedefinin %150'sini aşarsa o kutudan yeni randevu alınmaz.

## Roller

| Rol | Kim | Sorumluluk |
|---|---|---|
| Sprint sahibi | Kurucu (PO) | Ulaşım, görüşme, karar |
| Not tutan / ikinci görüşmeci | İkinci kişi (ortak veya danışman) | Not, zaman, puanlama uzlaşısı; yoksa görüşme kaydı (izinle) + aynı gün not |
| Analiz | Claude (bu depo) | Notların birleştirilmesi, kapı sayımı, fiyat analizi, karar güncellemeleri, haftalık rapor taslağı |
| Prototip/tasarım | Claude + tasarımcı | Prototip düzeltmeleri (görüşme bulgularına göre, haftada bir) |

## Riskler

| Risk | Belirti | Önlem |
|---|---|---|
| Randevu alınamıyor | 1. hafta sonunda < 3 randevu | Tanıştırma kanalını öne al (POS/İK yazılımı ortakları, UFRAD), mesajı "ürün" değil "dinlemek" olarak yeniden yaz, İstanbul dışı zincirlere yönel |
| Görüşmeler "harika fikir"le bitiyor | Taahhüt puanı ≤ 1 | Blok 8'de LOI'yi masaya koymak zorunlu; fiyatı ürün göstermeden sormak |
| Tek profil | Örneklem tablosu dengesiz | Haftalık kontrol; kutu doluysa randevu alma |
| Karar verici yok | Yetki puanı 0 | İkinci görüşmeyi karar vericiyle şart koş; LOI'yi ancak ona sun |
| Not kaybı | Ertesi güne kalan not | 10 dakika kuralı; kayıt izni; not şablonu telefondan doldurulabilir |
| Kendi tezimizi onaylatma | Yönlendirici sorular | Rehber §11 hata listesi; ikinci görüşmeci her görüşmede bir "kötü sinyal" yazmak zorunda |

## Bütçe

Fizibilite: ≈ 6.500 $ (≈ ₺316 bin): seyahat/şube ziyareti, prototip düzenlemesi, LOI hukuk incelemesi (1 saat), ulaşım aracı abonelikleri (LinkedIn), küçük hediye/ikram. Geliştirici maliyeti bu bütçede değil (Sprint 0–3 paralel).
