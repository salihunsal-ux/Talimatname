# Dış test turu — B bulguları (6–7 Kasım 2026)

Bağımsız bir test mühendisi demoyu uçtan uca denedi ve 14 bulgu yazdı
(B01–B14). Rapor bu depoda değil; bu sayfa bulguların **durumunu** ve
nereye bağlandığını tutuyor, böylece gereksinimlere giren değişiklikler
kaynağıyla birlikte izlenebiliyor.

Turun temeli `talimatname-kod@02e1ff5` — [bir önceki iç turun](08-bagimsiz-test-turu.md)
düzeltmelerinden (`f671a70`) bir commit öncesi. Bu yüzden iki tur kısmen
örtüşüyor.

## Durum

| ID | Öncelik | Bulgu | Durum |
|---|---|---|---|
| B01 | P1 | Başarısız cevapta istenen fotoğraf/not girilemiyor | **Kapandı** — saha kartında açıklama alanı ve fotoğraf düğmesi; engeller maddeye bağlanıyor |
| B02 | P1 | Sunucu aralık dışı ölçümü `passed` kabul ediyor | **Kapandı** — BR-08a, `resolve_answer` |
| B03 | P1 | Başkasının kilitlediği liste gönderilebiliyor | **Kapandı** — BR-26, `submit` içinde `ensure_writable` |
| B04 | P1 | Kritik başarısız cevap anında aksiyon üretmiyor | **Kapandı** — BR-10 tetiği cevabın kaydı |
| B05 | P1 | "Yapılamadı" aksiyon üretmiyor | **Kapandı** — `from_not_done`, orta öncelik / 72 sa |
| B06 | P2 | Pencere açılmadan cevap yazılabiliyor | **Kapanmıştı** — iç turun Y-1'i, BR-02a |
| B07 | P2 | Yönetici cevap detayında ölçüm ve metin değeri yok | **Kapandı** — değer, birim, metin cevabı ve `answered_by` |
| B08 | P2 | Ayşe demo hesabı kullanılamıyor; hata açıklaması anlamsız | **Kapandı** — başlık ekranda; Kadıköy şube müdürü hesabı açıldı |
| B09 | P2 | Düğme işlemden önce "kaydedildi" diyor; boş ölçüm hata gibi | **Kapandı** — `KayitDurumu`, iki hâlli aralık ipucu |
| B10 | P2 | Saha kartlarında liste adı ve gece yarısı tarihi eksik | **Kapandı** — `plan_name` özette; tarih gece yarısını aşan pencerede |
| B11 | P2 | Pano varsayılan iş günü UTC'den hesaplanıyor | **Kapandı** — `web/src/tarih.ts` ve `api/.../is_gunu.py`; plan ve rapor ekranları da |
| B12 | P2 | PNG dışındaki fotoğraf türleri JPEG diye etiketleniyor | **Kapandı** — dönüştürmek yerine reddediliyor; seçici de daraltıldı |
| B13 | P3 | Bazı yardımcı dokunma hedefleri 44 px altında | **Kapandı** — 375 px'te 44 px altında hedef kalmadı |
| B14 | P3 | PDF şube tablosu başlıkları sütuna sığmıyor | **Kapandı** — başlık hücreleri Paragraph, sarılıyor |

## Gereksinimlere giren değişiklikler

- **BR-08a** (yeni) · **FR-0307a** (yeni): ölçüm ve seçim maddelerinde
  geçer/geçmez kararını sunucu verir; istemcinin beyanı bağlayıcı değil.
  BR-08 "4,0 geçer / 4,1 geçmez" diyordu ama **kimin** karar verdiği
  yazılı değildi, o yüzden yalnızca istemcide uygulanmıştı.
- **BR-26** (ek cümle): kilit hem yazmada hem **gönderimde** denetlenir.
- **BR-10** (ek cümle): tetik cevabın kaydıdır, gönderim değil; düzeltilen
  cevap aksiyonu geri almaz.
- **BR-01** (ek cümle): tarih verilmeyen yerlerde "bugün" yerel/hesap saat
  diliminden hesaplanır, UTC'den değil.
- **API taslağı**: cevap ucu ölçüm/seçimde düzeltilmiş `state` dönebilir;
  okunamayan değer 422 `gecersiz-istek` (`errors[].alan = "value"`).
  `CalistirmaOzet` artık `plan_name`, `CevapCiktisi` artık `answered_by` taşıyor.

## Raporun düzeltilen tespiti

**B08'in kök nedeni.** Rapor "kaynak seed verisi Ayşe'yi içeriyor" diyor.
İçeren dosya `infra/memory.py`, yani testlerin kullandığı **bellek içi**
depo; canlı Postgres demosunun tohumu değil (depoda böyle bir betik yok,
demo kullanıcıları elle açılmış). "Eski personel #4821 — Maskeli"
kaydının Ayşe olduğu da çıkarım: maske sayacı sıralı olduğu için
etiketten kimlik okunamaz, ki maskelemenin amacı bu (BR-22).

Bu yüzden B08 ikiye ayrıldı:

1. **Veri işi** — **kapandı (7 Kasım).** Demoya Kadıköy kapsamlı bir
   şube müdürü açıldı: **Ayşe Şube · `+90 532 111 00 08`**, rol
   `branch_manager`, kapsam Kadıköy (KDK). Kurgu isim, demo numara
   aralığından; gerçek kişi verisi yok (ADR-0003). Giriş denendi:
   panelde yalnızca Kadıköy'ün iki listesi ve 32 aksiyonu görünüyor,
   menüde Personel / Bildirimler / Kurulum yok — Deniz Şube ile aynı
   kısıtlı profil. Dış raporun "Ayşe" beklentisi böylece gerçek bir
   hesaba karşılık geliyor.

   Kayıt, ilk oluşturmada Türkçe harfler olmadan yazıldığı için
   önce **personel içe aktarmasıyla** düzeltildi (`/setup/staff/import`
   telefona göre `full_name` günceller): tek kullanıcıyı yeniden
   adlandıran bir uç yoktu, `/users` yalnızca oluştur, rol değiştir,
   pasifleştir, maskele diyordu. Gerçek bir zincirde yanlış yazılmış
   bir isim imzalı kayıtlara düşeceği için bu eksik
   **kapatıldı (`talimatname-kod@b616d4e`)**: `PATCH /users/{user_id}`
   adı ve e-postayı düzeltiyor, panelde satır içi "Adı düzelt"
   düğmesiyle. Telefon bu uçtan değişmiyor (numara kişinin kimliği:
   giriş ve içe aktarma anahtarı), roller ayrı uçtan, maskeli kullanıcı
   değiştirilemiyor (BR-22 · 409), günlüğe değer değil yalnızca
   "ad değişti" yazılıyor (BR-21).
2. **Kod hatası** — giriş ekranı hata cümlesi olarak `detail` alanını
   `title`'ın önüne koyuyordu, o yüzden kullanıcı "Bu numarayla kayıtlı
   kullanıcı yok" yerine yalnızca "Telefon: +90…" görüyordu. Ayşe'ye
   özel değildi, **her** giriş hatası böyleydi. **Kapandı:** başlık hep
   duruyor, detay arkasına ekleniyor ("2 hakkınız kaldı" gibi gerçekten
   kullanıcıya ait olanlar kaybolmasın); `UnknownPhone` da numarayı geri
   yazmıyor.

## Raporun kaçırdıkları

- `reports.py` ölçüm günlüğünde aralık dışılığı kendi hesaplıyor. B02
  düzeltilmeden önce aynı veri için çalıştırma "%100 geçti", ölçüm
  günlüğü "aralık dışı" diyordu — tutarsızlık müdürün ekranında
  görünüyordu.
- B11 yalnızca panoda değil: aynı UTC kesimi plan başlangıç tarihinde,
  rapor aralığında **ve sunucuda** (tarih parametresiz `/runs`,
  `/dashboard`) da vardı. Plan başlangıcında etkisi en ağırı.
- B14 iki başlıkta değil üçte taşıyordu. Sunucunun yazı tipiyle (DejaVu
  Sans Bold, 8.5 pt) ölçüldüğünde "Zamanında" 53,3 pt, "Başarısız"
  43,0 pt ve "Zamanındalık" 64,8 pt; sütunların kullanılabilir genişliği
  sırayla 47,2 / 42,3 / 52,1 pt. Geliştirme makinesinin yazı tipinde
  (Segoe UI) hiçbiri taşmıyor — kusur yazı tipine bağlıydı, düzeltme
  değil.
- BR-10'un beş tetiğinden kaçırılan çalıştırma zaten yazılmıştı
  (`from_missed_run`); eksik olan tek kapsam-içi tetik "yapılamadı"ydı
  (B05). Sorun bildirimi v1 kapsamında yazılmadı (saha istemcisinin
  kendi eksik listesinde duruyor).
- `evidence_count` istemciden gelip satıra yazılıyor. Okumalar bunu
  doğrulanmış kanıt deposundan ezdiği için gönderim kapısı güvende
  (raporun servis probu bu yüzden üretimden zayıf, ki raporda da
  belirtilmiş); yine de satırda doğrulanmamış bir sayı duruyor.

## Canlı doğrulama turu (7 Kasım 2026, 21:47–22:00 TRT)

Düzeltmeler demoda (`demo.talimatname.com` / `saha.talimatname.com`)
gerçek bir listede denendi: 7 Kasım Kadıköy **Günlük kapanış**
(pencere 22:00–01:30, hazırlık payı 21:45'ten itibaren yazılabilir).
Liste gerçekten dolduruldu ve **gönderildi**; demoya iki yeni aksiyon
ve beş kanıt dosyası yazıldı. Aşağıdaki satırlar o turun çıktısıdır,
tahmin değil.

| Bulgu | Ne denendi | Ne görüldü |
|---|---|---|
| B02 | İstemci `state=passed`, değer 99 (aralık 0–4) | Sunucu `failed` yazdı |
| B02 | `4,0` / `4,1` | `passed` / `failed` — BR-08 sınırı birebir |
| B02 | `"altı"`, `1e999`, değer yok | 422 `gecersiz-istek`, `errors[].alan = "value"` |
| B03 | Emre kilidi tutarken Zeynep **gönderdi** | 409 `urn:talimatname:calistirma-kilitli` |
| B03 | Aynı anda Zeynep **yazdı** | 409, aynı tip |
| B04 | Kritik madde başarısız yazıldı | Aksiyon **cevap anında**: kritik, 4 sa, açık 107→108 |
| B05 | Kritik olmayan maddeye "yapılamadı" | Aksiyon: normal, **72 sa**, açıklamada sebep |
| B05 | Kritik maddeye "yapılamadı" | 422 `kritik-maddede-yapilamadi-yok` (BR-09) |
| B01 | Başarısız cevabın altındaki açıklama alanı | Yazıldı, kaydedildi, "not gerekiyor" engeli düştü |
| B01 | Engel satırına tıklandı | `#madde-<id>` çapasına gitti |
| B01 | Fotoğraf + kalan maddeler, sonra **Listeyi gönder** | 7/7, engel 0, `submitted`, %71, sonuç `failed` |
| B07 | Yönetici çalıştırma detayı | "4.1 °C ✕ Geçmedi", "Evet ✓ Geçti", metin cevabı, "Emre Personel · 21:52" |
| B08 | Kayıtlı olmayan numarayla giriş | "Bu numarayla kayıtlı kullanıcı yok" |
| B09 | Aralık dışı ölçüm | "Kabul aralığı 0–4°C: bu değer dışarıda, madde başarısız sayılır." |
| B10 | Saha kartı | "Günlük kapanış · Kadıköy · Pencere: 07/11 22:00–01:30" |
| B11 | Yönetici detayında saatler | 18:49Z yazma "21:49" göründü |
| B12 | Seçiciye WebP verildi | "Bu dosya türü yüklenemiyor (image/webp). JPEG ya da PNG bir fotoğraf seçin." |

B13 ve B14 bu turda tekrar denenmedi: ikisi de daha önce ölçümle
doğrulanmıştı (375 px'te 44 px altı hedef yok; sunucunun yazı tipiyle
başlık satırı 28 pt'ye sarıyor).

Raporun kaçırdığı tutarsızlık da kapandı: aynı ölçüm için çalıştırma
"başarısız", ölçüm günlüğü `out_of_range: true` diyor — ikisi artık
aynı kaynaktan.

### Turda çıkan yan gözlemler

1. **Kanıt tekrarı koruması çalışıyor.** Dört maddeye aynı baytlardan
   oluşan PNG yüklenince ilki kabul edildi, üçü
   409 `urn:talimatname:kanit-tekrari` ile döndü ("Bu fotoğraf daha
   önce gönderildi, yeniden çekin"). Dış raporda geçmiyor; beklenen
   davranış.
2. **`answered_by` yazma cevabında boş.** `PUT .../answers/{id}`
   dönüşündeki `CevapSonucu.answered_by` `null`; isim yalnızca
   çalıştırma detayı okunurken çözülüyor. Ekranda bir eksiklik
   doğurmuyor (istemci zaten tazeliyor) ama şema iki yerde aynı alanı
   farklı dolduruyor.
3. **Kilit çakışmasında ham kimlik.** 409'un `detail` alanı
   "Kilit sahibi: 73a8e2ba-…" diyor; istemci bunu isme çeviremiyor.
   Kişisel veri sızdırmıyor (opak kimlik) ama kullanıcıya "listeyi
   şu an kim dolduruyor" denemiyor. `claim`/`release` uçları yazıldığında
   (K01) birlikte düzeltilmeli.
4. **Personel içe aktarma raporu telefonları yanlış alanda
   döndürüyordu — düzeltildi (`talimatname-kod@3ab6008`).**
   `YuklemeRaporu.branches` şemada "Kabul edilen şube kodları" diye
   tanımlı ama `_personel_raporu` içine
   `[satir.phone for satir in rapor.rows]` koyuyordu
   (`routers/setup.py`). 200 kişilik bir yüklemede cevap gövdesi,
   istemcinin şube kodu sanacağı bir alanda 200 telefon numarası
   taşıyordu; hem sözleşme yanlıştı hem de numaralar beklenmedik bir
   yerdeydi (BR-21). Alanı okuyan kimse yok — web istemcisinde
   yalnızca test mock'larında geçiyor, ekranda `created` / `updated` /
   `error_rows` sayıları duruyor. Bu yüzden yeni bir alan açmak yerine
   personel raporunda boş bırakıldı; şube yüklemesinde kod listesi
   olduğu gibi kaldı ve alan açıklaması bunu söylüyor
   ("yalnızca şube yüklemesinde dolar"). İki test bekçi: personel
   cevabında numara geçmiyor, şube cevabında kod geçiyor.
5. **Seçenek etiketleri çalıştırma detayında yok.** `choice`
   maddelerinde `options` yalnızca sabitlenmiş şablon sürümünde
   duruyor; saha istemcisi ikinci bir istekle alıyor. Tasarım böyle,
   kusur değil — ama tek uçtan beslenen bir istemci seçenekleri
   göremez.

## Demoda bırakılan test verisi

**Kapandı.** 7 Kasım Kadıköy Kapanış listesi, yukarıdaki canlı turda
pencere açıkken gerçekten doldurulup gönderildi; test mühendisinin
`Süt dolabı sıcaklığı = 6` ölçümü aynı madde üzerinden 4,1'e
güncellendi, `QA 2026-11-07: …` notu devreden vardiya notu olarak
kayıtta kaldı (silinmedi; `audit_event` ekle-yalnız). Liste artık
`submitted`, sonuç `failed`, %71.
