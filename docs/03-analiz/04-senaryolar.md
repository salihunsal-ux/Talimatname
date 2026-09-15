# Uçtan uca senaryolar

> **v1 notu (ADR-0008):** S-05'teki duyuru-onay adımları v1.1; S-06'daki "herkes tamamlasın" v1'de "biri tamamlasın + kilit" olarak koşulur; S-01 adım 5'teki puan %88 artık bilgi amaçlıdır — çalıştırma "başarısız" olmasının nedeni kritik maddedir. S-02'de Bakırköy için eskalasyon v1'de sabit kurala göre koşar: 03:30 şube müdürüne push, bölge müdürü ve yöneticiye 07:00 sabah özeti (gece SMS yok; SMS yalnızca kritik madde). Diğer senaryolar v1'de aynen geçerlidir.

Senaryo = birden çok use case'i gerçek bir iş günü akışında birleştiren, test edilebilir hikâye. Her senaryo örnek veriyle (06-test/03) çalıştırılır; kabul testleri (06-test/02) bu adımlara bağlanır. Örnek zincir: **Kahve Durağı** — 25 şube, 3 bölge; Kadıköy şubesi 09:00–24:00 açık.

## S-01 · İlk kurulumdan ilk kapanışa (Gün 0 → Gün 1)

Aktörler: Cem (A-01), Selin (A-02), Ayşe (A-05), Emre (A-06). UC-01, UC-02, UC-05, UC-06, UC-07, UC-04, UC-08.

1. Cem davet bağlantısıyla girer, sihirbazda 25 şubeyi Excel'le yükler; 2 satır hatalı (eksik saat dilimi) → düzeltir, yeniden yükler. **Beklenen:** 3 bölge, 25 şube, 100 istasyon kayıtlı.
2. Selin kütüphaneden "Kapanış — kafe" şablonunu kopyalar; "Kahve makinesi temizlendi" maddesini fotoğraf zorunlu, "Buzdolabı sıcaklığı"nı 0–4 °C kritik yapar; yayınlar. **Beklenen:** Şablon v1 yayında.
3. Selin plan kurar: her gün 22:00–01:30, tolerans 2 sa, atanan "Kapanış sorumlusu" rolü, biri tamamlasın; eskalasyon varsayılan. **Beklenen:** 7 günlük önizlemede 25 × 7 çalıştırma, pazar kapalı olan 2 şube için pazar boş.
4. Ayşe Kadıköy tabletini QR ile kiosk yapar; Emre davet SMS'iyle girer, PIN belirler.
5. 22:00'de Emre tablette PIN ile geçer, listeyi yapar: buzdolabı 6 °C → uyarı, fotoğraf + not, kritik aksiyon açılır; zemin için "yapılamadı: malzeme yok"; 23:41 gönderir. **Beklenen:** Durum "Tamamlandı", puan %88 → "Başarısız çalıştırma"; 2 aksiyon (kritik 4 sa, orta 72 sa) Ayşe'ye atanmış; push gitmiş.
6. Ertesi sabah Selin ızgarada Kadıköy'ü kırmızı görür, hücreye tıklar, kanıtları ve olay izini inceler.

## S-02 · Sıradan bir gece: 25 şube, 3 sonuç

UC-07, UC-08, UC-09, UC-13, UC-15.

- 22 şube pencere içinde tamamlar (yeşil). Beşiktaş'ta Wi-Fi kesik: Emre'nin listesi 23:10'da yerelde tamamlanır, 07:30'da senklenir; sunucu zamanı düzeltmesiyle "zamanında" kalır. Bakırköy hiç başlamaz → 03:30'da "Kaçırıldı", 03:30 şube müdürü, 05:30 bölge müdürü Murat (push + SMS), 03:30 + 24 sa merkez.
- **Beklenen:** Izgara: 23 yeşil, 1 sarı (geç senk bayrağı, zamanında), 1 kırmızı; Murat'ın sabah özetinde Bakırköy; olay günlüğünde üç eskalasyon adımı.

## S-03 · Soğuk zincir denetimi (plansız, ayda bir)

UC-15, UC-16, UC-17.

1. Deniz (A-03) gıda müfettişi gelince "Ölçüm günlüğü" → Kadıköy, buzdolabı 2, son 30 gün → PDF (3 dk). **Beklenen:** Sayfa başına zaman damgası, aralık dışı ölçümler işaretli, son sayfada doğrulama kodu.
2. Müfettiş 12 Mart'taki 6 °C kaydını sorar → Deniz denetim izinde kim/ne zaman/hangi cihaz ve aksiyonun 3 saatte kapatıldığını gösterir.

## S-04 · Personel devri ve ortak cihaz

UC-02, UC-04, UC-18.

1. Emre işten ayrılır; Ayşe onu pasifleştirir → PIN'i çalışmaz, listelerdeki cevapları ve kanıtları görünür kalır.
2. Yeni personel Zeynep davetle girer, PIN belirler; aynı tablette 5 personel dönüşümlü kullanır; 2 dk hareketsizlikte kilit.
3. 6 ay sonra Emre KVKK silme talebi gönderir → Cem "Maskele": ad "Eski personel #4821", telefon silinmiş; kayıtlar ve kanıtlar iş kaydı olarak duruyor (kişi yüzü içeren fotoğraf yoksa).

## S-05 · Prosedür değişikliği ve duyuru

UC-05, UC-14.

1. Selin "Alerjen prosedürü v2" PDF'ini duyurur; hedef tüm personel; okudum + imza gerekli.
2. 48 saatte %70 onay; onaylamayanlara otomatik hatırlatma; 4. gün %96.
3. Şablon v2 (yeni alerjen maddesi) yayınlanır; o gece eski v1 ile başlamış çalıştırmalar v1'de biter, yeni pencere v2 ile açılır.

## S-06 · Haftalık derin temizlik ve "herkes tamamlasın"

UC-06, UC-08, UC-19.

1. Plan: her pazartesi 06:00–12:00, tolerans 0, atama "istasyon sorumluları", herkes tamamlasın.
2. Ayşe pazartesi sabahı hasta personelin istasyonunu başkasına atar (UC-19).
3. İki personel aynı listede farklı maddeleri doldurur; madde bazlı kilit çakışmayı önler. **Beklenen:** Çalıştırma, tüm atananların bölümleri bitince "Tamamlandı"; eksik kalan atanan raporda görünür (puan değil, eksik).

## S-07 · Tolerans, geç gönderim ve "yapılmayacak"

UC-07, UC-08, UC-13.

1. Pencere 01:30'da kapanır; Emre 01:50'de gönderir → "Geç tamamlandı" (tolerans 2 sa).
2. Başka şubede su kesintisi: Ayşe çalıştırmayı "Yapılmayacak — su kesintisi" işaretler → eskalasyon durur, rapora "yapılmayacak (sebep)" düşer; puanlamaya girmez.
3. Üçüncü şube 03:45'te açmaya çalışır → kilitli, "Kaçırıldı" bilgisi; sonradan tamamlanamaz.

## S-08 · Yaz saati ve saat dilimi sınırı

UC-07.

- 26 Ekim gecesi (varsayımsal yaz saati geçişi) kapanış penceresi 22:00–01:30: çalıştırma tek üretilir, pencere süresi doğru hesaplanır, rapor tarihi 26 Ekim. **Beklenen:** Çift üretim yok, kaçırma yok. (Türkiye'de yaz saati uygulanmıyor; test, saat dilimi motorunun doğruluğu için başka dilimde de çalıştırılır.)

## S-09 · Yapılamadı'nın sabahı (v1 eklemeleri E-1, E-3, sabit aksiyon)

UC-08, UC-10, UC-12, UC-19. Aktörler: Emre (A-06), Zeynep (A-06), Ayşe (A-05).

1. Cumartesi 23:30 Emre kapanışta "Zemin süpürüldü ve paspaslandı" maddesini **yapılamadı: malzeme yok** (not: paspas deterjanı bitti) işaretler; fotoğraf zorunlu madde olduğu hâlde yapılamadı seçilebilir (kritik değil). **Beklenen:** aksiyon #419 (orta, 72 sa) Ayşe'ye açılır, push gider; çalıştırma "tamamlandı" (kritik yok), puan bilgi amaçlı.
2. Pazar 07:45 Zeynep açılış listesini açar. **Beklenen:** listenin başında "Dün gece" bloğu: "1 madde yapılamadı — zemin (malzeme yok)"; blok cevap istemez, liste maddesi sayılmaz (FR-0613).
3. Ayşe 08:10 "Şubem" ekranında dün geceyi görür; deterjan gelince aksiyonu **not zorunlu** olarak kapatır ("2 bidon geldi, zemin yapıldı", fotoğraf isteğe bağlı). **Beklenen:** #419 kapalı; notlar silinemez; olay günlüğünde kapanış kaydı; bölge müdürü sabah özetinde "gecikmiş aksiyon" listesinden düşer.
4. Aynı sabah Burak hastadır; Ayşe kapanışı bugün için Emre'ye verir (UC-19). Telefonu olmayan yeni personel Deniz için kioskta **PIN atar** (E-1). **Beklenen:** çalıştırma Emre'de görünür, diğerleri "Emre yapıyor" görür; Deniz PIN ile girer, ilk girişte PIN değiştirmesi istenir; her iki işlem logda (FR-0211, FR-0521).

## S-10 · Gece 23:20 kritik sıcaklık (v1 eklemesi E-6)

UC-08, UC-12, UC-13. Aktörler: Emre (A-06), Ayşe (A-05), Murat (A-04).

1. 23:20 Emre mutfak buzdolabını 6,0 °C girer (aralık 0–4, kritik). **Beklenen:** sabit kural (FR-0405): fotoğraf + not zorunlu; kaydedilince aksiyon #418 (kritik, 4 sa) Ayşe'ye; **anında push** Ayşe ve Murat'a — sessiz saat muafiyeti (FR-1008).
2. Ayşe'nin telefonu kapalıdır; 10 dk içinde teslim/okunma yok. **Beklenen:** 23:30 Ayşe'ye SMS; Murat push'u 23:20'de okudu, SMS gitmez; teslim izi olay günlüğünde.
3. Emre 23:41 gönderir. **Beklenen:** çalıştırma "başarısız (kritik madde)"; puan %87 yalnızca bilgi; kayıt kilitlenir.
4. Ayşe 08:05 aksiyonu kapatır (servis, conta değişimi). **Beklenen:** 07:00 sabah özetinde Murat ve Selin "kritik açık, vadesi geçti" görmüştü; kapanış sonrası panoda hücre "başarısız" kalır (geçmiş değişmez), aksiyon "kapalı"; çalıştırma PDF'inde olay izi 23:20 → 23:30 SMS → 08:05.
5. Aynı gece Bakırköy kapanışı hiç başlamaz. **Beklenen:** gece kimse aranmaz: 01:30 pencere + 120 dk tolerans = 03:30'da "kaçırıldı", Bakırköy şube müdürüne push (sessiz saatte yalnızca push), Murat 07:00 sabah özetinde görür; personel 03:45'te açmaya çalışırsa liste kilitli (BR-11 v1, BR-27).

## Senaryo → test eşlemesi

| Senaryo | Kabul testleri |
|---|---|
| S-01 | TC-001…TC-004, TC-017…TC-032, TC-039…TC-050, TC-057…TC-061, TC-085…TC-088 |
| S-02 | TC-033…TC-038, TC-051…TC-056, TC-073…TC-078 |
| S-03 | TC-095…TC-103 |
| S-04 | TC-005…TC-008, TC-013…TC-016, TC-104…TC-107 |
| S-05 | TC-021…TC-024, TC-079…TC-084 |
| S-06 | TC-029…TC-031, TC-047, TC-108…TC-110 |
| S-07 | TC-035…TC-038, TC-045, TC-076 |
| S-08 | TC-032 |
| S-09 | TC-013, TC-039, TC-057…TC-061, TC-108, TC-113…TC-116 |
| S-10 | TC-034, TC-036, TC-045, TC-046, TC-073, TC-078, TC-117, TC-118 |
