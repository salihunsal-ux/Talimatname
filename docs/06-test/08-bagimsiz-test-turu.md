# Bağımsız test turu — 7 Kasım 2026

- Kapsam: `demo.talimatname.com` (panel) + `saha.talimatname.com` (saha istemcisi), canlı dağıtım
- Yöntem: şartname oracle alındı. Kod okuması değil, **çalışan sistem ölçüldü**;
  her bulgu ya HTTP cevabıyla ya tarayıcıda ölçülen değerle kanıtlanıyor.
- Boyutlar: yetki, veri kapsamı, gereksinim uyumu, erişilebilirlik, tasarım
  dili, hata yolları, mobil, ürünün kendi dürüstlük kuralı

## Özet

| | Sayı | Durum |
|---|---|---|
| Yüksek | 1 | kapandı |
| Orta | 3 | kapandı |
| Düşük | 5 | kapandı |
| Demo kalitesi | 2 | kapandı |
| Doğrulanan olumlu | 8 | — |

En ciddi bulgu ürünün çekirdek iddiasına dokunuyordu: **penceresi açılmamış
bir liste bugünden doldurulabiliyordu.**

> **7 Kasım 2026 · hepsi düzeltildi ve canlıda doğrulandı.** Y-1 için
> hazırlık payı seçildi (aşağıda). Her bulgunun altında **Düzeltme**
> notu var; düzeltmeler `talimatname-kod` deposunda, demo sunucuda
> yayında.

---

## YÜKSEK

### Y-1 · Pencere açılmadan liste doldurulabiliyor

**Ne oluyor.** Beşiktaş'ın "Kapanış (kafe)" çalıştırması `scheduled`,
penceresi `2026-11-07T21:00Z → 2026-11-08T00:30Z`. Saat 11:00'de saha
istemcisi bu listeyi **birincil düğmeyle** ("Listeyi aç") açıyor, ekranda
"792 dk kaldı" yazarken bütün maddeler cevaplanabilir hâlde geliyor.

**Sebep.** `api/src/talimatname/services/execution.py:350` —

```python
def _ensure_open(self, run: Run, now: datetime) -> None:
    if run.status in ("submitted", "cancelled"):
        raise RunClosed(...)
    if now >= run.tolerance_end:
        raise WindowClosed(...)      # yalnızca ÜST sınır
```

Alt sınır yok. `window_start`'tan önce yazmayı engelleyen hiçbir şey yok.

**Neden önemli.** Ürünün satış cümlesi "kim, ne zaman, kanıtıyla yaptı".
FR-1203 raporu "pencere içi / geç / kaçırıldı" diye ayırıyor. Kapanış listesi
13 saat önceden doldurulabiliyorsa "pencere içi" ölçüsü anlamını yitirir:
personel sabah gelip akşamki kapanışı işaretler, fotoğrafı da o an çeker.

**Şartname bu konuda sessiz.** FR-0610 yalnızca geri sayım, "geç" uyarısı ve
tolerans kilidinden söz ediyor; BR-03 yalnızca tolerans bitişini bağlıyor.
Yani bu hem bir kod açığı hem bir **gereksinim boşluğu** — kararı ürün
sahibinin vermesi gerekiyor (bkz. [Açık sorular](#açık-sorular)).

**Kanıt sınırı:** kod okuması + arayüzün listeyi açması. Demoyu kirletmemek
için pencere öncesi **canlı yazma denemesi yapılmadı**.

### Düzeltme — seçenek (c): hazırlık payı

`_ensure_open`a alt sınır eklendi ve yeni bir hata tipi geldi:
`pencere-acilmadi` (409, "Pencere henüz açılmadı"). Açılış anı
`window_start − run_prep_minutes`; ayar varsayılanı **15 dakika**
(0–120 arası). Pay, vardiya erken başladığında listenin elde olmasını
sağlıyor; akşamki kapanışın sabahtan işaretlenmesini engelliyor.

`writable_from` üç yüzeye eklendi — çalıştırma listesi, çalıştırma
detayı ve **senk manifesti** (mobil Faz B bunu okuyacak). Saha
istemcisi açılmamış listeyi birincil düğmeyle değil "Listeyi gör" ile,
salt okunur açıyor ve üstte "Pencere henüz açılmadı: N dk sonra
doldurulabilir" yazıyor.

Canlı doğrulama (7 Kasım):

```
PUT /runs/{scheduled}/answers/{id}
→ 409 urn:talimatname:pencere-acilmadi
  "Açılış: 2026-11-07T20:45:00+00:00"     (pencere 21:00, pay 15 dk)
arayüz: "Pencere henüz açılmadı: 499 dk sonra doldurulabilir."
```

**Yan bulgu.** Kural gelince **15 test düştü** ve hepsi fikstür
hatasıydı: "açık pencere"yi yalnızca üst sınırla tanımlıyorlardı,
yani sunucu izin verdiği için yanlışlıkları görünmüyordu. Saat ileri
alınarak düzeltilmedi — kanıt belirtecinin `iat`i geleceğe düşüp
doğrulanamıyor — pencere oynatıldı.

---

## ORTA

### O-1 · Bölge müdürüne çalışmayan iki menü maddesi gösteriliyor

Sunucu `/notifications` ve `/setup*` uç noktalarını yalnızca yöneticiye
açıyor. Panel menüsü ise tek bir `yonetim` bayrağıyla ikisini de bölge
müdürüne gösteriyor:

```ts
// web/src/bilesenler/Kabuk.tsx
{ anahtar: 'bildirimler', ad: tr.gezinme.bildirimler, yonetim: true },
{ anahtar: 'kurulum',     ad: tr.gezinme.kurulum,     yonetim: true },
...
const yonetim = rolVar(useBen(), 'admin', 'region_manager');
```

`+905321110002` (Murat Bölge) ile ölçülen menü:
`Pano · Şubeler · Personel · Şablonlar · Planlar · Aksiyonlar · **Bildirimler**
· Raporlar · Saha (demo) · **Kurulum** · Sistem durumu`

API ölçümü: `GET /notifications` → **403**, `GET /setup` → **403**.

Ürünün kendi ilkesiyle çelişiyor: sunucunun reddedeceği düğme gösterilmemeli.

### Düzeltme

Menüdeki tek bayrak ikiye ayrıldı: `yonetim` (sunucuda `Mudur` —
yönetici + bölge müdürü) ve `yalnizcaYonetici` (sunucuda `Yonetici`).
Sunucu kapısına dokunulmadı. `Kabuk.test.tsx` üç rol için menüyü
sınıyor. Canlı: bölge müdürünün menüsünde artık Bildirimler ve Kurulum
yok, Personel duruyor.

### O-2 · Doğrulama hataları kullanıcıya İngilizce gösteriliyor

Gövdesi hatalı bir istekte sunucu RFC 9457 zarfını Türkçe dolduruyor ama
alan sebeplerini Pydantic'ten ham geçiriyor:

```json
{ "title": "İstek doğrulanamadı",
  "errors": [{ "alan": "state",
               "sebep": "Input should be 'passed', 'failed', 'not_done' or 'not_applicable'" }] }
```

İstemci bu sebebi ekrana basıyor (`web/src/bilesenler/Durum.tsx`):

```ts
const sebep = problem?.errors?.length ? `: ${problem.errors[0].sebep}` : '';
```

Sonuç: Türk kullanıcı "İstek doğrulanamadı: Input should be 'passed'…"
görüyor. Elle yazılan iş hatalarında sorun yok ("Bu şube kodu zaten var") —
yalnızca şema seviyesindeki hatalar sızıyor.

### Düzeltme

Yeni `api/dogrulama_metni.py`: Pydantic hatasını **tipe göre**
Türkçeleştiriyor (mesaj metnine bakmıyor ki sürüm değişince bozulmasın),
tanınmayan tip İngilizceye değil "Değer geçerli değil"e düşüyor.
Alan doğrulayıcısının kendi Türkçe cümlesi (`value_error`) korunuyor.
Canlı:

```json
{"alan": "state",
 "sebep": "Şunlardan biri olmalı: 'passed', 'failed', 'not_done' ya da 'not_applicable'"}
```

### O-3 · Saha ilerleme sayacı talimat satırını cevaplanmış sayıyor

Hiç dokunulmamış listede ekran **"1/8 madde"** yazıyor; sunucuda cevap sayısı
**0**.

```ts
// web/src/features/saha/SahaSayfasi.tsx:176
const maddeler = veri.sections.flatMap((b) => b.items);               // 8 (7 cevaplanır + 1 talimat)
const cevaplanan = maddeler.filter(
  (m) => m.type === 'instruction' || m.answer !== null).length;       // 1
```

Talimat satırı hem paydaya hem paya giriyor. Sunucu onu puanlamıyor
(`execution.py:362`, "talimat satırı cevaplanmaz"), yani payda da sunucunun
saydığıyla (7) uyuşmuyor. Sonda "8/8" olarak kapanıyor, bu yüzden gözden
kaçmış; arada her an yanlış.

### Düzeltme

Talimat satırı artık ne paya ne paydaya giriyor. Aynı liste canlıda
**"0/7 madde"** gösteriyor.

---

## DÜŞÜK

### D-1 · Bildirimler ekranında makine kodu

Tüm panelde makine metni taraması yapıldı (11 ekran). Yalnızca iki sızıntı:
Bildirimler tablosunda **`surucu-yok`** ve **`alici-pasif`**. Sunucu zaten
Türkçe karşılığını gönderiyor (`error_detail`: "push sürücüsü bağlı değil");
ekran onu kullanmıyor. Not: `BildirimlerSayfasi.test.tsx:81` ham kodun
göründüğünü **test ediyor** — düzeltmede o beklenti de değişmeli.

### D-2 · Sayfa başlığı hiç değişmiyor, saha istemcisinde yanlış

`document.title` on bir ekranın hepsinde `"Talimatname · Yönetim paneli"`.
İki sonucu var: sekme değiştiren ya da ekran okuyucu kullanan kişi nerede
olduğunu anlayamıyor; ve **saha.talimatname.com** da aynı başlığı taşıyor —
saha istemcisi için düpedüz yanlış bilgi.

### D-3 · Saha ekranında başlık atlaması (h1 → h3)

Saha ekranı `h1`den doğrudan `h3`e geçiyor. Diğer on ekran temiz.

### D-4 · Form hatası alana bağlanmıyor

Var olan şube kodu (`BSK`) girilip gönderildiğinde sunucu doğru reddediyor
("Bu şube kodu zaten var", `role="alert"`, form değerleri korunuyor — bu
kısım iyi). Ama hata ilgili alana bağlı değil: `aria-invalid` yok,
`aria-describedby` yok, odak hatalı alana taşınmıyor. Ekran okuyucu cümleyi
duyuruyor ama hangi alan olduğunu söylemiyor.

### D-5 · Tema seçici dokunma hedefinin altında

375px'te tema `<select>` 36px yüksekliğinde; dokunma hedefi alt sınırı 44px.
Saha istemcisindeki tek küçük hedef — diğer bütün düğmeler sınırın üstünde.

---

### Düşük bulguların düzeltmeleri

| | Düzeltme |
|---|---|
| D-1 | Ekran `error_detail`i yazıyor ("push sürücüsü bağlı değil"); kod `title` özniteliğinde kaldı (destek konuşmasında lazım). Ham kodun göründüğünü doğrulayan test tersine çevrildi. Canlı taramada panelde makine kodu kalmadı. |
| D-2 | `sayfaBasligi.ts`: başlık ekran adıyla başlıyor ("Raporlar · Talimatname · Yönetim paneli") ve saha kapısı **"Talimatname · Saha"** diyor. |
| D-3 | Saha eksikler bölümü `h3` → `h2`; atlama kalmadı. |
| D-4 | `DomainError`a `field` eklendi: alanı olan kural hatası cevaba `errors` koyuyor (`{"alan": "code", …}`). Form `aria-invalid` + `aria-describedby` veriyor, hatayı alanın altına yazıyor ve odağı oraya taşıyor. Alanı olmayan kural hataları `errors` taşımıyor — uydurma alan adı üretilmiyor. |
| D-5 | `.tema-secici` 44 px'e çıkarıldı; 375 px'te küçük dokunma hedefi kalmadı. |

## Demo kalitesi (ürün hatası değil)

### DK-1 · Aylık rapor %3 zamanında tamamlanma gösteriyor

106 çalıştırma · 1 zamanında · 38 kaçırıldı · 67 açık. Sayılar tutarlı ve
rapor doğru çalışıyor, ama bir zincire gösterilecek demo olarak hikâye kötü:
"hiçbir şube listesini tamamlamıyor".

### Düzeltme

Yeni betik: `talimatname.araclar.demo_doldur`. Geçmiş günlere (10 Ekim →
1 Kasım) çalıştırma üretip **gerçek servislerle** dolduruyor — cevaplar
`write_answer`, gönderim `submit`; puan, sonuç, kritik aksiyon ve denetim
izi normal yoldan oluşuyor. Servisin saati çalıştırmanın penceresine
ayarlanıyor.

İki şeye dikkat edildi:

- **Demonun kendi geçmişine dokunulmuyor.** `--bitis 2026-11-02`
  sınırının ötesindeki hiçbir kayıt değişmiyor; gezerken kaçırılan liste
  kaçırılmış kalıyor (BR-03). Sınırın gerisi tohum verisi: hiç
  yaşanmamış bir geçmiş kuruluyor, var olan kayıt düzeltilmiyor.
- **Kanıt uydurulmuyor.** Fotoğraf zorunlu maddelere gerçekten bir dosya
  yükleniyor — belirgin bir yer tutucu görsel, `from_gallery` işaretli.
  `evidence_count`i elle yazmak "fotoğraf var" demek olurdu ve bu ürünün
  tam da iddia ettiği şeyi yalanlardı.

Sonuç — **Ekim 2026 raporu**: 66 çalıştırma, 60 zamanında, 6 kaçırıldı,
4 başarısız, **%91 zamanında tamamlanma**. Kasım ayı demoyu gezen kişiye
bırakıldı (hâlâ 67 açık liste var).

### DK-2 · Test turunun bıraktığı kalıntı

Yetki sınaması yöneticiyle `POST /templates` çağırdı ve başarılı oldu:
demoda **"Yetki denemesi"** adlı boş taslak şablon kaldı (iki kez — test
iki kez koşmuş).

### Düzeltme

İkisi de silindi. Öncesinde bağımlılıkları denetlendi: boş taslak, bağlı
plan ve çalıştırma yok. `audit_event`e **dokunulmadı** (ekle-yalnız):
şablonun oluşturulduğu olay kaydında duruyor ve durmalı. Kalan şablonlar:
Kapanış (kafe), Açılış, Açılış (kafe / hızlı servis), Haftalık genel
temizlik.

---

## Doğrulanan olumlu bulgular

Bunlar "bakılmadı" değil, **ölçüldü ve geçti**:

1. **Veri kapsamı kusursuz.** 16 çapraz erişim denemesi (2 rol × 8 şube):
   bölge müdürü yalnızca Anadolu'nun 3 şubesini, şube müdürü yalnızca
   Beşiktaş'ı görüyor; diğer her şube detayı 403. Çalıştırma listeleri de
   aynı şekilde daralıyor (11 / 5 / 2 kayıt).
2. **Yetki kapıları sağlam.** 11 uç nokta × 4 rol doğrudan API'den sınandı.
   Yetki yükseltmesi yok; tek sapma O-1.
3. **Kontrast temiz.** 11 ekran × 2 tema, görünür her metin düğümü canlı
   ölçüldü (WCAG oranı, 24px/18.66px-kalın eşikleriyle). **Sıfır ihlal.**
4. **Erişilebilirlik temeli sağlam.** Etiketsiz form alanı, erişilebilir adı
   olmayan düğme/bağ, `alt`sız görsel yok; ekran başına tek `h1`;
   `lang="tr"`; tema seçicide `aria-label="Tema"`.
5. **Dürüstlük kuralı tutuyor.** Bildirimler ekranı "Kanala verildi **0** /
   Gönderilemedi **115**" diyor ve başına "Hiçbir bildirim kanalı bağlı
   değil… bu liste eksiklerin kaydıdır" yazıyor. Uydurma teslimat yok.
6. **BR-03 sunucuda zorlanıyor.** Kaçırılmış çalıştırmaya cevap yazma denemesi
   `409 urn:talimatname:pencere-kapali` ile reddedildi; arayüz de o liste
   için "Listeyi gör" (salt okuma) gösteriyor, "Listeyi aç" değil.
7. **Mobil 375px temiz.** Saha istemcisinde yatay kaydırma yok, taşan öğe yok,
   D-5 dışında küçük dokunma hedefi yok.
8. **Şube kodu çakışması** sunucuda yakalanıyor ve form değerleri kayboluyor
   değil — kullanıcı baştan yazmak zorunda kalmıyor.

---

## Test edilmeyenler

Bu bir kesit, tam tur değil. Yapılmayanlar:

- TC-001…128 kabul vakalarının sistematik koşulması
- Yalnızca klavyeyle uçtan uca gezinme; gerçek ekran okuyucuyla dinleme
- Kurulum sihirbazının uçtan uca doldurulması
- Şablon sürümleme (taslak → yayın → yeni sürüm) senaryosu
- Plan önizleme (FR-0511) ve çakışma kuralı (FR-0517)
- Kanıt yükleme, PDF çıktısı, eskalasyon zinciri
- Çevrimdışı davranış (saha istemcisi zaten desteklemiyor, not düşülmüş)
- Yük/eşzamanlılık

## Kararlar

**Y-1 → seçenek (c), hazırlık payı.** Ürün sahibi kararı, 7 Kasım 2026.
Varsayılan 15 dakika. Bu karar şartnamedeki boşluğu da kapatıyor:
FR-0610 yalnızca üst sınırı anlatıyordu, alt sınır artık yazılı
(`run_prep_minutes`, BR-02'nin hazırlık payı).

Payın plan başına ayarlanması **v1.1'e** bırakıldı: bugün tek bir hesap
ayarı, bütün planlar için aynı.

## Şartnamede güncellenmesi gerekenler

Bu tur kodu değiştirdi; aşağıdakiler henüz belgeye işlenmedi:

- **BR-02**'ye hazırlık payı cümlesi: pencere `window_start − N dk`
  açılır, N hesap ayarı (varsayılan 15).
- **FR-0610**'a alt sınır: açılmamış listede yazma kapalı, liste okunur.
- **API taslağı**: `writable_from` üç yüzeyde (çalıştırma listesi,
  detayı, senk manifesti) ve `pencere-acilmadi` hata tipi.
- **ADR-0013** devir kapısı: senk sözleşmesine alan eklendi (geriye
  uyumlu), mobil geliştirici bunu okumalı.

## Açık sorular

1. Bulgular backlog'a hikâye olarak da girsin mi, yoksa bu belge yeterli mi?
2. Hazırlık payı 15 dakika doğru mu? Yeme-içme zincirinde vardiya ne kadar
   erken başlıyor — pilot öncesi bir şube müdürüne sorulabilir.
