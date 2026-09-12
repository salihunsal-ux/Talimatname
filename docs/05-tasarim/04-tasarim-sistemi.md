# Tasarım sistemi (v0 — geliştirme için token'lar)

Marka kaynağı: `marka/build_refined.py` (Talimatname · Mühür sistemi). Bu belge, tel-çerçevelerin yüksek doğruluklu tasarıma ve koda geçerken kullanacağı token'ları ve bileşen kurallarını tanımlar. Flutter'da `ThemeData`, web'de CSS değişkenleri olarak birebir taşınır.

## Renk

| Token | Açık tema | Koyu tema | Kullanım |
|---|---|---|---|
| `renk.zemin` | #f7f5ef (parşömen) | #15191c | Sayfa zemini |
| `renk.yuzey` | #ffffff | #1d2226 | Kart, liste, panel |
| `renk.yuzey2` | #efece4 | #262c31 | İkincil zemin, kutu |
| `renk.murekkep` | #1c2128 | #f1eee6 | Ana metin |
| `renk.murekkep2` | #4b5560 | #b5bcc4 | İkincil metin |
| `renk.sessiz` | #7b8590 | #8a9299 | Yardımcı metin, ikon |
| `renk.cizgi` | #d6d9d2 | #2f373d | Ayırıcı, kenarlık |
| `renk.marka` | #1f6f5b (defter yeşili) | #3fa98c | Birincil eylem, marka, "tamamlandı" |
| `renk.marka.acik` | #dcebe5 | #173a31 | Vurgu zemini |
| `renk.kritik` | #b8452f (mühür kızılı) | #e46f5a | Kritik, başarısız, kaçırıldı |
| `renk.kritik.acik` | #f3ddd8 | #3a201b | |
| `renk.uyari` | #b7791f | #e0a640 | Geç, tolerans, bekleyen |
| `renk.uyari.acik` | #f6ebd2 | #33290f | |
| `renk.pasif` | #c9ced6 | #3a424a | Kapalı gün, pasif |

Durum renkleri (marka/kritik/uyarı/pasif) yalnızca durum için; dekoratif kullanılmaz. Renk tek başına anlam taşımaz — her durumun ikonu ve etiketi vardır (NFR-11).

## Tipografi

| Rol | Yazı tipi | Boyut / ağırlık | Not |
|---|---|---|---|
| Marka wordmark | Bitter 700 | Logo dosyalarında; arayüz metninde kullanılmaz | |
| Başlık (mobil/web) | Sistem: SF Pro / Roboto / Segoe UI | 22 / 700 (ekran başlığı), 17 / 600 (bölüm) | Türkçe İ/ı için sistem yazı tipi |
| Gövde | Sistem | 16 / 400 (mobil), 14 / 400 (web) | Satır yüksekliği 1,45 |
| Etiket / meta | Sistem | 13 / 500, 12 / 400 | Büyük harf etiketlerde +0,06em aralık |
| Sayısal (sıcaklık, puan) | Sistem, tabular rakam | 28 / 700 | `font-variant-numeric: tabular-nums` |

Mobilde kullanıcı yazı boyutu ayarına saygı (dinamik tip); en büyük ayarda düzen bozulmaz (test: %130).

## Boşluk ve biçim

- Boşluk ölçeği: 4, 8, 12, 16, 24, 32 px. Kart iç boşluğu 16; liste satırı yüksekliği ≥ 56 (mobil).
- Köşe: kart 12, düğme 10, çip 999, kiosk avatar 14.
- Kenarlık 1 px `renk.cizgi`; gölge yalnızca yüzen öğelerde (bildirim kartı, alt sayfa).
- Dokunma hedefi ≥ 44 × 44; birincil eylem mobilde alt kenarda tam genişlik.

## Bileşenler (çekirdek)

| Bileşen | Kural |
|---|---|
| Durum çipi | İkon + metin; renk durum token'ından: tamamlandı ✓, geç ⏱, kaçırıldı ✕, kapalı –, planlı ○, devam ◐ |
| Liste satırı (madde) | Sol: 22 px durum kutusu; orta: başlık + tür çipi; sağ: meta (saat, değer); satır tamamı dokunulabilir |
| Sıcaklık girişi | Büyük sayı, ± adım (0,1), aralık göstergesi, aralık dışı → kritik renk ve açıklama |
| Kamera | Uygulama içi; deklanşör alt ortada; çekilen kareler şerit; "yalnızca kamera"da galeri simgesi yok |
| Yapılamadı sayfası | Alt sayfa (bottom sheet); sebep listesi büyük satırlar; "Diğer" seçilince not alanı açılır |
| Aksiyon kartı | Öncelik çipi sol üst, vade sağ üst (gecikince kritik renk), kaynak satırı, atanan avatarı |
| Izgara hücresi (web) | 22 px yüksek dolgu; hover'da tooltip (durum, saat, atanan); tıkla → detay |
| Kiosk kilit | Yatay; 3×N avatar ızgarası (≥ 96 px); PIN tuş takımı sağda |
| Boş durum | İkon + tek cümle + ilk eylem düğmesi |
| Bildirim kartı (sistem) | Uygulama ikonu (mühür), başlık = liste adı, gövde = pencere/son saat |

## İkonografi

Çizgi ikon seti (2 px, 24 px ızgara); durum ikonları dolu. Marka işareti (sayfa + mühür) yalnızca uygulama ikonu, giriş ekranı ve PDF başlığında; arayüz içinde tekrarlanmaz. Emoji kullanılmaz.

## PDF çıktıları

Markalı başlık (zincir logosu + "Talimatname ile oluşturuldu" alt bilgisi), sayfa numarası, her sayfada doğrulama kodu ve üretim zamanı; kanıt küçük resimleri 3 sütun; sıcaklık günlüğü tablo + mini grafik; renk baskıda siyah-beyaz okunur (durumlar ikonla).

## Hareket

Yalnızca geçiş ve geri bildirim: madde tamamlanınca 150 ms tik animasyonu; senk rozeti dönen ok; `prefers-reduced-motion` saygı. Süslü animasyon yok.

## Erişilebilirlik kontrol listesi

Kontrast ≥ 4,5:1 (metin), ≥ 3:1 (ikon); odak halkası görünür (web); ekran okuyucu etiketleri tüm ikon düğmelerinde; dinamik yazı boyutu; tek elle ulaşılabilir birincil eylem; sesli geri bildirim yok (gürültülü ortam).
