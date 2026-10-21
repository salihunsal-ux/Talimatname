# ADR-0012 · Barındırma: üretim Türkiye'de, geliştirme ortamları ücretsiz altyapıda; sağlayıcıya kilitlenme yok

- Tarih: 2026-10-21 · Durum: Kabul edildi (sağlayıcı seçimi pilot öncesi kesinleşir; ADR-0003'ü uygular, değiştirmez)

## Bağlam

[ADR-0003](0003-veri-tr-barindirma.md) "üretim verisi Türkiye'de" demişti ama **hangi sağlayıcı, hangi ortam, ne maliyet** sorusu açık kaldı; kodlama hazırlık listesinde de "Barındırma: TR bulut vs AB + standart sözleşme" işaretsiz duruyordu. Sprint 0 bu kararı gerektiriyor: depo, CI, staging ve sağlayıcı hesapları ilk iki haftanın işi.

Üç gerçek kararı şekillendiriyor:

**1 · Veri hacmi küçük.** Pilot ölçeğinde (15 şube × 2 liste × ~3 fotoğraf × 30 gün) ayda ≈ 2.700 kanıt fotoğrafı; cihazda ~300 KB'a sıkıştırıldığı için **≈ 0,8 GB/ay**, 24 aylık saklamayla ~20 GB. Depolama bir maliyet kalemi değil; yük küçük bir uygulama sunucusu, PostgreSQL ve saatlik çalışan zamanlayıcıda.

**2 · Barındırma bir satış argümanı.** Broşür ve tanıtım dosyasında "Veriler Türkiye'de" yazıyor; görüşme notunda `barindirma_sarti` alanı var (yok · tr-sunucu · on-premise · sozlesme-yeter). Henüz 0 görüşme notu olduğu için bu dağılım bilinmiyor — karar, veri gelince gözden geçirilecek biçimde kurulmalı.

**3 · Yığın taşınabilir.** FastAPI + PostgreSQL + Redis + S3 uyumlu nesne depolama (ADR-0002) herhangi bir VPS'te de, yönetilen serviste de çalışır. Kilitlenme, sağlayıcıya özel hizmet kullanıldığında başlar.

Bilgi sınırı: hiper ölçekleyicilerin (AWS/Google/Azure) Türkiye bölgesi durumu ve sağlayıcıların güncel KVKK/DPA belgeleri bu kararın yazıldığı tarihte doğrulanmalıdır; aşağıdaki seçenekler fiyat/konum ölçütleriyle yazılmıştır, marka taahhüdü değildir.

## Seçenekler

| | Nerede | Kaba maliyet (pilot ölçeği) | Artısı | Eksisi |
|---|---|---|---|---|
| **A · Yerli sağlayıcı** (Vargonen, Radore, Turhost, Türk Telekom/Turkcell bulut benzeri) | TR | ₺1.000–3.000/ay | "Veriler Türkiye'de" cümlesi korunur; aktarım izni gerekmez | Yönetilen servis çeşitliliği az; yedek ve izleme bizde |
| **B · AB sağlayıcı + standart sözleşme** (ör. Hetzner) | AB | €5–15/ay | En ucuz ve en iyi fiyat/performans | KVKK yurt dışı aktarım süreci (standart sözleşme + Kurul bildirimi), aydınlatma metni güncellemesi, satışta ek soru |
| **C · Hiper ölçekleyici** | TR bölgesi varsa TR, yoksa AB | Pilotta A'dan pahalı | Yönetilen Postgres/kuyruk, ölçek | Maliyet ve karmaşıklık bu aşamada gereksiz; TR bölgesi doğrulanmalı |

## Karar

1. **Üretim (pilot ve sonrası): A — Türkiye.** ADR-0003 aynen geçerli. Sağlayıcı, pilot sözleşmesinden önce seçilir; ölçüt sırası: KVKK/DPA belgeleri → yedekleme ve kurtarma → destek süresi → fiyat. Nesne depolama aynı ülkede tutulur.
2. **Geliştirme, CI ve demo ortamları ücretsiz ya da AB altyapısında olabilir** — tek şart: **gerçek kişisel veri yok**. Tohum ve fikstür verisi kullanılır (`docs/06-test/03-test-verisi-ve-ortam.md`). Bu, Sprint 0–2'yi sıfıra yakın maliyetle başlatır.
3. **Pilot verisi ücretsiz katmanda durmaz.** Gerekçe teknik değil sözleşmesel: ücretsiz katmanda veri işleme sözleşmesi imzalanamaz, SLA ve yedek garantisi yoktur, servisler uykuya geçebilir (saatlik zamanlayıcı ve bildirim bununla uyuşmaz).
4. **Taşınabilirlik şartı (bağlayıcı):** PostgreSQL standart sürüm, dosyalar **S3 uyumlu API** üzerinden, kuyruk Redis, her şey Docker Compose ile ayağa kalkar. Sağlayıcıya özel hizmet (özel kuyruk, özel kimlik, özel fonksiyon) kullanılmaz. Ortam değişikliği bir haftalık iş olmalıdır.
5. **Yedekleme:** günlük veritabanı yedeği + nesne depolama sürümleme, haftalık geri yükleme provası (Sprint 0 kontrol listesine girer). Yerli sağlayıcıda yönetilen yedek yoksa bu bizim işimizdir — karar maliyetinin görünmeyen kısmı budur.

## Sonuçlar

- Hazırlık listesindeki "Barındırma" maddesi kapanır; Sprint 0 depo/CI/staging işine engel kalmaz.
- Broşür, tanıtım dosyası ve aydınlatma metnindeki "veriler Türkiye'de" ifadesi doğruluğunu korur; **B'ye geçilirse üçü birden güncellenmek zorundadır** (ayrıca Kurul bildirimi ve müşteri bilgilendirmesi).
- Ücretsiz katman kullanımı geliştirme hızını artırır ama **pilot öncesi geçiş** bir iş kalemidir; Sprint 2 sonuna kadar yapılır, Sprint 0'da ortam değişkenleriyle hazırlanır.
- Maliyet, fizibilite modelinde anlamlı bir kalem değil (pilot ölçeğinde aylık birkaç bin lira); karar fiyatla değil, satış ve uyum gerekçesiyle alınmıştır.

## Gözden geçirme tetikleyicileri

- Görüşmelerde `barindirma_sarti` dağılımı: **"sozlesme-yeter" ≥ 15/20** ise B seçeneği (maliyet ve altyapı kalitesi) yeniden değerlendirilir.
- **"on-premise" ≥ 3/20** ise ayrı bir karar gerekir (kurulum modeli v1 kapsamında değildir).
- Hiper ölçekleyicide Türkiye bölgesi doğrulanırsa C yeniden tartılır (yönetilen Postgres + TR konum bir arada).
- Ölçek 100 şubeyi aşarsa ya da müşteri sayısı 10'u geçerse yönetilen servislere geçiş maliyeti yeniden hesaplanır.
