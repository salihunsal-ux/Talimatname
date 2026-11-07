# Bağımsız test turu — 7 Kasım 2026

- Kapsam: `demo.talimatname.com` (panel) + `saha.talimatname.com` (saha istemcisi), canlı dağıtım
- Yöntem: şartname oracle alındı. Kod okuması değil, **çalışan sistem ölçüldü**;
  her bulgu ya HTTP cevabıyla ya tarayıcıda ölçülen değerle kanıtlanıyor.
- Boyutlar: yetki, veri kapsamı, gereksinim uyumu, erişilebilirlik, tasarım
  dili, hata yolları, mobil, ürünün kendi dürüstlük kuralı

## Özet

| | Sayı |
|---|---|
| Yüksek | 1 |
| Orta | 3 |
| Düşük | 5 |
| Demo kalitesi | 2 |
| Doğrulanan olumlu | 8 |

En ciddi bulgu ürünün çekirdek iddiasına dokunuyor: **penceresi açılmamış bir
liste bugünden doldurulabiliyor.** Geri kalanı düzeltmesi ucuz.

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
Düzeltme menüde — bayrağı ikiye ayırmak (`yonetici` / `yonetim`). Sunucu
kapısı doğru, gevşetilmemeli.

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

## Demo kalitesi (ürün hatası değil)

### DK-1 · Aylık rapor %3 zamanında tamamlanma gösteriyor

106 çalıştırma · 1 zamanında · 38 kaçırıldı · 67 açık. Sayılar tutarlı ve
rapor doğru çalışıyor, ama bir zincire gösterilecek demo olarak hikâye kötü:
"hiçbir şube listesini tamamlamıyor". Demoyu dolduran turda geçmiş günlere
tamamlanmış çalıştırma yazılması gerekiyor.

### DK-2 · Test turunun bıraktığı kalıntı

Yetki sınaması yöneticiyle `POST /templates` çağırdı ve başarılı oldu:
demoda **"Yetki denemesi"** adlı boş taslak şablon var. Benim bıraktığım
kalıntı. API'de şablon silme uç noktası yok, veritabanından düşürülmeli.

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

## Açık sorular

1. **Y-1 kasıtlı mı?** Pencere açılmadan listeyi doldurabilmek bir kolaylık
   mı (hazırlık), yoksa kapatılmalı mı? Kapatılacaksa üç seçenek var:
   (a) `_ensure_open`'a alt sınır eklemek — en net, ama "5 dakika erken
   başladım" durumunu da keser; (b) yazmaya izin verip cevabı "pencere
   öncesi" diye işaretlemek ve raporda ayırmak; (c) `window_start`'tan N
   dakika önce açılan bir hazırlık payı. Şartname sessiz olduğu için bu bir
   ürün kararı, kod kararı değil.
2. Bulgular backlog'a hikâye olarak girsin mi, yoksa bu belge yeterli mi?
3. DK-1: demo verisi daha iyi bir hikâyeye çekilsin mi (geçmiş günlere
   tamamlanmış çalıştırmalar)?
