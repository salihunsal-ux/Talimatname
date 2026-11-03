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
| **Birincil düğme mürekkep rengine** çevrildi (eskiden marka yeşili) | Yeşil hem eylemi hem "tamamlandı" durumunu hem bağlantıyı gösteriyordu; sayfadaki her yeşil tıklanabilir sanılıyordu. Yeşil artık yalnızca **vurgu**: bağlantı, seçili bölüm, başarılı durum. Kural "mürekkep" değil **"sayfanın tersi"**: koyu temada krem hap (A-2) |
| **Devre dışı düğmenin yazısı okunur hâle geldi** | Yazı rengi `renk.yuzey` idi: her iki temada 1,58:1. Kurulum sihirbazında "neyin eksik olduğunu" söyleyen düğme buydu. Şimdi 3,6:1 — metin eşiğinin altında (standart devre dışı denetimi muaf tutuyor) ama okunuyor |
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

Kutulu denetimlerde kaynak ARIA değil, kutunun kendi hâli:
`.secim-cipi:has(input:checked)`. Plan formundaki gün ve şube çipleri
seçili görünümü JS'teki bir listeden hesaplayan bir stil üretecinden
alıyordu — aynı ayrışma kapısı, başka kılıkta.

## Renk

### Tema renkleri

| Token | Açık tema | Koyu tema | Kullanım |
|---|---|---|---|
| `renk.zemin` | #f7f5ef (parşömen) | #15191c | Sayfa zemini |
| `renk.yuzey` | #ffffff | #1d2226 | Kart, liste, panel |
| `renk.yuzey2` | #efece4 | #262c31 | İkincil zemin, kutu, hover |
| `renk.murekkep` | #1c2128 | #f1eee6 | Ana metin |
| `renk.murekkep2` | #4b5560 | #b5bcc4 | İkincil metin |
| `renk.sessiz` | **#5b6670** | **#929aa1** | Yardımcı metin, ikon |
| `renk.cizgi` | #d6d9d2 | #2f373d | Ayırıcı, kenarlık |
| `renk.marka` | #1f6f5b (defter yeşili) | **#45b394** | **Vurgu**: bağlantı, seçili bölüm, "tamamlandı", odak halkası |
| `renk.marka.acik` | #dcebe5 | #173a31 | Vurgu zemini |
| `renk.kritik` | **#a63d29** (mühür kızılı) | #e46f5a | Kritik, başarısız, kaçırıldı |
| `renk.kritik.acik` | #f3ddd8 | #3a201b | |
| `renk.uyari` | **#8c5d16** | #e0a640 | Geç, tolerans, bekleyen |
| `renk.uyari.acik` | #f6ebd2 | #33290f | |
| `renk.pasif` | #c9ced6 | #3a424a | Kapalı gün, pasif, devre dışı düğme |

Kalın yazılanlar A-1'de koyulaştı. Durum renkleri kendi açık zeminlerinin
üstünde okunmak zorunda ve beşi birden 4,5:1'in altındaydı: uyarı çipi
**3,07:1**, kritik 4,11:1, pasif 4,41:1, koyu temada marka 4,31:1 ve pasif
4,47:1. En kötüsü uyarıydı ve yalnızca çipte değil **her yerde**: beyaz
üstünde 3,64:1, yani "kaydedilmemiş değişiklik" uyarısı ve kanıt bayrakları
da okunaksızdı. Sayılar artık `web/src/styles/kontrast.test.ts` ile ölçülüyor
— yirmi bir çift, iki tema. Elle doğrulamak işe yaramamıştı: renkler
"yakışıyordu" ve üç çift aylarca altında kaldı.

Durum çifti (metin + zemin) **tek yerde** yazılı: `.durum--marka`,
`--kritik`, `--uyari`, `--pasif`, `--notr`, `--bos`. Çip (`.cip`) ve pano
ızgarası (`.izgara-hucre`) bu sınıfları paylaşıyor, biçimleri kendilerinin.
Önce iki kopya vardı — `Cip.tsx` içindeki `RENKLER` haritası ve panonun
`HUCRE`'si — ve ikisi de satır içi stil üretiyordu.

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
| `renk.koyu.cizgi` | #16201d (= yüzeyin kendisi, görünmez) | **#324039** | Çapanın kenarı |
| `renk.birincil.zemin` | #16201d | **#f1eee6** | Birincil düğme zemini |
| `renk.birincil.yazi` | #f1eee6 | **#15191c** | Birincil düğme yazısı |

**Çapa koyu temada yüzeyiyle ayrılamıyor.** Açık temada sayfadan 15,3:1
uzakta; koyu temada sayfa da koyu olduğu için 1,05:1 kalıyordu — üst bant,
giriş paneli ve pano manşeti zeminden ayrılmıyordu. Daha koyuya gitmek
mümkün değil, sayfa zaten siyaha yakın. Ayrım artık **kenardan**: çapa bir
tık yükseldi (#0f1416 → #1e2a26) ve `renk.koyu.cizgi` ile çevrelendi — açık
temanın kartları 1,43:1'lik bir çizgiyle ayırmasının aynısı. Kural:
*çapa, sayfadan ya yüzeyiyle (≥3:1) ya da kenarıyla (≥1,25:1) ayrılır.*

**Birincil düğme sayfanın tersi.** Zemini çapa yüzeyiydi, dolayısıyla koyu
temada sayfadan 1,05:1 ayrılıyordu: birincil eylemin kutu biçimi yoktu,
yalnızca yazısı duruyordu. Artık kendi rol token'ı var ve her iki temada
sayfadan ~15:1 uzakta — açık temada mürekkep hapı (15,31), koyu temada krem
hap (15,25). Yeşil iki temada da vurgu olarak kalıyor.

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
| Alan | `.alan`, `.alan-sarmal`, `.alan-etiket`, `.alan-ipucu`, `.alan--kod`, `--sayi`, `--saat`, `--dar`, `--orta`, `--genis` | Etiket her zaman görünür — placeholder etiket yerine geçmez. Sayı ve saat kutuları içeriği kadar; `.alan` varsayılanı tam genişlik |
| Alan grubu | `.alan-grubu` (fieldset + legend), `.alan-sirasi` | Uzun form bölümlere ayrılır; grup hem gözle hem ekran okuyucuyla okunan bir sınır. Alanlar **alt** kenarlarından hizalanır |
| Seçim çipi | `.secim-cipi` | Çoktan seçmeli etiket (gün, şube). Seçili hâl `:has(input:checked)` ile kutunun kendisinden türer; dar ekranda 44 px |
| Durum çipi | `Cip.tsx` (`marka` / `kritik` / `uyari` / `pasif` / `nötr`) | İkon + metin; renk tek başına anlam taşımaz |
| Kart | `.kart`, `.kart--yuzen` | Gölge yalnızca yüzen sürümde |
| Bildiri | `.bildiri` + `--hata` / `--saglam` / `--uyari` | `role="status"` veya `role="alert"` ile |
| Kabuk | `.kabuk-bant` (koyu), `.kabuk-menu`, `.kabuk-icerik` | Üst bant yapışkan ve koyu; banttaki ikincil düğme koyu zemine göre yeniden renklenir |
| Sayfa başlığı | `.sayfa-basligi`, `-alt`, `-denetimler`, `-denetim` | Başlık + alt başlık solda, sayfanın kendi denetimleri sağda ve **etiketleri üstünde**; altında ince ayraç |
| Giriş | `.giris`, `.giris-panel`, `.giris-form` | İki bölüm: solda koyu panel (ürün ne yapar), sağda form |
| Marka işareti | `Marka.tsx` | Sayfa + mühür; `koyu` sürümü koyu zemin için |
| Pano özeti | `.ozet-serit`, `.ozet-manset`, `.ozet-kutu` | Bir manşet (koyu, 44 px) + yan yana küçük sayılar — altı özdeş kutu değil |
| Tablo | `.tablo`, `td.sayisal`, `td.eylem`, `th[scope=row]`, `.tablo-kaydirma` | Sayısal sütunlar sağa yaslı ve tabular; dolgu sınıftan gelir, satır içi yazılmaz. Satır başlığı **anlamca `th`, ölçüce `td`** |
| Izgara tablosu | `.tablo--izgara` | Sütunlar içeriği kadar — tam genişlik tablo, iki sütunu sayfanın iki ucuna düşürüp aradaki bağı koparıyordu |
| Liste satırı | `.liste-satiri`, `--durgun` | Satırın tamamı tıklanabilir; seçili hâl `aria-current`. `--durgun` aynı ölçüler, hâlleri kapalı |
| Liste–detay | `.liste-detay`, `-kenar` | Kenarda seçilecekler, gövdede seçilen; ≤ 860 px'te tek sütun |
| Bölüm etiketi | `.bolum-etiketi` | Küçük, aralıklı, büyük harf: içerik değil, **içeriğin adı** |
| Madde satırı | `.madde-satiri`, `-ad`, `-eylem` | Şablon editörü; eylemler sağa toplanır, soldakiler maddeyi anlatır |
| Eylem şeridi | `.eylemler` | Bir kartın ya da formun altındaki düğme dizisi |
| Izgara hücresi | `.izgara-hucre` | Pano ızgarası; tıkla → detay. Seçili hücre **çerçeveden** okunur: zemin durumu anlatıyor |
| Boş durum | `.bos-durum` | İkon + tek cümle + ilk eylem |
| Veri listesi | `.veri-liste` (dl) | Ad/değer çiftleri |
| Bölüm başlığı | `.bolum-basligi` (h2 + p) | `.sayfa-basligi`ın sayfa içindeki karşılığı: başlık + bir satır açıklama |
| Sekme / adım şeridi | `.sekme-serit` | Sekmede `aria-selected`, sihirbaz adımında `aria-current="step"`; `ol` üzerinde de kullanılır |
| Yığın | `.yigin`, `--dar` | Dikey ritim `gap`ten; çocuğun kendi kenar boşluğu sıfırlanır (kural dosyanın **sonunda** durmalı) |
| Liste yığını | `.liste-yigin` (ul) | İşaretsiz dikey liste; satırlar `.liste-satiri` ya da `.kart` |
| Madde listesi | `.madde-listesi` | Gerçek madde işaretli liste (sihirbaz özeti) |
| Kart şeridi | `.kart-serit`, `-ad` | Çipler + ad + sağdaki durum; `.kart-ustu` künye içindir (metin, taban hizası) |
| Kutu ızgarası | `.kutu-izgara` + `.kutu` | Sayaç kutuları; pano manşetinden farkı: hepsi eşit ağırlıkta |
| Kanıt ızgarası | `.kanit-izgara`, `-gorsel`, `-yer`, `-alt`, `-bayrak` | Açılamayan görsel kırık simge değil, ne olduğunu söyleyen kutu |
| Onay etiketi | `.onay-etiketi` | Kutu + metin; süzgeç satırının sade seçeneği (çerçeveli `.secim-cipi` değil), 44 px |
| Süzgeç şeridi | `.suzgec-serit` | Başlık altında, sayfanın tamamını süzen denetimler |
| Satır eylemi | `.satir-eylem` | Tablo hücresindeki düğme dizisi, sağa yaslı |
| Vade | `.vade-metni`, `--gecikmis` | Renk tek başına anlam taşımıyor: metin de "3 saat gecikti" diyor |
| Durum metni | `.durum-metni`, `Durum.tsx` (`Yukleniyor`, `Hata`) | Yükleniyor sessiz bir satır, hata `.bildiri--hata` kutusu |
| Tehlikeli düğme | `.dugme--tehlike` | Maskeleme, silme: ikincil kalıp, yalnızca yazısı kırmızı |
| Dar sayfa | `.dar-sayfa`, `.dar-kart` | Tek kolonda okunan ekran (sihirbaz) ve tek başına duran kart (doğrulama, sistem durumu) |
| Müjde şeridi | `.mujde`, `--temiz`, `-ikon` | "Her şey yolunda" bir hata değil bir sonuç: `.bildiri` ölçüsünde değil |
| Sade liste | `.sade-liste` | Satırları kendi ayracını taşıyan liste; aralığı `gap` değil satırın üst çizgisi verir |
| Çıplak alan kümesi | `.alan-kumesi` | `fieldset` yalnızca gruplama için; çerçeveyi `.alan-grubu` çiziyor |
| Metin rolleri | `.meta`, `.ikincil-metin`, `.durum-metni`, `.hata-metni`, `.uyari-metni`, `.baslik-eki`, `.bag-kucuk` | Ölçü + renk birlikte; `.meta`yı bağlantıya vermek rengini eziyor, `.bag-kucuk` yalnızca ölçü verir |
| Sayısal | `.sayisal` | Tabular rakam her yerde; sağa yaslama yalnızca tablo sütununda |
| Kanıt | `.kanit-izgara` / `.kanit-serit`, `-cerceve`, `-gorsel`, `-yer`, `-alt`, `-bayrak`, `.kanit-dugme` | Galeri ızgara, çalıştırma detayı şerit; küçük resmin kendisi düğme |

Düz CSS; yardımcı sınıf (utility) çerçevesi yok. Bileşen katmanı küçük ve
adları Türkçe, çünkü belgelerle kod aynı sözlüğü kullanıyor.

**Dosyadaki sıra kuralın parçası.** Aynı özgüllükte sonra gelen tanım
kazanıyor, dolayısıyla bir bileşenin ölçüsünü ezmesi gereken kural
(`.yigin > * { margin-block: 0 }`) dosyanın **sonunda** duruyor; yukarı
taşınırsa hata vermeden etkisizleşir. Bu bir kez başa geldi: dar ekran
için yazılan çip kuralı, `.secim-cipi` tanımından önceki bir blokta
kaldığı için hiçbir şey yapmıyordu — testler değil, canlıda ölçmek
yakaladı (44 bekleniyordu, 36 geldi).

Bu yüzden iki kapı testi var (`web/src/styles/bilesenler.test.ts`):
**tanımlı her sınıf kullanılıyor** — ölü sınıf ya uygulanmamış bir karar
ya da ekranın satır içinde ezdiği bir kuraldır — ve **yığın sıfırlaması
dosyanın son kuralı**. Birincisi daha yazılırken `.arac-cubugu`yu
yakaladı; yerini `.sayfa-basligi` ile `.suzgec-serit` almıştı, kural
dosyada duruyordu.

Özgüllük yalnızca sırayla değil seçici türüyle de kazanıyor: bir metin
sınıfı (`.meta`, 0-1-0) eleman seçicisini (`a`, 0-0-1) eziyor. Bağlantıya
`.meta` vermek rengini sessiz griye düşürüyordu; ölçü veren ama renge
dokunmayan `.bag-kucuk` bu yüzden var.

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

Kâğıdın paleti panelinkiyle **aynı**, ama değerler Python tarafında elle
yazılı: PDF reportlab ile üretiliyor, CSS token'ını okuyamıyor. Tek kaynak
yine `tokens.css`; pdf.py'deki beş satır onun yansıması ve her birinin
yanında token adı yazılı. A-1'e kadar öyle değildi — kâğıdın kendi soğuk
gri ailesi vardı (#1f2937, #6b7280 …), ürünün parşömen/mürekkep ailesine
ait değildi ve şeritli satırda soluk metin **4,39:1** veriyordu.

## Hareket

Yalnızca geçiş ve geri bildirim: düğme hover/odak 120 ms, basılı hâlde 1 px
iniş; madde tamamlanınca 150 ms tik; senk rozeti dönen ok.
`prefers-reduced-motion: reduce` altında geçişler ve basma hareketi kapanır.
Süslü animasyon yok.

## Makine metni ekrana çıkmaz

Sistemin kendi biçimleri — RFC 5545 tekrar kuralı, ISO tarih, UUID, durum
kodu — ekranda olduğu gibi görünmez. Plan listesi
`FREQ=WEEKLY;BYDAY=MO,WE` yazıyordu; şube müdürünün okuduğu şey buydu.
Çeviri `web/src/features/planlar/tekrar.ts` içinde ve **tanımadığı dizgeyi
olduğu gibi döndürüyor**: uydurulmuş bir cümle, çiğ kuraldan kötüdür —
plan yanlış okunur ve kimse fark etmez.

Aynı kural tarihe de uzanıyor: çalıştırma detayı `2026-11-03` yerine
`3 Kasım 2026` yazıyor.

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
| ~~A-1~~ | ~~Çip renklerini 4,5:1'e çıkar (uyarı, kritik, pasif)~~ | **Bitti** — beş çift düzeldi (koyu temadaki ikisi listede bile değildi), durum çifti tek yerde toplandı, `kontrast.test.ts` ölçüyor. PDF'in token kullandığı doğru değilmiş: kendi paleti vardı, o da hizalandı |
| ~~A-2~~ | ~~Koyu temayı en az bir ekranda sına~~ | **Bitti** — dokuz ekran koyu temada açıldı ve ölçüldü (482 metin öğesi, eşiğin altında olan yalnızca devre dışı düğmeler ve o kasıtlı). Üç kusur çıktı ve düzeldi: çapa yüzeyi, birincil düğme, devre dışı düğme yazısı |
| A-9 | Tema seçimi yok | `:root[data-tema='koyu']` tanımlı ama hiçbir şey `data-tema` yazmıyor: koyu tema yalnızca işletim sistemi tercihini izliyor. Aydınlık mutfakta koyu cihaz kullanan şube müdürü açık temaya geçemiyor. Üst banda bir seçici + `localStorage` yeterli |
| A-3 | ~~Şablon editörü ve plan formuna v1 dilini yay~~ | **Bitti.** Editör `.liste-detay`ya, plan formu dört `.alan-grubu`na geçti; `anaDugme` ve `secimCipi()` satır içi stil üreteçleri silindi |
| ~~A-4~~ | ~~Tablo ritmi: satır yüksekliği, ayraç, sayısal hiza~~ | **Bitti** — her tablo `.tablo` + `.sayisal` + `.eylem`; satır içi dolgu kalmadı |
| ~~A-7~~ | ~~Kalan ekranlar: Şubeler, Personel, Aksiyonlar, Raporlar, Kurulum~~ | **Bitti** — beşinde de sayfa başlığı, boş durum ve sınıf katmanı var; 182 satır içi stil → 0 |
| ~~A-8~~ | ~~Kalan dokuz ekranın satır içi stilleri~~ | **Bitti** — 120 satır içi stil → 2. Kalan ikisi kasıtlı: pano durum hücresi ve `Cip`, rengi veriden hesaplıyor (bkz. A-1) |
| A-5 | İskelet yükleme (skeleton) | Belgede yazılı, hiç uygulanmadı |
| A-6 | Marka wordmark | İsim testi sonucuna bağlı (bkz. `01-strateji/03-isim-ve-marka.md`) |
