# Rakip özellik denetimi: robotPOS Operation / Franchise Manager karşısında v1 kapsamı

22 Ekim 2026. Kaynak: [robotPOS incelemesi](https://claude.ai/artifact/AC5g1eZ4hdh4fZhDff29Ax) ve [AdamPos incelemesi](https://claude.ai/artifact/55z4QkQZhanoVafKghhZoU) (Ekim 2026, kamuya açık tanıtımlar; ürünler denenmedi). Soru: **rakiplerin yaptığı ve bizim "v1'de muhakkak olmalı" dediğimiz bir şey eksik mi?**

Karşılaştırma iki ürünle yapıldı, çünkü yalnızca bu ikisi bizim işimize giriyor:
- **Operation Manager** — mobil saha/bayi denetimi: form, anlık fotoğraf, belge, rapor, aksiyon takibi. Liste fiyatı **$45/şube/ay + $250 kurulum**. Doğrudan rakip.
- **Franchise Manager** — royalty, bayi başvurusu, sözleşme, eğitim, belge, görev, destek (15+ modül). **$75/şube/ay.** Büyük kısmı bizim ürün tanımımızın dışında.

## 1. Operation Manager'ın anlattığı her özellik bizde var mı?

| robotPOS Operation Manager | Bizde | Not |
|---|---|---|
| Mobil denetim formu | **v1** | Sürümlü şablon, 6 madde türü + talimat (CAP-03) |
| Anlık fotoğraf | **v1 (daha güçlü)** | Yalnızca uygulama içi kamera, sunucu damgası, SHA-256, ham + damgalı kopya (ADR-0004). Rakiplerin hiçbirinde kanıt bütünlüğü anlatılmıyor |
| Belge toplama ve takibi | **v1** | Belge takvimi E-12: şube × belge türü, 30/7 gün uyarısı, süresi geçende aksiyon |
| Denetim raporu | **v1** | Çalıştırma PDF'i (doğrulama kodlu) + aylık tek sayfa özet + dönem PDF'i |
| Aksiyon takibi | **v1** | Açık/kapalı, not zorunlu kapanış, sabit vadeler, sabit eskalasyon |
| Denetim verisinin merkeze akması | **v1** | İstisna odaklı pano, çalıştırma detayı, sabah özeti |
| Periyodik denetim planı | **v1** | RRULE + pencere + tolerans (ADR-0005) — rakiplerde bu derinlikte anlatılmıyor |
| Şube/bölge/merkez yetki kademeleri | **v1** | 4 rol × kapsam |
| Çevrimdışı çalışma (mobil) | **v1** | Kuyruk + idempotent senk. robotPOS'ta hibrit olan **kasa**; Operation Manager için çevrimdışı anlatılmıyor |
| Denetim puanı | **v1 (kısmi)** | Yüzde puan + kritik kuralı var; **ağırlık ve eşik v1.1** (FR-0306) |
| Denetim sonunda imza | **v1.1** | CAP-17 gözden geçirme ve imza |
| Anomali uyarısı (iptal/iade/kasa farkı) | **yok** | POS verisi gerektiriyor; bizde POS entegrasyonu v2 (CAP-19) |

**Sonuç: Operation Manager'ın anlattığı işlevlerin tamamı v1'de karşılanıyor**, ikisi kısmi (puan eşiği, imza) ve biri bilinçli kapsam dışı (POS anomalisi).

## 2. Ama bir kullanım senaryosu eksik: bölge müdürünün denetim ziyareti

Operation Manager'ın sattığı asıl iş **"denetçi şubeye gider, formu doldurur, puan çıkar"**. Bizim 8 şablonumuzun tamamı ise **şube personelinin kendi kendini kontrolü** (açılış, kapanış, hijyen, soğuk zincir, derin temizlik, fritöz, kasa devri, teslimat kabul). Senaryo listemizde de (S-01…S-05) denetim ziyareti yok.

Teknik olarak v1 bunu **yeni gereksinim olmadan** yapabiliyor:

- Şablon: denetim formu = normal şablon (fotoğraf zorunlu, kritik, puan) — CAP-03.
- Plan: kapsam = şube(ler), tekrar = aylık, **atama = rol: bölge müdürü** (FR-0508).
- Mobil: çalıştırma bölge müdürüne atandığı için "Bugün" ekranında görünür (FR-0601) ve orada doldurulur.
- Çıktı: çalıştırma PDF'i = denetim raporu; başarısız maddeler → aksiyon (FR-0405).

Eksik olan üç küçük parça:

| | Eksik | Maliyet | Karar |
|---|---|---|---|
| 1 | **9. şablon: "Bölge müdürü şube denetimi"** (şablon kütüphanesinde yok) | içerik işi, ~1 gün (PO) | v1'e eklenecek |
| 2 | **Çok şubeli "Bugün"**: 25 şubeye bakan bölge müdürünün ekranında çalıştırmalar şubeye göre gruplanmalı | ~1 gün (mobil, ST-144 ile birlikte) | v1'e eklenecek, FR notu |
| 3 | Denetim puanı **eşiği** ("%80 altı → aksiyon") ve şube müdürü **imzası** | eşik ~1 gün, imza daha büyük | **v1.1'de kalıyor**; pilotta sorulacak |

Bu, ürüne yeni bir yetenek eklemiyor; **var olan yeteneği rakibin sattığı işe isimlendiriyor.** Satış tarafındaki değeri büyük: "sizin bölge müdürünüz zaten bu uygulamayla denetim yapıyor, ayrıca denetim yazılımı almanız gerekmiyor."

## 3. Franchise Manager: bilinçli olarak kapsam dışı

| robotPOS Franchise Manager | Bizim konumumuz |
|---|---|
| Royalty hesabı, reklam fonu | **Kapsam dışı.** Finans/muhasebe ürünü; POS cirosu ve faturalama gerekir |
| Bayi başvurusu, onboarding, kiralama | **Kapsam dışı** |
| Bayi ve tedarikçi sözleşmesi | **Kısmen** (şube belgeleri E-12); bayi sözleşmesi yönetimi yok |
| Eğitim ve el kitabı modülü | **Kısmen** (duyuru + okudum onayı v1.1); eğitim modülü yok → [büyüme listesi](04-buyume-firsatlari.md) |
| Şube görevleri, zamanında yapılmayana eskalasyon | **v1 — bu bizim çekirdeğimiz**, onlarda yan modül |
| Şube cari hesabı, borç tahsilatı, B2B sipariş, merkez mutfak | **Kapsam dışı** (B2B Manager'ın işi) |

Franchise Manager'ın yaptığı işin %80'i bizim ürün tanımımızın dışında. Bu, kapsam kararının (ADR-0008, basit ilk sürüm) **doğrulanmasıdır**, boşluk değil: aynı pazarda farklı iş yapıyoruz.

## 4. Açık kararı etkileyen bulgu: franchise sahibi rolü

robotPOS'ta **5 kademeli yetki** ve "franchise alan yalnızca kendi şubesini görür" ayrımı var; bizde [açık karar 3](../00-urun-merkezi.md) olarak duruyor (Gözlemci mi, şube müdürü yetkisi mi). Rakibin bunu ayrı bir kademe olarak kurmuş olması, franchise ağlarında bu ihtiyacın gerçek olduğuna dair **dolaylı kanıt**. Görüşme rehberine soru olarak girmeli; karar hâlâ sahadan gelecek veriye bağlı.

## 5. Fiyat çıpası

| | Liste fiyatı |
|---|---|
| Operation Manager (saha denetimi) | **$45/şube/ay** + $250 kurulum |
| Franchise Manager | $75/şube/ay + $250 kurulum |
| aiR Intelligence | $25/şube/ay |

robotPOS fiyatını açıkça yayınlayan tek firma; bu, bizim fiyat görüşmesinde kullanacağımız **tek kamuya açık çıpa**. Kendi fiyatımızı hâlâ broşüre yazmıyoruz (van Westendorp koruması), ama pilot görüşmesinde "bugün alternatif ne tutuyor" sorusunun cevabı artık belgeli. Kur etkisi ayrıca hesaplanmalı: fiyat USD cinsinden, KDV hariç.

## 6. Ne yapılacak

1. [x] 9. şablon ("Bölge müdürü şube denetimi") şablon kütüphanesine eklenecek — v1 içeriği.
2. [x] "Bugün" ekranında çok şubeli kullanıcı için şube gruplaması — FR notu + ST-144 kartına ek kriter.
3. [ ] Görüşme rehberine iki soru: franchise sahibi rolü; "bugün denetim için ne kullanıyorsunuz, ne ödüyorsunuz".
4. [ ] Puan eşiği ve imza: v1.1 sırasında, pilot sinyaline göre.
5. [ ] Rakip izleme: robotPOS Operation Manager'ın çevrimdışı davranışı ve denetim puanı modeli demo talebiyle doğrulanmalı (incelemede 9 açık soru listelendi).
