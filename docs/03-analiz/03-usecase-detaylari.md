# Kullanım senaryosu detayları

Biçim: amaç · aktörler · ön koşul · tetikleyici · ana akış · alternatif akışlar (A) · istisnalar (E) · son koşul · iş kuralları (BR, bkz. 04-gereksinimler/03) · gereksinimler (FR, bkz. 04-gereksinimler/01) · ekranlar (SCR, bkz. 05-tasarim/01). Numaralı adımlar geliştirici ve test için referanstır (örn. "UC-08 adım 6").

---

## UC-01 · Hesabı kur ve organizasyonu yükle

- **Amaç:** Yeni zincir hesabının bir saat içinde ilk listeyi çalıştırabilecek hâle gelmesi.
- **Aktörler:** A-01 Hesap yöneticisi (birincil); A-14 e-posta.
- **Ön koşul:** Talimatname ekibi hesabı ve ilk yönetici davetini oluşturmuş (MVP'de self-servis kayıt yok).
- **Tetikleyici:** Yönetici davet bağlantısıyla ilk kez giriş yapar.
- **Ana akış:**
  1. Yönetici şifre belirler, 2FA'yı (isteğe bağlı) açar.
  2. Kurulum sihirbazı adım 1: marka adı, saat dilimi, varsayılan çalışma saatleri, logo (isteğe bağlı).
  3. Adım 2: Excel şablonunu indirir; bölge, şube, istasyon satırlarını doldurur; yükler. Sistem doğrular (zorunlu alanlar, tekrar eden şube kodu, geçersiz saat dilimi) ve hata raporu gösterir.
  4. Adım 3: kütüphaneden 1–3 şablon seçer (örn. Kapanış — kafe); kopyalanır.
  5. Adım 4: seçilen şablon için plan önerisi gösterilir (kapanış: her gün, çalışma saatine göre pencere); yönetici onaylar veya düzenler (UC-06).
  6. Adım 5: personel Excel'i yükler veya davet bağlantısı üretir (UC-02).
  7. Sihirbaz özeti: kaç şube, kaç plan, ilk pencere ne zaman; "Yayınla".
- **Alternatif akışlar:**
  - A1 (adım 3): Yönetici Excel yerine elle 1–5 şube girer.
  - A2 (adım 4): Şablon seçmeden atlar; ızgara "plan yok" uyarısı gösterir.
- **İstisnalar:**
  - E1 (adım 3): Dosya 5 MB üstü veya format dışı → reddedilir, açıklama.
  - E2 (adım 3): %20'den fazla satır hatalı → yükleme bütün olarak reddedilir; hatalı satırlar indirilebilir raporla döner.
- **Son koşul:** Hiyerarşi, en az bir şablon ve plan kayıtlı; ilk çalıştırmalar 7 gün ileriye üretildi (UC-07).
- **BR:** BR-17, BR-18. **FR:** FR-0101…FR-0106, FR-1401…FR-1403. **SCR:** SCR-W-01, SCR-W-02.

---

## UC-02 · Personel, rol ve cihazları yönet

- **Amaç:** Yüksek personel devrinde hesap açma/kapamanın dakikalar sürmesi; ortak cihazların kayıtlı olması.
- **Aktörler:** A-01 (tüm hesap), A-05 (kendi şubesi, yalnızca personel ekleme/pasifleştirme); A-11 SMS.
- **Ön koşul:** Hiyerarşi yüklü.
- **Tetikleyici:** İşe giriş, işten ayrılma, rol değişikliği, yeni tablet.
- **Ana akış:**
  1. Yönetici "Personel" sayfasında ekle: ad, telefon, şube, istasyon(lar), rol.
  2. Sistem davet SMS'i gönderir (uygulama bağlantısı + tek kullanımlık kod).
  3. Rol ataması kapsamıyla birlikte yapılır (örn. Bölge müdürü → Bölge A).
  4. Kiosk cihazı: şube sayfasında "Cihaz ekle" → tablet uygulamada QR okutur → cihaz şubeye bağlanır, kiosk modu açılır.
  5. İşten ayrılma: "Pasifleştir" → giriş kapanır, atamaları kaldırılır, kayıtlar kalır; isteğe bağlı "kimliği maskele" (BR-22).
- **Alternatif akışlar:** A1: Toplu Excel yükleme (UC-01 adım 6 ile aynı doğrulama). A2: Şube müdürü kendi şubesine personel ekler; rol yalnızca Personel olabilir.
- **İstisnalar:** E1: Telefon numarası başka hesapta kayıtlı → aynı kişi iki hesapta çalışabilir; sistem numaraya hesap seçici sunar. E2: Davet SMS'i teslim edilemedi → panelde "iletilemedi", tekrar gönder.
- **Son koşul:** Kullanıcı giriş yapabilir; rol kapsamı ızgara ve bildirimlerde geçerli.
- **BR:** BR-19, BR-22. **FR:** FR-0107…FR-0110, FR-0201…FR-0206. **SCR:** SCR-W-02, SCR-W-03.

---

## UC-03 · Oturum aç

- **Aktörler:** Tüm insan aktörler; A-11 SMS.
- **Ana akış (personel/şube müdürü — mobil):**
  1. Telefon numarası girer → 6 haneli OTP SMS ile gelir → girer.
  2. İlk girişte KVKK aydınlatma metni gösterilir; "Okudum" onayı zaman damgasıyla kaydedilir (UC-18 için temel).
  3. Konum izni ayrı ekranda, gerekçesiyle istenir (yalnızca görev anında); reddedilebilir.
  4. Oturum cihazda 30 gün açık kalır (yenilenen token).
- **Ana akış (yönetici — web):** e-posta + şifre; 2FA açıksa TOTP; 12 saat oturum.
- **Alternatif:** A1: OTP gelmedi → 60 sn sonra tekrar gönder; 3 denemede 15 dk blok.
- **İstisnalar:** E1: Pasif kullanıcı → "Hesabınız kapalı, yöneticinize başvurun".
- **BR:** BR-15. **FR:** FR-0201…FR-0204, FR-1301. **SCR:** SCR-M-01, SCR-W-00.

---

## UC-04 · Ortak cihazda PIN ile geçiş yap

- **Amaç:** Tek tablette birden çok personelin ayrı ayrı kanıt bırakması.
- **Ön koşul:** Cihaz kiosk modunda kayıtlı (UC-02 adım 4); personelin PIN'i tanımlı (ilk girişte kendisi belirler).
- **Ana akış:**
  1. Kilit ekranında şube personel listesi (ad ve baş harf avatarı) görünür.
  2. Personel adına dokunur, 4 haneli PIN girer.
  3. Bugün ekranı o kişi adına açılır; sağ üstte "Değiştir" ile başka kişi geçer.
  4. 2 dk hareketsizlikte kilit ekranına döner (BR-19); tamamlanmamış madde cevapları yerelde korunur.
- **Alternatif:** A1: PIN unutuldu → şube müdürü kendi PIN'iyle sıfırlar; olay logda.
- **İstisnalar:** E1: 5 yanlış PIN → 1 dk blok; 3 blok → şube müdürüne bildirim.
- **Son koşul:** Her cevap ve kanıt PIN sahibine, cihaz kimliğiyle birlikte yazılır.
- **BR:** BR-19. **FR:** FR-0207…FR-0210. **SCR:** SCR-M-02.

---

## UC-05 · Şablon tasarla ve yayınla

- **Aktörler:** A-02 (birincil), A-03.
- **Ana akış:**
  1. Şablon listesi → "Yeni" veya kütüphaneden kopyala (30 Türkçe yeme-içme şablonu).
  2. Editör: bölümler ve maddeler; her madde için tür (onay, çoktan seçmeli, sayı+birim, sıcaklık, metin, fotoğraf, video, imza, barkod/QR, tarih-saat, talimat) ve ayarlar (zorunlu, kanıt zorunlu, ağırlık, kritik, ipucu, istasyon bağı).
  3. Sıcaklık maddesi: kabul aralığı (min–maks); aralık dışı → otomatik "başarısız" (BR-08).
  4. Koşullu mantık: (madde, cevap) → eylemler (ek soru, not iste, fotoğraf iste, aksiyon oluştur [atanan kuralı, öncelik], bildir [rol], bölüm atla).
  5. Puanlama: ağırlıklar, başarı eşiği (varsayılan %90), kritik madde kuralı.
  6. Şablon ayarları: yalnızca kamera, yapılamadı izinli mi, tolerans varsayılanı, sebep seti.
  7. Önizleme (mobil görünüm) → "Yayınla" (hemen / tarihli). Yeni sürüm oluşur; eski sürüm salt okunur, geçmiş çalıştırmalar ona bağlı kalır (BR-18).
- **Alternatif:** A1: SOP/PDF yükle → taslak madde listesi (CAP-15, Should); yönetici düzenlemeden yayınlayamaz. A2: Şube türüne göre varyant (Should).
- **İstisnalar:** E1: Kritik işaretli madde "yapılamadı izinli" ise → çelişki uyarısı, yayın engellenir.
- **Son koşul:** Şablon sürümü yayında; planlar yeni sürümü bir sonraki üretimden itibaren kullanır (başlanmış çalıştırmalar eski sürümde).
- **BR:** BR-06, BR-07, BR-08, BR-09, BR-14, BR-18. **FR:** FR-0301…FR-0312, FR-0401…FR-0404. **SCR:** SCR-W-04, SCR-W-05.

---

## UC-06 · Plan tanımla

- **Aktörler:** A-02 (birincil); A-04 kendi bölgesi için.
- **Ana akış:**
  1. Plan listesi → "Yeni plan": şablon sürümü seç.
  2. Kapsam: şubeler (hiyerarşi ağacı, akıllı grup veya tek tek).
  3. Tekrar: günlük (saat listesi), her N saat, haftanın günleri, aylık; bitiş tarihi (isteğe bağlı). Arka planda RRULE.
  4. Pencere: başlangıç/bitiş saati (şube saat diliminde); gece yarısını aşan pencere açılış gününe yazılır (BR-01); tolerans (BR-02); "çalışma saatlerinden türet" seçeneği.
  5. Atama: rol / kişi / grup / istasyon; "biri tamamlasın" veya "herkes tamamlasın" (BR-16).
  6. Hatırlatma: açılışta, bitişe 30 dk kala, bitişte; kanal (push; kritik listede SMS).
  7. Eskalasyon merdiveni: varsayılan (BR-11) veya özel adımlar.
  8. Önizleme: önümüzdeki 7 günün çalıştırma takvimi (tatil günleri düşülmüş) → Kaydet.
- **Alternatif:** A1: Tek seferlik liste (tarih + son saat + hedef şubeler). A2: Vardiya bazlı tekrar (Should).
- **İstisnalar:** E1: Pencere süresi tolerans dahil 24 saati aşıyor → uyarı. E2: Aynı şube-şablon-pencere için çakışan plan → engellenir.
- **Son koşul:** Plan aktif; UC-07 çalıştırmaları üretir.
- **BR:** BR-01, BR-02, BR-11, BR-16, BR-17. **FR:** FR-0501…FR-0512. **SCR:** SCR-W-06.

---

## UC-07 · Çalıştırmaları üret ve hatırlat (sistem)

- **Aktör:** A-08 Zamanlayıcı; A-10, A-11.
- **Ana akış:**
  1. Her saat başı: tüm aktif planlar için 7 gün ileriye kadar üretilmemiş pencereler hesaplanır (RRULE, şube saat dilimi, kapalı gün takvimi) → "Planlandı" çalıştırmaları oluşturulur (BR-17, BR-18).
  2. Pencere başlangıcında durum "Açık"; atananlara "açılış" bildirimi.
  3. Bitişe 30 dk kala tamamlanmamışsa hatırlatma; bitişte "pencere kapandı" bildirimi.
  4. Tolerans sonunda tamamlanmamış çalıştırma "Kaçırıldı" (BR-03) → UC-13 eskalasyon.
- **Alternatif:** A1: Plan değiştiğinde gelecekteki "Planlandı" çalıştırmalar yeniden hesaplanır; "Açık/Devam" olanlar korunur.
- **İstisnalar:** E1: Push teslim edilemedi (token geçersiz) → teslimat izine yazılır; kritik listede SMS'e düşer (BR-23).
- **Son koşul:** Her pencere için tek çalıştırma; bildirim teslimat izi kayıtlı.
- **BR:** BR-01, BR-02, BR-03, BR-17, BR-23. **FR:** FR-0513…FR-0518, FR-1001…FR-1006.

---

## UC-08 · Listeyi tamamla ve kanıt yükle

- **Aktör:** A-06 Personel (A-05 de tamamlayabilir); A-13 depolama.
- **Ön koşul:** Çalıştırma "Açık"; kullanıcı atanmış (veya şubede atama serbest).
- **Ana akış:**
  1. Bugün ekranında çalıştırmaya dokunur; ilerleme çubuğu ve pencere geri sayımı görünür.
  2. Maddeleri sırayla cevaplar; onay maddeleri tek dokunuş; sayı/sıcaklık sayısal klavye; çoktan seçmeli büyük düğmeler.
  3. Fotoğraf zorunlu maddede kamera açılır (yalnızca kamera ayarı varsa galeri yok — BR-14); 1–5 fotoğraf; cihazda ~300 KB'a sıkıştırılır; sunucu zamanı ve konum (izin varsa) damgalanır (BR-13, BR-15).
  4. Koşullu mantık tetiklenirse ek soru/not/fotoğraf istenir; aksiyon otomatik oluşur (BR-10).
  5. Maddeyi yapamıyorsa "Yapılamadı" (UC-10).
  6. Tüm zorunlu maddeler cevaplanınca "Gönder" aktif olur (BR-05); gönderim puanı hesaplar (BR-06, BR-07), durum "Tamamlandı" veya "Geç tamamlandı" (BR-02).
  7. Gönderim sonrası salt okunur; düzeltme "ek" kaydıyla (BR-12).
- **Alternatif:** A1: Birden çok kişi aynı listede ("herkes tamamlasın" veya iş bölümü): madde bazlı kilit; son yazan kazanır (BR-24). A2: Kaldığı yerden devam (uygulama kapanmış). A3: QR ile istasyondan başlatma (Should).
- **İstisnalar:** E1: Kamera izni yok → izin ekranı; izin verilmezse madde tamamlanamaz, açıklama. E2: Pencere kapandı, tolerans içinde → devam edebilir, "geç" işareti; tolerans bitti → düzenleme kilitlenir (BR-03). E3: Depolama alanı yok → uyarı, kuyruk beklemede.
- **Son koşul:** Cevaplar ve kanıtlar sunucuda; puan ve durum hesaplı; olay günlüğünde kayıt.
- **BR:** BR-02, BR-03, BR-05, BR-06, BR-07, BR-08, BR-10, BR-12, BR-13, BR-14, BR-15, BR-24. **FR:** FR-0601…FR-0612. **SCR:** SCR-M-03, SCR-M-04, SCR-M-05.

---

## UC-09 · Çevrimdışı tamamla ve senkronize et

- **Ana akış:**
  1. Uygulama açılışta önümüzdeki 48 saatin çalıştırmalarını ve şablon sürümlerini önbelleğe alır.
  2. Bağlantı yokken UC-08 aynen çalışır; cevaplar ve kanıtlar yerel kuyrukta (SQLite + dosya), ekranda "gönderildi (bekliyor)" rozeti.
  3. Bağlantı gelince arka planda senk: önce cevaplar, sonra kanıt dosyaları; sunucu, cihaz zaman farkını hesaplar ve düzeltilmiş zamanı yazar, ham değeri logda tutar (BR-13).
  4. Çakışma: madde bazlı son yazan kazanır; kanıt asla silinmez (BR-24).
- **İstisnalar:** E1: 72 saatten eski kuyruk → yine senklenir, "geç senk" bayrağıyla. E2: Kuyruk 500 kanıtı aştı → yeni fotoğraf engellenir, uyarı. E3: Senk sırasında uygulama kapatıldı → kaldığı yerden devam (idempotent yükleme).
- **Son koşul:** Sunucu ve cihaz tutarlı; teslimat ve senk günlüğü destek için görünür.
- **BR:** BR-13, BR-24. **FR:** FR-0701…FR-0708. **SCR:** SCR-M-04 (rozet), SCR-M-11 (senk durumu).

---

## UC-10 · Yapılamadı bildir

- **Ana akış:**
  1. Madde ekranında "Yapılamadı" → sebep seti (malzeme yok, ekipman arızalı, zaman yetmedi, yetkim yok, diğer) (BR-09).
  2. "Diğer" seçilirse not zorunlu; isteğe bağlı fotoğraf.
  3. Kaydet → madde "yapılamadı" olarak işaretlenir; puanı düşürür; aksiyon otomatik açılır (atanan: şube müdürü; vade: öncelik kuralı — BR-10).
  4. Şube müdürü aksiyonu görür; sebebi doğrular veya reddeder (yorumla).
- **Alternatif:** A1: Şablon kritik maddede "yapılamadı"yı kapatmışsa düğme görünmez; madde atlanamaz.
- **Son koşul:** Aksiyon açık; olay logda; "yapılamadı" sebepleri raporda (R-3).
- **BR:** BR-09, BR-10. **FR:** FR-0801…FR-0805. **SCR:** SCR-M-06.

---

## UC-11 · Sorun bildir

- **Ana akış:**
  1. Bugün ekranından "Sorun bildir": kategori (ekipman, tedarik, hijyen, güvenlik, diğer), istasyon, fotoğraf, not.
  2. Kayıt şube müdürüne düşer (push); şube müdürü aksiyona çevirir veya kapatır (sebep).
- **Alternatif:** A1: Şube müdürü sorunu bölge müdürüne yükseltir.
- **BR:** BR-10. **FR:** FR-0806…FR-0809. **SCR:** SCR-M-07.

---

## UC-12 · Aksiyonu yönet ve kapat

- **Aktörler:** A-05, A-04 (birincil); A-06 kapanış kanıtı yükleyebilir; A-02.
- **Ana akış:**
  1. "Aksiyonlarım" listesi (bana atananlar, şubem, gecikmişler) filtreleriyle.
  2. Aksiyon kartı: kaynak (madde/sorun/elle), şube-istasyon, öncelik, vade, durum, yorum dizisi.
  3. Durum geçişleri: açık → devam → kapatma bekliyor → kapalı / reddedildi. Kapatırken fotoğraf/not (BR-10).
  4. Şablon "onaylı kapanış" isterse bölge müdürü onaylar (Should).
  5. Elle aksiyon oluşturma: başlık, şube, atanan, vade, öncelik.
- **İstisnalar:** E1: Toplu kapatma yok; her aksiyon tek tek kanıtla kapanır.
- **BR:** BR-10, BR-11. **FR:** FR-0901…FR-0910. **SCR:** SCR-M-08, SCR-W-09.

---

## UC-13 · Eskalasyonu yürüt (sistem)

- **Ana akış:**
  1. Tetik: çalıştırma "Kaçırıldı" veya aksiyon vadesi geçti.
  2. Merdiven (BR-11): 0. adım şube müdürü (push); +2 saat bölge müdürü (push + SMS kritikse); +24 saat merkez (operasyon müdürü).
  3. Her adım olay günlüğüne ve aksiyon yorum dizisine yazılır.
  4. Şube müdürü çalıştırmayı "yapılmayacak + sebep" işaretlerse (BR-04) merdiven durur.
- **İstisnalar:** E1: Alıcı pasif/atanmamış → bir üst halkaya geçer, logda "alıcı yok".
- **BR:** BR-04, BR-11, BR-23. **FR:** FR-0911…FR-0915, FR-1007.

---

## UC-14 · Duyuru yayınla ve onay topla

- **Ana akış:**
  1. Duyuru: başlık, metin, görsel/PDF; hedef (hesap, bölge, şube, rol, akıllı grup); yayın zamanı; "okudum onayı gerekli" ve "imza gerekli" (Should).
  2. Hedef kullanıcılarda duyuru "onay bekliyor" ile açılır; "Okudum ve anladım" zaman damgalı.
  3. Panelde onay oranı ve onaylamayan listesi; 48 saat sonra otomatik hatırlatma (BR-25).
- **Alternatif:** A1: Duyuru bir şablon sürümüne bağlanır; onaylamayana liste açılmaz (Should).
- **BR:** BR-25. **FR:** FR-1101…FR-1106. **SCR:** SCR-M-09, SCR-W-10.

---

## UC-15 · Operasyonu izle ve raporla

- **Ana akış:**
  1. Operasyon panosu: bugün şube × liste ızgarası (tamamlandı / geç / devam / kaçırıldı / kapalı / planlı); canlı.
  2. Hücreye tıkla → çalıştırma detayı: maddeler, cevaplar, kanıt küçük resimleri, damga bilgisi, olay izi.
  3. Raporlar: tamamlanma ve zamanındalık (şube/bölge/liste/dönem, trend, şube sıralaması); başarısız madde analizi (ilk 10, ısı haritası, yapılamadı sebepleri); ölçüm günlüğü (ekipman zaman serisi, aralık dışı); aksiyon raporu (açık/gecikmiş, ortalama kapanış).
  4. Kanıt galerisi: filtreler (şube, istasyon, madde, tarih), tam boy görüntüleme.
  5. Kişi düzeyi: yalnızca şube/bölge müdürüne, gecikme/eksik listesi; puan ve sıralama yok (BR-20).
- **Alternatif:** A1: Yönetici mobil görünümü (özet ızgara, aksiyon kapatma, kanıt). A2: Planlı e-posta özeti (Should).
- **BR:** BR-20. **FR:** FR-1201…FR-1212. **SCR:** SCR-W-07, SCR-W-08, SCR-W-11, SCR-M-10.

---

## UC-16 · Denetim kaydını ve kanıtı dışa aktar

- **Ana akış:**
  1. Çalıştırma detayından "PDF" → markalı rapor (maddeler, cevaplar, kanıt küçük resimleri, imzalar, zaman damgaları, denetim izi özeti ve doğrulama kodu).
  2. Dönem raporu: şube + şablon + tarih aralığı → PDF (örn. 30 günlük soğuk zincir); Excel ham veri.
  3. Süreli paylaşım bağlantısı (7 gün) — denetçiye e-posta.
- **İstisnalar:** E1: 500 çalıştırmadan büyük dönem → arka planda üretilir, hazır olunca bildirim.
- **FR:** FR-1213…FR-1218. **SCR:** SCR-W-08, SCR-W-11.

---

## UC-17 · Denetim izini görüntüle ve doğrula

- **Ana akış:**
  1. Çalıştırma veya aksiyon üzerinde "Denetim izi": kim, ne zaman, nereden (IP/cihaz), ne (olay), önce/sonra özeti.
  2. Doğrulama: günlük kök özeti ve dış zaman damgası (RFC 3161) gösterilir; PDF'teki doğrulama kodu bu zincire bağlanır.
- **FR:** FR-1301…FR-1306. **SCR:** SCR-W-12.

---

## UC-18 · KVKK talebini işle

- **Ana akış:**
  1. Hesap yöneticisi "Kişisel veri talepleri": kişi seç → "Dışa aktar" (JSON + kanıt dosyaları ZIP) veya "Sil/Maskele".
  2. Silme: kimlik alanları maskelenir, kanıt dosyaları kişisel içerik taşıyorsa silinir, işletme kaydı (madde cevabı, zaman) anonim kalır (BR-21, BR-22).
  3. Saklama politikası: hesap düzeyinde süre (varsayılan 24 ay); süresi dolan kanıtlar zamanlayıcı ile silinir, özet log kalır.
- **FR:** FR-1307…FR-1312. **SCR:** SCR-W-13.

---

## UC-19 · Günün listelerini ata (yeniden atama)

- **Aktör:** A-05 Şube müdürü.
- **Ana akış:**
  1. Bugün (yönetici görünümü): şubenin bugünkü çalıştırmaları ve varsayılan atananlar.
  2. Çalıştırmaya dokun → atananı değiştir (vardiyadaki personelden seç); "herkes tamamlasın" listelerinde kişi ekle/çıkar.
  3. Değişiklik anında push ile yeni atanana gider; olay logda.
- **BR:** BR-16. **FR:** FR-0519, FR-0520. **SCR:** SCR-M-10, SCR-W-07.

---

## UC-20 · Çalıştırmayı gözden geçir ve onayla (Should)

- **Ana akış:**
  1. Bölge müdürü veya kalite, tamamlanmış çalıştırmayı açar; "Gözden geçirildi" işareti ve not; ikinci imza (isteğe bağlı).
  2. Kanıt fotoğrafı üzerinde yorum (annotation v1.x).
- **FR:** FR-1701…FR-1703. **SCR:** SCR-W-08, SCR-M-10.
