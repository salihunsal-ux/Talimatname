# Şablon kütüphanesi — v1'in 9 şablonu (taslak, sahada doğrulanacak)

Tarih: 15 Eylül 2026. Kapsam belgesi (02-urun/06, Ş-6) v1'de **9 hazır şablon** der; bu belge o şablonların madde madde içeriğidir. Durum: **taslak** — pilot görüşmelerinde (Blok 8 prototipiyle) ve şube ziyaretlerinde (gözlem formu §1–2) düzeltilir; her görüşmede eklenen/silinen maddeler alttaki değişiklik günlüğüne işlenir. Blok 8 prototipindeki kapanış listesi bu belgedeki 1 numaralı şablondur.

## Tasarım kuralları

- **Madde türleri (v1):** onay · çoktan seçmeli (Evet / Hayır / Uygun değil) · sayı + birim · sıcaklık (°C, kabul aralığı) · metin · fotoğraf (1–3) · talimat (cevapsız). Ayarlar: zorunlu · fotoğraf zorunlu · kritik (sıcaklıkta min–maks).
- **Sayı maddesi de aralık ister (uygulamadan gelen not, 24 Ekim 2026).** Yukarıdaki satır aralığı yalnızca sıcaklığa bağlıyor ama yayın doğrulaması (FR-0312) `sayı` türünde de alt/üst sınır arıyor; sınırsız bir sayı puanlanamıyor. Kütüphanede "Kasa açılış tutarı" maddesine bu yüzden geniş bir aralık (0–100.000 ₺) verildi. **Karar gerekiyor:** ya bu satır "sayı ve sıcaklıkta min–maks" olarak düzeltilir, ya FR-0312 sayı türünde aralığı isteğe bağlı sayar.
- **Tek sabit kural (FR-0405):** "Hayır / Uygun değil / aralık dışı" → fotoğraf + not zorunlu; madde kritikse aksiyon (şube müdürü, 4 saat). Bu yüzden çoktan seçmeli sorular **"Evet" her zaman uygun durum** olacak şekilde yazılır ("Gaz vanası kapatıldı mı?" — evet iyi). "Uygun değil" = madde bu şubede geçerli değil (ekipman yok).
- **Uzunluk:** kapanış ≤ 16, diğerleri ≤ 12 cevaplı madde; hedef süre kapanış 6–8 dk, saatlik 1–2 dk. Personel listeyi telefonla/tabletle eldiven çıkarmadan bitirebilmeli.
- **Fotoğraf zorunlu** yalnızca sonradan tartışılan işlerde (çöp, zemin, teşhir, kepenk, Z raporu, irsaliye); liste başına ≤ 4.
- **Kritik** yalnızca gıda güvenliği, iş güvenliği ve para: sıcaklık, gaz, haşere, kasa farkı; liste başına ≤ 4. Kritik madde başarısız → çalıştırma "başarısız".
- **Talimat satırı** cevap istemez; bir uyarıyı veya başka listeye yönlendirmeyi taşır.
- **Pencere ve tolerans** sabitler tablosundan (kapanış 120 dk · saatlik 0 · haftalık 240 dk); diğerleri aşağıda plan bazında. Şube çalışma saatinden türetme (P-2) kullanılır: "kapanıştan 60 dk önce", "açılıştan 45 dk önce".
- **Şubeye uyarlama:** ekipman sayısı (dolap, fritöz), tedarik günleri, saatler şube planında değişir; şablon "kopyala-düzenle" ile çoğaltılır (Ş-6). İstasyon bağı v1.1.
- **Sıcaklık aralıkları:** soğuk muhafaza 0–4 °C (teşhir vitrini 0–5), dondurucu −30…−18 °C, sıcak tutma 65–90 °C, teslimatta soğuk 0–5 °C ve donuk ≤ −15 °C (araçta tolerans). Kızartma yağı: toplam polar madde ≤ %24 kullanım, %25 üstü değiştir (Türk Gıda Kodeksi kızartma yağları tebliği). Bu değerler şablonda varsayılandır; zincirin HACCP planı farklıysa merkez değiştirir.

Tablolarda: **Z** zorunlu · **F** fotoğraf zorunlu · **K** kritik.

## 1. Kapanış (kafe / hızlı servis)

| | |
|---|---|
| Amaç | Gün sonunda hijyen, gıda güvenliği ve güvenli kapanış; ertesi sabah "dün gece" özetinin kaynağı |
| Tekrar | Günlük, şube kapanış saatinden 60 dk önce başlar; pencere kapanış + 90 dk (ör. 22:00–01:30); tolerans 120 dk |
| Atama | Şubedeki herkes görür, biri tamamlasın (ilk açan alır) |
| Süre hedefi | 6–8 dk · 15 cevaplı madde + 1 talimat · 4 fotoğraf · 4 kritik |

**A · Bar ve mutfak**

| # | Madde | Tür | Z | F | K | Not |
|---|---|---|---|---|---|---|
| 1 | Espresso makinesi geri yıkama yapıldı; süt hortumları ve buhar çubuğu temizlendi | onay | Z | | | |
| 2 | Kahve makinesi ve öğütücü temizlendi | fotoğraf (1) | Z | F | | Makine önden |
| 3 | Süt dolabı sıcaklığı | sıcaklık 0–4 °C | Z | | K | |
| 4 | Mutfak buzdolabı sıcaklığı | sıcaklık 0–4 °C | Z | | K | Şubede dolap sayısı kadar çoğaltılır |
| 5 | Dondurucu sıcaklığı | sıcaklık −30…−18 °C | Z | | K | |
| 6 | Açık ürünler etiketlendi (ürün adı, açılış tarihi) ve dolaba kaldırıldı | çoktan seçmeli | Z | | | Hayır → foto + not |
| 7 | Fritöz kapatıldı, yağ süzüldü, kapağı kapatıldı | çoktan seçmeli | Z | | | Fritöz yoksa "uygun değil" yerine madde şube planından çıkarılır |
| 8 | Tezgâh, kesme yüzeyleri ve lavabo dezenfekte edildi; bulaşık bitti, makine kapağı açık | onay | Z | | | |

**B · Salon ve tuvalet**

| # | Madde | Tür | Z | F | K | Not |
|---|---|---|---|---|---|---|
| 9 | Masalar, sandalyeler ve servis istasyonu silindi | onay | Z | | | |
| 10 | Zemin süpürüldü ve paspaslandı | fotoğraf (1) | Z | F | | Salon genel |
| 11 | Tuvaletler temizlendi; sabun, kâğıt havlu, tuvalet kâğıdı dolduruldu | onay | Z | | | |
| 12 | Çöpler dışarı çıkarıldı, kovalara yeni poşet takıldı | fotoğraf (1) | Z | F | | Çöp alanı |

**C · Güvenlik ve kapanış**

| # | Madde | Tür | Z | F | K | Not |
|---|---|---|---|---|---|---|
| — | Kasa kapanışını "Kasa devri" listesinde tamamlayın | talimat | | | | |
| 13 | Gaz vanası kapatıldı | çoktan seçmeli | Z | | K | Hayır → aksiyon (4 sa) + anında bildirim |
| 14 | Ocak, fırın, ızgara, tost makinesi kapalı ve fişleri çekili; ışıklar, klima, tabela kapalı; su vanası kapalı | onay | Z | | | |
| 15 | Kapı ve kepenk kilitlendi, alarm kuruldu | fotoğraf (1) | Z | F | | Kepenk dışarıdan |

## 2. Açılış

| | |
|---|---|
| Amaç | Güne hazır, güvenli ve temiz açılış; gece yapılamayanların sabah devralınması |
| Tekrar | Günlük, açılıştan 45 dk önce; pencere açılış + 30 dk (ör. 07:45–09:00); tolerans 60 dk |
| Atama | Şubedeki herkes, biri tamamlasın |
| Süre hedefi | 5 dk · 13 madde · 1 fotoğraf · 2 kritik |

Listenin başında sistem **"Dün gece"** bloğunu gösterir (E-3): dün kapanışta yapılamayan ve başarısız maddeler, açık aksiyonlar. Madde değildir, cevap istemez.

| # | Madde | Tür | Z | F | K | Not |
|---|---|---|---|---|---|---|
| 1 | Süt dolabı sıcaklığı | sıcaklık 0–4 °C | Z | | K | |
| 2 | Mutfak buzdolabı sıcaklığı | sıcaklık 0–4 °C | Z | | K | |
| 3 | Tarihi geçmiş veya etiketsiz ürün yok (SKT kontrolü yapıldı) | çoktan seçmeli | Z | | | Hayır → foto + not (imha) |
| 4 | Espresso makinesi açıldı, ısındı, ilk shot atıldı ve döküldü | onay | Z | | | |
| 5 | Su filtresi ve buz makinesi çalışıyor; buz haznesi temiz | onay | Z | | | |
| 6 | Günlük ön hazırlık (şurup, süt, sos, ekmek) tamamlandı | onay | Z | | | |
| 7 | Teşhir vitrini yerleştirildi; etiketler ve fiyatlar tam | fotoğraf (1) | Z | F | | Vitrin önden |
| 8 | Salon ve dış oturma alanı temiz, masalar düzenli | onay | Z | | | |
| 9 | Tuvalet açılış kontrolü (temiz, sabun, kâğıt) | onay | Z | | | |
| 10 | Müzik, ışık, klima ve tabela açık | onay | | | | |
| 11 | Personel üniformalı, saç ve sakal düzenli, eller yıkandı | çoktan seçmeli | Z | | | |
| 12 | Kasa açılış tutarı (para üstü) sayıldı | sayı + birim (₺) | Z | | | |
| 13 | Kapı açıldı | onay | Z | | | Zaman damgası = fiili açılış saati |

## 3. Saatlik tuvalet ve hijyen kontrolü

| | |
|---|---|
| Amaç | Gün içinde müşteri alanının ve el hijyeninin sürekliliği |
| Tekrar | 10:00–22:00 arası her 2 saat (hızlı serviste her saat); pencere 15 dk; tolerans 0 |
| Atama | Rol: salon personeli |
| Süre hedefi | 1–2 dk · 7 madde · fotoğraf isteğe bağlı · kritik yok |

| # | Madde | Tür | Z | F | K | Not |
|---|---|---|---|---|---|---|
| 1 | Klozet, lavabo ve ayna temiz | çoktan seçmeli | Z | | | |
| 2 | Sabun, kâğıt havlu / el kurutma, tuvalet kâğıdı dolu | çoktan seçmeli | Z | | | |
| 3 | Zemin kuru, çöp kovası boş | çoktan seçmeli | Z | | | |
| 4 | Koku ve havalandırma uygun | çoktan seçmeli | Z | | | |
| 5 | Genel görünüm | fotoğraf (1) | | | | İsteğe bağlı |
| 6 | El yıkama ve eldiven değişimi yapıldı | onay | Z | | | |
| 7 | Salon masaları ve servis istasyonu temiz; şeker, peçete, karıştırıcı dolu | onay | Z | | | |

## 4. Soğuk zincir sıcaklık kaydı

| | |
|---|---|
| Amaç | HACCP sıcaklık günlüğü; denetimde dönem PDF'i (R-4) bu listeden üretilir |
| Tekrar | Günde 3 kez: 08:00, 14:00, 20:00; pencere 60 dk; tolerans 30 dk |
| Atama | Şubedeki herkes, biri tamamlasın |
| Süre hedefi | 2 dk · 5 ölçüm + 1 talimat · tamamı kritik |

| # | Madde | Tür | Z | F | K | Not |
|---|---|---|---|---|---|---|
| 1 | Süt dolabı | sıcaklık 0–4 °C | Z | | K | |
| 2 | Mutfak buzdolabı | sıcaklık 0–4 °C | Z | | K | Dolap sayısı kadar çoğaltılır |
| 3 | Teşhir vitrini | sıcaklık 0–5 °C | Z | | K | |
| 4 | Dondurucu | sıcaklık −30…−18 °C | Z | | K | |
| 5 | Sıcak tutma (benmari/ısıtıcı) | sıcaklık 65–90 °C | | | K | Yalnızca sıcak servis olan şubede |
| — | Aralık dışı ölçümde ürünleri başka dolaba taşıyın ve şube müdürüne haber verin; sistem aksiyonu otomatik açar | talimat | | | | |

## 5. Haftalık derin temizlik

| | |
|---|---|
| Amaç | Günlük temizliğin ulaşmadığı yerler; yangın (davlumbaz) ve haşere riski |
| Tekrar | Haftalık, Pazartesi 14:00–17:00 (veya şubenin kapalı/sakin günü); tolerans 240 dk |
| Atama | Şubedeki herkes, biri tamamlasın (bölüm paylaşımı v1.1) |
| Süre hedefi | 60–90 dk iş, 4 dk kayıt · 10 madde · 3 fotoğraf · 1 kritik |

| # | Madde | Tür | Z | F | K | Not |
|---|---|---|---|---|---|---|
| 1 | Davlumbaz filtreleri söküldü, yağı çözüldü, takıldı | fotoğraf (1) | Z | F | | Filtre temizken |
| 2 | Fritöz tamamen boşaltıldı, kazan kaynatıldı ve durulandı | çoktan seçmeli | Z | | | Fritöz yoksa planda yok |
| 3 | Buzdolabı ve dolap içleri boşaltılıp silindi, contalar temizlendi | fotoğraf (1) | Z | F | | |
| 4 | Depo rafları düzenli; ilk giren ilk çıkar (FIFO) uygulanıyor; yerde ürün yok | çoktan seçmeli | Z | | | |
| 5 | Bulaşık makinesi kireç çözme yapıldı, filtreler temizlendi | onay | Z | | | |
| 6 | Espresso makinesi grup başlıkları/contaları ve öğütücü hazneleri derin temizlendi | onay | Z | | | |
| 7 | Klima filtreleri temizlendi | onay | | | | |
| 8 | Yağ tutucu (gres kapanı) boşaltıldı | çoktan seçmeli | Z | | | |
| 9 | Haşere izleme: tuzaklar kontrol edildi, iz yok | çoktan seçmeli | Z | | K | Hayır → foto + not + aksiyon |
| 10 | Duvarlar, kapılar, süpürgelikler ve çöp alanı yıkandı | fotoğraf (1) | Z | F | | Çöp alanı |

## 6. Fritöz yağı kontrolü ve değişimi

| | |
|---|---|
| Amaç | Kızartma yağı kalitesi (polar madde) ve atık yağ kaydı; yağ değişiminin kanıtı |
| Tekrar | Günlük, yoğunluk öncesi 15:00–17:00; tolerans 120 dk |
| Atama | Rol: mutfak |
| Süre hedefi | 3 dk · fritöz başına 3 madde (örnek 2 fritöz) + 1 madde + 1 talimat · 1 kritik/fritöz |

| # | Madde | Tür | Z | F | K | Not |
|---|---|---|---|---|---|---|
| — | Toplam polar madde %25'i geçen yağ kullanılamaz (TGK kızartma yağları tebliği); ölçüm cihazı/şeridiyle ölçün | talimat | | | | |
| 1 | Fritöz 1 — polar madde ölçümü | sayı + birim (%) | Z | | | |
| 2 | Fritöz 1 — yağ kullanılabilir (polar ≤ %24; köpük, koyu renk, duman yok) | çoktan seçmeli | Z | | K | Hayır → foto + not + aksiyon: değiştir |
| 3 | Fritöz 1 — yağ değiştirildiyse yeni yağ ve tarih etiketi | fotoğraf (1) | | | | Yalnızca değişim gününde |
| 4 | Fritöz 2 — polar madde ölçümü | sayı + birim (%) | Z | | | |
| 5 | Fritöz 2 — yağ kullanılabilir | çoktan seçmeli | Z | | K | |
| 6 | Fritöz 2 — yağ değiştirildiyse yeni yağ ve tarih etiketi | fotoğraf (1) | | | | |
| 7 | Atık yağ bidonunda yer var (dolmadan toplama firması çağrıldı) | çoktan seçmeli | Z | | | |

## 7. Kasa devri

| | |
|---|---|
| Amaç | Vardiya sonu ve gün sonu nakit/POS mutabakatı; devralanın kaydı |
| Tekrar | Günlük 2 kez: vardiya değişimi 16:00 ve kapanış (kapanış listesinden talimatla yönlendirilir); pencere 30 dk; tolerans 60 dk |
| Atama | Rol: kasa sorumlusu |
| Süre hedefi | 4 dk · 7 madde · 1 fotoğraf · 1 kritik |

| # | Madde | Tür | Z | F | K | Not |
|---|---|---|---|---|---|---|
| 1 | Z raporu / vardiya raporu alındı | fotoğraf (1) | Z | F | | Rapor fişi |
| 2 | Kasadaki nakit sayıldı | sayı + birim (₺) | Z | | | |
| 3 | POS gün sonu (batch) alındı | çoktan seçmeli | Z | | | |
| 4 | Nakit ile rapor arasında fark yok (± ₺50 içinde) | çoktan seçmeli | Z | | K | Hayır → foto + not + aksiyon (şube müdürü) |
| 5 | Para üstü kasası ayrıldı — tutar | sayı + birim (₺) | Z | | | |
| 6 | Nakit kasaya/çantaya kilitlendi, anahtar teslim edildi | onay | Z | | | |
| 7 | Devralan kişi | metin | Z | | | Ad; vardiya değişiminde |

## 8. Teslimat kabul

| | |
|---|---|
| Amaç | Tedarikçi teslimatında soğuk zincir, miktar, tarih ve ambalaj kontrolü; red kaydı |
| Tekrar | Tedarik günleri (ör. Pzt / Çar / Cum) 07:00–11:00; tolerans 60 dk. Teslimat gelmeyen gün şube müdürü listeyi "yapılmayacak" işaretler (isteğe bağlı başlatma v1.1, Y-11) |
| Atama | Rol: mutfak veya şube müdürü |
| Süre hedefi | 4 dk · 9 madde · 1 fotoğraf · 3 kritik |

| # | Madde | Tür | Z | F | K | Not |
|---|---|---|---|---|---|---|
| 1 | İrsaliye ile gelen ürünler eşleşti (çeşit ve adet) | çoktan seçmeli | Z | | | Hayır → foto + not (eksik/fazla) |
| 2 | Araç kasası sıcaklığı (soğuk ürün varsa) | sıcaklık 0–5 °C | | | K | Araç göstergesi |
| 3 | Soğuk ürün sıcaklığı (örnek ürün, prob veya kızılötesi) | sıcaklık 0–5 °C | Z | | K | |
| 4 | Donuk ürün sıcaklığı | sıcaklık −30…−15 °C | | | K | Donuk ürün varsa |
| 5 | Ambalajlar sağlam; hasar, sızıntı, buz çözülme izi yok | çoktan seçmeli | Z | | | |
| 6 | Son kullanma / tavsiye edilen tüketim tarihi: en yakın tarih ≥ 3 gün | çoktan seçmeli | Z | | | |
| 7 | İrsaliye | fotoğraf (1) | Z | F | | Okunaklı |
| 8 | Ürünler 15 dk içinde soğutucuya/depoya yerleştirildi (FIFO) | onay | Z | | | |
| 9 | Tüm ürünler kabul edildi (red yok) | çoktan seçmeli | Z | | | Hayır → foto + not: reddedilen ürünler ve sebep |

## 9. Şube denetimi (denetçi)

| | |
|---|---|
| Amaç | Bölge müdürünün şube ziyaretinde standart denetim: hijyen, gıda güvenliği, görünüm, belge ve personel; puanlı rapor ve aksiyon. [Rakip denetimi](../01-strateji/05-rakip-ozellik-denetimi.md) §2 ile eklendi — robotPOS Operation Manager'ın sattığı iş |
| Tekrar | Aylık (ör. ayın ilk 10 günü içinde), pencere iş günü 09:00–19:00; tolerans 0. Plansız ziyaret için tek seferlik liste (FR-0512) |
| Atama | **Rol: denetçi** (A-11) — şube personeline görünmez, çalıştırma şubeye bağlıdır. Bölge müdürü de doldurabilir; denetçi ayrı rol çünkü planı değiştiremez, listeyi iptal edemez (`talimatname-kod@e98d80d`) |
| Durum | **Yazıldı** — kütüphanede `sube-denetimi`. Listenin başında altı satırlık **denetim protokolü** var (talimat satırı): habersiz gel, önce gözlem, sıra, ölçümü kendin yap, başarısız maddede ne yazılır, kapanış görüşmesi |
| Süre hedefi | 12–15 dk · 16 madde · 6 fotoğraf · 3 kritik |

| # | Madde | Tür | Z | F | K | Not |
|---|---|---|---|---|---|---|
| 1 | Giriş, vitrin ve tabela: temiz, aydınlatma çalışıyor, kampanya görseli güncel | fotoğraf (1) | Z | F | | Cepheden |
| 2 | Salon ve müşteri alanı düzeni (masa, sandalye, servis istasyonu) | fotoğraf (1) | Z | F | | |
| 3 | Tuvalet: temizlik, sarf malzeme, kontrol çizelgesi dolu | çoktan seçmeli | Z | | | Hayır → foto + not |
| 4 | Personel kıyafeti, bone/eldiven, kişisel hijyen | çoktan seçmeli | Z | | | |
| 5 | El yıkama istasyonu: sabun, kâğıt, sıcak su | onay | Z | | | |
| 6 | Soğutucu sıcaklıkları (örnek 2 dolap) | sıcaklık 0–4 °C | Z | | K | Şubenin kendi kaydıyla karşılaştırılır |
| 7 | Dondurucu sıcaklığı | sıcaklık −30…−18 °C | Z | | K | |
| 8 | Açık ürün etiketleme ve SKT kontrolü (rastgele 5 ürün) | çoktan seçmeli | Z | | K | Hayır → foto + not, ürün adıyla |
| 9 | Depo düzeni ve FIFO; yerden yükseklik | fotoğraf (1) | Z | F | | |
| 10 | Haşere izi yok; ilaçlama belgesi güncel | çoktan seçmeli | Z | | | Hayır → aksiyon (24 sa). **Yazıldı:** madde `action_priority="high"` (BR-10 takip işareti) |
| 11 | Yasal belgeler yerinde ve geçerli (ruhsat, hijyen eğitimi, ilaçlama, yangın tüpü) | çoktan seçmeli | Z | | | Belge takvimiyle (E-12) karşılaştırılır |
| 12 | Mutfak ekipmanı çalışıyor; davlumbaz ve filtre temiz | fotoğraf (1) | Z | F | | |
| 13 | Son 7 günün kapanış listeleri tamamlanmış (uygulamadan kontrol) | çoktan seçmeli | Z | | | Hayır → not: hangi gün, sebep |
| 14 | Kasa ve fiyat kontrolü: menü fiyatları merkez listesiyle aynı | çoktan seçmeli | Z | | | Hayır → foto + not |
| 15 | Şube müdürüyle görüşme: açık sorunlar ve ihtiyaçlar | metin | Z | | | Serbest not |
| 16 | Genel değerlendirme fotoğrafı (mutfak genel) | fotoğraf (1) | Z | F | | |

Puan bilgi amaçlıdır (FR-0306); **eşik ve ağırlık v1.1**'dedir. Kritik madde başarısızsa çalıştırma "Başarısız" olur ve aksiyon açılır (FR-0307, FR-0405). Denetim sonunda şube müdürünün imzası v1.1 (CAP-17).

## Sahada doğrulanacak sorular

- Kapanış listesi gerçek şubede kaç dakika sürüyor; hangi madde "gereksiz", hangisi eksik? (gözlem formu §2)
- Fotoğraf zorunlu madde sayısı 4 fazla mı? Personel hangi fotoğrafı çekmek istemiyor?
- Soğuk zincir günde 3 ölçüm mü, 2 mi? Kaç dolap? Prob var mı, dolap göstergesi mi okunuyor?
- Yağ ölçümü şeritle mi yapılıyor, hiç yapılmıyor mu? (yapılmıyorsa "sayı" maddesi çıkar, "gün sayısı" kalır)
- Kasa devri ayrı liste mi, kapanışın parçası mı? Franchise şubelerde merkez nakit görmek istiyor mu?
- Teslimat günleri sabit mi? Tedarikçi çeşitliliği (merkez depo mu, yerel mi)?
- Bölge müdürü denetimi bugün nasıl yapılıyor: kâğıt form, Excel, ayrı yazılım? Aylık mı, habersiz mi? Puan/eşik kullanılıyor mu?
- Denetim sonunda şube müdürünün imzası isteniyor mu (v1.1 kararı buna bağlı)?

## Değişiklik günlüğü

| Tarih | Kaynak | Değişiklik |
|---|---|---|
| 2026-09-15 | İlk taslak | 8 şablon, 73 cevaplı madde + 3 talimat satırı; kapanış şablonu Blok 8 prototipine işlendi |
