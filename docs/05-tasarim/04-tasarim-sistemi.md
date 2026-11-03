# Tasarım sistemi (v1 — web panelinde uygulandı)

Marka kaynağı: `marka/build_refined.py` (Talimatname · Mühür sistemi).

**Durum.** v0'da bu belge yalnızca bir token listesiydi; artık web paneli bu
token'ların üstüne kurulu ve belge kodun **tek kaynağı**. Değer değişikliği
önce burada, sonra `web/src/styles/tokens.css` içinde yapılır. Mobil
(Flutter) henüz yazılmadı (ADR-0013 Faz B); bu belgenin mobil satırları hâlâ
hedef, uygulanan değil.

| Katman | Dosya | Durum |
|---|---|---|
| Token | `web/src/styles/tokens.css` | Uygulandı |
| Bileşen | `web/src/styles/bilesenler.css` | Uygulandı |
| React bileşenleri | `web/src/bilesenler/` (`Alan`, `Cip`, `Dugme`, `Kabuk`, `Kart`, `Marka`) | Uygulandı |
| Flutter `ThemeData` | — | Yazılmadı |

## v1'de ne değişti

Dört karar; hepsi çalışan panele bakılarak alındı, maket üstünde değil.

| Karar | Gerekçe |
|---|---|
| **Koyu çapa yüzeyi** eklendi (`renk.koyu` ailesi): üst bant, giriş paneli, pano manşeti | Panel baştan sona açık parşömendi; hiyerarşi yoktu ve ürün "operasyon aracı" değil "form sayfası" gibi duruyordu. Zemini değiştirmek yerine sayfanın **ağırlık merkezine** koyu bir yüzey kondu |
| **Birincil düğme mürekkep rengine** çevrildi (eskiden marka yeşili) | Yeşil hem eylemi hem "tamamlandı" durumunu hem bağlantıyı gösteriyordu; sayfadaki her yeşil tıklanabilir sanılıyordu. Yeşil artık yalnızca **vurgu**: bağlantı, seçili bölüm, başarılı durum |
| `renk.sessiz` koyulaştırıldı (#7b8590 → **#636e79**) | Eski değer parşömen üstünde 3,44:1 veriyordu; NFR-11 metin için 4,5:1 istiyor. Yeni değer 4,77:1 |
| **Marka işareti** (sayfa + mühür) koda alındı: `Marka.tsx`, koyu zemin sürümüyle | Giriş ekranı ve üst bant isimsiz bir metin satırıyla açılıyordu. İşaret isimden bağımsız çizildi — isim testi hangi sonucu verirse versin işaret kalır, yanındaki yazı değişir |

Seçili hâl artık **erişilebilirlik özniteliğinden** türüyor
(`[aria-pressed]`, `[aria-selected]`, `[aria-current]`), ayrı bir `secili`
prop'undan değil: ekran okuyucuyla göz aynı kaynağı okusun. Ayrı prop
ikisinin sessizce ayrışmasına açık kapı bırakıyordu — nitekim düğmelerin
bileşen katmanına taşınması sırasında beş yerde görsel seçili hâl düşmüş,
bunu testler değil ekrana bakmak yakalamıştı.

Aynı kural **bağlı vurgulara** da uzanıyor: pano ızgarasında açık detayın
satırı `tr:has(.izgara-hucre[aria-pressed='true'])` ile işaretleniyor, yani
hücrenin kendi ARIA durumundan. İkinci bir "seçili satır" bayrağı tutmak,
ayrışmayı bir kez daha davet ederdi.

## Renk

### Tema renkleri

| Token | Açık tema | Koyu tema | Kullanım |
|---|---|---|---|
| `renk.zemin` | #f7f5ef (parşömen) | #15191c | Sayfa zemini |
| `renk.yuzey` | #ffffff | #1d2226 | Kart, liste, panel |
| `renk.yuzey2` | #efece4 | #262c31 | İkincil zemin, kutu, hover |
| `renk.murekkep` | #1c2128 | #f1eee6 | Ana metin |
| `renk.murekkep2` | #4b5560 | #b5bcc4 | İkincil metin |
| `renk.sessiz` | **#636e79** | #8a9299 | Yardımcı metin, ikon |
| `renk.cizgi` | #d6d9d2 | #2f373d | Ayırıcı, kenarlık |
| `renk.marka` | #1f6f5b (defter yeşili) | #3fa98c | **Vurgu**: bağlantı, seçili bölüm, "tamamlandı", odak halkası |
| `renk.marka.acik` | #dcebe5 | #173a31 | Vurgu zemini |
| `renk.kritik` | #b8452f (mühür kızılı) | #e46f5a | Kritik, başarısız, kaçırıldı |
| `renk.kritik.acik` | #f3ddd8 | #3a201b | |
| `renk.uyari` | #b7791f | #e0a640 | Geç, tolerans, bekleyen |
| `renk.uyari.acik` | #f6ebd2 | #33290f | |
| `renk.pasif` | #c9ced6 | #3a424a | Kapalı gün, pasif, devre dışı düğme |

### Koyu çapa yüzeyi

Temadan **bağımsız** ikinci bir yüzey. Açık temada da koyu, koyu temada bir
tık daha koyu; üstündeki metin ve vurgu ayrı token, çünkü açık tema renkleri
bu zeminde okunmuyor.

| Token | Açık tema | Koyu tema | Kullanım |
|---|---|---|---|
| `renk.koyu` | #16201d | #0f1416 | Üst bant, giriş paneli, pano manşeti, birincil düğme |
| `renk.koyu.murekkep` | #f1eee6 | #f1eee6 | Koyu yüzeyde metin |
| `renk.koyu.sessiz` | #9aa2a8 | #9aa2a8 | Koyu yüzeyde yardımcı metin |
| `renk.koyu.marka` | #3fa98c | #3fa98c | Koyu yüzeyde vurgu (açık tema yeşili burada okunmuyor) |

Kural: bir ekranda **en fazla bir** koyu çapa alanı — üst bant hariç. İkinci
bir çapa hiyerarşiyi yok eder; çapanın işi "önce buraya bak" demek.

Durum renkleri (marka/kritik/uyarı/pasif) yalnızca durum için; dekoratif
kullanılmaz. Renk tek başına anlam taşımaz — her durumun ikonu ve etiketi
vardır (NFR-11).

## Tipografi

| Rol | Token | Boyut / ağırlık | Not |
|---|---|---|---|
| Marka wordmark | — | Bitter 700, logo dosyalarında | Arayüz metninde kullanılmaz |
| Vaat başlığı (giriş paneli) | — | 34 / 700, aralık −0,025em | Yalnızca giriş; ≤860 px'te `baslik.ekran`'a iner |
| Manşet sayı (pano) | — | 44 / 700, tabular | Sayfada tek tane |
| Ekran başlığı | `baslik.ekran` | 22 / 700 | |
| Bölüm başlığı | `baslik.bolum` | 17 / 600 | |
| Gövde | `govde` | 14 / 400 (web), 16 (mobil hedefi) | Satır yüksekliği 1,45 |
| Etiket | `etiket` | 13 / 500–600 | Çip, küçük düğme |
| Meta | `meta` | 12 / 400 | Büyük harf etiketlerde +0,08–0,12em aralık |
| Sayısal | — | tabular rakam | `font-variant-numeric: tabular-nums` |

Yazı tipi yığını: `'Segoe UI', 'SF Pro Text', Roboto, system-ui, sans-serif`
— Türkçe İ/ı için sistem yazı tipi.

**Açık iş:** vaat başlığı (34) ve manşet sayı (44) `bilesenler.css` içinde
düz sayı olarak duruyor, token değil. İkisi de tek yerde kullanıldığı için
şimdilik kabul edildi; üçüncü bir kullanım çıkarsa token'a taşınır.

Mobilde kullanıcı yazı boyutu ayarına saygı (dinamik tip); en büyük ayarda
düzen bozulmaz (hedef test: %130). *Mobil yazılmadığı için bu henüz
sınanmadı.*

## Boşluk ve biçim

- Boşluk ölçeği: **4, 8, 12, 16, 24, 32** px (`bosluk.1`…`bosluk.8`; 20 ve 28
  bilerek yok — ara değer isteyen bir yerleşim, yanlış yerleşimdir).
- Kart iç boşluğu 16; içerik alanı 24, ≥1200 px'te 32, ≤720 px'te 16.
- İçerik genişliği en çok **1120 px**.
- Köşe: kart 12 (`kose.kart`), düğme 10 (`kose.dugme`), çip 999 (`kose.cip`).
- Kenarlık 1 px `renk.cizgi`; gölge yalnızca yüzen öğelerde
  (`golge.yuzen` = `0 6px 24px rgb(28 33 40 / 12%)`).
- Dokunma hedefi ≥ 44 × 44 (`button` ve `a` için genel kural). Tek istisna
  `dugme--kucuk` (32 px, yoğun tablolarda satır içi eylem) — ≤720 px'te o da
  44'e çıkar: küçük hedef masaüstünde sorun değil, parmakta sorun.

## Kırılma noktaları

| Nokta | Ne olur |
|---|---|
| ≥ 1200 px | İçerik dolgusu 24 → 32 |
| ≤ 860 px | Giriş paneli üste geçer ve kısalır (açıklama + maddeler gizlenir); telefonda ilk görülmesi gereken şey **form** |
| ≤ 720 px | Yan menü yatay kaydırılan şeride iner, üst banttaki alt başlık gizlenir, içerik dolgusu 16, küçük düğmeler 44 px |

Panel şube müdürü tarafından telefondan da açılıyor; "web = masaüstü"
varsayımı yok.

## Bileşenler

### Uygulanan (web)

| Bileşen | Sınıf / dosya | Kural |
|---|---|---|
| Düğme | `.dugme` + `--birincil` / `--ikincil` / `--sessiz` / `--tam` / `--kucuk` | Birincil = `renk.koyu`; seçili hâl ARIA özniteliğinden; devre dışı `renk.pasif` |
| Alan | `.alan`, `.alan-sarmal`, `.alan-etiket`, `.alan-ipucu`, `.alan--kod` | Etiket her zaman görünür — placeholder etiket yerine geçmez |
| Durum çipi | `Cip.tsx` (`marka` / `kritik` / `uyari` / `pasif` / `nötr`) | İkon + metin; renk tek başına anlam taşımaz |
| Kart | `.kart`, `.kart--yuzen` | Gölge yalnızca yüzen sürümde |
| Bildiri | `.bildiri` + `--hata` / `--saglam` / `--uyari` | `role="status"` veya `role="alert"` ile |
| Kabuk | `.kabuk-bant` (koyu), `.kabuk-menu`, `.kabuk-icerik` | Üst bant yapışkan ve koyu; banttaki ikincil düğme koyu zemine göre yeniden renklenir |
| Sayfa başlığı | `.sayfa-basligi`, `-alt`, `-denetimler`, `-denetim` | Başlık + alt başlık solda, sayfanın kendi denetimleri sağda ve **etiketleri üstünde**; altında ince ayraç |
| Giriş | `.giris`, `.giris-panel`, `.giris-form` | İki bölüm: solda koyu panel (ürün ne yapar), sağda form |
| Marka işareti | `Marka.tsx` | Sayfa + mühür; `koyu` sürümü koyu zemin için |
| Pano özeti | `.ozet-serit`, `.ozet-manset`, `.ozet-kutu` | Bir manşet (koyu, 44 px) + yan yana küçük sayılar — altı özdeş kutu değil |
| Tablo | `.tablo`, `td.sayisal`, `.tablo-kaydirma` | Sayısal sütunlar sağa yaslı ve tabular; dolgu sınıftan gelir, satır içi yazılmaz |
| Izgara tablosu | `.tablo--izgara` | Sütunlar içeriği kadar — tam genişlik tablo, iki sütunu sayfanın iki ucuna düşürüp aradaki bağı koparıyordu |
| Liste satırı | `.liste-satiri` | Satırın tamamı tıklanabilir; seçili hâl `aria-current` |
| Izgara hücresi | `.izgara-hucre` | Pano ızgarası; tıkla → detay. Seçili hücre **çerçeveden** okunur: zemin durumu anlatıyor |
| Boş durum | `.bos-durum` | İkon + tek cümle + ilk eylem |
| Araç çubuğu | `.arac-cubugu`, `--sag` | Başlık satırı + eylemler |
| Veri listesi | `.veri-liste` (dl) | Ad/değer çiftleri |

Düz CSS; yardımcı sınıf (utility) çerçevesi yok. Bileşen katmanı küçük ve
adları Türkçe, çünkü belgelerle kod aynı sözlüğü kullanıyor.

### Henüz yazılmadı (mobil hedefi)

| Bileşen | Kural |
|---|---|
| Sıcaklık girişi | Büyük sayı, ± adım (0,1), aralık göstergesi, aralık dışı → kritik renk ve açıklama |
| Kamera | Uygulama içi; deklanşör alt ortada; çekilen kareler şerit; "yalnızca kamera"da galeri simgesi yok |
| Yapılamadı sayfası | Alt sayfa (bottom sheet); sebep listesi büyük satırlar; "Diğer" seçilince not alanı açılır |
| Aksiyon kartı (mobil) | Öncelik çipi sol üst, vade sağ üst (gecikince kritik renk), kaynak satırı, atanan avatarı |
| Kiosk kilit | Yatay; 3×N avatar ızgarası (≥ 96 px); PIN tuş takımı sağda |
| Bildirim kartı (sistem) | Uygulama ikonu (mühür), başlık = liste adı, gövde = pencere/son saat |

## İkonografi

Çizgi ikon seti (2 px, 24 px ızgara); durum ikonları dolu. Marka işareti
(sayfa + mühür) yalnızca uygulama ikonu, giriş ekranı, üst bant ve PDF
başlığında; içerik alanında tekrarlanmaz. Emoji kullanılmaz.

## PDF çıktıları

Markalı başlık (zincir logosu), sayfa numarası, her sayfada doğrulama kodu ve
üretim zamanı; alt bilgi `zincir · Talimatname · zaman` (zincir adı ürün
adıyla aynıysa tekrarlanmaz); kanıt küçük resimleri 3 sütun; sıcaklık günlüğü
tablo + mini grafik; renk baskıda siyah-beyaz okunur (durumlar ikonla).
Uygulama: `api/src/talimatname/services/pdf.py`.

## Hareket

Yalnızca geçiş ve geri bildirim: düğme hover/odak 120 ms, basılı hâlde 1 px
iniş; madde tamamlanınca 150 ms tik; senk rozeti dönen ok.
`prefers-reduced-motion: reduce` altında geçişler ve basma hareketi kapanır.
Süslü animasyon yok.

## Erişilebilirlik

Hedef: metin ≥ 4,5:1, ikon ve kenarlık ≥ 3:1 (NFR-11). Odak halkası görünür
(`:focus-visible`, 2 px `renk.marka`); ekran okuyucu etiketleri tüm ikon
düğmelerinde; `.sr-only` yardımcı sınıfı mevcut.

### Ölçülen kontrast (açık tema)

| Çift | Oran | |
|---|---|---|
| `murekkep` / parşömen | 14,84:1 | ✓ |
| `murekkep2` / parşömen | 6,96:1 | ✓ |
| `sessiz` / parşömen | 4,77:1 | ✓ |
| `sessiz` / `yuzey2` | 4,41:1 | ✕ |
| `marka` / parşömen (bağlantı) | 5,53:1 | ✓ |
| Birincil düğme yazısı | 14,39:1 | ✓ |
| Çip **marka** (yazı/zemin) | 4,90:1 | ✓ |
| Çip **nötr** | 6,43:1 | ✓ |
| Çip **pasif** | 4,41:1 | ✕ |
| Çip **kritik** | 4,11:1 | ✕ |
| Çip **uyarı** | 3,07:1 | ✕ |

Koyu çapa yüzeyinde: metin 14,39:1, yardımcı metin 6,44:1, vurgu 5,77:1 —
hepsi geçiyor.

**Dört satır hedefin altında**, en kötüsü uyarı çipi (3,07:1). Çip yazısı
13 px / 600 ağırlık, yani WCAG'in "büyük metin" istisnasına girmiyor; bu
gerçek bir açık. Buraya yazılıyor çünkü v0'ın "kontrast ≥ 4,5:1" satırı
sınanmamış bir iddiaydı — ölçünce tutmadığı görüldü.

Devre dışı düğme (`renk.pasif` üstünde beyaz yazı) kontrast ölçütünün
dışındadır (WCAG 1.4.3, devre dışı denetim istisnası).

## Açık işler

| # | İş | Not |
|---|---|---|
| A-1 | Çip renklerini 4,5:1'e çıkar (uyarı, kritik, pasif) | Yazı rengini koyulaştırmak yetiyor; ama zemin token'ları durum ızgarasında ve PDF'te de kullanıldığı için önce oraya bakılmalı |
| A-2 | Koyu temayı en az bir ekranda sına | Token'lar tanımlı, hiçbir ekranda açılıp bakılmadı — bugün açılsa ne olacağını bilmiyoruz |
| A-3 | Şablon editörü ve plan formuna v1 dilini yay | En yoğun iki ekran, hâlâ ızgarasız |
| A-4 | Tablo ritmi: satır yüksekliği, ayraç, sayısal hiza | Pano ızgarası sınıf katmanına geçti; kalan tablolar hâlâ kendi satır içi dolgularını yazıyor |
| A-5 | İskelet yükleme (skeleton) | Belgede yazılı, hiç uygulanmadı |
| A-6 | Marka wordmark | İsim testi sonucuna bağlı (bkz. `01-strateji/03-isim-ve-marka.md`) |
