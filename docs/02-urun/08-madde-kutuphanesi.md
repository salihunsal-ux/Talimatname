# Madde kütüphanesi ve işletme türü paketleri (v1.1 — CAP-20)

Karar: [ADR-0010](../adr/0010-madde-kutuphanesi-v1-1.md). Bu belge özelliğin ürün tanımıdır: kavramlar, kullanıcı akışı, içerik planı, sürümleme, aşamalar. v1'de yalnızca veri modeli hazırlığı yapılır; özellik v1.1'in ilk epic'idir (EP-13).

## 1. Kavramlar

| Kavram | Tanım | v1'de karşılığı |
|---|---|---|
| **Kütüphane maddesi** | Talimatname'nin sağladığı, hesaplar arası paylaşılan, sürümlü tek talimat: başlık, tür, önerilen ayarlar (zorunlu / fotoğraf / kritik / sıcaklık aralığı), alan etiketi, ipucu, mevzuat notu | Yok — maddeler şablonun içinde |
| **Kütüphane şablonu (set)** | Kütüphane maddelerinden kurulmuş sıralı, bölümlü liste (bugünkü 9 şablon) | 8 şablon (FR-0311) |
| **Paket** | Bir işletme türü için şablon seti + varsayılan planlar (kafe paketi: 9 şablon, 89 madde, planlar) | Yok — sihirbaz tek şablonla başlar |
| **Hesap maddesi / hesap şablonu** | Zincirin kopyası; kaynağını hatırlar (`kaynak_madde_id`, `kaynak_surum`); serbestçe değiştirilir | Kopyala-düzenle (kaynak yalnızca şablon düzeyinde) |
| **Kendi maddesi** | Zincirin sıfırdan yazdığı madde; kaynağı yok; istenirse hesabın kendi kütüphanesine "kaydet" | Editörde madde ekle (yalnızca o şablonda) |

Personel bu kavramların hiçbirini görmez; listeyi görür. Kütüphane merkezin (Yönetici) editöründe yaşar.

## 2. Kullanıcı akışları (Selin — operasyon müdürü)

1. **Paketle başla.** Sihirbaz adım 2: "İşletme türü: kafe / hızlı servis / restoran / fırın-pastane" → paket önerilir (şablon listesi ve planlar); "yalnızca kapanışla başla" seçeneği korunur (v1 davranışı).
2. **Kütüphaneden madde ekle.** Şablon editöründe "+ Madde" → sekmeler: *Kütüphane* (alan ve tür filtresi, arama: "gaz vanası") · *Hesabım* (kendi kaydettikleri) · *Yeni*. Kütüphane maddesi eklenince ayarları önerilen değerlerle gelir; değiştirilebilir.
3. **Kendi maddesini kaydet.** Editörde yazılan maddeyi "hesap kütüphanesine kaydet" → diğer şablonlarda yeniden kullanılır; şube türü etiketi verilebilir.
4. **Kaynak güncellemesi.** Talimatname bir kütüphane maddesini güncellediğinde (ör. kızartma yağı eşiği tebliğle değişti) ilgili hesap şablonlarında "kütüphane maddesi güncellendi — farkı gör · uygula · yoksay" bandı; uygulama yeni taslak sürüm açar (FR-0301), yayın kararı zincirde. Zincir maddeyi kendi değiştirdiyse fark yan yana gösterilir.
5. **Şablonu paket olarak sakla (hesap içi).** Zincirin kendi şablon seti yeni şubeye tek tıkla uygulanır ("Kadıköy setini Bornova'ya uygula") — bugün plan kopyalamayla yapılıyor; paket bunu adlandırır.

## 3. İçerik planı (yazılımdan önce)

- **Kaynak:** 02-urun/07 şablon kütüphanesi (73 madde + 3 talimat) tohum; pilot şubelerin duvar listeleri ve sıcaklık defterleri (gözlem formu §1); görüşme notlarındaki "bizde bu var" maddeleri; Gıda Hijyeni Yönetmeliği / HACCP ön koşul programları; TGK kızartma yağı tebliği.
- **Hedef:** v1.1'de 200–300 madde, 4 paket (kafe, hızlı servis, restoran, fırın-pastane), 12–16 şablon.
- **Madde şeması:** id · başlık · tür · alan (bar / mutfak / salon / tuvalet / depo / kasa / dış alan / araç) · önerilen ayarlar · sıcaklık aralığı (varsa) · ipucu (personele tek cümle) · mevzuat notu (merkeze) · işletme türü etiketleri · sürüm · değişiklik notu.
- **Yazım kuralları:** 02-urun/07 tasarım kuralları (Evet = uygun; ≤ 16 madde/liste; kritik yalnızca gıda güvenliği, iş güvenliği, para; fotoğraf yalnızca tartışılan işler).
- **Kim:** PO + kalite/gıda güvenliği danışmanı (yarı zamanlı, Sprint 8–12); her madde bir kez sahada görülmüş olmalı ("masa başı madde" yok).
- **Dil:** Türkçe; i18n hazır alanlar (v1.1 sonrası).

## 4. Sürümleme ve kaynak takibi

- Kütüphane maddesi sürümlüdür (`surum`); hesap maddesi `kaynak_madde_id` + `kaynak_surum` taşır; kopyada değişiklik kaynağı koparmaz, `degistirildi=true` işaretler.
- Kütüphane güncellemesi hesap şablonunu **kendiliğinden değiştirmez** (yayındaki sürüm değişmez ilkesi, FR-0301); yalnızca öneri bandı çıkar.
- Kütüphane şablonu güncellenince madde ekleme/çıkarma önerisi de aynı bantla gelir; zincir tek tek kabul eder.
- Kütüphane içeriği ürün deposunda sürümlü veri dosyası olarak yaşar (JSON/YAML), tohum betiğiyle yüklenir; değişiklik günlüğü tutulur.

## 5. Aşamalar

| Aşama | Kapsam | Ne zaman |
|---|---|---|
| v1 (şimdi) | Veri modelinde alanlar (boş); 9 şablon içeriği sahada doğrulanır; etiket şeması belirlenir | Sprint 0–9 |
| v1.1 · EP-13 | Kütüphane maddesi varlığı ve tohum; editörde "kütüphaneden ekle" ve "hesap kütüphanesine kaydet"; işletme türü paketleri ve sihirbaz adımı; kaynak güncelleme bandı; 200–300 madde, 4 paket | Pilot geri bildirimi sonrası ilk sıra (S11+) |
| v2 | Başka dikeyler için paketler (perakende, eczane, spor salonu, otel mutfağı) — her biri kendi doğrulamasıyla; **marka kütüphanesi** (franchise merkezi → bayiler, yerel alanlar hariç kilitli); Ş-8 AI taslak kütüphane maddeleriyle eşleştirme | Franchise sinyaline ve dikey kararına göre |

Yapılmayacaklar: topluluk/pazaryeri; kullanıcı maddelerinin hesaplar arası paylaşımı; madde başına ücretlendirme.

## 6. Fonksiyonel gereksinim taslakları (v1.1)

| FR | Gereksinim |
|---|---|
| FR-0313 | Kütüphane maddesi: hesaplar arası paylaşılan, sürümlü, etiketli (alan, işletme türü) madde tanımı; önerilen ayarlarla gelir; yalnızca Talimatname içerik ekibi düzenler. |
| FR-0314 | Şablon editöründe "kütüphaneden madde ekle": alan/tür/işletme türü filtresi ve arama; eklenen madde `kaynak_madde_id` ve `kaynak_surum` taşır; ayarları değiştirilebilir. |
| FR-0315 | Hesap kütüphanesi: zincir kendi maddesini kaydeder, etiketler, diğer şablonlarında kullanır; yalnızca o hesapta görünür. |
| FR-0316 | Kaynak güncelleme: kütüphane maddesi/şablonu yeni sürüm alınca ilgili hesap şablonlarında bant; fark görünümü; "uygula" yeni taslak sürüm açar; "yoksay" kaydedilir. Yayındaki sürüm hiçbir zaman kendiliğinden değişmez. |
| FR-0317 | İşletme türü paketleri: paket = sıralı şablon seti + varsayılan planlar; sihirbaz adım 2'de tür seçimi paketi önerir; tek şablonla başlama seçeneği kalır. |
| FR-0318 | Hesap içi set uygulama: bir şubenin şablon+plan seti başka şube(ler)e tek işlemle uygulanır; çalıştırmalar 7 gün ileri üretilir. |

## 7. Açık sorular (pilotta)

- Zincirler kütüphaneden mi başlıyor, kendi listelerini mi yazıyor? (Blok 2 "listeler nerede yazılı" cevapları)
- Hangi alan etiketleri gerçekten kullanılıyor; istasyon kavramıyla (v1.1) birleşir mi?
- Kaynak güncelleme bandı işe yarıyor mu, yoksa gürültü mü? (pilotta bir kez tebliğ değişikliği simüle edilir)
- Franchise merkezleri "marka kütüphanesi"ni satın alma nedeni sayıyor mu? (Blok 6)
