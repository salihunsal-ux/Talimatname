# Çalıştırma sonucu: "Başarısız" ne demek?

- Tarih: 2026-11-11 · Durum: **karar bekliyor**
- İlgili: BR-06, BR-07, FR-0306, FR-0307, BR-10, BR-11
- Bulunduğu yer: demoya denetim şablonu girilirken (8 Kasım turu)

## Durum

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
**takip edilecek bir aksiyona dönmedi** — denetçi elle açabilir, kural
açmıyor. Seçenek: maddeye "başarısızsa aksiyon aç (öncelik, vade)"
bayrağı eklemek (şablon alanı + BR-10'a tetik). v1.1 işi gibi duruyor;
v1'de denetçi elle açar.
