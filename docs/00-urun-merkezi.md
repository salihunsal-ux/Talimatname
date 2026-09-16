# Ürün merkezi — Talimatname

Buradan başla. Bu sayfa ürünün tek sayfalık özeti, karar haritası ve belge navigasyonudur. Ayrıntı için bağlantılara git; burada yalnızca güncel karar ve durum tutulur.

## Ürün özeti

| | |
|---|---|
| Ne | Çok şubeli yeme-içme zincirleri için kanıtlı, tekrarlı talimat listesi (açılış, kapanış, hijyen, soğuk zincir, haftalık temizlik) — mobil personel uygulaması + web yönetim paneli |
| Kimin için | Satın alan: zincir merkezi operasyon müdürü (5–100 şube). Kullanan: şube müdürü ve personel (tablet/telefon), bölge müdürü, kalite sorumlusu |
| Neyin yerine | WhatsApp grupları, kâğıt formlar, Excel, sıcaklık defteri |
| Değer | Her iş kanıtla (fotoğraf, ölçüm, zaman, konum) kapanır; yapılmayan iş sebebiyle merkeze düşer; denetim kaydı 3 dakikada PDF |
| Fiyat çıpası | Zincir: ~₺730/şube/ay (Baz senaryo 15 $) · tekil işletme self-servisi MVP dışı |
| Durum | Doğrulama sprinti kiti hazır (14 Eylül 2026): hafta 0 — hedef liste onayı ve ilk ulaşım mesajları; Sprint 0 paralel başlayabilir |

## Karar haritası

| Karar | Seçim | Kayıt |
|---|---|---|
| Çalışma adı | Talimatname (geçici; isim testi kartları: yap lütfen, tamamlist, tembihle) | [ADR-0001](adr/0001-calisma-adi-talimatname.md), [İsim ve marka](01-strateji/03-isim-ve-marka.md) |
| İlk dikey ve müşteri | Yeme-içme zincirleri; zincir merkezi | [MVP kapsamı §1](02-urun/03-mvp-kapsam.html) |
| v1 çekirdek | Basit, ilk gün kullanılabilir çekirdek: 6 madde türü, sabit kural, 4 rol, sabit eskalasyon + sabah özeti, istisna odaklı ızgara; duyuru/koşul editörü/raporların çoğu v1.1 | [ADR-0008](adr/0008-v1-cekirdek.md), [v1 çekirdek kapsamı](02-urun/06-v1-cekirdek-kapsam.md) |
| Sürüm planı | GA 10. sprint (Alfa 6, Beta 8), 2 sprint tampon | [Backlog ve sprint planı](07-gelistirme/03-backlog-ve-sprint-plani.md) |
| WhatsApp | MVP dışı; push + SMS yedek | [ADR-0006](adr/0006-whatsapp-mvp-disi.md) |
| Kişi skoru | Yok; şube düzeyinde skor, kişi düzeyinde yalnızca gecikme/eksik görünümü | [ADR-0007](adr/0007-kisi-skoru-yok.md) |
| Teknoloji | Flutter mobil, React web, Python/FastAPI, PostgreSQL, S3 uyumlu depolama | [ADR-0002](adr/0002-mobil-flutter-web-react.md), [Teknik mimari](07-gelistirme/01-teknik-mimari.md) |
| Ekip | İki serbest geliştirici + yarı zamanlı tasarımcı; Sprint 2 sonu devam/dur kapısı; Sprint 0 başlangıcı 5 Ekim | [ADR-0009](adr/0009-ekip-modeli-serbest-gelistirici.md), [Seçim süreci](07-gelistirme/07-serbest-gelistirici-secimi.md) |
| Madde kütüphanesi | v1'de şablon düzeyinde kütüphane (8 şablon, kopyala-düzenle); madde kütüphanesi + işletme türü paketleri v1.1'in ilk epic'i; başka dikeyler ve marka kütüphanesi v2 | [ADR-0010](adr/0010-madde-kutuphanesi-v1-1.md), [08-madde-kutuphanesi](02-urun/08-madde-kutuphanesi.md) |
| Barındırma | Türkiye'de yerel bulut (pilot BT şartlarına göre AB + standart sözleşme seçeneği) | [ADR-0003](adr/0003-veri-tr-barindirma.md) |
| Kanıt bütünlüğü | Sunucu zamanı, dosya hash'i, ekle-yalnız olay günlüğü (hash zinciri) | [ADR-0004](adr/0004-kanit-butunlugu-hash-zinciri.md) |
| Tekrar kuralları | RRULE (RFC 5545) + pencere kavramı; gece yarısını aşan pencere aynı iş günü | [ADR-0005](adr/0005-tekrar-kurallari-rrule.md) |
| Biyometri | Yok (KVKK 2026/921); kimlik OTP ve PIN | [KVKK ve güvenlik](04-gereksinimler/06-kvkk-ve-guvenlik.md) |

## Açık kararlar (pilot görüşmelerinden beslenecek)

1. Ortak cihaz (kiosk) modunun Must kalıp kalmayacağı — şubelerde tablet oranı + 3 şubede saha kiosk denemesi ([karar kuralı](01-strateji/dogrulama-sprinti/07-kiosk-saha-denemesi.md))
2. Tekil işletme self-servisi (v1.x?)
3. Franchise sahibi rolü: Gözlemci mi, şube müdürü yetkisi mi
4. Barındırma: TR bulut vs AB + standart sözleşme (pilotların BT şartı)
5. Bluetooth sıcaklık probu (Could → Should?)
6. Kesin marka adı
7. ~~Geliştirme ekibi~~ — karar: iki serbest geliştirici ([ADR-0009](adr/0009-ekip-modeli-serbest-gelistirici.md)); açık kalan: seçim (ilan 17 Eylül → teklif 30 Eylül) ve Sprint 2 sonu devam/dur kapısı

## Belge navigasyonu (okuma sırası)

1. Strateji: [Fizibilite](01-strateji/01-fizibilite.html) → [Pilot görüşme rehberi](01-strateji/02-pilot-gorusme-rehberi.html) → [İsim ve marka](01-strateji/03-isim-ve-marka.md) → [Doğrulama sprinti kiti](01-strateji/dogrulama-sprinti/00-sprint-plani.md) (plan, hedef liste, ulaşım, not şablonu + puanla.py, LOI, gözlem, haftalık rapor)
2. Ürün: [Vizyon ve konumlanma](02-urun/01-urun-vizyonu-ve-konumlanma.md) → [Personalar](02-urun/02-personalar.md) → [MVP kapsamı](02-urun/03-mvp-kapsam.html) → [Yetenek haritası](02-urun/04-yetenek-haritasi.md) → [v1 çekirdek gözden geçirme](02-urun/05-v1-cekirdek-gozden-gecirme.md) → [v1 çekirdek kapsamı](02-urun/06-v1-cekirdek-kapsam.md) (kaynak) → [Şablon kütüphanesi](02-urun/07-sablon-kutuphanesi.md) (8 şablonun maddeleri, taslak) → [Madde kütüphanesi ve paketler](02-urun/08-madde-kutuphanesi.md) (v1.1 ilk epic)
3. Analiz: [Aktörler](03-analiz/01-aktorler.md) → [Use case kataloğu](03-analiz/02-usecase-katalogu.md) → [Use case detayları](03-analiz/03-usecase-detaylari.md) → [Senaryolar](03-analiz/04-senaryolar.md)
4. Gereksinimler: [Fonksiyonel](04-gereksinimler/01-fonksiyonel-gereksinimler.md) → [Fonksiyonel olmayan](04-gereksinimler/02-fonksiyonel-olmayan.md) → [İş kuralları](04-gereksinimler/03-is-kurallari.md) → [Veri modeli](04-gereksinimler/04-veri-modeli.md) → [API taslağı](04-gereksinimler/05-api-taslagi.md) → [KVKK ve güvenlik](04-gereksinimler/06-kvkk-ve-guvenlik.md) → [Hukuki metin taslakları](04-gereksinimler/hukuki/README.md) (aydınlatma, veri işleme sözleşmesi; avukat incelemesi bekliyor)
5. Tasarım: [Ekran envanteri ve navigasyon](05-tasarim/01-ekran-envanteri-ve-navigasyon.md) → [Mobil ekranlar](05-tasarim/02-mobil-ekranlar.html) → [Web ekranlar](05-tasarim/03-web-ekranlar.html) → [Tasarım sistemi](05-tasarim/04-tasarim-sistemi.md) → [Blok 8 prototipi](05-tasarim/05-prototip/README.md) → [Kanıt raporu örnekleri](05-tasarim/06-kanit-raporu/README.md) (çalıştırma PDF'i, aylık özet, sıcaklık günlüğü) → [Tanıtım broşürü ve ekran tasarımları](05-tasarim/07-brosur/README.md)
6. Test: [Strateji](06-test/01-test-stratejisi.md) → [Kabul test senaryoları](06-test/02-kabul-test-senaryolari.md) → [Test verisi ve ortam](06-test/03-test-verisi-ve-ortam.md) → [Cihaz matrisi](06-test/04-cihaz-matrisi.md) → [Pilot UAT](06-test/05-pilot-uat-plani.md)
7. Geliştirme: [Kodlama hazırlık indeksi](07-gelistirme/00-kodlama-hazirlik-indeksi.md) → [Teknik mimari](07-gelistirme/01-teknik-mimari.md) → [Repo ve ortam](07-gelistirme/02-repo-ve-ortam-kurulumu.md) → [Backlog ve sprint planı](07-gelistirme/03-backlog-ve-sprint-plani.md) → [DoR/DoD](07-gelistirme/04-tanimlar-dor-dod.md) → [Sprint 0 ve teknik spike'lar](07-gelistirme/05-sprint0-ve-teknik-spike.md) → [Serbest geliştirici seçimi](07-gelistirme/07-serbest-gelistirici-secimi.md) → [İlk gün paketi](07-gelistirme/06-ilk-gun-paketi.md) → [İçe aktarma şablonları](07-gelistirme/sablonlar/)

## Kimlik şeması (izlenebilirlik)

| Önek | Nesne | Tanımlandığı belge |
|---|---|---|
| CAP-xx | Yetenek (capability) | 02-urun/04 |
| A-xx | Aktör | 03-analiz/01 |
| UC-xx | Kullanım senaryosu (use case) | 03-analiz/02, 03 |
| S-xx | Uçtan uca senaryo | 03-analiz/04 |
| FR-xxx | Fonksiyonel gereksinim | 04-gereksinimler/01 |
| NFR-xx | Fonksiyonel olmayan gereksinim | 04-gereksinimler/02 |
| BR-xx | İş kuralı | 04-gereksinimler/03 |
| SCR-M-xx / SCR-W-xx | Mobil / web ekranı | 05-tasarim/01 |
| TC-xxx | Kabul test senaryosu | 06-test/02 |
| EP-xx / ST-xxx | Epic / kullanıcı hikâyesi | 07-gelistirme/03 |

İzlenebilirlik zinciri: CAP → UC → FR → SCR → TC → ST. Her FR en az bir UC'ye, her TC en az bir FR'ye bağlıdır.

## Dış bağlantılar

- Ürün dosyası (tek sayfa, tüm belgeler): https://claude.ai/code/artifact/bb2f5c58-4b72-4fc5-80c9-0baef13cd2b4 — depoda `index.html`, `python build_index.py` ile yenilenir
- Fizibilite (canlı sayfa): https://claude.ai/code/artifact/7624c049-c18f-45d6-b7c5-c750bcd7798f
- MVP kapsamı (canlı sayfa): https://claude.ai/code/artifact/c7feaa95-847e-473e-bd87-8f95646bb515
- Pilot görüşme rehberi (canlı sayfa): https://claude.ai/code/artifact/7dda6bc8-bf82-4c28-a572-b6572652e421
- Logo tuvali (düzenlenebilir): https://claude.ai/code/artifact/96cf8183-a732-4988-acd2-731b83545950
- Blok 8 prototipi (telefonda aç): https://claude.ai/code/artifact/229e7396-313c-487b-9a31-ada9caa05e69
- Yönetici web prototipi (LOI turu, masaüstü): https://claude.ai/code/artifact/96276ca2-4d59-49b2-8bb2-50ec77e394f5
- Tanıtım broşürü ve ekran tasarımları (düzenlenebilir tuval): https://claude.ai/artifact/3LpwvVXZczJMNLqnKrBVn2
