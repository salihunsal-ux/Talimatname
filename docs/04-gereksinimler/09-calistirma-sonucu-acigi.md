# Çalıştırma sonucu: "Başarısız" ne demek?

- Tarih: 2026-11-11 · Durum: **kapandı (11 Kasım, seçenek A)**
- İlgili: BR-06, BR-07, FR-0306, FR-0307, BR-10, BR-11
- Bulunduğu yer: demoya denetim şablonu girilirken (8 Kasım turu)

## Kapanış (11 Kasım 2026)

**Seçenek A uygulandı** (`talimatname-kod@0de53d0`): sonuç yalnızca
kritik maddeyle belirleniyor, kritik olmayan eksik puana yansıyor.
`evaluate`'in açıklaması ve `test_tc020_puan_yuzdesi` birlikte
güncellendi; "yapılamadı" da aynı kurala girdi (puanı düşürür, sonucu
belirlemez — kritik maddede zaten denenemiyor, BR-09).

Aşağıdaki çözümleme duruyor: kararın gerekçesi, değişen koddan uzun
ömürlü.

**Sonucu kabul edilen bedel.** Panonun istisna süzgeci `result` ve
`late`e bakıyor; artık düşük puanlı ama kritiksiz bir çalıştırma
varsayılan görünümde **işaretlenmiyor**. Puan eşiği bilerek
eklenmedi: BR-07 eşiği ve ağırlığı v1.1'e bırakıyor, burada uydurmak
kuralı ikinci kez çatallardı. Seçenek C (üçüncü durum `eksikli`) bu
boşluğun gerçek cevabı ve v1.1'de açık duruyor.

**Geçmiş kayıtlar yeniden hesaplanmadı.** Eski kuralla kapanmış
çalıştırmalar `failed` olarak duruyor; sonucu sonradan yeniden yazmak,
gönderilmiş bir kaydı değiştirmek olurdu. Demodaki 8 Kasım denetimi
bu yüzden hâlâ "Başarısız" görünüyor.

## Durum (karar öncesi çözümleme)

16 maddelik bir denetim dolduruldu. Bir madde başarısız: *"Haşere izi
yok; ilaçlama belgesi güncel" → Hayır* (kritik **değil**). Sonuç:

```
puan 94 · sonuç: failed
```

Panoda Kadıköy satırı, dondurucusu bozulmuş bir şubeyle **aynı**
görünüyor.

## Açık

Kural ile kod başka şey söylüyor ve ikisi de bilinçli yazılmış.

| Kaynak | Ne diyor |
|---|---|
| **BR-07** | "'Başarısız çalıştırma' **yalnızca** BR-06 (kritik madde) ile belirlenir." |
| **FR-0307** | "Kritik madde başarısızsa çalıştırma puandan bağımsız 'Başarısız' işaretlenir." |
| `domain/scoring.py` | `result = "failed" if failed_critical or len(passed) != len(scored)` |
| `evaluate` açıklaması | Yalnızca kritik maddeden söz ediyor; ikinci koşulu **yazmıyor** |
| `test_tc020_puan_yuzdesi` | `assert sonuc.result == "failed"  # puan geçse de bir madde başarısız` |

Yani gereksinim "yalnızca kritik" diyor, kod "herhangi bir madde"
diyor, kodun kendi açıklaması gereksinimi tekrarlıyor ve test kodun
davranışını kilitliyor. Üçü aynı anda doğru olamaz.

## Neden önemli

"Başarısız" bu üründe ucuz bir etiket değil: panoda kırmızı satır,
BR-11'de anında push, aylık raporda başarısızlık sayısı. Her küçük
eksik bunu tetiklerse etiket anlamını yitirir — zamanlayıcının beş gün
kırmızı duran sağlık bayrağıyla aynı hata: hep kırmızı bir bayrak,
bayrak değildir.

Öte yandan "bir maddesi eksik liste tamamlanmış sayılmaz" itirazı da
haklı. Sorun ikisinin **tek bir alana** sıkıştırılmış olması.

## Seçenekler

| | Kurgu | Artısı | Eksisi |
|---|---|---|---|
| **A** | BR-07 uygulanır: `failed` yalnızca kritik maddeyle. Diğer eksikler puana yansır | Gereksinim karşılanır; kırmızı, gerçekten kırmızı olanı gösterir | %60 puanlı bir liste "geçti" görünür |
| **B** | Kod doğru kabul edilir, BR-07 ve FR-0307 düzeltilir | Değişiklik yok, belge gerçeğe uyar | Kritik madde ayrımı anlamsızlaşır: ikisi de aynı sonucu veriyorsa "kritik" işareti yalnızca aksiyon açıyor demektir |
| **C** | Üçüncü durum: `passed` / **`eksikli`** / `failed`. Kritik → `failed`, kritik olmayan eksik → `eksikli` | İki soruyu ayırır; pano üç renk gösterir | Şema, PDF, rapor ve pano değişir; v1 kapsamını büyütür |

## Tavsiye

**A, şimdi; C'yi v1.1 için aç.** Gerekçe: bugün yazılı kural A diyor ve
"kritik" işaretinin bir anlamı olması gerekiyor. C doğru cevap gibi
duruyor ama v1'i genişletiyor; puan zaten eksiği gösteriyor (%94),
yani A ile bilgi kaybolmuyor — yalnızca alarm, alarmlık olana kalıyor.

Hangisi seçilirse `test_tc020_puan_yuzdesi` ve `evaluate` açıklaması
birlikte güncellenmeli.

## İlgili ikinci açık: madde başına aksiyon kuralı

Denetim şablonunun kaynağı (`02-urun/07` §9) 10. madde için
"Hayır → aksiyon (24 sa)" diyor. Bugün böyle bir kural **yok**: BR-10
aksiyonu yalnızca beş tetikten açıyor (kritik madde, yapılamadı,
kaçırılan çalıştırma, sorun bildirimi, elle). Kritik olmayan bir
başarısız cevap aksiyon doğurmuyor.

Bu yüzden 8 Kasım denetiminde ilaçlama belgesi bulgusu kayda geçti ama
takip edilecek bir aksiyona dönmedi. **Kapandı (11 Kasım,
`talimatname-kod@ff7b44b`):** maddeye `action_priority` işareti
eklendi (göç 0012). İşaretli, kritik olmayan bir madde başarısız
cevaplandığında aksiyon açılıyor; önceliği şablon söylüyor, vade
ondan türüyor. Kritik maddede kullanılmıyor — kritik kuralı zaten
kendi aksiyonunu açıyor. İşaretsiz maddede davranış değişmedi.

Denetim şablonunda ilaçlama maddesi `high` (24 sa), kaynak belgenin
istediği gibi. Böylece A'nın bedeli büyük ölçüde kapandı: bulgu
panoda "açık aksiyon" olarak görünüyor, puan eşiğine gerek kalmadan.

Yolda bir kusur daha çıktı: kütüphane kopyası madde alanlarını tek tek
yazıyordu ve yeni alanı **sessizce düşürüyordu** — işaret kütüphanede
duruyor, hesaba kopyalanan şablonda yok oluyordu. Kopya artık alan
listesi tutmuyor (`replace`) ve test alanları `fields()` ile geziyor.
