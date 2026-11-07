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
| B08 | P2 | Ayşe demo hesabı kullanılamıyor; hata açıklaması anlamsız | **Kod yarısı kapandı** — başlık artık ekranda; hesap kararı açık (aşağıya bakın) |
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

1. **Veri işi** — demoya kullanılabilir bir Kadıköy şube müdürü hesabı
   eklenecek mi? Karar bekliyor.
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

## Demoda bırakılan test verisi

7 Kasım Kadıköy Kapanış listesinde test mühendisinin yazdığı
`Süt dolabı sıcaklığı = 6` ve `QA 2026-11-07: …` notu duruyor; liste
gönderilmedi. Kaçırılmış bir listeyi geriye dönük doldurmak yasak
(BR-03) ama bu liste Kasım'da **açık**: ya iptal sebebiyle kapatılır ya
bırakılır. Karar bekliyor.
