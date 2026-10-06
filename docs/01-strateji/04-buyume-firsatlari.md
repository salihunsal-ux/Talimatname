# Büyüme fırsatları ve boşluklar — park listesi

Tarih: 16 Eylül 2026. Bu bir plan değil, **bir kenarda duran liste**: v1 çekirdeği (ADR-0008) ve v1.1 sırası değişmez; buradaki bir madde yol haritasına ancak bir kapı (K1/K2/K3) veya pilot sinyaliyle girer. Puanlar yargısal (1 düşük – 3 yüksek): **K** kazanç etkisi (ARPU, yeni gelir kalemi veya pazar), **R** rekabet etkisi (fark yaratır / rakibi dengeler), **E** efor (3 = ağır). Rakip bilgisi fizibilite §rakipler ve 2026 öncesi kamuya açık bilgiden; fiyat/ARPU tahminleri varsayımdır, teklif ve pilot verisiyle düzelir. Baz ARPU: ~₺730 (15 $)/şube/ay.

## A · Aynı müşteriye daha fazla (ARPU ↑)

| # | Fırsat | Neden | Kazanç | K | R | E | Tetikleyici / kanıt |
|---|---|---|---|---|---|---|---|
| A1 | **Sıcaklık sensörleri (kablosuz) + alarm** | Soğuk zincir zaten kritik madde; sensör manuel ölçümü kaldırır, gece alarmı verir. Mitti ve Jolt'un ARPU çarpanı budur | Şube başına 4–6 sensör × donanım + aylık abonelik; ARPU 2–4× (marj donanımda düşük) | 3 | 3 | 3 | Blok 6 prob talebi ≥ 1/3; pilotta aralık dışı olay sayısı; kalite sorumlusu talebi |
| A2 | **Tarih etiketi yazıcı entegrasyonu** | Açılış/kapanışta "açık ürün etiketlendi" maddesi var; etiket yazıcı (Jolt modeli) kanıtı fiziksel yapar | Donanım + sarf marjı; kilitli müşteri | 2 | 2 | 2 | Şube ziyaretinde elle etiket yazımı gözlemi |
| A3 | **Duyuru, okundu onayı, mikro-eğitim** (D-1…D-4, v1.1) | Prosedür değişikliği + 2 dakikalık eğitim kartı; Connecteam'in çekirdeği | Kademe farkı (Pro): +%20–30 ARPU | 2 | 2 | 2 | Blok 5 "acil duyuru nasıl" cevapları; v1.1 sırası |
| A4 | **Denetim formu (skorlu inspection)** — bölge müdürü ziyaret denetimi, kalite iç denetimi | Mitti/SafetyCulture'ın ana ürünü; bizde "liste" var, "denetim" yok; bölge müdürü ziyaretini ürünün içine alır | Kademe farkı; bölge müdürü lisansı | 3 | 3 | 2 | Blok 1 ziyaret sıklığı; pilotta bölge müdürü "ziyarette ne kullanıyorum" sorusu |
| A5 | **Sorun → bakım iş emri, ekipman kartı** | "Ekipman arızalı" en sık yapılamadı sebebi; ekipman geçmişi (buzdolabı 2'nin 3. arızası) | Ek modül; servis firmalarıyla kanal | 2 | 2 | 2 | Pilotta yapılamadı sebep dağılımı (ekipman ≥ %20) |
| A6 | **Franchise: marka kütüphanesi + bayi uyum görünümü** (E-10) | Merkez standart setini dağıtır, bayi uyumunu görür; franchise sözleşmesindeki "sistem zorunluluğu" dağıtım kanalıdır | Bayi başına lisans; zincir başına 50–300 şube tek satışla | 3 | 3 | 2 | Blok 6 franchise soruları; ≥ 2 franchise zinciri "merkez görsün" derse |
| A7 | **WhatsApp kanalı** (ADR-0006 ertelemesi) | Benimseme engelini düşürür: bildirim WhatsApp'tan, cevap uygulamada | Doğrudan gelir yok; kayıp azaltır | 1 | 2 | 2 | Pilotta push okunma oranı < %60 ise |
| A8 | **POS entegrasyonu** (Z raporu otomatik, kasa devri) ve **İK/PDKS** (vardiya → atama) | Kasa devri listesindeki sayıları otomatik doldurur; vardiya bazlı tekrar (P-8) | Kurumsal kademe; POS ortaklığı kanal | 2 | 2 | 3 | Blok 4 POS/İK cevapları; 2 POS sağlayıcısıyla ortaklık görüşmesi |
| A9 | **AI fotoğraf ön kontrolü** | Kanıt fotoğrafında "çöp alanı boş mu, tezgâh temiz mi" ön değerlendirme; yöneticinin galeriyi taramasını azaltır | Premium; yanlış pozitif riski, KVKK dikkat (kişi tespiti yok) | 2 | 2 | 3 | 10k+ kanıt fotoğrafı birikince; kalite ekibinin inceleme süresi ölçümü |
| A10 | **Sesle tamamlama / eldivenli mod** | Mutfakta eldivenle dokunmatik zor; "yapıldı" sesle | Benimseme; fark yaratıcı küçük özellik | 1 | 2 | 2 | Kiosk saha denemesinde yanlış dokunuş sayısı |
| A11 | **Çok dil** (personel: Arapça, Farsça, İngilizce; arayüz) | Blok 5 yabancı personel oranı; şablon maddeleri çevrilir | Zorunluluk kademesi; İstanbul dışı ve turistik bölge | 1 | 1 | 2 | Blok 5 oranı ≥ %15 |
| A12 | **Benchmark (anonim kıyas)** | "Sektörde kapanış zamanında tamamlanma %81, siz %74" — yalnızca bizde olabilir | Elde tutma + üst kademe; veri kazancı | 2 | 3 | 2 | ≥ 30 zincir, ≥ 500 şube verisi |
| A14 | **Üretim–satış mutabakatı (L0–L1, donanımsız)** | Kayıt dışı satışın imzası: üretilen > satılan. Sayım ve fire maddeleri + POS adedi + eşik ve aksiyon; haftalık kör malzeme sayımı ikinci kaynak | Fark parayla ifade edilir; ROI doğrudan. Pro kademesi | 3 | 3 | 2 | Blok 3 “üretilen–satılan tutuyor mu” cevabı: ≥ 5 zincir somut tutar söylerse ([ADR-0011](../adr/0011-uretim-satis-mutabakati.md), [S-11](../03-analiz/04-senaryolar.md)) |
| A15 | **Kamera ile üretim sayımı (L2)** | Fırın ağzı/tezgâh kamerası; adet ve tip otomatik. Personelin beyanından bağımsız sayaç | ARPU çarpanı; donanım + abonelik | 3 | 3 | 3 | A14 sinyali güçlü + bir vardiyalık görüntüyle ölçüm spike'ı (hedef ±%3) |
| A16 | **POS–kamera olay eşleştirme (L3)** | Çekmece açılışı / tezgâh etkileşimi ↔ fiş kaydı (±30 sn); yurt dışında olgun kategori (exception-based reporting) | Kurumsal kademe; en güçlü kanıt | 2 | 3 | 3 | A15 + POS entegrasyonu (A8); KVKK ölçülülük değerlendirmesi |
| A17 | **Müşteriye görünen “son kontrol” kartı** | Tuvalet/masa QR'ı: müşteri okutunca “en son 14:20'de kontrol edildi” görür (kişi adı yok) | Güven ve pazarlama etkisi; personel disiplinini artırır | 2 | 3 | 1 | Pilotta saatlik hijyen listesi düzenli işliyorsa; şube müdürü “müşteri sorar mı” tepkisi |
| A18 | **Dış servis için misafir aksiyon kapatma** | Servis firması bağlantıyla gelir, fotoğraf ve not ekleyip aksiyonu kapatır; hesap açmaz | Aksiyon döngüsünün gerçek tıkanma noktası; kurumsal kademe | 2 | 2 | 2 | Pilotta aksiyonların kaçı dış servis bekliyor (ölçülecek) |
| A19 | **Tekrar eden sorun görünümü** | “Bakırköy’de dondurucu 3 haftada 4. kez”: aynı madde + aynı şube kalıbı; kök neden alanı | Tek tek kapanan aksiyonların gizlediği kalıbı açar; R-3'ün üstünde kavram | 2 | 2 | 1 | Pilot 4. hafta: tekrar eden madde sayısı ≥ 5 |
| A20 | **Açılış saati uyumu** | “Kapı açıldı” maddesinin zaman damgasından şube açılış gecikmesi raporu | Franchise merkezleri için somut; veri zaten var | 1 | 2 | 1 | Franchise görüşmelerinde talep gelirse |
| A13 | **Denetçi doğrulama sayfası (herkese açık)** | PDF'teki doğrulama kodu ile denetçi/franchise merkezi kaydı çevrimiçi doğrular; U-1'in dışa açılması | Güven; satışta fark | 1 | 3 | 1 | Pilot kalite sorumlusu "denetçi kabul eder mi" cevabı |
| A21 → **E-13** | **Denetim dosyası + denetçiye zaman sınırlı misafir bağlantısı** · *6 Eki 2026: kapsam belgesine **v1.1 adayı** olarak alındı (FR-1221, FR-1313, TC-127); sıraya girmesi K1 sinyaline bağlı* | Ürünün satış cümlesi “denetim geldiğinde üç dakika” ama bugün üç ayrı PDF var; klasörü toplamak hâlâ müdürün işi. Tek pakette son 90 gün: ölçüm günlüğü + ilgili çalıştırmalar + belgeler + rastgele kanıt örnekleri + doğrulama kodu. Denetçiye ya da franchise merkezine **hesap açmadan 48 saatlik salt-okunur bağlantı**. A13'ün (doğrulama sayfası) doğal büyüğü | Yeni gelir kalemi değil, **kapanış oranı**: satın alma gerekçesini tek ekrana indirir; franchise merkezine ikinci kullanıcı kapısı | 2 | 3 | 1 | “Son denetimde sizden ne istediler, hazırlamanız kaç saat sürdü?” → ≥ 2 saat diyen ≥ 8/20 görüşme |
| A22 | **Geri çağırma / acil kampanya modu** | Tedarikçi lot geri çağırdığında ya da mevzuat bir gecede değiştiğinde zincire anlık tek seferlik görev: “şu lotu raftan çek, fotoğrafla, adedini gir”; merkez şube şube kapanışı canlı izler, sonunda tek kanıt dosyası. FR-0512 (tek seferlik liste) altyapısının üstüne kriz başlığı | Olay başına değer çok yüksek, sıklık düşük; sözleşme yenilemesinde “bir kez işe yaradı” etkisi | 2 | 2 | 2 | Son iki yılda ürün çekme/geri çağırma yaşadım diyen ≥ 5/20; ya da zincirde kalite müdürü kadrosu |
| A23 | **Kişi bazlı zorunlu belge takibi** (portör, hijyen eğitimi, iş sağlığı) | Belge takvimi (E-12) şube bazlı; denetçinin ilk istediği ise personel sertifikası. Kişi–belge–bitiş tarihi, süresi dolanda uyarı ve vardiyaya yazma ikazı. **Sınır: yalnızca “belge var/yok + bitiş tarihi” tutulur; tahlil sonucu, sağlık verisi ve belge görseli tutulmaz** (KVKK m.6 özel nitelikli veri — hukuk görüşü olmadan başlamaz). ADR-0007'nin kişi skoru yasağı değişmez | Denetim hikâyesini tamamlar; şube müdürünün elindeki Excel'i ürüne alır | 2 | 2 | 1 | “Portör ve hijyen belgelerini kim takip ediyor, nerede duruyor?” → Excel/kâğıt diyen ≥ 10/20 |
| A24 | **Liste yükü analizi** | Benimsemeyi öldüren şey liste şişmesidir: müşteri 15 maddeyi 40'a çıkarır, personel bırakır. Madde başına gerçek süre ve “arka arkaya üç saniyede onaylanan maddeler” verisi zaten toplanıyor; merkeze “bu liste 18 dakika, şu 6 madde okunmadan onaylanıyor” raporu ve madde çıkarma önerisi | Churn savunması; K3 ölçümünü (tamamlanma oranı) doğrudan yukarı çeker | 1 | 2 | 1 | Pilotta ortalama liste süresi > 10 dk ya da tamamlanma oranı < %85 |
| A25 | **Yumuşak başlangıç** (ilk 10–14 gün eskalasyon ve puan kapalı) | Pilotun en kırılgan anı ilk iki haftadır; ilk günlerde eskalasyon yağmuru “bu sistem bizi dövüyor” algısı yaratır. Ölçüm açık, ceza kapalı; sürenin sonunda merkez “başlangıç raporu” görür ve kademeli açar | Pilot başarı oranı; satışta “personel direnir” itirazını düşürür | 1 | 1 | 1 | LOI görüşmelerinde “personel direnir” itirazı ≥ 5/20 ya da pilot ilk haftasında şube müdürü şikâyeti |
| A26 | **Kanıt örneklemesi (merkez kalite güvencesi)** | “Fotoğraf var ama kimse bakmıyor” — kanıtın değeri bakılmadıkça sıfırdır. Haftada N rastgele kanıt merkeze düşer; onay/ret; ret → yeniden çekim aksiyonu ve o maddenin örnekleme oranı artar | Kanıt kalitesini korur; A9 (AI ön kontrol) gelene kadar insanlı çözüm, denetim hikâyesini güçlendirir | 1 | 2 | 1 | Pilotta işaretli kanıt oranı > %5 ya da merkezin “fotoğraflara kim bakacak” sorusu |

## B · Yeni segmentler (SAM ↑)

Fizibilite ilk dikeyi yeme-içme (SAM ≈ 99.700 lokasyon) seçti; aşağıdakiler ayrı sayım ve saha doğrulaması ister. Ortak nokta: **tekrarlı liste + fotoğraf/ölçüm kanıtı + çok şube**. Şablon kütüphanesi (ADR-0010) her dikeyin giriş kapısıdır.

| # | Segment | Uyum | Farklı olan | K | R | E | Ne zaman |
|---|---|---|---|---|---|---|---|
| B1 | **Perakende zincirleri** (market, giyim, kozmetik) | Açılış/kapanış, görsel düzen fotoğrafı, kasa devri, teslimat kabul birebir | Sıcaklık yok; planogram/raf fotoğrafı var; mağaza sayıları büyük | 3 | 2 | 1 (yazılım) / 2 (içerik) | GA sonrası ilk yeni dikey adayı; 3 zincirle görüşme |
| B2 | **Eczane ve ilaç depoları** | Soğuk zincir (aşı/insülin) kayıt zorunluluğu | Mevzuat ağır; tek şubeler çok (self-servis gerekir) | 2 | 2 | 2 | Sensör (A1) ile birlikte |
| B3 | **Otel housekeeping** | Oda kontrol listesi + fotoğraf; kat sorumlusu = şube müdürü | Oda = istasyon (v1.1); yüksek sezon devri | 2 | 1 | 2 | İstasyon kavramı v1.1'de |
| B4 | **Spor salonu, güzellik, klinik hijyen** | Saatlik hijyen listesi, ekipman kontrolü | Sağlık verisi yok (dikkat); küçük zincirler | 1 | 1 | 1 | Şablon paketiyle deneme |
| B5 | **Fabrika vardiya kontrolleri (5S), depo/lojistik** | Vardiya başı/sonu kontroller, teslimat kabul | Endüstriyel rakipler güçlü; farklı satış | 2 | 1 | 2 | Sonra |
| B6 | **Tekil işletme self-servisi** (kapsam dışı) | Kafe sahibi tek şube | Fizibilitede LTV/CAC zayıf (2,7); destek yükü | 1 | 1 | 2 | Yalnızca kredi kartı + sıfır destek modeliyle; K2 sonrası talep sayısına göre |
| B7 | **Yurt dışı (Türkçe konuşulan / bölge)** | tamamlist adı bunun için düşünülmüştü | Yerelleştirme + ödeme + mevzuat | 2 | 1 | 3 | 24. ay kapısından sonra |

## C · Gelir kalemleri

| # | Kalem | Model | Not |
|---|---|---|---|
| C1 | Kurulum ve eğitim bedeli | Şube başına tek seferlik (Jolt 500–600 $ alıyor) | Blok 7 sorusu: "kurulum bedava olmalı mı"; pilotta ölçülür |
| C2 | Tablet paketi | Cihaz satışı (düşük marj) veya aylık kiralama (+₺300–400/şube) | Kiosk kararı ve donanım ortaklığı (fizibilite: "tablet oranı < %50 ise paket") |
| C3 | Kademeler | Temel (v1) / Pro (duyuru, denetim formu, raporlar) / Kurumsal (API, SSO, 2FA, SLA, saklama uzatma) | v1.1'den itibaren; fiyat farkı van Westendorp bandına göre |
| C4 | Sensör aboneliği | Donanım + veri + alarm, sensör başına aylık | A1 |
| C5 | Franchise lisansı | Bayi başına; marka merkezi öder veya bayiye yansıtır | A6 |
| C6 | Saklama uzatma ve arşiv dışa aktarımı | 24 ay → 5 yıl | Kurumsal |
| C7 | Danışman kanalı | Kalite/gıda güvenliği danışmanları şablon paketi yazar, komisyon veya bayilik | ADR-0010 içerik ihtiyacıyla örtüşür |
| C8 | Beyaz etiket / gömülü | POS veya İK yazılımı bizim motoru kendi ürününde satar | A8; kanal ile çakışır — dikkat |

## D · Dağıtım ve kanal

- **POS / İK yazılımı ortaklıkları:** Blok 4 "POS'un görev modülü var mı" cevabı tehdit de fırsat da olabilir: modülü zayıfsa entegrasyon + tavsiye ortaklığı.
- **Kalite danışmanları ve denetim şirketleri:** müşteriye zaten gidiyorlar; "kanıt sistemi" tavsiye ederler; C7.
- **UFRAD ve franchise fuarları:** A6 ile birlikte; franchise merkezleri tek satışta 50–300 şube.
- **Kanıt PDF'inde marka:** her denetimde denetçi Talimatname'yi görür — A13 ile viral.
- **Tedarikçi zincirleri:** teslimat kabul listesi tedarikçiyle paylaşılırsa tedarikçi ödeyen ikinci taraf olabilir (uzak).

## E · Boşluklar ve riskler (bizde olmayan, rakipte olan; zayıf yanlar)

| Boşluk | Kimde var | Ne kadar önemli | Cevabımız |
|---|---|---|---|
| Skorlu denetim/inspection formu | Mitti (çekirdek), Zenput, Xenia | Yüksek — bölge müdürü ziyareti ürünün dışında kalıyor | A4 v1.1/v2 adayı; v1'de "liste" bilinçli seçim |
| Sensörler ve etiket yazıcı | Jolt, Mitti | Yüksek (ARPU) | A1, A2 — pilot sinyaline göre |
| Duyuru, eğitim, sohbet, vardiya planı | Connecteam | Orta — biz "tek iş" konumundayız; sohbet bilerek yok | A3 v1.1; sohbet ve vardiya asla |
| Ücretsiz kademe | Mitti/SafetyCulture free tier | Orta — küçük zincirde "bedava olsun" itirazı | Self-servis yok (B6); değer kanıtı PDF + kanıt |
| Kişi bazlı skor | Jolt satış argümanı | Düşük–orta — bazı alıcılar ister | ADR-0007 bilinçli hayır; şube skoru + "kanıt kişiyi korur" mesajı |
| Entegrasyonlar (POS, İK, muhasebe) | Küresel oyuncular | Orta (100+ şube) | A8 kurumsal kademe |
| Çok dil, iOS kiosk kısıtları | Küreseller | Düşük (TR) | A11 ihtiyaç halinde |
| Büyük zincir gereksinimleri (SSO, ISO 27001, SLA) | Küreseller | Orta — 100+ zincir bu turda hedef değil | Kurumsal kademe; ISO 27001 GA + 12 ay |
| Yerel rakip (CheckMaster) fiyat ve saha satışı | CheckMaster | Bilinmiyor — görüşmelerde sorulacak | Blok 4 sorusu; farkımız kanıt bütünlüğü + içerik + kiosk |
| Donanım tedariki (tablet) | — | Orta — kiosk Must kalırsa lojistik | C2 ortaklık |
| Küreselin Türkçeleşmesi | Mitti/Connecteam | Orta–uzun vade | Hız + yerel içerik + mevzuat + saha; benchmark verisi (A12) |

## F · Sıralama önerisi (şimdilik)

Kazanç × rekabet / efor ile ilk beş — hepsi bir sinyale bağlı:

1. **A14 Üretim–satış mutabakatı (L0–L1)** — donanımsız, v1.1'e girebilir, argümanı doğrudan para: “açıklanamayan 9 adet”. *Sinyal:* Blok 3'teki yeni soru.
2. **A6 Franchise marka kütüphanesi** — tek satışta çok şube; ADR-0010'un doğal devamı. *Sinyal:* Blok 6.
3. **A4 Denetim formu** — Mitti'nin çekirdeğini bizim "liste + kanıt" motoruna eklemek; bölge müdürünü ürüne bağlar. *Sinyal:* pilot bölge müdürü kullanımı.
4. **A1 Sensörler** — ARPU çarpanı; donanım işi olduğundan ortakla. *Sinyal:* prob talebi, aralık dışı olay sayısı.
5. **B1 Perakende paketi** — en düşük eforlu yeni dikey (aynı motor, yeni içerik). *Sinyal:* GA sonrası 3 perakende görüşmesi.
6. **A13 Doğrulama sayfası** — ucuz, güven ve pazarlama etkisi büyük. *Sinyal:* kalite sorumlularının denetçi sorusu.

**5 Ekim 2026 eklemesi (A21–A26).** İlk beşi değiştirmiyorum; ama **A21 (denetim dosyası)** ve **A23 (kişi belgesi)** ucuz olmaları ve aynı satış cümlesini tamamlamaları nedeniyle A13 ile birlikte düşünülmeli — üçü tek bir “denetim günü” paketidir. **A24/A25/A26** yeni gelir değil **pilotu ayakta tutan** mekanizmalar; sinyal beklemeden, pilot verisi kötüye giderse devreye alınır.

Fizibilite modeline etkisi: hiçbiri Baz senaryoya girmedi; A1/A6/C3 gerçekleşirse ARPU varsayımı (15 $) yukarı revize edilir — 24. ay kapısında yeniden koşulur.

## Güncelleme kuralı

Her görüşmede bu listeye giren/çıkan bir madde varsa haftalık raporun "kapsam kararlarına etki" tablosuna yazılır; listeye madde eklemek serbest, yol haritasına almak kapıya bağlı.
